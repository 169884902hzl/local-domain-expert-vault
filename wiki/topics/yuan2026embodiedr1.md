---
title: "Embodied-R1: Reinforced embodied reasoning for general robotic manipulation"
tags: [manipulation, imitation, VLM, RL, robot-learning]
created: "2026-05-03"
updated: "2026-05-03"
type: "literature"
status: "done"
summary: "提出 \"pointing\" 作为统一的具身无关中间表征，定义四种指向能力(REG/RRG/OFG/VTG)，基于 Qwen2.5-VL-3B 构建 Embodied-R1，通过两阶段 GRPO 强化微调在 11 个基准和真实机器人任务上实现 SOTA 零样本操控。"
authors: "Yuan, Yifu; Cui, Haiqin; Huang, Yaoting; Chen, Yibin; Ni, Fei et al."
year: "2026"
venue: "arXiv Preprint"
zotero_key: "FHNQDJGZ"
---
## 摘要

Generalization in embodied AI is hindered by the "seeing-to-doing gap," which stems from data scarcity and embodiment（具身） heterogeneity. To address this, we pioneer "pointing" as a unified, embodiment（具身）-agnostic intermediate representation, defining four core embodied pointing abilities that bridge high-level vision-language comprehension with low-level action primitives. We introduce Embodied-R1, a 3B Vision-Language Model（视觉-语言模型） (VLM) specifically designed for embodied reasoning and pointing. We use a wide range of embodied and general visual reasoning datasets as sources to construct a large-scale dataset, Embodied-Points-200K, which supports key embodied pointing capabilities. We then train Embodied-R1 using a two-stage Reinforced Fine-tuning (RFT) curriculum with a specialized multi-task（多任务） reward（奖励） design. Embodied-R1 achieves state-of-the-art（现有最优方法） performance on 11 embodied spatial and pointing benchmarks. Critically, it demonstrates robust zero-shot（零样本） generalization by achieving a 56.2% success rate in the SIMPLEREnv and 87.5% across 8 real-world XArm tasks without any task-specific fine-tuning, representing a 62% improvement over strong baselines. Furthermore, the model exhibits high robustness against diverse visual disturbances. Our work shows that a pointing-centric representation, combined with an RFT training paradigm, offers an effective and generalizable pathway to closing the perception-action gap in robotics.

## 中文简述

提出基于视觉-语言的操控方法，具有零样本泛化特点。

**研究方向**: 机器人操控、模仿学习、视觉-语言模型、强化学习、机器人学习

## 关键贡献

1. **提出 "pointing" 作为统一的具身无关中间表征**，定义四种核心指向能力（REG、RRG、OFG、VTG），桥接高层视觉语言理解与低层动作原语
2. **构建 Embodied-Points-200K 数据集**，包含约 20 万高质量样本，覆盖四种指向能力，采用 "问题-验证" 对而非传统 "问题-答案" 对的格式以适配 RFT
3. **提出 Embodied-R1**（3B 参数），基于 Qwen2.5-VL 架构，通过两阶段 GRPO 强化微调训练，在 11 个空间推理和指向基准上达到 SOTA
4. **实现零样本机器人操控**：SIMPLEREnv 56.2% 成功率、真实 XArm 8 任务 87.5% 成功率，较强 baseline 提升 62%，无需任务特定微调
## 结构化提取

- Problem: VLM 的 "seeing-to-doing gap"，即无法将视觉感知可靠转化为机器人动作；数据稀缺和具身异构性是根本原因
- Method: 基于 Qwen2.5-VL-3B 的 Embodied-R1，定义四种指向能力（REG/RRG/OFG/VTG），两阶段 GRPO 强化微调，多任务混合奖励设计
- Tasks: 空间推理（15 个子任务）、指向定位（REG/RRG/OFG）、视觉轨迹生成（VTG）、机器人桌面操控（SIMPLEREnv 4 任务 + XArm 8 任务）
- Sensors: RGB 相机（主），RGB-D 相机（RGBD 变体），Intel RealSense L515 LiDAR 相机（真实世界，640×480，第三人称视角）
- Robot Setup: WidowX 臂（SIMPLEREnv 仿真），xArm 6（真实世界 8 任务），AhaRobot 双臂（泛化测试）
- Metrics: 多选准确率（空间推理），点在 mask 准确率（REG/RRG/OFG），RMSE/MAE/LLM Score（VTG），抓取成功率和任务成功率（操控）
- Limitations: 未与学习型策略集成；无长时序任务分解；pointing 表征对力控/扭转/DLO 不够；RGB-D 融合尚不成熟
- Evidence Notes: 全文精读，所有关键实验数据均从原文表格直接提取。附录 E 的 limitations 提供了作者自己对方法局限性的坦诚评估。
## 本地引用关系

-
## 证据元数据

