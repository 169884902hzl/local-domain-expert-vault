---
title: "Self-Improving Loops for Visual Robotic Planning"
tags: [manipulation, imitation, RL, planning]
created: "2026-05-07"
updated: "2026-05-07"
type: "literature"
status: "done"
summary: "提出 SILVR 框架，让领域内视频生成模型通过自收集轨迹的迭代微调持续改进对新任务的视觉规划能力，结合 IPA 评分组合引入互联网视频先验，在 MetaWorld 12 个未见任务和真实 Panda 机械臂上验证了显著的自改进效果，最终可蒸馏为轻量级扩散策略。"
authors: "Luo, Calvin; Zeng, Zilai; Jia, Mingxi; Du, Yilun; Sun, Chen"
year: "2026"
venue: "arXiv Preprint"
zotero_key: "53B76XTP"
---
## 摘要

Video generative models trained on expert demonstrations have been utilized as performant text-conditioned visual planners for solving robotic tasks. However, generalization to unseen tasks remains a challenge. Whereas improved generalization may be facilitated by leveraging learned prior knowledge from additional pre-collected offline data sources, such as web-scale video datasets, in the era of experience we aim to design agents that can continuously improve in an online manner from self-collected behaviors. In this work we thus propose the Self-Improving Loops for Visual Robotic Planning (SILVR), where an in-domain video model iteratively updates itself on self-produced trajectories, and steadily improves its performance for a specified task of interest. We apply SILVR to a diverse suite of MetaWorld tasks, as well as two manipulation（操控） tasks on a real robot arm, and find that performance improvements continuously emerge over multiple iterations for novel tasks unseen during initial in-domain video model training. We demonstrate that SILVR is robust in the absence of human-provided ground-truth reward（奖励） functions or expert-quality demonstrations, and is preferable to alternate approaches that utilize online experience in terms of performance and sample efficiency.

## 中文简述

提出基于学习方法的操控方法，具有泛化能力特点。

**研究方向**: 机器人操控、模仿学习、强化学习、运动规划

## 关键贡献

1. **SILVR 框架**：提出 Self-Improving Loops for Visual Robotic Planning，领域内视频模型迭代地在自生成轨迹上更新自身，稳步提升指定任务的规划性能
2. **IPA 实际部署验证**：将 Inverse Probabilistic Adaptation（评分组合）应用于真实机器人场景，验证互联网视频先验对 sim-to-real 的关键作用
3. **多维度鲁棒性验证**：证明 SILVR 在无 GT 奖励函数（可用 VLM 替代）、非专家演示数据初始化、无数据过滤等条件下仍能有效自改进
4. **蒸馏部署**：将最终改进后的视频规划器蒸馏为轻量级 Diffusion Policy，实现高效推理，且蒸馏后性能略优于教师模型
5. **全面实验覆盖**：MetaWorld-v2 12 个未见任务 + 真实 Franka Panda 机械臂（推杯、开抽屉），与 DSRL 和 BCIL 基线对比
## 结构化提取

- **Problem**: 视频生成模型作为视觉规划器泛化到未见任务困难，且仅依赖离线数据无法持续改进
- **Method**: SILVR 框架（迭代自改进循环）+ IPA（评分组合融合互联网先验）+ 可选蒸馏为轻量策略
- **Tasks**: MetaWorld-v2 12 个未见任务（推/拉/抓取等）、Panda 机械臂推杯（未见颜色）、Panda 机械臂开抽屉（未见颜色）
- **Sensors**: RGB 相机（视觉观测帧）
- **Robot Setup**: MetaWorld 仿真环境（Sawyer 机械臂）、真实 Franka Emika Panda 单臂
- **Metrics**: 任务成功率（GT/人工/VLM 判断）
- **Limitations**: 冷启动假设、推理计算成本高、缺乏显式探索机制、迭代约 5 次后饱和
- **Evidence Notes**:

  - MetaWorld 5 次迭代 GT Filter 成功率从 14.7% 提升至 44.2%，VLM Filter 从 17.0% 至 38.4%（Table 1）
  - 蒸馏策略达到 49.2%，超越视频规划器教师模型
  - DSRL 无法改进（9.4→7.7），BCIL 快速饱和（5.6→23.2）
  - 真实机器人实验：配合 AnimateDiff 先验可持续改进，无先验时性能下降
  - 次优数据（70% random + 30% expert）初始化仍可实现自改进（Figure 6）
  - 迭代 5 次后边际增益递减，推测策略局部最优（Figure 4）
  - VLM 过滤（GPT-5、Gemini-2.5-Pro）可替代 GT 奖励实现自改进（Figure 5a）
