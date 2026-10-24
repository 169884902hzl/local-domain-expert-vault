---
title: "FASTER: Value-guided sampling for fast RL"
tags: [manipulation, RL, diffusion, test-time-scaling]
created: "2026-05-06"
updated: "2026-05-06"
type: "literature"
status: "done"
summary: "将扩散策略的 best-of-N 采样建模为去噪 MDP，学习噪声级 critic 在初始噪声阶段筛选候选动作，以单次去噪成本恢复 best-of-N 的性能收益，在操控任务和 VLA 微调中实现 4.5-8 倍计算加速"
authors: "Dong, Perry; Swerdlow, Alexander; Sadigh, Dorsa; Finn, Chelsea"
year: "2026"
venue: "arXiv Preprint"
zotero_key: "U82JMRTK"
---
## 摘要

Some of the most performant reinforcement learning（强化学习） algorithms today can be prohibitively expensive as they use test-time scaling methods such as sampling multiple action candidates and selecting the best one. In this work, we propose FASTER, a method for getting the benefits of sampling-based test-time scaling of diffusion（扩散）-based policies without the computational cost by tracing the performance gain of action samples back to earlier in the denoising process. Our key insight is that we can model the denoising of multiple action candidates and selecting the best one as a Markov Decision Process (MDP) where the goal is to progressively filter action candidates before denoising is complete. With this MDP, we can learn a policy and value function in the denoising space that predicts the downstream value of action candidates in the denoising process and filters them while maximizing returns. The result is a method that is lightweight and can be plugged into existing generative RL algorithms. Across challenging long-horizon（长时序） manipulation（操控） tasks in online and batch-online RL, FASTER consistently improves the underlying policies and achieves the best overall performance among the compared methods. Applied to a pretrained VLA, FASTER achieves the same performance while substantially reducing training and inference compute requirements. Code is available at https://github.com/alexanderswerdlow/faster .

## 中文简述

将扩散策略的 best-of-N 采样建模为去噪 MDP，通过噪声级 critic 在去噪前筛选最优候选，实现 4.5-8 倍计算加速。

**研究方向**: 机器人操控、强化学习、扩散策略、test-time scaling

## 关键贡献

1. **去噪过滤 MDP 框架**：将多候选去噪 + 最优选择建模为 Markov Decision Process，状态包含环境状态、去噪步、候选集和部分去噪结果，动作是保留/丢弃决策，奖励由动作级 critic 提供。
2. **噪声级 critic（Q_dn）**：学习在初始噪声阶段预测候选的下游回报，将过滤决策从完整去噪链提前到最廉价的噪声评估。训练目标简化为对动作级 critic 的一步回归：L_reg = ||Q_dn(s, ε*) - sg[Q_a(s, a*)]||²。
3. **计算效率**：将推理时 actor 前向传播从 O(TN) 降至 O(T)，仅用 N 次轻量 critic 评估替代 N-1 次完整去噪。在 VLA 场景下（critic 20M vs actor 3.3B），噪声评估开销可忽略。
4. **模块化设计**：可作为插件应用于任意依赖 best-of-N 采样的扩散/流策略 RL 算法，验证了 EXPO（FASTER-EXPO）和 IDQL（FASTER-IDQL）两种变体。
## 结构化提取

