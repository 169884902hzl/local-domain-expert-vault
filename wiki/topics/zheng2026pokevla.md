---
title: "PokeVLA: Empowering pocket-sized vision-language-action model with comprehensive world knowledge guidance"
tags: [manipulation, imitation, VLM, robot-learning]
created: "2026-04-29"
updated: "2026-04-29"
type: "literature"
status: "done"
summary: "PokeVLA 提出轻量级（1.22B 参数）VLA 模型，通过两阶段训练——大规模 embodied VLM 预训练（2.4M 样本）和目标感知分割+几何对齐+动作查询注入的后训练——在 LIBERO-Plus 和真实场景达到 SOTA 成功率和鲁棒性。"
authors: "Zheng, Yupeng; Li, Xiang; Gu, Songen; Zheng, Yuhang; Tian, Shuai et al."
year: "2026"
venue: "arXiv Preprint"
zotero_key: "RICZMJ5V"
---
## 摘要

Recent advances in Vision-Language-Action (VLA) models have opened new avenues for robot manipulation（机器人操控）, yet existing methods exhibit limited efficiency and a lack of high-level knowledge and spatial awareness. To address these challenges, we propose PokeVLA, a lightweight yet powerful foundation model for embodied manipulation（操控） that effectively infuses vision-language understanding into action learning. Our framework introduces a two-stage training paradigm: first, we pre-train a compact vision-language model（视觉-语言模型） (PokeVLM) on a curated multimodal（多模态） dataset of 2.4M samples encompassing spatial grounding, affordance（可供性）, and embodied reasoning tasks; second, we inject manipulation（操控）-relevant representations into the action space through multi-view goal-aware semantics learning, geometry alignment, and a novel action expert. Extensive experiments demonstrate state-of-the-art（现有最优方法） performance on the LIBERO-Plus benchmark and in real-world deployment, outperforming comparable baselines in success rate and robustness under diverse perturbations. To foster reproducibility and community progress, we will open-source our code, model weights, and the scripts for the curated pre-training dataset. Project page: https://getterupper.github.io/PokeVLA

## 中文简述

提出基于视觉-语言的操控方法。

**研究方向**: 机器人操控、模仿学习、视觉-语言模型、机器人学习

## 关键贡献

1. 构建了约 2.4M 条目的大规模 embodied 多模态预训练数据集，覆盖通用 VQA、空间定位、affordance 学习和 embodied reasoning 四类任务，用于预训练 tiny-scale embodied VLM（PokeVLM）
2. 提出学习操控相关表征的新方法：多视角一致的操控目标语义分割 + 几何对齐，配合新型 action head 通过 action queries 高效注入这些表征到动作学习过程
3. 在仿真基准和真实世界场景中进行了广泛验证，证明了方法的鲁棒性和有效性
## 结构化提取

- Problem: 现有 VLA 模型缺乏 embodied 领域知识、多视角空间一致性和高级目标引导，导致操控效率和泛化性不足
- Method: 两阶段训练——Stage 1 在 2.4M embodied 多模态数据上预训练 tiny VLM（PokeVLM），Stage 2 通过 goal-aware segmentation（LISA-style `<SEG>` token + coarse-to-fine decoding）、geometry alignment（VGGT distillation）和 novel action head（multi-source cross-attention）注入操控相关表征
- Tasks: 桌面操控（pick-and-place、spatial referring、color referring、object manipulation），LIBERO/LIBERO-Plus benchmark（Spatial/Object/Goal/Long suites）
- Sensors: 双目 RGB 相机（base view + wrist view），Realsense D435；本体感知（关节状态）
- Robot Setup: 仿真：LIBERO 环境；真实：UFACTORY xArm7 + parallel gripper，GELLO 遥操作采集
- Metrics: 成功率（%），VLM 准确率（0-1），L1 loss（训练）
- Limitations: robot initialization 扰动鲁棒性不足（52.9%）；language perturbation 偏弱（71.4%）；tiny VLM 推理容量受限；仅验证桌面场景
- Evidence Notes:

  - LIBERO 98.2% total（Table IV），LIBERO-Plus fine-tuned 83.5%（Table V），transfer 79.3%（Table V blue rows）
  - 真实世界 81.25% vs VLA-Adapter 68.75%（Table IX），扰动 63.0% vs 43.0%（Table X）
  - 消融：三组件联合 78.2% → 85.3%（Table VI），预训练数据消融 Table VII
  - VLM 评测：Where2Place Point 0.163（vs 0.075），RefSpatial Placement 0.180（vs 0.012）（Table III）
