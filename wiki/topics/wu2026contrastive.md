---
title: "Policy contrastive decoding for robotic foundation models"
tags: [imitation, diffusion, robot-learning]
created: "2026-05-09"
updated: "2026-05-09"
type: "literature"
status: "done"
summary: "提出训练无关的 Policy Contrastive Decoding（PCD），通过对比原始观测与目标物体遮蔽观测的动作概率分布，消除机器人基础模型中的伪相关性，即插即用提升 OpenVLA/Octo/π0 在仿真和真实环境中的泛化性能"
authors: "Wu, Shihan; Luo, Xu; Zhang, Ji; Xie, Junlin; Song, Jingkuan et al."
year: "2026"
venue: "arXiv Preprint"
zotero_key: "GRISRDJ4"
---
## 摘要

Robotic foundation models, or generalist robot policies, hold immense potential to enable flexible, general-purpose and dexterous（灵巧） robotic systems. Despite their advancements, our empirical experiments reveal that existing robot policies are prone to learning spurious correlations from pre-training trajectories, adversely affecting their generalization capabilities beyond the training data. To tackle this, we propose a novel Policy Contrastive Decoding (PCD) approach, which redirects the robot policy's focus toward object-relevant visual clues by contrasting action probability distributions derived from original and object-masked visual inputs. As a training-free method, our PCD can be used as a plugin to improve different types of robot policies without needing to finetune or access model weights. We conduct extensive experiments on top of three open-source robot policies, including the autoregressive policy OpenVLA and the diffusion（扩散）-based policies Octo and $π_0$. The obtained results in both simulation and real-world environments prove PCD's flexibility and effectiveness, e.g., PCD enhances the state-of-the-art（现有最优方法） policy $π_0$ by 8.9% in the simulation environment and by 108% in the real-world environment. Code and demos are publicly available at: https://koorye.github.io/PCD.

## 中文简述

提出基于扩散模型的灵巧手方法，具有泛化能力特点。

**研究方向**: 模仿学习、扩散模型、机器人学习

## 关键贡献

1. **PCD 方法**：首次提出训练无关（training-free）、即插即用的 Policy Contrastive Decoding，通过对比原始观测与物体遮蔽观测的动作概率分布，将策略注意力从伪特征重定向到物体相关特征
2. **Track2Mask 策略**：结合 Grounding DINO + SAM2 实现自动目标检测、跟踪和遮蔽，支持人工 Point/Box 提示和自动检测两种模式
3. **KDE-based Probabilistic Modeling（KDE-PM）**：通过核密度估计为扩散策略（Octo, π0）近似动作概率分布，使 PCD 兼容自回归和扩散两类策略
4. **广泛验证**：在 SIMPLER 仿真（9任务）和真实世界（6任务）共 15 个任务上，对 OpenVLA、Octo、π0 三个基线策略进行测试，一致取得显著提升
## 结构化提取

- Problem: 机器人基础模型在预训练数据中学到伪相关（依赖背景/纹理等任务无关特征而非目标物体），导致分布偏移时泛化性能严重退化
- Method: Policy Contrastive Decoding（PCD）——训练无关、即插即用的推理时方法；通过对比原始观测与目标物体遮蔽观测的动作概率分布消除伪相关影响；Track2Mask 自动检测/跟踪/遮蔽目标物体；KDE-PM 为扩散策略近似概率分布
- Tasks: 9 仿真任务（SIMPLER: Close/Open Drawer, Move Near, Pick Coke Can, Apple Drawer, Carrot Plate, Eggplant Basket, Spoon Towel, Stack Cube）+ 6 真实任务（Pick Ball, Pick Plug, Move Near, Cookies Towel, Banana Plate, Stack Cube）
- Sensors: RGB 相机（第三人称视角；附录 K 验证了含腕部相机的多视角场景）
- Robot Setup: 仿真：Google Robot + WidowX；真实：AGILEX PIPER 6DOF 机械臂
- Metrics: 成功率（%），95% 置信区间，300 trials（仿真）/20 trials（真实）；推理延迟（s/step），显存占用（MB）
- Limitations: 推理延迟翻倍；仅推理阶段；依赖物体检测质量；未覆盖柔性物体/DLO
- Evidence Notes:

  - Fig.1 CAM 可视化直接证明策略注意力在背景而非目标物体
  - Table 1 仿真 9 任务完整数据：PCD 一致提升三个基线
  - Fig.3 真实世界 6 任务：π0+PCD 平均提升 108%
  - Fig.5 鲁棒性测试：改变光照/背景/纹理/空间关系后 PCD 一致缓解退化
  - Table 6 PCD vs CFG：PCD 显著优于 CFG
  - Table 8 不完全遮蔽消融：β=0.6 时退化为基线
  - Appendix K 多视角：LIBERO-90 上 miniVLA+PCD 平均 71.2→79.6%
