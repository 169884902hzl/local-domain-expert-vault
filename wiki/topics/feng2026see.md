---
title: "See what matters: Differentiable grid sample pruning for generalizable vision-language-action model"
tags: [manipulation, imitation, VLM]
created: "2026-05-13"
updated: "2026-05-13"
type: "literature"
status: "done"
summary: "GridS 提出可微双线性网格采样模块，将 VLA 视觉 token 从 256 压缩至 16（甚至 1），通过端到端优化的连续坐标预测保留亚 patch 级空间精度，在 76% FLOPs 削减下不降成功率且 OOD 泛化提升 28.6%。"
authors: "Feng, Yixu; Zhao, Zinan; Ma, Yanxiang; Xia, Chenghao; Du, Chengbin et al."
year: "2026"
venue: "arXiv Preprint"
zotero_key: "ZNCQ6JEE"
---
## 摘要

Vision-Language-Action (VLA) models have shown remarkable promise in robotics manipulation（操控）, yet their high computational cost hinders real-time deployment. Existing token pruning methods suffer from a fundamental trade-off: aggressive compression using pruning inevitably discards critical geometric details like contact points, leading to severe performance degradation. This forces a compromise, limiting the achievable compression rate and thus the potential speedup. We argue that breaking this trade-off requires rethinking compression as a geometry-aware, continuous token resampling in the vision encoder. To this end, we propose the Differentiable Grid Sampler (GridS), a plug-and-play module that performs task-aware, continuous resampling of visual tokens in VLA. By adaptively predicting a minimal set of salient coordinates and extracting features via differentiable interpolation, GridS preserves essential spatial information while achieving drastic compression (with fewer than 10% original visual tokens). Experiments on both LIBERO benchmark and a real robotic platform demonstrate that validating the lowest feasible visual token count reported to date, GridS achieves a 76% reduction in FLOPs with no degradation in the success rate. The code is available at https://github.com/Fediory/Grid-Sampler.

## 中文简述

提出基于视觉-语言的操控方法，具有泛化能力特点。

**研究方向**: 机器人操控、模仿学习、视觉-语言模型

## 关键贡献

1. 提出 GridS（Differentiable Grid Sampler），首个将 VLA token 压缩重构为几何感知的连续重采样过程的模块，突破离散选择的量化误差限制
2. 设计可微双线性采样机制，支持亚 patch 级特征提取并保持端到端梯度流动，仅用任务损失训练无需辅助监督
3. 在 π₀/π₀.₅/SmolVLA 三种 VLA 架构上验证即插即用性，LIBERO 上 256→16 token 实现 76% FLOPs 削减且成功率 +1.6%
4. 发现极端压缩（K=1）下 π₀.₅ 仍能保持 96.6% vs baseline 96.7%，揭示了 VLA 视觉信息中的大量冗余
5. 真实机器人实验表明 GridS 在 OOD 场景下成功率提升 28.6%，并揭示了"学习即遗忘"的信息瓶颈效应
## 结构化提取

- Problem: VLA 视觉 token 数量过多导致计算瓶颈；现有离散 token pruning 方法在压缩率与操控精度间存在权衡，亚 patch 级关键信息被丢失
- Method: GridS（Differentiable Grid Sampler）——全局平均池化→MLP 预测连续坐标→可微双线性插值采样→坐标位置嵌入注入，即插即用模块
- Tasks: 桌面操控（pick-place/stack/insert）、双臂操控（transfer cube/bimanual insertion）、长序列任务
- Sensors: RGB 图像（第三人称 Intel RealSense D435 + 腕部 RealSense D405），不使用深度
- Robot Setup: 仿真（LIBERO 单臂、ALOHA 双臂 MuJoCo）；真实（LeRobot SO-100 单臂 6-DoF）
- Metrics: 成功率 SR(%)、FLOPs(G)、推理时间(s)、OOD 成功率、训练时间/step、信息保留度
- Limitations: 单 batch 推理加速有限(~1.2×)；静态 K 值不能自适应；LoRA 下 -8.3%；Robot Initial States 和 Language 扰动退化
- Evidence Notes: 全文 25 页含完整实验；LIBERO 4 suites × 多 backbone × 多 token 预算；真实 3 任务 × 21 OOD 场景；LIBERO-PLUS 7 维扰动 × 5 难度等级；RoboTwin 补充实验；消融实验覆盖 pooling/MLP/坐标注入/插值方法
## 本地引用关系

