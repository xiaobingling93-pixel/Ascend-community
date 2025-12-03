# Ascend 开源与第三方软件建仓及分支命名指导

---

## 建仓规范

### 仓库命名

在Ascend社区GitCode组织下引入开源软件时，仓库名称应：

- **有官方Git仓库的软件**：与社区官方仓库名称保持一致
- **无官方Git仓库的软件**：使用与官网一致的软件名称，仅使用小写字母、数字及连字符（-），避免其他特殊字符

### 分支与标签规范

#### 1. 分支类型与命名

| 分支类型 | 命名规范 | 用途与规则 |
|----------|----------|------------|
| 社区版本分支(tag) | `{社区版本号}` | **基线分支**。保持与上游社区版本一致，不允许直接修改，仅用于同步更新。 |
| 定制开发分支 | `ascend/{定制修改方仓库名}/{社区版本号}` | **开发分支**。基于社区版本分支创建，用于承载大量定制修改。 |

#### 2. 版本号处理规则

社区版本号转换为分支名称时：
- 保留字母、数字、`.`、`_`、`-`
- 特殊字符替换为 `_`
- 删除中文字符

#### 3. 建仓流程

1. 在GitCode组织下创建空仓库
2. 克隆上游仓库并切换到目标版本
3. 推送版本tag（确保基线可追溯）
4. 创建并推送定制开发分支（开始定制开发）

### 示例：引入 OpenSSL v3.0.9

#### 第一步：在GitCode创建空仓库
在Ascend社区GitCode组织下创建名为 `openssl` 的仓库。

#### 第二步：克隆上游仓库并建立分支

```bash
# 1. 克隆上游仓库
git clone https://github.com/openssl/openssl.git temp-openssl
cd temp-openssl

# 2. 切换到目标版本commit
git checkout openssl-3.0.9  # 切换到上游的3.0.9 tag版本

# 3. 创建定制开发分支（基于当前commit）
git checkout -b ascend/mindspeed/openssl-3.0.9

# 4. 在定制开发分支添加定制修改

# 5. 推送到GitCode
git remote add gitcode https://gitcode.com/Ascend/openssl.git

# 推送分支和tag
git push gitcode ascend/mindspeed/openssl-3.0.9   # 推送定制开发分支
git push gitcode openssl-3.0.9          # 推送版本tag
```

#### 第三步：最终仓库结构

```
openssl/
├── ascend/mindspeed/openssl-3.0.9       # 定制开发分支（默认分支）
└── openssl-3.0.9             # 版本tag（指向上游版本）
```

---

## 文档维护

本文档由Ascend安全SIG管理小组维护，更新需通过社区评审流程。
