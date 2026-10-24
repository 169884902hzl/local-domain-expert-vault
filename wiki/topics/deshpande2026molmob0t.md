---
title: "MolmoB0T: Large-scale simulation enables zero-shot manipulation"
tags: [manipulation, imitation, VLM, flow-matching, sim-to-real]
created: "2026-05-08"
updated: "2026-05-08"
type: "literature"
status: "done"
summary: "基于 MolmoSpaces 生成 1.7M 仿真专家轨迹，训练三种策略架构（VLM+flow-matching、π0 复现、轻量 Transformer），在 Franka FR3 和 RB-Y1 上实现零样本 Sim-to-Real，桌面 pick-and-place 达 79.2% 超过 π0.5 的 39.2%"
authors: "Deshpande, Abhay; Guru, Maya; Hendrix, Rose; Jauhri, Snehal; Eftekhar, Ainaz et al."
year: "2026"
venue: "arXiv Preprint"
zotero_key: "94TIWX8M"
---
## 摘要

A prevailing view in robot learning is that simulation alone is not enough; effective sim-to-real（仿真到真实迁移） transfer is widely believed to require at least some real-world data collection or task-specific fine-tuning to bridge the gap between simulated and physical environments. We challenge that assumption. With sufficiently large-scale and diverse simulated synthetic training data, we show that zero-shot（零样本） transfer to the real world is not only possible, but effective for both static and mobile manipulation（移动操控）. We introduce MolmoBot-Engine, a fully open-source pipeline for procedural data generation across robots, tasks, and diverse simulated environments in MolmoSpaces. With it, we release MolmoBot-Data, a dataset of 1.8 million expert trajectories for articulated object manipulation（操控） and pick-and-place tasks. We train three policy classes: MolmoBot, a Molmo2-based multi-frame vision-language model（视觉-语言模型） with a flow-matching action head; MolmoBot-Pi0, which replicates the $π_0$ architecture to enable direct comparison; and MolmoBot-SPOC, a lightweight policy suitable for edge deployment and amenable to RL fine-tuning. We evaluate on two robotic platforms: the Franka FR3 for tabletop manipulation（操控） tasks and the Rainbow Robotics RB-Y1 mobile manipulator for door opening, drawer manipulation（操控）, cabinet interaction, and mobile pick-and-place. Without any real-world fine-tuning, our policies achieve zero-shot（零样本） transfer to unseen objects and environments. On tabletop pick-and-place, MolmoBot achieves a success rate of 79.2% in real world evaluations across 4 settings, outperforming $π_{0.5}$ at 39.2%. Our results demonstrate that procedural environment generation combined with diverse articulated assets can produce robust manipulation（操控） policies that generalize broadly to the real world. Technical website: https://allenai.github.io/MolmoBot

## 中文简述

提出基于视觉-语言的移动操控方法，具有仿真到真实迁移特点。

**研究方向**: 机器人操控、模仿学习、视觉-语言模型、Flow Matching、仿真到真实迁移

## 关键贡献

1. **MolmoBot-Engine**：基于 MolmoSpaces 的全开源程序化数据生成管线，支持多机器人、多任务、多环境的专家轨迹生成
2. **MolmoBot-Data**：1.7M 专家轨迹数据集（5,704 小时），覆盖 8 种任务类型、94k+ 环境、11k+ 物体、9k+ 容器，涉及 Franka FR3 和 RB-Y1 两种平台
3. **三种策略架构**：
   - MolmoBot：基于 Molmo2-4B VLM + DiT flow-matching action head
   - MolmoBot-Pi0：复现 π0 架构（Paligemma 3B），用于控制变量比较
   - MolmoBot-SPOC：轻量 Transformer 策略，适合边缘部署和 RL 微调
4. **零样本 Sim-to-Real 成果**：无需真实数据微调，在 DROID 桌面 pick-and-place 上 MolmoBot 达 79.2%，超过使用 >10k 小时真实数据训练的 π0.5（39.2%）
5. 全栈开源：数据、生成管线、训练代码、模型权重
## 结构化提取

