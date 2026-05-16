---
title: "CRAFT: Video Diffusion for Bimanual Robot Data Generation"
tags: [manipulation, imitation, RL, diffusion, sim-to-real]
created: "2026-05-07"
updated: "2026-05-07"
type: "literature"
status: "done"
summary: "提出 CRAFT 框架，利用 Canny 边缘引导视频扩散模型（Wan2.1）从仿真轨迹生成七维度多样化的双臂操控训练数据（物体位姿/光照/颜色/背景/跨具身/视角/腕部+第三方视角），在仿真和真实双臂任务上全面超越现有数据增强基线。"
authors: "Chen, Jason; Liu, I-Chun Arthur; Sukhatme, Gaurav; Seita, Daniel"
year: "2026"
venue: "arXiv Preprint"
zotero_key: "TW5GGKQF"
---
## 摘要

Bimanual（双臂） robot learning from demonstrations is fundamentally limited by the cost and narrow visual diversity of real-world data, which constrains policy robustness across viewpoints, object configurations, and embodiments. We present Canny-guided Robot Data Generation using Video Diffusion（扩散） Transformers (CRAFT), a video diffusion（扩散）-based framework for scalable bimanual（双臂） demonstration（示范数据） generation that synthesizes temporally coherent manipulation（操控） videos while producing action labels. By conditioning video diffusion（扩散） on edge-based structural cues extracted from simulator-generated trajectories, CRAFT produces physically plausible trajectory variations and supports a unified augmentation pipeline spanning object pose changes, camera viewpoints, lighting and background variations, cross-embodiment（具身） transfer, and multi-view synthesis. We leverage a pre-trained video diffusion model（扩散模型） to convert simulated videos, along with action labels from the simulation trajectories, into action-consistent demonstrations. Starting from only a few real-world demonstrations, CRAFT generates a large, visually diverse set of photorealistic training data, bypassing the need to replay demonstrations on the real robot (Sim2Real). Across simulated and real-world bimanual（双臂） tasks, CRAFT improves success rates over existing augmentation strategies and straightforward data scaling, demonstrating that diffusion（扩散）-based video generation can substantially expand demonstration（示范数据） diversity and improve generalization for dual-arm manipulation（双臂操控） tasks. Our project website is available at: https://craftaug.github.io/

## 中文简述

提出基于扩散模型的双臂方法，具有仿真到真实迁移特点。

**研究方向**: 机器人操控、模仿学习、强化学习、扩散模型、仿真到真实迁移

## 关键贡献

1. **CRAFT 框架**：首个利用 Canny 边缘图作为控制信号条件化视频扩散模型（Wan2.1-Fun-Control），生成高质量、视觉多样化的机器人操作视频，同时保留 action labels。
2. **统一七维度增强管线**：在单一框架内整合物体位姿、光照、物体颜色、背景、跨具身迁移、相机视角、腕部+第三方视角七种增强技术，用户可灵活组合任意子集。
3. **双臂跨具身迁移**：提出基于正运动学/逆运动学的双臂轨迹重定向管线，结合视频扩散生成目标机器人图像，实现无需目标机器人数据采集的策略训练。
4. **充分实验验证**：仿真（RoboTwin 基准，UR5→Franka）和真实世界（xArm7→Franka）六类任务上全面超越 Shadow、VISTA、RoboEngine、SAM3、Color Jitter 等基线。
## 结构化提取

- **Problem**: 双臂模仿学习数据采集成本高、视觉多样性不足；现有增强方法碎片化、不生成新 action labels、未覆盖双臂场景
- **Method**: Canny 边缘引导视频扩散（Wan2.1-Fun-Control）+ 数字孪生轨迹扩展 + 七维度增强管线（物体位姿/光照/颜色/背景/跨具身/视角/腕部+第三方视角）
- **Tasks**: Lift Pot/Roller（协调式）、Place Cans in Plasticbox（并行式）、Stack Bowls（顺序式）— 均为双臂刚体操控
- **Sensors**: 第三方 RGB 相机（Intel RealSense D435i）、腕部相机（可选，最多 3 个 D435i）、AprilTags（物体定位）
- **Robot Setup**: 双臂 Franka Research 3 + GELLO 遥操作（真实世界）；双臂 UR5 (WSG grippers) 和 Franka Panda（仿真）；双臂 xArm7（跨具身源机器人）
- **Metrics**: 成功率（仿真：%；真实：20 次试验成功数）
- **Limitations**: 视频生成伪影；近距离相机依赖；提示工程需求；仿真器和物体网格依赖；子任务分解假设；未验证可变形物体
- **Evidence Notes**: 全文证据充分。仿真跨具身（Table I）和真实世界七维度增强（Table III）均有定量对比；Canny 边缘消融（Table II）清晰隔离了条件化信号贡献。参考图像选择对接触区域保真度的影响有定性对比（附录 Figure 9）。跨具身的真实世界结果尤其有力——从 xArm7 迁移到 Franka 时，CRAFT 超越了直接在 Franka 上采集的数据（17/20 vs 5/20 on LR）。
## 本地引用关系

