# 🗂️ Ascend community 仓库整体介绍

## 📌概述

community 仓库是昇腾（Ascend）社区的核心管理仓库，用于实现**组织级权限的统一管理**。通过层级化的目录结构和配置文件，实现对项目、SIG组、代码仓库及成员权限的规范化管理。

## 🛠️ 核心功能

1. **统一权限管理**  
   集中管理 Ascend 组织下所有项目和 SIG 组的成员权限
2. **结构化配置**  
   通过 YAML 文件定义各层级的权限关系
3. **精细化权限控制**  
   支持从项目→SIG→仓库→分支/目录/文件→目录/文件的五级权限配置
4. **职责分离**  
   明确划分 TC 成员、SIG Maintainers、Committers、Reviewers 等角色职责

## 📊 核心管理文件体系

| 文件             | 位置                                      | 核心作用                          | 管理范围       |
|------------------|-------------------------------------------|-----------------------------------|---------------------|
| `org-info.yaml`  | 项目目录（如 `Ascend/community/MindCluster/`） | 定义项目级 TC 成员和 SIG 框架     | 项目全局架构      |
| `sig-info.yaml`  | SIG 目录（如 `sigs/RecSDK/`）           | 配置 SIG 内仓库的精细权限规则     | SIG 组内所有仓库代码合入权限 |
| `repo-info.yaml`  | SIG 目录（如 `sigs/ascend/`）           | 定义仓库分支结构与属性     | SIG 组内所有仓库创建 |

## 📂 目录治理结构

community代码仓目录结构对应管理组织结构：

| 分层 | 内容 | 目录层级  |说明|
|--|--|--|--|
|  平台组织 |Ascend   | 0层 |组织
|  仓库    | community  | 一层 |权限管理统一仓库
|  目录    | MindStudio/MindCluster/... | 二层 |项目目录
|  文件    | org-info.yaml  | 三层 |项目成员权限管理
|  目录    | sigs  | 三层 |项目SIG集合
|  目录    | RecSDK/DrivingSDK/... | 四层 |一个SIG一个目录
|  文件    | sig-info.yaml  | 五层 |单个SIG仓库权限管理

具体示例：

```plaintext
Ascend（组织根）
└── community（权限仓库）
    ├── MindStudio（项目）
    │   ├── org-info.yaml
    │   └── sigs（SIG组集合）
    │       ├── msit
    │       │   └── sig-info.yaml (核心权限文件)
    │       │   └── ascend/
    │       │       └── *.yaml（仓库配置）
    │       └── mstt
    ├── MindCluster（项目）
    ├── docs (文档仓库)
    └── common (公共SIG)
        ├── org-info.yaml
        └── sigs（SIG组集合）
            └── infrastructure（基础设施SIG）
                └── sig-info.yaml (核心权限文件)  
                └── ascend/
                    └── *.yaml（仓库配置）
```

## 🔄 权限继承规则

- 低层级配置覆盖高层级权限。
- 权限变更通过PR流程审核。
- Ascend/community仓库每隔10分钟进行定时同步，权限配置后10分钟内生效。

## 📚 教程与规范文档

- 📘 [Ascend社区协作指南](https://gitcode.com/Ascend/community/blob/master/docs/role-guidance.md) - 所有角色的完整操作流程
- 📋 [org-info.yaml编写指南](https://gitcode.com/Ascend/community/blob/master/docs/org-info-guidance.md) - 项目级配置详解
- 🔧 [sig-info.yaml编写指南](https://gitcode.com/Ascend/community/blob/master/docs/sig-info-guidance.md) - SIG权限配置详解
- 📁 [repo-info.yaml编写指南](https://gitcode.com/Ascend/community/blob/master/docs/repo-info-guidance.md) - 仓库属性管理说明
