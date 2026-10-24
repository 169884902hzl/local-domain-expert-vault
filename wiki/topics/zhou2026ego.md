---
title: "Ego to world: Collaborative spatial reasoning in embodied systems via reinforcement learning"
tags: [manipulation, imitation, VLM, RL, robot-learning]
created: "2026-05-08"
updated: "2026-05-08"
type: "literature"
status: "done"
summary: "提出 E2W 多视角空间推理基准和 CoRL（SFT+GRPO）训练框架，通过 Cross-View Spatial Reward 实现多智能体 ego-centric 视角融合，在计数、空间关系推理和抓取任务上超越 GPT-5 等闭源模型。"
authors: "Zhou, Heng; Kang, Li; Qin, Yiran; Song, Xiufeng; Yu, Ao et al."
year: "2026"
venue: "arXiv Preprint"
zotero_key: "XP8Z3TBP"
---
## 摘要

Understanding the world from distributed, partial viewpoints is a fundamental challenge for embodied multi-agent systems. Each agent perceives the environment through an ego-centric view that is often limited by occlusion and ambiguity. To study this problem, we introduce the Ego-to-World (E2W) benchmark, which evaluates a vision-language model（视觉-语言模型）'s ability to fuse heterogeneous viewpoints across three tasks: (i) global counting, (ii) relational location reasoning, and (iii) action-oriented grasping（抓取） that requires predicting view-specific image coordinates. To address this setting, we propose CoRL, a two-stage framework that combines Chain-of-Thought supervised fine-tuning with reinforcement learning（强化学习） using Group-Relative Policy Optimization. Its core component, the Cross-View Spatial Reward（奖励） (CVSR), provides dense task-aligned feedback by linking reasoning steps to visual evidence, ensuring coherent cross-view entity resolution, and guiding the model toward correct final predictions. Experiments on E2W show that CoRL consistently surpasses strong proprietary and open-source baselines on both reasoning and perception-grounding metrics, while ablations further confirm the necessity of each CVSR component. Beyond that, CoRL generalizes to external spatial reasoning benchmarks and enables effective real-world multi-robot manipulation（机器人操控） with calibrated multi-camera rigs, demonstrating cross-view localization and successful grasp-and-place execution. Together, E2W and CoRL provide a principled foundation for learning world-centric scene understanding from distributed, ego-centric observations, advancing collaborative embodied AI.

## 中文简述

提出基于强化学习的抓取方法，具有泛化能力特点。

**研究方向**: 机器人操控、模仿学习、视觉-语言模型、强化学习、机器人学习

## 关键贡献

1. **形式化协作感知问题**：首次将多智能体 ego-centric 视角融合的空间推理问题形式化，定义了"协作空间推理"任务设置
2. **E2W 基准**：提出 Ego-to-World (E2W) Benchmark，包含三项任务（全局计数 E2W-1、空间关系推理 E2W-2、抓取定位 E2W-3），覆盖 100k+ 仿真和 60k+ 真实样本，15k+ 场景，50+ 物体类别
3. **CoRL 框架**：两阶段训练（SFT → RL/GRPO），核心是 Cross-View Spatial Reward (CVSR)，通过 grounding、overlap、answer 三个子奖励提供密集的空间对齐信号
4. **跨基准泛化和真实机器人验证**：CoRL-7B 在 Where2Place 上超越 RoboPoint，在真实双臂 + 移动底座平台上实现 65% 抓取成功率
## 结构化提取

- **Problem**: 多智能体具身系统中，如何融合分布式 ego-centric 局部视角实现全局空间推理和精确抓取
- **Method**: CoRL — 两阶段 SFT(CoT) + RL(GRPO)，核心是 Cross-View Spatial Reward (CVSR)，包含 grounding（匈牙利匹配 IoU）、overlap（跨视角实体消解）、answer（任务正确性）三个子奖励
- **Tasks**: (1) 全局计数 E2W-1, (2) 空间关系推理 E2W-2, (3) 抓取定位 E2W-3（预测 2D 坐标）
- **Sensors**: RGB ego-centric 相机（仿真：RoboFactory/ManiSkill3 多智能体环境；真实：Intel RealSense D435 RGB-D）
- **Robot Setup**: 两台 Franka Research 3 机械臂 + 一台 Realman 移动底座；每台配备 RGB-D 相机；开放回路执行流程：CoRL 预测坐标 → SAM2 分割 → AnyGrasp 抓取姿态 → Deoxys 控制器
- **Metrics**: QA 任务用 exact match accuracy；抓取任务用归一化距离分数（0-100）；Where2Place 用空间预测得分
- **Limitations**: 静态同步观测、集中式 VLM 架构、无动态场景、2D 坐标空间、物体类别有限、真实抓取成功率有限
- **Evidence Notes**: 全文可获取。主实验 Table 1 对比闭源/开源/SFT/RL-ZERO/CoRL 共 12 个模型；消融 Table 2 验证 4 个 CVSR 组件；Table 3 多视角 vs 单视角对比；Table 4 Where2Place 泛化和真实机器人评估。所有数据均来自论文原文。
## 本地引用关系

