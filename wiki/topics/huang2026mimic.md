---
title: "Mimic intent, not just trajectories"
tags: [manipulation, imitation, VLM, planning]
created: "2026-05-02"
updated: "2026-05-02"
type: "literature"
status: "done"
summary: "提出频域多尺度 action tokenizer (SDAT)，通过 DCT 频谱分解将行为意图与执行细节解耦，实现意图驱动的模仿学习、one-shot 技能迁移和泛化增强"
authors: "Huang, Renming; Zeng, Chendong; Tang, Wenjing; Cai, Jintian; Lu, Cewu et al."
year: "2026"
venue: "arXiv Preprint"
zotero_key: "J5233CPF"
---
## 摘要

While imitation learning（模仿学习） (IL) has achieved impressive success in dexterous manipulation（灵巧操控） through generative modeling and pretraining（预训练）, state-of-the-art（现有最优方法） approaches like Vision-Language-Action (VLA) models still struggle with adaptation to environmental changes and skill transfer. We argue this stems from mimicking raw trajectories without understanding the underlying intent. To address this, we propose explicitly disentangling behavior intent from execution details in end-2-end IL: Mimic Intent, Not just Trajectories(MINT). We achieve this via multi-scale frequency-space tokenization, which enforces a spectral decomposition of action chunk representation. We learn action tokens with a multi-scale coarse-to-fine structure, and force the coarsest token to capture low-frequency global structure and finer tokens to encode high-frequency details. This yields an abstract Intent token that facilitates planning and transfer, and multi-scale Execution tokens that enable precise adaptation to environmental dynamics. Building on this hierarchy, our policy generates trajectories through next-scale autoregression, performing progressive intent-to-execution reasoning, thus boosting learning efficiency and generalization. Crucially, this disentanglement enables one-shot（单样本） transfer of skills, by simply injecting the Intent token from a demonstration（示范数据） into the autoregressive generation process. Experiments on several manipulation（操控） benchmarks and on a real robot demonstrate state-of-the-art（现有最优方法） success rates, superior inference efficiency, robust generalization against disturbances, and effective one-shot（单样本） transfer.

## 中文简述

提出基于模仿学习的灵巧手方法，具有泛化能力特点。

**研究方向**: 机器人操控、模仿学习、视觉-语言模型、运动规划

## 关键贡献

1. **频谱解耦动作分词器 (SDAT)**：通过 DCT 将 action chunk 从时域变换到频域，使用多尺度残差量化将轨迹分解为低频意图 token (S1) 和高频执行 token (S2~SK)
2. **逐尺度频谱重建目标**：渐进式频域重建约束，强制粗粒度 token 捕获低频全局结构，细粒度 token 专精高频细节，实现 intent-execution 的结构性解耦
3. **Next-scale 自回归策略**：跨尺度自回归、尺度内并行生成的混合注意力机制，实现从意图到执行的渐进推理
4. **意图驱动动作集成 (Intent-based Action Ensemble)**：基于意图 token 余弦相似度的自适应加权，解决行为切换时的时间一致性冲突
5. **One-shot 技能迁移**：从单次示范提取意图 token 并注入策略的自回归生成过程，无需微调即可实现新任务/新布局/扩展时序的迁移
## 结构化提取

- Problem: VLA 模型直接模仿轨迹无法理解行为意图，导致泛化和迁移能力差
- Method: 频谱解耦动作分词器 (SDAT) + Next-scale 自回归策略 + 意图驱动动作集成
- Tasks: 桌面操控（物体操作、长时序组合任务、灵巧操控）；基准包括 LIBERO, CALVIN, MetaWorld, LIBERO-Plus
- Sensors: RGB 图像（单/双摄像头）+ 语言指令 + 机器人本体感知状态
- Robot Setup: 仿真 (LIBERO/CALVIN/MetaWorld) + 真实 6-DOF Piper-X 机械臂
- Metrics: 任务成功率 (LIBERO/MetaWorld), 平均完成序列长度 (CALVIN), 泛化成功率 (LIBERO-Plus), one-shot 迁移成功率
- Limitations: 意图多样性受限于训练数据；未利用大规模网络数据；意图 token 组合性未探索
- Evidence Notes:

  - SDAT 频谱约束使 S1 token 在 t-SNE 中形成语义一致的行为聚类（图 1、图 6）
  - 逐尺度时域约束过拟合高频噪声，性能低于无逐尺度约束（82.8% vs 87.8%）
  - 意图 token 注入 one-shot 迁移平均 77%，语言 fine-tune 仅 17%（Table III）
  - 真实机器人上比 π₀.5 高 29%，仅用 20 次示范/任务