- Fulltext Quality: fulltext (HTML version from arXiv, all sections including appendices read)
- Evidence Coverage: high (abstract, introduction, full method, all experiments, ablations, conclusion, appendix E limitations all covered)
- Confidence: high
- Summary: 提出 "pointing" 作为统一的具身无关中间表征，定义四种指向能力(REG/RRG/OFG/VTG)，基于 Qwen2.5-VL-3B 构建 Embodied-R1，通过两阶段 GRPO 强化微调在 11 个基准和真实机器人任务上实现 SOTA 零样本操控。


## Problem

机器人操控中的 "seeing-to-doing gap"：VLM 虽具备强大的视觉感知能力，但无法可靠地将感知理解转化为有效的机器人动作。根本原因有两个：
1. **数据稀缺**：有限的具身数据不足以将语言/视觉与物理动作充分对齐
2. **具身异构性**：不同机器人形态阻碍了知识迁移

现有 VLA 方案的不足：
- **端到端 VLA**（如 OpenVLA）：动作模态与预训练网络空间数据存在根本不匹配，导致知识遗忘和任务冲突
- **模块化 VLA**（如 SoFar）：依赖多模型级联，容易产生级联失败、推理延迟高、缺乏全局场景空间理解
- **Affordance VLA**（如 FSD, RoboPoint）：视觉辅助信号类型有限，SFT 训练的 CoT 推理模板僵化，泛化能力受限


## Method

### 模型架构
- 基座模型：**Qwen2.5-VL-3B-Instruct**
- 组成：ViT 视觉编码器 + Projector + LLM
- 输入：多模态输入 x=(I, Q)，I 为图像，Q 为文本指令
- 输出：自回归生成文本响应 y，包含推理过程和坐标预测

### 四种指向能力
所有能力统一输出图像上的坐标点 p=(p,q)∈[0,w]×[0,h]：

1. **REG (Referring Expression Grounding)**：通过语言描述定位物体，在对应 mask 内生成一个点
2. **RRG (Region Referring Grounding)**：根据关系语言识别空间区域（如"杯子和碗之间的空间"），在自由空间中生成放置点
3. **OFG (Object Functional Grounding)**：识别物体的功能显著部位（affordance），如刀柄
4. **VTG (Visual Trace Generation)**：生成有序点序列 τ={p_t | t=1,2,...,T}，形成以物体为中心的操控轨迹（agent-agnostic）

### 数据构建
- **Stage 1 数据**：
  - Embodied-Spatial-84K：来自 SAT 和 WhatsUp 基准，统一为多选格式
  - ViRL-subset-18K：通用知识数据，防止灾难性遗忘
- **Stage 2 数据** (Embodied-Points-200K)：
  - REG 数据：RefCOCO + RoboRefIt + RoboPoint，验证标准改为点是否落在分割 mask 内
  - RRG 数据：从约 100 万开源具身数据集中经启发式过滤得到 33K 样本 + Isaac Gym 仿真数据（RGB-D 输入）
  - OFG 数据：基于 HandAL 数据集（212 个真实物体），40K 功能抓取点，GPT-4o 重写功能相关问题
  - VTG 数据：GPT-4o 识别关键物体 → 自监督关键点提取器 + Grounded-SAM → Cotracker3 跟踪 → 下采样至 8 个等距离散点投影回初始图像

### 训练策略（两阶段 RFT）
- **Stage 1**：增强空间推理能力，训练 2 个 epoch
- **Stage 2**：多任务混合训练具身指向能力，训练 1 个 epoch
- **算法**：GRPO（Group Relative Policy Optimization），每次生成 G 个候选响应，归一化奖励计算优势
- **多任务奖励设计**（每任务总奖励归一化到 [0,1]）：
  - 格式奖励 r_format：检查 <think/> 和 <answer></answer> 标签及 <point> 坐标格式
  - 准确度奖励 r_acc：多选题答案匹配
  - 点在 Mask 奖励 r_mask：预测点是否在 ground-truth mask 内
  - 点距离奖励 r_dis：欧氏距离密集辅助奖励
  - 视觉轨迹奖励 r_trace：RMSE 轨迹相似度
  - 环境奖励 r_env：Isaac Gym 仿真器反馈（二值）
  - 示例：R_RRG = 0.1×r_format + 0.2×r_dis + 0.7×r_mask

### 动作执行器
- **Affordance Points Branch (-P)**：预测抓取点和放置点 → CuRobo 运动规划器生成无碰撞路径
- **Visual Traces Branch (-V)**：VTG 生成的 2D 视觉轨迹 → Pinhole 模型映射到 3D 笛卡尔坐标 → 插值形成 SE(3) 完整轨迹


## Experiments

### 空间推理（Table 1, 15 个子任务, 5 个基准）
- Embodied-R1 平均排名 2.1（开源最佳），优于 FSD-13B（4.6）、RoboBrain-7B（4.4）
- 添加通用知识数据进一步提升（从 Rank 3.4 到 2.1）
- 超越仅用 SFT 训练的 Embodied-SFT（Rank 3.7）
- 在 EmbSpatial-Bench 上达到 67.4%（开源最佳）

