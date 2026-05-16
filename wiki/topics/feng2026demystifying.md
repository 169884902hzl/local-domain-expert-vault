---
title: "Demystifying action space design for robotic manipulation policies"
tags: [manipulation, imitation, robot-learning, DLO, bimanual]
created: "2026-04-29"
updated: "2026-04-29"
type: "literature"
status: "done"
summary: "首个大规模系统性研究动作空间设计（时间轴：absolute vs delta；空间轴：joint vs task space）对模仿学习策略性能的影响，基于 13000+ 真实 rollouts 和 500+ 训练模型，证明 chunk-wise delta + joint space 在单硬件平台上最优，task space 在跨体态迁移场景中占优。"
authors: "Feng, Yuchun; Zheng, Jinliang; Wang, Zhihao; Liu, Dongxiu; Li, Jianxiong et al."
year: "2026"
venue: "arXiv Preprint"
zotero_key: "24X3RVD6"
---
## 摘要

The specification of the action space plays a pivotal role in imitation-based robotic manipulation（机器人操控） policy learning, fundamentally shaping the optimization landscape of policy learning. While recent advances have focused heavily on scaling training data and model capacity, the choice of action space remains guided by ad-hoc heuristics or legacy designs, leading to an ambiguous understanding of robotic policy design philosophies. To address this ambiguity, we conducted a large-scale and systematic empirical study, confirming that the action space does have significant and complex impacts on robotic policy learning. We dissect the action design space along temporal and spatial axes, facilitating a structured analysis of how these choices govern both policy learnability and control stability. Based on 13,000+ real-world rollouts on a bimanual（双臂） robot and evaluation on 500+ trained models over four scenarios, we examine the trade-offs between absolute vs. delta representations, and joint-space vs. task-space parameterizations. Our large-scale results suggest that properly designing the policy to predict delta actions consistently improves performance, while joint-space and task-space representations offer complementary strengths, favoring control stability and generalization, respectively.

## 中文简述

提出基于模仿学习的绳索操控方法，具有泛化能力特点。

**研究方向**: 机器人操控、模仿学习、机器人学习、可变形物体操控、双臂操控

## 关键贡献

1. **动作空间分类法**：沿空间轴（joint space vs task space）和时间轴（absolute vs delta）正交分解动作空间设计空间，建立了系统性的分析框架
2. **chunk-wise vs step-wise delta 理论分析**：Proposition 4.1 证明 step-wise delta 的误差放大随 horizon k 线性增长（O(k)），而 chunk-wise delta 保持常数界 O(1)
3. **大规模实证基准**：13000+ 真实 rollouts、500+ 训练模型、4 个平台（单臂 AgileX、双臂 AgileX、AIRBOT、RoboTwin 2.0）、14 个任务
4. **设计指南**：
   - 执行 horizon k 须与时间抽象匹配（delta 短 horizon、absolute 长 horizon）
   - 单硬件平台最优：joint space + chunk-wise delta
   - 跨体态/迁移学习：task space 更优（embodiment-invariant）
   - Flow-matching 模型在 joint space 上表现尤其突出
5. **跨验证实验**：数据规模（100/250/500 demos）、训练时长（300-1200 epochs）、多任务学习、跨体态迁移、π0 foundation model 微调，全面验证结论鲁棒性
## 结构化提取

- Problem: 模仿学习策略的动作空间设计缺乏系统性理解和共识，现有研究依赖 ad-hoc 经验，影响可复现性和基础模型发展
- Method: 沿时间轴（absolute/delta）和空间轴（joint/task space）正交分解动作空间，用 Regression 和 Flow Matching 两种策略骨干，在 4 个硬件平台上系统对比 8 种动作空间配置
- Tasks: Touch Cube（精度验证）, Pick Up Cup（接触动力学）, Pick & Place（序列任务）, Bimanual Cube Transfer（双臂协调）, RoboTwin 2.0 10 个仿真任务
- Sensors: 第三人称相机 + 腕部相机（双臂平台每臂各一个）
- Robot Setup: AgileX PiPER 6-DoF 单臂、AgileX PiPER 双臂、AIRBOT 6-DoF（跨体态）、RoboTwin 2.0 仿真（AgileX embodiment）
- Metrics: Progress Score（分级评分，0-1）、Success Rate（仿真）、3 次独立试验 × 10 rollouts 统计显著性
- Limitations: 未覆盖高 DoF/动态/灵巧操作；固定分类法未探索混合表示；chunking horizon 仍为启发式；仅 position-based 控制
- Evidence Notes: 完整正文 + 附录，包含详细统计表、跨验证实验、理论证明。Table 1 主结果、Table H.1-H.3 详细统计、Fig. 3-6 分析图。所有结论均有充分实验支撑。
## 本地引用关系

-
## 证据元数据

- Fulltext Quality: fulltext（arXiv HTML 完整抓取，含所有正文、附录、表格）
- Evidence Coverage: 高（完整覆盖方法、实验、理论证明、附录统计）
- Confidence: high
- Summary: 首个大规模系统性研究动作空间设计（时间轴：absolute vs delta；空间轴：joint vs task space）对模仿学习策略性能的影响，基于 13000+ 真实 rollouts 和 500+ 训练模型，证明 chunk-wise delta + joint space 在单硬件平台上最优，task space 在跨体态迁移场景中占优。


## Problem