## 本地引用关系

- [[wu2026contrastive]]
## 证据元数据

- Fulltext Quality: fulltext
- Evidence Coverage: complete（正文+附录A-L全部读取，含15个任务的完整实验数据）
- Confidence: high
- Summary: 提出训练无关的 Policy Contrastive Decoding（PCD），通过对比原始观测与目标物体遮蔽观测的动作概率分布，消除机器人基础模型中的伪相关性，即插即用提升 OpenVLA/Octo/π0 在仿真和真实环境中的泛化性能


## Problem

机器人基础模型（generalist robot policies）在预训练数据上容易学到**伪相关（spurious correlations）**——即依赖任务无关的视觉特征（背景纹理、光照区域、物体位置等）而非目标物体本身来预测动作。作者通过实验证据表明：
- 仅改变光照区域位置，OpenVLA 成功率下降 36%
- 仅改变抽屉把手位置，成功率下降 32%
- CAM 可视化确认模型注意力集中在背景而非目标物体

这种伪相关导致模型在部署环境与训练环境存在分布偏移时性能严重退化。


## Method

### 核心公式

给定预训练策略 π_θ，对当前观测 o_i 和物体遮蔽观测 ô_i（目标物体被 inpainting 移除）：

$$\pi^*_\theta(a_i|l, o_i) = \frac{1}{C} \cdot \pi_\theta(a_i|l, o_i) \cdot \left(\frac{\pi_\theta(a_i|l, o_i)}{\pi_\theta(a_i|l, \hat{o}_i)}\right)^\alpha$$

其中 C 为归一化常数，α ≥ 0 控制对比强度（α=0 退化为基线）。

### Track2Mask 模块
1. 初始帧标注：人工 Point/Box 提示 或 Grounding DINO 自动检测
2. SAM2 在后续帧跟踪并分割目标物体
3. LaMa inpainting 移除分割区域，生成物体遮蔽观测