## 本地引用关系

-
## 证据元数据

- Fulltext Quality: fulltext
- Evidence Coverage: complete
- Confidence: high
- Summary: 提出 SILVR 框架，让领域内视频生成模型通过自收集轨迹的迭代微调持续改进对新任务的视觉规划能力，结合 IPA 评分组合引入互联网视频先验，在 MetaWorld 12 个未见任务和真实 Panda 机械臂上验证了显著的自改进效果，最终可蒸馏为轻量级扩散策略。


## Problem

视频生成模型在专家演示数据上训练后可作为文本条件视觉规划器用于机器人任务，但泛化到未见任务仍然困难。即使利用互联网规模视频数据预训练，模型仍仅依赖离线数据，无法从自收集的在线经验中持续改进。本文研究如何让视觉规划器突破离线数据限制，通过自收集行为实现对新任务的迭代自改进。


## Method

### 核心架构
SILVR 基于 UniPi 框架，包含两个核心组件：
- **文本到视频模型**：根据当前观测和任务文本提示生成未来帧序列作为视觉规划
- **逆动力学模型（IDM）**：将连续帧对转化为可执行的机器人动作

### Inverse Probabilistic Adaptation (IPA)
训练无关的评分组合方法，将领域内小模型与互联网预训练大模型结合：
```
ε̃_inv = ε_general(τ_t, t) + α·ε_general(τ_t, t|text) + γ·ε_θ(τ_t, t|text) - ε_general(τ_t, t)
```
- `γ`：先验强度
- `α`：文本条件引导尺度
- 领域内模型提供环境特定的视觉特征和动力学知识
- 大模型提供更强的文本条件泛化能力作为主去噪器

### 自改进循环（Algorithm 1）
1. 初始化领域内视频模型 `ε_θ`（在通用演示数据上预训练）
2. 每次迭代：
   - 可选：通过 IPA 与互联网视频模型组合
   - 执行 N 次视觉规划 rollout 收集轨迹
   - 用过滤函数筛选成功轨迹
   - 用累积数据微调领域内视频模型（IDM 也可同步微调）
3. 重复 K 次迭代
4. 可选：将最终视频模型蒸馏为轻量级 Diffusion Policy

### 实现细节
- 视频模型基于 AVDC 架构，增加跨注意力层改进文本条件
- 生成 8 帧未来帧，MetaWorld 帧跳 1，真实机器人帧跳 16
- 互联网预训练模型使用 AnimateDiff（~2B 参数），预训练于 WebVid-10M
- IDM 两种实现：MLP-IDM（用于真实）+ Diffusion-IDM（用于仿真）
- 每次迭代微调 8000-10000 步


## Experiments

### MetaWorld-v2 仿真实验
- **预训练数据**：8 个任务的 25 段演示
- **评估任务**：12 个未见任务
- **每次迭代**：30 条轨迹，3 个种子取平均

**主要结果（Table 1，5 次迭代平均成功率）**：

| 方法 | Iter 0 | Iter 1 | Iter 2 | Iter 3 | Iter 4 |
|------|--------|--------|--------|--------|--------|
| DSRL (GT Filter) | 9.4 | 8.3 | 7.4 | 7.5 | 7.7 |
| BCIL (GT Filter) | 5.6 | 12.3 | 20.9 | 23.3 | 23.2 |
| SILVR (GT Filter) | 14.7 | 27.7 | 33.5 | 43.5 | 44.2 |
| SILVR (VLM Filter) | 17.0 | 24.4 | 28.7 | 34.4 | 38.4 |
| SILVR-Distilled DP | - | - | - | - | **49.2** |

