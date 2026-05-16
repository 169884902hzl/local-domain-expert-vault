---
title: "VLA-Thinker: Boosting Vision-Language-Action Models through Thinking-with-Image Reasoning"
tags: [manipulation, imitation, VLM, RL, robot-learning]
created: "2026-05-07"
updated: "2026-05-07"
type: "literature"
status: "done"
summary: "首个\"thinking-with-image\"推理框架的 VLA 模型，将视觉感知建模为可动态调用的推理动作（ZOOM-IN 裁剪工具），通过 SFT 冷启动 + GRPO 轨迹级 RL 两阶段训练，在 LIBERO 上达到 97.5% SOTA 成功率。"
authors: "Wang, Chaoyang; Bao, Wenrui; Gao, Sicheng; Xu, Bingxin; Tian, Yu et al."
year: "2026"
venue: "arXiv Preprint"
zotero_key: "V68I74HU"
---
## 摘要

Vision-Language-Action (VLA) models have shown promising capabilities for embodied intelligence, but most existing approaches rely on text-based chain-of-thought reasoning where visual inputs are treated as static context. This limits the ability of the model to actively revisit the environment and resolve ambiguities during long-horizon（长时序） tasks. We propose VLA-Thinker, a thinking-with-image reasoning framework that models perception as a dynamically invocable reasoning action. To train such a system, we introduce a two-stage training pipeline consisting of (1) an SFT cold-start phase with curated visual Chain-of-Thought data to activate structured reasoning and tool-use behaviors, and (2) GRPO-based reinforcement learning（强化学习） to align complete reasoning-action trajectories with task-level success. Extensive experiments on LIBERO and RoboTwin 2.0 benchmarks demonstrate that VLA-Thinker significantly improves manipulation（操控） performance, achieving 97.5% success rate on LIBERO and strong gains across long-horizon（长时序） robotic tasks. Project and Codes: https://cywang735.github.io/VLA-Thinker/ .

## 中文简述

提出基于强化学习的线缆操控方法，具有长时序任务特点。

**研究方向**: 机器人操控、模仿学习、视觉-语言模型、强化学习、机器人学习

## 关键贡献

1. **Thinking-with-Image 推理范式**：首个将视觉感知建模为可动态调用的推理动作的 VLA 模型，实现了感知-推理-动作的交织（interleaved）协作过程，而非传统的静态视觉编码+纯文本推理。
2. **两阶段训练管线**：SFT 冷启动阶段使用 Qwen3-VL-30B-A3B 合成的视觉 CoT 数据激活结构化推理和工具调用行为；GRPO 强化学习阶段在稀疏的任务级成功奖励下对完整推理-动作轨迹进行因果对齐。
3. **SOTA 性能**：在 LIBERO 基准上达到 97.5% 平均成功率（+6.5% vs OpenVLA-OFT），在 RoboTwin 2.0 双臂操控基准上全面领先，尤其长时序任务优势显著。
## 结构化提取

- Problem: 现有 VLA 推理方法采用文本链式推理范式，视觉输入被一次性静态编码，无法在长时序操控中主动重观察环境以解决歧义和从错误中恢复
- Method: Thinking-with-Image 框架 + 两阶段训练（SFT 冷启动合成 CoT 数据 + GRPO 轨迹级 RL），将 ZOOM-IN 裁剪工具作为可动态调用的推理动作，基于 OpenVLA-OFT 基座模型
- Tasks: 语言引导的机器人操控（LIBERO: Spatial/Object/Goal/Long 任务套件；RoboTwin 2.0: 双臂协作任务，涵盖短/中/长/超长时序）
- Sensors: 单视角 RGB 图像（不用腕部相机），语言指令，本体感知状态（LIBERO 不用本体感知）
- Robot Setup: LIBERO 单臂 Franka Panda；RoboTwin 2.0 双臂机器人（多种构型），仿真环境
- Metrics: 成功率 SR (Success Rate, %)，每任务 50（LIBERO）或 100（RoboTwin 2.0）个随机化初始场景
- Limitations: 仅单一 ZOOM-IN 视觉工具；继承 MLLM 幻觉问题；仅仿真验证无真实机器人实验
- Evidence Notes: 全文证据完整，包含完整方法描述、定量实验结果（LIBERO 四个套件 + RoboTwin 2.0 三个时序层级）、消融实验（训练阶段消融）、训练曲线分析、推理速度对比。缺少：真实机器人实验、多样视觉工具的消融、Sim-to-Real 迁移验证。
## 本地引用关系

