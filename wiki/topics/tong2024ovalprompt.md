---
title: "OVAL-prompt: Open-vocabulary affordance localization for robot manipulation through LLM affordance-grounding"
tags: [manipulation, imitation, VLM]
created: "2026-04-27"
updated: "2026-04-27"
type: "literature"
status: "done"
summary: "提出 OVAL-Prompt，通过 VLM（VLPart）进行开放词汇物体部件分割 + LLM（GPT-4）进行 affordance-to-part 接地，实现零样本开放词汇 affordance 定位。无需微调，在 UMD 数据集上 F-score 0.711（vs 最佳监督方法 GSE 0.855）。Cut 任务 0.823 超越所有基线。真实机器人 6 物体抓取：分割准确时 grasp+pickup 成功率接近 100%。核心发现：LLM 理解 affordance，re-prompting 关键。"
authors: "Tong, Edmond; Opipari, Anthony; Lewis, Stanley; Zeng, Zhen; Jenkins, Odest Chadwicke"
year: "2024"
venue: "arXiv Preprint"
zotero_key: "XHHHKR77"
---
## 摘要

In order for robots to interact with objects effectively, they must understand the form and function of each object they encounter. Essentially, robots need to understand which actions each object affords, and where those affordances can be acted on. Robots are ultimately expected to operate in unstructured human environments, where the set of objects and affordances is not known to the robot before deployment (i.e. the open-vocabulary setting). In this work, we introduce OVAL-Prompt, a prompt-based approach for open-vocabulary affordance（可供性） localization in RGB-D images. By leveraging a Vision Language Model (VLM) for open-vocabulary object part segmentation and a Large Language Model（大语言模型） (LLM) to ground each part-segment-affordance（可供性）, OVAL-Prompt demonstrates generalizability to novel object instances, categories, and affordances without domain-specific finetuning. Quantitative experiments demonstrate that without any finetuning, OVAL-Prompt achieves localization accuracy that is competitive with supervised baseline models. Moreover, qualitative experiments show that OVAL-Prompt enables affordance（可供性）-based robot manipulation（机器人操控） of open-vocabulary object instances and categories. Project Page: https://ekjt.github.io/OVAL-Prompt/

## 中文简述

提出基于大语言模型的操控方法，具有泛化能力特点。

**研究方向**: 机器人操控、模仿学习、视觉-语言模型

## 关键贡献

1. **OVAL-Prompt 算法**：首个纯提示驱动的零样本开放词汇 affordance 定位管线。VLM 检测物体→LLM 将 affordance 接地到物体部件→VLM 分割部件→机器人抓取。无需微调。
2. **Re-prompting 机制**：VLM 分割失败时，LLM 提供替代部件名称（如"cup rim"替代"cup top"），显著提升分割成功率。
3. **与监督基线竞争力的零样本结果**：UMD 数据集 F-score 0.711，Cut 任务 0.823 超越所有监督方法。
4. **真实机器人验证**：Fetch 机器人 + Dex-Net 抓取引擎，6 物体 60 次试验验证。
## 结构化提取

- **Problem**: 开放词汇 affordance 定位——机器人需要在非结构化环境中操控未见物体，但传统方法依赖固定标签集的监督训练。预训练 LLM/VLM 能否零样本完成？
- **Method**: OVAL-Prompt：VLM（VLPart）物体检测 + LLM（GPT-4）affordance-to-part 接地 + VLM 部件分割 + Dex-Net 抓取。Re-prompting 机制处理分割失败。无需微调。
- **Tasks**: UMD 数据集（7 affordances × 17 物体类，105 物品），AGD20K（36 affordance 类别），真实机器人抓取（6 物体 × 10 trials）。
- **Sensors**: RGB-D 相机（Fetch 机器人内置）。深度图用于 Dex-Net 抓取规划。
- **Robot Setup**: Fetch and Freight Research Edition 机器人。Dex-Net 抓取引擎 + MoveIt 运动规划。Top-down pickup 策略。
- **Metrics**: UMD: Weighted F1-score（β=1）。AGD20K: KLD, SIM, NSS。Robot: 分割成功率、抓取成功率、pickup 成功率。
- **Limitations**: 分割精度不足（整个物体 vs 部件）；可扩展性差（逐物体 LLM 查询）；依赖预定义物体列表；仅 top-down 抓取；类别名称敏感；空间关系困难；无闭环反馈；仅 RGB-D。
- **Evidence Notes**: UMD 有 Tab. I（7 方法 × 7 affordances），消融有 Tab. III（3 变体 × 7 affordances），机器人有 Tab. II（6 物体 × 10 trials × 3 指标）。AGD20K 有 Tab. IV（补充材料，9 方法）。Cut 任务超越所有监督方法。Re-prompting 消融显示关键贡献（0.392→0.711）。整体证据强度：中-强（标准数据集 + 消融 + 真实机器人，但机器人实验规模小且仅 top-down）。
## 本地引用关系

