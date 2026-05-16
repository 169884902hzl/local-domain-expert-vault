---
title: "Preference aligned visuomotor diffusion policies for deformable object manipulation"
tags: [manipulation, imitation, diffusion, robot-learning, DLO]
created: "2026-04-27"
updated: "2026-04-27"
type: "literature"
status: "done"
summary: "提出 RKO（Relative-KTO），结合 KTO 的二值标签偏好学习和 RPO 的语义相似度重加权，对预训练扩散策略进行偏好对齐。在 3 种衣物折叠任务（trousers/sleeves/t-shirt）× 3 种偏好上对比 DPO/RPO/KTO/RKO/DDPM。RKO 在 9 个任务中 4 个最优，偏好对齐方法全面优于 DDPM 基线。样本效率：RKO 在 20→95 演示下持续优于 DDPM，训练 40-50k 步即达强性能（vs DDPM 100k）。"
authors: "Moletta, Marco; Welle, Michael C.; Kragic, Danica"
year: "2026"
venue: "arXiv Preprint"
zotero_key: "ZCX8CBE9"
---
## 摘要

Humans naturally develop preferences for how manipulation（操控） tasks should be performed, which are often subtle, personal, and difficult to articulate. Although it is important for robots to account for these preferences to increase personalization and user satisfaction, they remain largely underexplored in robotic manipulation（机器人操控）, particularly in the context of deformable objects like garments and fabrics. In this work, we study how to adapt pretrained visuomotor diffusion（扩散） policies to reflect preferred behaviors using limited demonstrations. We introduce RKO, a novel preference-alignment method that combines the benefits of two recent frameworks: RPO and KTO. We evaluate RKO against common preference learning frameworks, including these two, as well as a baseline vanilla diffusion policy（扩散策略）, on real-world cloth-folding tasks spanning multiple garments and preference settings. We show that preference-aligned policies (particularly RKO) achieve superior performance and sample efficiency compared to standard diffusion policy（扩散策略） fine-tuning. These results highlight the importance and feasibility of structured preference learning for scaling personalized robot behavior in complex deformable object（可变形物体） manipulation（操控） tasks.

## 中文简述

提出基于扩散策略的操控方法。

**研究方向**: 机器人操控、模仿学习、扩散模型、机器人学习、可变形物体操控

## 关键贡献

1. **RKO（Relative-KTO）偏好对齐方法**：首次将 KTO 的二值标签（无需配对比较）与 RPO 的语义相似度重加权结合。对语义模糊区域（偏好与不偏好在嵌入空间接近）分配更大梯度权重，提高对齐效率。
2. **首个 DOM 偏好对齐系统对比**：首次系统对比 DPO/RPO/KTO/RKO 在可变形物体操控中的表现，在 3 种衣物 × 3 种偏好上进行真实世界评估。
3. **循环偏好数据集设计**：3 个偏好集循环充当 winner/loser/reference，确保公平对比。每偏好 60 条 winner + 60 条 loser 演示。
4. **样本效率验证**：20-95 演示下 RKO 持续优于 DDPM，40-50k 训练步即收敛（vs DDPM 100k）。
## 结构化提取

- **Problem**: 可变形物体操控中的用户偏好对齐。现有扩散策略无法适应用户特定的执行偏好。偏好隐含且难以表达。需要样本高效的对齐框架。
- **Method**: RKO（Relative-KTO）：结合 KTO 二值标签 + RPO 语义相似度重加权。预训练参考策略（100 演示）+ 偏好数据集（60 winner + 60 loser）进行对齐。DDPM 扩散策略 + U-Net 去噪骨干。对比 DPO/RPO/KTO/DDPM。
- **Tasks**: 3 种衣物折叠（trousers 单臂, sleeves 双臂, t-shirt 双臂）× 3 种偏好。步进评分评估 pick-and-place 正确性。
- **Sensors**: 3 个 Intel RealSense D435（2 腕装 + 1 俯视），RGB 图像输入。Trousers 用 2 相机，sleeves/t-shirt 用 3 相机。
- **Robot Setup**: 双臂 UFactory Lite6 机器人。遥操作采集演示（Quest2ROS Oculus app）。Teleoperation + human takeover。
- **Metrics**: 步进评分（归一化到 1，pick 成功 > place 成功），10 runs/任务/方法。Bayesian A/B 测试（成功阈 0.75）。总计 1170 次执行。
- **Limitations**: 标准差大（10 runs 偏少）；仅衣物折叠；偏好人为定义；循环数据集可能偏差；无仿真；评估不包含折叠质量；双臂失败率高；DPO 不一致。
- **Evidence Notes**: 性能对比有 3 个表格（Tab. I-III），9 任务 × 5 方法 × 10 runs。样本效率有 Fig. 5（20-95 演示递增）。消融有 RKO_noRW 对比。统计验证有 Bayesian A/B 测试（RKO>DDPM 70-87%）。标准差普遍较大（0.15-0.43），说明变异性高。整体证据强度：中-强（真实世界实验 + 系统对比 + 统计验证，但 runs 偏少且标准差大）。
## 本地引用关系

