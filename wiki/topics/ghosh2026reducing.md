---
title: "Reducing Oracle Feedback with Vision-Language Embeddings for Preference-Based RL"
tags: [manipulation, VLM, RL]
created: "2026-05-07"
updated: "2026-05-07"
type: "literature"
status: "done"
summary: "ROVED 框架通过 VLE 生成偏好标签、不确定性过滤选择性地查询 oracle，并在训练中参数高效微调 VLE，在 Meta-World 操控任务上减少 50-80% oracle 查询量且支持跨任务迁移累计节省 75-90% 标注。"
authors: "Ghosh, Udita; Raychaudhuri, Dripta S.; Li, Jiachen; Karydis, Konstantinos; Roy-Chowdhury, Amit"
year: "2026"
venue: "arXiv Preprint"
zotero_key: "I2KI63UV"
---
## 摘要

Preference-based reinforcement learning（强化学习） can learn effective reward（奖励） functions from comparisons, but its scalability is constrained by the high cost of oracle feedback. Lightweight vision-language embedding (VLE) models provide a cheaper alternative, but their noisy outputs limit their effectiveness as standalone reward（奖励） generators. To address this challenge, we propose ROVED, a hybrid framework that combines VLE-based supervision with targeted oracle feedback. Our method uses the VLE to generate segment-level preferences and defers to an oracle only for samples with high uncertainty, identified through a filtering mechanism. In addition, we introduce a parameter-efficient fine-tuning method that adapts the VLE with the obtained oracle feedback in order to improve the model over time in a synergistic fashion. This ensures the retention of the scalability of embeddings and the accuracy of oracles, while avoiding their inefficiencies. Across multiple robotic manipulation（机器人操控） tasks, ROVED matches or surpasses prior preference-based methods while reducing oracle queries by up to 80%. Remarkably, the adapted VLE generalizes across tasks, yielding cumulative annotation savings of up to 90%, highlighting the practicality of combining scalable embeddings with precise oracle supervision for preference-based RL.

## 中文简述

提出基于强化学习的操控方法，具有泛化能力特点。

**研究方向**: 机器人操控、视觉-语言模型、强化学习

## 关键贡献

1. 提出 ROVED 框架，首次将 VLE 作为补充性噪声标签源与选择性 oracle 反馈结合，实现高效 PbRL。
2. 设计两个关键技术：(i) 参数高效 VLE 自适应方案，结合动力学感知自监督目标和稀疏 oracle 偏好反馈微调 VLE；(ii) 基于不确定性的样本选择策略，仅对高不确定性样本查询 oracle。
3. 实验证明：在 Meta-World 操控任务上达到 oracle-only 方法性能，同时减少 50-80% 标注成本；通过跨任务迁移实现 75-90% 累计标注节省。
## 结构化提取

- Problem: PbRL 中 oracle 反馈成本高，纯 VLE 偏好噪声大，需要兼顾可扩展性与精度的混合方法
- Method: ROVED = VLE 偏好生成 + 参数高效 VLE 微调（偏好损失 + 逆动力学损失）+ 不确定性感知三分过滤（clean/noisy/uncertain）+ 选择性 oracle 查询
- Tasks: 8 个 Meta-World 刚体操控任务（door-open/close, drawer-open/close, window-open/close, button-press, sweep-into）
- Sensors: state-based 观测（策略训练），图像观测（VLE 偏好计算）
- Robot Setup: Meta-World Sawyer 机械臂（仿真）
- Metrics: 成功率（success rate），oracle 查询数量，标注节省百分比
- Limitations: 仅仿真无真机，状态观测非图像观测策略，迁移限于同类任务，仍需初始 oracle 标注
- Evidence Notes:

  - Fig. 3: 8 任务学习曲线，ROVED 在减少 50-80% 查询下匹配 PEBBLE
  - Fig. 4: 跨任务迁移实验，累计节省 75-90%
  - Fig. 5: VLM oracle 实验，ROVED 减少 50% VLM 查询
  - Fig. 8: 4 组消融实验，各组件均有贡献
  - 表格型具体数字未在论文中明确给出（仅学习曲线图），成功率需从图中读取
## 本地引用关系

- [[ghosh2026reducing]]
## 证据元数据

- Fulltext Quality: fulltext（arXiv HTML 全文获取）
- Evidence Coverage: 完整覆盖（摘要、方法、实验、消融、结论均基于全文）
- Confidence: high
- Summary: ROVED 框架通过 VLE 生成偏好标签、不确定性过滤选择性地查询 oracle，并在训练中参数高效微调 VLE，在 Meta-World 操控任务上减少 50-80% oracle 查询量且支持跨任务迁移累计节省 75-90% 标注。


## Problem

Preference-based RL (PbRL) 能从偏好比较中学习奖励函数，但依赖大量昂贵的 oracle 反馈（人工或 VLM），限制了可扩展性。轻量级 VLE 模型虽可低成本生成偏好，但噪声大、精度不足，无法独立作为可靠奖励来源。核心矛盾：如何同时保留 VLE 的可扩展性和 oracle 的准确性？


## Method

### 整体架构

ROVED 基于 PEBBLE + SAC 框架，核心创新在于三阶段循环：

1. **VLE 偏好生成**（Sec. IV-A）：冻结预训练 VLE（LIV 或 DecisionNCE），对轨迹段对 (σ₀, σ₁) 计算基于图像-文本余弦相似度的片段回报 Rᵢ = Σ r_t^vle，按回报大小分配偏好标签 ỹ。

