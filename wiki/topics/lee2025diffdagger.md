---
title: "Diff-DAgger: Uncertainty estimation with diffusion policy for robotic manipulation"
tags: [manipulation, imitation, diffusion, robot-learning]
created: "2026-04-25"
updated: "2026-04-25"
type: "literature"
status: "done"
summary: "提出 Diff-DAgger，利用扩散策略训练目标（diffusion loss）作为不确定性估计器实现 robot-gated DAgger。核心洞察：扩散 loss 在 OOD 状态下高、在 in-distribution 多模态状态下低（不像 ensemble variance 会误判多模态为不确定）。通过计算生成动作的 diffusion loss 与训练集分布的分位数比较决定是否请求专家干预。F1 +39%（预测失败）、成功率 +20.6%、wall-clock 快 7.8 倍，3 仿真任务（stacking/pushing/plugging）+ 2 真实任务（stacking/loading）"
authors: "Lee, Sung-Wook; Kang, Xuhui; Kuo, Yen-Ling"
year: "2025"
venue: "arXiv Preprint"
zotero_key: "PF38GPCZ"
---
## 摘要

Recently, diffusion policy（扩散策略） has shown impressive results in handling multi-modal（多模态） tasks in robotic manipulation（机器人操控）. However, it has fundamental limitations in out-of-distribution failures that persist due to compounding errors and its limited capability to extrapolate. One way to address these limitations is robot-gated DAgger, an interactive imitation learning（模仿学习） with a robot query system to actively seek expert help during policy rollout. While robot-gated DAgger has high potential for learning at scale, existing methods like Ensemble-DAgger struggle with highly expressive policies: They often misinterpret policy disagreements as uncertainty at multi-modal（多模态） decision points. To address this problem, we introduce Diff-DAgger, an efficient robot-gated DAgger algorithm that leverages the training objective of diffusion policy（扩散策略）. We evaluate Diff-DAgger across different robot tasks including stacking, pushing, and plugging, and show that Diff-DAgger improves the task failure prediction by 39.0%, the task completion rate by 20.6%, and reduces the wall-clock time by a factor of 7.8. We hope that this work opens up a path for efficiently incorporating expressive yet data-hungry policies into interactive robot learning settings. The project website is available at: https://diffdagger.github.io.

## 中文简述

提出基于扩散策略的推动方法。

**研究方向**: 机器人操控、模仿学习、扩散模型、机器人学习

## 证据元数据

- **Fulltext Quality**: fulltext
- **Evidence Coverage**: 读取了全文，包括 abstract、introduction、related work (Sec II)、method (Sec III)、experiments (Sec IV)、tables (I-IV)、figures (1-6)、算法伪代码 (Algorithm 1)
- **Confidence**: high — 全文完整，arXiv 2025 预印本（v4），5 个操控任务（3 仿真 + 2 真实），100 episodes 评估，完整消融和统计
- **Summary**: 提出 Diff-DAgger，利用扩散策略训练目标（diffusion loss）作为不确定性估计器实现 robot-gated DAgger。核心洞察：扩散 loss 在 OOD 状态下高、在 in-distribution 多模态状态下低（不像 ensemble variance 会误判多模态为不确定）。通过计算生成动作的 diffusion loss 与训练集分布的分位数比较决定是否请求专家干预。F1 +39%（预测失败）、成功率 +20.6%、wall-clock 快 7.8 倍，3 仿真任务（stacking/pushing/plugging）+ 2 真实任务（stacking/loading）
## 关键贡献

1. 基于扩散 loss 的 robot-gated 查询系统：直接利用扩散策略训练目标作为不确定性估计
2. 在多模态数据分布中准确区分 in-distribution（uni/multi-modal）和 OOD 状态
3. 单策略架构（vs ensemble 的多策略），显著减少训练/推理/阈值设置的 wall-clock 时间
4. 完整的 5 任务评估（3 仿真 + 2 真实），涵盖接触丰富、高精度、多模态场景
## 结构化提取

- **Problem**: 扩散策略的 OOD 失败 + 现有 robot-gated DAgger 在多模态数据上的不确定性误判
- **Method**: Diff-DAgger — 扩散 loss 作为不确定性估计 + 分位数阈值 + 连续 K 步验证
- **Tasks**: Stacking/Pushing/Plugging（仿真 ManiSkill）+ Stacking/Loading（真实 Franka）
- **Sensors**: RGB 相机（3 视角/单视角）+ 关节编码器 + 物体位姿
- **Robot Setup**: ManiSkill（仿真）+ Franka Research 3（真实）
- **Metrics**: F1（失败预测）、成功率（100/20 episodes）、wall-clock 时间
- **Limitations**: 训练成本、手动阈值、有限任务多样性
- **Evidence Notes**: 全文读取，Tables I-IV 提供完整超参数和性能对比
## 本地引用关系

