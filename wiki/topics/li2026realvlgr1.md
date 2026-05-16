---
title: "RealVLG-R1: A large-scale real-world visual-language grounding benchmark for robotic perception and manipulation"
tags: [manipulation, imitation, VLM, RL, robot-learning]
created: "2026-05-03"
updated: "2026-05-03"
type: "literature"
status: "done"
summary: "构建 RealVLG-11B 大规模真实世界多粒度视觉-语言 grounding + 抓取数据集，并提出基于强化微调（GRPO/GSPO）的 RealVLG-R1 模型，实现从自然语言指令到检测框、分割掩码、抓取姿态和接触点的统一零样本预测。"
authors: "Li, Linfei; Zhang, Lin; Shen, Ying"
year: "2026"
venue: "arXiv Preprint"
zotero_key: "F5BMHB8K"
---
## 摘要

Visual-language grounding aims to establish semantic correspondences between natural language and visual entities, enabling models to accurately identify and localize target objects based on textual instructions. Existing VLG approaches focus on coarse-grained, object-level localization, while traditional robotic grasping（抓取） methods rely predominantly on geometric cues and lack language guidance, which limits their applicability in language-driven manipulation（操控） scenarios. To address these limitations, we propose the RealVLG framework, which integrates the RealVLG-11B dataset and the RealVLG-R1 model to unify real-world visual-language grounding and grasping（抓取） tasks. RealVLG-11B dataset provides multi-granularity annotations including bounding boxes, segmentation masks, grasp poses, contact points, and human-verified fine-grained language descriptions, covering approximately 165,000 images, over 800 object instances, 1.3 million segmentation, detection, and language annotations, and roughly 11 billion grasping（抓取） examples. Building on this dataset, RealVLG-R1 employs Reinforcement Fine-tuning on pretrained large-scale vision-language models to predict bounding boxes, segmentation masks, grasp poses, and contact points in a unified manner given natural language instructions. Experimental results demonstrate that RealVLG supports zero-shot（零样本） perception and manipulation（操控） in real-world unseen environments, establishing a unified semantic-visual multimodal（多模态） benchmark that provides a comprehensive data and evaluation platform for language-driven robotic perception and grasping（抓取） policy learning. All data and code are publicly available at https://github.com/lif314/RealVLG-R1.

## 中文简述

提出基于模仿学习的抓取方法，具有零样本泛化特点。

**研究方向**: 机器人操控、模仿学习、视觉-语言模型、强化学习、机器人学习

## 关键贡献

1. **RealVLG-11B 数据集**：迄今最大的真实世界多粒度 grounding + 抓取数据集，整合 Cornell、VMRD、OCID-Grasp、GraspNet、GraspClutter6D 五个数据集，包含约 165,000 张图像、800+ 物体实例、130 万分割/检测/语言标注、约 110 亿抓取样本。提供统一标注管线：GPT-4o 生成语言描述 → Qwen-VL-Max 验证对齐 → SAM2 生成分割掩码 → 人工复核。
2. **RealVLG-R1 模型**：首个基于 LVLM 的端到端机器人感知模型，统一分割、grounding 和抓取感知。采用 RLVR（Reinforcement Learning with Verifiable Rewards）范式，使用 GRPO/GSPO 策略优化 + 任务特定的可验证复合奖励函数，替代传统 SFT 的固定监督。
3. **RealVLG Benchmark**：统一的视觉-语言 grounding + 抓取评测基准，定义了 Seen/Similar/Novel 三级泛化评测分割，并提出 Validity Rate (VR) 指标量化 LVLM 输出稳定性。
## 结构化提取

