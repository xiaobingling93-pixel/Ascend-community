# pre-commit本地运行指南

## 目录

- [pre-commit简介](#pre-commit简介)
- [pre-commit本地运行方法](#pre-commit本地运行方法)
- [pre-commit检测屏蔽方法](#pre-commit检测屏蔽方法)
- [常见问题](#常见问题)
- [官方参考链接](#官方参考链接)

## pre-commit简介

pre-commit 是一款基于 Git 钩子（Git Hooks）的开源代码质量管控工具，在执行 `git commit`提交代码前，会自动完成代码校验、格式规范化、基础问题排查等工作，校验不通过则阻断提交流程，从源头保障代码规范统一、质量合规。

## pre-commit本地运行方法

### 1. 配置国内镜像

配置国内pip镜像源，提升安装下载速度，解决安装卡顿、超时等问题。

```bash
pip config set global.index-url https://mirrors.huaweicloud.com/repository/pypi/simple
```

### 2. 安装pre-commit

```bash
pip install pre-commit
```

### 3. 安装Git钩子

注册Git钩子，后续执行 `git commit` 命令时，自动触发代码检查流程，无需手动调用。

```bash
pre-commit install
```

### 4. 执行代码检查

扫描Git暂存区内的改动文件，自动完成代码格式化与合规性检查，并完成格式化问题代码自动修复，其它未能自动修复的错误请参考提示人工修复。
若pre-commit run执行时出现安装组件失败， 优先检查本地配置文件 `.pre-commit-config.yaml` 是否与主库保持一致，不一致请同步更新。

```bash
git add .
pre-commit run
```

### 5. 提交代码

钩子安装成功后，提交代码时可自动修复代码格式类问题，若没有其他不能自动修复的代码问题可提交成功；否则会提交失败，请人工解决其它不能自动修复的问题后再行commit。

```bash
git add .
git commit -S -m "test"
```

## pre-commit检测屏蔽方法

不建议跳过检测，避免不合规代码入库。以下按使用场景，整理各类合规屏蔽方式，精准控制检测范围。

### 一、局部精准屏蔽（推荐）

仅对单行、代码块屏蔽指定检测，不影响全局，精细化管控，推荐日常使用。大部分格式化、校验工具（如clang-format、ruff、black、isort等），均可使用**off/on**语法控制屏蔽范围，语法通用，用法一致。

#### 1. 单行代码屏蔽

在单行代码末尾添加注释，仅对当前一行生效，精准屏蔽，不影响其他代码。

##### Python（ruff/flake8）

```python
# 跳过指定规则
import unused_module  # noqa: F401
# 跳过单行所有检查
long_code_line  # noqa
```

##### C/C++（clang-tidy/clang-format）

```cpp
// 跳过指定clang-tidy规则
int num;  // NOLINT(modernize-use-auto)
// 跳过单行全部检查
int value;  // NOLINT
```

##### Go语言

```go
// 跳过指定规则
var unused_str string  //nolint:unused
// 跳过单行全部检查
var temp_num int  //nolint
```

#### 2. 代码块屏蔽（通用off/on语法）

对一段连续代码屏蔽指定检查项，关闭后记得用on恢复，不影响后续代码检测。

##### clang-format 格式化屏蔽（C/C++）

```cpp
// clang-format off
// 自定义排版，不执行自动格式化
void test_func() {
int a = 1;
// 随意缩进、格式保留
}
// clang-format on
```

##### ruff 格式化/检查屏蔽（Python）

```python
# ruff: off
# 本段代码跳过ruff格式化、语法检查
def demo():
    unused_var = 0  # 不提示未使用变量
    long_long_long_long_long_long_line  # 不提示行过长
# ruff: on
```

##### black/isort 格式化屏蔽（Python）

```python
# fmt: off
# 跳过black自动格式化
data = {'a':1,'b':2,'c':3}
# fmt: on

# isort: off
# 跳过导入排序
import os
import sys
import json
# isort: on
```

### 两种常用屏蔽语法区别

|屏蔽方式|适用场景|特点|
|---|---|---|
|`// xxx off / xxx on`|仅跳过**格式化**（clang-format、ruff、black）|专一屏蔽格式，保留语法检查，稳妥安全|
|`// NOLINT / noqa / nolint`|跳过**格式化+语法校验**|屏蔽范围广，特殊场景慎用|

### 重要使用提醒

1. 优先使用单行、代码块屏蔽，尽量不全局关闭检测

2. 使用off关闭屏蔽后，务必用on恢复，避免全程跳过检查

3. off/on语法适配绝大多数格式化工具，用法通用，记忆方便

4. 大范围屏蔽建议在配置文件中排除，不建议在代码内滥用

### 二、单次提交跳过（临时全局屏蔽）

仅对当前一次提交生效，跳过所有pre-commit检查，可以直接提交。此修改不会作用到门禁pre-commit检测任务。

```bash
git commit -S -m "提交信息" --no-verify
```

### 三、配置文件排除（永久屏蔽）

修改项目根目录 `.pre-commit-config.yaml`，针对某条规则，排除指定文件或文件夹，不影响其他规则运行。此修改会作用到门禁pre-commit检测任务，请谨慎使用。

```yaml
-   id: clang-format  # 要屏蔽的规则ID
    exclude: |
      (?i)test/.*
      demo/xxx.cpp
```

### 四、卸载钩子（彻底关闭）

彻底关闭pre-commit自动检测，后续提交不再触发检查，恢复检测需重新安装钩子。此修改不会作用到门禁pre-commit检测任务。

```bash
# 卸载钩子，关闭自动检查
pre-commit uninstall

# 重新安装，恢复自动检查
pre-commit install
```

## 常见问题

以下整理了日常使用pre-commit过程中高频遇到的问题及对应解决方案，方便快速排查处理：

### Q1：Windows环境下，clang-format代码格式化功能无法使用怎么办？

**解决方案：**必须安装 Windows C++ 运行库，否则clang-format无法正常运行。

运行库下载地址：[https://learn.microsoft.com/en-us/cpp/windows/latest-supported-vc-redist?view=msvc-170#visual-studio-2015-2017-2019-and-2022](https://learn.microsoft.com/en-us/cpp/windows/latest-supported-vc-redist?view=msvc-170#visual-studio-2015-2017-2019-and-2022)

---

### Q2：执行pre-commit run报错，提示配置文件异常怎么办？

**解决方案：**优先核对本地 `.pre-commit-config.yaml` 文件，确认与仓库主分支版本完全一致。若文件不一致，从主分支同步覆盖后，重新执行检查命令即可。

---

### Q3：pre-commit检查不通过，能强制提交代码吗？

**解决方案：**不建议强制提交。建议按照提示逐一修复问题，重新运行检查，全部通过后再提交。如果有规则冲突或者误报情况，请参考第3章节中屏蔽检测。

---

### Q4：重新拉取代码后，pre-commit不自动检查了怎么办？

**解决方案：**重新克隆仓库后，重新执行pre-commit install挂钩子即可，第一次执行pre-commit run会安装检测工具，请耐心等待几分钟。

```bash
pre-commit install
```

---

### Q5：如何手动运行全量代码检查？

**解决方案：**如需排查整个项目的代码合规问题，可执行全量检查命令，耗时较长，建议按需使用。

```bash
pre-commit run --all-files
```

### Q6：pre-commit运行速度很慢，怎么提升效率？

**解决方案：**一是确认已配置国内pip镜像，避免组件下载卡顿；二是pre-commit默认只检查已add的改动文件，不要使用全量检查命令；三是定期清理缓存，或更新pre-commit至最新版本。

---

## 官方参考链接

pre-commit 官方文档：[https://pre-commit.com/](https://pre-commit.com/)
