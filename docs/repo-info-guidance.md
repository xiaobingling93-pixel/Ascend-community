# 仓库信息yaml文件指导说明

***

## 1 简介

### 1.1 文件作用

昇腾社区组织内每个代码仓库都对应一个repo-info.yaml 文件，用于定义该仓库的基本配置信息（如名称、描述、类型、分支规则等）。每个仓库的文件名需要使用仓库名。

### 1.2 文件位置

文件位于 community 仓库内特定 SIG 组的目录(项目名/sigs/sig名称/ascend/仓库名.yaml)下。

- 例如：community 仓库自身的配置文件路径为 infrastructure/sigs/community/ascend/community.yaml。
- 例如：MindCluster项目的mind-cluster仓的配置文件路径为 MindCluster/sigs/mind-cluster/ascend/mind-cluster.yaml。

### 1.3 目录结构解析 (以 community.yaml 为例)

- infrastructure/：代表 infrastructure 项目。
- sigs/：存放 infrastructure 项目下的所有 SIG 组。
- community/：代表 community SIG 组。
- ascend/：代表昇腾社区组织 (ascend)。该目录下存放 community SIG 组管理的所有仓库的 repo-info.yaml 文件。

### 1.4 文件管理

文件由其所在目录对应的SIG组负责管理。例如，位于 infrastructure/sigs/community/ascend/ 下的community.yaml文件由community SIG组管理。

### 1.5修改流程

仓库信息的yaml 文件只能通过提PR的方式进行修改，PR合入前需要仓库信息yaml文件对应sig组的maintainers进行检视，检视通过后PR才能合入。

## 2 文件格式详解

repo-info.yaml 是 YAML 格式文件，包含以下顶层字段：

| 字段 | 类型 |层级| 说明 |
|--|--|--|--|
| name | 字符串 |一层| 仓库名，必填 |
| rename_from |  字符串 |一层| 修改前的仓库名，可选 |
| description | 字符串 | 一层| 仓库描述，必填 |
| type| 字符串 |一层| 仓库类型（填写public），必填|
| branches| 列表 |一层| 仓库分支信息，必填|

上述 branches 的每一条分支记录包含如下元素：

| 字段 | 类型 | 层级|说明 |
|--|--|--|--|
| name | 字符串 |二层| 分支名, 必填 |
| type | 字符串 |二层| 分支类型(可填写protected，表示分支是受保护分支；否则不填写，表示普通分支), 可选 |
| create_from| 字符串 |二层|  基于哪个分支创建当前分支, 如name值为test，create_from值为master，表示基于master分支创建test分支，可选 |

## testDemo.yaml 样例

```text
# sig组下各仓库基本信息
name: testDemo2     # 修改后的仓库名
rename_from: testDemo   # 修改前的仓库名 （如需要修改仓库名）
description: "test Demo2"  # 仓库描述
type: public     # 仓库类型（公仓）
branches:
  - name: master    # 分支名
    type: protected    # 分支类型，这里的type值只能填protected，表示该分支为保护分支；要么不填
  - name: test
    type: protected
    create_from: master   # 基于某个分支创建分支
```

## 3 常用事件流程

### 3.1 创建仓库

1. 确认仓库名为AAA，选择仓库所属的sig，在对应sig下创建ascend/AAA.yaml。

    ```text
    name: AAA                   # 仓库名
    description: "AAA Demo"        # 仓库描述
    type: public                    # 仓库类型（公仓）
    branches:
      - name: master                # 分支名
        type: protected             # 分支类型，这里的type值只能填protected，表示该分支为保护分支；要么不填
    ```

2. 修改对应的sig-info.yaml文件内容。
3. 提交pr给sig的maintainer打标签（/lgtm 和 /approve）。
4. pr合入后5分钟生效，对应仓库会创建。

### 3.2 修改仓库信息

1. 修改仓库名需要将仓库name字段值修改为新的仓库名，rename字段值填充为旧的仓库名；修改仓库描述直接修改description字段值；修改仓库类型直接修改仓库type字段值。

    ```text
    name: AAA      # 新的仓库名
    rename_from: testDemo   # 修改前的仓库名
    description: "AAA Demo"   # 仓库描述
    type: public     # 仓库类型（公仓）
    branches:
      - name: master                # 分支名
        type: protected             # 分支类型，这里的type值只能填protected，表示该分支为保护分支；要么不填
    ```

2. 修改对应的sig-info.yaml文件内容。
3. 提交pr给sig的maintainer打标签（/lgtm 和 /approve）。
4. pr合入后5分钟生效，对应仓库信息会修改。

### 3.3 删除仓库

1. 机器人不支持删除仓库，需要先删除对应仓库的yaml文件。

    ```text
    name: AAA                   # 仓库名
    description: "AAA Demo"        # 仓库描述
    type: public                    # 仓库类型（公仓）
    branches:
      - name: master                # 分支名
        type: protected             # 分支类型，这里的type值只能填protected，表示该分支为保护分支；要么不填
    ```

2. 修改对应的sig-info.yaml文件内容。
3. 提交pr给sig的maintainer打标签（/lgtm 和 /approve）。
4. 管理员在gitcode的web页面进行操作删除。

### 3.4 新增分支

1. 找到需要新增分支的仓库的yaml文件
2. 修改yaml文件，新增基于master的release_202503分支

    ```text
    name: AAA                 # 仓库名
    description: "AAA Demo"       # 仓库描述
    type: public                    # 仓库类型（公仓）
    branches:
      - name: master                # 分支名
        type: protected             # 分支类型，这里的type值只能填protected，表示该分支为保护分支；要么不填
      - name: release_202503
        type: protected
        create_from: master          # 基于master分支创建分支
    ```

3. 提交pr给sig的maintainer打标签（/lgtm 和 /approve）。
4. pr合入后5分钟生效，对应分支会创建。

### 3.5 删除分支

1. 机器人不支持删除分支，需要先修改yaml文件，删除对应的分支字段

    ```text
    name: AAA                 # 仓库名
    description: "AAA Demo"       # 仓库描述
    type: public                    # 仓库类型（公仓）
    branches:
      - name: master                # 分支名
        type: protected             # 分支类型，这里的type值只能填protected，表示该分支为保护分支；要么不填
    ```

2. 提交pr给sig的maintainer打标签（/lgtm 和 /approve）
3. 管理员在gitcode的web页面进行操作删除。

### 3.6 删除保护分支

1. 机器人不支持删除保护分支，需要先修改yaml文件，删除分支对应的type字段

    ```text
    name: AAA                 # 仓库名
    description: "AAA Demo"       # 仓库描述
    type: public                    # 仓库类型（公仓）
    branches:
      - name: master                # 分支名
        type: protected             # 分支类型，这里的type值只能填protected，表示该分支为保护分支；要么不填
    ```

2. 提交pr给sig的maintainer打标签（/lgtm 和 /approve）
3. 管理员在gitcode的web页面进行操作删除。

## 注意事项 

- 创建仓库时，仓库名不支持包含空格。
- 当需要创建一个新仓库时，机器人会将main分支或者master分支作为仓库的默认分支创建好。
- 仓库名即仓库路径，修改仓库名（name）后，仓库路径随之修改。
- 如果仓库分支的create_from字段没有填写，默认基于master分支创建分支。
- 机器人不支持删除动作，删除仓库操作和删除保护分支操作需要管理员在gitcode的web页面进行操作。
