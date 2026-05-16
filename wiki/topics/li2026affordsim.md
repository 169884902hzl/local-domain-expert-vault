---
title: "AffordSim: A Scalable Data Generator and Benchmark for Affordance-Aware Robotic Manipulation"
tags: [manipulation, imitation, VLM, RL, diffusion]
created: "2026-05-07"
updated: "2026-05-07"
type: "literature"
status: "done"
summary: "首个将开放词汇 3D 可供性预测（VoxAfford）集成到机器人操控数据生成管线的仿真框架，含 50 任务 benchmark 和 4 种 IL baseline 评测，揭示可供性需求高的任务（倒水、挂杯）仍是当前方法的关键瓶颈。"
authors: "Li, Mingyang; Xu, Haofan; Sun, Haowen; Chen, Xinzhe; Ren, Sihua et al."
year: "2026"
venue: "arXiv Preprint"
zotero_key: "HFD7AG6E"
---
## 摘要

Simulation-based data generation has become a dominant paradigm for training robotic manipulation（机器人操控） policies, yet existing platforms do not incorporate object affordance（可供性） information into trajectory generation. As a result, tasks requiring precise interaction with specific functional regions--grasping（抓取） a mug by its handle, pouring from a cup's rim, or hanging a mug on a hook--cannot be automatically generated with semantically correct trajectories. We introduce AffordSim, the first simulation framework that integrates open-vocabulary 3D affordance（可供性） prediction into the manipulation（操控） data generation pipeline. AffordSim uses our VoxAfford model, an open-vocabulary 3D affordance（可供性） detector that enhances MLLM output tokens with multi-scale geometric features, to predict affordance（可供性） maps on object point clouds, guiding grasp pose estimation toward task-relevant functional regions. Built on NVIDIA Isaac Sim with cross-embodiment（具身） support (Franka FR3, Panda, UR5e, Kinova), VLM-powered task generation, and novel domain randomization using DA3-based 3D Gaussian reconstruction from real photographs, AffordSim enables automated, scalable generation of affordance（可供性）-aware manipulation（操控） data. We establish a benchmark of 50 tasks across 7 categories (grasping（抓取）, placing, stacking, pushing/pulling, pouring, mug hanging, long-horizon（长时序） composite) and evaluate 4 imitation learning（模仿学习） baselines (BC, Diffusion Policy（扩散策略）, ACT, Pi 0.5). Our results reveal that while grasping（抓取） is largely solved (53-93% success), affordance（可供性）-demanding tasks such as pouring into narrow containers (1-43%) and mug hanging (0-47%) remain significantly more challenging for current imitation learning（模仿学习） methods, highlighting the need for affordance（可供性）-aware data generation. Zero-shot（零样本） sim-to-real（仿真到真实迁移） experiments on a real Franka FR3 validate the transferability of the generated data.

## 中文简述

提出基于扩散策略的抓取方法，具有仿真到真实迁移特点。

**研究方向**: 机器人操控、模仿学习、视觉-语言模型、强化学习、扩散模型

## 关键贡献

1. **首个可供性感知的仿真数据生成框架**：将开放词汇 3D 可供性预测（VoxAfford）集成到轨迹生成管线中，实现自动化的可供性引导抓取姿态估计和运动规划。
2. **VoxAfford 可供性引导抓取选择**：通过多尺度几何特征增强 MLLM 输出 token，在点云上预测可供性热图，结合运动学可行性联合评分选择最优抓取。
3. **VLM 驱动的自动化任务-场景生成**：自然语言任务描述自动转换为仿真场景，支持 4 种机器人平台（Franka FR3、Panda、UR5e、Kinova），无需任务特定工程。
4. **DA3 3D Gaussian 重建的真实背景域随机化**：5 轴域随机化（背景纹理、光照、物体纹理、物体位姿、DA3 Gaussian 背景），用真实照片重建的场景作为背景渲染。
5. **50 任务 benchmark 跨 7 类操控**：grasping、placing、stacking、pushing/pulling、pouring、mug hanging、long-horizon composite，评测 4 种 IL 方法。
6. **关键发现**：grasping 任务基本解决（53-93%），但可供性需求高的任务（倒水入窄容器 1-43%，挂杯 0-47%）仍是核心挑战，揭示了"可供性复杂度"作为缺失的评测维度。
## 结构化提取