- **Problem**: 扩散策略 RL 中 best-of-N 采样的计算开销随候选数线性增长，对大模型不可接受
- **Method**: 将去噪过滤建模为 MDP，学习噪声级 critic Q_dn(s, ε) 在初始噪声阶段筛选最优候选，仅执行单次完整去噪
- **Tasks**: 7-DoF 机械臂操控（Lift/Can/Square/Tool Hang/LIBERO-90 共 9 个任务）
- **Sensors**: 论文未详细说明传感器配置；Robomimic 使用本体感觉+图像观测，LIBERO 使用图像+语言指令
- **Robot Setup**: 模拟环境中的 7-DoF 机械臂（Robomimic: Franka/Panda；LIBERO: Franka）
- **Metrics**: 成功率（sparse binary reward），计算 FLOPs，推理延迟（ms），update step 时间（s）
- **Limitations**: 不改进样本效率；仅适用于有噪声种子的扩散/流策略；仅评测稀疏奖励操控任务；未在 DLO 或其他非刚体操控场景验证
- **Evidence Notes**: 全文证据完整。关键数据点：(1) FASTER-EXPO 在线 RL 下整体最优（Figure 3）；(2) VLA 场景 4.5× update 加速、8× inference FLOPs 减少（Figure 6）；(3) 噪声级过滤等价于多步过滤（Figure 9-10）；(4) 蒸馏 baseline 远差于 FASTER（Figure 11）。附录提供了蒸馏消融、超参数细节和计算分析。
## 本地引用关系

-
## 证据元数据

- Fulltext Quality: fulltext
- Evidence Coverage: 完整覆盖所有章节，包括方法、实验、消融、附录
- Confidence: high
- Summary: 将扩散策略的 best-of-N 采样建模为去噪 MDP，学习噪声级 critic 在初始噪声阶段筛选候选动作，以单次去噪成本恢复 best-of-N 的性能收益，在操控任务和 VLA 微调中实现 4.5-8 倍计算加速


## Problem

当前最有效的扩散策略 RL 方法（如 EXPO、IDQL）依赖 test-time scaling：采样 N 个动作候选并全量去噪后选择最优。这导致推理和训练的计算开销随 N 线性增长，尤其对大模型（如 3.3B 参数 VLA）不可接受。核心困难在于：噪声样本与最终动作结果之间没有直接监督信号，映射仅通过去噪过程隐式定义，因此无法在去噪完成前判断哪些候选值得执行。


## Method

### 核心思路
FASTER 的关键洞察是：best-of-N 采样的性能增益主要来源于初始噪声的方差，而非去噪过程本身。因此可以在去噪开始前（t=T）就评估哪些噪声种子会产出高价值动作。

### 去噪过滤 MDP（Section 4.1）
- **状态** s_t = (s, t, C_t, {a^(i)_t}_{i∈C_t})：环境状态 s、去噪步 t、存活候选集 C_t、部分去噪结果
- **动作** m_{t,i} ∈ {0,1}：保留或丢弃每个候选
- **转移**：对存活候选执行一步去噪
- **奖励**：非终止步为 0；终止时 r = Q_a(s, a*)

### 学习（Section 4.2）
使用 TD 学习训练去噪 critic Q_dn(s_t, m_t)。在实际实现中简化为单步决策（Section 4.3）：
1. 采样 N 个噪声候选 {ε_i}
2. 选择 i* = argmax_i Q_dn(s, ε_i)
3. 仅对 ε_{i*} 执行完整去噪得到 a* = π_θ(s, ε_{i*})
4. 用 L_reg = ||Q_dn(s, ε_{i*}) - sg[Q_a(s, a*)]||² 训练 Q_dn

### 两种变体
- **FASTER-EXPO**：选择的最优噪声去噪后作为 EXPO 基策略的提案，下游 edit 步骤不变
- **FASTER-IDQL**：选择的最优噪声去噪后直接执行，无 edit 策略

### 计算分析（Section 4.4）
- Best-of-N 成本：C_BoN = T·N·F_actor + N·F_critic
- FASTER 成本：C_FASTER = N·F_critic + T·F_actor
- 当 T=N, F_actor=F_critic=F 时，约 T/2 倍加速
- VLA 场景（critic 20M vs actor 3.3B）：critic 评估开销可忽略，理论加速更高


## Experiments

### 环境
- **Robomimic**：Lift、Can、Square、Tool Hang（7-DoF 机械臂，稀疏奖励）
- **LIBERO**：pi0.5_libero 预训练后，在 libero_90 的 5 个 held-out 任务上微调（3.3B 参数 VLA）
- 总计 9 个操控任务

