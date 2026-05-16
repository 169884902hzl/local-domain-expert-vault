---
title: "Learning human-intention priors from large-scale human demonstrations for robotic manipulation"
tags: [manipulation, imitation, VLM, robot-learning]
created: "2026-04-30"
updated: "2026-04-30"
type: "literature"
status: "done"
summary: "MoT-HRA 通过层级化 Mixture-of-Transformer 架构将人类视频中的操控意图分解为 3D 轨迹、MANO 手部运动先验和机器人动作三个耦合专家，在 SimplerEnv 上达到 66.1% 平均成功率，显著优于现有 VLA 方法。"
authors: "Xie, Yifan; Wang, YuAn; Chen, Guangyu; Liu, Jinkun; Sun, Yu et al."
year: "2026"
venue: "arXiv Preprint"
zotero_key: "NK6BZ47U"
---
## 摘要

Human videos contain rich manipulation（操控） priors, but using them for robot learning remains difficult because raw observations entangle scene understanding, human motion, and embodiment（具身）-specific action. We introduce MoT-HRA, a hierarchical vision-language-action framework that learns human-intention priors from large-scale human demonstrations. We first curate HA-2.2M, a 2.2M-episode action-language dataset reconstructed from heterogeneous human videos through hand-centric filtering, spatial reconstruction, temporal segmentation, and language alignment. On top of this dataset, MoT-HRA factorizes manipulation（操控） into three coupled experts: a vision-language expert predicts an embodiment（具身）-agnostic 3D trajectory, an intention expert models MANO-style hand motion as a latent human-motion prior, and a fine expert maps the intention-aware representation to robot action chunks. A shared-attention trunk and read-only key-value transfer allow downstream control to use human priors while limiting interference with upstream representations. Experiments on hand motion generation, simulated manipulation（操控）, and real-world robot tasks show that MoT-HRA improves motion plausibility and robust control under distribution shift.

## 中文简述

提出基于视觉-语言的操控方法，具有人类视频学习特点。

**研究方向**: 机器人操控、模仿学习、视觉-语言模型、机器人学习

## 关键贡献

1. **HA-2.2M 数据集**：构建了 2.2M 集的动作-语言数据集，来源于 HowTo100M (1.4M)、Ego4D (630K)、Epic-Kitchens (120K)、Something-Something-V2 (50K) 四个异构人类视频源，通过 hand-centric 过滤、空间重建、时间分割和语言对齐重建得到。
2. **MoT-HRA 架构**：提出层级化 Mixture-of-Transformer VLA 框架，将操控动作生成分解为视觉-语言专家（3D 轨迹预测）、意图专家（MANO 手部运动建模）和精细专家（机器人动作映射），通过共享注意力主干和只读 KV 转移实现知识隔离。
3. **实验验证**：在手部运动生成、SimplerEnv 仿真操控和真实世界机器人任务上验证了方法的有效性，SimplerEnv 平均成功率 66.1%（vs. 次优 43.8%）。
## 结构化提取

- **Problem**: 如何将大规模人类视频中的操控意图先验结构化地迁移到机器人策略，同时避免人类运动先验被机器人 loss 覆盖
- **Method**: MoT-HRA（层级化 Mixture-of-Transformer VLA），三个耦合专家 + 知识隔离 + 条件 Flow Matching
- **Tasks**: 手部运动生成、桌面操控（Spoon/Carrot/Stack/Eggplant）、长时序 Clean/Pouring 任务
- **Sensors**: 单目 RGB（224×224）
- **Robot Setup**: SimplerEnv WidowX（仿真）、平行夹爪 + 灵巧手（真实）
- **Metrics**: ADE、DTW、Rotation Error、Joint Rotation Error（手部运动）；Success Rate（操控任务）
- **Limitations**: 自动标注噪声；未测试动态交互/多物体长时序/差异大的具身；手指精度受限于域迁移；真实世界实验数值在补充材料
- **Evidence Notes**: 全文证据充分，Table 1-3 提供定量对比和消融。真实世界实验数值缺失（在补充材料），但主文定性结论可靠。与 Being-H0、VITRA、π₀ 等强 baseline 有公平对比。
## 本地引用关系

-
## 证据元数据

