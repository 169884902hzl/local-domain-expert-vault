---
title: "RoboAgent: Chaining Basic Capabilities for Embodied Task Planning"
tags: [VLM, RL, robot-learning, planning]
created: "2026-05-06"
updated: "2026-05-06"
type: "literature"
status: "done"
summary: "提出 capability-driven 的具身任务规划框架 RoboAgent，用单一 VLM（Qwen2.5-VL-3B）同时实现调度器和 5 个子能力（EG/OG/SD/AD/ES），通过三阶段训练（专家 SFT → DAgger SFT → 专家引导 RFT）在 ALFWorld 和 EB-ALFRED 上达到 SOTA。"
authors: "Xu, Peiran; Zheng, Jiaqi; Mu, Yadong"
year: "2026"
venue: "arXiv Preprint"
zotero_key: "KZUDDZCH"
---
## 摘要

This paper focuses on embodied task planning, where an agent acquires visual observations from the environment and executes atomic actions to accomplish a given task. Although recent Vision-Language Models (VLMs) have achieved impressive results in multimodal（多模态） understanding and reasoning, their performance remains limited when applied to embodied planning that involves multi-turn interaction, long-horizon（长时序） reasoning, and extended context analysis. To bridge this gap, we propose RoboAgent, a capability-driven planning pipeline in which the model actively invokes different sub-capabilities. Each capability maintains its own context, and produces intermediate reasoning results or interacts with the environment according to the query given by a scheduler. This framework decomposes complex planning into a sequence of basic vision-language problems that VLMs can better address, enabling a more transparent and controllable reasoning process. The scheduler and all capabilities are implemented with a single VLM, without relying on external tools. To train this VLM, we adopt a multi-stage paradigm that consists of: (1) behavior cloning with expert plans, (2) DAgger training using trajectories collected by the model, and (3) reinforcement learning（强化学习） guided by an expert policy. Across these stages, we exploit the internal information of the environment simulator to construct high-quality supervision for each capability, and we further introduce augmented and synthetic data to enhance the model's performance in more diverse scenarios. Extensive experiments on widely used embodied task planning benchmarks validate the effectiveness of the proposed approach. Our codes will be available at https://github.com/woyut/RoboAgent_CVPR26.

## 中文简述

提出基于强化学习的操控方法，具有长时序任务特点。

**研究方向**: 视觉-语言模型、强化学习、机器人学习、运动规划

## 关键贡献

1. **Capability-driven 规划管线**：将复杂规划分解为 5 个基本视觉-语言子能力（EG/OG/SD/AD/ES），每个能力维护独立上下文，由中央调度器协调调用，使推理过程透明可控
2. **三阶段训练范式**：结合专家轨迹 SFT → DAgger 式 SFT（利用模型生成数据 + 仿真器内部信息构建纠正监督）→ EIPO 强化微调（专家引导策略优化）
3. **全流程单一 VLM 实现**：调度器和所有能力均由同一个端到端可训练的 VLM 实现，不依赖外部工具
4. **跨模态、跨域泛化**：同一模型在视觉环境和文本环境均表现优秀，且能跨仿真器泛化
## 结构化提取

- **Problem**: VLM 在具身任务规划中的多轮交互、长时序推理和扩展上下文处理能力不足，现有 CoT/RL 方法的推理链缺乏原则性监督
- **Method**: Capability-driven planning pipeline，单一 VLM 实现调度器 + 5 个子能力（EG/OG/SD/AD/ES），三阶段训练（Expert SFT → DAgger SFT → EIPO RFT）
- **Tasks**: 具身任务规划（导航 + 物体操控），包括 pick, clean, heat, cool, examine, slice, place 等操作
- **Sensors**: RGB egocentric 图像（300×300 / 500×500），文本观察模式（物体列表 + 动作反馈）
- **Robot Setup**: AI2-THOR / Habitat / VirtualHome 仿真器中的虚拟智能体，固定原子动作空间
- **Metrics**: Success Rate (SR), Subgoal Success Rate (SSR)
- **Limitations**: 跨仿真器域差距大；依赖仿真器特权信息；能力集固定；未做真实机器人实验；3B 模型规模限制
- **Evidence Notes**:

  - EB-ALFRED: SR 67.0%（超越 WAP-7B 的 62.7% 和 GPT-4o 的 56.3%），在 Visual(78) 和 Long(80) 分数上特别突出
  - ALFWorld 视觉模式: SR 77.6%（远超 SEEA-R1 的 36.0% 和 GPT-4o 的 24.0%），Pick 类别达 92%
  - ALFWorld 文本模式: seen 92.1%, unseen 94.0%（与 DynaMind-Qwen2.5-7B 相当）
  - OOD 跨域: EB-Habitat 22.3%, LoTa-WAH SSR 22.1%（开源最优但远低于闭源）
  - 消融: DAgger 阶段是 ALFWorld 提升的关键（+28.3%），RFT 阶段进一步提升 4.5%
  - EIPO vs GRPO: EIPO 收敛更快、最终 SR 更高
