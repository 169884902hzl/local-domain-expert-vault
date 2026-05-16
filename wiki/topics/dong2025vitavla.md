---
title: "VITA-VLA: Efficiently teaching vision-language models to act via action expert distillation"
tags: [manipulation, imitation, VLM]
created: "2026-04-27"
updated: "2026-04-27"
type: "literature"
status: "done"
summary: "提出 VITA-VLA，通过知识蒸馏将小型动作模型（Seer）的动作能力迁移到 7B VLM（VITA-1.5/Qwen-2.5-7B）。架构仅增加 action token + state encoder，保留 VLM 原始结构。两阶段训练：Stage 1 对齐隐藏表示（30M 参数，MSE loss）；Stage 2 端到端微调（MAE+BCE loss）。LIBERO 97.3%（+11.8%），LIBERO-LONG 93.5%（+24.5%），CALVIN ABC-D Task1 92.5%。真实世界 5 任务 82.0%（+17% vs Seer）。"
authors: "Dong, Shaoqi; Fu, Chaoyou; Gao, Haihan; Zhang, Yi-Fan; Yan, Chi et al."
year: "2025"
venue: "arXiv Preprint"
zotero_key: "MXCU6GJA"
---
## 摘要

Vision-Language Action (VLA) models significantly advance robotic manipulation（机器人操控） by leveraging the strong perception capabilities of pretrained vision-language models (VLMs). By integrating action modules into these pretrained models, VLA methods exhibit improved generalization. However, training them from scratch is costly. In this work, we propose a simple yet effective distillation-based framework that equips VLMs with action-execution capability by transferring knowledge from pretrained small action models. Our architecture retains the original VLM structure, adding only an action token and a state encoder to incorporate physical inputs. To distill action knowledge, we adopt a two-stage training strategy. First, we perform lightweight alignment by mapping VLM hidden states into the action space of the small action model, enabling effective reuse of its pretrained action decoder and avoiding expensive pretraining（预训练）. Second, we selectively fine-tune the language model, state encoder, and action modules, enabling the system to integrate multimodal（多模态） inputs with precise action generation. Specifically, the action token provides the VLM with a direct handle for predicting future actions, while the state encoder allows the model to incorporate robot dynamics not captured by vision alone. This design yields substantial efficiency gains over training large VLA models from scratch. Compared with previous state-of-the-art（现有最优方法） methods, our method achieves 97.3% average success rate on LIBERO (11.8% improvement) and 93.5% on LIBERO-LONG (24.5% improvement). In real-world experiments across five manipulation（操控） tasks, our method consistently outperforms the teacher model, achieving 82.0% success rate (17% improvement), which demonstrate that action distillation effectively enables VLMs to generate precise actions while substantially reducing training costs.

## 中文简述

提出基于视觉-语言的操控方法，具有泛化能力特点。

**研究方向**: 机器人操控、模仿学习、视觉-语言模型

## 关键贡献

1. **蒸馏式 VLA 架构**：保留 VLM（VITA-1.5-7B）原始结构，仅增加 action token（可学习查询）和 state encoder（线性层编码关节状态），使 VLM 主动参与动作建模而非仅作特征提取器。
2. **两阶段训练策略**：Stage 1 对齐——将 VLM 隐藏状态映射到小型动作模型（Seer）的动作空间（30M 参数，MSE loss）；Stage 2 微调——端到端优化 LLM + state encoder + action module（MAE+BCE loss）。
3. **复用预训练动作解码器**：直接复用 Seer 的两层 MLP 动作解码器，避免从头预训练。Action mapper（3 层 MLP）将 VLM 隐藏状态投影到解码器输入空间。
4. **全面验证**：LIBERO 97.3%（SOTA），LIBERO-LONG 93.5%（+24.5%），CALVIN ABC-D 92.5%，真实世界 5 任务 82.0%。
## 结构化提取