## 本地引用关系

-
## 证据元数据

- Fulltext Quality: fulltext (arXiv HTML conversion, 75K chars, all sections readable including tables, figures descriptions, and references)
- Evidence Coverage: comprehensive (method, experiments, ablations, real-robot, one-shot transfer all covered)
- Confidence: high
- Summary: 提出频域多尺度 action tokenizer (SDAT)，通过 DCT 频谱分解将行为意图与执行细节解耦，实现意图驱动的模仿学习、one-shot 技能迁移和泛化增强


## Problem

当前端到端模仿学习（尤其是 VLA 模型）直接模仿原始轨迹信号，未建模"为什么执行这些动作序列"。导致策略过拟合于示范数据的表面关联，而非捕获底层的**行为意图 (behavioral intent)**。这造成：(1) 环境变化下的泛化能力差；(2) 技能迁移困难。


## Method

### 整体框架
MINT 是一个两阶段模仿学习框架：
- **阶段 1**：训练 SDAT 分词器，从示范轨迹学习结构化离散表征
- **阶段 2**：训练 MINT 策略，在学到的 token 空间中进行渐进式意图到执行推理

### SDAT (Spectrally Disentangled Action Tokenizer)
1. **Action Encoder**: 将连续动作序列 A ∈ R^{H×D} 编码为压缩潜变量 f ∈ R^{L×C}
2. **多尺度残差量化**: 递归地在残差特征上进行量化，产生 K 个尺度的 token maps S = {s1, ..., sK}，共享 codebook (V 个向量)
3. **频谱解码器**: 对每个累积特征 f̂^(k) 解码到时域再 DCT 到频域，得到频谱重建 F^(k)
4. **逐尺度频谱损失**: L_freq = Σ λk ||F - F^(k)||²，强制不同尺度关注不同频段
5. **训练目标**: L_freq + Codebook loss + Commitment loss + 辅助 L1 重建

### MINT 策略学习
- **Next-scale 自回归**: p(s1, s2, ..., sK) = Π p(sk | s1, ..., s_{k-1})，尺度间自回归、尺度内并行
- **混合注意力掩码**: token map 在尺度 k 只能 attend 到 ≤k 的尺度
- **意图驱动集成**: 动作 a_t = Σ w_h^{intent} · a_{t|o_{t-h}}，权重由意图 token 余弦相似度确定

### 模型架构
- **MINT-30M**: 从零训练的 decoder-only Transformer (30M 参数)，frozen SigLIP + DINOv2 视觉编码，frozen BERT 语言编码 + FiLM
- **MINT-4B**: PaliGemma-2.6B VLM backbone (frozen) + 300M action expert (from scratch)，总参数约 4B


## Experiments

### 基准性能 (Table I)
| Benchmark | MINT-30M | MINT-4B | 最佳 baseline |
|-----------|----------|---------|---------------|
| LIBERO Avg | 95.2 | ~97 | π₀.5: 96.9 |
| LIBERO-90 | - | 97.7 | π₀.5: 96.0 |
| CALVIN (len) | - | ~4.5 | RoboVLMs: 4.49 |
| MetaWorld Avg | - | ~56 | π₀: 50.8 |

注：MINT-30M 在 LIBERO 上远超 OpenVLA (76.5) 和 π₀ (86.0)；MINT-4B 在 MetaWorld Very Hard 任务上成功率近乎 π₀ 的 3 倍。