## 本地引用关系

-
## 证据元数据

- Fulltext Quality: fulltext
- Evidence Coverage: 完整覆盖（正文全部章节 + 附录关键细节）
- Confidence: high
- Summary: 提出 capability-driven 的具身任务规划框架 RoboAgent，用单一 VLM（Qwen2.5-VL-3B）同时实现调度器和 5 个子能力（EG/OG/SD/AD/ES），通过三阶段训练（专家 SFT → DAgger SFT → 专家引导 RFT）在 ALFWorld 和 EB-ALFRED 上达到 SOTA。


## Problem

具身任务规划（Embodied Task Planning, ETP）中，VLM 需要在多轮交互、长时序推理和扩展上下文分析的条件下生成动作序列。现有方法的推理链缺乏原则性表述和直接监督，难以确保推理的可靠性和对决策的实用性。


## Method

### 架构设计
- **调度器（Scheduler）**：接收任务指令，维护历史上下文，输出 CoT 推理 + 能力调用序列
- **5 个子能力**：
  - **EG（Exploration Guidance）**：根据场景布局常识预测目标物体最可能的探索方向
  - **OG（Object Grounding）**：开放词汇目标检测，判断当前视野中是否有目标物体，输出 JSON 格式 bbox
  - **SD（Scene Description）**：生成目标物体的文本描述（位置、状态、与其他物体的关系）
  - **AD（Action Decoding）**：将导航/操控命令翻译为可执行的原子动作序列（分 exploration 和 manipulation 两种模式）
  - **ES（Experience Summarization）**：总结最近动作序列的执行结果，分析失败原因

### 训练流程
**Stage 1: 专家 SFT**
- 利用 ALFRED 训练集的专家轨迹，通过 LLM 解析指令提取关键物体
- 将专家轨迹分解为交替的 exploration 和 manipulation 子计划
- 利用仿真器内部信息（场景图、分割掩码、环境反馈）构建每个能力的 GT 监督
- 生成 640K 训练样本

**Stage 2: DAgger SFT**
- 部署 Stage 1 模型收集新轨迹（成功+失败）
- 为模型生成的每个能力调用构建纠正性 GT（基于语义匹配 + 仿真器信息）
- 数据增强：物体同义词替换、描述短语替换、动作重述、跨域物体替换
- 生成 690K 样本

**Stage 3: 专家引导 RFT（EIPO）**
- 提出 Expert-Induced Policy Optimization（EIPO）算法
- 利用专家策略计算优势函数 A_{π*}，避免 MC 估计的方差问题
- 引入 GRPO 式组内平均作为 baseline，使"相对更好"的动作获得正梯度
- 合成 25K 轨迹用于训练

### 基座模型
Qwen2.5-VL-3B


## Experiments

### 基准和环境
- **EB-ALFRED**（EmbodiedBench 视觉环境，基于 AI2-THOR）
- **ALFWorld**（文本+视觉双模式环境）
- **EB-Habitat**（OOD 视觉环境）
- **LoTa-WAH**（OOD 文本环境，基于 VirtualHome）

### 主要结果