- **Problem**: VLA 模型训练成本高。离散化方法忽略状态信息，扩散方法仅用 VLM 作特征提取器。需要高效地将小型动作模型能力迁移到 VLM。
- **Method**: VITA-VLA：保留 VLM 结构 + action token（可学习查询）+ state encoder（线性层）。两阶段训练：Stage 1 MSE 对齐 VLM 和 Seer 隐藏表示（30M 参数）；Stage 2 MAE+BCE 端到端微调。复用 Seer 动作解码器。
- **Tasks**: CALVIN ABC-D（34 任务，零样本泛化到环境 D）、LIBERO（4 suite, 40 任务）、真实世界 5 任务（Close Drawer, Stack Cups, Stack Blocks, Pick Place Sponge, Pick Place Block）。
- **Sensors**: 仿真：2 视角 RGB（static + wrist），200×200。真实：ALOHA 平台 RGB 相机。State：6-DoF 臂状态 + 1D 夹爪宽度。
- **Robot Setup**: 仿真：Franka Panda（CALVIN, LIBERO）。真实：ALOHA 双臂机器人（但仅用单臂数据）。动作空间：7-DoF（6 关节 + 1 夹爪）。
- **Metrics**: Success Rate（CALVIN 1000 rollouts, LIBERO 500 rollouts, LIBERO-LONG 20 rollouts/task, 真实 40 rollouts/task），Average Length（CALVIN 连续任务数）。
- **Limitations**: 依赖预训练动作专家；推理速度慢；长视界 Avg. Len. 不如 Seer；仅单臂数据；教师模型能力限制上限；图像分辨率低；未与同级别 VLA 对比；状态编码简单。
- **Evidence Notes**: 定量结果有 CALVIN（Tab. 1, 1000 rollouts）、LIBERO（Tab. 2, 500 episodes）、LIBERO-LONG（Tab. 3, 20 rollouts × 10 tasks）、真实世界（Tab. 4, 40 rollouts × 5 tasks × 3 methods）。消融有 three training settings（two-stage vs only-ft vs freeze-vlm）。图像分辨率消融（200 vs 224）。整体证据强度：强（多基准 + 真实世界 + 消融，评估协议标准）。
## 本地引用关系

- [[chen2025benchmarking]]
- [[ma2025running]]
- [[wang2025vlaadapter]]
## 证据元数据

- **Zotero Key**: MXCU6GJA
- **Citekey**: dong2025vitavla
- **Authors**: Dong Shaoqi, Fu Chaoyou, Gao Haihan, Zhang Yi-Fan, Yan Chi, Wu Chu, Liu Xiaoyu, Shen Yunhang, Huo Jing, Jiang Deqiang, Cao Haoyu, Gao Yang, Sun Xing, He Ran, Shan Caifeng
- **Affiliation**: Nanjing University + Tencent Youtu Lab + CASIA
- **Venue**: arXiv preprint, 2025-10
- **Paper Type**: Methods paper (VLA via knowledge distillation from small action model)
- **Fulltext Quality**: Complete, ~8044 words with tables, figures, appendix
- **Evidence Coverage**: High for LIBERO/CALVIN benchmarks (Tab. 1-4); High for ablation (two-stage vs only-ft vs freeze-vlm); High for real-world (5 tasks, 40 trials each)
- **Confidence**: High on benchmark comparisons (standard evaluation protocols); High on real-world (40 rollouts × 3 methods × 5 tasks = 600 trials)
- **Summary**: 提出 VITA-VLA，通过知识蒸馏将小型动作模型（Seer）的动作能力迁移到 7B VLM（VITA-1.5/Qwen-2.5-7B）。架构仅增加 action token + state encoder，保留 VLM 原始结构。两阶段训练：Stage 1 对齐隐藏表示（30M 参数，MSE loss）；Stage 2 端到端微调（MAE+BCE loss）。LIBERO 97.3%（+11.8%），LIBERO-LONG 93.5%（+24.5%），CALVIN ABC-D Task1 92.5%。真实世界 5 任务 82.0%（+17% vs Seer）。


## Problem

VLA 模型训练成本高昂。离散化方法（OpenVLA, RT-2）忽略机器人状态信息，动作预测不精确；扩散方法（π0, GR00T）将 VLM 仅用作特征提取器，未充分利用其端到端建模能力。从小型动作模型从头训练 VLA 需要大规模数据集和巨大计算资源。核心问题：如何高效地将小型动作模型的动作能力迁移到大型 VLM？


## Method

### 架构（Fig. 2）
- **骨干**：VITA-1.5-7B（InternViT-300M + 3-layer MLP connector + Qwen-2.5-7B）
- **State Encoder**：6-DoF 臂状态 + 2D 夹爪状态（one-hot）→ 线性层 → 与文本 token 同维度
- **Action Token**：可学习查询 token，重复 3 次（预测 3 步未来动作）。同一 token 共享，利用连续动作的时间相关性。
- **输入序列**：[img1]...[img98] [text1]...[textm] [state] [act1][act2][act3]（13 时间步）
- **Action Mapper**：3 层 MLP，将 VLM 最后一层隐藏状态投影到动作空间
- **Action Decoder**：复用 Seer 的 2 层 MLP，输出 7-DoF 动作（6 关节 + 1 夹爪）

### Stage 1: 对齐（Fig. 3 左）
- VLM 和 Seer 接收相同输入（图像 + 文本 + 状态）
- 提取两者 action token 最后一层隐藏状态
- MSE loss 对齐：L_align = (1/N)Σ∥M(a_h^VLA) - a_h^Small∥²
- 仅训练 state encoder + action tokens + action mapper（~30M 参数）
- VLM 参数冻结

### Stage 2: 端到端微调（Fig. 3 右）
- 复用 Stage 1 的 action mapper 和 Seer 的 action decoder
- L_total = L_arm(MAE) + 0.01 × L_gripper(BCE)
- 微调 LLM + state encoder + action tokens + action mapper + action decoder
- DeepSpeed ZeRO-2 训练


## Experiments