- [[blancomulero2024benchmarking]]
- [[kuroki2025gendom]]
## 证据元数据

- **Zotero Key**: ZCX8CBE9
- **Citekey**: moletta2026preference
- **Authors**: Moletta Marco, Welle Michael C., Kragic Danica
- **Affiliation**: KTH Royal Institute of Technology, Sweden + INCAR Robotics AB
- **Venue**: arXiv preprint, 2026-02
- **Paper Type**: Methods paper (preference alignment for diffusion policies in deformable object manipulation)
- **Fulltext Quality**: Complete, 8 pages with tables, figures, and sample efficiency experiments
- **Evidence Coverage**: High for preference alignment comparison (Tab. I-III); High for sample efficiency (Fig. 5, 20-95 demos); Medium for ablation (single condition, RKO_noRW)
- **Confidence**: High on performance comparison (10 runs × 9 tasks × 5 methods = 450 executions, plus 720 for sample efficiency); Medium on statistical significance (large standard deviations, Bayesian A/B test supports RKO>DDPM at 70-87%)
- **Summary**: 提出 RKO（Relative-KTO），结合 KTO 的二值标签偏好学习和 RPO 的语义相似度重加权，对预训练扩散策略进行偏好对齐。在 3 种衣物折叠任务（trousers/sleeves/t-shirt）× 3 种偏好上对比 DPO/RPO/KTO/RKO/DDPM。RKO 在 9 个任务中 4 个最优，偏好对齐方法全面优于 DDPM 基线。样本效率：RKO 在 20→95 演示下持续优于 DDPM，训练 40-50k 步即达强性能（vs DDPM 100k）。


## Problem

可变形物体操控（DOM）中的用户偏好对齐问题。不同用户对衣物折叠有不同的执行偏好（如折叠方式、路径选择），但这些偏好通常是隐性的、微妙的、难以用语言表达的。现有扩散策略从大量演示中学习通用行为，但无法适应用户特定的偏好。直接收集偏好演示成本高，需要样本高效的对齐框架。核心挑战：如何用有限的偏好演示高效对齐预训练扩散策略？


## Method

### 偏好对齐框架
- 预训练参考策略 π_ref：100 演示（70 标准 + 30 takeover）
- 偏好数据集 D_pref：60 winner + 60 loser 演示/偏好
- Takeover：50% 的 winner 演示来自 human takeover（处理 OOD 状态）
- 循环分配：pref1→winner=pref1, loser=pref2, ref=pref3

### RKO（Diffusion-RKO）
- 二值标签 q ∈ {+1, -1}（无需配对）
- 每样本奖励优势：A_b = β · (∥ε-ε_θ∥² - ∥ε-ε_ref∥²) - Q_ref
- 效用：U_b = σ(q_b · A_b)
- 语义重加权：s_pos_i = 1 + max_j ω_{i,j}（赢家关注最近输家）; s_neg_j = Σ_i ω_{i,j}（输家关注所有赢家密度）
- ω_{i,j} 基于余弦相似度的 softmax（编码器嵌入，温度 τ=0.15）
- 损失：L_RKO = -1/Σs_b · Σ s_b · σ(q_b · A_b)

### 其他方法
- **DPO**：配对比较，β=10
- **RPO**：配对 + 相似度重加权，β=20, τ=0.15
- **KTO**：二值标签无重加权，β=12
- **DDPM**：仅在 winner 演示上训练

### 实验设置
- 2 个 UFactory Lite6 机器人 + 3 个 RealSense D435（2 腕装 + 1 俯视）
- 3 种衣物：trousers（单臂，2 相机）、sleeves（双臂，3 相机）、t-shirt（双臂，3 相机）
- 评估：步进评分（pick-and-place 正确性），归一化到 1
- 10 runs/任务/方法，总计 1170 次执行
- 训练 100k 步，偏好模型选 best reward difference checkpoint


