---
title: "ROSClaw: A hierarchical semantic-physical framework for heterogeneous multi-agent collaboration"
tags: [manipulation, imitation, VLM, RL, sim-to-real]
created: "2026-05-10"
updated: "2026-05-10"
type: "literature"
status: "done"
summary: "提出三层语义-物理架构 ROSClaw，通过 e-URDF 物理约束和数字孪生前置仿真实现异构多机器人协作，支持策略学习与任务执行的统一闭环。"
authors: "Zhao, Rongfeng; Zhang, Xuanhao; Guo, Zhaochen; Shao, Xiang; Zhu, Zhongpan et al."
year: "2026"
venue: "arXiv Preprint"
zotero_key: "7492FQVB"
---
## 摘要

The integration of large language models (LLMs) with embodied agents has improved high-level reasoning capabilities; however, a critical gap remains between semantic understanding and physical execution. While vision-language-action (VLA) and vision-language-navigation (VLN) systems enable robots to perform manipulation（操控） and navigation tasks from natural language instructions, they still struggle with long-horizon（长时序） sequential and temporally structured tasks. Existing frameworks typically adopt modular pipelines for data collection, skill training, and policy deployment, resulting in high costs in experimental validation and policy optimization. To address these limitations, we propose ROSClaw, an agent framework for heterogeneous robots that integrates policy learning and task execution within a unified vision-language model（视觉-语言模型） (VLM) controller. The framework leverages e-URDF representations of heterogeneous robots as physical constraints to construct a sim-to-real（仿真到真实迁移） topological mapping, enabling real-time access to the physical states of both simulated and real-world agents. We further incorporate a data collection and state accumulation mechanism that stores robot states, multimodal（多模态） observations, and execution trajectories during real-world execution, enabling subsequent iterative policy optimization. During deployment, a unified agent maintains semantic continuity between reasoning and execution, and dynamically assigns task-specific control to different agents, thereby improving robustness in multi-policy execution. By establishing an autonomous closed-loop（闭环） framework, ROSClaw minimizes the reliance on robot-specific development workflows. The framework supports hardware-level validation, automated generation of SDK-level control programs, and tool-based execution, enabling rapid cross-platform transfer and continual improvement of robotic skills. Ours project page: https://www.rosclaw.io/.

## 中文简述

提出基于模仿学习的导航方法，具有仿真到真实迁移特点。

**研究方向**: 机器人操控、模仿学习、视觉-语言模型、强化学习、仿真到真实迁移

## 关键贡献

1. **ROSClaw 系统架构**：跨越信息空间、软件系统、物理世界的三层语义-物理框架，将大模型宏观知识引擎与底层高频物理控制解耦，在单一 agent 循环内集成策略学习与长时序任务执行。
2. **e-URDF 物理约束 + 数据采集与状态累积机制**：基于 Isaac Lab 构建无头数字孪生沙盒，在指令下发物理资源池之前，通过 e-URDF 表示进行碰撞检测和关节力矩验证，严格约束物理边界；同时持续记录执行轨迹和任务状态，存入本地资源池以支持后续策略优化。
3. **异构多智能体真实世界验证**：在人形机器人、固定机械臂、移动操控平台上验证，展示共享环境中的鲁棒协作，包括移动操控、导航和精确操作。
## 结构化提取

- **Problem**: 语义理解与物理执行之间的断层；异构多机器人系统中策略学习与任务执行的模块化割裂；缺乏闭环数据反馈机制。
- **Method**: 三层语义-物理架构（认知层 LLM/VLM + 协调自动化层 OpenClaw/Online Tool Pool + 物理世界层 ROS 统一控制），e-URDF 物理约束前置验证（Isaac Lab 数字孪生），Local Resource Pool 数据采集与状态累积。
- **Tasks**: 异构多机器人协作（移动操控 + 导航 + 精确抓取）；云台多智能体编舞编排。
- **Sensors**: RealSense 相机（RGB-D）；头部摄像头（人形机器人）；VLM 感知 API（桌面水果检测）；DINO-X API（抓取候选点生成）。
- **Robot Setup**: 4 台异构机器人——移动机械臂（轮式底盘 + 双指夹爪）、人形机器人（头部摄像头 + 双手）、固定机械臂、移动操控系统。环境：智能家居 ~60㎡，厨房+客厅。
- **Metrics**: 未提供定量指标（成功率、精度、完成时间等）。仅给出云台编舞生成时间约 3 分钟的定性数据。
- **Limitations**: 仅结构化/半动态环境评估；闭环学习未完成；无定量 baseline 对比；URDF 精度依赖；跨场景泛化未验证。
- **Evidence Notes**: 论文以系统展示为主，提供了详细的任务执行流程描述和示意图（Fig.3-5），但缺少定量实验结果。e-URDF 物理防火墙的有效性通过任务成功完成间接验证，未报告拦截/误报统计。
## 本地引用关系