- [[chen2026craft]]
## 证据元数据

- Fulltext Quality: fulltext
- Evidence Coverage: complete（全文含方法、实验、消融、局限性和附录）
- Confidence: high
- Summary: 提出 CRAFT 框架，利用 Canny 边缘引导视频扩散模型（Wan2.1）从仿真轨迹生成七维度多样化的双臂操控训练数据（物体位姿/光照/颜色/背景/跨具身/视角/腕部+第三方视角），在仿真和真实双臂任务上全面超越现有数据增强基线。


## Problem

双臂机器人模仿学习受限于真实示范数据采集成本高且视觉多样性狭窄。现有数据增强方法各自聚焦单一维度（仅视角、仅背景、仅跨具身），缺乏统一管线来同时覆盖物体位姿变化、光照、背景、相机视角、跨具身迁移和多视角生成。此外，跨具身方法（如 Shadow、Mirage、RoVi-Aug）未扩展到双臂场景，且不生成新的 action labels。


## Method

CRAFT 分为三个阶段：

### 阶段一：Trajectory Expansion（轨迹扩展）
- 利用数字孪生管线（AprilTags 定位 + RoboTwin 物体网格）将真实示教 `D_real` 转移到仿真环境 `D_sim`
- 受 DexMimicGen 启发，将轨迹分解为物体中心子任务，施加变换算子 T 生成新场景配置下的候选轨迹
- 在仿真中验证任务成功，仅保留成功轨迹，渲染为源视频 `V^s`
- 从源视频提取 Canny 边缘控制视频 `V^c`（附加边缘加粗和连通性后处理）

### 阶段二：Video Generation（视频生成）
- 骨干模型：Wan2.1-Fun-Control 1.3B（零样本生成）
- 条件分布：`p_φ(V^d | I^f, V^c, l)`，其中 `V^c` 是 Canny 边缘视频，`I^f` 是真实参考图像，`l` 是语言指令
- **选择 Canny 边缘而非深度/骨架姿态**：骨架仅捕获机器人手臂不含物体信息，深度保留过多细节限制多样性，Canny 在结构保留和视觉灵活性间取得平衡
- 通过选择性修改 `I^f` 和 `l`（保持 `V^c` 固定）生成多样化目标视频

### 阶段三：Augmented Dataset Construction（七维度增强）
1. **物体位姿**：仿真中随机平移/旋转物体，参考图像选择捕获夹爪-物体接触的帧以提升接触合成保真度
2. **光照**：用 Veo3 生成不同环境光照的参考图像变体（保留阴影和反射）
3. **物体颜色**：使用空白桌面参考图像（无物体），通过语言指令指定颜色，LLM 自动生成颜色列表
4. **背景**：省略参考图像，仅通过语言指令描述背景，LLM 自动生成背景描述集
5. **跨具身**：FK 提取源机器人末端执行器位姿 → IK 映射到目标机器人关节配置 → 仿真中生成 Canny 边缘 → 视频扩散生成目标机器人视频
6. **相机视角**：在仿真中放置多个相机，将最多 4 个视角 tile 为单张图像
7. **腕部+第三方视角**：tile 左腕/右腕/第三方视角为单张图像，第四块留空

下游策略使用 ACT，生成视频配对仿真轨迹的 action labels。


## Experiments

### 仿真实验（RoboTwin 基准）
- **设置**：UR5 (WSG grippers) → Franka Panda 跨具身迁移，3 个任务
  - Lift Pot (LP)：协调式（双臂同时抓取）
  - Place Cans (PC)：并行式（双臂独立操作）
  - Stack Bowls (SB)：顺序式（按序堆叠）
- **跨具身结果**（Table I）：
  | 方法 | LP | PC | SB |
  |------|-----|-----|-----|
  | Collected Target | 55.0% | 69.0% | 59.0% |
  | Shadow | 2.0% | 2.3% | 6.0% |
  | CRAFT (Target) | 11.3% | 6.0% | 21.6% |
  | **CRAFT (Ours, 1000 demos)** | **82.6%** | **89.3%** | **86.0%** |
- CRAFT (Ours) 无需采集目标机器人数据，但超越直接在目标机器人上采集 100 次示范的基线

