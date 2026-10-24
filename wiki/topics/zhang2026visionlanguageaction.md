---
title: "A vision-language-action model for adaptive ultrasound-guided needle insertion and needle tracking"
tags: [manipulation, VLM, robot-learning]
created: "2026-04-29"
updated: "2026-04-29"
type: "literature"
status: "done"
summary: "首次将 VLA 模型应用于机器人超声（RUS）引导的自动针插入与跟踪，提出 CDF 跟踪头融合多层视觉特征、TraCon 寄存器实现参数高效微调、异步管线解耦跟踪与控制、不确定性感知控制策略，在跟踪精度和插入成功率上显著优于现有方法和手动操作。"
authors: "Zhang, Yuelin; Ding, Qingpeng; Tang, Longxiang; Fang, Chengyu; Cheng, Shing Shin"
year: "2026"
venue: "arXiv Preprint"
zotero_key: "4KSXEIW9"
---
## 摘要

Ultrasound (US)-guided needle insertion is a critical yet challenging procedure due to dynamic imaging conditions and difficulties in needle visualization. Many methods have been proposed for automated needle insertion, but they often rely on hand-crafted pipelines with modular controllers, whose performance degrades in challenging cases. In this paper, a Vision-Language-Action (VLA) model is proposed for adaptive and automated US-guided needle insertion and tracking on a robotic ultrasound (RUS) system. This framework provides a unified approach to needle tracking and needle insertion control, enabling real-time, dynamically adaptive adjustment of insertion based on the obtained needle position and environment awareness. To achieve real-time and end-to-end（端到端） tracking, a Cross-Depth Fusion (CDF) tracking head is proposed, integrating shallow positional and deep semantic features from the large-scale vision backbone. To adapt the pretrained vision backbone for tracking tasks, a Tracking-Conditioning (TraCon) register is introduced for parameter-efficient feature conditioning. After needle tracking, an uncertainty-aware control policy and an asynchronous VLA pipeline are presented for adaptive needle insertion control, ensuring timely decision-making for improved safety and outcomes. Extensive experiments on both needle tracking and insertion show that our method consistently outperforms state-of-the-art（现有最优方法） trackers and manual operation, achieving higher tracking accuracy, improved insertion success rates, and reduced procedure time, highlighting promising directions for RUS-based intelligent intervention.

## 中文简述

提出基于视觉-语言的插入方法，具有端到端特点。

**研究方向**: 机器人操控、视觉-语言模型、机器人学习

## 关键贡献

1. **Cross-Depth Fusion (CDF) 跟踪头**：融合 ViT 编码器的浅层位置信息和深层语义信息，实现端到端实时针跟踪（~25 FPS），避免仅使用单层特征导致的信息损失。
2. **Tracking-Conditioning (TraCon) 寄存器**：仅 0.5M 参数的可学习 token，通过 Conditional Feature Gating 外部调节冻结的视觉骨干网络，实现参数高效的跟踪任务适配，避免了直接微调视觉编码器带来的跟踪-动作目标冲突。
3. **不确定性感知控制策略**：当针尖可视性下降时自动降低插入速度，遵循专家操作原则"看不清时减速"，确保操作安全和持续跟踪。
4. **异步 VLA 管线**：将跟踪（~25 FPS）与动作生成（~10 FPS）解耦为两个并行分支，保证实时跟踪反馈的同时维持精确的插入控制决策。
## 结构化提取

- Problem: 超声引导针插入中动态成像、针可视性差、手工管线脆弱、缺乏语义推理
- Method: 基于 Qwen2.5-VL-3B 的 VLA 模型，CDF 跟踪头 + TraCon 寄存器 + 异步管线 + 不确定性感知控制
- Tasks: US 引导针跟踪（IPS/IPM）、自适应针插入控制
- Sensors: 超声成像（Wisonic Clover 60, C5-1 凸阵探头）、光学跟踪器（ClaroNav MicronTracker 3，仅用于 GT 标注）
- Robot Setup: 自定义 RUS 平台（线性 manipulator 控制针轴向位移 + 伺服调整角度 + UR5e 机械臂操控超声探头，3-DOF 平移）
- Metrics: AUC(%), Precision(%), Err±SD(mm)（跟踪）; SUC(%), T(s)（插入，成功 = 针尖距目标 <5mm）
- Limitations: 跟踪速度仅勉强实时、数据集规模小、仅 phantom 验证、探头 3-DOF 有限、IPS 成功率仅 70%
- Evidence Notes: 全文从 arXiv HTML 获取，涵盖完整的实验结果表格和消融分析。主要证据来自 Table I（跟踪评估和消融）和 Table II（插入评估和消融），所有数字均直接来自原文。
## 本地引用关系