### 指向能力（Table 2-4）
| 指标 | RoboRefIt | Where2Place | VABench-P | Part-Afford |
|------|-----------|-------------|-----------|-------------|
| GPT-4o | 15.28 | 29.06 | 9.30 | 10.15 |
| FSD | 56.73 | 45.81 | 61.82 | 9.55 |
| Embodied-SFT | 83.85 | 41.25 | 50.46 | 40.20 |
| **Embodied-R1** | **85.58** | **69.50** | **66.00** | **56.63** |

VTG 轨迹精度（VABench-V）：
- RMSE: 77.8（最佳，FSD 为 78.3）
- MAE: 45.0（最佳，FSD 为 63.4）
- LLM Score: 7.3（最佳）

3D 指向（Open6DOR-Position）：
- Embodied-R1-RGBD: 90.2%（Level0: 99.8%，Level1: 50.9%）
- Embodied-R1-RGB: 66.8%

### SIMPLEREnv 仿真（Table 5, WidowX 臂, 零样本）
| 方法 | 平均成功率 |
|------|-----------|
| OpenVLA | 1.0% |
| Octo-S | 30.0% |
| SoFar | 53.8% |
| **Embodied-R1** | **56.2%** |

- 超越所有端到端、模块化和 affordance VLA，包括需要微调的模型

### 真实世界评估（Table 6, xArm 6, 8 个桌面操控任务, 零样本）
| 方法 | 平均成功率 |
|------|-----------|
| RoboPoint | 12.5% |
| FSD | 25.0% |
| Embodied-R1-P | 83.3% |
| **Embodied-R1-T** | **87.5%** |

- 在空间推理任务（如"移动最近的物体"）上优势尤为明显
- 视觉轨迹版本 (-V/T) 略优于点位版本 (-P)

### 鲁棒性（Table 7）
- 原始场景：100% 抓取+成功
- 背景变化：100%
- 背景+光照变化：83%
- 背景+光照+高度变化：83%

### 消融实验
1. **RL vs SFT + Think vs No-Think**（Table 8）：
   - RL w/ Think: 65.50 / 65.39（最佳）
   - RL w/o Think: 63.00 / 60.50
   - SFT w/ Think: 41.25 / 47.67
   - SFT w/o Think: 36.85 / 50.46
   - RL 是 OOD 泛化的关键；CoT 在 SFT 下无显著帮助甚至有害

2. **混合训练 vs 单独训练**（Table 9）：
   - 混合训练在 Part-Afford (56.63 vs 51.25)、Where2Place (69.50 vs 65.50)、VABench-P (66.00 vs 65.39) 上均优于单独训练


## Limitations

1. **未与学习型策略集成**：当前仅与经典运动规划器(CuRobo)结合，尚未与可学习策略集成，限制了动态环境中的执行效率
2. **长时序任务**：当前框架仅处理单步指令，不具备长时序任务分解能力
3. **"Pointing" 表征的固有限制**：2D 坐标点表征对于需要精确力控、扭转、擦拭或与可变形物体复杂交互的任务不够丰富（明确指出 DLO 的局限性）
4. **3D 信息整合初步**：RGB-D 版本在复杂空间关系任务中表现略低于 2D 版本，depth map 可能产生幻觉


## Key Takeaways

### 对 DLO 操控的启示
- 论文 Appendix E 明确指出 pointing 表征对可变形物体操控不足，需要更丰富的表征
- VTG 的 object-centric 视觉轨迹思路可能可以适配 DLO 操控的轨迹规划，但需要从点序列扩展到曲线/形状描述
- 两阶段 RFT + 多任务奖励设计的方法论可迁移到 DLO 操控的 VLM 训练中

### 对 VLM-based 控制的启示
- **Pointing 作为中间表征**避免了直接预测低层具身特定动作，保留了 VLM 的视觉泛化能力——这是一个重要的设计原则
- **RFT 优于 SFT**：GRPO 强化微调比监督微调在 OOD 泛化上显著更强，特别是在多解问题（"multi-solution dilemma"）中
- **混合训练促进知识共享**：多任务混合训练比单独训练效果更好
- **3B 小模型的可行性**：通过精心设计的数据和训练策略，3B 模型可以超越 7B 甚至 13B 模型

### 方法论参考
- "问题-验证" 对（非 "问题-答案" 对）的数据格式设计值得借鉴
- 多任务奖励归一化到 [0,1] 的设计确保了混合训练的稳定性
- Isaac Gym 仿真器反馈作为环境奖励是一个有趣的 RL 信号来源

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

- [[yuan|Yuan, Yifu]]
- [[cui-haiqin|Cui, Haiqin]]