- Problem: 现有 VLG 仅做物体级粗粒度定位，抓取方法缺乏语言语义引导，数据集缺乏真实世界的多粒度语言-视觉-抓取联合标注
- Method: 基于 LVLM（Qwen2.5-VL）的端到端模型，采用 RLVR（GRPO/GSPO）策略优化 + 可验证复合奖励函数，统一预测 bbox、分割掩码、抓取姿态和接触点
- Tasks: Visual-Language Grounding（检测、分割）+ Visual Grasping（抓取姿态预测、接触点预测）
- Sensors: RGB 相机（论文未明确提及深度，但部分源数据集包含 RGB-D）
- Robot Setup: 仅数据集评测，未进行真实机器人实验；抓取表示为矩形抓取姿态（4-DoF: x, y, θ, w）
- Metrics: gIoU、cIoU（检测），Sα、Fβ（分割），mIoU、gAcc（抓取），Validity Rate (VR)
- Limitations: 无真实机器人实验、仅 4-DoF 抓取、刚性物体为主、训练效率未报告
- Evidence Notes: 完整证据来自 arXiv HTML 全文。Table 3 数据质量对比、Table 4 benchmark 结果均有具体数值。消融实验通过 GRPO vs GSPO 对比呈现。缺少真实机器人物理实验数据。
## 本地引用关系

-
## 证据元数据

- Fulltext Quality: fulltext (arXiv HTML)
- Evidence Coverage: 完整覆盖摘要、方法、实验、结论；参考文献仅部分浏览
- Confidence: high
- Summary: 构建 RealVLG-11B 大规模真实世界多粒度视觉-语言 grounding + 抓取数据集，并提出基于强化微调（GRPO/GSPO）的 RealVLG-R1 模型，实现从自然语言指令到检测框、分割掩码、抓取姿态和接触点的统一零样本预测。


## Problem

现有视觉-语言 grounding（VLG）研究仅停留在粗粒度的物体级定位，未扩展到可操作的抓取理解（actionable grasp understanding）；传统抓取方法依赖几何线索，缺乏语言语义引导。同时，现有抓取数据集要么缺少语言标注，要么基于低分辨率合成场景（如 Grasp-Anything 系列使用扩散模型生成），缺乏真实世界的多样性和精细语义对齐。这导致语义理解与操控推理之间存在鸿沟，无法满足语言驱动的真实机器人操控需求。


## Method

### 数据集构建（RealVLG-11B）
- **数据来源**：整合 Cornell（单物体）、VMRD（多物体关系）、OCID-Grasp（渐进填充）、GraspNet 和 GraspClutter6D（杂乱场景）五个真实世界抓取数据集。
- **统一标注管线**：
  1. **语言标注**：提取每个物体的 3D 模型，渲染 8 个视角 → GPT-4o 生成 Meta Description → 逐图像生成 Language Instruction（包含类别、颜色、形状、属性、空间关系）
  2. **Grounding 标注**：Qwen-VL-Max 基于 Language Instruction 检测 bbox → SAM2 生成分割掩码验证对齐
  3. **抓取姿态标准化**：将不同格式的抓取标注统一为矩形抓取姿态（Rect Grasp Pose），并基于分割掩码计算接触点（接触点投影到掩码边界确保在物体表面）
  4. **人工验证**：人工交叉验证 Meta Description、Language Instruction、Bbox、Segmentation 四模态一致性
- **评测分割**：~800 物体分为 Seen（48 训练物体）、Similar（50 相似但未见物体）、Novel（37 全新物体），每子集约 15K 图像、150K 物体实例、300M 抓取标注

### 模型（RealVLG-R1）
- **Backbone**：Qwen2.5-VL 系列（3B/7B）
- **训练策略**：RLVR 范式，用 GRPO/GSPO 替代 SFT，使用可验证奖励驱动策略优化
  - GRPO：token 级重要性权重，适合小模型的精细动作精度
  - GSPO：序列级裁剪重要性权重（长度归一化），适合大模型的稳定优化
- **复合奖励函数** R(q,o) = R_Format + R_Task：
  - **Bbox**：二值 IoU 奖励（IoU ≥ τ_iou → 1）
  - **Segmentation**：IoU 奖励 + S-measure 掩码质量奖励
  - **Grasp**：Huber 损失之和的负值（角度用 sin/cos 表示处理周期性）
  - **Contact**：矩形对齐二值奖励 + 接触点 L2 距离惩罚
- **推理管线**：输入图像 + 任务 prompt → LVLM 生成 `<answer>` 结构化输出 → 分割任务额外经过 frozen SAM2 生成掩码
- **训练设置**：仅用 10% 训练集，10 epochs


## Experiments

