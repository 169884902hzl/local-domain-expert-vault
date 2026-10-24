---
title: "ViViDex: Learning Vision-Based Dexterous Manipulation from Human Videos"
tags: [manipulation, RL, imitation, diffusion]
created: "2026-04-25"
updated: "2026-04-25"
type: "literature"
status: "done"
summary: "提出 ViViDex 框架，从人类视频中提取参考轨迹，用 RL + trajectory-guided reward 训练基于状态的灵巧操控策略，再 rollout 成功轨迹训练统一的基于点云的视觉策略，在三个灵巧操控任务上仅用 1 条视频即超越 DexMV（需 97 条）的效果"
authors: "Chen, Zerui; Chen, Shizhe; Arlaud, Etienne; Laptev, Ivan; Schmid, Cordelia"
year: "2025"
venue: "2025 IEEE International Conference on Robotics and Automation (ICRA)"
zotero_key: "I25NQ6M2"
---
## 摘要

In this work, we aim to learn a unified vision-based policy for multi-fingered robot hands to manipulate a variety of objects in diverse poses. Though prior work has shown benefits of using human videos for policy learning, performance gains have been limited by the noise in estimated trajectories. Moreover, reliance on privileged object information such as ground-truth object states further limits the applicability in realistic scenarios. To address these limitations, we propose a new framework ViViDex to improve vision-based policy learning from human videos. It first uses reinforcement learning（强化学习） with trajectory guided rewards to train state-based policies for each video, obtaining both visually natural and physically plausible trajectories from the video. We then rollout successful episodes from state-based policies and train a unified visual policy without using any privileged information. We propose coordinate transformation to further enhance the visual point cloud（点云） representation, and compare behavior cloning and diffusion policy（扩散策略） for the visual policy training. Experiments both in simulation and on the real robot demonstrate that ViViDex outperforms state-of-theart approaches on three dexterous manipulation（灵巧操控） tasks. Project website: zerchen.github.io/projects/vividex.html.

## 中文简述

提出基于扩散策略的灵巧手方法，具有人类视频学习特点。

**研究方向**: 机器人操控、强化学习、模仿学习、扩散模型

## 证据元数据

- **Fulltext Quality**: fulltext
- **Evidence Coverage**: 读取了全文，包括 abstract、introduction、related work、method (Sec III)、experiments (Sec IV)、tables (I-VI)、figures (1-4)
- **Confidence**: high — 全文完整，三个灵巧操控任务（relocate/pour/place inside）在仿真和真实机器人上验证充分
- **Summary**: 提出 ViViDex 框架，从人类视频中提取参考轨迹，用 RL + trajectory-guided reward 训练基于状态的灵巧操控策略，再 rollout 成功轨迹训练统一的基于点云的视觉策略，在三个灵巧操控任务上仅用 1 条视频即超越 DexMV（需 97 条）的效果
## 关键贡献

1. 提出 ViViDex 框架，三阶段学习：参考轨迹提取 → RL 轨迹引导的状态策略 → 统一视觉策略
2. 设计 trajectory-guided reward，将参考轨迹分为 pre-grasp 和 manipulation 两阶段，分别约束手指和物体运动
3. 提出坐标变换增强点云表示：将世界坐标系的点云变换到目标坐标系和手关节坐标系
4. 对比了 BC 和 3D Diffusion Policy 两种视觉策略训练方式
## 结构化提取

- **Problem**: 从人类视频学习灵巧操控中的轨迹噪声和特权信息依赖问题
- **Method**: ViViDex — 参考轨迹提取 + trajectory-guided RL + 坐标变换增强的统一视觉策略
- **Tasks**: Relocate、Pour、Place Inside（灵巧操控）
- **Sensors**: RGB-D 相机（3D 点云），机器人本体感觉
- **Robot Setup**: Adroit hand (MuJoCo) / Allegro hand + UR5 (SAPIEN/真实)
- **Metrics**: 成功率 SR10、SR3（3cm 阈值）、轨迹误差 Eo/Eh
- **Limitations**: 预定义物体、无臂仿真、真实数据收集依赖 sim 对齐
- **Evidence Notes**: 全文读取，Tables I-VI 提供完整定量结果，含消融和真实实验
## 本地引用关系

- [[chen2025coordinated]]
- [[chen2025vegetable]]
- [[han2025upvital]]
- [[lee2025diffdagger]]
## Problem

从人类视频中学习灵巧操控策略面临两大问题：(1) 估计的轨迹噪声大，直接使用效果差；(2) 现有方法依赖特权信息（物体 CAD 模型/位姿），限制实际应用。


## Method

三阶段流程：
1. **参考轨迹提取**：从 DexYCB 人类视频中用 MANO 估计手姿态，优化 motion retargeting 将人手映射到机器人手
2. **状态策略训练**：PPO + trajectory-guided reward（pre-grasp 阶段约束手指接近轨迹；manipulation 阶段联合约束手指+物体+接触+抬起）；训练时做轨迹增强（随机初始物体位姿/旋转/目标位姿）
3. **视觉策略训练**：rollout 成功的 state-based 策略获取训练数据；将 3D 点云变换到目标坐标系和手指关节坐标系；用 PointNet 提取特征后与本体感觉状态拼接，通过 BC 或 3D Diffusion Policy 预测动作

关键设计：
- Pre-grasp 和 manipulation 两阶段 reward 函数
- 轨迹增强：随机初始位置/旋转/目标位置插值
- 多坐标系点云融合（world + target + palm + fingertips）


## Experiments

- **仿真**：MuJoCo（Adroit hand）+ SAPIEN（Allegro hand + UR5 臂）
- **物体**：5 个 seen YCB 物体 + 10 个 unseen YCB 物体
- **任务**：Relocate（移动物体到目标位姿）、Pour（倒粒子）、Place Inside（将香蕉放入杯中）
- **关键结果**：
  - 状态策略：仅 1 条视频/物体即达 SR10=100%（Adroit），大幅超越 DexMV-DAPG（97 条视频）
  - 视觉策略：3D Diffusion Policy 统一策略 seen 物体 SR3=99%，unseen=50%
  - 坐标变换：目标坐标系使 seen 平均 SR3 从 81%→95%；手指关节坐标系进一步提升至 97%
  - 真实机器人：UR5+Allegro hand，unified diffusion 策略 seen=80%，unseen=68%


## Limitations

1. 依赖 DexYCB 数据集中预定义的物体类型
2. SAPIEN 仿真中灵巧手不带臂（自由移动），不够真实
3. 真实机器人数据收集需要 sim-to-real 对齐特定物体位置
4. Pour 和 Place Inside 任务在真实机器人上未验证


## Key Takeaways

- 将人类视频轨迹作为 RL reward 引导而非直接模仿，可显著降低视频数量需求（97→1）
- 两阶段 reward 设计（pre-grasp + manipulation）是灵巧操控成功的关键
- 坐标变换到目标/手关节坐标系是点云表示的有效增强手段
- 3D Diffusion Policy 比 BC 在统一多物体视觉策略上更鲁棒

## 相关概念

- [[robotic-manipulation]]
- [[reinforcement-learning]]
- [[imitation-learning]]
- [[diffusion-model]]
- [[grasping]]

## 相关研究者

- [[chen-zerui|Chen, Zerui]]
- [[chen|Chen, Shizhe]]
- [[laptev-ivan|Laptev, Ivan]]
- [[schmid|Schmid, Cordelia]]