- Problem: 仿真数据能否单独支撑零样本 Sim-to-Real 操控？当前操控基础模型训练数据和流程封闭，社区无法复现
- Method: 程序化生成大规模仿真专家轨迹（MolmoBot-Engine + MuJoCo + MolmoSpaces），三轴域随机化（环境/动作/相机），三种策略架构（VLM+flow-matching / π0复现 / 轻量Transformer），纯行为克隆训练
- Tasks: Pick, Pick-and-Place, PnP Next-To, PnP Color, Open（抽屉/柜子）, Door Open（桌面 + 移动平台），共 8 种任务类型
- Sensors: RGB 相机（头部、外部、腕部），关节状态（本体感知），无深度
- Robot Setup: Franka FR3（7-DoF + Robotiq 2F-85，固定底座，DROID 配置 15Hz）；Rainbow RB-Y1（全向底盘 + 6-DoF 躯干 + 双 7-DoF 臂）
- Metrics: 成功率（oracle：任意时刻完成 / end-of-episode：最终时刻完成）；真实世界 120 episodes（DROID），仿真 200-1000 episodes/task
- Limitations: 仅刚体和铰接物体；RB-Y1 真实门开启成功率低（2/9）；PnP Next-To 任务弱；不支持软体/DLO；论文消融部分不完整
- Evidence Notes: 真实世界 DROID 结果基于 3 台机器人、4 环境、2 机构，120 episodes 总量，每个任务仅 3 次试验。仿真结果基于 200-1000 episodes，方差更低。MolmoBot-Pi0 控制变量实验证实数据优势独立于架构。RB-Y1 真实世界评估受硬件急停影响较大。
## 本地引用关系

-
## 证据元数据

- Fulltext Quality: partial（HTML 全文在第 5.2 节截断，缺少 5.3 消融分析和第 6 节讨论/结论；通过项目主页和博客补充实验数据）
- Evidence Coverage: high（方法、数据管线、模型架构、主要实验结果完整；消融分析部分缺失）
- Confidence: high
- Summary: 基于 MolmoSpaces 生成 1.7M 仿真专家轨迹，训练三种策略架构（VLM+flow-matching、π0 复现、轻量 Transformer），在 Franka FR3 和 RB-Y1 上实现零样本 Sim-to-Real，桌面 pick-and-place 达 79.2% 超过 π0.5 的 39.2%


## Problem

机器人操控领域的主流观点认为：**仿真数据不足以单独支撑真实世界操控**，必须结合真实数据收集或任务特定微调来弥合 Sim-to-Real gap。同时，当前最强操控基础模型（GR00T、π0/π0.5、Gemini Robotics）的训练数据、配方和流程大多封闭，仅集中在少数资源充足的工业实验室。

本文的核心问题：**当仿真数据在规模和多样性上足够大时，能否实现零样本 Sim-to-Real 迁移？** 即不使用任何真实数据、不使用光追渲染、不做显式域适应，仅靠仿真数据训练的策略能否在真实世界中工作？


## Method

### 数据生成管线（MolmoBot-Engine）

- **基础平台**：MolmoSpaces（232k 程序化生成室内环境，48k 可操作物体）
- **仿真器**：MuJoCo（非光追渲染），强调**多样性优于逼真度**
- **物体来源**：iTHOR + Objaverse，按可抓取尺寸和水密碰撞网格过滤
- **域随机化**（三大轴）：
  1. **环境随机化**：光照（数量、位置、强度、颜色）、纹理（程序化 + 真实纹理图）、动力学（摩擦系数、质量、关节阻尼）
  2. **动作随机化**：初始关节配置随机化
  3. **相机随机化**：大幅随机化相机位姿（策略甚至能处理对抗性相机移动）
