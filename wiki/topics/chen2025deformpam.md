---
title: "DeformPAM: Data-efficient learning for long-horizon deformable object manipulation via preference-based action alignment"
tags: [manipulation, imitation, diffusion]
created: "2026-04-25"
updated: "2026-04-25"
type: "literature"
status: "done"
summary: "提出 DeformPAM 框架，通过偏好学习训练隐式 reward 模型，在推理时对扩散策略采样的多个候选动作进行 reward-guided 选择，在颗粒堆塑形、绳子塑形、T恤展开三个可变形物体长时序任务上显著提升质量"
authors: "Chen, Wendi; Xue, Han; Zhou, Fangyuan; Fang, Yuan; Lu, Cewu"
year: "2025"
venue: "arXiv Preprint"
zotero_key: "ULDP9XLR"
---
## 摘要

In recent years, imitation learning（模仿学习） has made progress in the field of robotic manipulation（机器人操控）. However, it still faces challenges when addressing complex long-horizon（长时序） tasks with deformable objects, such as high-dimensional state spaces, complex dynamics, and multimodal（多模态） action distributions. Traditional imitation learning（模仿学习） methods often require a large amount of data and encounter distributional shifts and accumulative errors in these tasks. To address these issues, we propose a data-efficient（数据高效） general learning framework (DeformPAM) based on preference learning and reward（奖励）-guided action selection. DeformPAM decomposes long-horizon（长时序） tasks into multiple action primitives, utilizes 3D point cloud（点云） inputs and diffusion（扩散） models to model action distributions, and trains an implicit reward（奖励） model using human preference data. During the inference phase, the reward（奖励） model scores multiple candidate actions, selecting the optimal action for execution, thereby reducing the occurrence of anomalous actions and improving task completion quality. Experiments conducted on three challenging real-world long-horizon（长时序） deformable object（可变形物体） manipulation（操控） tasks demonstrate the effectiveness of this method. Results show that DeformPAM improves both task completion quality and efficiency compared to baseline methods even with limited data. Code and data will be available at deform-pam.robotflow.ai.

## 中文简述

提出基于扩散模型的操控方法，具有长时序任务特点。

**研究方向**: 机器人操控、模仿学习、扩散模型

## 证据元数据

- **Fulltext Quality**: fulltext
- **Evidence Coverage**: 读取了全文，包括 abstract、introduction、related work、method (Sec III-IV)、experiments (Sec V)、figures (1-6)、tables (I)、conclusion
- **Confidence**: high — 全文完整，三个真实世界长时序任务验证充分
- **Summary**: 提出 DeformPAM 框架，通过偏好学习训练隐式 reward 模型，在推理时对扩散策略采样的多个候选动作进行 reward-guided 选择，在颗粒堆塑形、绳子塑形、T恤展开三个可变形物体长时序任务上显著提升质量
## 关键贡献

1. 设计基于偏好学习和 reward 引导动作选择的通用框架 DeformPAM
2. 利用 DPO 从人类偏好数据学习隐式 reward 模型（而非显式 reward 或直接微调策略）
3. 提出 Reward-guided Action Selection (RAS)：推理时采样 N 个动作，用隐式 reward 选最优
4. 在颗粒/1D/2D 三类可变形物体的长时序任务上验证
## 结构化提取

- **Problem**: 长时序可变形物体操控中的分布偏移和累积误差
- **Method**: DeformPAM — 扩散策略 + DPO 偏好学习 + 隐式 reward 引导动作选择
- **Tasks**: 颗粒堆塑形（T字形）、绳子塑形（圆形）、T恤展开
- **Sensors**: RGB-D 相机（3D 点云输入）、Grounded SAM 分割
- **Robot Setup**: Flexiv Rizon 4 双臂 + DH-Robotics PGC-50-35 夹爪
- **Metrics**: IoU、Coverage、Earth Mover's Distance (EMD)
- **Limitations**: 需人类偏好标注、仅预定义原语、DPO 遗忘
- **Evidence Notes**: 全文读取，Fig 4 提供逐步质量曲线，Fig 5-6 提供消融和热图
## 本地引用关系

- [[chen2025coordinated]]
- [[gao2024prime]]
- [[lee2025diffdagger]]
- [[li2025routing]]
- [[scheikl620movement]]
## Problem

长时序可变形物体操控中，模仿学习面临高维状态空间、复杂动力学和多模态动作分布。传统方法需要大量数据且易受分布偏移和累积误差影响。


## Method

三阶段流程：
1. **监督学习**：收集少量演示，用扩散模型训练原始动作原语策略（ResUNet3D + Transformer + Diffusion Head）
2. **偏好学习**：用原始策略 rollout，记录 N 个候选动作，人类排序标注偏好 → DPO 微调 → 提取隐式 reward
3. **推理**：原始策略采样 N=8 动作 → 隐式 reward 打分 → 选最高分执行

关键技术：
- 并行推理：一次 forward 生成 N 个候选动作
- 高效偏好标注：排序式标注 + 笛卡尔积生成偏好对
- 隐式 reward：r(a,P) = -E[‖ε-ε_PL‖² - ‖ε-ε_SL‖²]（DPO 隐式 reward）


## Experiments

- **任务**：颗粒堆塑形（T字形）、绳子塑形（圆形）、T恤展开（平整）
- **硬件**：Flexiv Rizon 4 双臂 + DH-Robotics 夹爪 + 3D 相机
- **数据量**：~30-90 序列/任务（远少于 Diffusion Policy 的数千帧）
- **关键结果**：
  - DeformPAM 在三个任务上均优于 SL、SL+SL、DPO+RAS、Explicit RAS
  - 隐式 RAS 优于显式 RAS（避免 reward 过拟合）
  - 直接用 DPO 微调的策略因遗忘问题表现更差
  - N=8 采样 + RAS 显著提升覆盖率（T恤 0.82→0.85+）


## Limitations

1. 需要人类偏好标注（虽然量不大）
2. 仅验证了预定义动作原语（sweep、pick-place、fling）
3. DPO 微调可能导致遗忘
4. 未探索更多复杂任务


## Key Takeaways

- RAS（reward-guided action selection）是比直接策略微调更稳健的利用偏好数据的方式
- 隐式 reward 模型比显式 reward 模型更抗过拟合
- 动作原语分解降低长时序任务的 horizon 长度
- 从扩散模型隐式提取 reward 是一个巧妙的技术

## 相关概念

- [[robotic-manipulation]]
- [[imitation-learning]]
- [[diffusion-model]]
- [[vision-language-model]]
- [[deformable-linear-object]]
- [[bimanual-manipulation]]
- [[grasping]]

## 相关研究者

- [[chen-wendi|Chen, Wendi]]
- [[lu|Lu, Cewu]]