- [[chen2025coordinated]]
- [[hartz2024art]]
- [[keunknowndiffuser]]
- [[scheikl620movement]]
- [[wu2025tacdiffusion]]
- [[zhu2024scaling]]
## Problem

扩散策略在多模态操控任务中表现优异但存在 OOD 失败问题（compounding errors + 无法外推）。Robot-gated DAgger 通过机器人自主查询专家来解决此问题，但现有方法（Ensemble-DAgger）在多模态决策点将策略分歧误判为不确定性，导致假阳性过高。


## Method

- **Diffusion Policy 基础**：
  - DDPM 框架：从 N(0,I) 迭代去噪恢复结构化动作序列
  - 训练 loss：Lπ(o,a,ε,t) = ‖f(ε,a,t) − fθ(o,√α_t·a + √(1-α_t)·ε,t)‖²
  - U-Net 架构 + FiLM conditioning
- **OOD 检测（Diffusion Loss）**：
  - 对每个数据点计算期望 diffusion loss：L̄(o,a,π) = E[ε,t][Lπ(o,a,ε,t)]
  - 实现上用 batch Nb=512 采样噪声和时间步取平均
  - 给定分位数阈值 α，若 diffusion loss 超过训练集的 α-分位数则判定 OOD
  - 连续 K 步违反阈值才触发专家干预（减少假阳性）
- **数据聚合与策略更新**：
  - 初始 Ni 条专家演示训练策略
  - 专家干预后完成任务，所有数据加入训练集
  - 每 Nd 次干预后更新策略（训练 + 阈值设置）
- **观察空间**：
  - 状态：关节位置 + 末端位姿 + 物体位姿（ground truth）
  - 图像：R3M ResNet18 + spatial softmax（3 相机/1 相机）


## Experiments

- **仿真任务（ManiSkill）**：
  - Stacking：94%（state）/ 94%（image） vs BC 89%/85%, Ens-DA 72%/83%, Thrifty 79%/86%
  - Pushing（1 expert）：96%/87% vs BC 89%/72%, Ens-DA 87%/81%, Thrifty 85%/81%
  - Pushing（2 experts）：87%/79% vs BC 74%/71%, Ens-DA 70%/59%, Thrifty 69%/68%
  - Plugging：92%/84% vs BC 75%/49%, Ens-DA 69%/37%, Thrifty 65%/47%
- **真实任务（Franka Research 3）**：
  - Stacking：80% vs BC 60%
  - Loading：95% vs BC 80%
- **失败预测（F1，visuomotor）**：
  - Stacking 0.83, Pushing(1) 0.88, Pushing(2) 0.77, Plugging 0.75
  - vs Ensemble-DAgger：42.7% higher F1, 38.4% greater accuracy
  - vs ThriftyDAgger：22.6% higher F1, 32.8% greater accuracy
- **Wall-clock 时间**：总计 0.54h vs Ensemble 4.2h（7.8x faster）
- **Emergent 行为**：DAgger 训练的策略展现恢复行为（失败后重试）


## Limitations

1. 扩散策略训练本身计算成本较高（相比简单 BC）
2. 加速策略训练的很多选择是性能与速度的权衡
3. 分位数阈值 α 和连续步 K 需要手动调参
4. 专家类型限制（运动规划器/RL agent，非通用）
5. 仅在 5 个任务上验证，任务多样性有限


## Key Takeaways

- 扩散 loss 是天然的不确定性估计器：in-distribution 多模态下低 loss，OOD 下高 loss
- Ensemble variance 在多模态任务中产生系统性误判（将分歧视为不确定），这是根本性问题
- 单策略架构带来的计算效率提升是实际部署的关键
- DAgger 收集的数据能产生 offline BC 无法学到的恢复行为
- 分位数阈值 + 连续 K 步验证是实用的假阳性过滤策略

## 相关概念

- [[robotic-manipulation]]
- [[imitation-learning]]
- [[diffusion-model]]
- [[robot-learning]]
- [[vision-language-model]]

## 相关研究者

- [[lee|Lee, Sung-Wook]]
