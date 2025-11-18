# Ascend 社区开发者测试贡献指南

昇腾（Ascend）社区作为一个开放、创新的平台，欢迎业界所有开发者参与开发者测试贡献，共同构筑社区的质量保障体系。开发者可以从单元测试与系统测试两个维度开展贡献活动，相关测试用例会在代码合入 [门禁](https://gitcode.com/Ascend/ci-infra/blob/master/docs/%E9%97%A8%E7%A6%81%E8%A6%81%E6%B1%82.md) 过程中被执行，后续章节会做详细说明。在进行贡献前，请先签署 [CLA](https://clasign.osinfra.cn/sign/gitee_ascend-1611222220829317930)。

## 分类

- **单元测试**（Unit Test）：针对特定函数或代码片段的测试，形式通常为类与函数，以功能为粒度归集在一个测试文件中。在门禁开发者测试检查项的 [UT](https://gitcode.com/Ascend/ci-infra/blob/master/docs/%E9%97%A8%E7%A6%81%E8%A6%81%E6%B1%82.md) 阶段执行
- **系统测试**（System Test）：针对特性模块与特性的测试，形式通常为一个或多个测试文件以及对应的配置与数据文件。在门禁开发者测试检查项的 [前冒烟](https://gitcode.com/Ascend/ci-infra/blob/master/docs/%E9%97%A8%E7%A6%81%E8%A6%81%E6%B1%82.md) 阶段执行

### 单元测试

开发者在进行常规代码贡献活动时，除了增加修改功能代码外，还需要针对这部分代码变更，配套进行已有单元测试用例的刷新或补充新的单元测试用例。
> 各个项目的单元测试用例一般归档在项目代码仓根目录的test或tests文件夹下，针对不同功能模块可能存在不同的子文件夹

### 系统测试

特性与模块级的贡献，通常涉及多次代码合入，在单元测试的基础上，开发者需要在RFC（Request for Comments）提案中增加对应的系统测试设计与说明，以issue形式与项目maintainer沟通以进行已有系统测试用例的刷新或补充新的系统测试用例，issue的提交与处理请参考 [Issue提交指南](https://gitcode.com/Ascend/community/blob/master/docs/contributor/issue-guide.md)。
> 各个项目的系统测试用例一般归档在与项目代码仓关联的独立用例代码仓，形成单独的系统测试用例集合

## 规范

1. 开发者在昇腾（Ascend）社区贡献测试代码时需在代码头部增加版权声明，明确代码的版权归属，并同步增加许可证声明

    版权声明格式可参考
    ```
    Copyright (c) [Year] [name of copyright holder]
    ```
    许可证声明方式可参考（以Mulan PSL v2为例）
    ```
    This program is licensed under Mulan PSL v2.
    You can use it according to the terms and conditions of the Mulan PSL v2.
           http://license.coscl.org.cn/MulanPSL2
    THIS PROGRAM IS PROVIDED ON AN "AS IS" BASIS, WITHOUT WARRANTIES OF ANY KIND,
    EITHER EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO NON-INFRINGEMENT,
    MERCHANTABILITY OR FIT FOR A PARTICULAR PURPOSE.
    See the Mulan PSL v2 for more details.
    ```

2. 开发者在昇腾（Ascend）社区贡献测试代码时需要遵循社区已发布的编码规范要求，具体请参考门禁 [编码安全与规范检查项](https://gitcode.com/Ascend/ci-infra/blob/master/docs/%E9%97%A8%E7%A6%81%E8%A6%81%E6%B1%82.md)
3. 昇腾（Ascend）社区当前在代码合入自动化测试阶段，对代码的测试覆盖率有一定的量化要求，具体请参考门禁 [开发者测试检查项](https://gitcode.com/Ascend/ci-infra/blob/master/docs/%E9%97%A8%E7%A6%81%E8%A6%81%E6%B1%82.md)
4. 昇腾（Ascend）社区下项目测试用例的贡献与常规代码提交合入标准保持一致，具体请参考 [PR提交指南](https://gitcode.com/Ascend/community/blob/master/docs/contributor/pr-guide.md)
5. 昇腾（Ascend）社区中不同项目通常对测试用例有一定规则约束（命名、组织形式等），开发者贡献时可以参考代码仓下已有用例文件或项目SIG提供的相关说明文档

## 工具

昇腾（Ascend）社区推荐使用以下通用的测试工具与框架，**算子开发等其他特殊场景，遵循对应项目的框架要求**

| 编程语言   | 测试工具/框架         |
|--------|-----------------|
| C&C++  | GoogleTest      |
| Python | unittest/pytest |
| Golang | GoConvey        |