-
## 证据元数据

- Fulltext Quality: fulltext
- Evidence Coverage: complete（全文通过 arXiv HTML 获取，涵盖方法、实验、消融、讨论）
- Confidence: high
- Summary: 首次将 VLA 模型应用于机器人超声（RUS）引导的自动针插入与跟踪，提出 CDF 跟踪头融合多层视觉特征、TraCon 寄存器实现参数高效微调、异步管线解耦跟踪与控制、不确定性感知控制策略，在跟踪精度和插入成功率上显著优于现有方法和手动操作。


## Problem

超声（US）引导的针插入是重要的临床操作，但面临动态成像条件、针可视性差、遮挡和成像伪影等挑战。现有的自动化方法依赖手工设计的模块化管线（粒子滤波跟踪 + 独立控制器），在复杂场景下脆弱性高、泛化能力差，且缺乏高层语义推理能力。虽然 VLA 模型在开放世界任务中展现了强大的多模态理解和推理能力，但由于计算开销大、数据需求高，尚未被应用于超声引导的针插入与跟踪。


## Method

### 整体架构
基于 Qwen2.5-VL-3B 构建 VLA 模型，包含三个核心组件：
- **视觉编码器** ε_V：基于 ViT 的预训练视觉骨干（冻结）
- **CDF 跟踪头** φ_T：专用针跟踪模块
- **LLM** φ_L：用于解释输入和生成动作指令

输入包括超声图像观测 O_t = [x_t, z_t]（搜索图 + 模板图）和语言指令 I。

### TraCon 寄存器
- 轻量可学习 token R ∈ ℝ^{B×L_r×C}（L_r=4，仅 0.5M 参数）
- 拼接到视觉观测后输入冻结的 ViT 编码器
- 编码后的 TraCon 特征同时送入 CDF 跟踪头和 LLM
- 在 CDF 头中通过 Conditional Feature Gating（改进的 FiLM）与视觉特征融合：f' = f ⊙ (α·γ(r)) + α·β(r)，其中 α 为可学习标量门控

### CDF 跟踪头
- 从 ViT 提取浅层特征（位置信息为主）和深层特征（语义信息为主）
- **语义融合（SemFus）**：通过通道维度的 cross-attention 分别融合搜索图和模板图的跨深度特征
- **位置相关（PosCor）**：对融合后的特征进行空间维度的 attention 相关，定位目标
- 最终通过 Conditional Feature Gating 整合 TraCon 寄存器信息，预测 bounding box

### 异步管线
- **实时分支**：视觉编码 → CDF 跟踪头 → 输出针位置（~25 FPS）
- **深度分支**：视觉编码 → LLM → 输出动作指令（~10 FPS）
- 两个分支共享视觉编码器，跟踪分支不等 LLM 完成就处理下一帧

### 不确定性感知控制策略
- 语言指令模板：描述目标位置、插入技术，并指示"可视性下降时减速"
- 输出动作 A = [θ_n, v_n, v_p]：插入角度、插入速度、探头移动速度
- 到达目标时输出 [STOP] token 终止
- LLM 基于全局上下文推理自适应调节速度，无需显式的超参数调控

### 训练策略（2 阶段）
- **Stage 1**：跟踪预训练，仅训练 CDF 头和 TraCon 寄存器，冻结其余模块
  - 数据集 D_1：41,075 帧 / 239 视频（1920×1080），105 IPS + 134 IPM 试验
  - 光学跟踪器 ClaroNav MicronTracker 3 获取 GT（RMSE 0.189 mm）
  - 多种材料：鲜猪肉、琼脂、硅胶、人工肿瘤
