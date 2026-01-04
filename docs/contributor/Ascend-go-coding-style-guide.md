# 昇腾社区 Go 语言编程指导（建议稿）

<!-- TOC -->

- [说明](#说明)
- [约定](#约定)
- [例外](#例外)
- [适用范围](#适用范围)
    - [代码风格](#1-代码风格)
        - [命名](#11-命名)
        - [格式](#12-格式)
        - [注释](#13-注释)
    - [通用编码](#2-通用编码)
        - [代码设计](#21-代码设计)
        - [包管理](#22-包管理)
        - [CGO](#23-cgo)
        - [常量](#24-常量)
        - [表达式](#25-表达式)
        - [控制语句](#26-控制语句)
        - [字符串](#27-字符串)
        - [结构体和接口](#28-结构体和接口)
        - [函数设计](#29-函数设计)
        - [错误处理](#210-错误处理)

<!-- /TOC -->

## 说明

本指导以[Effective Go](https://go.dev/doc/effective_go)和[Go Code Review Comments](https://github.com/golang/go/wiki/CodeReviewComments)为基础，结合业界最佳实践，给参与Ascend开源社区项目的开发者提供编程指导。

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

在不违背总体原则，经过充分考虑，有充足理由的前提下，可以适当违背本指导中的约定。
例外破坏了代码的一致性，请尽量避免。'规则'的例外应该是极少的。

下列情况，应风格一致性原则优先： 
**修改和适配外部开源代码、第三方代码时，应该遵守开源代码、第三方代码已有规范，保持风格统一。** 

## 适用范围

Ascend 社区所有开源仓

---

### 1. 代码风格

#### 1.1 命名

Go语言使用大小写来控制可见性：首字母大写的标识符是导出的（public），首字母小写的标识符是包内私有的（private）。

##### 规则 1.1.1 Go文件使用小写+下划线的方式命名，以.go结尾

Go源文件使用小写字母和下划线命名，例如：`user_service.go`、`http_client.go`。

测试文件以`_test.go`结尾，例如：`user_service_test.go`。

##### 规则 1.1.2 包名使用简短、小写、单数形式的单词，避免使用下划线或混合大小写

包名应该简短、有意义，使用小写字母，不使用下划线或驼峰命名。

```go
// Good
package user
package httpclient
package config

// Bad
package UserService
package http_client
package userService
```

##### 规则 1.1.3 导出函数和类型命名采用大驼峰风格

所有导出的（首字母大写）函数、类型、常量、变量使用大驼峰命名风格。

```go
// 导出的类型
type UserInfo struct {
    Name string
}

// 导出的函数
func GetUserInfo(id int) (*UserInfo, error) {
    // ...
}

// 导出的常量
const MaxRetryCount = 3
```

##### 规则 1.1.4 非导出函数、变量、结构体字段采用小驼峰命名风格

非导出的（首字母小写）函数、变量、结构体字段使用小驼峰命名风格。

```go
// 非导出的类型
type userInfo struct {
    name string  // 小驼峰
    age  int
}

// 非导出的函数
func getUserInfo(id int) (*userInfo, error) {
    // ...
}

// 非导出的变量
var defaultTimeout = 30 * time.Second
```

##### 规则 1.1.5 常量命名采用大驼峰风格，包内私有常量使用小驼峰

导出的常量使用大驼峰，包内私有常量使用小驼峰。

```go
// 导出的常量
const DefaultTimeout = 30 * time.Second
const MaxRetryCount = 3

// 包内私有常量
const defaultTimeout = 30 * time.Second
const maxRetryCount = 3
```

##### 规则 1.1.6 变量命名应该简短且有意义，避免使用单字母变量名（除了循环变量）

```go
// Good
userName := "admin"
userCount := 10

for i := 0; i < len(users); i++ {
    // i 作为循环变量是可以的
}

// Bad
u := "admin"
c := 10
```

#### 1.2 格式

##### 规则 1.2.1 使用gofmt格式化代码

所有Go代码必须使用`gofmt`工具进行格式化。建议在提交代码前运行`gofmt -w .`。

大多数IDE和编辑器都支持保存时自动运行gofmt。

##### 建议 1.2.2 行宽不超过 120 个字符

建议每行字符数不要超过 120 个。如果超过120个字符，请选择合理的方式进行换行。

例外:

- 如果一行注释包含了超过120 个字符的命令或URL，则可以保持一行，以方便复制、粘贴和通过grep查找；
- 包含长路径的 import 语句可以超出120 个字符，但是也需要尽量避免；

##### 规则 1.2.3 使用Tab进行缩进

Go语言标准使用Tab进行缩进，不要使用空格。gofmt会自动将空格转换为Tab。

##### 规则 1.2.4 表达式换行要保持换行的一致性

较长的表达式，不满足行宽要求的时候，需要在适当的地方换行。一般在较低优先级运算符或连接符后面截断。

```go
// Good
if (currentValue > threshold) &&
    someCondition {
    doSomething()
}

result := reallyReallyLongVariableName1 +
    reallyReallyLongVariableName2
```

##### 规则 1.2.5 左大括号不换行（K&R风格）

Go语言强制要求左大括号不换行，这是语言规范的一部分。

```go
// Good
func Foo(a int) {
    if a > 0 {
        // ...
    }
}

type MyStruct struct {
    Field1 string
    Field2 int
}

// Bad (编译错误)
func Foo(a int)
{
    // ...
}
```

##### 规则 1.2.6 合理安排空行，保持代码紧凑

减少不必要的空行，可以显示更多的代码，方便代码阅读。下面有一些建议遵守的规则：

- 根据上下内容的相关程度，合理安排空行；
- 函数内部、类型定义内部，不使用连续空行
- 不使用连续 **3** 个空行，或更多
- 函数之间使用一个空行分隔

```go
// Good
func Foo() {
    // ...
}

func Bar() {
    // ...
}

// Bad
func Foo() {
    // ...
}



func Bar() {  // 最多使用连续2个空行
    // ...
}
```

#### 1.3 注释

一般的，尽量通过清晰的架构逻辑，好的符号命名来提高代码可读性；需要的时候，才辅以注释说明。 
注释是为了帮助阅读者快速读懂代码，所以要从读者的角度出发，**按需注释**。

注释内容要简洁、明了、无二义性，信息全面且不冗余。

##### 规则 1.3.1 所有导出的函数、类型、变量、常量必须有注释

导出的标识符必须有注释，注释应该以标识符名称开头，使用完整的句子。

```go
// GetUserInfo 根据用户ID获取用户信息
// 如果用户不存在，返回 ErrUserNotFound 错误
func GetUserInfo(id int) (*UserInfo, error) {
    // ...
}

// UserInfo 表示用户信息
type UserInfo struct {
    Name string // 用户名
    Age  int    // 年龄
}

// MaxRetryCount 表示最大重试次数
const MaxRetryCount = 3
```

##### 规则 1.3.2 代码注释置于对应代码的上方，注释符与注释内容之间要有1个空格

```go
// this is multi-
// line comment
var foo int // this single-line comment
```

##### 规则 1.3.3 代码中禁止使用 TODO/TBD/FIXME 等注释，建议提issue跟踪

##### 建议 1.3.4 不要写空有格式的函数头注释

并不是所有的函数都需要函数头注释，函数尽量通过函数名自注释，按需写函数头注释；函数原型无法表达的，却又希望读者知道的信息，才需要加函数头注释辅助说明。
不要写无用、信息冗余的函数头，函数头注释内容可选，但不限于：功能说明、返回值，性能约束、用法、算法实现、并发安全等。

```go
// Good
// ProcessData 处理数据并返回处理结果
// 注意：此函数不是并发安全的，调用者需要自行加锁
func ProcessData(data []byte) ([]byte, error) {
    // ...
}

// Bad
/*
 * 函数名：ProcessData
 * 功能：处理数据
 * 参数：data
 * 返回值：处理结果
 */
func ProcessData(data []byte) ([]byte, error) {
    // ...
}
```

##### 建议 1.3.5 不用的代码段直接删除，不要注释掉

被注释掉的代码，无法被正常维护；当企图恢复使用这段代码时，极有可能引入易被忽略的缺陷。
正确的做法是，不需要的代码直接删除掉。若再需要时，考虑移植或重写这段代码。

### 2. 通用编码

#### 2.1 代码设计

##### 规则 2.1.1 函数执行结果传递，优先使用返回值，避免使用全局变量

Go语言支持多返回值，应该充分利用这一特性。

```go
// Good
func GetUser(id int) (*User, error) {
    // ...
}

// Bad
var globalUser *User
var globalErr error

func GetUser(id int) {
    // 修改全局变量
}
```

##### 规则 2.1.2 删除无效、冗余或永不执行的代码

大多数现代编译器在许多情况下可以对无效或从不执行的代码告警，为了响应告警应主动识别无效的语句或表达式，并将其从代码中删除，以清除告警。

##### 规则 2.1.3 使用defer确保资源释放

使用defer确保资源（如文件、锁、连接等）能够正确释放。

```go
// Good
func ReadFile(filename string) ([]byte, error) {
    f, err := os.Open(filename)
    if err != nil {
        return nil, err
    }
    defer f.Close()
    
    return ioutil.ReadAll(f)
}
```

#### 2.2 包管理

##### 规则 2.2.1 禁止包循环依赖

包循环依赖会导致编译错误，应该通过优化架构设计来避免。

##### 规则 2.2.2 禁止导入未使用的包

Go编译器会报错，但应该主动避免导入不需要的包。

##### 规则 2.2.3 import语句分组：标准库、第三方库、本地包，用空行分隔

```go
import (
    // 标准库
    "fmt"
    "os"
    "time"
    
    // 第三方库
    "github.com/gin-gonic/gin"
    "golang.org/x/crypto/bcrypt"
    
    // 本地包
    "project/internal/config"
    "project/internal/db"
)
```

##### 规则 2.2.4 使用go.mod管理依赖

使用Go Modules进行依赖管理，不要将vendor目录提交到版本控制系统（除非项目要求）。

#### 2.3 CGO

CGO允许Go代码调用C代码，但会降低代码的可移植性、增加构建复杂度，并可能影响性能。应该谨慎使用CGO。

##### 规则 2.3.1 最小化CGO的使用

仅在确实需要调用C代码时使用CGO。优先考虑使用纯Go实现或Go标准库提供的功能。

```go
// Good - 优先使用纯Go实现
import "crypto/sha256"

func Hash(data []byte) []byte {
    h := sha256.Sum256(data)
    return h[:]
}

// Bad - 不必要地使用CGO调用C的哈希函数
/*
#include <openssl/sha.h>
*/
import "C"
```

##### 规则 2.3.2 CGO代码必须正确管理内存

在Go和C之间传递数据时，必须正确管理内存，避免内存泄漏和未定义行为。

```go
// Good
/*
#include <stdlib.h>
*/
import "C"
import "unsafe"

func AllocateCString(s string) *C.char {
    cstr := C.CString(s)
    return cstr
}

func FreeCString(cstr *C.char) {
    C.free(unsafe.Pointer(cstr))
}

func ProcessString(s string) {
    cstr := AllocateCString(s)
    defer FreeCString(cstr)  // 确保释放内存
    
    // 使用cstr调用C函数
    C.someCFunction(cstr)
}

// Bad
func ProcessString(s string) {
    cstr := C.CString(s)
    // 没有释放内存，导致内存泄漏
    C.someCFunction(cstr)
}
```

##### 规则 2.3.3 CGO调用必须进行错误处理

调用C代码时，必须检查返回值并处理可能的错误，防止程序崩溃。

```go
// Good
/*
#include <errno.h>
#include <stdlib.h>
*/
import "C"
import "syscall"

func CallCFunction() error {
    result := C.someCFunction()
    if result == nil {
        errno := C.errno
        if errno != 0 {
            return syscall.Errno(errno)
        }
        return errors.New("C function returned NULL")
    }
    // 处理result
    return nil
}

// Bad
func CallCFunction() {
    result := C.someCFunction()  // 没有检查错误
    // 如果result为NULL，后续操作可能导致panic
}
```

##### 规则 2.3.4 CGO代码必须进行边界检查

在Go和C之间传递数据时，必须进行边界检查，防止缓冲区溢出等安全漏洞。

```go
// Good
func ProcessBuffer(data []byte, maxSize int) error {
    if len(data) > maxSize {
        return errors.New("data too large")
    }
    
    cdata := (*C.char)(unsafe.Pointer(&data[0]))
    result := C.processBuffer(cdata, C.size_t(len(data)))
    if result != 0 {
        return errors.New("C function failed")
    }
    return nil
}

// Bad
func ProcessBuffer(data []byte) {
    cdata := (*C.char)(unsafe.Pointer(&data[0]))
    // 没有边界检查，可能导致缓冲区溢出
    C.processBuffer(cdata, C.size_t(len(data)))
}
```

##### 建议 2.3.5 为CGO代码编写详细的文档注释

CGO代码涉及跨语言调用，应该编写详细的文档注释，说明内存管理、错误处理等注意事项。

```go
// ProcessData 调用C函数处理数据
// 
// 注意：
// - 函数内部会分配C内存，调用者无需手动释放
// - 如果C函数返回错误，会返回非nil的error
// - data的长度不能超过MAX_DATA_SIZE，否则会返回错误
func ProcessData(data []byte) error {
    // ...
}
```

#### 2.4 常量

##### 规则 2.4.1 使用const定义常量，禁止使用变量作为常量

```go
// Good
const MaxRetryCount = 3
const DefaultTimeout = 30 * time.Second

// Bad
var MaxRetryCount = 3
```

##### 规则 2.4.2 禁止使用魔鬼数字（看不懂、难以理解的数字）

```go
// Good
const MaxConnections = 100
if count > MaxConnections {
    // ...
}

// Bad
if count > 100 {
    // ...
}
```

##### 建议 2.4.3 建议每个常量保证单一职责

#### 2.5 表达式

##### 规则 2.5.1 通过使用括号明确操作符的优先级，避免出现低级错误

```go
// Good
if cond1 || (cond2 && cond3) {
    // ...
}

// Bad
if cond1 || cond2 && cond3 {
    // ...
}
```

#### 2.6 控制语句

##### 规则 2.6.1 switch语句要有default分支

```go
// Good
switch value {
case 1:
    // ...
case 2:
    // ...
default:
    // ...
}
```

##### 规则 2.6.2 尽早返回，减少嵌套

使用早期返回可以减少代码嵌套，提高可读性。

```go
// Good
func Process(data []byte) error {
    if len(data) == 0 {
        return errors.New("data is empty")
    }
    
    if err := validate(data); err != nil {
        return err
    }
    
    // 处理逻辑
    return nil
}

// Bad
func Process(data []byte) error {
    if len(data) > 0 {
        if err := validate(data); err == nil {
            // 处理逻辑
            return nil
        } else {
            return err
        }
    } else {
        return errors.New("data is empty")
    }
}
```

#### 2.7 字符串

##### 规则 2.7.1 字符串拼接优先使用strings.Builder或fmt.Sprintf，避免使用+操作符进行大量拼接

```go
// Good
var builder strings.Builder
for _, s := range strings {
    builder.WriteString(s)
}
result := builder.String()

// Bad (大量拼接时)
result := ""
for _, s := range strings {
    result += s
}
```

#### 2.8 结构体和接口

##### 规则 2.8.1 结构体字段命名：导出字段使用大驼峰，非导出字段使用小驼峰

导出的结构体字段（首字母大写）使用大驼峰命名风格，非导出的结构体字段（首字母小写）使用小驼峰命名风格。

```go
// Good
type User struct {
    Name     string  // 导出字段，使用大驼峰
    Age      int     // 导出字段，使用大驼峰
    email    string  // 非导出字段，使用小驼峰
}

// Bad
type User struct {
    user_name string  // 使用下划线，不符合Go命名规范
    User_Name string  // 导出字段使用下划线，不符合规范
}
```

##### 规则 2.8.2 接口应该小而专注，避免定义过于庞大的接口

```go
// Good
type Reader interface {
    Read([]byte) (int, error)
}

type Writer interface {
    Write([]byte) (int, error)
}

// Bad
type ReadWriteCloser interface {
    Read([]byte) (int, error)
    Write([]byte) (int, error)
    Close() error
    Flush() error
    Seek(int64, int) (int64, error)
    // ... 太多方法
}
```

##### 规则 2.8.3 结构体初始化使用字段名，避免位置参数

```go
// Good
user := User{
    Name: "Alice",
    Age:  30,
}

// Bad (当字段顺序可能变化时)
user := User{"Alice", 30}
```

#### 2.9 函数设计

##### 规则 2.9.1 函数应该简短，单一职责

函数应该专注于做一件事，并且做好。建议函数长度不超过50行。

##### 规则 2.9.2 函数参数不宜过多，超过5个参数时考虑使用结构体

```go
// Good
type CreateUserRequest struct {
    Name    string
    Email   string
    Age     int
    Phone   string
    Address string
}

func CreateUser(req CreateUserRequest) error {
    // ...
}

// Bad
func CreateUser(name, email string, age int, phone string, address string, city string, country string) error {
    // ...
}
```

##### 规则 2.9.3 函数返回值应该包含error，除非函数不可能失败

```go
// Good
func GetUser(id int) (*User, error) {
    // ...
}

// Bad
func GetUser(id int) *User {
    // 如果失败怎么办？
}
```

##### 规则 2.9.4 使用命名返回值提高可读性，但要谨慎使用

命名返回值可以提高代码可读性，但过度使用可能导致代码混乱。

```go
// Good (简单场景)
func Divide(a, b float64) (result float64, err error) {
    if b == 0 {
        return 0, errors.New("division by zero")
    }
    result = a / b
    return
}

// Bad (复杂场景，容易混淆)
func ComplexFunction() (result1, result2, result3 int, err1, err2 error) {
    // 太多命名返回值，容易混淆
}
```

#### 2.10 错误处理

##### 规则 2.10.1 必须检查并处理所有错误

不要忽略错误返回值，必须显式处理。

```go
// Good
data, err := ioutil.ReadFile(filename)
if err != nil {
    return err
}

// Bad
data, _ := ioutil.ReadFile(filename)
```

##### 规则 2.10.2 错误信息应该提供上下文信息

使用`fmt.Errorf`或`errors.Wrap`（如果使用pkg/errors）为错误添加上下文。

```go
// Good
if err != nil {
    return fmt.Errorf("failed to read config file %s: %w", filename, err)
}

// Bad
if err != nil {
    return err
}
```

##### 规则 2.10.3 使用errors.New或fmt.Errorf创建错误，避免使用字符串

```go
// Good
return errors.New("user not found")
return fmt.Errorf("user %d not found", id)

// Bad
return "user not found"
```

##### 规则 2.10.4 导出的错误变量应该以Err开头

```go
// Good
var ErrUserNotFound = errors.New("user not found")
var ErrInvalidInput = errors.New("invalid input")

// Bad
var UserNotFound = errors.New("user not found")
```

---
