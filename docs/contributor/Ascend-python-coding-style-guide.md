# 昇腾社区 python 语言编程指导（建议稿）

<!-- TOC -->

- [说明](#说明)
- [约定](#约定)
- [例外](#例外)
- [适用范围](#适用范围)
    - [排版](#1-排版)
        - [缩进](#11-缩进)
        - [语句](#12-语句)
        - [空格](#13-空格)
        - [导入](#14-导入)
    - [注释](#2-注释)
    - [命名](#3-命名)
    - [编码](#4-编码)
    - [异常处理](#5-异常处理)
    - [测试用例](#6-测试用例)

<!-- /TOC -->

## 说明

本指导基于python语言指定而成，给参与Ascend开源社区项目的开发者提供编程指导。

规则并不是完美的，通过禁止在特定情况下有用的特性，可能会对代码实现造成影响。但是我们制定规则的目的是“为了大多数程序员可以得到更多的好处”。

参考本指导之前，希望您具有相应的python语言基础能力，而不是通过该文档来学习python语言。

1. 熟知python语言的基本语言特性；
2. 了解python语言的标准库；

如果希望改进某个规则，建议提交Issue并说明理由，经Ascend运营团队评审后可接纳并修改生效。

## 约定

**规则**：编程时必须遵守的约定(must)

**建议**：编程时应该遵守的约定(should)

本指导适用通用python标准，如果没有特定的标准版本，适用所有的版本(python3.8/3.9/3.10/3.11)。

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

## 1. 排版

### 1.1 缩进

### 规则1.1 程序块采用 4 个空格缩进风格编写

说明： 程序块采用缩进风格编写，缩进的空格数为 4 个，是业界通用的标准。

### 规则1.2 禁止混合使用空格(space)和跳格(Tab)

说明： 推荐的缩进方式为仅使用空格(space)。如果已有代码中混合使用了空格及跳格，要全部转换为空格。
设置方法: Setting->Editor->Code Style ->Python->Tabs and Indents; 去掉Smart tabs勾选

### 1.2 语句

### 规则1.3 相对独立的程序块之间、变量说明之后必须加空行

说明： 相对独立的程序块之间、变量说明之后加上空行，代码可理解性会增强很多。

```python
// Bad
程序块之间未加空行
if len(deviceName) < _MAX_NAME_LEN:
...
writer = LogWriter()

// Good
合理留白
if len(deviceName) < _MAX_NAME_LEN:
...

writer = LogWriter()

```

### 规则1.4 一行长度小于 120 个字符，与python标准库（ 80字符）看齐

说明： 使用Pycharm自带的格式化功能统一格式化代码，格式化设置好窗口宽度限制为 120 。
设置方法: Setting->Editor->Code Style ->Python->Wrapping and Braces->Hard wrap at  较长的语句、表达式或参数要分成多行书写，首选使用括号（包括{},[],()）内的行延续，推荐使用反斜杠(\）进行断行。长表达式要在低优先级操作符处划分新行，操作符统一放在新行行首或原行行尾，划分出的新行要进行适当的缩进，使排版整齐，语句可读。

```python
// Bad
一行字符太多太长，阅读代码不方便
if width == 0 and height == 0 and color == 'red' and emphasis == 'strong' and 
highlight > 100:
    x = 1

// Good
if width == 0 and height == 0 and color == 'red' and emphasis == 'strong' \
    and highlight > 100:
    x = 1

```

### 1.3 空格

### 规则1.5 在两个以上的关键字、变量、常量进行对等操作时，它们之间的操作符前后要加空格

说明： 采用这种松散方式编写代码的目的是使代码更加清晰。在长语句中，如果需要加的空格非常多，那么应该保持整体清晰，而在局部不加空格。给操作符留空格时不要连续留一个以上空格。

1.逗号、分号（假如用到的话）只在后面加空格。

```python
// Bad
print(a,b , c)

// Good
print(a, b, c)
```

2.比较操作符">"、">="、"<"、"<="、"=="，赋值操作符"="、"+="，算术操作符"+"、"-"、"%"，逻辑操作符"and"、"or"等双目操作符的前后加空格

```python
// Bad
a=b+ c
a+=2
if current_time>= MAX_TIME_VALUE
   
// Good
a = b + c
a += 2
if current_time >= MAX_TIME_VALUE:
```

### 1.4 导入

### 规则1.6 加载模块必须分开每个模块占一行

说明： 单独使用一行来加载模块，让程序依赖变得更清晰。虽然一行只能加载一个模块，但同一个模块内的多个符号可以在同一行加载。

```python
 // Bad
import sys, os
  
 // Good
import sys
import os
from sys import stdin, stdout
```

### 规则1.7 禁止使用import *的方式导入某个模块的所有成员

说明： from xxx import *会将其他模块中的所有成员挨个赋值给当前范围的同名变量，如果当前范围已经有同名变量，则会静默将其覆盖。这种方式容易导致名字冲突，且冲突后不容易定位，应当尽量避免使用。
正确示例： 如果需要使用yyy，则from xxx import yyy

### 2. 注释

注释和文档字符串的原则是有助于对程序的阅读理解。python没有类型信息，IDE不能帮助提示，如果没有注释，动态语言就很难理解。注释不宜太多也不能太少，一般建议建议有效注释量（包括文档字符串）应该在20%以上。 撰写好的注释有以下建议：注释描述必须准确、易懂、简洁，不能有二义性；

1. 避免在注释和文档字符串中使用缩写，如果要使用缩写则需要有必要的说明；
2. 修改代码时始终优先更新相应的注释/文档字符串，以保证注释/文档字符串与代码的一致性;
3. 有含义的变量，如果不能充分自注释，则需要添加必要的注释；
4. 全局变量建议添加详细注释，包括对其功能、取值范围、哪些函数或过程修改它以及存取时注意事项等的说明。

## 类、接口和函数

### 规则2.1 文档字符串多于一行时，末尾的"""要自成一行

#### 说明： 对于只有一行的文档字符串，把"""放到同一行也没问题

```python
class TreeError(libxmlError):
"""
功能描述：
接口：
"""
```

### 规则2.2 公共函数的文档字符串写在函数声明(def FunctionName(self):)所在行的下一行，并向后缩进4个空格

说明：公共函数文档字符串的内容可选择包括（但不限于）功能描述、输入参数、输出参数、返回值、
调用关系（函数、表）、异常描述等。异常描述除描述函数内部抛出的异常外，还必须说明异常的含义
及什么条件下抛出该异常。

```python
def load_batch(fpath):
"""
功能描述：
参数：
返回值：
异常描述：
"""
```

### 规则2.3 公共属性的注释写在属性声明的上方，与声明保持同样的缩进。行内注释应以#和一个空格作为开始，与后面的文字注释以一个空格隔开

说明：行内注释的形式是在语句的上一行中加注释，它们应以#和一个空格作为开始。行内注释要少用。

```python
//Bad
#Compensate for border
x = x + 1

 // Good
# Compensate for border
x = x + 1
```

### 规则2.3 文档字符串多于一行时，末尾的"""要自成一行

说明：对于只有一行的文档字符串，把"""放到同一行也没问题。

```python
//Bad
"""Return a foobang
Optional plotz says to frobnicate the bizbaz first."""

 // Good
"""Return a foobang
Optional plotz says to frobnicate the bizbaz first.
"""

# 单行场景
"""API for interacting with the volume manager."""
```

### 3. 命名

### 建议3.1 变量（variable）命名要有明确含义，使用完整的单词或大家可以理解的缩写，避免在循环控制变量中使用单个无意义字符，比如i,j,k等

## 命名规范汇总

1. 除了Classes类名、Exceptions异常是大写字母抬头的驼峰命名规则；
2. Global/Class Constants全局常量/类常量是大写+下划线；
3. 其他全都都是使用小写+下划线(_)；
4. 如果涉及到私有成员则需要加下划线(_)或者双下划线(__)作为前缀。

## 命名规范详细情况

| Type（类型）| Public(公共类/方法/变量)| Internal(内部类/方法/变量) |
| --- | --- | --- |
|Modules（模块名） | lower_with_under | _lower_with_under |
|Packages（包名）  | lower_with_under |不涉及  |
|Classes（类名）  | CapWords | CapWords |
|Exceptions（异常）  |CapWords  | 不涉及 |
|Functions/Method Names（方法/函数名 |lower_with_under()  |  _lower_with_under() |
|Global/Class Constants（全局常量/类常量 ) | CAPS_WITH_UNDER | _CAPS_WITH_UNDER |
|Global/Class Variables（全局变量/类变量） | lower_with_under | lower_with_under |
|Instance Variables（实例变量） | lower_with_under |_lower_with_under 或 __lower_with_under(当需要名字修饰时) |
|Function/Method Parameters（方法/函数参数） | lower_with_under | _lower_with_under() 或__lower_with_under()(当需要名字修饰时) |
|Local Variables（局部变量） | lower_with_under | _lower_with_under() 或__lower_with_under() （当需要名字修饰时） |

说明 :
lower_with_under : 小写字母+下划线
CapWords : 大写字母开头(驼峰)
__lower_with_under 或者 _lower_with_under : 下划线抬头的小写+下划线
CAPS_WITH_UNDER : 大写字母+下划线

```python
 // Good
from sample_package import sample_module
from sample_module import SampleClass
sample_global_variable = 0
M_SAMPLE_GLOBAL_CONSTANT = 0
class SampleClass(object):
    SAMPLE_CLASS_CONSTANT = 0
    def sample_member_method(self, sample_parameter):
        pass

    def sample_function():
        sample_function_variable = 0
        sample_instant_variable = SampleClass()
class MyClass(object):
    def my_func(self):
        self._member = 1 # 单下划线开头，暗示此成员仅供类的内部操作使用，外部不应该访问。
    def _my_private_func(self): # 单下划线开头，暗示此方法仅供类的内部操作使用，外部不应该访问。
        pass
class Mapping:
    def __init__(self, iterable):
        self.items_list = []
        self.__update(iterable) # 双下划线开头，会被解释器改名为_Mapping__update,外部如果使用修改后的名字仍可访问
    def update(self, iterable):
        for item in iterable:
            self.items_list.append(item)
            __update = update # 作为update方法的私有复制成员，不会跟派生类成员重名
class MappingSubclass(Mapping):
    # 和基类同名方法，修改了参数个数，但是不会影响基类__init__
    def update(self, keys, values):
        for item in zip(keys, values):
            self.items_list.append(item)
    _update = update # 被解释器改名为_MappingSubclass__update，不会跟基类成员重名
```

### 4. 编码

### 规则4.1 与None作比较要使用“is”或“is not”，不要使用等号

说明：is”判断是否指向同一个对象（判断两个对象的id是否相等），“==”会调用eq方法判断是否等价（判断两个对象的值是否相等）。
示例：
同一个实例，使用“is”和“==”的判断结果不同。

```shell
// Bad
>>> def sample_sort_list(sample_inst):
        if sample_inst is []:
            return
        sample_inst.sort()
>>> fake_list = (2,3,1,4)
>>> sample_sort_list(fake_list)
Traceback (most recent call last):
File "<pyshell#232>", line 1, in <module>
sample_sort_list(fake_list)
File "<pyshell#230>", line 4, in sample_sort_list
sample_inst.sort()
AttributeError: 'tuple' object has no attribute 'sort

//Good

>>> def sample_sort_list(sample_inst):
        if not isinstance(sample_inst, list):
            raise TypeError(r"sample_sort_list in para type error %s" % 
type(sample_inst))
sample_inst.sort()
>>> fake_list = (2,3,1,4)
>>> sample_sort_list(fake_list)
Traceback (most recent call last):
File "<pyshell#235>", line 1, in <module>
sample_sort_list(fake_list)
File "<pyshell#234>", line 3, in sample_sort_list
raise TypeError(r"sample_sort_list in para type error %s" %
type(sample_inst))
TypeError: sample_sort_list in para type error <type 'tuple'
```

## 建议4.2 传递实例类型参数后，函数内应使用isinstance函数进行参数检查，不要使用type

说明: 如果类型有对应的工厂函数，可使用它对类型做相应转换，否则可以使用isinstance函数来检测。使用函数/方法参数传递实例类型参数后，函数内对此参数进行检查应使用isinstance函数，使用isnot None，len(para) != 0等其它逻辑方法都是不安全的。

```bash
>>> class Bad(object): 
    def __eq__(self, other): return True
>>> bad_inst = Bad()
>>> bad_inst == None
True
>>> bad_inst is None
False
```

## 建议4.3 使用推导式代替重复的逻辑操作构造序列。但推导式必须考虑可读性，不在一个推导式中使用三个以上的for语句

说明：推导式（comprehension）是一种精炼的序列生成写法，在可以使用推导式完成简单逻辑，生成序列的场合尽量使用推导式，但如果逻辑较为复杂（>=3个for语句），则不推荐强行使用推导式，因为这会使推导式代码的可读性变差。

```python
//Bad
# 可以简化的列表构建
odd_num_list = []
for i in range(100):
    if i % 2 == 1:
        odd_num_list.append(i)

//Good

odd_num_list = [i for i in range(100) if i % 2 == 1]
```

### 规则4.4 避免在无关的变量或无关的概念之间重用名字，避免因重名而导致的意外赋值和错误引用

说明：Python的函数/类定义和C语言不同，函数/类定义语句实际上是给一个名字赋值。因此重复定义一个函数/类的名字不会导致错误，后定义的会覆盖前面的。但是重复定义很容易掩盖编码问题，让同一个名字的函数/类在不同的执行阶段具有不同的含义，不利于可读性，应予以禁止。Python在解析一个被引用的名字时遵循LEGB顺序（Local - Enclosed - Global - Builtin），从内层一直查找到外层。内层定义的变量会覆盖外层的同名变量。在代码修改时，同名的变量容易导致错误的引用，也不利于代码可读性，应当尽量避免。

### 规则4.5 避免变量在其生命周期内的对象类型发生变化

说明：Python是动态类型语言，允许变量被赋值为不同类型对象，但这么做可能会导致运行时错误，且因为变量上下文语义变化导致代码复杂度提升，难以调试和维护，也不会有任何性能的提升。

## 建议4.6 函数接口定义入参，可明确限定类型，防止误用

说明：python没有类型信息，IDE不能帮助提示，但是如果接口定义指定类型限定，可以避免接口调用传参错误，同时IDE分析后可以进行类型检测。

### 5. 异常处理

### 规则5.1 使用try...except...结构对代码作保护时，需要在异常后使用finally...结构保证操作对象的释放，或者使用with方式的语法结构

说明：使用try...except...结构对代码作保护时，如果代码执行出现了异常，为了能够可靠地关闭操作对象，需要使用finally...结构确保释放操作对象。

### 6. 测试用例

### 规则6.1 函数参数中的可变参数不要使用默认值，在定义时使用None

说明：参数的默认值会在方法定义被执行时就已经设定了 ，这就意味着默认值只会被设定一次，当函数定义后，每次被调用时都会有"预计算"的过程。当参数的默认值是一个可变的对象时，就显得尤为重要，例如参数值是一个list或dict，如果方法体修改这个值(例如往list里追加数据)，那么这个修改就会影响到下一次调用这个方法，这显然不是一种好的方式。应对种情况的方式是将参数的默认值设定为None。

### 规则6.2 严禁使用注释行等形式仅使功能或者用例失效，测试用例应该使用用例级别的方式控制用例不被调度，或者直 接删除无效代码

说明： 测试用例如果失效或者阻塞，可以采用使用级别控制的方式进行管理，或者直接删除无效用例。
