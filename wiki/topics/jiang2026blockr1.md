---
title: "Block-R1: Rethinking the role of block size in multi-domain reinforcement learning for diffusion large language models"
tags: [VLM, RL, diffusion]
created: "2026-05-13"
updated: "2026-05-13"
type: "literature"
status: "done"
summary: "揭示扩散语言模型多域 RL 后训练中 block size 域冲突问题，通过 teacher-student 管线为每个训练样本分配最优 block size，构建 41K 数据集和跨域 benchmark，在 13 个数据集上大幅超越固定 block size 基线"
authors: "Jiang, Yan; Qiu, Ruihong; Huang, Zi"
year: "2026"
venue: "arXiv Preprint"
zotero_key: "4M2SRRK9"
---
## 摘要

Recently, reinforcement learning（强化学习） (RL) has been widely applied during post-training for diffusion（扩散） large language models (dLLMs) to enhance reasoning with block-wise semi-autoregressive generation. Block size has therefore become a vital factor in dLLMs, since it determines the parallel decoding granularity and affects the rollout trajectories during RL optimisation, e.g., GRPO. Instead of investigating the effect of block size during inference on individual domains, this paper studies block size from a domain conflict perspective for dLLM RL post-training in multi-domain scenarios. The main contributions are: (1) a formulation of domain block size conflict in multi-domain RL for dLLMs, which will largely affect the post-training effectiveness for rollout-based RL methods; (2) a novel dataset, Block-R1-41K is constructed with a best-improved training block size for each sample, which also induces a Block Size Conflict Score to quantitatively measure the domain conflict; (3) a new benchmark, Block-R1, for flexible RL post-training for dLLMs in both single and cross domain; and (4) a simple yet powerful cross-domain post-training method with sample-level best-improved training block sizes. Extensive experiments on 13 distinct datasets, 7 latest RL algorithms, and various different dLLM backbones are covered in Block-R1. The benchmark is open-sourced at https://github.com/YanJiangJerry/Block-R1, with the dataset released at https://huggingface.co/datasets/dLLM-R1/Block-R1-41K.

## 中文简述

揭示扩散语言模型（dLLM）多域 RL 后训练中的 block size 域冲突问题，提出 sample-level best-improved block size 分配方法，构建 Block-R1-41K 数据集和 benchmark，在 13 个数据集上全面超越固定 block size 基线。

**研究方向**: 扩散语言模型、强化学习后训练、多域推理

## 关键贡献

1. **域 block size 冲突的形式化定义**（Definition 3, Theorem 3）：证明在域间偏好分歧条件下，固定 block size 存在不可消除的结构性次优性
2. **Block-R1-41K 数据集**：通过 teacher-student 评估管线为每个训练样本分配 best-improved training block size，诱导出 Block Size Conflict Score（BCS）度量域冲突
3. **Block-R1 benchmark**：覆盖 13 个数据集、7 种 RL 算法、10 个 dLLM backbone 的跨域 RL 后训练 benchmark
4. **Sample-level block-conditioned training**：简单有效的跨域训练方法，在 rollout 生成时使用样本级 block size 标注，无需修改现有 RL 目标函数
## 结构化提取

- Problem: 扩散语言模型多域 RL 后训练中，不同域对 block size 的偏好不同，固定 block size 导致域间冲突，使多域联合训练性能下降
- Method: Teacher-student 评估管线为每个训练样本选择 best-improved block size；训练时使用样本级 block-conditioned policy；BCS 度量域间冲突
- Tasks: 数学推理（GSM8K, MATH500, Countdown）、代码生成（KodCode, HumanEval, MBPP）、逻辑谜题（Sudoku, KK）、通用能力（HellaSwag, MMLU, ARC-E）、高级推理（MMLU-Pro, ARC-C）
- Sensors: not_applicable（纯语言模型，无传感器）
- Robot Setup: not_applicable（纯语言模型，无机器人）
- Metrics: Zero-shot pass@1 accuracy（%），best checkpoint，13 个 benchmark 数据集
- Limitations: 仅限 block-based dLLMs；数据集构建需要 teacher-student 评估开销；依赖候选 block size 集合；评估受生成长度（256 token）限制
- Evidence Notes:

  - Table 1: 跨域泛化主结果，Block-R1 在所有 13 域上大幅超越 Vanilla 多域 RL
  - Table 3: 跨 6 个 dLLM backbone 验证泛化性
  - Table 5: 单域 RL 中 Block-R1 仍有效
  - Table 6: BCS 与多域 RL 性能下降强相关
  - Table 2: 推理时 Block-R1 + b1 接近 Oracle 上界
  - Theorem 3: 固定 block size 结构性次优的理论证明
  - Figure 5: 不同 block size 下 reward improvement 差异显著
  - Figure 6: 各域 best-improved block size 分布差异