-
## 证据元数据

- Fulltext Quality: fulltext
- Evidence Coverage: complete（全文从 arXiv 获取，包含正文、附录、实验表格）
- Confidence: high
- Summary: 提出 E2W 多视角空间推理基准和 CoRL（SFT+GRPO）训练框架，通过 Cross-View Spatial Reward 实现多智能体 ego-centric 视角融合，在计数、空间关系推理和抓取任务上超越 GPT-5 等闭源模型。


## Problem

多智能体具身系统中，每个智能体仅有 ego-centric 局部视角，受遮挡和视角歧义限制。核心问题：如何让 VLM 融合多个分布式 ego-centric 观测，实现全局一致的场景理解、空间推理和精确抓取预测？现有方法（如 COMBO）假设共享全局状态，回避了跨视角实体消解的难题。


## Method

### 整体架构
CoRL 框架采用两阶段训练：

**Stage 1: Supervised Fine-Tuning (SFT)**
- 基于 Chain-of-Thought (CoT) 标注数据训练
- 训练格式：(x, q, r, a)，x 为多视角输入，q 为查询，r 为推理链，a 为最终答案
- 标准 next-token log-likelihood 损失
- 3 epochs, cosine-decay, peak lr=2e-5, batch_size=4, grad_accum=4

**Stage 2: Reinforcement Learning (GRPO)**
- 基于 Group Relative Policy Optimization (GRPO) 进行微调
- 每个 input 采样 G=8 个候选响应，计算 group-relative advantage
- Clipped surrogate + KL 正则化（β=0.04, ε=0.2）
- RL 训练 200 steps, lr=1e-6
- 硬件：8× NVIDIA H200

### Cross-View Spatial Reward (CVSR)
总奖励：R = λ₁ R_format + λ₂ R_CVSR (λ₁=0.1, λ₂=1.0)

CVSR = w_ground × R_ground + w_overlap × R_overlap + w_ans × R_ans

权重：w_ans=0.7, w_ground=0.1, w_overlap=0.2

- **R_ground（定位奖励）**：预测关键物体的 bounding box，通过匈牙利算法做最优二部匹配，计算平均 IoU，提供密集定位信号
- **R_overlap（重叠准确度）**：要求模型报告在多个视角中出现的唯一物体实例数量，与真实值比较（二元奖励），驱动跨视角实体消解
- **R_ans（答案正确性）**：QA 任务用精确匹配（二元），抓取任务用距离衰减奖励（d_max=100 pixels）
- **R_format（格式奖励）**：输出结构正确性（推理过程在 `<think/>` 标签中），二元奖励

### Backbone
基于 Qwen2.5-VL-Instruct（3B/7B）


## Experiments

### 主实验（Table 1: E2W-Bench）

| Model | E2W-1 | E2W-2(S) | E2W-2(R) | Reasoning Avg | E2W-3(S) | E2W-3(R) | Perception Avg |
|-------|-------|----------|----------|---------------|----------|----------|----------------|
| GPT-5 | 42.5 | 48.5 | 72.5 | 54.50 | 50.43 | 12.02 | 31.23 |
| Gemini-2.5-Pro | 32.5 | 42.5 | 50.0 | 41.67 | 35.98 | 10.15 | 23.07 |
| Qwen2.5VL-32B | 21.5 | 28.0 | 37.0 | 28.83 | 31.25 | 9.16 | 20.21 |
| 7B+SFT | 44.5 | 88.0 | 84.5 | 72.33 | 90.99 | 40.76 | 65.88 |
| 7B+RL-ZERO | 16.0 | 56.0 | 82.5 | 51.50 | 92.60 | 11.65 | 52.13 |
| **CoRL-7B** | **61.0** | **97.0** | **90.0** | **82.67** | 95.69 | **44.32** | **70.01** |

