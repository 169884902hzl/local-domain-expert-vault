---
title: "Compose by focus: Scene graph-based atomic skills"
tags: [manipulation, imitation, VLM, diffusion, robot-learning]
created: "2026-05-03"
updated: "2026-05-03"
type: "literature"
status: "done"
summary: "提出 focused scene graph 表示法，仅编码任务相关物体的 3D 几何和语义关系作为图节点与边，用 GAT 编码图特征后条件化 Diffusion Policy，实现原子技能在杂乱场景中的零样本组合，仿真和真实实验均大幅超越 2D/3D Diffusion Policy 和 π0。"
authors: "Qi, Han; Chen, Changhe; Yang, Heng"
year: "2026"
venue: "arXiv Preprint"
zotero_key: "TH2VBE5J"
---
## 摘要

A key requirement for generalist robots is compositional generalization - the ability to combine atomic skills to solve complex, long-horizon（长时序） tasks. While prior work has primarily focused on synthesizing a planner that sequences pre-learned skills, robust execution of the individual skills themselves remains challenging, as visuomotor policies often fail under distribution shifts induced by scene composition. To address this, we introduce a scene graph-based representation that focuses on task-relevant objects and relations, thereby mitigating sensitivity to irrelevant variation. Building on this idea, we develop a scene-graph skill learning framework that integrates graph neural networks with diffusion（扩散）-based imitation learning（模仿学习）, and further combine "focused" scene-graph skills with a vision-language model（视觉-语言模型） (VLM) based task planner. Experiments in both simulation and real-world manipulation（操控） tasks demonstrate substantially higher success rates than state-of-the-art（现有最优方法） baselines, highlighting improved robustness and compositional generalization in long-horizon（长时序） tasks.

## 中文简述

提出基于扩散模型的操控方法，具有泛化能力特点。

**研究方向**: 机器人操控、模仿学习、视觉-语言模型、扩散模型、机器人学习

## 关键贡献

1. **Scene graph 作为行为克隆的结构化输入**：提出将 RGB-D 观测转换为 3D 语义场景图（节点 = 物体 3D 点云嵌入，边 = VLM 推理的物体间关系），替代原始 2D 图像或 3D 点云。利用 Grounded-SAM 分割 + CLIP/DP3 编码节点，VLM（ChatGPT）推理边关系。
2. **Scene graph + Diffusion Policy 端到端训练**：将 GAT 编码的图特征与 CLIP 文本特征一起条件化 Diffusion Policy，在多技能训练数据上统一训练单一策略网络。
3. **Compose-by-Focus 框架验证**：在 5 个仿真多技能任务（13 个原子技能）和 2 个真实世界任务（6 个原子技能）上，场景图方法在技能组合场景下的成功率比基线高 40-90 个百分点。
## 结构化提取

- Problem: 视觉-运动策略在场景组合时的分布偏移问题——单技能训练的策略无法在多物体杂乱场景中鲁棒执行
- Method: Focused 3D Scene Graph（节点=Grounded-SAM 分割的点云，边=VLM 推理的语义关系）+ 2 层 GAT 编码 + Diffusion Policy 条件化
- Tasks: 刚体操控（pick, place, push, pull, tool use, obstacle avoidance），长时序组合任务
- Sensors: RGB-D 相机（仿真 + 真实 RealSENSE L515 双目）
- Robot Setup: 单臂机器人，6-DoF 末端执行器，SpaceMouse 示教
- Metrics: 成功率（完成的子技能比例），每个任务 50 seeds（仿真）或 20 trials（真实）
- Limitations: VLM 计算开销；Grounded-SAM 分割精度依赖；仅覆盖训练时已见原子技能；未验证 DLO/可变形物体
- Evidence Notes:

  - 仿真 5 个任务 13 个原子技能，单技能接近 1.0，组合平均 0.86 vs 基线 0.0-0.77（Table I）
  - 真实蔬菜拾取组合 0.97 vs 基线最高 0.2（Table II）
  - 真实工具使用 0.9 vs 基线最高 0.6（Table III）
  - 消融确认 3D 节点、图结构、GNN 三者缺一不可（Fig. 6）
## 本地引用关系

-
## 证据元数据

- Fulltext Quality: fulltext (arXiv HTML)
- Evidence Coverage: high (全文含仿真 + 真实实验 + 消融，共 7 张表/图)
- Confidence: high
- Summary: 提出 focused scene graph 表示法，仅编码任务相关物体的 3D 几何和语义关系作为图节点与边，用 GAT 编码图特征后条件化 Diffusion Policy，实现原子技能在杂乱场景中的零样本组合，仿真和真实实验均大幅超越 2D/3D Diffusion Policy 和 π0。


## Problem

现有机器人模仿学习方法在单技能场景训练后，面对多物体杂乱场景（即需要技能组合的长时序任务）时，视觉-运动策略因分布偏移（distribution shift）而严重退化。之前工作多关注高层规划器的技能串联，但忽略了底层技能本身的组合鲁棒性问题：如何构造原子技能使其能在未见过的场景组合中保持有效？

核心假设：可组合的技能必须是 **focused** 的——仅关注与当前技能相关的物体和关系，忽略无关干扰物。


## Method

### 整体架构