- **专家轨迹生成**：基于 Task-and-Motion Planning (TAMP)，在程序化环境中生成最短路径专家
- **数据生成效率**：100 块 A100 GPU，约 660 episodes/GPU-hour，全量数据集约 6,500 GPU-hours，相当于实时收集的 2.6 倍吞吐量

### 机器人平台

- **Franka FR3**：7-DoF + Robotiq 2F-85 夹爪，固定底座（0.58m），DROID 配置，15Hz
- **Rainbow RB-Y1**：全向底盘（3-DoF）+ 6-DoF 躯干 + 2-DoF 头部 + 双 7-DoF 臂，双平行夹爪

### MolmoBot 架构

- **视觉编码器**：SigLIP2（冻结），图像 patch token 通过多头注意力池化为 192 token
- **语言模型**：Molmo2-4B，双向注意力（视觉 token）+ 因果注意力（文本 token），支持多帧输入（F=2 或 F=3）
- **Action Head**：DiT（Diffusion Transformer），通过交叉注意力从 LLM 各层获取特征，flow-matching 迭代去噪生成动作 chunk
- **输入**：多相机 RGB 图像（头部、外部、腕部）+ 语言指令 + 可选 2D 点坐标
- **训练**：仅训练 action head 和 LLM，视觉编码器和投影层冻结

### MolmoBot-Pi0

- 与 π0 完全相同架构：Paligemma 3B + flow-matching action expert
- 使用 openpi 代码库训练，200k steps，batch size 1024，lr 5e-5
- 目的：控制架构变量，纯数据效果对比

### MolmoBot-SPOC

- 基于 SPOC 导航架构改造
- SigLIP2-Base patch 16/256 编码器（保留全部 patch token）
- 动作预测：分类问题，连续动作通过分位数分箱量化为 256 bins
- 不依赖轨迹历史，仅用当前步观测
- 轻量级，适合 RL fine-tuning


## Experiments

### 真实世界 DROID 评估（Franka FR3）

- **设置**：3 台物理 DROID 机器人，4 个环境（Workroom/Kitchen/Bedroom/Office），跨 2 个机构，40 个 pick-and-place 任务，每个 3 次试验，共 120 episodes
- **主要结果**：

| Policy | 总体成功率 |
|--------|-----------|
| π0-DROID | ~13% |
| π0.5-DROID | 39.2% |
| MolmoBot-Pi0 | 46.7% |
| MolmoBot-Img | ~72% |
| **MolmoBot (F=2)** | **79.2%** |

- 关键发现：MolmoBot-Pi0（用 π0 架构但纯仿真数据训练）甚至超过了用真实数据训练的 π0.5，说明**数据质量/多样性比架构更重要**

### 真实世界 RB-Y1 移动操控

- 门开启任务：3 扇不同的拉门，9 次试验
  - 4/9 抓取成功，2/9 门打开成功
  - 主要失败原因：硬件急停（e-stop）、右侧门把手数据不足、碰撞
- 这是 RB-Y1 平台上**首个通用 pick-and-place 和铰接物体操控策略**

### 仿真评估

| Model | Pick MSProc | Pick Classic | Pick | Pick Rand-Cam | Pick&Place | PnP Next-To | PnP Color | Avg |
|-------|-----------|-----------|------|-----------|-----------|-----------|-----------|-----|
| π0.5-Finetune | 48.0 | 28.3 | 25.8 | 29.7 | 43.5 | 28.4 | 48.3 | 36.0 |
| MolmoBot-Pi0 | 66.2 | 35.7 | 33.3 | 39.8 | 44.7 | 24.7 | 46.2 | 41.5 |
| MolmoBot-Img | 92.2 | 63.5 | 61.4 | 62.1 | 63.0 | 21.0 | 67.8 | 61.6 |
| **MolmoBot (F=2)** | **93.5** | **66.8** | **64.0** | **63.7** | **66.4** | **26.4** | **67.8** | **64.1** |