## 本地引用关系

-
## 证据元数据

- Fulltext Quality: fulltext
- Evidence Coverage: 完整覆盖正文（Section 1-8）、附录 B-F、所有实验表格和定理证明
- Confidence: high
- Summary: 揭示扩散语言模型多域 RL 后训练中 block size 域冲突问题，通过 teacher-student 管线为每个训练样本分配最优 block size，构建 41K 数据集和跨域 benchmark，在 13 个数据集上大幅超越固定 block size 基线


## Problem

扩散语言模型（dLLMs）在 RL 后训练（post-training）中使用固定 block size 进行半自回归生成本。当进行多域联合 RL 训练时，不同推理域（数学推理、代码生成、逻辑谜题等）对 block size 有不同偏好——某些域偏好小块以实现细粒度中间验证，另一些域偏好大块以保持全局格式一致性。统一固定 block size 导致**域 block size 冲突（Domain Block Size Conflict）**：多域联合训练的性能甚至低于单域训练，有时低于无 RL 基线。


## Method

### 核心洞察
Block size 是 dLLM 并行解码粒度的关键参数。GRPO 等基于 rollout 的 RL 方法中，目标函数 J_GRPO(θ, c) 显式依赖于 block size c——改变 c 会改变轨迹分布、奖励分布和优势估计（Remark 1）。

### 数据集构建（5 阶段管线）
1. **Stage 1 - 跨域源选择**：从数学推理（GSM8K, MATH500, Countdown）、代码生成（KodCode）、逻辑谜题（Sudoku, KK）等 5 大领域选择有官方训练集的 benchmark
2. **Stage 2 - 跨域奖励设计**：三组件奖励：format-based（格式约束）、accuracy-based（域特定验证）、constraint-based（连续部分奖励）
3. **Stage 3 - Teacher-Student 过滤**：用强模型 LLaDA2.0-mini (16B) 作为 teacher，弱模型 LLaDA-8B-Base 作为 student，在所有候选 block size 上评估。过滤掉过易、过难和异常样本
4. **Stage 4 - Best-improved block size 选择**：对每个样本 x，选择使 teacher-student 改进差最大的 block size：c*_x = argmax_{c∈B} [A_θT(x,c) - A_θS(x,c)]
5. **Stage 5 - 平衡多域组装**：等量采样各域，最终得到 41K+ 样本，每个样本附带 best-improved block size 标注

### 训练方法
将全局固定 block-conditioned policy π_θ(c) 替换为样本特定 block-conditioned policy π_θ(c*_x)。每个训练样本在自己的最优 block size 下生成 rollout，实现 block-conditioned policy update。O(1) 的 block size 查找不增加训练复杂度。

### Block Size Conflict Score（BCS）
基于 Wasserstein 距离度量两个域的 best-improved block size 分布差异。BCS 越大，域冲突越严重，固定 block size 的多域训练性能下降越明显。


## Experiments

