# 社区 Roadmap 编写与发布指导

使用 Gitcode Issue 对各组织的规划和中长期目标进行追踪和管理。本文档对社区各项目编写 Roadmap 类 Issue 给出参考和规范，以帮助制定和维护高质量的 Roadmap。

以下是一个完整的Roadmap Issue示例，展示了所有推荐元素的实际应用。建议先浏览此示例以获得整体印象，再阅读后续的详细规范说明。

```markdown
创建Issue名称：[Roadmap] MindSpeed Core Roadmap 2026 Q1

--- 
# MindSpeed Core Roadmap 2026 Q1

本季度重点聚焦长序列并行能力增强、FSDP 训练能力构建及文档体系优化，持续提升训练性能、生态兼容性与开发易用性。

## Focus

- Long Sequence: 增强 KV Allgather CP 并行能力与 CP 代码可维护性
- FSDP Capability: 构建 FSDP2 训练后端与 Attn+MoE 端到端训练方案
- Documentation: 系统化优化资料结构与贡献合规文档

## Long Sequence Enhancement

- [ ] **KV Allgather CP 并行方案支持**
Goal: 支持 KV Allgather CP 并行方案
Issue: [相关Issue链接]  

- [ ] **CP 代码重构与接口对齐**
Goal: 完成 CP 代码重构，接口对齐 TE，提升 VeRL 等生态库接入易用性
Issue: [相关Issue链接] 

## FSDP Capability

- [ ] **基于 FSDP2 的训练后端搭建**
Goal: 搭建基于 FSDP2 方案的训练后端，支持 HuggingFace 模型直接接入并与 mcore 解耦
Issue: [相关Issue链接] 

- [ ] **Attn(FSDP) + MoE(EP+FSDP) 训练方案**
Goal: 基于 Qwen 及 QwenVL 系列构建端到端训练能力
Issue: [相关Issue链接] 

## Documentation Optimization

- [ ] **资料文档结构优化 [🙋 Help Wanted]**
Goal: 调整现有资料文档结构，开展系统性文档优化，补充贡献指南、目录结构、文档 license 等合规性相关内容
Issue: [相关Issue链接] 

```

## 1. 标题格式

**格式：** `[Roadmap] <项目名称> Roadmap <时间范围>`，按季度发布使用Q1/Q2/Q3/Q4标记，半年度发布使用H1/H2标记

**示例：**

- `[Roadmap] MindSpeed Core Roadmap 2026 Q1`

## 2. 顶层内容

### 2.1 开场描述（可选）

提供项目概述、愿景或总体方向简述。

### 2.2 Focus/重点聚焦部分

列出本周期最关键的3-5个聚焦方向，建议按照项目的**功能领域**或**技术模块**进行分组，涵盖全局视角：

```markdown
## Focus

• New feature & function: 新特性与新功能开发...
• Feature compatibility & reliability: 完整兼容性和生产级可靠性...
• Usability: 易用性改进...
• Kernel optimization: 内核优化...
• Reinforcement learning: 强化学习框架集成...
• Multimodal: 多模态增强...
```

**特点：**

- 概括和整体性描述当前周期当前项目的主要发展方向，不需要详细展开

## 3. 主要功能模块章节

### 3.1 章节划分原则

按照项目的**功能领域**或**技术模块**进行分组，如：

- **Base Engine Features** - 基础引擎特性
- **Parallelism** - 并行处理
- **Server Reliability** - 服务器可靠性
- **Kernel** - 内核优化

### 3.2 每个模块的结构

每个模块下包含多个**具体工作项**，格式如下：

```markdown
## [模块名称]

- [ ] **工作项名称/功能描述**
Goal: [目标描述]
Owner: @GitCodeID      [可选]
Issue: [相关Issue链接]   [可选]
PR: [相关PR链接]         [可选]

- [ ] **另一个工作项**
Goal: [目标描述]
Owner: @GitCodeID      [可选]
Issue: [相关Issue链接]   [可选]
PR: [相关PR链接]         [可选]
```

## 4. 关键元数据字段

每个工作项应包含的关键信息：

### 4.1 Goal

- **含义**：工作目标或简短描述
- **用途**：说明该工作项的目标
- **例子**：`Goal: 支持在代码仓配置流水线`

### 4.2 Owner

- **含义**：责任人
- **格式**：`Owner: @GitCodeID`
- **用途**：明确谁负责或主导该工作项
- **例子**：`Owner: @zhangsan`

### 4.3 Issue

- **含义**：关联的Gitcode Issue
- **格式**：`Issue: <Issue链接>`
- **用途**：追踪详细设计和讨论
- **例子**：`Issue: https://gitcode.com/Ascend/community/issues/8`

### 4.4 PR（Pull Request）

- **含义**：相关的实现PR
- **格式**：`PR: <PR链接>`
- **用途**：链接实现工作
- **例子**：`PR: https://gitcode.com/Ascend/community/pull/270`

## 5. 可选补充内容

### 5.1 🙋 Help Wanted 标记

对于希望社区开发者重点参与贡献的工作项，建议使用 **[🙋 Help Wanted]** 标记进行标识：

```markdown
- [ ] **工作项名称 [🙋 Help Wanted]**
Goal: [目标描述]
Owner: TBD
Issue: #123
```

### 5.2 Sub-issues

在Roadmap Issue底部列出跨周期关联的Roadmap Issue或大型工作项的拆分Issue。

**与工作项Issue字段的区别：**

- **工作项中的Issue字段**：链接的是具体工作项的详细设计、讨论或跟踪Issue
- **Sub-issues章节**：用于关联其他周期的Roadmap Issue（如上一季度未完成的工作），或将大型工作项拆分为多个独立追踪的子Issue

```markdown
## Sub-issues

[xxx Roadmap (2025 Q4) #12780](link)  <!-- 关联上季度Roadmap -->
[Feature X Phase 2 #12800](link)      <!-- 大型工作项的拆分 -->
```