- SILVR 从 Iteration 1 起大幅超越所有基线
- DSRL 无法改进，BCIL 快速饱和在低成功率
- 蒸馏策略达到最佳整体性能 49.2%

### 真实机器人实验（Franka Panda）
**推杯任务**：
- 场景：3 个不同颜色杯子，指定颜色推向前方
- 训练色：红、绿、蓝、粉（120 段演示）
- 测试色：橙、紫（未见颜色）
- SILVR 配合 AnimateDiff 持续改进；无互联网先验时性能下降

**开抽屉任务**：
- 场景：两个不同颜色抽屉，指定颜色打开
- 训练色：红、绿、蓝（144 段演示）
- 测试色：黄色（未见）
- 同样需要互联网视频先验才能实现自改进

### 关键发现

**迭代饱和**（Figure 4）：SILVR 在约 Iteration 5 达到饱和，之后边际增益递减。作者推测可能是任务特定策略陷入局部最优。

**VLM 过滤**（Figure 5a）：GPT-5 和 Gemini-2.5-Pro 均可替代 GT 奖励信号实现自改进，其中 Gemini 表现最佳。无过滤时 MetaWorld 改进微弱。

**无过滤在真实机器人有效**（Figure 5b）：配合互联网先验，即使不过滤数据也能持续改进。原因：次优数据仍传递了环境视觉和动力学信息，通过 IPA 组合后仍能产生有效规划。

**次优数据初始化**（Figure 6）：70% 随机 + 30% 专家的数据仍能实现自改进。某些任务（Drawer Close, Reach Wall, Button Press Wall）从次优初始化反而获益更多。


## Limitations

1. **冷启动问题**：SILVR 隐式假设初始模型（可配合互联网先验）对新任务有一定成功率来收集有效经验；当新任务过于困难时此假设不成立
2. **计算成本**：视频生成过程推理速度慢，需要蒸馏才能高效部署
3. **互联网模型选择权衡**：AnimateDiff 在质量和效率间取得平衡，但更新更强的视频生成模型值得探索
4. **探索不足**：当前框架缺乏显式探索机制，可能导致"单模态"行为和早期饱和
5. **Sim-to-Real 差距**：MetaWorld 中互联网先验帮助不大，但真实世界部署时至关重要，表明仿真无法完全反映真实复杂度


## Key Takeaways

1. **视觉规划优于直接策略的迁移性**：将动力学建模与动作预测解耦，使得学到的环境视觉动力学更易迁移到新任务，基础泛化性能显著优于 Diffusion Policy
2. **评分组合是高效的知识融合方式**：IPA 不需要训练即可组合互联网先验和领域内知识，且对次优数据具有鲁棒性——次优演示仍传递了环境视觉和动力学信息
3. **VLM 作为奖励信号的可行性**：GPT-5/Gemini-2.5-Pro 可作为任务成功判断器，降低对人工奖励函数的依赖
4. **蒸馏可超越教师**：视频规划器蒸馏为轻量级策略后性能略有提升，表明视觉规划作为"中间表征"可能捕获了更丰富的任务结构
5. **对 DLO 操控的启示**：SILVR 的自改进范式可应用于 DLO 操控场景——先用视频模型学习 DLO 的视觉动力学，再通过自收集数据迭代改进，VLM 可作为操控成功的自动评估器

## 相关概念

- [[robotic-manipulation]]
- [[imitation-learning]]
- [[reinforcement-learning]]
- [[planning]]
- [[vision-language-model]]
- [[diffusion-model]]
- [[deformable-linear-object]]
- [[grasping]]

## 相关研究者

- [[luo-calvin|Luo, Calvin]]
- [[zeng-zilai|Zeng, Zilai]]
- [[du-yilun|Du, Yilun]]
- [[sun-chen|Sun, Chen]]