2. **VLE 自适应**（Sec. IV-B）：在冻结 VLE 之上添加两层可训练 MLP（G_L 和 G_I），通过两个目标微调：
   - **偏好损失**：用少量 oracle 偏好样本微调 G_L、G_I，使其更对齐任务偏好
   - **逆动力学损失**（自监督）：训练适配后的图像嵌入预测动作 transition ‖f(G_I∘F_I(o_t), G_I∘F_I(o_{t+1})) - a_t‖²，使嵌入捕获环境动力学

3. **噪声缓解与选择性 oracle 反馈**（Sec. IV-C）：基于 KL 散度三分策略：
   - D_KL(ỹ‖P_θ) < τ_lower → 标记为 clean，直接用于训练（数据集 D_τl）
   - D_KL(ỹ‖P_θ) > τ_upper → 标记为 noisy，翻转标签后训练（数据集 D_τu）
   - τ_lower ≤ D_KL ≤ τ_upper → 标记为 uncertain，按 oracle 预算采样送 oracle 标注（数据集 D_o）
   - τ_lower = τ_base + τ_unc，其中 τ_base = -ln(ρ) + αρ 动态计算，τ_unc = β_t · s_KL 随训练衰减

### 关键技术细节

- **VLE 选择**：默认使用 LIV，也支持 DecisionNCE
- **训练循环**：6K 步预探索后开始训练，每 3K 步采样 128 偏好对，oracle 预算为 0.25N（32 对）
- **奖励模型**：3 个 MLP 集成，3 层隐藏层 256 单元，Leaky ReLU + tanh 输出
- **自适应层**：2 层 MLP（256, 64, ReLU），逆动力学头 128-64-4 MLP


## Experiments

### 数据集与环境
- **基准**：Meta-World 8 个操控任务（door-open, door-close, drawer-open, drawer-close, window-open, window-close, button-press, sweep-into）
- **观测**：state-based（状态观测），VLE 使用图像观测计算偏好
- **骨干算法**：SAC + PEBBLE
- **VLE**：LIV（默认）、DecisionNCE

### 主要结果

**反馈效率**（Fig. 3）：
- ROVED 使用 x oracle 查询 ≈ PEBBLE 使用 z 查询（z >> x）的性能
- 简单任务减少 50% 查询，困难任务（button-press, sweep-into, drawer-open）减少 63.5%-80%
- 独立 VLE（LIV/DecisionNCE）因噪声大无法有效完成任务
- ROVED 在同等 oracle 预算下优于 SURF 和 MRN

**跨任务迁移**（Fig. 4）：
- 同任务不同物体（door-open → drawer-open）：减少 75-90% 查询
- 同物体不同任务（window-close → window-open）：减少 75-90% 查询
- 迁移方式：用源任务微调后的 VLE 权重初始化目标任务 VLE

**VLM oracle 实验**（Fig. 5）：
- 使用 Gemini-Pro-1.5 作为 oracle，ROVED 减少 50% 查询量且不降低性能
- VLE 生成偏好速度 < 0.009s/query vs VLM ~5s/query，快三个数量级

### 消融实验

1. **VLE 自适应影响**（Fig. 6, 8）：移除后成功率先升后降，因 VLE 无法随策略进化适应分布漂移
2. **逆动力学损失**（Fig. 8）：移除后性能后期退化，因缺乏动力学理解导致分布漂移时泛化失败
3. **选择性反馈**（Fig. 8）：随机采样替代不确定性选择，性能下降但仍优于 PEBBLE 同等预算
4. **VLE 骨干鲁棒性**（Fig. 7）：LIV 和 DecisionNCE 均可工作，DecisionNCE 略优于 LIV


## Limitations

1. **仅仿真验证**：所有实验均在 Meta-World 仿真环境中进行，未涉及真实机器人
2. **状态观测为主**：策略训练使用 state-based 观测，VLE 仅用于偏好生成，未在 image-based RL 设置中验证
3. **迁移范围有限**：跨任务迁移仅在同类任务（同物体或同任务类型）间验证，未测试跨物体类别或跨领域的迁移
4. **仍需 oracle**：未完全消除人工标注需求，初始阶段仍需 250 oracle 样本
5. **未讨论 DLO 操控**：仅涉及刚体操控，未涉及可变形物体或长时序复杂任务
6. **未报告计算开销**：VLE 微调和三分过滤的额外计算成本未量化


## Key Takeaways

1. **VLE + 选择性 oracle 的混合策略是降低 PbRL 标注成本的有效途径**：纯 VLE 太噪声，纯 oracle 太昂贵，混合方案兼顾两者优势。这与 DLO 操控中的奖励设计困境类似——复杂任务难以手工设计奖励，可考虑类似混合策略。
2. **逆动力学自监督目标是关键**：使 VLE 嵌入捕获环境动力学，而非仅依赖偏好监督。这一思路可迁移到 DLO 操控的 VLM 奖励设计——让嵌入理解形变动力学。
3. **不确定性感知的标注选择具有通用价值**：KL 散度三分策略可应用于任何需要降低标注成本的场景，包括 DLO 任务中的人工偏好收集。
4. **跨任务迁移的 VLE 微调**：VLE 在一个任务上微调后可迁移到相关任务，这对多任务机器人操控系统有实际意义。

## 相关概念

- [[robotic-manipulation]]
- [[vision-language-model]]
- [[reinforcement-learning]]
- [[deformable-linear-object]]

## 相关研究者

- [[ghosh|Ghosh, Udita]]
- [[raychaudhuri|Raychaudhuri, Dripta S.]]
- [[li-jiachen|Li, Jiachen]]
- [[karydis|Karydis, Konstantinos]]
- [[roy-chowdhury|Roy-Chowdhury, Amit]]
