---
title: "Environmental understanding vision-language model for embodied agent"
tags: [imitation, VLM, RL, robot-learning, planning]
created: "2026-05-15"
updated: "2026-05-15"
type: "literature"
status: "done"
summary: "提出 EUEA 框架，通过在单一 VLM 中微调四组环境理解技能（物体感知、任务规划、动作理解、目标识别），结合采样恢复步骤和 GRPO 精炼阶段，在 ALFRED 上实现 86.48% 任务成功率。"
authors: "Bang, Jinsik; Bae, Jaeyeon; Lee, Donggyu; Jung, Siyeol; Kim, Taehwan"
year: "2026"
venue: "arXiv Preprint"
zotero_key: "TA6B4DNN"
---
## 摘要

Vision-language models (VLMs) have shown strong perception and reasoning abilities for instruction-following embodied agents. However, despite these abilities and their generalization performance, they still face limitations in environmental understanding, often failing on interactions or relying on environment metadata during execution. To address this challenge, we propose a novel framework named Environmental Understanding Embodied Agent (EUEA), which fine-tunes four core skills: 1) object perception for identifying relevant objects, 2) task planning for generating interaction subgoals, 3) action understanding for judging success likelihood, and 4) goal recognition for determining goal completion. By fine-tuning VLMs with EUEA skills, our framework enables more reliable task execution for instruction-following. We further introduce a recovery step that leverages these core skills and a group relative policy optimization (GRPO) stage that refines inconsistent skill predictions. The recovery step samples alternative actions to correct failure cases, and the GRPO stage refines inconsistent skill predictions. Across ALFRED tasks, our VLM significantly outperforms a behavior-cloning baseline, achieving an 8.86% improvement in average success rate. The recovery and GRPO stages provide an additional 3.03% gain, further enhancing overall performance. Finally, our skill-level analyses reveal key limitations in the environmental understanding of closed- and open-source VLMs and identify the capabilities necessary for effective agent-environment interaction.

## 中文简述

提出基于模仿学习的操控方法，具有泛化能力特点。

**研究方向**: 模仿学习、视觉-语言模型、强化学习、机器人学习、运动规划

## 关键贡献

1. **EUEA 框架**：在单一 VLM 中集成四组核心技能（物体感知、任务规划、动作理解、目标识别），无需分离模块建模，实现端到端学习
2. **采样恢复步骤 + GRPO 精炼**：无需额外训练即可恢复失败动作（采样替代动作），GRPO 阶段通过规则奖励进一步修正不一致预测，额外提升 3.03%
3. **大规模技能数据集和评估基准**：提供 1.24M（ALFRED）和 3.7M（LangR）样本的技能数据集，以及基于 ALFRED 和 LangR 的技能评估基准，同时揭示了现有开源/闭源 VLM 在环境理解技能上的关键不足
## 结构化提取

- Problem: VLM 在具身指令跟随中缺乏环境理解能力，交互执行常失败或依赖环境元数据
- Method: EUEA 框架——在单一 VLM（InternVL3-8B）中微调四组环境理解技能（物体感知、任务规划、动作理解、目标识别），结合采样恢复步骤和 GRPO 精炼阶段
- Tasks: 指令跟随（instruction-following），6 类日常任务（Examine in Light, Pick&Place, Pick Two&Place, Clean&Place, Cool&Place, Heat&Place）
- Sensors: 单目 RGB 图像（单帧）
- Robot Setup: 仿真环境（AI2-THOR / Habitat 2.0），离散动作空间，POMDP 建模
- Metrics: 任务成功率（Task Success Rate），技能评估（IoU、Jaccard、Accuracy、Cosine Similarity）
- Limitations: 仅离散环境、无连续控制、低级导航不足、依赖直觉预测而非显式推理、重复动作问题
- Evidence Notes: 全文可获取，实验数据完整（任务评估+技能评估+消融+OOD+恢复对比+backbone对比），所有数字均可追溯至原文表格和图表
## 本地引用关系

-
## 证据元数据

- Fulltext Quality: fulltext（arXiv HTML 全文，含所有公式、表格、图表描述和参考文献）
- Evidence Coverage: 完整覆盖 Method、Experiments（任务评估+技能评估+消融+OOD+恢复步骤+VLM backbone 对比）、Limitations、Conclusion
- Confidence: high
- Summary: 提出 EUEA 框架，通过在单一 VLM 中微调四组环境理解技能（物体感知、任务规划、动作理解、目标识别），结合采样恢复步骤和 GRPO 精炼阶段，在 ALFRED 上实现 86.48% 任务成功率。