- **Problem**: 现有仿真平台不考虑物体可供性信息，无法自动生成可供性需求高的操控任务（倒水、挂杯）的语义正确轨迹
- **Method**: VoxAfford（开放词汇 3D 可供性检测）集成到 Isaac Sim 数据生成管线；可供性引导抓取姿态估计 + cuRobo 运动规划；VLM 自动任务-场景生成；DA3 3D Gaussian 域随机化
- **Tasks**: 50 任务跨 7 类（grasping/placing/stacking/push-pull/pouring/mug-hanging/long-horizon composite）
- **Sensors**: 双目 RGB-D（腕部 + 第三人称视角，256×256），7-DOF 本体感知
- **Robot Setup**: Franka FR3, Franka Panda, UR5e, Kinova；单臂桌面场景；Franka Hand 夹爪
- **Metrics**: 任务成功率（SR），子任务成功率；30 rollouts/task（仿真），10 trials/task（真实）
- **Limitations**: 仅刚体；VoxAfford 对非标准可供性覆盖不足；无灵巧/双臂操控；DA3 需真实照片
- **Evidence Notes**:

  - 4 种 IL baseline 在 17 代表性任务上的完整成功率数据（Table 1）
  - 可供性集成消融：Manual 87% vs AnyGrasp 20% vs VoxAfford 61% vs Oracle 92%（Table 2）
  - 跨 4 种机器人平台轨迹生成成功率 83-95%
  - 零样本 sim-to-real：Pi 0.5 在 6 类任务上 10-60%（Table 3）
  - 域随机化使 Pi 0.5 从 17% 提升到 27%，在新场景保持一致性能（Table 4）
## 本地引用关系

-
## 证据元数据

- Fulltext Quality: fulltext
- Evidence Coverage: complete（含正文、表格、附录）
- Confidence: high
- Summary: 首个将开放词汇 3D 可供性预测（VoxAfford）集成到机器人操控数据生成管线的仿真框架，含 50 任务 benchmark 和 4 种 IL baseline 评测，揭示可供性需求高的任务（倒水、挂杯）仍是当前方法的关键瓶颈。


## Problem

现有仿真数据生成平台（RoboTwin、RoboCasa、ManiSkill2 等）在生成操控轨迹时不考虑物体的可供性（affordance）信息。对于需要与物体特定功能区域精确交互的任务（如握杯把倒水、将马克杯挂在钩子上），现有方法要么依赖人工设计抓取姿态（不可扩展），要么使用通用抓取估计（如 AnyGrasp）忽略任务语义，导致功能错误（如抓杯身而非杯把）。这使得可供性需求高的任务无法自动生成语义正确的轨迹。


## Method

### 核心架构
AffordSim 管线包含 5 个阶段：
1. **VLM 场景生成**：自然语言任务描述 → VLM → 场景配置（物体、位姿、机器人、目标条件）
2. **点云获取**：从仿真场景捕获目标物体点云 P ∈ ℝ^{N×3}
3. **VoxAfford 可供性预测**：预测可供性热图 A: P → [0,1]，为每个表面点生成可供性得分
4. **可供性引导抓取选择**：在可供性峰值区域采样多个接近方向，生成候选抓取集合，联合评分选择最优抓取
5. **运动规划 + 域随机化**：cuRobo GPU 加速运动规划，生成观测-动作轨迹对

### VoxAfford 可供性检测
- 基于冻结 3D VQVAE 编码器的多尺度几何特征，通过交叉注意力注入 MLLM 输出 token
- 开放词汇设定：接受任意自然语言可供性查询（如"graspable handle"、"pourable rim"）
- 跨物体类别泛化，无需任务特定微调

### 可供性引导抓取评分
联合评分函数：s_k = s_k^{aff} · s_k^{kin}
- s_k^{aff}：抓取接触区域的平均可供性值
- s_k^{kin} = f(g_k, q)：运动学可行性和无碰撞评估
- 最终选择 g* = argmax s_k

### 域随机化（5 轴）
1. 背景纹理随机化
2. 光照随机化（数量、位置、强度、颜色）
3. 物体 PBR 材质随机化（反照率、粗糙度、金属度）
4. 物体位姿扰动
5. **DA3 3D Gaussian 背景**：从 10-20 张真实照片重建高斯场，渲染任意视角的逼真背景


## Experiments

### Benchmark 评测（Table 1，17 个代表性任务）

| Category | Task | BC | ACT | DP | Pi 0.5 |
|----------|------|-----|-----|-----|--------|
| Grasping | pick_banana | 53 | 63 | 87 | **93** |
| Grasping | pick_red_cup | 17 | **77** | 63 | 80 |
| Placing | pick_banana_place_plate | 37 | 60 | 84 | **93** |
| Placing | pick_cup_place_shelf | 5 | 7 | 3 | **47** |
| Placing | pick_kettle_place_coffee_machine | 27 | 43 | 49 | **65** |
| Stacking | stack_two_blocks | 30 | 43 | 47 | **77** |
| Stacking | stack_three_blocks | 13 | 27 | 28 | **53** |
| Push/Pull | push_box_to_target | 23 | 63 | 67 | **78** |
| Push/Pull | pull_drawer_open | 37 | 53 | 58 | **86** |
| Pouring | pour_basket_into_bowl | 20 | 86 | 94 | **99** |
| Pouring | pour_pan_into_bowl | 7 | 33 | **87** | 92 |
| Pouring | pour_cup_into_bowl | 1 | 24 | 36 | **43** |
| Mug Hanging | hang_mug_on_rack | 0 | 10 | 17 | **47** |
| Mug Hanging | hang_mug_on_hook | 0 | 7 | 13 | **33** |
| Long Horizon | pick_cup_pour_place_coffee_machine | 0 | 3 | 8 | **16** |
| Long Horizon | pick_cup_pour_hang_on_rack | 0 | 1 | 3 | **21** |
| Long Horizon | open_microwave_place_can | 0 | 0 | 2 | **13** |
| **Average** | | **16** | **35** | **44** | **61** |

