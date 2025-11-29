# 昇腾社区 C++ 语言编程指导（建议稿）

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
        - [头文件和预处理](#22-头文件和预处理)
        - [常量](#23-常量)
        - [表达式](#24-表达式)
        - [转换](#25-转换)
        - [控制语句](#26-控制语句)
        - [字符串](#27-字符串)
        - [断言](#28-断言)
        - [类和对象](#29-类和对象)
        - [函数设计](#210-函数设计)
        - [函数使用](#211-函数使用)
        - [内存](#212-内存)
        - [文件](#213-文件)

<!-- /TOC -->

## 说明

本指导以[Google C++ Style Guide](https://google.github.io/styleguide/cppguide.html)为基础，给参与Ascend开源社区项目的开发者提供编程指导。

规则并不是完美的，通过禁止在特定情况下有用的特性，可能会对代码实现造成影响。但是我们制定规则的目的是“为了大多数程序员可以得到更多的好处”。

参考本指导之前，希望您具有相应的C++语言基础能力，而不是通过该文档来学习C++语言。

1. 了解C++语言的ISO标准；
2. 熟知C++语言的基本语言特性，包括C++ 03/11/14/17/20相关特性；
3. 了解C++语言的标准库；

如果希望改进某个规则，建议提交Issue并说明理由，经Ascend运营团队评审后可接纳并修改生效。

## 约定

**规则**：编程时必须遵守的约定(must)

**建议**：编程时应该遵守的约定(should)

本指导适用通用C++标准，如果没有特定的标准版本，适用所有的版本(C++03/11/14/17/20)。

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

__驼峰风格(CamelCase)__
大小写字母混用，单词连在一起，不同单词间通过单词首字母大写来分开。
按连接后的首字母是否大写，又分: 大驼峰(UpperCamelCase)和小驼峰(lowerCamelCase)

| 类型                                       | 命名风格      |
| ---------------------------------------- | --------- |
| 类类型，结构体类型，枚举类型，联合体类型等类型定义， 作用域名称         | 大驼峰       |
| 函数(包括全局函数，作用域函数，成员函数)                    | 大驼峰       |
| 全局变量(包括全局和命名空间域下的变量，类静态变量)，局部变量，函数参数，类、结构体和联合体中的成员变量 | 小驼峰       |
| 宏，常量(const)，枚举值，goto 标签                  | 全大写，下划线分割 |

注意：
上表中__常量__是指全局作用域、namespace域、类的静态成员域下，以 const或constexpr 修饰的基本数据类型、枚举、字符串类型的变量，不包括数组和其他类型变量。
上表中__变量__是指除常量定义以外的其他变量，均使用小驼峰风格。


##### 规则 1.1.1 C++文件使用小写+下划线的方式命名，以.cpp结尾，头文件以.h结尾

目前业界还有一些其他的后缀的表示方法：
- 头文件：.hh, .hpp, .hxx
- cpp文件：.cc, .cxx, .c

如果当前项目组使用了某种特定的后缀，那么可以继续使用，但是请保持风格统一。
但是对于本文档，我们默认使用.h和.cpp作为后缀。

##### 规则 1.1.2 函数命名统一使用大驼峰风格，一般采用动词或者动宾结构

```cpp
class List {
public:
	void AddElement(const Element& element);
	Element GetElement(const unsigned int index) const;
	bool IsEmpty() const;
};

namespace Utils {
    void DeleteUser();
}
```
##### 规则 1.1.3 类型命名采用大驼峰命名风格

所有类型命名——类、结构体、联合体、类型定义（typedef）、枚举——使用相同约定，例如：
```cpp
// classes, structs and unions
class UrlTable { ...
struct UrlTableProperties { ...
union Packet { ...
// typedefs
typedef std::map<std::string, UrlTableProperties*> PropertiesMap;
// enums
enum UrlTableErrors { ...
```

对于命名空间的命名，建议使用大驼峰：
```cpp
// namespace
namespace FileUtils {   
}
```

##### 规则 1.1.4 通用变量命名采用小驼峰，包括全局变量，函数形参，局部变量，成员变量

```cpp
std::string tableName;  // Good: 推荐此风格
std::string tablename;  // Bad: 禁止此风格
std::string path;       // Good: 只有一个单词时，小驼峰为全小写
```

全局变量应增加 'g_' 前缀，静态变量命名不需要加特殊前缀
全局变量是应当尽量少使用的，使用时应特别注意，所以加上前缀用于视觉上的突出，促使开发人员对这些变量的使用更加小心。
- 全局静态变量命名与全局变量相同。
- 函数内的静态变量命名与普通局部变量相同。
- 类的静态成员变量和普通成员变量相同。

```cpp
int g_activeConnectCount;

void Func()
{
    static int packetCount = 0; 
    ...
}
```

类的成员变量命名以小驼峰加后下划线组成

```cpp
class Foo {
private:
    std::string fileName_;   // 添加_后缀，类似于K&R命名风格
};
```

##### 规则 1.1.5 宏、枚举值采用全大写，下划线连接的格式
全局作用域内，有名和匿名namespace内的 const 常量，类的静态成员常量，全大写，下划线连接；函数局部 const 常量和类的普通const成员变量，使用小驼峰命名风格。

```cpp
#define MAX(a, b)   (((a) < (b)) ? (b) : (a)) // 仅对宏命名举例，并不推荐用宏实现此类功能

enum TintColor {    // 注意，枚举类型名用大驼峰，其下面的取值是全大写，下划线相连
    RED,
    DARK_RED,
    GREEN,
    LIGHT_GREEN
};

int Func(...)
{
    const unsigned int bufferSize = 100;    // 函数局部常量
    char *p = new char[bufferSize];
    ...
}

namespace Utils {
	const unsigned int DEFAULT_FILE_SIZE_KB = 200;        // 全局常量
}

```

#### 1.2 格式

##### 建议 1.2.1 行宽不超过 120 个字符
建议每行字符数不要超过 120 个。如果超过120个字符，请选择合理的方式进行换行。

例外:
- 如果一行注释包含了超过120 个字符的命令或URL，则可以保持一行，以方便复制、粘贴和通过grep查找；
- 包含长路径的 #include 语句可以超出120 个字符，但是也需要尽量避免；
- 编译预处理中的error信息可以超出一行。
预处理的 error 信息在一行便于阅读和理解，即使超过 120 个字符。
```cpp
#ifndef XXX_YYY_ZZZ
#error Header aaaa/bbbb/cccc/abc.h must only be included after xxxx/yyyy/zzzz/xyz.h, because xxxxxxxxxxxxxxxxxxxxxxxxxxxxx
#endif
```

##### 规则 1.2.2 使用空格进行缩进，每次缩进4个空格
只允许使用空格(space)进行缩进，每次缩进为 4 个空格。不允许使用Tab符进行缩进。
当前几乎所有的集成开发环境（IDE）都支持配置将Tab符自动扩展为4空格输入；请配置您的IDE支持使用空格进行缩进。

##### 规则 1.2.3 在声明指针、引用变量或参数时, `&`、`*`跟随变量名，另外一边留空格

```cpp
char *c;
const std::string &str;
```

##### 规则 1.2.4 if语句必须要使用大括号
我们要求if语句都需要使用大括号，即便只有一条语句。
理由：
- 代码逻辑直观，易读；
- 在已有条件语句代码上增加新代码时不容易出错；
- 对于在if语句中使用函数式宏时，有大括号保护不易出错（如果宏定义时遗漏了大括号）。

```cpp
// 即使if分支代码只有一行，也必须使用大括号
if (cond) {
    single line code;
}
```

##### 规则 1.2.5 for/while等循环语句必须使用大括号

和条件表达式类似，我们要求for/while循环语句必须加上大括号，即便循环体是空的，或循环语句只有一条。
```cpp
for (int i = 0; i < someRange; i++) {   // Good: 使用了大括号
    DoSomething();
}
```
```cpp
while (condition) { }   // Good：循环体是空，使用大括号
```

##### 规则 1.2.6 表达式换行要保持换行的一致性，运算符放行末
较长的表达式，不满足行宽要求的时候，需要在适当的地方换行。一般在较低优先级运算符或连接符后面截断，运算符或连接符放在行末。
运算符、连接符放在行末，表示“未结束，后续还有”。
例（假设下面第一行已经不满足行宽要求）：

```cpp
if ((currentValue > threshold) &&  // Good：换行后，逻辑操作符放在行尾
    someCondition) {
    DoSomething();
    ...
}

int result = reallyReallyLongVariableName1 +    // Good
             reallyReallyLongVariableName2;
```
表达式换行后，注意保持合理对齐，或者4空格缩进。参考下面例子

```cpp
int sum = longVariableName1 + longVariableName2 + longVariableName3 +
    longVariableName4 + longVariableName5 + longVariableName6;         // Good: 4空格缩进

int sum = longVariableName1 + longVariableName2 + longVariableName3 +
          longVariableName4 + longVariableName5 + longVariableName6;   // Good: 保持对齐
```

##### 规则 1.2.7 使用 K&R 缩进风格
__K&R风格__
换行时，函数（不包括lambda表达式）左大括号另起一行放行首，并独占一行；其他左大括号跟随语句放行末。
右大括号独占一行，除非后面跟着同一语句的剩余部分，如 do 语句中的 while，或者 if 语句的 else/else if，或者逗号、分号。

如：
```cpp
struct MyType {     // 跟随语句放行末，前置1空格
    ...
};

int Foo(int a)
{                   // 函数左大括号独占一行，放行首
    if (...) {
        ...
    } else {
        ...
    }
}
```
推荐这种风格的理由：

- 代码更紧凑；
- 相比另起一行，放行末使代码阅读节奏感上更连续；
- 符合后来语言的习惯，符合业界主流习惯；
- 现代集成开发环境（IDE）都具有代码缩进对齐显示的辅助功能，大括号放在行尾并不会对缩进和范围产生理解上的影响。


对于空函数体，可以将大括号放在同一行：
```cpp
class MyClass {
public:
    MyClass() : value_(0) {}
   
private:
    int value_;
};
```

##### 规则 1.2.8 多个变量定义和赋值语句不允许写在一行
每行只有一个变量初始化的语句，更容易阅读和理解。

##### 规则 1.2.9 合理安排空行，保持代码紧凑

减少不必要的空行，可以显示更多的代码，方便代码阅读。下面有一些建议遵守的规则：
- 根据上下内容的相关程度，合理安排空行；
- 函数内部、类型定义内部、宏内部、初始化表达式内部，不使用连续空行
- 不使用连续 **3** 个空行，或更多
- 大括号内的代码块行首之前和行尾之后不要加空行，但namespace的大括号内不作要求。

```cpp
int Foo()
{
    ...
}



int Bar()  // Bad：最多使用连续2个空行。
{
    ...
}


if (...) {
        // Bad：大括号内的代码块行首不要加入空行
    ...
        // Bad：大括号内的代码块行尾不要加入空行
}

int Foo(...)
{
        // Bad：函数体内行首不要加空行
    ...
}
```

#### 1.3 注释
一般的，尽量通过清晰的架构逻辑，好的符号命名来提高代码可读性；需要的时候，才辅以注释说明。 
注释是为了帮助阅读者快速读懂代码，所以要从读者的角度出发，**按需注释**。

注释内容要简洁、明了、无二义性，信息全面且不冗余。

在 C++ 代码中，使用 `/*` `*/`和 `//` 都是可以的。 
按注释的目的和位置，注释可分为不同的类型，如文件头注释、函数头注释、代码注释等等； 
同一类型的注释应该保持统一的风格。

##### 规则 1.3.1 代码注释置于对应代码的上方或右边，注释符与注释内容之间要有1个空格，右置注释与前面代码至少1空格，使用 `//`，而不是 `/**/`

```cpp
// this is multi-
// line comment
int foo; // this single-line comment
```

##### 规则 1.3.2 代码中禁止使用 TODO/TBD/FIXME 等注释，建议提issue跟踪

##### 建议 1.3.3 不要写空有格式的函数头注释

并不是所有的函数都需要函数头注释，函数尽量通过函数名自注释，按需写函数头注释；函数原型无法表达的，却又希望读者知道的信息，才需要加函数头注释辅助说明。
不要写无用、信息冗余的函数头，函数头注释内容可选，但不限于：功能说明、返回值，性能约束、用法、内存约定、算法实现、可重入的要求等。
例：

```cpp
/*
 * 返回实际写入的字节数，-1表示写入失败
 * 注意，内存 buf 由调用者负责释放
 */
int WriteString(const char *buf, int len);
```

坏的例子：
```cpp
/*
 * 函数名：WriteString
 * 功能：写入字符串
 * 参数：
 * 返回值：
 */
int WriteString(const char *buf, int len);
```
上面例子中的问题：

- 参数、返回值，空有格式没内容
- 函数名信息冗余
- 关键的 buf 由谁释放没有说清楚

##### 建议 1.3.4 不用的代码段直接删除，不要注释掉
被注释掉的代码，无法被正常维护；当企图恢复使用这段代码时，极有可能引入易被忽略的缺陷。
正确的做法是，不需要的代码直接删除掉。若再需要时，考虑移植或重写这段代码。

这里说的注释掉代码，包括用 /* */ 和 //，还包括 #if 0， #ifdef NEVER_DEFINED 等等。

### 2. 通用编码

#### 2.1 代码设计

##### 规则 2.1.1 对所有外部数据进行合法性检查，包括但不限于：函数入参、外部输入命令行、文件、环境变量、用户数据等

##### 规则 2.1.2 函数执行结果传递，优先使用返回值，尽量避免使用出参

```cpp
FooBar *Func(const std::string &in);
```

##### 规则 2.1.3 删除无效、冗余或永不执行的代码

大多数现代编译器在许多情况下可以对无效或从不执行的代码告警，为了响应告警应主动识别无效的语句或表达式，并将其从代码中删除，以清除告警。

##### 规则 2.1.4 需要指定捕获异常种类，禁止捕获所有异常

```cpp
// 错误示范
try {
  // do something;
} catch (...) {
  // do something;
}
// 正确示范
try {
  // do something;
} catch (const std::bad_alloc &e) {
  // do something;
}
```

#### 2.2 头文件和预处理

##### 规则 2.2.1 禁止头文件循环依赖

头文件循环依赖，指a.h包含b.h，b.h包含c.h，c.h包含a.h之类导致任何一个头文件修改，都导致所有包含了a.h/b.h/c.h的代码全部重新编译一遍。
头文件循环依赖直接体现了架构设计上的不合理，可通过优化架构去避免。

##### 规则 2.2.2 禁止包含用不到的头文件

##### 规则 2.2.3 禁止通过 extern 声明的方式引用外部函数接口、变量

##### 规则 2.2.4 禁止在extern "C"中包含头文件

##### 规则 2.2.5 禁止在头文件中或者#include之前使用using导入命名空间

#### 2.3 常量

##### 规则 2.3.1 禁止使用宏表示常量

##### 规则 2.3.2 禁止使用魔鬼数字（看不懂、难以理解的数字）

##### 建议 2.3.3 建议每个常量保证单一职责

#### 2.4 表达式

##### 规则 2.4.1 通过使用括号明确操作符的优先级，避免出现低级错误

```cpp
// 正确示范
if (cond1 || (cond2 && cond3)) {
  ...
}

// 错误示范
if (cond1 || cond2 && cond3) {
  ...
}
```

#### 2.5 转换

##### 规则 2.5.1 使用C++提供的类型转换，而不是C风格的类型转换，避免使用const_cast和reinterpret_cast

#### 2.6 控制语句

##### 规则 2.6.1 switch语句要有default分支

#### 2.7 字符串

##### 规则 2.7.1 对字符串进行存储操作，确保字符串有’\0’结束符

#### 2.8 断言

##### 规则 2.8.1 断言不能用于校验程序在运行期间可能导致的错误，可能发生的运行错误要用错误处理代码来处理

#### 2.9 类和对象

##### 规则 2.9.1 单个对象释放使用delete，数组对象释放使用delete []

```cpp
const int kSize = 5;
int *numberArray = new int[kSize];
int *number = new int();
...
delete[] numberArray;
numberArray = nullptr;
delete number;
number = nullptr;
```

##### 规则 2.9.2 禁止使用std::move操作const对象

##### 规则 2.9.3 严格使用virtual/override/final修饰虚函数

```cpp
class Base {
  public:
    virtual void Func();
};

class Derived : public Base {
  public:
    void Func() override;
};

class FinalDerived : public Derived {
  public:
    void Func() final;
};
```

#### 2.10 函数设计

##### 规则 2.10.1 使用 RAII 特性来帮助追踪动态分配

```cpp
// 正确示范
{
  std::lock_guard<std::mutex> lock(mutex_);
  ...
}
```

##### 规则 2.10.2 非局部范围使用lambda时，避免按引用捕获

```cpp
{
  int local_var = 1;
  auto func = [&]() { ...; std::cout << local_var << std::endl; };
  thread_pool.commit(func);
}
```

##### 规则 2.10.3 禁止虚函数使用缺省参数值

##### 建议 2.10.4 使用强类型参数，避免使用void*

#### 2.11 函数使用

##### 规则 2.11.1 函数传参传递，要求入参在前，出参在后

```cpp
bool Func(const std::string &in, FooBar *out1, FooBar *out2);
```

##### 规则 2.11.2 函数传参传递，要求入参用 `const T &`，出参用 `T *`

```cpp
bool Func(const std::string &in, FooBar *out1, FooBar *out2);
```

##### 规则 2.11.3 函数传参传递，不涉及所有权的场景，使用T * 或const T & 作为参数，而不是智能指针

```cpp
// 正确示范
bool Func(const FooBar &in);
// 错误示范
bool Func(std::shared_ptr<FooBar> in);
```

##### 规则 2.11.4 函数传参传递，如需传递所有权，建议使用shared_ptr + move传参

```cpp
class Foo {
  public:
    explicit Foo(std::shared_ptr<T> x):x_(std::move(x)){}
  private:
    std::shared_ptr<T> x_;
};
```

##### 规则 2.11.5 单参数构造函数必须用explicit修饰，多参数构造函数禁止使用explicit修饰

```cpp
explicit Foo(int x);          //good ，单参数构造函数使用explicit修饰
explicit Foo(int x, int y=0); //good ，有默认参数的单参数构造函数使用explicit修饰
Foo(int x, int y=0);          //bad  ，有默认参数的单参数构造函数没有使用explicit修饰
explicit Foo(int x, int y);   //bad  ，多参数构造函数使用了explicit修饰
```

##### 规则 2.11.6 拷贝构造和拷贝赋值操作符应该是成对出现或者禁止

```cpp
class Foo {
  private:
    Foo(const Foo&) = default;
    Foo& operator=(const Foo&) = default;
    Foo(Foo&&) = delete;
    Foo& operator=(Foo&&) = delete;
};
```

##### 规则 2.11.7 禁止保存、delete指针参数

#### 2.12 内存

##### 规则 2.12.1 内存分配后必须判断是否成功

内存分配失败后，那么后续的操作存在未定义的行为风险。比如malloc申请失败返回了空指针，对空指针的解引用是一种未定义行为。

##### 规则 2.12.2 禁止引用未初始化的内存

malloc、new分配出来的内存没有被初始化为0，要确保内存被引用前是被初始化的。

#### 2.13 文件

##### 规则 2.13.1 必须对文件路径进行规范化后再使用

当文件路径来自外部数据时，需要先将文件路径规范化，如果没有作规范化处理，攻击者就有机会通过恶意构造文件路径进行文件的越权访问：
例如，攻击者可以构造“../../../etc/passwd”的方式进行任意文件访问。
在linux下，使用realpath函数，在windows下，使用PathCanonicalize函数进行文件路径的规范化。

【错误代码示例】
以下代码从外部获取到文件名称，拼接成文件路径后，直接对文件内容进行读取，导致攻击者可以读取到任意文件的内容：

```cpp
char *fileName = GetMsgFromRemote();
...
sprintf_s(untrustPath, sizeof(untrustPath), "/tmp/%s", fileName);
char *text = ReadFileContent(untrustPath);   // Bad，读取前未检查untrustPath是否允许访问
```

【正确代码示例】
正确的做法是，对路径进行规范化后，再判断路径是否是本程序所认为的合法的路径：

```cpp
char *fileName = GetMsgFromRemote();
...
sprintf_s(untrustPath, sizeof(untrustPath), "/tmp/%s", fileName);
char path[PATH_MAX] = {0};
if (realpath(untrustPath, path) == NULL) {
    //error
    ...
}
if (!IsValidPath(path)) {    // Good，检查文件位置是否正确
    //error
    ...
}
char *text = ReadFileContent(path);
```

【例外】
运行于控制台的命令行程序，通过控制台手工输入文件路径，可以作为本建议例外。

##### 规则 2.13.2 不要在共享目录中创建临时文件

程序的临时文件应当是程序自身独享的，任何将自身临时文件置于共享目录的做法，将导致其他共享用户获得该程序的额外信息，产生信息泄露。因此，不要在任何共享目录创建仅由程序自身使用的临时文件。
如Linux下的/tmp目录是一个所有用户都可以访问的共享目录，不应在该目录下创建仅由程序自身使用的临时文件。

---
