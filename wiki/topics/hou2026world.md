---
title: "World model for robot learning: A comprehensive survey"
tags: [RL, robot-learning, physics-simulation, planning]
created: "2026-05-16"
updated: "2026-05-16"
type: "literature"
status: "done"
summary: "以机器人学习为中心的世界模型综述，按架构范式（IDM/单骨干/MoE/统一VLA/隐空间）分类梳理世界模型与策略的耦合方式，系统总结世界模型作为仿真器（RL训练+评估）和视频世界模型的四阶段能力演进，并覆盖导航、自动驾驶、数据集和评测基准。"
authors: "Hou, Bohan; Li, Gen; Jia, Jindou; An, Tuo; Guo, Xinying et al."
year: "2026"
venue: "arXiv Preprint"
zotero_key: "H6NFKZBE"
---
## 摘要

World models, which are predictive representations of how environments evolve under actions, have become a central component of robot learning. They support policy learning, planning, simulation, evaluation, data generation, and have advanced rapidly with the rise of foundation models and large-scale video generation. However, the literature remains fragmented across architectures, functional roles, and embodied application domains. To address this gap, we present a comprehensive review of world models from a robot-learning perspective. We examine how world models are coupled with robot policies, how they serve as learned simulators for reinforcement learning（强化学习） and evaluation, and how robotic video world models have progressed from imagination-based generation to controllable, structured, and foundation-scale formulations. We further connect these ideas to navigation and autonomous driving, and summarize representative datasets, benchmarks, and evaluation protocols. Overall, this survey systematically reviews the rapidly growing literature on world models for robot learning, clarifies key paradigms and applications, and highlights major challenges and future directions for predictive modeling in embodied agents. To facilitate continued access to newly emerging works, benchmarks, and resources, we will maintain and regularly update the accompanying GitHub repository alongside this survey.

## 中文简述

提出基于强化学习的导航方法。

**研究方向**: 强化学习、机器人学习、物理仿真、运动规划

## 关键贡献

1. 提出 policy-centric 的世界模型综述视角，聚焦预测模型如何与 VLA 策略耦合以支持动作生成、规划、仿真、评估和数据生成
2. 建立精细的分类体系：将世界模型-策略耦合分为 IDM 式解耦、单骨干统一、MoE/MoT 专家融合、统一 VLA 和隐空间世界建模五大架构范式
3. 从概率视角统一理解：策略模型、被动世界模型、可控世界模型和逆动力学模型可视为同一联合预测-控制分布的不同边际或条件查询
4. 系统梳理世界模型作为仿真器的两大功能角色：RL 训练环境 + 策略评估/排名器，并提出仿真器-策略共进化范式
5. 按能力四阶段组织机器人视频世界模型文献：想象式生成 → 动作可控生成 → 结构感知生成 → 基础规模世界模型
6. 覆盖导航和自动驾驶领域的世界模型应用
7. 总结代表性数据集、评测基准和实验结果，提供 LIBERO/RoboTwin/CALVIN/SIMPLER 上的系统比较
8. 讨论六大挑战和未来方向：因果条件差距、效率瓶颈、多模态感知瓶颈、经典控制集成、符号结构集成、评估指标缺失
## 结构化提取

- Problem: 机器人世界模型文献在架构范式、功能角色和应用领域上高度碎片化，缺乏从策略学习角度的系统性分类
- Method: 综述论文；按架构范式（IDM/单骨干/MoE/统一VLA/隐空间）和功能角色（策略耦合/仿真器/视频生成）组织文献
- Tasks: 机械臂操控（LIBERO, RoboTwin, CALVIN）、导航（室内）、自动驾驶
- Sensors: 以视觉（RGB/多视角）为主，部分涉及深度、触觉、力觉
- Robot Setup: 涵盖单臂、双臂、人形机器人、移动操控平台
- Metrics: 任务成功率、长时域一致性、动作忠实度、策略排名保真度
- Limitations: 因果条件差距、效率瓶颈、多模态感知不足、评估标准不统一、长时域误差累积
- Evidence Notes: 完整精读全文 8 个章节，覆盖全部架构范式、仿真器应用、视频世界模型演进、导航/自动驾驶应用、数据集/基准/实验结果比较、挑战与未来方向。所有结论均基于原文内容，未编造任何证据。
## 本地引用关系

- [[hou2026world]]
## 证据元数据

- Fulltext Quality: fulltext
- Evidence Coverage: high（完整精读 195K 字符综述全文，覆盖全部 8 个章节）
- Confidence: high
- Summary: 以机器人学习为中心的世界模型综述，按架构范式（IDM/单骨干/MoE/统一VLA/隐空间）分类梳理世界模型与策略的耦合方式，系统总结世界模型作为仿真器（RL训练+评估）和视频世界模型的四阶段能力演进，并覆盖导航、自动驾驶、数据集和评测基准。


## Problem

机器人策略学习领域近年来快速发展，但纯反应式 VLA 策略在复杂物理环境中面临长时域推理、时间信用分配和复合误差等挑战。世界模型作为环境动态的预测性表示，可以为策略学习、规划、仿真、评估和数据生成提供支持。然而，现有文献在架构、功能角色和应用领域上高度碎片化，缺乏一个从机器人学习视角出发的系统性综述。


## Method

综述论文，无单一方法论。核心组织框架如下：

### 概率统一视角（Section 3.1）
将策略模型、世界模型、逆动力学模型统一为联合分布 p(o_{t+1:t+k}, a_{t+1:t+k} | o_t, l) 的不同查询方式：
- 策略模型：对 o 积分，得 p(a|o,l)
- 被动世界模型：对 a 积分，得 p(o|o,l)
- 可控世界模型：p(o|o,a)
- 逆动力学模型：p(a|o:o+k)