## 本地引用关系

-
## 证据元数据

- Fulltext Quality: fulltext
- Evidence Coverage: complete（全文包含 Introduction、Related Works、System Overview、VLM Pre-training、VL-Action Post-Training、Simulation Evaluation、Real-World Experiments、Conclusion，共 8 节，含完整表格和消融实验）
- Confidence: high
- Summary: PokeVLA 提出轻量级（1.22B 参数）VLA 模型，通过两阶段训练——大规模 embodied VLM 预训练（2.4M 样本）和目标感知分割+几何对齐+动作查询注入的后训练——在 LIBERO-Plus 和真实场景达到 SOTA 成功率和鲁棒性。


## Problem

现有 VLA 模型存在三大瓶颈：
1. **预训练知识域间隙**：通用 VLM 的知识与机器人操控需求之间存在显著域差异
2. **缺少多视角空间一致性**：缺乏一致的空间信息导致对涉及绝对/相对位置的高级语言指令泛化不足
3. **缺乏高级知识预测**：无法预测与任务相关的高级知识，导致缺乏对操控目标的细粒度引导


## Method

### 两阶段框架

**Stage 1: PokeVLM 预训练**
- 基础架构：Prismatic-VLM 框架，Qwen2.5-0.5B 语言模型 + DINOv2 + SigLIP 双视觉编码器
- 预训练数据（约 2.4M 样本）：
  - 通用理解：LLaVA-Instruct-665K（665K）
  - 空间定位：RefSpatial Simulator + RoboPoint + RoboSpatial + RoboRefIt（694K）
  - Affordance：HOVA（Ego4D + Epic100）+ MolmoAct（553K）
  - 推理：RefSpatial 2D Reasoning + Cosmos-Reason1（511K）
- 所有点坐标归一化到 [0,1] 范围，去除错误标注，用 LLM 丰富操作语言描述

**Stage 2: VL-Action 后训练**

三大核心组件：

1. **Goal-Aware Segmentation（目标感知分割）**
   - 引入 `<SEG>` 特殊 token（受 LISA 启发），通过 embedding-as-mask 范式生成多视角语义分割 mask
   - Coarse-to-Fine 解码：粗阶段用 SAM prompt encoder 生成语义 logit map，细阶段精炼为高质量分割结果
   - 训练损失：sigmoid focal loss + KLD loss
   - 关键创新：单个 `<SEG>` token 与多视角输入交互，隐式编码场景 3D 结构知识

2. **Geometry Alignment（几何对齐）**
   - 仅训练阶段使用 VGGT（3D 几何基础模型），推理无额外开销
   - 将 VLM 最后一层视觉 token 的隐状态与 VGGT 提取的几何特征对齐
   - 损失函数：余弦相似度损失（式 5）

3. **Action Head（动作头）**
   - Action queries 通过 cross-attention 聚合四类信息：
     - VLM 最后一层的视觉隐状态 h_v（3D 空间结构）
     - `<SEG>` embedding h_seg（目标感知语义）
     - VLM 输出的 query embeddings h_q + 机器人本体感知状态 s_t
   - L 层结构，每层包含：self-attention（action latents）+ 3 个 cross-attention 模块
   - 最终通过 LayerNorm + MLP 输出 action chunk A_t
   - 损失：L1 loss

总体训练目标：L = L_action + 0.2 × L_seg + 0.4 × L_geo

### 训练细节
- VLM 预训练：8 GPU，batch size 128，AdamW，lr=2e-5，cosine decay，2 epochs
- 后训练：8 GPU，batch size 64，AdamW + LoRA，lr=1e-4，cosine annealing + warmup，150K steps


## Experiments

### 仿真基准（LIBERO）

| Method | Params(B) | Spatial | Object | Goal | Long | Total |
|--------|-----------|---------|--------|------|------|-------|
| OpenVLA | 7 | 84.7 | 88.4 | 79.2 | 53.7 | 76.5 |
| OpenVLA-OFT | 7 | 97.6 | 98.4 | 97.9 | 94.5 | 97.1 |
| π₀ | 3 | 96.8 | 98.8 | 95.8 | 85.2 | 94.2 |
| DreamVLA | 0.57 | 97.5 | 94.0 | 89.5 | 89.5 | 92.6 |
| VLA-Adapter | 1.22 | 99.6 | 99.6 | 98.2 | 96.4 | 98.5 |
| **PokeVLA** | **1.22** | **99.6** | **99.6** | **98.4** | **95.2** | **98.2** |