- **Stage 2**：LLM 微调（LoRA），冻结 CDF 头和 TraCon 寄存器
  - 数据集 D_2：3,852 帧 / 18 视频，9 IPS + 9 IPM 试验
  - 专家演示收集动作 GT


## Experiments

### 针跟踪评估（Table I）
对比方法：SiamRPN++, SiamCAR, SiamBAN, SwinTrack, STMTrack, MixFormer, LoRAT

| 方法 | Mean AUC(%) | Mean P(%) | Mean Err±SD(mm) |
|------|------------|-----------|-----------------|
| LoRAT (次优) | 62.0 | 85.2 | 3.37±2.62 |
| **Ours** | **63.5** | **88.9** | **3.01±2.20** |

- Err 和 SD 分别改善 10.7% 和 16.0%
- 唯一在 IPS 和 IPM 两个任务上 SD < 2mm 的方法

跟踪消融（Table I 下半部分）：
- L_r=16 vs 默认 L_r=4：无明显改善甚至略差
- 无 TraCon（L_r=0）：AUC -0.7, P -2.8
- 仅浅层特征：Err +0.48, SD +0.42
- 仅深层特征：Err +0.31, SD +0.75

### 针插入评估（Table II）
- VLA RUS 插入：40 次尝试（20 IPS + 20 IPM）
- 手动插入：5 名经验用户各 8 次，共 40 次尝试

| 方法 | Mean SUC(%) | Mean T(s) |
|------|------------|-----------|
| Manual | 60.0 | 23.2 |
| **Ours** | **80.0** | **17.3** |

- 成功率提升 33.3%（IPM 更达 63.6%），时间减少 25.4%
- 跟踪 FPS 25.1，动作生成 FPS 10.4

插入消融（Table II 下半部分）：
- L_r=16：SUC -5.0%
- 无 TraCon：SUC -7.5%，T +7.2s
- 无异步管线：SUC -12.5%（跟踪和动作共享 13.1 FPS，不满足实时需求）
- 无不确定性控制：SUC -10.0%（恒速 10 mm/s 导致跟踪丢失）


## Limitations

1. 跟踪速度仅勉强满足实时需求（~25 FPS），效率仍有提升空间
2. 数据集规模有限（跟踪集 239 视频、插入集仅 18 视频），多样性和泛化性待验证
3. 仅在 phantom/simulator 上验证，缺乏真实临床场景评估
4. 探头操作仅 3 自由度平移，未利用多自由度主动增强针可视性
5. 未与现有手工管线或 VLA 模型进行定量比较（理由是缺乏开源实现）
6. 插入成功率在 IPS 场景下仅 70%，仍有较大失败率


## Key Takeaways

1. **VLA 在医疗机器人中的应用范式**：该工作首次将 VLA 模型应用于 RUS 引导的针插入，展示了大模型在医疗场景中"感知-推理-行动"统一的潜力。异步管线设计对其他需要不同频率感知和控制的机器人任务有借鉴价值。

2. **参数高效适配策略**：TraCon 寄存器通过 0.5M 参数的外部调节实现视觉骨干的跟踪任务适配，避免了直接微调带来的多任务冲突。这种"外部调节而非内部修改"的思路对 DLO 操控等数据稀缺场景同样适用。

3. **与 DLO 操控的关联**：不确定性感知控制策略（可视性差时减速）可类比到 DLO 操控中的遮挡处理。CDF 跟踪头融合浅层位置和深层语义特征的设计思路，对于 DLO 形状跟踪和状态估计也有参考价值。

4. **异步管线架构**：将高频跟踪与低频决策解耦的异步设计，适用于任何需要同时进行实时感知和高层决策的机器人系统，包括 DLO 操控中的连续形状跟踪与间歇性策略调整。

5. **局限性参考**：小规模数据集上的 VLA 训练仍具挑战性，TraCon 的轻量适配是关键；实时性约束在 VLA 架构中不可忽视，需要专用模块处理高频任务。

## 相关概念

- [[robotic-manipulation]]
- [[vision-language-model]]
- [[robot-learning]]
- [[sim-to-real]]
- [[deformable-linear-object]]

## 相关研究者

- [[zhang-yuelin|Zhang, Yuelin]]
- [[cheng-shing-shin|Cheng, Shing Shin]]