### 消融实验（Table II）
- **CRAFT w/ Canny vs w/o Canny**（Stack Bowls，150 demos）
- Canny 边缘条件化的成功率约为无 Canny 的两倍
- 原因：原始仿真图像保留过多低级细节，扩散模型难以处理夹爪-物体接触等关键结构特征

### 真实世界实验
- **设置**：双臂 Franka Research 3 + GELLO 遥操作，1 或 3 个 RealSense D435i 相机，RTX 5090 训练/推理
- **3 个任务**：Lift Roller (LR)、Place Cans (PC)、Stack Bowls (SB)
- **七维度增强结果**（Table III，每条件 20 次试验）：

| 增强维度 | ACT w/o Aug | CRAFT Pose-Only | Baseline Aug | CRAFT (Ours) |
|---------|-------------|-----------------|--------------|-------------|
| Lighting (LR/PC/SB) | 3/1/0 | 5/3/2 | 13/9/8 | **17/14/12** |
| Background (LR/PC/SB) | 4/0/0 | 7/2/3 | 4/5/6 | **18/15/10** |
| Camera View (LR/PC/SB) | 6/3/2 | 13/5/7 | 14/8/6 | **19/18/18** |
| Object Color (LR/PC/SB) | 2/0/1 | 5/2/3 | 15/9/11 | **18/18/17** |
| Wrist+3rd Person (LR/PC/SB) | 15/11/13 | 13/8/10 | N/A | **20/19/20** |

- **跨具身（真实世界）**（Table I 右侧）：CRAFT (Ours) 17/15/16 vs Shadow 2/1/1 vs Collected Target 5/2/3
- 基线方法：Color Jitter（光照）、RoboEngine（背景）、VISTA（视角）、SAM3（物体颜色）

### 硬件配置
- 视频生成：RTX 5090（小规模）/ 3× RTX 6000（大规模）
- 策略训练/推理：单块 RTX 4090（仿真）/ RTX 5090（真实）
- 视频生成模型：Wan2.1-Fun-Control 1.3B，零样本


## Limitations

1. **视频生成瑕疵**：合成视频可能包含视觉伪影或时序不一致，影响下游策略学习
2. **近距离相机要求**：第三方相机必须靠近机器人和物体，远距离视角产生噪声 Canny 边缘，尤其降低夹爪-物体接触区域的生成质量
3. **提示工程依赖**：虽然零样本生成，但高质量结果需要仔细的 prompt 工程和信息性参考图像
4. **仿真器依赖**：轨迹扩展需要仿真器和物体网格构建数字孪生，限制了难以精确仿真的任务/物体
5. **子任务分解假设**：假设任务可分解为物体中心子任务，不适用于所有操控任务
6. **未测试可变形物体**：作者明确指出未在 DLO 等可变形物体上验证，但提到 SoftMimicGen 可能作为未来扩展方向


## Key Takeaways

1. **Canny 边缘条件化的有效性**：相比深度图和骨架姿态，Canny 边缘在结构保留和视觉多样性之间取得最佳平衡，消融实验证实其将近成功率翻倍。这对我们思考如何为 DLO 操控设计视觉条件信号有参考价值。
2. **视频扩散作为数据增强范式**：从少量真实示教（50-200 次）扩展到 1000 次多样化生成数据，在仿真和真实世界均显著提升策略鲁棒性。这种方法可部分替代昂贵的真实机器人数据采集。
3. **模块化管线的灵活性**：七种增强技术可独立或组合使用，用户可根据下游任务需求灵活配置。
4. **双臂跨具身迁移的实用性**：FK/IK 重定向 + 视频扩散的组合在双臂场景下有效（Shadow 等方法仅验证过单臂），且生成的新 action labels 是关键优势。
5. **对 DLO 操控的局限**：明确未在可变形物体上测试，Canny 边缘提取对 DLO 的细长、柔性轮廓可能不够鲁棒，轨迹扩展的物体中心子任务分解假设也可能不适用于 DLO 的连续变形特征。
6. **数字孪生的双刃剑**：需要精确的物体网格和仿真环境，这既是质量保证也是应用瓶颈。

## 相关概念

- [[robotic-manipulation]]
- [[imitation-learning]]
- [[reinforcement-learning]]
- [[diffusion-model]]
- [[sim-to-real]]
- [[vision-language-model]]
- [[deformable-linear-object]]
- [[bimanual-manipulation]]
- [[grasping]]

## 相关研究者

- [[chen-jason|Chen, Jason]]
- [[liu-i-chun-arthur|Liu, I-Chun Arthur]]
- [[sukhatme|Sukhatme, Gaurav]]
- [[seita|Seita, Daniel]]