- [[jeong2026your]]
- [[mitrano2024grasp]]
## 证据元数据

- **Zotero Key**: XHHHKR77
- **Citekey**: tong2024ovalprompt
- **Authors**: Tong Edmond, Opipari Anthony, Lewis Stanley, Zeng Zhen, Jenkins Odest Chadwicke
- **Affiliation**: University of Michigan, Ann Arbor + J.P. Morgan AI Research
- **Venue**: arXiv preprint, 2024-05
- **Paper Type**: Methods paper (open-vocabulary affordance localization via LLM+VLM prompting)
- **Fulltext Quality**: Complete, 8 pages with tables, figures, supplementary
- **Evidence Coverage**: High for UMD dataset (Tab. I, 7 affordances × 17 objects); High for ablation (Tab. III); Medium for real-robot (Tab. II, 6 objects × 10 trials); Medium for AGD20K (Tab. IV, supplementary)
- **Confidence**: High on UMD benchmark comparison (weighted F-score, established dataset); Medium on robot demo (small scale, 6 objects, top-down grasp only)
- **Summary**: 提出 OVAL-Prompt，通过 VLM（VLPart）进行开放词汇物体部件分割 + LLM（GPT-4）进行 affordance-to-part 接地，实现零样本开放词汇 affordance 定位。无需微调，在 UMD 数据集上 F-score 0.711（vs 最佳监督方法 GSE 0.855）。Cut 任务 0.823 超越所有基线。真实机器人 6 物体抓取：分割准确时 grasp+pickup 成功率接近 100%。核心发现：LLM 理解 affordance，re-prompting 关键。


## Problem

机器人需要在非结构化环境中操控开放词汇的物体，但传统 affordance 检测方法依赖固定标签集的监督训练，无法泛化到未见物体和 affordance。开放词汇 affordance 定位仍需领域微调。核心问题：预训练的 LLM 和 VLM 能否在无需领域微调的情况下完成开放词汇 affordance 定位？


## Method

### 管线（Fig. 1）
1. **VLM 物体检测**：输入 RGB 图像 + 候选物体列表 → VLPart 检测物体（置信度 >50%）
2. **LLM Affordance 接地**：
   - Object Prompt：给定任务和物体列表，LLM 选择合适物体
   - Part Prompt：LLM 指定物体的哪个部件支持该 affordance
   - 结构化输出：Objects: + Reason:（chain-of-thought）
3. **VLM 部件分割**：VLPart 对指定部件生成二值 mask
4. **Re-prompting**：分割失败时，LLM 提供替代部件名称
5. **抓取执行**：Dex-Net 基于 mask + 深度图生成抓取姿态 → MoveIt 执行

### 关键设计
- VLM：VLPart（swin-base cascade, lvis+paco+pascalpart+partimagenet）
- LLM：GPT-4 API，temperature=0
- 抓取：Dex-Net → top-down pickup（x,y,z + 朝下夹爪 + z 轴旋转）
- 无需训练/微调


## Experiments

### UMD 数据集（Tab. I, 7 affordances × 17 物体类）
| 方法 | Grasp | W-Grasp | Cut | Contain | Support | Scoop | Pound | Avg. |
|------|-------|---------|-----|---------|---------|-------|-------|------|
| HMP | 0.367 | 0.373 | 0.415 | 0.810 | 0.643 | 0.524 | 0.767 | 0.557 |
| GSE | 0.779 | 0.840 | 0.776 | 0.924 | 0.893 | 0.856 | 0.918 | **0.855** |
| OVAL-Prompt | 0.650 | 0.718 | **0.823** | 0.688 | 0.538 | 0.753 | 0.809 | 0.711 |