### CALVIN ABC-D（Tab. 1）
| 方法 | Task 1 | Avg. Len. |
|------|--------|-----------|
| Seer-Large | 88.4 | 3.76 |
| OpenVLA | 62.8 | 0.90 |
| VITA-VLA (two-stage) | **92.5** | 3.18 |
| VITA-VLA (only-ft) | 86.0 | 3.08 |
| VITA-VLA (freeze-vlm) | 45.3 | - |

- Task 1 超过 Seer 4.1%，但 Avg. Len. 低于 Seer（3.18 vs 3.76），长视界任务过渡不够鲁棒

### LIBERO（Tab. 2）
| 方法 | SPATIAL | OBJECT | GOAL | LONG | Average |
|------|---------|--------|------|------|---------|
| π0-FAST | 96.4 | 96.8 | 88.6 | 60.2 | 85.5 |
| VITA-VLA | **98.0** | **99.8** | **97.9** | **93.5** | **97.3** |

- LONG 任务提升 24.5%（vs CoT-VLA 69.0%），展现强长视界规划能力

### LIBERO-LONG 逐任务（Tab. 3）
- VITA-VLA (two-stage) 93.5% vs Seer 87.7% vs OpenVLA 54.0%
- Task 1-4 全部 100%，Task 10 为 90%

### 真实世界（Tab. 4, ALOHA 平台, 40 trials/任务）
| 方法 | Close Drawer | Stack Cups | Stack Blocks | Pick Place Sponge | Pick Place Block | Avg. |
|------|-------------|-----------|-------------|-------------------|-----------------|------|
| Seer | 87.5 | 32.5 | 60.0 | 75.0 | 70.0 | 65.0 |
| VITA-VLA (two-stage) | **97.5** | **52.5** | **80.0** | **87.5** | **92.5** | **82.0** |

- 真实世界全面超越教师模型 Seer（+17%）
- 复杂任务（Stack, Pick&Place）优势明显

### 消融
- **Two-stage vs Only-ft**：Stage 1 对齐带来 6.5% CALVIN Task1 和 1% LIBERO-LONG 提升
- **Freeze-VLM**：仅 45.3% CALVIN Task1，说明必须微调 VLM
- **图像分辨率**：200×200 优于 224×224（VLM 难以理解低分辨率放大的图像）


## Limitations

1. **依赖预训练动作专家**：需要已有的小型动作模型（Seer），在缺乏适当动作专家的领域受限。
2. **推理速度慢**：7B VLM 推理速度远慢于小型模型，未报告具体推理频率。
3. **长视界 Avg. Len. 不如 Seer**：CALVIN ABC-D Avg. Len. 3.18 vs Seer 3.76，任务过渡时 VLM 可能误判上下文。
4. **仅单臂数据**：CALVIN 和 LIBERO 均为单臂操控，未涉及双臂或 DLO 操控。
5. **Seer 教师选择限制**：知识蒸馏的上限受教师模型能力约束。
6. **图像分辨率低**：200×200 分辨率限制了视觉感知精度。
7. **未与同级别 VLA 对比**：未与 π0、GR00T 等扩散式 VLA 在相同基准上全面对比。
8. **状态编码简单**：仅用线性层编码机器人状态，可能限制复杂动力学建模。


## Key Takeaways

1. **知识蒸馏是 VLA 高效训练的有效路径**：通过两阶段蒸馏（对齐 + 微调），将小型动作模型能力迁移到 7B VLM，避免从头预训练。对 VLA 研究的启示：可先训练小型专家模型，再蒸馏到大 VLM。
2. **VLM 应主动参与动作建模**：action token 作为可学习查询，使 VLM 在自回归框架内融合视觉-语言-状态信息预测动作，优于仅将 VLM 当作特征提取器的扩散式方法。
3. **与 [[wang2025vlaadapter]]（VLA-Adapter）对比**：两者都关注高效 VLA 训练。VLA-Adapter 用 Bridge Attention 融合 VL→A，0.5B 模型达到 97.3%；VITA-VLA 用知识蒸馏，7B 模型达 97.3%。VLA-Adapter 更轻量，VITA-VLA 架构更通用。
4. **与 [[chen2025benchmarking]]（RoboTwin Challenge）相关**：挑战赛揭示了 3D 表示的重要性。VITA-VLA 保留了 VLM 的视觉理解能力，但未引入显式 3D 表示，可考虑与 AnchorDP3/SEM 的 3D 模态结合。
5. **对本研究方向的启示**：双臂 DLO 操控的 VLA 可采用蒸馏范式——先训练小型 DLO 操控专家，再蒸馏到 VLM 获得泛化能力。Action token + state encoder 设计可复用。

## 相关概念

- [[robotic-manipulation]]
- [[imitation-learning]]
- [[vision-language-model]]
- [[deformable-linear-object]]
- [[bimanual-manipulation]]
- [[grasping]]

## 相关研究者

- [[dong|Dong, Shaoqi]]