## Problem

VLM 在指令跟随的具身智能体中已展现强大的感知和推理能力，但在环境理解方面仍存在关键局限：
1. 交互执行时常失败，无法准确理解当前环境状态
2. 依赖环境元数据（如 object ID、mask），而非从视觉观测中直接获取信息
3. 端到端模型缺乏显式的环境解释能力
4. 现有恢复方法依赖预定义失败类型或外部环境反馈，缺乏视觉基础


## Method

### 框架设计
基于 reward-free POMDP 建模。在每个时间步 t，VLM 仅接收单帧图像 f_t 和累积记忆 M，推理出所有任务相关信息后，选择当前动作 a_t、交互目标 o_t 和 bounding box b_t。

### 四组核心技能（8 个子技能）

**物体感知（Object Perception）**
- Object Recognition (OR)：识别当前图像中存在的物体，v_t = π_θ(I_OR, f_t)
- Object Detection (OD)：检测与当前目标相关的物体的 bounding box，b_t = π_θ(I_OD, sg_t, a_t, o_t, f_t)

**任务规划（Task Planning）**
- Subgoal Task Planning (STP)：为给定主目标生成子目标序列，sg_n = π_θ(I_STP, M)
- Step-by-Step Action Planning (SAP)：为当前子目标生成交互动作，a_t, o_t = π_θ(I_SAP, f_t, v_t, p_t, sg_t, m_{t-k:t-1})

**动作理解（Action Understanding）**
- Action Success Prediction (ASP)：预测当前动作是否会成功（Yes/No），ASP_t = π_θ(I_ASP, a_t, o_t, b_t, f_t)
- Future Situation Captioning (FSC)：描述动作执行后预期的环境变化，FSC_t = π_θ(I_FSC, a_t, o_t, b_t, f_t)
- Action Grounding (AG)：从两帧图像中推断执行了什么动作，a_{t-1}, o_{t-1}, b_{t-1} = π_θ(I_AG, f_{t-1:t})
- ASP 和 FSC 数据通过随机探索生成失败丰富的交互数据（专家轨迹以成功为主），FSC 额外用 caption 描述动作前后图像差异

**目标识别（Goal Recognition）**
- Main Goal Recognition (GR_main)：判断主目标是否已完成，GR_main = π_θ(I_GR_main, M)
- Subgoal Recognition (GR_sub)：判断子目标是否已完成（决定何时切换下一子目标），GR_sub = π_θ(I_GR_sub, sg_t, a_{t-n:t}, f_{t-n:t})

### 采样恢复步骤（Recovery Step）
- 当动作失败时触发（通过图像是否变化判断）
- 采样 n=10 次 SAP 生成替代动作-物体对，选择负对数似然得分最低的（最高置信度）
- 若所有采样与失败动作相同，改为采样 OD 获取新 bounding box
- 无需额外训练

### GRPO 精炼阶段
- 奖励函数：R_total = R_OP + R_TP + R_AU + R_GR
  - R_OP：Jaccard（OR）+ IoU（OD）
  - R_TP：动作-物体对正确性（SAP）+ 动作序列顺序（STP）
  - R_AU：成功预测正确性（ASP/FSC）+ 动作-物体-bbox 组合正确性（AG）
  - R_GR：主目标/子目标预测正确性
- 采样策略：每个实例采样 8 个响应，筛选归一化标准差超过阈值 τ 的模糊案例，构建约 10k 紧凑数据集
- 使用 LoRA 微调 InternVL3-8B，5 epochs（early stopping）

### 训练细节
- 主干 VLM：InternVL3-8B
- SFT：全参数微调 1 epoch，8×A100 80GB，batch size 128，序列长度 8192
- GRPO：LoRA 微调，2×A100 80GB，batch size 64，5/10 epochs（early stopping）
- 视觉编码器冻结，MLP + LLM 微调
- BC baseline：仅保留 OD + SAP + GR_sub（移除其他技能）


## Experiments

### 数据集
- **ALFRED**：基于 AI2-THOR，8,055 专家演示，25,743 人工标注，428k 图像-动作对
- **LangR**：基于 Habitat 2.0，150k episodes，55k 指令（仅用于技能评估，因包含不可见物体交互）
- 技能数据集：ALFRED 1.24M（382k train + 858k val + 5.3k eval），LangR 3.7M（906k train + 2.8M val + 4.4k eval）