**EB-ALFRED（SR%）**
| 方法 | 基座 | Avg | Base | Common | Complex | Visual | Spatial | Long |
|------|------|-----|------|--------|---------|--------|---------|------|
| Claude-3.7-Sonnet | - | 67.7 | 68 | 68 | 70 | 68 | 62 | 70 |
| WAP | Qwen2.5-VL-7B | 62.7 | 66 | 62 | 70 | 56 | 52 | 70 |
| **RoboAgent** | **Qwen2.5-VL-3B** | **67.0** | **72** | 48 | 64 | **78** | **60** | **80** |

**ALFWorld 视觉模式（SR%）**
| 方法 | 基座 | Avg |
|------|------|-----|
| SEEA-R1 | Qwen2.5-VL-7B | 36.0 |
| GPT-4o | - | 24.0 |
| **RoboAgent** | **Qwen2.5-VL-3B** | **77.6** |

**ALFWorld 文本模式（SR%）**
| 方法 | seen | unseen |
|------|------|--------|
| DynaMind | 92.5 | 89.1 |
| **RoboAgent** | **92.1** | **94.0** |

### 消融实验
| 配置 | AW (SR%) | EB (SR%) |
|------|----------|----------|
| SFT-expert only | 44.8 | 62.0 |
| + DAgger (model-generated) | 73.1 | 64.3 |
| + RFT (aug. syn.) | **77.6** | **67.0** |

关键发现：
- DAgger 训练对 ALFWorld 提升巨大（44.8 → 73.1），证明纠正性监督对能力学习的重要性
- RFT 阶段需要数据增强和合成轨迹才能有效，仅用专家数据效果有限
- EIPO 比 GRPO 收敛更快、最终性能更高

### OOD 泛化
- EB-Habitat（不同仿真器）：SR 22.3%，低于闭源模型（GPT-4o: 59.0%），但在开源模型中最佳
- LoTa-WAH（不同仿真器）：SSR 22.1%，显著优于同等规模的 LLaMA-7B（3.7%）


## Limitations

1. **跨仿真器域差距仍显著**：在 OOD 环境（EB-Habitat, LoTa-WAH）中与闭源模型存在明显差距，仿真器间域差异仍然很大
2. **依赖仿真器内部信息**：训练利用了场景图、分割掩码等特权信息（inference 时不可用），限制了方法在真实世界的直接迁移
3. **能力集固定**：5 个能力是预定义的，未探索动态演化的能力集合
4. **仅在仿真环境验证**：未涉及真实机器人实验
5. **小模型基座**：使用 3B 参数的 VLM，能力边界可能受限于模型规模


## Key Takeaways

### 与我们研究的相关性
1. **capability decomposition 思路可借鉴**：将复杂的具身规划拆分为可独立训练和监督的子能力，每个能力有明确的输入/输出接口。这种思路对 DLO 操控中的长时序任务规划有启发——可以定义 DLO 特有的子能力（如形状评估、抓取点选择、轨迹规划）
2. **仿真器特权信息用于训练**：利用场景图等仿真器内部信息构建高质量 GT 监督信号，这种"训练时有特权信息、推理时不需要"的范式在 Sim-to-Real 迁移中很有价值
3. **多阶段训练管线有效**：SFT → DAgger → RFT 的渐进式训练策略，在稀疏奖励长时序任务上显著优于纯 RL 方法
4. **小模型 + 好方法 > 大模型通用方法**：3B 模型通过精心设计的方法在特定任务上超越 72B 模型和 GPT-4o，说明领域特化的训练策略的重要性

### 局限性对 DLO 操控的启示
- 该方法不涉及真实机器人实验，且依赖固定动作空间，与 DLO 操控中连续动作控制的需求有差距
- 能力定义偏向室内导航和简单操控（pick/place/heat 等），对柔性物体操控的复杂动力学尚未覆盖

## 相关概念

- [[vision-language-model]]
- [[reinforcement-learning]]
- [[robot-learning]]
- [[planning]]
- [[sim-to-real]]
- [[deformable-linear-object]]
- [[bimanual-manipulation]]
- [[grasping]]

## 相关研究者

- [[xu-peiran|Xu, Peiran]]