模仿学习策略的动作空间设计对策略性能有决定性影响，但研究社区缺乏共识和系统性理解。现有工作多依赖 ad-hoc 经验或继承旧代码库的配置，导致"state-of-the-art"结果常与特定但未文档化的控制选择混淆。需要大规模实证研究来建立统一的动作空间设计指南。


## Method

- **策略架构**：FiLM-conditioned ResNet-18 视觉编码器 + 6 层 Transformer decoder，支持两种生成范式：
  - Regression-based（MSE loss，即 ACT 变体）
  - Flow Matching-based（velocity field 学习，即 Diffusion Policy 变体）
- **时间抽象**：
  - Absolute（0阶）：策略直接预测目标状态
  - Delta（1阶）：策略预测增量，分 chunk-wise（相对 chunk 起始状态）和 step-wise（相对前一步预测）
- **空间抽象**：
  - Joint space：直接输出关节位置
  - Task space：输出末端执行器位姿，经 IK 转换为关节命令
- **Action Chunking**：默认 k=60 训练（2 秒 @30Hz），推理时 delta 用 k=30、absolute 用 k=60
- **评估协议**：6×6 网格覆盖空间初始化，每实验 3 独立试验 × 10 rollouts，报告 progress score
- **理论工具**：线性化分析 total transformation T_total = (I_k ⊗ S_t) M_time，研究谱性质对稳定性的影响


## Experiments

### 数据集与平台
| 平台 | 类型 | 任务数 | Demo 数/任务 |
|------|------|--------|-------------|
| 单臂 AgileX PiPER | 真实 | 3（Touch Cube, Pick Cup, Pick & Place） | 100/250/500 |
| 双臂 AgileX PiPER | 真实 | 1（Bimanual Transfer） | 250 |
| AIRBOT | 真实 | 1（Touch Cube，跨体态） | 250 |
| RoboTwin 2.0 | 仿真（hard mode） | 10 | 50 |

### 主要结果（Table 1，单臂 AgileX，250 demos，600 epochs）
| 配置 | ACT avg | DP avg |
|------|---------|--------|
| abs-EE | 69.0 | 74.0 |
| **delta-EE** | 89.6 | 91.4 |
| abs-Joint | 77.3 | 85.0 |
| **delta-Joint** | 88.0 | **95.9** |

- delta 在所有配置下一致优于 absolute（平均提升 10-20 个百分点）
- Joint space + delta（DP）达到最高 95.9%
- Flow-matching 在 joint space 上优势尤为明显

### 关键发现
1. **Chunk-wise delta > Step-wise delta**：差距达 10%+，理论证明 step-wise 的 O(k) 误差放大
2. **Delta 一致最优**：跨所有平台、任务、模型变体、数据规模、训练时长
3. **Joint space 整体更鲁棒**：但 task space 在低数据/短训练下可竞争
4. **Flow-matching + Joint space 组合最强**：flow-matching 能更好捕捉 joint space 的复杂多模态分布
5. **跨体态/迁移学习时 task space 反转**：task space 的 embodiment-invariant 性质使其在跨机器人场景中更优
6. **数据规模效应**：joint space 从更多数据和更长训练中获益更大

### 仿真验证（RoboTwin 2.0, 10 tasks avg）
- delta-Joint(DP): 48.0% > delta-EE(DP): 37.0% > abs-Joint(ACT): 40.0% > abs-EE(ACT): 26.7%
- 趋势与真实实验一致


## Limitations

1. **不涵盖高自由度系统**：未验证 humanoid 或多指手等高 DoF 场景的结论泛化性
2. **不涵盖动态/灵巧操作**：如乒乓球、布料折叠等动态任务可能对 action latency 和 horizon coupling 有不同约束
3. **固定分类法**：未探索混合/自适应动作空间（如根据任务阶段动态切换表示）
4. **Action chunking 理论不完整**：horizon 选择仍为启发式，缺乏严格的理论指导
5. **未研究 force/torque 级控制**：仅限 position-based 控制器
6. **跨体态验证范围有限**：仅 AgileX vs AIRBOT 两种形态


## Key Takeaways

1. **对 DLO 操控的启示**：双臂 DLO 操作属于需要精细协调的接触丰富任务，推荐使用 joint space + chunk-wise delta 作为基线。但若需要 Sim-to-Real 迁移或跨机器人部署，应考虑 task space 的 embodiment-invariant 优势
2. **Flow-matching 在 joint space 上的优势**：DLO 操控中 joint space 的多模态分布更复杂，flow-matching 比 regression 更适合捕捉这种结构
3. **Horizon 调节策略**：delta 动作用短 horizon（快速纠正）、absolute 用长 horizon（全局一致性）——这对长时序 DLO 任务（如绳索打结）的 horizon 选择有直接指导意义
4. **评估方法论参考**：6×6 网格空间覆盖 + 多独立试验的评估协议值得在 DLO 操控实验中采用
5. **Action space 不是实现细节而是核心设计**：在比较不同方法时应严格控制动作空间变量

## 相关概念

- [[robotic-manipulation]]
- [[imitation-learning]]
- [[robot-learning]]
- [[deformable-linear-object]]
- [[bimanual-manipulation]]
- [[vision-language-model]]
- [[diffusion-model]]
- [[grasping]]

## 相关研究者

- [[feng-yuchun|Feng, Yuchun]]
- [[zheng-jinliang|Zheng, Jinliang]]