- Fulltext Quality: fulltext（arXiv HTML 完整获取）
- Evidence Coverage: 完整覆盖全部章节（方法细节、公式、实验表格、消融实验、局限性声明均有）
- Confidence: high
- Summary: MoT-HRA 通过层级化 Mixture-of-Transformer 架构将人类视频中的操控意图分解为 3D 轨迹、MANO 手部运动先验和机器人动作三个耦合专家，在 SimplerEnv 上达到 66.1% 平均成功率，显著优于现有 VLA 方法。


## Problem

人类视频中包含丰富的操控先验知识，但将其用于机器人学习面临核心困难：原始观察中纠缠了场景理解、人体运动和具身特定的动作。现有的 VLA 方法直接从像素到动作的映射会丢失可迁移的人类运动先验，且在视觉外观、视角、物体实例或具身变化时策略变得脆弱。关键问题是：如何将人类演示中的操控意图结构化地提取出来，作为机器人策略的先验，而非将人类视频简单视为噪声化的机器人动作替代品？


## Method

### 整体架构

MoT-HRA 基于 Mixture-of-Transformers 设计，包含一个跨任务共享注意力主干和三个任务特定专家。核心思想是将动作生成层次化分解：

$$p_\theta(a_{1:H}|o,w) \approx \int p_{\theta_a}(a_{1:H}|o,w,\tau_{1:H},h^{int}_{1:H}) \cdot q_{\theta_m}(h^{int}_{1:H}|o,w,\tau_{1:H}) \cdot p_{\theta_\tau}(\tau_{1:H}|o,w) \, d\tau \, dh$$

### HA-2.2M 数据管线

1. **粗过滤**：Gemini 标注手部中心动作片段 → V-JEPA 分类器全量筛选
2. **透视与背景重建**：VitPose 检测手部 → HaMeR 估计绝对尺度 MANO 手姿 → Depth Anything 3 预测单目深度 → 对齐到手的绝对尺度
3. **细过滤**：V-JEPA 时间分割模型（38K 手工标注训练）预测动作边界 → Gemini 合并连续意图片段并生成动作描述

### 三个耦合专家

- **视觉-语言专家**：基于 PaliGemma2 初始化，自回归预测离散化 3D 路径点 $\tau_h = (b_h^x, b_h^y, b_h^z)$，坐标量化为 B 个 bin。图像-文本 token 双向注意力，3D token 因果注意力。
- **意图专家**：基于条件 Flow Matching，从高斯噪声去噪生成 MANO 手部序列。每个手状态 $m_h = [w_h, j_h]$，其中 $w_h \in \mathbb{R}^7$（腕部平移+四元数），$j_h \in \mathbb{R}^{60}$（15 个手指关节四元数）。分离腕部和手指 loss。
- **精细专家**：同样基于条件 Flow Matching，将意图感知表示映射到机器人动作块。条件包含图像-文本特征、3D 轨迹状态和潜在意图状态 $h^{int}_{1:H}$。

### 知识隔离

通过 read-only KV transfer 实现：上游表示对下游可见，但下游 loss 不传播到上游缓存。VLA/轨迹专家不受 MANO 和 action loss 影响，机器人动作专家可利用意图线索但不覆盖意图表示。

### 联合训练

$\mathcal{L} = \lambda_{3d}\mathcal{L}_{3d} + \lambda_m \mathbb{1}_m \mathcal{L}_{mano} + \lambda_a \mathbb{1}_a \mathcal{L}_{act}$

人类演示集主要监督轨迹和意图专家，机器人数据集（AgiBot-World）主要监督轨迹和精细专家。在机器人样本上，意图专家通过只读接口提供潜在条件但不接收 MANO loss。


## Experiments

### 手部运动生成（Table 1）

在 Ego4D（held-out）和 OakInk 上评估，每数据集 200 clips × 5 seeds。

| Method | Ego4D ADE↓ | Ego4D DTW↓ | Ego4D Rot↓ | Ego4D J-Rot↓ | OakInk ADE↓ | OakInk DTW↓ | OakInk Rot↓ | OakInk J-Rot↓ |
|--------|-----------|-----------|-----------|-------------|-----------|-----------|-----------|-------------|
| Being-H0 | 0.185 | 0.174 | 38.27 | 44.03 | 0.245 | 0.233 | 44.91 | 49.18 |
| VITRA | 0.154 | 0.146 | 33.26 | 41.81 | 0.211 | 0.201 | 42.59 | 41.72 |
| MoT-HRA | **0.136** | **0.127** | **28.95** | **34.16** | **0.184** | **0.176** | **38.47** | **40.12** |