- OVAL-Prompt 零样本平均 F-score 0.711，比 HMP 高 0.154，比 GSE 低 0.144
- Cut 任务 0.823 超越所有方法（包括监督方法）
- Contain 和 Support 较低（VLM 难以分割容器内部和支撑面）

### 消融（Tab. III）
| 变体 | Avg. F-score |
|------|-------------|
| VLM only | 0.011 |
| No Re-prompting | 0.392 |
| Full Network | **0.711** |

- VLM 单独几乎无法做 affordance 定位（F-score 0.011）
- Re-prompting 贡献 0.319 的 F-score 提升（0.392→0.711）

### 真实机器人（Tab. II, Fetch 机器人, 6 物体 × 10 trials）
| 物体 | 分割成功 | 抓取成功 | 抓取成功 |
|------|---------|---------|---------|
| Brush | 10/10 | 10/10 | 10/10 |
| Clamp | 6/10 | 6/6 | 5/6 |
| Mug | 10/10 | 10/10 | 7/10 |
| Lightsaber | 5/10 | 5/5 | 5/5 |
| Spatula | 7/10 | 7/7 | 6/7 |
| Walkie Talkie | 4/10 | 4/4 | 4/4 |

- 分割准确时抓取成功率接近 100%
- 失败主因：VLM 分割整个物体而非部件

### AGD20K 数据集（Tab. IV, 补充材料）
- KLD 较高（因为输出是二值 mask 而非分布），SIM 和 NSS 竞争性强


## Limitations

1. **分割精度不足**：VLM 经常分割整个物体而非特定部件（如"handle"→ 整个工具）。Contain（0.688）和 Support（0.538）得分低。
2. **可扩展性差**：每个物体需要单独 LLM 查询，无法同时处理多个物体和 affordance。
3. **依赖预定义物体列表**：VLM 需要候选物体列表输入，无法完全自主发现。
4. **仅 top-down 抓取**：机器人实验简化为 top-down pickup，未验证其他抓取策略。
5. **类别名称敏感**：VLM 对不常见名称（如"turner"）识别差，需要常见名称（如"spatula"）。
6. **空间关系困难**：LLM 生成的部件描述涉及空间关系（如"cup top"）时，VLM 难以处理。
7. **无闭环反馈**：管线是开环的，抓取失败后无恢复机制。
8. **仅单模态输入**：只使用 RGB-D，未利用触觉或力反馈。


## Key Takeaways

1. **LLM 理解 affordance**：GPT-4 能将 affordance 正确映射到物体部件，re-prompting 贡献 0.319 F-score 提升。对 VLA 研究的启示：LLM 可作为 affordance 知识源指导抓取规划。
2. **VLM+LLM 零样本管线的实用性**：无需微调即可达到监督方法 83% 的性能（0.711/0.855）。在快速原型开发和新物体场景中有实用价值。
3. **与 [[jeong2026your]]（VLA Deviation Detection）互补**：Jeong et al. 关注 VLA 导航头的偏差检测，OVAL-Prompt 关注 affordance 定位。两者结合：affordance 定位提供抓取目标 → VLA 执行 → 偏差检测监控。
4. **与 [[mitrano2024grasp]]（GL-signature）互补**：GL-signature 用拓扑约束指导重抓取（运动规划层），OVAL-Prompt 用 LLM 接地 affordance 到部件（感知层）。
5. **对本研究方向的启示**：双臂 DLO 操控可引入 OVAL-Prompt 式的 affordance 定位——用 LLM 确定 DLO 的哪个部位/关键点应被哪只手臂抓取，结合分割 mask 指导抓取规划。

## 相关概念

- [[robotic-manipulation]]
- [[imitation-learning]]
- [[vision-language-model]]
- [[deformable-linear-object]]
- [[bimanual-manipulation]]
- [[grasping]]

## 相关研究者

- [[tong|Tong, Edmond]]