### KDE-PM（针对扩散策略）
1. 用扩散策略采样 N=24 个候选动作 {a_i(j)}
2. 对每个动作维度独立做 KDE：π_θ(a_t|l,o_i) ≈ (1/C') Σ K((a_t - a_t(j))/b)
3. 同理对 ô_i 生成遮蔽分布
4. 代入核心公式计算对比概率

### 推理流程
对每一步：获取遮蔽观测 → 计算两组概率分布 → 对比修正 → 采样动作 → 执行


## Experiments

### 仿真实验（SIMPLER 基准）

| 基线策略 | Base 成功率 | +PCD 最佳成功率 | 相对提升 | 最佳 α |
|---------|-----------|---------------|---------|-------|
| OpenVLA | 16.8% | 25.3%（GDINO） | +50.6% | 0.8 |
| Octo | 13.8% | 17.9%（GDINO） | +29.7% | 1.0 |
| π0 | 63.9% | 69.6%（GDINO） | +8.9% | 0.2 |

- 9 个任务（Google Robot 5 + WidowX 4），每任务 300 trials
- 三种标注方式（Point, Box, GDINO）均有效，GDINO 通常最优或接近最优
- π0 本身已很强（63.9% avg），PCD 仍能进一步提升

### 真实世界实验

| 指标 | π0 baseline | π0 + PCD |
|------|-----------|----------|
| 平均成功率 | ~20%（6任务平均） | +108% 提升 |
| 时间开销 | baseline | +24% |

- AGILEX PIPER 6DOF 机械臂，6 个操控任务
- 每任务 20 trials，随机化配置和朝向
- π0 先用 LoRA（rank=16）在 6 个任务各 10 条演示上 fine-tune
- 复杂背景（塑料瓶、篮子、垃圾桶等干扰物）下仍有效

### 消融实验

1. **α 敏感性**：α > 0 时 PCD 一致优于基线，但最优值因策略而异（Octo 1.0, OpenVLA 0.8, π0 0.2）
2. **检测模型**：Grounding DINO > YOLO World ≈ SED，但三者均有效
3. **Inpainting 策略**：LaMa > Telea > Navier-Stokes，但差异不大
4. **鲁棒性测试**：改变光照、背景、纹理、空间关系后，PCD 一致缓解性能下降；10 个未见场景中 4 个甚至超过原始训练场景

### 计算开销
- 推理延迟约翻倍（OpenVLA: 0.86→1.77s, Octo: 0.21→0.39s, π0: 0.66→1.09s）
- 显存增加：Octo 1.22x, π0 1.37x, OpenVLA 几乎无变化
- 真实场景中延迟增加仅带来 24% 总时间增加（因为物理执行占主导）

### PCD vs. Classifier-Free Guidance（CFG）
- PCD 优于 CFG（68.1% vs 62.7%，π0 on SIMPLER）
- CFG 在噪声空间中操作，早期介入会破坏语义完整性
- PCD 是显式后验修正，更稳定


## Limitations

1. **计算开销**：每步需额外一次前向传播（物体遮蔽输入），推理延迟翻倍；扩散策略还需 KDE-PM 采样 24 个候选
2. **仅推理阶段**：只解决推理时的伪相关问题，不涉及训练阶段预防伪相关的学习
3. **物体检测依赖**：Track2Mask 依赖 GDINO + SAM2 的检测/跟踪质量；检测失败时 PCD 退化为基线；不完全遮蔽（β=0.6）时性能接近基线
4. **多物体长序列任务**：当前对所有任务相关物体同时遮蔽；长序列任务需按子任务切换遮蔽目标（已验证可行但需 LLM 规划器）
5. **α 需策略级调参**：不同基线策略的最优 α 差异大（0.2~1.0），论文用统一参数，有任务级调参空间
6. **未涉及 DLO/柔性物体**：实验全部是刚性物体操控


## Key Takeaways

1. **伪相关是机器人基础模型泛化瓶颈之一**：这篇工作通过实验证据（CAM 可视化 + 定量消融）明确证明了该问题的严重性——改变光照就能让策略下降 36%，这在实际部署中极易发生
2. **Contrastive Decoding 思想迁移到机器人操控**：从 VLM anti-hallucination（VCD/ICD）迁移到机器人策略推理，通过对比"有无物体"两个分布来突出物体相关特征，思路简洁有效
3. **训练无关 = 部署友好**：不需要 fine-tune、不需要访问模型权重，对开源闭源模型都适用，降低部署门槛
4. **对 DLO 操控的启示**：DLO 任务中视觉特征更复杂（绳子形状、纹理、遮挡），伪相关问题可能更严重。PCD 的思路是否适用于 DLO 取决于能否可靠检测/跟踪 DLO 并生成有效遮蔽观测
5. **与 Sim-to-Real 的关系**：PCD 部分缓解了 OOD 泛化问题（改变背景/光照/纹理后性能恢复），但未从根本上解决 sim-to-real gap

## 相关概念

- [[imitation-learning]]
- [[diffusion-model]]
- [[robot-learning]]
- [[vision-language-model]]
- [[deformable-linear-object]]
- [[grasping]]

## 相关研究者

- [[wu-shihan|Wu, Shihan]]
- [[luo-xu|Luo, Xu]]
- [[zhang-ji-swjtu|Zhang, Ji]]
- [[xie-junlin|Xie, Junlin]]