-
## 证据元数据

- Fulltext Quality: fulltext
- Evidence Coverage: high（全文 25 页，含 6 个 Appendix，实验覆盖 LIBERO/ALOHA/Real-world/LIBERO-PLUS/RoboTwin）
- Confidence: high
- Summary: GridS 提出可微双线性网格采样模块，将 VLA 视觉 token 从 256 压缩至 16（甚至 1），通过端到端优化的连续坐标预测保留亚 patch 级空间精度，在 76% FLOPs 削减下不降成功率且 OOD 泛化提升 28.6%。


## Problem

VLA 模型因视觉编码器生成大量 token（如 DINOv2 产生 16×16=256 个），导致下游 Transformer 的二次方计算瓶颈。现有 token pruning 方法（语义剪枝/动态剪枝）依赖离散 patch 选择，存在量化误差——当操控关键点（如抓取点）恰好在两个 patch 边界时，离散选择不可避免地丢失空间精度。这种"效率-性能"权衡限制了可用压缩率。


## Method

### 核心架构（两阶段）
**阶段一：全局坐标预测**
- 将密集特征图 T_dense 通过 Global Average Pooling 聚合为上下文向量 z ∈ R^C
- 轻量 MLP 预测 K 组连续归一化坐标 P ∈ [0,1]^{K×2}（Sigmoid 确保坐标在图像范围内）
- K ≪ H×W（如 K=16 vs 256）

**阶段二：网格采样 + 几何注入**
- 对预测坐标执行可微双线性采样：每个坐标从最近 4 个 patch 特征加权插值
- 权重 ω 由坐标偏移计算：ω₁=(1-Δx)(1-Δy), ω₂=Δx(1-Δy), ω₃=(1-Δx)Δy, ω₄=ΔxΔy
- Coordinate Encoder 将预测坐标映射为位置嵌入，加到采样特征上恢复空间感知

### 关键技术特点
- **可微性**：双线性插值对坐标 (x,y) 完全可微，梯度从任务损失回传到坐标预测器，实现数据驱动的自适应采样
- **即插即用**：模块插入视觉编码器和 Transformer 之间，与标准微调联合优化
- **无需辅助损失**：仅用主任务损失（flow-matching 或自回归），无 ground-truth attention map

### 训练目标
- 端到端联合优化，GridS 在标准 VLA fine-tuning 过程中一起训练
- 无额外 pipeline 步骤，因为 VLA 本身需要 fine-tuning


## Experiments

### 数据集/Benchmark
| Benchmark | 任务类型 | 评估内容 |
|-----------|---------|---------|
| LIBERO (4 suites) | 仿真桌面操控 | Spatial/Object/Goal/Long，各 10 任务 |
| ALOHA | 仿真双臂操控 | Transfer Cube / Bimanual Insertion |
| Real-world (SO100) | 真实单臂 | Pick & Place / Transfer Pen / Stack Cubes |
| LIBERO-PLUS | 零样本 OOD | 7 维扰动×5 难度等级，10030 任务 |
| RoboTwin 2.0 | 仿真双臂 | Place Bread Skillet |

### 主要结果

**LIBERO (π₀ backbone)：**
| 配置 | Vis. Tokens | FLOPs (G) | Time (s) | Avg. SR (%) | Δ SR |
|------|-----------|----------|---------|------------|------|
| π₀ baseline | 256 | 216.01 | 8.17 | 94.4 | — |
| π₀ + FastV† | 100 | 143.59 | 7.32 | 92.9 | -1.5 |
| π₀ + SparseVLM† | 100 | 150.30 | 7.48 | 89.8 | -4.6 |
| π₀ + VLA-Cache† | 256 | 188.12 | 7.52 | 93.8 | -0.6 |
| **π₀ + GridS₁₆** | **16** | **51.65** | **6.05** | **96.0** | **+1.6** |
| π₀ + GridS₄ | 4 | 43.61 | 5.86 | 95.5 | +1.1 |