### 任务评估（ALFRED，429 个任务，6 类）
| VLM Agent | Avg. | Look | Pick | Pick Two | Clean | Cool | Heat |
|-----------|------|------|------|----------|-------|------|------|
| Human | 91.00 | - | - | - | - | - | - |
| EMMA* | 67.83 | 66.67 | 71.95 | 75.93 | 65.31 | 55.56 | 71.80 |
| BC (InternVL3-8B) | 74.59 | 88.89 | 73.17 | 57.41 | 62.24 | 96.83 | 75.64 |
| Ours (SFT) | 83.45 | 90.74 | 86.59 | 75.93 | 65.31 | 98.41 | 91.03 |
| Ours (GRPO) | 85.78 | 90.74 | 85.37 | 85.19 | 74.49 | 98.41 | 87.18 |
| Ours (GRPO + Recovery) | **86.48** | - | - | - | - | - | - |

- SFT 阶段比 BC 提升 8.86%
- GRPO 阶段额外提升 2.33%（总计 +11.19%）
- Recovery 步骤额外提升 0.7%（总计 +11.89%）
- EMMA 依赖环境元数据和高级交互，本文仅依赖视觉观测和低级动作

### 恢复方法对比
- 本文采样恢复 > 外部环境反馈（oracle feedback），尤其在 GRPO 阶段
- 说明基于智能体自身环境理解的采样优于依赖外部反馈

### 消融实验
| 移除技能 | 性能下降 |
|---------|---------|
| Action Understanding (AU) | -9.32% |
| Action Grounding (AG) | -4.9% |
| Subgoal Task Planning (STP) | -2.8% |
| Goal Recognition Main (GR_main) | -2.33% |
| Future Situation Captioning (FSC) | -1.86% |
- AU 影响最大（包含 ASP + FSC + AG），说明预测动作结果对任务成功至关重要

### VLM Backbone 对比（SFT 阶段）
- InternVL2.5-4B：比 BC 提升 12.84%
- Qwen2.5-VL-3B：比 BC 提升 37.53%
- 方法在不同规模 backbone 上均有效

### OOD 泛化
- ALFRED 微调的模型在 LangR 技能评估上优于 zero-shot InternVL3-8B（除物体感知外）
- 说明 EUEA 技能在分布偏移下可迁移

### 技能评估（关键发现）
- Gemini-2.5-Pro 零样本最强，但 Step-by-Step Action Planning 仅 85.76%（14% 动作失败）
- 大多数零样本 VLM 在动作成功预测、动作接地和物体感知上表现有限
- 微调后的模型在所有技能上显著提升
- 目标识别上 Gemini-2.5-Pro 与微调模型差距仅 4.6%


## Limitations

1. **离散环境限制**：仅在离散动作空间中评估，无法全面理解连续状态转换
2. **无连续控制**：未扩展到连续环境（如真实机器人操控）
3. **导航不足**：聚焦于交互，低级导航仍具挑战
4. **缺乏显式推理**：当前模型（包括本文方法）依赖直觉预测而非显式推理，可能导致环境误理解
5. **重复动作问题**：多步交互中 VLM 可能重复先前动作（SFT 导致 token 分布平坦化），recovery 步骤部分缓解但未完全解决
6. **记忆窗口固定**：k=4 的记忆窗口可能对长 horizon 任务不足


## Key Takeaways

1. **技能分解范式有价值**：将环境理解显式分解为可微调的子技能，使 VLM 获得结构化的环境感知能力。这种范式可迁移到 DLO 操控中（如形状感知、抓取点预测、状态预测）
2. **Action Understanding 最关键**：消融显示预测动作结果对任务成功影响最大（-9.32%），这提示在 DLO 操控中引入形变预测（"这个抓取会成功吗？"）可能带来显著收益
3. **采样恢复比外部反馈更有效**：不依赖预定义失败类型，通过模型自身置信度采样恢复。这一思路可直接用于 DLO 操控的失败恢复
4. **零样本 VLM 仍有限**：即使是 Gemini-2.5-Pro 在 step-by-step 动作规划上也只有 85.76%，说明领域微调的必要性
5. **GRPO 用于动作修正**：将 group-based RL 从推理增强扩展到动作精炼，在紧凑的模糊案例集上即可有效提升性能

## 相关概念

- [[imitation-learning]]
- [[vision-language-model]]
- [[reinforcement-learning]]
- [[robot-learning]]
- [[planning]]
- [[deformable-linear-object]]
- [[grasping]]

## 相关研究者

- [[bang|Bang, Jinsik]]
- [[kim-taehwan|Kim, Taehwan]]