关键发现：
- CoRL-7B Reasoning 平均 82.67%，远超 GPT-5 的 54.50%
- SFT 提供强基线，RL 在其基础上进一步提升（特别是 E2W-1 从 44.5→61.0）
- RL-ZERO（无 SFT 初始化）表现差，证明 SFT 冷启动必要性
- 闭源模型在 Perception (E2W-3) 上普遍较弱，暴露了精细空间 grounding 的不足

### 消融实验（Table 2: CVSR 组件）

| Setting | E2W-1 | E2W-2(S) | E2W-3(S) |
|---------|-------|----------|----------|
| CoRL (full) | 61.0 | 97.0 | 95.69 |
| w/o R_ans | 10.5 | 15.5 | 40.32 |
| w/o R_ground | 50.5 | 90.5 | 74.32 |
| w/o R_overlap | 56.5 | 90.0 | 84.31 |
| w/o R_format | 58.5 | 93.0 | 89.31 |

- R_ans 最为关键（去掉后 E2W-1 从 61→10.5）
- R_ground 对抓取定位影响最大（-21 points）
- R_overlap 对计数和关系推理有稳定提升
- 所有组件互补，缺一不可

### 多视角 vs 单视角（Table 3）

| Setting | E2W-1 | E2W-2(S) |
|---------|-------|----------|
| 7B Single-view | 34.0 | 54.0 |
| 7B Multi-view | **61.0** | **97.0** |

多 ego-centric 视角持续优于单全局视角，因为近距离视角提供更丰富的几何细节，避免了透视畸变。

### 外部基准：Where2Place（Table 4 left）
- CoRL-7B: **50.9**
- RoboPoint: 46.8
- Molmo-7B: 45.0
- SpaceLLaVA: 11.8

跨视角训练的单图像空间 grounding 能力也得到保持。

### 真实机器人评估（Table 4 right）
- 蓝色方块抓取：CoRL-7B **65%** vs RoboPoint 0%
- 杨桃对齐抓取：CoRL-7B **30%** vs RoboPoint 0%

主要失败模式：空间推理正确但坐标预测落在物体边缘（非推理错误）。

### 数据集规模
- E2W-1 (Counting): 30k 仿真样本
- E2W-2 (Location Reasoning): 35k 仿真 + 25k 真实 = 60k
- E2W-3 (Grasping): 35k 仿真 + 35k 真实 = 70k
- 每个任务 200 测试样本，1000 冷启动样本
- 训练集/测试集场景不重叠


## Limitations

1. **静态同步快照**：当前框架假设所有智能体的观测是同步的静态快照，未处理异步传感和时序推理
2. **集中式架构**：单一 VLM 处理所有视角，存在通信开销和单点故障问题，大规模智能体场景的可扩展性未验证
3. **无动态场景**：不处理移动物体或动态智能体场景，需要跨时间+跨视角的追踪和重识别
4. **2D 坐标空间**：坐标预测仅在 2D 图像空间，未利用深度信息进行完整 3D 空间 grounding
5. **物体类别有限**：50+ 类别虽有一定覆盖，但真实环境的长尾分布需要更强的领域不变表示
6. **真实机器人成功率有限**：E2W-3(R) 真实世界抓取仅 44.32%，主要因坐标精度不足


## Key Takeaways

1. **多 ego-centric 视角 > 单全局视角**：近距离互补观测比完整但远距离的全局视角更有效，这对多机器人协作系统的传感器布局设计有启示
2. **SFT+RL 两阶段训练的必要性**：SFT 提供推理先验，RL 在此基础上精炼空间一致性，缺少任何一环都显著下降
3. **CVSR 奖励设计可迁移**：跨视角 grounding + overlap + answer 的奖励组合具有通用性，可适配其他多视角空间推理任务
4. **与 DLO 操控的关联**：虽然本文聚焦刚性物体，但其多视角融合和空间 grounding 的方法论可启发 DLO 场景中的多相机协同观测与操控方案
5. **开放回路抓取的局限**：真实部署采用开放回路（无闭环修正），坐标预测精度仍有限，实际应用需要结合闭环控制

## 相关概念

- [[robotic-manipulation]]
- [[imitation-learning]]
- [[vision-language-model]]
- [[reinforcement-learning]]
- [[robot-learning]]
- [[deformable-linear-object]]
- [[bimanual-manipulation]]
- [[grasping]]

## 相关研究者

- [[zhou-heng|Zhou, Heng]]
- [[kang|Kang, Li]]