## Experiments

### 性能对比（Tab. I-III）
**Trousers（单臂）**:
| 模型 | Pref 1 | Pref 2 | Pref 3 |
|------|--------|--------|--------|
| DDPM | 0.701 | 0.667 | 0.453 |
| RKO  | **0.910** | 0.760 | **0.620** |

**Sleeves（双臂）**:
| 模型 | Pref 1 | Pref 2 | Pref 3 |
|------|--------|--------|--------|
| DDPM | 0.510 | 0.563 | 0.626 |
| RKO  | 0.715 | **0.695** | 0.695 |

**T-shirt（双臂）**:
| 模型 | Pref 1 | Pref 2 | Pref 3 |
|------|--------|--------|--------|
| DDPM | 0.496 | 0.453 | 0.593 |
| RKO  | **0.605** | 0.550 | **0.660** |

- RKO 在 9 个任务中 4 个最优，KTO 3 个，RPO 2 个
- 偏好方法全面优于 DDPM 基线（除 DPO 个别例外）

### 样本效率（Fig. 5）
- RKO 在 Trousers-Pref1 和 Sleeves-Pref1 从 20 到 95 演示持续优于 DDPM
- 20 演示时 RKO 可能受限于 winner+loser 数据不足，导致 OOD 状态
- 随数据量增加 RKO 优势更显著
- RKO_noRW（无重加权）性能低于完整 RKO，验证重加权贡献

### 统计验证
- Bayesian A/B 测试：RKO 优于 DDPM 的概率 87%（Trousers）和 70.1%（Sleeves）


## Limitations

1. **标准差大**：多数任务标准差 0.15-0.43，变异性高，统计显著性有限。10 runs/任务偏少。
2. **仅衣物折叠**：未涉及其他可变形物体（绳索、布料展开、食品）。任务类型单一。
3. **偏好定义人为**：3 种偏好通过 pick-and-place 位置定义，非真实用户偏好采集。
4. **循环数据集可能引入偏差**：loser 和 reference 来自不同偏好集，可能不代表"真实的不偏好行为"。
5. **无仿真对比**：全部真实世界实验，无法做大规模消融或可重复性验证。
6. **评估度量的局限**：步进评分仅评估 pick-and-place 正确性，不评估折叠质量（如褶皱、对齐精度）。
7. **双臂任务失败率高**：双臂任务（sleeves, t-shirt）由于协调复杂度，失败率明显高于单臂（trousers）。
8. **DPO 表现不一致**：DPO 在部分任务甚至低于 DDPM，说明配对比较可能不适合 DOM 偏好对齐。


## Key Takeaways

1. **偏好对齐优于从头训练**：在有限演示场景下，用 winner/loser 对比对齐预训练策略比直接在 winner 上训练 DDPM 更高效。对 DLO 操控的启示：可对双臂穿缆策略用"成功/失败"标签进行 KTO/RKO 对齐。
2. **二值标签 + 语义重加权是有效组合**：KTO 的二值标签降低了数据采集成本（无需配对），RPO 的语义重加权聚焦困难样本。RKO 结合两者优势。
3. **与 [[blancomulero2024benchmarking]]（Cloth Benchmark）相关**：两者都关注布料操控评估。Garcia-Camacho et al. 提供评估基准，Moletta et al. 提供偏好对齐的评估方案（步进评分）。
4. **与 [[kuroki2025gendom]]（GenDOM）互补**：GenDOM 通过物理参数估计实现 one-shot 泛化，RKO 通过偏好对齐实现行为个性化。两者结合：先用 GenDOM 估计物体参数实现基础操控，再用 RKO 对齐用户偏好。
5. **对本研究方向的启示**：双臂 DLO 操控可引入偏好对齐——不同用户对穿缆路径/张紧力度有不同偏好。用 winner/loser 演示进行 RKO 对齐，可在保持基础操控能力的同时适应用户偏好。

## 相关概念

- [[robotic-manipulation]]
- [[imitation-learning]]
- [[diffusion-model]]
- [[robot-learning]]
- [[deformable-linear-object]]
- [[bimanual-manipulation]]

## 相关研究者

- [[moletta|Moletta, Marco]]