- 所有方法在 grasping 上表现最好（53-93%）
- 可供性需求高的任务性能骤降：pouring（窄容器 1-43%）、mug hanging（0-47%）
- Pi 0.5 全面最优（61% 均值），DP（44%）、ACT（35%）、BC（16%）

### 跨平台评测
4 种机器人轨迹生成成功率：Franka FR3 94%、Panda 92%、UR5e 83%、Kinova 95%。UR5e 因 6-DOF 限制在方向敏感任务上较低。

### 可供性集成消融（Table 2）
| 策略 | 成功率 |
|------|--------|
| Manual（人工设计） | 87% |
| AnyGrasp（通用抓取） | 20% |
| **VoxAfford（本文）** | **61%** |
| Human Aff.（oracle） | 92% |

- VoxAfford 大幅超越 AnyGrasp（倒水任务：80%/63% vs 20%/0%）
- Mug hanging 任务 VoxAfford 仅 10-17%，因训练数据缺乏挂杯相关可供性
- Oracle 上限 92%，差距主要来自 VoxAfford 训练覆盖不足

### Zero-shot Sim-to-Real（Table 3）
在真实 Franka FR3 上评测 Pi 0.5：
- Grasping: 60%
- Placing: 30%
- Push/Pull: 40%
- Stacking: 20%
- Pouring: 20%
- Mug Hanging: 10%
- 真实世界成功率与仿真中的可供性复杂度梯度一致

### 域随机化鲁棒性（Table 4）
- 无 DR 训练：DP 3%、Pi 0.5 17%（标准场景）
- 有 DR 训练：Pi 0.5 提升到 27%
- DR 训练的策略在新场景（不同桌布、背景物体）下保持一致性能


## Limitations

1. **VoxAfford 预测精度限制**：对几何异常物体（薄工具手柄、透明物体）、遮挡严重场景、功能区域模糊的对称容器预测精度下降。
2. **仅限刚体操控**：不支持可变形物体（布料、绳索、面团），需要不同的仿真后端和可供性表示。
3. **无灵巧手内操控和双臂任务**：未覆盖 in-hand manipulation 和 bimanual tasks。
4. **DA3 背景重建需要真实照片**：每个工作空间需 10-20 张照片的一次性采集，限制了快速迁移到新环境的能力。
5. **VoxAfford 训练覆盖不足**：对非标准可供性（如挂杯需要抓杯身而非杯把）缺乏训练数据，导致 mug hanging 任务表现差（10-17%）。


## Key Takeaways

1. **可供性是操控数据生成的关键缺失维度**：当前仿真平台不考虑物体功能区域，导致可供性需求高的任务（倒水、挂杯）成功率极低。这对 DLO 操控也有启发——线缆等可变形物体同样有功能区域（如端点、连接点），需要类似的感知引导。
2. **开放词汇可供性检测是可行方向**：VoxAfford 通过 MLLM + 几何特征融合实现跨类别泛化，避免了逐物体标注。这种范式可推广到 DLO 的功能性区域检测。
3. **IL 方法能力分层明显**：Pi 0.5 >> DP > ACT >> BC，预训练 VLA 模型在复杂操控任务上有显著优势。选择 VLM-based 控制架构是正确的方向。
4. **可供性复杂度是新评测维度**：论文揭示抓取已基本解决（53-93%），但精确功能交互仍是开放问题。这一发现对 benchmark 设计有指导意义。
5. **Sim-to-Real 可行但仍有差距**：零样本迁移成功验证了管线有效性，但高可供性任务真实世界成功率低（mug hanging 10%），说明仅靠数据增强不够，需要更好的可供性推理能力。

## 相关概念

- [[robotic-manipulation]]
- [[imitation-learning]]
- [[vision-language-model]]
- [[reinforcement-learning]]
- [[diffusion-model]]
- [[deformable-linear-object]]
- [[bimanual-manipulation]]
- [[grasping]]

## 相关研究者

- [[li-mingyang|Li, Mingyang]]
- [[xu-haofan|Xu, Haofan]]