LIBERO 上接近饱和，1.22B 参数匹配 7B 模型性能。

### LIBERO-Plus（直接训练）

| Method | Params | Task Total | Perturbation Total |
|--------|--------|------------|-------------------|
| OpenVLA-OFT | 7B | 79.5 | 79.5 |
| VLA-Adapter | 1.22B | 81.0 | 81.0 |
| **PokeVLA** | **1.22B** | **83.5** | **83.5** |

在 7 种扰动下表现稳健：lighting 99.0%、background 99.3%、camera viewpoint 98.2%。

### LIBERO-Plus（零样本迁移，仅 LIBERO 训练）

| Method | Total |
|--------|-------|
| OpenVLA-OFT | 69.6 |
| VLA-Adapter | 59.1 |
| **PokeVLA** | **79.3** |

迁移优势显著：camera 84.7%（vs 56.4%）、language 84.8%（vs 79.5%）、noise 89.8%（vs 75.8%）。

### 真实世界（xArm7，8 任务，97 物体）

| Method | Task1-8 平均 |
|--------|-------------|
| OpenVLA-OFT | 20.0% |
| VLA-Adapter | 68.75% |
| **PokeVLA** | **81.25%** |

扰动场景：PokeVLA 63.0% vs VLA-Adapter 43.0%（+20.0%）。

### 消融实验（LIBERO-Plus，560 runs/suite）
- 去掉预训练：78.2% → 加上预训练 82.9%（+4.7%）
- 去掉几何对齐：+3.0%（长程任务从 75.5% → 81.4%）
- 去掉目标分割：+4.3%（对 lighting、background、noise 扰动提升最大）
- 三者结合：85.3%（从 baseline 78.2% 提升 7.1%）

### 预训练数据消融
- 去掉 Grounding 数据：Goal 和 Long 任务显著下降
- 去掉 Affordance 数据：robot initialization 鲁棒性从 46.6% 降至 39.7%
- 去掉 Reasoning 数据：language 扰动下从 73.1% 降至 66.9%

### VLM 评测
- PokeVLM 在 Where2Place、RefSpatial、CV-Bench 上均显著优于原始 Prismatic-VLM
- 空间定位能力大幅提升（如 Where2Place Point: 0.075 → 0.163），通用能力保持


## Limitations

1. Robot initialization 扰动仍然是最大挑战（LIBERO-Plus 52.9%），说明对初始位姿变化的适应仍有提升空间
2. Language perturbation 在 LIBERO-Plus fine-tuned 设定下为 71.4%，表明语义理解在复杂语言变化下仍有局限
3. 真实世界部分扰动场景成功率较低（如 Task8 P3: 3/10）
4. Tiny-scale VLM（0.5B）的推理能力可能受限于模型容量
5. 预训练数据主要覆盖桌面场景，对非结构化环境的泛化能力未验证


## Key Takeaways

1. **Embodied VLM 预训练的重要性**：2.4M 样本的多维预训练（grounding + affordance + reasoning）比单一数据类型更有效，每类数据贡献不同能力维度
2. **目标感知分割作为辅助任务**：通过 `<SEG>` token 引导的跨视角一致语义分割，能有效引导注意力聚焦于操控目标，显著提升鲁棒性
3. **Geometry alignment 的效率设计**：仅训练阶段使用 VGGT，推理零开销，是值得借鉴的 sim-to-real 友好设计
4. **Action queries 作为感知-动作桥梁**：受自动驾驶启发，用可学习 queries 聚合多源信息后注入 action expert，比直接传递原始特征更有效
5. **轻量化路径的可行性**：1.22B 参数在多项指标上匹配甚至超越 7B 模型，说明架构设计和训练策略的重要性不亚于参数规模
6. **对 DLO 操控的启示**：多视角一致性学习、目标感知分割和几何对齐的思路可迁移到 DLO 操控场景，特别是 DLO 的多视角几何理解

## 相关概念

- [[robotic-manipulation]]
- [[imitation-learning]]
- [[vision-language-model]]
- [[robot-learning]]
- [[sim-to-real]]
- [[deformable-linear-object]]
- [[grasping]]

## 相关研究者

- [[zheng-yupeng|Zheng, Yupeng]]
- [[gu|Gu, Songen]]
- [[zheng-yuhang|Zheng, Yuhang]]
