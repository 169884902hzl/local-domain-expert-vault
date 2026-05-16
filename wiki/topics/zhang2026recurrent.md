---
title: "Recurrent reasoning with vision-language models for estimating long-horizon embodied task progress"
tags: [imitation, VLM, RL, robot-learning]
created: "2026-05-06"
updated: "2026-05-06"
type: "literature"
status: "done"
summary: "提出 R²VLM，通过循环推理框架让 VLM 对局部视频片段迭代更新 Chain-of-Thought 来估计长时序具身任务进度，在 ALFRED 和 Ego4D 上达到 SOTA，并验证了策略学习增强、RL 奖励建模和主动辅助三种下游应用。"
authors: "Zhang, Yuelin; Cheng, Sijie; Li, Chen; Li, Zongzhao; Huang, Yuxin et al."
year: "2026"
venue: "arXiv Preprint"
zotero_key: "ZNX2PQI6"
---
## 摘要

Accurately estimating task progress is critical for embodied agents to plan and execute long-horizon（长时序）, multi-step tasks. Despite promising advances, existing Vision-Language Models (VLMs) based methods primarily leverage their video understanding capabilities, while neglecting their complex reasoning potential. Furthermore, processing long video trajectories with VLMs is computationally prohibitive for real-world deployment. To address these challenges, we propose the Recurrent Reasoning Vision-Language Model（视觉-语言模型） ($\text{R}^2$VLM). Our model features a recurrent reasoning framework that processes local video snippets iteratively, maintaining a global context through an evolving Chain of Thought (CoT). This CoT explicitly records task decomposition, key steps, and their completion status, enabling the model to reason about complex temporal dependencies. This design avoids the high cost of processing long videos while preserving essential reasoning capabilities. We train $\text{R}^2$VLM on large-scale, automatically generated datasets from ALFRED and Ego4D. Extensive experiments on progress estimation and downstream applications, including progress-enhanced policy learning, reward（奖励） modeling for reinforcement learning（强化学习）, and proactive assistance, demonstrate that $\text{R}^2$VLM achieves strong performance and generalization, achieving a new state-of-the-art（现有最优方法） in long-horizon（长时序） task progress estimation. The models and benchmarks are publicly available at \href{https://huggingface.co/collections/zhangyuelin/r2vlm}{huggingface}.

## 中文简述

提出基于强化学习的操控方法，具有泛化能力特点。

**研究方向**: 模仿学习、视觉-语言模型、强化学习、机器人学习

## 关键贡献

1. **循环推理框架**：提出 R²VLM，对局部视频片段进行迭代推理，通过不断演进的 Chain-of-Thought（CoT）维护全局上下文，避免处理完整长视频的计算开销
2. **结构化 CoT 设计**：CoT 显式记录任务分解、关键步骤及其完成状态，使模型能推理复杂的时间依赖关系
3. **自动化数据构建管线**：从 ALFRED 和 Ego4D 自动生成大规模多轮增量视频交互数据集，包含 CoT 标注和干扰任务描述
4. **多奖励 RL 训练**：设计 Format、Bin、MAE、Improvement、Finish 五种奖励函数的两阶段训练策略（SFT → PPO），专为多轮循环推理优化
5. **多下游应用验证**：验证了进度增强的策略学习、RL 奖励建模、步级主动辅助三种下游应用的有效性
## 结构化提取

- **Problem**: 长时序具身任务的实时进度估计——需要同时处理复杂时间依赖和长视频的计算效率
- **Method**: R²VLM（Recurrent Reasoning VLM），基于 Qwen2.5-VL-7B，循环推理框架 + 演进式 CoT + SFT/PPO 两阶段训练
- **Tasks**: 长时序任务进度估计、进度增强策略学习、RL 奖励建模、步级主动辅助
- **Sensors**: 自中心（egocentric）视频（ALFRED: 1fps 4帧/片段, Ego4D: 2fps 4帧/片段）
- **Robot Setup**: AI2-THOR 2.0 仿真环境（ALFRED）+ 真实世界第一人称视频（Ego4D）；策略学习下游使用 Seq2Seq 模型和 SPRINT（IQL）
- **Metrics**: p_mae（进度 MAE）、Δp_mae（增量 MAE）、bin（步级区间准确率）、acc（任务完成准确率）
- **Limitations**: 真实世界噪声和执行路径多样性导致性能下降；需要 SFT 冷启动才能做 RL；Ego4D 自动标注质量有限
- **Evidence Notes**: 主实验 4 指标全 SOTA；消融证实循环推理 + 多奖励设计各组件有效性；下游任务中基于步骤的进度优于时间基进度；密集奖励在 RL 中优于稀疏奖励
## 本地引用关系

-
## 证据元数据

- Fulltext Quality: fulltext
- Evidence Coverage: high（方法、实验、消融、下游应用均有详细数据）
- Confidence: high
- Summary: 提出 R²VLM，通过循环推理框架让 VLM 对局部视频片段迭代更新 Chain-of-Thought 来估计长时序具身任务进度，在 ALFRED 和 Ego4D 上达到 SOTA，并验证了策略学习增强、RL 奖励建模和主动辅助三种下游应用。


## Problem

具身智能体在执行长时序（long-horizon）、多步骤任务时，需要准确估计当前任务进度以支持规划和决策。现有基于 VLM 的方法（GVL、ROVER）主要利用 VLM 的视频理解能力，但忽略了其推理潜力；同时，让 VLM 处理完整长视频轨迹在计算上代价过高，无法实际部署。


## Method

### 核心架构

R²VLM 基于 Qwen2.5-VL-7B-Instruct 构建，核心是循环推理框架：

- **输入**：任务描述 τ + 当前视频片段 v_t（从流式视频中均匀采样 4 帧）+ 历史链式思考 c_{t-1}
- **输出**：更新后的链式思考 c_t + 进度估计 p_t ∈ [0, 100]
- **推理形式**：c_t, p_t = f_θ(τ, v_t, c_{t-1})

### Chain-of-Thought 结构

CoT 包含三个顺序元素：
1. 长时序任务的分解（子任务列表）
2. 已观察/未观察到的关键步骤分析
3. 基于完成步骤比例的进度估计

初始迭代时，利用 VLM 的常识知识生成初始 CoT；后续迭代中动态调整任务分解（合并、拆分或重排步骤），并基于新视频片段更新完成状态。

### 数据构建

- **视频片段**：ALFRED 以 4 秒间隔（1 fps）、Ego4D 以 2 秒间隔（2 fps）切分，每段采样 4 帧
- **进度定义**：基于完成步骤的比例，假设单步骤内线性变化（公式 4）
- **干扰任务**：约束生成策略使干扰任务匹配前 n_r 步但偏离后续步骤，提高模型鲁棒性
- **CoT 生成**：利用大模型（Qwen2.5-VL-72B）将数据集中的先验知识整合为结构化 CoT

### 训练策略

两阶段训练：
1. **SFT**：学习推理模式（任务分解、步骤推理、进度估计）
2. **RL（PPO）**：从 SFT 的早 checkpoint 开始，使用五种奖励：
   - Format Reward：输出格式正确性
   - Bin Reward：进度是否落在正确的步骤区间
   - MAE Reward：连续精度奖励 R_mae = max(1 - |p_t - p_t^gt|/δ_1, 0)
   - Improvement Reward：鼓励当前轮次误差小于前一轮（最关键的奖励）
   - Finish Reward：任务完成判断准确性
   - 总奖励：R_overall = R_fmt · (R_bin · R_mae + αR_imp + βR_fin)

选择 PPO 而非 GRPO，因为 GRPO 需要相同输入生成多个候选，与多轮设定（每轮 c_{t-1} 不同）不兼容。

### 数据集规模

- ALFRED：11,499 条轨迹，124,821 个对话元组
- Ego4D：13,965 条轨迹，127,694 个对话元组
- 基准测试经人工审核，ALFRED 保留率 93%（669/722），Ego4D 保留率 74%（529/718）


## Experiments

### 主实验（Table 1）

在 ALFRED 和 Ego4D 两个基准上，对比了 GPT-5、Gemini 2.5 Pro、Qwen2.5-VL-72B、InternVL3-78B、MiniCPM-V-2.6 等模型。

四个评估指标：
- **p_mae**：进度 MAE（越低越好）
- **Δp_mae**：进度增量 MAE（奖励建模能力）
- **bin**：进度是否在正确区间（步级判断能力）
- **acc**：任务完成判断准确率

R²VLM 关键结果：
- **ALFRED**：p_mae = 2.19, Δp_mae = 1.37, bin = 0.951, acc = 0.988
- **Ego4D**：p_mae = 9.56, Δp_mae = 4.02, bin = 0.708, acc = 0.775
- Qwen2.5-VL-7B baseline 在 ALFRED 上 p_mae = 27.87，72B 版本为 24.88
- R²VLM 在两个数据集四个指标上均达到 SOTA

三种模型变体对比：
- R²VLM-Zero（直接 RL）：失败，无法发展有效推理模式
- R²VLM-SFT：已有不错性能（ALFRED acc = 0.961）
- R²VLM（SFT + RL）：进一步提升（ALFRED acc = 0.988）

### 消融实验

**视频片段 vs 完整视频（Fig. 4）**：
- 随视频时长增加，完整视频输入精度下降（注意力分散和幻觉）
- 片段输入精度保持稳定
- 片段输入推理时间为常数；完整视频输入推理时间随视频长度线性增长

**奖励设计（Table 2）**：
- 移除 MAE 奖励：bin 略升但 p_mae 和 acc 显著下降
- 移除 Improvement 奖励：p_mae 从 2.19 升至 2.42（+10.5%），acc 从 0.988 降至 0.978
- 移除 Bin 奖励：性能全面下降
- 三者组合最优

### 下游应用

**1. 进度增强的策略学习（Table 3）**：
- 使用 Seq2Seq + 进度监控框架
- R²VLM 估计的进度（基于步骤完成比例）优于时间基进度
- ALFRED valid_seen 目标条件成功率提升 2.2%，valid_unseen 提升 0.4%

**2. RL 奖励建模（Table 4）**：
- 基于 SPRINT 模型进行在线 RL（IQL）
- R²VLM 提供密集奖励信号，在 2-5 步任务上均一致提升性能
- 稀疏奖励或 Qwen2.5-VL 奖励常常降低性能

**3. 步级主动辅助（Fig. 6）**：
- 持续接收流式视频，2 秒片段周期性推理
- 轻量 LLM（Qwen2.5-7B）从更新 CoT 提取结构化步骤状态
- 能准确检测关键转换并实时更新步骤状态


## Limitations

1. **真实世界性能下降**：Ego4D 上表现显著低于 ALFRED，主要因为：(i) 真实环境更复杂、噪声更多；(ii) 不同执行者完成同一任务的路径差异大
2. **RL-Zero 失败**：直接对基座模型做 RL 无法发展有效推理模式，需要 SFT 冷启动
3. **基准数据生成质量**：Ego4D 自动标注保留率仅 74%，反映大模型在复杂真实场景中数据生成的局限性
4. **泛化能力边界**：论文未展示跨域（mixed training → cross-domain testing）的详细结果（仅提到在附录中）
5. **实时性**：虽然片段输入优于完整视频，但具体推理延迟未量化


## Key Takeaways

1. **循环 CoT 是处理长时序任务的关键设计**：通过历史 CoT 作为记忆载体，避免了 VLM 处理完整长视频的计算瓶颈，同时保持全局上下文——这一思路可迁移到 DLO 操控中的长时序规划
2. **VLM 的推理能力需要显式激发**：零样本 VLM 的进度估计能力很差（p_mae > 24），需要 SFT + RL 两阶段训练才能激发推理潜力
3. **Improvement Reward 最关键**：鼓励模型在多轮推理中持续改进，对 DLO 操控中的渐进式执行监控有启发
4. **基于步骤完成比例的进度定义优于时间基进度**：在策略学习下游任务中得到验证，对 DLO 任务中的分阶段操控（如先定位再夹取再绕线）有直接参考价值
5. **VLM 作为密集奖励信号源**：R²VLM 提供的进度增量可直接作为 RL 奖励，在 2-5 步操控任务上均有效，为双臂 DLO 操控的 RL 训练提供了可行的奖励设计路径

## 相关概念

- [[imitation-learning]]
- [[vision-language-model]]
- [[reinforcement-learning]]
- [[robot-learning]]
- [[deformable-linear-object]]
- [[bimanual-manipulation]]

## 相关研究者

- [[zhang-yuelin|Zhang, Yuelin]]
- [[cheng-sijie|Cheng, Sijie]]