### 架构范式分类（Section 3.2-3.6）
1. **IDM 式**：世界模型先生成未来观测，独立逆动力学模块从中恢复动作（UniPi, VPP, MimicVideo, Gen2Act 等）
2. **单骨干式**：单一生成骨干联合建模视频和动作，通过去噪/流匹配统一目标训练（UVA, UWA, Cosmos Policy, DreamZero 等）
3. **MoE/MoT 式**：保持视频/动作专家分离参数化，通过共享注意力/交叉注意力交互（GE-Act, Motus, LingBot-VA, BagelVLA 等）
4. **统一 VLA**：未来预测内化于统一多模态策略骨干（GR-1, UP-VLA, WorldVLA, DreamVLA, UniVLA 等）
5. **隐空间世界建模**：避免像素空间生成，在表征空间内化未来动态（FLARE, VLA-JEPA, JEPA-VLA, WoG, DIAL）

### 世界模型作为仿真器（Section 4）
- **RL 训练**：世界模型作为学习环境替代真实交互，支持 GRPO 式策略优化（World-Env, VLA-RFT, WMPO, PlayWorld 等）
- **策略评估**：通过想象 rollout 排名/筛选候选策略或动作序列（GPC, WorldEval, WorldArena, DreamPlan 等）
- **共进化范式**：策略和世界模型迭代相互改进（World-VLA-Loop, VLAW, WoVR）

### 视频世界模型能力演进（Section 5）
1. 想象式生成：为策略学习提供额外监督（Dreamitate, RoboDreamer, DreamGen）
2. 动作可控：强调生成未来对动作的忠实度（IRASim, Ctrl-World, EnerVerse-AC）
3. 结构感知：引入 mask/几何/多视角等交互先验（Mask2IV, TesserAct, RoboVIP）
4. 基础规模：将大规模视频骨干适配为可复用世界模型（Vid2World, DreamDojo, GigaWorld-0, Cosmos Predict 2.5）

### 数据集与评测（Section 7）
- 数据集多维度比较：涵盖 OXE, DROID, BridgeData V2, AgiBot World, RoboMIND 2.0 等
- 三类评测基准：开环预测质量、闭环任务效用、物理一致性/可控性/可执行性诊断
- LIBERO 四套件上最强方法达 98.5% 平均成功率（Cosmos Policy, LingBot-VA）


## Experiments

综述论文，不包含原创实验。但系统汇总了代表性方法在标准基准上的结果：

### LIBERO 基准（Table 5）
| 方法组 | Spatial | Object | Goal | Long | Avg |
|--------|---------|--------|------|------|-----|
| Cosmos Policy (单骨干) | 98.1 | 100.0 | 98.2 | 97.6 | 98.5 |
| LingBot-VA (MoE) | 98.5 | 99.6 | 97.2 | 98.5 | 98.5 |
| Say-Dream-ACT (IDM) | 99.4 | 99.2 | 98.6 | 95.4 | 98.1 |
| VLA-JEPA (隐空间) | 96.2 | 99.6 | 97.2 | 95.8 | 97.2 |
| DreamVLA (统一VLA) | 97.5 | 94.0 | 89.5 | 89.5 | 92.6 |

### 关键发现
- 强性能不限于单一架构范式，各范式均可达到竞争力表现
- Long 套件是关键分水岭，暴露长时域鲁棒性差异
- 跨基准（LIBERO vs RoboTwin vs CALVIN）泛化仍有限，说明当前世界模型对实体形态和动作空间敏感


## Limitations

1. **因果条件差距**：许多世界模型的预测更多依赖历史上下文和任务意图而非具体机器人动作，导致生成未来在语义上合理但与候选动作的物理后果不一致
2. **效率瓶颈**：视频生成和扩散去噪的训练和推理开销远大于标准 VLA，实时部署困难
3. **多模态感知瓶颈**：当前世界模型主要依赖视觉和本体感受，缺乏触觉、力觉等接触信号的集成
4. **经典控制集成不足**：学习动态与形式化控制保证（如 Lyapunov 稳定性）的融合仍不成熟
5. **符号结构缺失**：像素/隐空间预测在长时域推理中面临误差累积，符号化抽象（对象中心、关系化）可作为互补但尚在早期
6. **评估标准不统一**：缺乏功能感知的标准化评测框架，视觉保真度与控制效用之间的关联仍弱
7. 作为综述论文，未提供新的实验验证或方法贡献


## Key Takeaways

1. **世界模型的核心价值不在于视觉逼真度，而在于动作一致性和控制实用性**：对 DLO 操控等接触密集任务，物理一致性比像素保真度更重要
2. **隐空间世界建模是值得关注的轻量化方向**：避免昂贵的像素空间生成，直接在表征空间内化未来动态（如 VLA-JEPA, WoG），适合 DLO 等需要高频控制的场景
3. **仿真器-策略共进化范式有潜力**：世界模型和策略迭代相互改进（VLAW, WoVR），对 Sim-to-Real 场景特别有吸引力
4. **长时域操控仍是核心挑战**：LIBERO Long 套件上方法间差距最大，对 DLO 长序列操控（如打结、绕线）有直接启示
5. **多模态感知是下一步关键方向**：触觉和力反馈的集成对 DLO 操控中摩擦、刚度估计至关重要
6. **五种架构范式提供了不同灵活度-集成度的权衡**：DLO 操控可能更适合 MoE/隐空间范式，因为它们可以在保留专业化处理的同时融入物理先验

## 相关概念

- [[reinforcement-learning]]
- [[robot-learning]]
- [[sim-to-real]]
- [[planning]]
- [[vision-language-model]]
- [[deformable-linear-object]]
- [[bimanual-manipulation]]

## 相关研究者

- [[hou|Hou, Bohan]]