### 主要结果（Table 1, LLaDA-8B-Instruct + StableDRL）
| 方法 | Countdown | GSM8K | MATH500 | HumanEval | MBPP | KodCode | Sudoku | KK | HellaSwag | MMLU | ARC-E | MMLU-Pro | ARC-C |
|------|-----------|-------|---------|-----------|------|---------|--------|----|-----------|------|-------|----------|-------|
| LLaDA (No RL) | 16.80 | 76.19 | 32.00 | 28.66 | 33.60 | 22.00 | 7.81 | 30.00 | 56.21 | 53.46 | 76.98 | 33.79 | 73.21 |
| Vanilla (多域, 固定 bs=32) | 30.08 | 57.24 | 28.20 | 24.39 | 24.40 | 22.60 | 9.77 | 30.14 | 52.10 | 52.06 | 73.95 | 29.79 | 65.87 |
| **Block-R1** | **62.11** | **80.74** | **35.80** | **34.76** | **34.80** | **28.60** | **26.95** | **50.14** | **64.07** | **62.22** | **90.53** | **37.96** | **82.51** |

- Vanilla 多域 RL 在多数域上显著劣于单域 RL，甚至低于无 RL 基线（如 GSM8K: 57.24 vs 76.19）
- Block-R1 在所有 13 个域上全面超越 Vanilla，多个域上超越单域 RL 最佳结果

### 跨 backbone 泛化（Table 3）
在 6 个 dLLM backbone（LLaDA-8B, LLaDA-1.5, Dream-7B, SDAR-8B, TraDo-8B, LLaDA2.0-16B）上均有效，平均提升 5-20 个百分点。

### 单域 RL 有效性（Table 5）
Block-R1 在单域 RL 中同样有效，尤其在 Countdown、GSM8K 和 KK 上增益明显。

### BCS 与多域 RL 性能关系（Table 6）
- 大 BCS 域对（如 Countdown-KK: BCS=0.1969）：固定 block 混域训练导致严重性能下降（Countdown 从 58.98 降至 23.44）
- 小 BCS 域对（如 MATH500-KodCode: BCS=0.0103）：混域训练影响较小甚至有益

### 推理时动态 block size（Table 2）
Block-R1 + b1 在 GSM8K 上达到 83.70%，接近 Oracle 上界 84.31%，说明 block size 适配在推理时仍有价值。

### 关键消融/分析
- Figure 5：不同 block size 下的 reward improvement 差异巨大，KodCode 在 bs=64/128 时甚至出现负改进
- Figure 6：各域 best-improved block size 分布显著不同（Countdown 偏小, Sudoku 偏大）
- 定理证明（Appendix E）：在偏好分歧假设下，固定 block size 存在结构性次优


## Limitations

1. **仅限于 block-based dLLMs**：方法可能不直接泛化到非自回归或非 block-based 生成范式
2. **数据集构建开销**：teacher-student 评估需 O(2NSQTL²) 计算，N=样本数, S=候选 block size 数, Q=rollout 数, T=扩散步, L=生成长度
3. **依赖候选 block size 集合**：性能受候选集 B = {4, 8, 16, 32, 64, 128} 的选择影响，未探索更细粒度或连续化 block size
4. **评估限制**：best checkpoint 选择，零样本设置，最长生成 256 token，可能不完全反映长推理场景


## Key Takeaways

### 对 dLLM 研究的启示
- Block size 不是中性超参数，而是直接影响 RL 后训练效果的**结构性因子**
- 多域 RL 训练不能简单堆叠各域数据，需要考虑域间结构冲突
- Sample-level 适配优于 domain-level 适配，因为同一域内不同样本也可能需要不同 block size

### 与机器人/DLO 操控的相关性
- **间接相关**：本文关注 dLLM 而非机器人控制，但其核心思想——"不同任务需要不同的生成/决策粒度"——可迁移到分层控制中
- 扩散策略（Diffusion Policy）在机器人操控中也使用扩散模型，可能面临类似的"扩散步长/块大小与任务粒度不匹配"问题
- RL 后训练中的域冲突分析框架（BCS）可为机器人多任务 RL 训练提供参考

## 相关概念

- [[vision-language-model]]
- [[reinforcement-learning]]
- [[diffusion-model]]
- [[deformable-linear-object]]

## 相关研究者

- [[jiang-yan|Jiang, Yan]]
- [[qiu-ruihong|Qiu, Ruihong]]
- [[huang-zi|Huang, Zi]]