-
## 证据元数据

- Fulltext Quality: fulltext
- Evidence Coverage: complete（全文包含 Abstract、Introduction、Method、Experiments、Ablation、Related Work、Conclusion、Appendix）
- Confidence: high
- Summary: 首个"thinking-with-image"推理框架的 VLA 模型，将视觉感知建模为可动态调用的推理动作（ZOOM-IN 裁剪工具），通过 SFT 冷启动 + GRPO 轨迹级 RL 两阶段训练，在 LIBERO 上达到 97.5% SOTA 成功率。


## Problem

现有 VLA 推理方法（如 CoT-VLA、ECoT）依赖文本链式推理范式：视觉输入被一次性编码为静态上下文，推理过程主要在语言空间展开。这限制了模型在长时序操控任务中主动重新观察环境、解决歧义和从中间错误中恢复的能力。尤其当任务涉及精细空间定位或多步骤子目标跟踪时，静态视觉编码不足以支撑鲁棒决策。


## Method

### 核心思想
将感知（perception）从被动的一次性输入转变为可主动调用的推理动作。在推理过程中，模型可以动态调用视觉工具（如 ZOOM-IN 裁剪）获取任务相关的局部视觉证据，形成多模态交织的推理-动作轨迹。

### 问题形式化
给定语言指令 T₀ 和初始视觉观测 V₀，模型迭代生成序列：
- τ = {T₁, C₁, V₁, T₂, C₂, V₂, ..., Tₖ, Aₖ}
- Tₖ: 文本推理步骤（中间假设/思考）
- Cₖ: 感知工具调用（如 crop_image）
- Vₖ: 工具返回的视觉证据（裁剪后的子图）
- Aₖ: 最终环境动作

每次迭代由控制器/解析器决定：继续推理+调用工具，还是终止并输出动作。

### 视觉工具
当前仅实现一种工具：**ZOOM-IN**（crop_image），按 bbox 裁剪指定区域以获取细节。作者明确表示此工具仅作为代表性实例验证范式有效性，期待社区探索更多视觉工具。

### 训练策略

**阶段 1：SFT 冷启动**
- 使用 Qwen3-VL-30B-A3B-Instruct 合成高质量具身 CoT 数据
- 关键帧选择：通过检测夹爪状态变化确定子任务边界
- 关键帧：生成包含工具调用和文本推理的完整 CoT 注释
- 中间帧：生成纯文本 CoT 推理注释保证连续性
- 数据量：LIBERO 273,465 标注关键帧；RoboTwin 2.0 215,784 标注关键帧
- 训练：100k steps，batch size 64，lr 1e-5，混合注意力掩码（CoT 自回归 + 动作双向）

**阶段 2：GRPO 强化学习**
- 奖励函数：R(τ) = αs·I_success + αf·I_format（稀疏，仅轨迹末尾给出）
- 采样一组 M 条轨迹，用组内相对优势消除显式价值函数
- 训练：batch size 128，lr 2e-6，KL 惩罚防止灾难性遗忘
- 目标函数跟随 DeepSeek R1 的 GRPO 公式

### 基座模型
基于 OpenVLA-OFT（OpenVLA + LLaMA2-7B + action chunking + parallel decoding），仅使用单视角图像、语言指令和本体感知状态作为输入（不用腕部相机）。


## Experiments

### 基准
1. **LIBERO**：语言引导操控，5 个任务套件（Spatial/Object/Goal/Long/90），每任务 50 个测试场景
2. **RoboTwin 2.0**：双臂操控模拟基准，50 个双臂协作任务，强域随机化，每任务 100 个测试场景

### LIBERO 主结果（Tab. 2）

| Model | Spatial | Object | Goal | Long | Avg |
|-------|---------|--------|------|------|-----|
| OpenVLA-OFT | 91.6 | 95.3 | 90.6 | 86.5 | 91.0 |
| VLA-Thinker (Ours) | **98.7** | **99.0** | **95.2** | **96.9** | **97.5** |
| Δ | +7.1 | +3.7 | +4.6 | +10.4 | +6.5 |