MoT-HRA 在所有指标上全面领先，但手指关节旋转改进较小，表明细粒度手指运动在域迁移下仍是最难点。

### SimplerEnv 仿真操控（Table 2）

| Method | Spoon | Carrot | Stack | Eggplant | Average |
|--------|-------|--------|-------|----------|---------|
| RoboVLMs | 45.8 | 20.8 | 4.2 | 79.2 | 37.5 |
| OpenVLA-OFT | 34.2 | 30.0 | 30.0 | 72.5 | 41.7 |
| π₀ | 29.1 | 0.0 | 16.6 | 62.5 | 27.1 |
| π₀-FAST | 29.1 | 21.9 | 10.8 | 66.6 | 32.1 |
| SpatialVLA | 16.7 | 25.0 | 29.2 | 100.0 | 42.7 |
| ThinkACT | 58.3 | 37.5 | 8.7 | 70.8 | 43.8 |
| MoT-HRA | **78.1** | **62.5** | **40.6** | 83.3 | **66.1** |

MoT-HRA 在 Spoon 和 Carrot 上优势最明显（需要精确空间定位和稳定放置），整体平均 66.1% 远超次优 ThinkACT（43.8%）。SpatialVLA 在 Eggplant 上最强（100%），但 MoT-HRA 更均衡。

### 真实世界实验

- 平行夹爪和灵巧手两种具身
- Clean 和 Pouring 长时序任务
- 150 条任务特定轨迹后训练
- OOD 变化：物体位置、类别、颜色
- 每方法 20 trials，优于 π₀ 和 GigaBrain-0
- 具体数值在补充材料中（主文未给）

### 消融实验（Table 3）

| 3D Trajectory | Intention Expert | Knowledge Insulation | ADE↓ | DTW↓ | Rot↓ | J-Rot↓ | SimplerEnv Avg↑ |
|:-:|:-:|:-:|------|------|------|--------|----------------|
| | | | 0.205 | 0.196 | 40.16 | 44.90 | 48.4 |
| ✓ | | | 0.182 | 0.173 | 36.64 | 42.53 | 52.1 |
| ✓ | ✓ | | 0.140 | 0.133 | 30.45 | 35.97 | 62.7 |
| ✓ | ✓ | ✓ | 0.136 | 0.127 | 28.95 | 34.16 | 66.1 |

每个组件单调贡献，从 π₀ 式直接 VLA（48.4%）到完整模型（66.1%），验证了层级分解的有效性。


## Limitations

1. **数据质量限制**：自动构建的人类演示集存在噪声、模糊的手-物接触和不完美的动作-语言对齐，可能削弱学到的意图先验
2. **评估覆盖有限**：未涵盖高度动态交互、多物体长时序规划或差异较大的具身形态
3. **手指运动精度**：细粒度手指关节旋转在强域迁移下改进较小，仍是最难点
4. **真实世界实验细节**：主文仅给定性描述，具体数值在补充材料中


## Key Takeaways

1. **层级化分解是核心设计**：将操控分解为"在哪里交互"(3D 轨迹) → "人类如何表达意图"(MANO 手部运动) → "机器人如何执行"(动作块)，这个分解思路对 DLO 操控有参考价值——DLO 的形变轨迹本质上也是"空间意图"的一种表达
2. **知识隔离策略值得关注**：read-only KV transfer 防止下游机器人 loss 覆盖上游人类运动先验，这种梯度隔离机制可用于多阶段学习
3. **人类视频作为先验而非替代**：论文明确主张"人类演示不是机器人动作的噪声替代，而是操控意图的结构化证据"，这一观点对我们理解如何利用人类视频学习 DLO 操控有指导意义
4. **大规模数据重建管线的参考价值**：HA-2.2M 的粗过滤→空间重建→细过滤管线可作为构建 DLO 相关人类视频数据集的参考

## 相关概念

- [[robotic-manipulation]]
- [[imitation-learning]]
- [[vision-language-model]]
- [[robot-learning]]
- [[deformable-linear-object]]
- [[grasping]]

## 相关研究者

- [[xie-yifan|Xie, Yifan]]