### Baselines
EXPO, IDQL, RLPD, QSM, DSRL, QAM, FQL（共 7 个对比方法）

### 主要结果

**在线 RL（Figure 3）**：
- FASTER-EXPO 在所有评估方法中整体表现最强
- 显著优于高样本效率方法 RLPD
- 基于 action gradient 的方法（QSM、QAM）表现较弱
- DSRL 在噪声潜空间引导策略，样本效率较差
- FQL 的行为正则化阻碍探索

**Batch-online RL（Figure 5）**：
- FASTER-EXPO 在迭代次数上与 EXPO 持平
- 在计算效率上优于 EXPO

**计算效率（Figure 3, 4, 6）**：
- FASTER 与各自 baseline 在成功率上处于误差范围内
- VLA 场景：update step 从 11.6s → 2.5s（4.5× 加速），inference 从 566ms → 335ms（1.7× 加速），inference FLOPs 减少 8 倍
- Robomimic 场景：inference FLOPs 约 8 倍减少

**VLA 微调（Section 5.3, Figure 7）**：
- FASTER-EXPO 在 5 个 libero_90 任务上多数与 EXPO 持平
- 用 3.3B 参数 pi0.5_libero checkpoint，在线 RL 微调，无离线数据
- 20M 参数 critic vs 3.3B 参数 actor

### 消融实验

1. **Critic 大小（Figure 8）**：0.25× 到 1.0× Q_a 的参数量，性能基本一致 → Q_dn 可远小于 Q_a
2. **过滤步骤（Figure 9）**：不同去噪步骤过滤，性能一致 → 初始噪声过滤即有效
3. **完整 MDP vs 单步（Figure 10）**：学习自适应过滤策略与固定初始噪声过滤性能相当
4. **蒸馏 baseline（Figure 11）**：将 value-maximizing 分布蒸馏到单策略表现远差于 FASTER → 蒸馏训练不稳定


## Limitations

1. **不改进样本效率**：FASTER 专注于计算效率，FASTER-EXPO 的样本效率优势主要来自 EXPO 本身
2. **依赖初始噪声种子结构**：仅适用于使用噪声种子的策略类别（扩散/流策略），无法直接扩展到无此结构的策略
3. **仅评测操控任务**：未在非操控场景验证（如导航、DLO 操控等）
4. **稀疏奖励设定**：所有任务使用稀疏二值奖励，密集奖励下的表现未验证
5. **未与非扩散方法直接对比计算效率**（作者解释：扩散策略是机器人领域主导策略类，且表达能力更强）


## Key Takeaways

### 与 DLO 操控的关联
- 本论文**不直接涉及 DLO 操控**，但方法通用性强，可应用于任何使用扩散策略的 RL 场景
- 若 DLO 操控采用扩散策略 + best-of-N 推理，FASTER 可直接降低推理延迟
- 噪声级 critic 的思路值得借鉴：在长时序 DLO 任务中，推理延迟是实际部署的关键瓶颈

### 与 VLM-based 控制的关联
- FASTER 已验证可在 VLA（π0.5）上有效工作
- 对大规模 VLM/VLA 的 RL 微调尤其有价值：critic 远小于 actor 时收益最大
- 可作为 VLA 在线微调的通用加速组件

### 方法论启示
- 初始噪声对扩散模型输出质量的决定性作用（与图像生成领域的发现一致）
- 将采样选择问题建模为 MDP 是一个优雅的框架化思路
- 单步噪声过滤等价于多步去噪过滤，说明去噪链早期信号已足够

## 相关概念

- [[robotic-manipulation]]
- [[reinforcement-learning]]
- [[diffusion-model]]
- [[test-time-scaling]]
- [[vision-language-model]]
- [[deformable-linear-object]]

## 相关研究者

- [[dong-perry|Dong, Perry]]
- [[sadigh|Sadigh, Dorsa]]
- [[finn|Finn, Chelsea]]