对比其他 SOTA：UnifiedVLA (95.5%), π₀ (94.2%), GR00T N1 (93.9%), PD-VLA (94.7%)。

### RoboTwin 2.0 主结果（Tab. 3）

| Horizon | VLA-Thinker | OpenVLA-OFT | DeepThinkVLA | π₀ |
|---------|-------------|-------------|--------------|------|
| Short (100-130 steps) | **62.3** | 21.3 | 55.0 | 45.5 |
| Medium (150-230 steps) | **70.7** | 47.1 | 65.3 | 58.8 |
| Long+ExtraLong (280-650 steps) | **64.6** | 46.5 | 57.8 | 43.3 |

关键观察：随着任务时序增长，VLA-Thinker 的相对优势更显著，说明 thinking-with-image 有效缓解了长推理-动作链中的误差累积。

### 消融实验（Tab. 4）

| Method | Spatial | Object | Goal | Long | Avg |
|--------|---------|--------|------|------|-----|
| OpenVLA-OFT | 91.6 | 95.3 | 90.6 | 86.5 | 91.0 |
| VLA-Thinker-SFT only | 95.9 | 96.7 | 93.4 | 94.0 | 95.0 |
| VLA-Thinker-GRPO only | 90.6 | 88.5 | 87.2 | 86.7 | 88.2 |
| VLA-Thinker (Full) | **98.7** | **99.0** | **95.2** | **96.9** | **97.5** |

结论：
- SFT 激活推理格式和工具调用模式，但未充分优化最终任务成功率
- GRPO-only 缺乏结构化推理先验导致严重退化（88.2%）
- 两阶段互补：SFT 提供归纳偏置，GRPO 进行轨迹级因果对齐

### 训练曲线分析（Fig. 3）
- 任务成功奖励从 0.82 稳步提升至 0.96
- 推理长度逐渐减少：模型学会了选择性调用工具，避免冗余推理

### 推理速度
VLA-Thinker 比 OpenVLA-OFT 平均慢 19%（因自回归推理过程），但性能增益显著（+7.1% ~ +10.4%）。


## Limitations

1. **单一视觉工具**：仅使用 ZOOM-IN（裁剪），未探索目标定位、分割或网页搜索等更丰富的感知工具
2. **MLLM 幻觉继承**：基于预训练多模态大语言模型，不可避免地继承其在视觉/空间推理中的幻觉问题
3. **仅仿真验证**：所有实验均在仿真基准（LIBERO、RoboTwin 2.0）上进行，未在真实机器人上验证
4. **Sim-to-Real gap**：未讨论从仿真到真实迁移的挑战和策略


## Key Takeaways

### 对 DLO 操控的启示
- thinking-with-image 范式天然适合需要精细视觉反馈的 DLO 操控任务（如线缆穿过孔洞时需要反复放大观察接触状态）
- ZOOM-IN 工具可扩展为 DLO 专用的视觉工具（如形状跟踪、接触点检测、张力估计）
- 长时序任务优势明显，适用于 DLO 多步骤操控（抓取→对齐→穿过→固定）

### 对 VLM-based 控制的启示
- 两阶段训练（SFT 冷启动 + GRPO 轨迹级 RL）是稳定训练 VLA 推理能力的有效模式
- GRPO 的组内相对优势消除了显式价值函数需求，降低了在稀疏奖励下优化长时序轨迹的方差
- 将感知建模为可调用动作而非静态输入，是提升 VLM 在复杂操控场景中鲁棒性的关键设计选择
- RL 阶段推理长度下降表明模型学会了"何时不需要推理"，这对实际部署的计算效率很重要

### 技术亮点
- 用 Qwen3-VL 自动合成 CoT 数据的策略解决了具身推理数据稀缺问题
- 夹爪状态变化检测作为子任务边界划分的启发式方法简单有效
- 混合注意力掩码（CoT 自回归 + 动作双向）是训练效率的巧妙设计

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

- [[wang-chaoyang|Wang, Chaoyang]]