### 泛化 (LIBERO-Plus, Table II)
- MINT 在相机视角变化和机器人初始化偏移上显著优于所有 baseline
- MINT-4B+ (fine-tuned) 在 7 个扰动维度上平均表现超过 π₀.5+，特别是 Camera (95.2 vs 67.2) 和 Noise (92.3 vs 72.6)
- 比最强 baseline OpenVLA-OFT 高约 15% 成功率

### One-shot 迁移 (Table III)
| 方法 | 新任务 | 新布局 | 扩展时序 | 平均 |
|------|--------|--------|----------|------|
| Replay | 0.28 | 0.12 | 0.04 | 0.11 |
| Fine-tune (MINT-30M, language) | 0.42 | 0.08 | 0.00 | 0.17 |
| **Intent-injection (MINT-Zero-30M)** | **0.90** | **0.68** | **0.72** | **0.77** |

意图 token 注入比语言指令 one-shot fine-tune 高出约 60%。

### 真实机器人实验
- **平台**: 6-DOF Piper-X 机械臂，双摄像头 RGB 输入
- **数据**: 每任务 20 次示范，BridgeDataV2 (60K 轨迹) 预训练
- **任务**: 放置香蕉、堆叠积木 (seen)、插入标记 (seen)、堆叠杯子 (unseen)
- **结果**: MINT-4B 在所有任务上统计显著优于 ACT、π₀、π₀*.5，比 π₀*.5 总体高约 29%
- **零样本泛化**: 在未见过的"堆叠杯子"任务上，MINT 通过共享"堆叠"意图有效泛化

### 消融实验 (Table IV)
| 设置 | CALVIN (len) | LIBERO-Long |
|------|-------------|-------------|
| Terminal Time-Domain Loss | 4.36 | 87.8 |
| + Terminal Spectral Loss | 4.41 | 88.2 |
| + Scale-Wise Time-Domain Loss | 4.06 | 82.8 |
| **Scale-Wise Spectral Loss (ours)** | **4.54** | **93.4** |
| No Ensemble | 4.09 | 85.8 |
| Temporal Ensemble (ACT) | 4.32 | 89.2 |
| Action-based Ensemble | 4.10 | 90.4 |
| **Intent-based Ensemble (ours)** | **4.57** | **93.2** |

关键发现：逐尺度时域约束反而降低性能 (82.8%)，因过拟合高频噪声；频谱分解是解耦意图与执行的关键。


## Limitations

1. **意图多样性受限于训练数据**：MINT 依赖轨迹示范学习意图，意图的种类和覆盖范围受限于可用数据集
2. **未探索大规模网络数据**：使用互联网规模视频数据可提供更丰富的行为和更广泛的任务覆盖
3. **意图 token 的组合性**：离散意图 token 的重组以零样本合成新行为尚待探索


## Key Takeaways

### 对 DLO 操控的启示
- **频谱分解思路适用于 DLO**：DLO 轨迹同样具有低频全局形变和高频局部调整的结构，SDAT 的思路可直接迁移到 DLO 操控的动作表征
- **意图 token 作为技能描述符**：对于 DLO 的不同操控模式（缠绕、打结、展平），意图 token 可作为比语言更精确的技能指定方式
- **One-shot 迁移能力**：单次示范即可提取意图 token 迁移到新布局，对 DLO 的新物体/新配置场景有直接价值

### 对 VLM-based 控制的启示
- **解耦优于端到端**：显式分离高层意图和低层执行比直接映射 (VLM → action) 更高效
- **频域优于时域**：频谱约束能学到语义更一致的 token 空间（t-SNE 可视化验证），时域约束会导致碎片化
- **小模型也能强泛化**：MINT-30M (从零训练) 在泛化上超越多个预训练 VLA，说明架构设计比参数量更重要

## 相关概念

- [[robotic-manipulation]]
- [[imitation-learning]]
- [[vision-language-model]]
- [[planning]]
- [[deformable-linear-object]]
- [[grasping]]

## 相关研究者

- [[huang-renming|Huang, Renming]]
