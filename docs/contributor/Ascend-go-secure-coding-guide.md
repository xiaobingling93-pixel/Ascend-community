# 昇腾社区 Go 语言安全编程指导（建议稿）

<!-- TOC -->

- [说明](#说明)
- [约定](#约定)
- [例外](#例外)
- [适用范围](#适用范围)
    - [安全编码](#1-安全编码)
        - [总体规则](#11-总体规则)
        - [输入验证](#12-输入验证)
        - [表达式与语句](#13-表达式与语句)
        - [资源管理](#14-资源管理)
        - [错误处理](#15-错误处理)
        - [标准库](#16-标准库)
        - [并发安全](#17-并发安全)
        - [内存](#18-内存)
        - [文件](#19-文件)
        - [网络](#110-网络)
        - [加密与随机数](#111-加密与随机数)

<!-- /TOC -->

## 说明

本指导基于Go语言制定而成，给参与Ascend开源社区项目的开发者提供安全编程指导。

规则并不是完美的，通过禁止在特定情况下有用的特性，可能会对代码实现造成影响。但是我们制定规则的目的是"为了大多数程序员可以得到更多的好处"。

参考本指导之前，希望您具有相应的Go语言基础能力，而不是通过该文档来学习Go语言。

1. 了解Go语言的语法和特性；
2. 熟知Go语言的基本语言特性，包括Go 1.x相关特性；
3. 了解Go语言的标准库；

如果希望改进某个规则，建议提交Issue并说明理由，经Ascend运营团队评审后可接纳并修改生效。

## 约定

**规则**：编程时必须遵守的约定(must)

**建议**：编程时应该遵守的约定(should)

本指导适用Go 1.x版本，如果没有特定的版本要求，适用所有Go 1.x版本。

## 例外

无论是'规则'还是'建议'，都必须理解该条目这么规定的原因，并努力遵守。
但是，有些规则和建议可能会有例外。

在不违背总体原则，经过充分考虑，有充足的理由的前提下，可以适当违背本指导中约定。
例外破坏了代码的一致性，请尽量避免。'规则'的例外应该是极少的。 

## 适用范围

Ascend 社区所有开源仓

---

### 1. 安全编码

#### 1.1 总体规则

##### 规则 1.1.1 保证类型安全

Go语言是静态类型语言，应该充分利用类型系统来保证类型安全。避免不必要的类型转换和类型断言。

```go
// Good
func ProcessInt(value int) {
    // ...
}

// Bad
func ProcessInt(value interface{}) {
    intValue := value.(int)  // 不安全的类型断言
    // ...
}
```

##### 规则 1.1.2 避免使用unsafe包

除非有充分的理由，否则应该避免使用`unsafe`包。使用`unsafe`包会破坏类型安全，可能导致内存安全问题。

```go
// Good
func CopySlice(dst, src []byte) {
    copy(dst, src)
}

// Bad
import "unsafe"

func CopySlice(dst, src []byte) {
    // 使用unsafe可能导致内存安全问题
    unsafe.Copy(unsafe.Pointer(&dst[0]), unsafe.Pointer(&src[0]), len(src))
}
```

##### 规则 1.1.3 禁止使用未定义行为

遵循Go语言规范，禁止使用规范中未定义的行为。对于编译器实现的特性或者扩展特性也需要谨慎使用，这些特性会降低代码的可移植性。

#### 1.2 输入验证

##### 规则 1.2.1 对所有外部输入进行验证和清理

所有来自外部的输入（用户输入、网络数据、文件内容、环境变量等）都必须进行验证和清理。

```go
// Good
func ProcessUserInput(input string) error {
    // 验证输入长度
    if len(input) > MaxInputLength {
        return errors.New("input too long")
    }
    
    // 验证输入格式
    if !isValidFormat(input) {
        return errors.New("invalid input format")
    }
    
    // 清理输入（去除危险字符等）
    cleaned := sanitizeInput(input)
    
    // 处理清理后的输入
    return process(cleaned)
}

// Bad
func ProcessUserInput(input string) error {
    // 直接使用未验证的输入
    return process(input)
}
```

##### 规则 1.2.2 外部数据作为数组索引或切片操作时必须校验边界

```go
// Good
func GetElement(slice []int, index int) (int, error) {
    if index < 0 || index >= len(slice) {
        return 0, errors.New("index out of range")
    }
    return slice[index], nil
}

// Bad
func GetElement(slice []int, index int) int {
    return slice[index]  // 可能导致panic
}
```

##### 规则 1.2.3 禁止直接使用外部数据拼接SQL命令

必须使用参数化查询或预编译语句，防止SQL注入攻击。

```go
// Good
func GetUser(db *sql.DB, id int) (*User, error) {
    var user User
    err := db.QueryRow("SELECT id, name, email FROM users WHERE id = ?", id).Scan(
        &user.ID, &user.Name, &user.Email)
    return &user, err
}

// Bad
func GetUser(db *sql.DB, id string) (*User, error) {
    query := fmt.Sprintf("SELECT * FROM users WHERE id = %s", id)  // SQL注入风险
    // ...
}
```

##### 规则 1.2.4 禁止直接使用外部数据构造命令执行

禁止直接使用外部数据构造系统命令，防止命令注入攻击。

```go
// Good
func ExecuteCommand(cmd string, args []string) error {
    execCmd := exec.Command(cmd, args...)
    return execCmd.Run()
}

// Bad
func ExecuteCommand(userInput string) error {
    cmd := exec.Command("sh", "-c", userInput)  // 命令注入风险
    return cmd.Run()
}
```

#### 1.3 表达式与语句

##### 规则 1.3.1 确保整数运算不溢出

对于可能来自外部数据的整数运算，需要确保不会导致溢出。

```go
// Good
func SafeAdd(a, b int) (int, error) {
    if a > 0 && b > math.MaxInt-a {
        return 0, errors.New("integer overflow")
    }
    if a < 0 && b < math.MinInt-a {
        return 0, errors.New("integer underflow")
    }
    return a + b, nil
}

// Bad
func UnsafeAdd(a, b int) int {
    return a + b  // 可能溢出
}
```

##### 规则 1.3.2 确保除法和取余运算不会导致除零错误

```go
// Good
func SafeDivide(a, b int) (int, error) {
    if b == 0 {
        return 0, errors.New("division by zero")
    }
    return a / b, nil
}

// Bad
func UnsafeDivide(a, b int) int {
    return a / b  // 除零会导致panic
}
```

##### 规则 1.3.3 &&和||操作符的右侧操作数不要包含副作用

逻辑与（&&）、逻辑或（||）表达式中的右操作数是否被求值，取决于左操作数的求值结果。如果右操作数包含副作用，则不能确定是否确实发生了副作用。

```go
// Good
if isValid && processData() {
    // processData只在isValid为true时调用
}

// Bad
if isValid && (count++ > 0) {
    // count++的副作用不确定是否发生
}
```

##### 规则 1.3.4 循环必须安全退出

在应用程序中，一个重复提供服务的逻辑循环应当设计退出机制，并且将资源正确释放后安全退出。

```go
// Good
func ProcessLoop(ctx context.Context) {
    for {
        select {
        case <-ctx.Done():
            return
        case data := <-dataChan:
            process(data)
        }
    }
}

// Bad
func ProcessLoop() {
    for {
        process(data)  // 无法退出
    }
}
```

#### 1.4 资源管理

##### 规则 1.4.1 禁止将局部变量的地址传递到其作用域外

```go
// Good
func GetValue() int {
    value := 42
    return value
}

// Bad
func GetPointer() *int {
    value := 42
    return &value  // 返回局部变量的地址，危险
}
```

##### 规则 1.4.2 禁止解引用空指针

解引用空指针会导致运行时panic，在使用指针前必须检查是否为nil。

```go
// Good
func ProcessUser(user *User) error {
    if user == nil {
        return errors.New("user is nil")
    }
    return user.Process()
}

// Bad
func ProcessUser(user *User) error {
    return user.Process()  // 如果user为nil，会导致panic
}
```

##### 规则 1.4.3 禁止对nil接口调用方法

对nil接口调用方法会导致运行时panic，在使用接口前必须检查是否为nil。

```go
// Good
func ProcessWriter(w io.Writer) error {
    if w == nil {
        return errors.New("writer is nil")
    }
    _, err := w.Write([]byte("data"))
    return err
}

// Bad
func ProcessWriter(w io.Writer) error {
    _, err := w.Write([]byte("data"))  // 如果w为nil，会导致panic
    return err
}
```

##### 规则 1.4.4 切片和map操作前必须检查nil

虽然对nil切片进行某些操作（如range）不会panic，但可能导致逻辑错误。对nil map进行操作会导致panic。

```go
// Good
func ProcessSlice(s []int) {
    if s == nil {
        return
    }
    // 处理切片
}

func ProcessMap(m map[string]int) {
    if m == nil {
        return
    }
    // 处理map
}

// Bad
func ProcessSlice(s []int) {
    for i := range s {  // 如果s为nil，虽然不会panic，但逻辑可能不正确
        // ...
    }
}

func ProcessMap(m map[string]int) {
    value := m["key"]  // 如果m为nil，会导致panic
}
```

##### 规则 1.4.5 禁止对nil channel进行操作

对nil channel进行发送、接收或关闭操作会导致运行时panic或永久阻塞。

```go
// Good
func SendData(ch chan<- int, data int) error {
    if ch == nil {
        return errors.New("channel is nil")
    }
    ch <- data
    return nil
}

func CloseChannel(ch chan int) error {
    if ch == nil {
        return errors.New("channel is nil")
    }
    close(ch)
    return nil
}

// Bad
func SendData(ch chan<- int, data int) {
    ch <- data  // 如果ch为nil，会导致永久阻塞
}

func CloseChannel(ch chan int) {
    close(ch)  // 如果ch为nil，会导致panic
}
```

##### 规则 1.4.6 禁止对nil函数类型进行调用

对nil函数类型进行调用会导致运行时panic。

```go
// Good
type Handler func() error

func ExecuteHandler(h Handler) error {
    if h == nil {
        return errors.New("handler is nil")
    }
    return h()
}

// Bad
type Handler func() error

func ExecuteHandler(h Handler) error {
    return h()  // 如果h为nil，会导致panic
}
```

#### 1.5 错误处理

##### 规则 1.5.1 错误信息不应泄露敏感信息

错误信息应该提供有用的上下文，但不应该泄露敏感信息（如密码、密钥、内部路径等）。

```go
// Good
if err != nil {
    return fmt.Errorf("authentication failed")
}

// Bad
if err != nil {
    return fmt.Errorf("authentication failed: password %s is incorrect", password)
}
```

##### 规则 1.5.2 使用errors.Is和errors.As进行错误检查

使用`errors.Is`和`errors.As`来检查和处理特定类型的错误，而不是直接比较错误值。

```go
// Good
if errors.Is(err, os.ErrNotExist) {
    // 处理文件不存在的情况
}

var pathErr *os.PathError
if errors.As(err, &pathErr) {
    // 处理路径错误
}

// Bad
if err == os.ErrNotExist {  // 可能无法匹配包装的错误
    // ...
}
```

#### 1.6 标准库

##### 规则 1.6.1 调用格式化函数时，禁止format参数受外部数据控制

```go
// Good
log.Printf("User %s logged in", sanitize(username))

// Bad
format := userInput  // 来自外部输入
log.Printf(format, username)  // 格式化字符串注入风险
```

##### 规则 1.6.2 使用strings包进行字符串操作，避免手动操作字节

```go
// Good
if strings.Contains(str, substr) {
    // ...
}

// Bad
if bytes.Contains([]byte(str), []byte(substr)) {  // 对于字符串，应该使用strings包
    // ...
}
```

##### 规则 1.6.3 禁止使用os.Exit和log.Fatal（除了main函数）

使用`os.Exit`和`log.Fatal`会立即终止程序，导致defer函数无法执行，资源无法正确释放。

```go
// Good
func Process() error {
    if err := doSomething(); err != nil {
        return err  // 返回错误，让调用者处理
    }
    return nil
}

// Bad
func Process() {
    if err := doSomething(); err != nil {
        log.Fatal(err)  // 立即退出，defer不会执行
    }
}
```

#### 1.7 并发安全

##### 规则 1.7.1 共享资源访问必须使用同步机制

多个goroutine访问共享资源时，必须使用mutex、channel等同步机制，避免数据竞争。

```go
// Good
type SafeCounter struct {
    mu    sync.RWMutex
    count int
}

func (c *SafeCounter) Increment() {
    c.mu.Lock()
    defer c.mu.Unlock()
    c.count++
}

func (c *SafeCounter) Get() int {
    c.mu.RLock()
    defer c.mu.RUnlock()
    return c.count
}

// Bad
type UnsafeCounter struct {
    count int
}

func (c *UnsafeCounter) Increment() {
    c.count++  // 并发不安全，存在数据竞争
}
```

##### 规则 1.7.2 尽量缩短在临界区内停留的时间

在持有锁的情况下，应尽量减少执行时间，以提高程序的并发性能。长时间持有锁可能导致其他goroutine长时间等待，降低系统吞吐量。

```go
// Good
func (c *Counter) Process(data []byte) error {
    // 在临界区外进行耗时操作
    processed := expensiveOperation(data)
    
    // 只在必要时进入临界区
    c.mu.Lock()
    c.count += len(processed)
    c.mu.Unlock()
    
    return nil
}

// Bad
func (c *Counter) Process(data []byte) error {
    c.mu.Lock()
    defer c.mu.Unlock()
    
    // 在临界区内进行耗时操作，会阻塞其他goroutine
    processed := expensiveOperation(data)
    c.count += len(processed)
    
    return nil
}
```

##### 规则 1.7.3 避免goroutine被永久阻塞

确保goroutine能够正常退出，避免因channel未关闭、死锁等原因导致goroutine永久阻塞。

```go
// Good
func ProcessWithTimeout(ctx context.Context, ch <-chan int) error {
    for {
        select {
        case <-ctx.Done():
            return ctx.Err()
        case data, ok := <-ch:
            if !ok {
                return nil  // channel已关闭，正常退出
            }
            process(data)
        }
    }
}

// Bad
func Process(ch <-chan int) {
    for {
        data := <-ch  // 如果channel未关闭且没有发送者，会永久阻塞
        process(data)
    }
}
```

##### 规则 1.7.4 使用带超时的channel操作

对channel操作设置超时，避免goroutine永久阻塞。

```go
// Good
func SendWithTimeout(ch chan<- int, data int, timeout time.Duration) error {
    select {
    case ch <- data:
        return nil
    case <-time.After(timeout):
        return errors.New("send timeout")
    }
}

func ReceiveWithTimeout(ch <-chan int, timeout time.Duration) (int, error) {
    select {
    case data := <-ch:
        return data, nil
    case <-time.After(timeout):
        return 0, errors.New("receive timeout")
    }
}

// Bad
func Send(ch chan<- int, data int) {
    ch <- data  // 如果channel已满且没有接收者，会永久阻塞
}
```

##### 规则 1.7.5 避免死锁

确保锁的获取顺序一致，避免多个goroutine相互等待导致死锁。

```go
// Good
func Transfer(from, to *Account, amount int) error {
    // 使用一致的锁获取顺序（按地址排序）
    first, second := from, to
    if uintptr(unsafe.Pointer(from)) > uintptr(unsafe.Pointer(to)) {
        first, second = to, from
    }
    
    first.mu.Lock()
    defer first.mu.Unlock()
    second.mu.Lock()
    defer second.mu.Unlock()
    
    // 执行转账操作
    return nil
}

// Bad
func Transfer(from, to *Account, amount int) error {
    from.mu.Lock()
    to.mu.Lock()  // 如果另一个goroutine同时执行反向转账，可能导致死锁
    defer from.mu.Unlock()
    defer to.mu.Unlock()
    
    // 执行转账操作
    return nil
}
```

##### 规则 1.7.6 使用context控制goroutine生命周期

使用context来控制和取消goroutine，避免goroutine泄漏。

```go
// Good
func Worker(ctx context.Context, jobs <-chan Job) {
    for {
        select {
        case <-ctx.Done():
            return  // 收到取消信号，退出goroutine
        case job, ok := <-jobs:
            if !ok {
                return  // channel已关闭，退出goroutine
            }
            processJob(job)
        }
    }
}

// Bad
func Worker(jobs <-chan Job) {
    for job := range jobs {
        processJob(job)  // 如果context被取消，无法退出
    }
}
```

#### 1.8 内存

##### 规则 1.8.1 严禁使用string类型存储敏感信息

string类型在Go中是不可变的，敏感信息（如密码、密钥）存储在string中后，无法安全地清除。应该使用`[]byte`并在使用后清零。

```go
// Good
func VerifyPassword(password []byte) bool {
    // 验证密码
    // 使用后清零
    for i := range password {
        password[i] = 0
    }
    return true
}

// Bad
func VerifyPassword(password string) bool {
    // string是不可变的，无法清零
    // 敏感信息可能残留在内存中
    return true
}
```

##### 规则 1.8.2 内存中的敏感信息使用完毕后立即清零

口令、密钥等敏感信息使用完毕后立即清零，避免被攻击者获取。

```go
// Good
func ProcessSensitiveData(data []byte) {
    // 处理敏感数据
    process(data)
    
    // 使用后清零
    for i := range data {
        data[i] = 0
    }
}

// Bad
func ProcessSensitiveData(data []byte) {
    // 处理敏感数据
    process(data)
    // 没有清零，敏感信息残留在内存中
}
```

##### 规则 1.8.3 避免在日志中输出敏感信息

不要在日志、错误消息中输出敏感信息（密码、密钥、令牌等）。

```go
// Good
log.Printf("User authentication failed for user ID: %d", userID)

// Bad
log.Printf("User authentication failed: password %s is incorrect", password)
```

#### 1.9 文件

##### 规则 1.9.1 外部文件路径使用前必须进行规范化并校验

当文件路径来自外部数据时，需要先将文件路径规范化，如果没有作规范化处理，攻击者就有机会通过恶意构造文件路径进行文件的越权访问。

```go
// Good
func ReadFile(userInput string) ([]byte, error) {
    // 规范化路径
    cleanPath := filepath.Clean(userInput)
    absPath, err := filepath.Abs(cleanPath)
    if err != nil {
        return nil, err
    }
    
    // 验证路径是否在允许的目录下
    baseDir := "/allowed/directory"
    if !strings.HasPrefix(absPath, baseDir) {
        return nil, errors.New("invalid file path")
    }
    
    return ioutil.ReadFile(absPath)
}

// Bad
func ReadFile(userInput string) ([]byte, error) {
    return ioutil.ReadFile(userInput)  // 路径遍历风险
}
```

##### 规则 1.9.2 不要在共享目录中创建临时文件

程序的临时文件应当是程序自身独享的，任何将自身临时文件置于共享目录的做法，将导致其他共享用户获得该程序的额外信息，产生信息泄露。

```go
// Good
tmpFile, err := os.CreateTemp("", "prefix-*.tmp")
if err != nil {
    return err
}
defer os.Remove(tmpFile.Name())

// Bad
tmpFile, err := os.Create("/tmp/shared-file.tmp")  // 共享目录
```

##### 规则 1.9.3 文件操作必须检查权限

创建或修改文件时，必须设置适当的文件权限，避免文件被未授权访问。

```go
// Good
f, err := os.OpenFile(filename, os.O_CREATE|os.O_WRONLY, 0600)  // 仅所有者可读写
if err != nil {
    return err
}
defer f.Close()

// Bad
f, err := os.OpenFile(filename, os.O_CREATE|os.O_WRONLY, 0666)  // 所有用户可读写
```

#### 1.10 网络

##### 规则 1.10.1 使用HTTPS进行网络通信

涉及敏感信息的网络通信必须使用HTTPS，禁止使用HTTP。

```go
// Good
client := &http.Client{
    Transport: &http.Transport{
        TLSClientConfig: &tls.Config{
            MinVersion: tls.VersionTLS12,
        },
    },
}

// Bad
resp, err := http.Get("http://example.com/api")  // 未加密
```

##### 规则 1.10.2 验证TLS证书

使用HTTPS时，必须验证服务器证书，禁止跳过证书验证。

```go
// Good
client := &http.Client{
    Transport: &http.Transport{
        TLSClientConfig: &tls.Config{
            MinVersion: tls.VersionTLS12,
        },
    },
}

// Bad
client := &http.Client{
    Transport: &http.Transport{
        TLSClientConfig: &tls.Config{
            InsecureSkipVerify: true,  // 跳过证书验证，危险
        },
    },
}
```

##### 规则 1.10.3 设置合理的超时时间

网络请求必须设置超时时间，避免无限等待。

```go
// Good
client := &http.Client{
    Timeout: 30 * time.Second,
}

// Bad
client := &http.Client{}  // 没有超时设置
```

#### 1.11 加密与随机数

##### 规则 1.11.1 禁用math/rand产生用于安全用途的随机数

`math/rand`生成的是伪随机数，不适合用于安全用途。应该使用`crypto/rand`。

```go
// Good
import "crypto/rand"

func GenerateToken() (string, error) {
    tokenBytes := make([]byte, 32)
    _, err := rand.Read(tokenBytes)
    if err != nil {
        return "", err
    }
    return hex.EncodeToString(tokenBytes), nil
}

// Bad
import "math/rand"

func GenerateToken() string {
    return fmt.Sprintf("%d", rand.Int())  // 伪随机数，不安全
}
```

##### 规则 1.11.2 使用标准库的加密函数

使用`crypto`包中的标准加密函数，不要自己实现加密算法。

```go
// Good
import (
    "crypto/aes"
    "crypto/cipher"
    "crypto/rand"
)

func Encrypt(data []byte, key []byte) ([]byte, error) {
    block, err := aes.NewCipher(key)
    if err != nil {
        return nil, err
    }
    // 使用标准库的加密函数
    // ...
}

// Bad
func Encrypt(data []byte, key []byte) []byte {
    // 自己实现的加密算法，不安全
    // ...
}
```

##### 规则 1.11.3 使用强密码哈希算法

存储密码时，必须使用强密码哈希算法（如bcrypt、argon2），禁止使用MD5、SHA1等弱哈希算法。

```go
// Good
import "golang.org/x/crypto/bcrypt"

func HashPassword(password string) (string, error) {
    hash, err := bcrypt.GenerateFromPassword([]byte(password), bcrypt.DefaultCost)
    if err != nil {
        return "", err
    }
    return string(hash), nil
}

// Bad
import "crypto/sha256"

func HashPassword(password string) string {
    hash := sha256.Sum256([]byte(password))
    return hex.EncodeToString(hash[:])  // SHA256不适合用于密码哈希
}
```

---