- MolmoBot 在所有仿真任务上均大幅领先基线
- PnP Next-To 任务表现最低（26.4%），暗示空间关系推理仍有挑战

### RB-Y1 仿真评估

| Model | Pick | Pick&Place | Open | Door Open |
|-------|------|-----------|------|-----------|
| MolmoBot Multitask | 44.8% | 22.5% | 25.2% | 70.2% |
| MolmoBot Door Specialist | — | — | — | 77.7% |

### 消融分析

- （注：HTML 版本第 5.3 节消融分析被截断，以下为从结果表中推断的部分消融）
- **多帧 vs 单帧**：MolmoBot (F=2) 64.1% > MolmoBot (F=3) 62.4% > MolmoBot-Img（单帧）61.6%
- **架构 vs 数据**：MolmoBot-Pi0（同 π0 架构 + 仿真数据）41.5% 远超 π0.5-Finetune 36.0%，说明数据优势独立于架构
- **数据规模**：论文声明消融验证了数据规模和多样性的重要性（细节缺失）


## Limitations

1. **任务范围有限**：仅支持刚体和铰接物体操控（pick/pick-and-place/门/抽屉/柜子开启），不支持软体、可变形物体（DLO）、精细接触操控
2. **RB-Y1 真实世界效果有限**：门开启成功率仅 2/9，硬件兼容性和数据覆盖不足（如右侧把手配置）
3. **仿真器局限性**：MuJoCo 的物理模拟能力制约了可生成数据的任务类型
4. **PnP Next-To 任务表现差**：空间关系推理（"放在旁边"）成功率仅 26.4%，暗示语言-空间理解仍有不足
5. **消融分析不完整**：无法从当前可获取的论文版本中完整评估各设计选择的贡献
6. **评估协议**：真实世界评估每个任务仅 3 次试验，置信区间较大


## Key Takeaways

### 对 DLO 操控的启示
- **多样性 > 逼真度**：仿真数据的关键不在于渲染质量，而在于环境、物体、相机、动力学的多样性——这一原则可能也适用于 DLO 仿真（如多样化绳索属性、环境配置）
- **域随机化策略**：光照、纹理、摩擦系数、质量的随机化是 Sim-to-Real 的核心，DLO 仿真中可推广到弯曲刚度、阻尼、质量密度等参数
- **数据生成效率**：仿真数据生成速度是人工遥操作的 2.6 倍，对于需要大量数据的 DLO 操控学习有吸引力
- **当前局限**：MolmoBot-Engine 明确声明不支持软体/可变形物体，这意味着 DLO 需要新的仿真管线（如 SoftGym、PlasticineLab）

### 对 VLM-based 控制的启示
- **VLM + Flow Matching 有效**：MolmoBot 的核心架构（VLM backbone + DiT flow-matching action head）是当前 VLA 的主流范式
- **多帧输入有帮助但边际递减**：F=2 优于 F=3，说明 2 帧已足够捕捉运动趋势
- **轻量策略也有竞争力**：SPOC 架构用分类替代 flow-matching，参数少但仍有不错表现，适合实时控制
- **纯仿真训练可行**：首次大规模验证了 VLA 完全在仿真数据上训练可以达到或超过真实数据训练的效果

### 方法论启示
- **开放性**：全栈开源（数据、管线、训练代码、模型）为社区提供了可复现的研究基础
- **跨平台泛化**：同一数据管线支持桌面和移动操控平台，展示了方法的通用性
- **评估标准化**：使用 DROID 标准配置进行公平比较

## 相关概念

- [[robotic-manipulation]]
- [[imitation-learning]]
- [[vision-language-model]]
- [[flow-matching]]
- [[sim-to-real]]
- [[deformable-linear-object]]
- [[grasping]]

## 相关研究者

- [[deshpande|Deshpande, Abhay]]
- [[jauhri|Jauhri, Snehal]]