### 数据质量评估（Table 3）
与 Grasp-Anything 和 Grasp-Anything++ 对比（各 10,000 随机样本）：
- **语言多样性（MTLD）**：RealVLG-11B 显著更高，因为包含丰富属性和空间关系描述
- **视觉-语言对齐（CLIP Score）**：RealVLG-11B 更优
- **空间一致性**：Seg-in-Bbox (Rs) = 0.99（近完美），Grasp-in-Seg (Rg) 比 Grasp-Anything 高约 0.3

### Benchmark 结果（Table 4）

**Visual Grounding 部分**：
| 模型 | gIoU | cIoU | Fβ | Sα | VR |
|------|------|------|-----|-----|-----|
| Qwen-VL-Max（闭源） | 92.3% | 93.2% | 87.8% | 44.8% | ~60-70% |
| Qwen2.5-VL（开源） | ~50% | - | ~75% | - | ~100% |
| Qwen2.5-VL+SFT | ~55%（+5%） | - | - | - | ~100% |
| **RealVLG-R1-3B** | >87% | - | - | - | 100% |
| **RealVLG-R1-7B** | 89% | - | - | - | 100% |
| RealVLG-R1-7B (Novel) | ~88% | - | - | - | 100% |

**Visual Grasping 部分**：
| 模型 | mIoU (Seen) | gAcc (Seen) | mIoU (Novel) | gAcc (Novel) |
|------|-------------|-------------|--------------|--------------|
| Qwen2.5-VL/SFT | <5% | <3% | - | - |
| **RealVLG-R1-3B (GRPO)** | 34.7% | 40.3% | - | - |
| RealVLG-R1-3B (GSPO) | 29.2% | - | - | 100% VR |
| RealVLG-R1-3B (Novel) | - | - | 26.9% | 20.2% |
| **RealVLG-R1-7B (GSPO)** | - | - | 55.3% | 37.2% |

**关键发现**：
- RL 相比 SFT 在 grounding 任务提升 30+ 个百分点 gIoU
- GRPO 在小模型上抓取精度更高，GSPO 在大模型上稳定性更好
- Novel 场景下仍有合理泛化（gIoU~88%, mIoU/gAcc=26.9%/20.2%）

### 局限性
- 论文未报告真实机器人物理实验结果，仅限于数据集评测
- 抓取表示限于矩形抓取姿态（4-DoF），未扩展到 6-DoF
- 语言描述依赖 GPT-4o 生成，可能存在偏差
- GSPO 在小模型上可能降低精细动作精度


## Limitations

1. **未进行真实机器人验证**：所有实验仅在数据集上评测，缺乏真实机械臂抓取实验
2. **仅支持 4-DoF 矩形抓取**：未覆盖 6-DoF 抓取姿态，限制了对复杂抓取场景的适用性
3. **数据集仍以刚性物体为主**：不涉及 DLO 或铰接物体
4. **训练效率**：虽然仅用 10% 数据，但 RL 训练的计算开销可能较大（论文未报告训练时间）
5. **语言标注管线依赖 GPT-4o**：成本高且可能引入模型偏差


## Key Takeaways

1. **RL 微调优于 SFT 用于多解任务**：抓取本身存在多种可行解，SFT 强制拟合单一标签导致"平均预测"，而 RLVR 用可验证奖励驱动能更好处理多解性。这对我们的 DLO 操控有启发——DLO 形态多样，抓取点更多，RL 微调可能比 SFT 更合适。
2. **多粒度标注管线设计精巧**：GPT-4o 生成 → VLM 验证 → 人工复核的三阶段管线可复用于构建 DLO 操控数据集。
3. **统一 grounding + 抓取的端到端思路**：从语言到动作的统一模型减少多阶段误差累积，这为语言驱动的 DLO 操控提供了架构参考。
4. **GRPO vs GSPO 的模型规模适配性**：小模型用 GRPO（token 级权重）抓取精度更高，大模型用 GSPO（序列级权重）更稳定——选择策略优化算法时需考虑模型规模。

## 相关概念

- [[robotic-manipulation]]
- [[imitation-learning]]
- [[vision-language-model]]
- [[reinforcement-learning]]
- [[robot-learning]]
- [[diffusion-model]]
- [[deformable-linear-object]]
- [[grasping]]

## 相关研究者

- [[li-linfei|Li, Linfei]]
- [[zhang-lin|Zhang, Lin]]
- [[shen-ying|Shen, Ying]]