**π₀.₅ backbone：** GridS₁₆ 从 96.7% → 97.7%（+1.0），GridS₄ 保持 96.7%（+0.0）

**真实世界 (SmolVLA, SO100)：**
- Stack Cubes：GridS 60.0% vs Baseline 7.6%（+52.4%）
- OOD 场景：GridS 38.1% vs Baseline 0%
- 推理时间减少最高 3.3s

**极端压缩 (K=1, π₀.₅)：** 96.6% vs dense 96.7%，仅差 0.1%

**训练加速：** batch=128 时 π₀ 加速 3.4×，π₀.₅ 加速 2.9×

### 消融实验
- **Token 数量**：真实 Stack Cubes 任务呈倒 U 形，K=16 最优（61.9%），K=4 完全失败，K=32 退化至 19%
- **替代下采样**：Random Sampling 87.8%，Top-K 90.5%，GridS 96.0%
- **架构消融**：GAP > Conv-Downsample(-4.4%)，SAM 引导(-6.2%)，去坐标注入(-3.6%)，最近邻插值(-4.1%)
- **视点丢失鲁棒性**：仅腕部相机时 GridS 在 Long 任务上 70% vs Baseline 30%

### LIBERO-PLUS 零样本 OOD
- 视觉/空间扰动（Camera Viewpoints）上 GridS 大幅领先：Spatial +19.4%，LIBERO-10 +10.8%
- Sensor Noise / Light Conditions 上 GridS 持续优于 baseline
- Robot Initial States 和 Language Instructions 上 GridS 弱于 baseline（-8%~-14% / -6%~-12%）
- 整体保持接近无损：Spatial -0.4%，Goal -0.2%


## Limitations

1. **单次推理加速有限**：单 batch 推理仅 ~1.2× 加速，因 JAX 编译后密集 baseline 已高度优化，瓶颈在固定 kernel 开销
2. **静态 token 预算**：K 值需预设，不能根据场景复杂度自适应调整；过多 token 引入噪声反而降低性能
3. **PEFT 兼容性差**：与 LoRA 配合时低于 dense baseline 8.3%，因 GridS 改变了空间分布，LoRA 参数不足以重新对齐注意力
4. **Robot Initial States 敏感**：关节角大幅偏移时需高分辨率运动链反馈，压缩过度会丢失本体感受细节
5. **语言指令扰动退化**：极端压缩可能丢弃理解复杂语言指令所需的细微视觉线索


## Key Takeaways

1. **连续采样 > 离散剪枝**：对于需要亚 patch 精度的操控任务，可微双线性采样优于离散 patch 丢弃，这一结论可能适用于 DLO 操控中的接触点定位
2. **信息瓶颈即正则化**：压缩到 10% 甚至 0.4% token 反而提升 OOD 泛化，因为强制模型学习因果物理机制而非记住环境布局——这与 DLO 操控中减少对特定构型过拟合的思路一致
3. **即插即用设计**：GridS 不改变 VLA 主干架构，仅插入视觉编码器后，可考虑将类似思路应用于 DLO 的视觉感知模块
4. **倒 U 形 token 曲线**：存在最优 token 数量，过多引入噪声——在 DLO 多阶段操控中可能需要按任务阶段动态调整
5. **与异步执行互补**：GridS 降低视觉编码器开销，异步架构（SmolVLA/RTC）解耦视觉与控制频率，两者可叠加

## 相关概念

- [[robotic-manipulation]]
- [[imitation-learning]]
- [[vision-language-model]]
- [[deformable-linear-object]]
- [[bimanual-manipulation]]
- [[grasping]]

## 相关研究者

- [[feng-yixu|Feng, Yixu]]