-
## 证据元数据

- Fulltext Quality: fulltext
- Evidence Coverage: 完整覆盖全文（Introduction、Related Work、Framework Overview、Validation、Conclusion），无缺失章节
- Confidence: high
- Summary: 提出三层语义-物理架构 ROSClaw，通过 e-URDF 物理约束和数字孪生前置仿真实现异构多机器人协作，支持策略学习与任务执行的统一闭环。


## Problem

LLM 与具身智能体的集成提升了高层推理能力，但**语义理解与物理执行之间存在根本性缺口**。具体表现为：

1. **语义-物理断层**：现有 VLA/VLN 系统在长时序（long-horizon）顺序任务中易出错累积，现有分层框架缺乏显式物理约束，导致大模型生成物理不可行的任务计划。
2. **模块化管线割裂**：数据采集、策略训练、部署被拆分为独立阶段，引入语义和分布不一致，且强依赖手动环境重置。
3. **异构平台碎片化**：不同机器人 SDK 和接口不统一，工程师需大量硬件级调优，限制了可扩展性和复用性。
4. **缺乏闭环数据反馈**：物理交互经验未被转化为可复用知识，系统无法持续自我改进。


## Method

### 整体架构：三层语义-物理体系

```
认知层 (Cognitive Layer)
  ↕ 双向反馈
协调自动化层 (Coordination Automation Layer)
  ↕ e-URDF 物理拦截
ROSClaw 物理世界 (Physical World)
```

### 认知层（Cognitive Layer）
- 由 LLM 和 VLM 组成，作为高层决策引擎
- 负责低频任务分解、长时序推理、环境语义理解
- **双向交互范式**：不仅向协调层下发结构化语义表示和任务计划，同时接收来自物理世界的执行反馈、环境状态和交互结果
- 通过与真实数据的迭代交互，逐步将语义推理与物理执行对齐

### 协调自动化层（Coordination Automation Layer）
- 核心系统 **OpenClaw**，负责任务逻辑抽象和自动化工具编排
- **Online Tool Pool**：聚合各机器人 SDK、MCP（Model Context Protocol）和多系统 API 接口，作为"数字字典"将抽象指令映射为可执行软件调用
- **e-URDF 物理防护**：在动作下发物理世界之前，通过数字孪生引擎（Isaac Lab）进行前向动力学仿真和碰撞检测，确保物理可行性

### ROSClaw 物理世界（Physical World）
- 接口高频 ROS 和平台特定驱动，统一控制异构智能体
- **Local Resource Pool（本地资源池）**：核心创新之一
  - 执行过程中实时采集机器人物理状态
  - 调用 Online Tool Pool 连接物理传感器获取数据
  - 多模态观测 + 成功的长时序执行轨迹标准化后存入资源池
  - 形成可复用技能表示，支持持续策略精炼和跨场景泛化
  - 可上传至云端模型资源池用于大规模模型微调/训练

### 关键技术机制
- **异步解耦**：低频语义规划与高频物理控制分离，实现不同时间尺度的稳定交互
- **Task Execution Supervision (TES)**：任务执行监督机制
- **"Train once, deploy everywhere"范式**：通过 Online Tool Pool 实现跨平台泛化


## Experiments

### 实验环境
- 智能家居环境（厨房 + 客厅，约 60 平方米）
- 包含 3 张桌子、1 个水槽、6 个橱柜、1 个冰箱
- 空间划分为 S1（移动操控区）、S2（定点抓取区）、S3（移动导航区）

