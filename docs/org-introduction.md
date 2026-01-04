
# 昇腾Ascend开源软件仓库

面向开发者提供基于华为昇腾Ascend AI处理器的应用使能、训推加速、集群管理、工具链等全栈开源软件，让开发者可以便捷高效的编写在昇腾Ascend硬件设备上运行的人工智能应用程序。

<table style="width:100%">
  <tr>
    <th style="width:10%;text-align:center;"><span style="font-size:17px;">项目</span></th>
    <th style="width:75%;text-align:center;"><span style="font-size:17px;">简介</span></th>
  </tr>
  <tr>
    <td>
      <a href="https://gitcode.com/Ascend/AscendNPU-IR"><span style="font-size:16px;">AscendNPU IR</span></a><br>
    </td>
    <td><span style="font-size:16px;"><b>AscendNPU IR</b> 是基于 MLIR 构建的，面向昇腾亲和算子编译时使用的中间表示，提供昇腾完备表达能力，通过编译优化提升昇腾AI处理器计算效率，支持通过生态框架使能昇腾AI处理器与深度调优。</span></td>
  </tr>
  <tr>
    <td>
      <span style="font-size:16px;">MindIE</span><br>
      <a href="https://gitcode.com/Ascend/MindIE-SD"><span style="font-size:16px;">- MindIE SD</span></a><br>
      <a href="https://gitcode.com/Ascend/MindIE-LLM"><span style="font-size:16px;">- MindIE LLM</span></a><br>
      <a href="https://gitcode.com/Ascend/MindIE-Motor"><span style="font-size:16px;">- MindIE Motor</span></a><br>
      <a href="https://gitcode.com/Ascend/MindIE-Turbo"><span style="font-size:16px;">- MindIE Turbo</span></a><br>
    </td>
    <td>
      <span style="font-size:16px;"><b>MindIE SD</b> 是 MindIE 的视图生成推理模型套件，它的目标是为稳定扩散（Stable Diffusion）系列大模型提供在昇腾硬件及其软件栈上的端到端推理解决方案。该软件系统内部集成了各功能模块，并对外提供统一的编程接口。</span><br>
      <span style="font-size:16px;"><b>MindIE LLM</b> 是MindIE下的大语言模型推理组件，基于昇腾硬件提供业界通用大模型推理能力，同时提供多并发请求的调度功能，支持Continuous Batching、Page Attention、FlashDecoding等加速特性，使能用户高性能推理需求。</span><br>
      <span style="font-size:16px;"><b>MindIE Motor</b> 是面向通用模型场景的推理服务化框架，通过开放、可扩展的推理服务化平台架构提供推理服务化能力，支持对接业界主流推理框架接口，满足大语言模型的高性能推理需求。</span><br>
      <span style="font-size:16px;"><b>MindIE Turbo</b> 是基于NPU芯片的大语言模型推理引擎加速插件库，旨在承载自研的大语言模型优化算法及推理引擎相关优化。</span><br>
    </td>
  </tr>
  <tr>
    <td>
      <span style="font-size:16px;">MindSpeed</span><br>
      <a href="https://gitcode.com/Ascend/MindSpeed"><span style="font-size:16px;">- MindSpeed Core</span></a><br>
      <a href="https://gitcode.com/Ascend/MindSpeed-MM"><span style="font-size:16px;">- MindSpeed-MM</span></a><br>
      <a href="https://gitcode.com/Ascend/MindSpeed-LLM"><span style="font-size:16px;">- MindSpeed-LLM</span></a><br>
      <a href="https://gitcode.com/Ascend/MindSpeed-RL"><span style="font-size:16px;">- MindSpeed-RL</span></a><br>
      <a href="https://gitcode.com/Ascend/MindSpeed-Core-MS"><span style="font-size:16px;">- MindSpeed-Core-MS</span></a><br>
    </td>
    <td>
      <span style="font-size:16px;"><b>MindSpeed Core</b> 是针对华为昇腾设备的大模型加速库。</span><br>
      <span style="font-size:16px;"><b>MindSpeed MM</b> 是面向大规模分布式训练的昇腾多模态大模型套件，支持业界主流多模态大模型训练，旨在为华为 昇腾芯片 提供端到端的多模态训练解决方案, 包含预置业界主流模型，数据工程，分布式训练及加速，预训练、微调、后训练、在线推理任务等特性。</span><br>
      <span style="font-size:16px;"><b>MindSpeed LLM</b> 是基于昇腾生态的大语言模型分布式训练框架，旨在为华为 昇腾芯片 生态合作伙伴提供端到端的大语言模型训练方案，包含分布式预训练、分布式指令微调以及对应的开发工具链，如：数据预处理、权重转换、在线推理、基线评估等。</span><br>
      <span style="font-size:16px;"><b>MindSpeed RL</b> 是基于昇腾生态的强化学习加速框架，旨在为华为 昇腾芯片 生态合作伙伴提供端到端的RL训推解决方案，支持超大昇腾集群训推共卡/分离部署、多模型异步流水调度、训推异构切分通信等核心加速能力。</span><br>
      <span style="font-size:16px;"><b>MindSpeed-Core-MS</b> 是连接华为自研AI框架MindSpore+华为昇腾大模型加速解决方案MindSpeed的重要组件，旨在提供华为全栈易用的端到端的自然语言模型以及多模态模型训练解决方案。</span>
    </td>
  </tr>
  <tr>
    <td>
      <span style="font-size:16px;">MindSeriesSDK</span><br>
      <a href="https://gitcode.com/Ascend/RecSDK"><span style="font-size:16px;">- RecSDK</span></a><br>
    </td>
    <td><span style="font-size:16px;">提供昇腾AI处理器加速的各类AI软件开发套件（SDK），提供极简易用的API，加速高性能AI应用的开发，赋能千行百业。</span></td>
  </tr>
  <tr>
    <td >
      <span style="font-size:16px;">MindStudio</span><br>
      <a href="https://gitcode.com/Ascend/mstt"><span style="font-size:16px;">- mstt</span></a><br>
      <a href="https://gitcode.com/Ascend/msit"><span style="font-size:16px;">- msit</span></a><br>
      <a href="https://gitcode.com/Ascend/msot"><span style="font-size:16px;">- msot</span></a><br>
    </td>
    <td ><span style="font-size:16px;"><b>MindStudio</b> 是面向昇腾AI开发者提供的全流程工具链，致力于提供端到端的昇腾AI应用开发解决方案，使能开发者高效完成训练开发、推理开发和算子开发</span></td>
  </tr>
  <tr>
    <td>
      <a href="https://gitcode.com/Ascend/mind-cluster"><span style="font-size:16px;">MindCluster</span></a><br>
    </td>
    <td><span style="font-size:16px;"><b>MindCluster</b> 是支持NPU（昇腾AI处理器）构建的深度学习系统组件，专为训练和推理任务提供集群级解决方案。深度学习平台开发厂商可以减少底层资源调度相关软件开发工作量，快速使能合作伙伴基于MindCluster开发深度学习平台。</span></td>
  </tr>
</table>

## 关于社区

## 参与贡献

  - [社区会议日历](https://meeting.osinfra.cn/ascend)
  - [开源协作指南](./role-guidance.md)
  - [机器人使用指南](https://gitcode.com/Ascend/infrastructure/blob/master/docs/robot/robot%E4%BD%BF%E7%94%A8%E6%8C%87%E5%8D%97.md)
  - [FAQ](./FAQ/infra-faq.md)
  - [Code of Conduct](../docs/contributor/code-of-conduct.md)

## 相关链接

- [昇腾社区](https://www.hiascend.com/)