1. **Scene Graph 构建**（§III-B）：
   - 输入：RGB-D 图像
   - Grounded-SAM 分割任务相关物体的 mask → 提取对应 3D 点云
   - Farthest point sampling 下采样 → DP3 Encoder（MLP）编码为节点特征 h_i^(0)
   - VLM（ChatGPT）从 RGB 推理物体间关系（grasp, next, inside 等）→ 边
   - 子图仅包含：机器人末端、相关物体、目标、可选障碍物

2. **GAT 图编码**（§III-C）：
   - 2 层 GAT：Layer 1（4 heads, ELU, concat），Layer 2（1 head, Identity, avg）
   - Global mean pool → 图特征向量 F
   - 技能描述用 CLIP 编码为文本特征 P

3. **Diffusion Policy**（§III-C）：
   - 条件化：图特征 F + 文本特征 P + 机器人位姿 Q
   - 标准 DDPM 去噪：A_t^{k-1} = α_k(A_t^k - γ_k ε_θ(A_t^k, k, F, P, Q)) + σ_k N(0, I)
   - 训练目标：MSE loss 预测噪声
   - 端到端训练点云编码器、图编码器和扩散模型

4. **测试时技能组合**（§III-D）：
   - VLM（ChatGPT-4V）分解长时序任务为子目标序列
   - 每个子目标动态构建 focused sub-scene-graph
   - 训练好的单一策略依次执行

### 关键设计选择
- 节点：物体 3D 点云（非 2D crop），保证空间丰富性
- 边：语义关系（VLM 推理），非纯几何邻近
- 图规模小（仅相关物体），VLM 开销可控


## Experiments

### 仿真实验（ManiSkill2）

**任务设计**：5 组多技能任务，13 个原子技能，每组 100 条 demo

| 任务 | 原子技能数 | 组合场景描述 |
|------|-----------|-------------|
| Cube Out and In | 2 | 移出红方块 + 放入蓝方块 |
| Sort by Color | 3 | 按颜色匹配放置 |
| Blocks Stacking Game | 3 | 逻辑条件操作 |
| Tools Usage | 2 | L 形工具拉 + 棍推 |
| Obstacle Avoidance | 3 | 含障碍物避让的工具使用 |

**单技能结果**（Table I(a)）：所有方法均接近 1.0，确认基线实现正确。

**技能组合结果**（Table I(b)）：

| 方法 | Cube Out/In | Sort Color | Blocks Stack | Tools Use | Obstacle Avoid |
|------|------------|-----------|-------------|-----------|---------------|
| Diffusion Policy | 0.0 | 0.04 | 0.47 | 0.0 | 0.52 |
| DP3 | 0.27 | 0.07 | 0.48 | 0.13 | 0.44 |
| π0 | 0.15 | 0.02 | 0.77 | 0.07 | 0.49 |
| **Scene Graph** | **0.78** | **0.79** | **0.93** | **0.88** | **0.90** |

基线平均下降 50-70%，Scene Graph 仅小幅下降。

**消融实验**（Fig. 6）：
- 2D 节点 vs 3D 节点：3D 点云表示显著优于 2D crop（DINOv2）
- 图 vs 点云拼接：无图结构的点云拼接无法处理可变物体数量
- GNN vs 节点拼接：GNN 排列不变性关键，拼接方法对物体顺序敏感

### 真实世界实验

**蔬菜拾取**（Table II）：
- 单技能（含干扰物）：Scene Graph 1.0, π0 1.0, DP3 0.7, DP 0.6
- 组合：Scene Graph **0.97**, DP 0.0, DP3 0.2, π0 0.05

**工具使用**（Table III）：
- Scene Graph **0.9**, DP3 0.6, DP 0.4, π0 0.075

真实场景中 π0 大幅退步，说明大规模预训练不能替代结构化表示。


## Limitations

1. **VLM 依赖**：动态构建场景图依赖 VLM（ChatGPT），引入额外计算开销（虽然子图小，开销可控）
2. **分割质量依赖**：依赖 Grounded-SAM 的分割精度，mask 不准确会传播错误
3. **技能覆盖假设**：测试时所有原子技能必须在训练时已学到，不支持新技能的即时学习
4. **未涉及 DLO 或可变形物体**：实验限于刚体操控，未验证对可变形物体的适用性


## Key Takeaways

1. **Focused 表示是组合泛化的关键**：仅编码任务相关物体的子图，而非全场景，能有效对抗分布偏移。这一思路对 DLO 操控有启发——可以构建以 DLO 为中心的子图，忽略无关刚体。
2. **Scene graph 作为 VLM 与低层策略的自然接口**：VLM 理解场景语义 → 生成子图 → GNN 编码 → 条件化 Diffusion Policy，这个管线设计清晰且可扩展。
3. **数据效率**：不需要组合爆炸的长时序 demo，仅用单技能 demo 即可实现零样本组合，数据成本从指数级降为线性。
4. **3D 点云节点 + 语义边**的组合优于纯 2D 或纯 3D 方法，说明几何与语义信息的互补性。

## 相关概念

- [[robotic-manipulation]]
- [[imitation-learning]]
- [[vision-language-model]]
- [[diffusion-model]]
- [[robot-learning]]
- [[deformable-linear-object]]
- [[grasping]]

## 相关研究者

- [[qi|Qi, Han]]
- [[chen-changhe|Chen, Changhe]]
- [[yang-heng|Yang, Heng]]