### 任务 1：时序任务多机器人协作操作

**参与机器人**：
- 移动机械臂（轮式底盘 + 双指夹爪）→ 移动操控
- 人形机器人（头部摄像头）→ 感知 + 导航 + 物品运输
- 固定机械臂 → 精确抓取

**任务流程**：
1. ROSClaw 分析用户需求，根据可达区域分配任务
2. 移动机械臂靠近门，用臂开门，然后移开
3. 人形机器人进入客厅，靠近桌子，拿起果篮等待
4. ROSClaw 通过 VLM 感知桌面水果（数量、类别），调用 DINO-X API 生成抓取候选点
5. 固定机械臂抓取用户指定的猕猴桃放入果篮（组间协作）
6. 人形机器人沿导航轨迹将果篮从客厅桌子运到厨房水槽

### 任务 2：e-URDF 物理防护与数据采集验证

**固定机械臂操作组**：
- 用户远程交互对话："桌上有什么水果？"
- ROSClaw 激活 RealSense 相机，通过 VLM API 感知桌面环境
- 系统以结构化列表返回水果颜色、类别、相对固定臂的 3D 位置
- 根据用户指令分解任务为可执行步骤，同时回传关键执行轨迹和感知结果

**云台多智能体编排组**：
- 用户："我想看云台跳舞"
- ROSClaw 实例化云台 agent，调用音乐生成模型生成 ~20 秒音乐
- 启动 Isaac Lab，创建 MCP 服务接口物理云台单元，注册到 Online Tool Pool
- 在 Isaac Lab 中加载云台 URDF 模型，持续验证自动编排舞蹈动作的物理安全性
- 连接 7 个物理云台单元执行编排的舞蹈动作
- **结果**：多云台协调舞蹈行为生成时间约 3 分钟，人工参与仅限于初始指令

### 量化结果
- **未提供定量 benchmark 对比表**。论文以系统展示和任务完成度为主，未给出成功率、精度等数值指标。这是明确的证据缺口。


## Limitations

1. **评估环境局限**：当前评估主要在结构化或半动态环境中进行，尚未建立处理高频干扰、感知噪声和模型随机性的系统性框架。
2. **闭环学习未完成**：Local Resource Pool 实现了数据累积，但尚未形成将数据采集与自主策略优化紧密结合的闭环学习系统。
3. **缺少定量对比**：未与 baseline 方法（如纯 LLM 规划、传统分层架构）进行定量比较实验。
4. **鲁棒性未验证**：未在高度非结构化环境中测试系统的鲁棒性。
5. **泛化性存疑**：仅展示了特定智能家居场景，跨场景泛化能力未经证实。


## Key Takeaways

1. **e-URDF 物理约束表示**：将异构机器人 URDF 模型集成到数字孪生中作为物理约束层，在 LLM 输出与物理执行之间设置"防火墙"。这种设计思路可借鉴到 DLO 操控中——将线缆的物理模型作为约束前置验证。
2. **Online Tool Pool 概念**：统一抽象异构机器人 SDK/API 的方案值得关注，但其"数字字典"映射机制的具体实现细节（如如何自动发现和注册新工具）未充分说明。
3. **数据采集与状态累积**：将多模态观测和执行轨迹标准化存入本地资源池的思路，与 DLO 操控中的数据复用需求契合，但该论文的闭环学习尚未真正实现。
4. **对 DLO/VLM 研究的启示有限**：论文聚焦异构多机器人协作的系统工程问题，而非操控方法本身。对 VLM-based control 的贡献更多在系统集成层面。
5. **Sim-to-Real 思路**：e-URDF + Isaac Lab 的前置仿真验证是实用的 Sim-to-Real 安全策略，但依赖准确的 URDF 建模，对 DLO 等可变形物体难以直接应用。

## 相关概念

- [[robotic-manipulation]]
- [[imitation-learning]]
- [[vision-language-model]]
- [[reinforcement-learning]]
- [[sim-to-real]]
- [[deformable-linear-object]]
- [[bimanual-manipulation]]
- [[grasping]]

## 相关研究者

- [[zhao-rongfeng|Zhao, Rongfeng]]
