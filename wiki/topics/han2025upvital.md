---
title: "UpViTaL: Unpaired Visual-Tactile Self-Supervised Representation Learning for Dexterous Robotic Manipulation"
tags: [manipulation, RL]
created: "2026-04-25"
updated: "2026-04-25"
type: "literature"
status: "done"
summary: "提出 UpViTaL 框架，利用非配对视觉-触觉数据通过自监督表示学习辅助 RL 灵巧操控。核心设计：(1) LSTM 触觉自编码器从时序触觉序列学习触觉表示；(2) MAE 视觉预训练从图像学习视觉表示；(3) 触觉重建误差作为 RL 奖励信号（非输入），实现部署时无需触觉传感器。V-Pretrain-Treward 在 seen 物体上 84.8%、unseen 77.8%，与配对视觉-触觉预训练 SOTA（84.4%/78.2%）相当，比纯视觉预训练提升 30%+"
authors: "Han, Guwen; Liu, Qingtao; Cui, Yu; Chen, Anjun; Chen, Jiming et al."
year: "2025"
venue: "2025 IEEE International Conference on Robotics and Automation (ICRA)"
zotero_key: "94J4QGKQ"
---
## 摘要

Visual and tactile（触觉） pretraining（预训练） have been extensively studied in dexterous（灵巧） robot manipulation（机器人操控） tasks. However, existing methods typically require the simultaneous acquisition of visual and tactile（触觉） data, making it difficult to utilize low-cost, unpaired visual-tactile（触觉） datasets. Moreover, these methods often rely on tactile（触觉） sensors to provide input data for reinforcement learning（强化学习） (RL) during the physical deployment of robotic dexterous（灵巧） hands, which highly increases deployment costs. To address these challenges, we propose UpViTaL, an unpaired visualtactile self-supervised（自监督） representation learning（表征学习） method for RLbased robot dexterous manipulation（灵巧操控）. Specifically, we collect low-cost unpaired visual and tactile（触觉） datasets for manipulation（操控） skill learning using a camera and tactile（触觉） gloves on three robot manipulation（机器人操控） tasks. The temporal tactile（触觉） self-supervised（自监督） representation learning（表征学习） module of UpViTaL is used to explore efficient tactile（触觉） representations from time-series tactile（触觉） data. In parallel, the visual pretraining（预训练） module of UpViTaL helps to extract efficient visual representations from visual data. In addition, we fuse unpaired visual-tactile（触觉） representations through an RL reward（奖励） mechanism, which does not require robotic dexterous（灵巧） hands tactile（触觉） sensors for practical deployment. We validate our approach on three dexterous（灵巧） robot manipulation（机器人操控） tasks. Experimental results demonstrate that UpViTaL can efficiently learn robot manipulation（机器人操控） skills. Compared to existing approaches for visual pretraining（预训练）, our method significantly improves the success rate by more than 30%.

## 中文简述

提出基于强化学习的灵巧手方法，具有自监督特点。

**研究方向**: 机器人操控、强化学习

## 证据元数据

- **Fulltext Quality**: fulltext
- **Evidence Coverage**: 读取了全文，包括 abstract、introduction、related work (Sec II)、method (Sec III)、experiments (Sec IV)、tables (I)、figures (1-5)
- **Confidence**: high — 全文完整，ICRA 2025 正式发表，3 个灵巧操控任务 × seen/unseen 物体系统评估，Shadow Hand 仿真 + 真实实验
- **Summary**: 提出 UpViTaL 框架，利用非配对视觉-触觉数据通过自监督表示学习辅助 RL 灵巧操控。核心设计：(1) LSTM 触觉自编码器从时序触觉序列学习触觉表示；(2) MAE 视觉预训练从图像学习视觉表示；(3) 触觉重建误差作为 RL 奖励信号（非输入），实现部署时无需触觉传感器。V-Pretrain-Treward 在 seen 物体上 84.8%、unseen 77.8%，与配对视觉-触觉预训练 SOTA（84.4%/78.2%）相当，比纯视觉预训练提升 30%+
## 关键贡献

1. 非配对视觉-触觉自监督 RL 框架：视觉和触觉数据独立采集，无需对齐
2. LSTM 时序触觉自编码器：从触觉手套采集的时序触觉序列中学习触觉先验
3. 触觉感知奖励：将触觉重建误差融入 RL 奖励函数，部署时无需触觉传感器输入
4. 与配对方法 SOTA 相当的性能，同时简化数据采集和部署
## 结构化提取

- **Problem**: 配对视觉-触觉数据采集困难和触觉传感器部署成本高
- **Method**: UpViTaL — LSTM 触觉自编码器 + MAE 视觉预训练 + 触觉重建误差奖励 + PPO
- **Tasks**: BottleCap Turning、Faucet Screwing、Lever Sliding
- **Sensors**: RGB 相机 + 20 通道力传感器（仿真）/ 触觉手套（数据采集）
- **Robot Setup**: Shadow Hand 24-DOF（仿真 Isaac Gym + 真实）
- **Metrics**: 成功率（100 次评估 × 4 seeds）
- **Limitations**: 域间隙、任务有限、视觉冻结、真实实验无定量
- **Evidence Notes**: 全文读取，Table I 提供完整 seen/unseen 对比和消融结果
## 本地引用关系

- [[funk2024evetac]]
- [[george2024vital]]
- [[liu2025forcemimic]]
- [[zhao2025polytouch]]
## Problem

现有视觉-触觉预训练方法需要同时采集配对数据，难以利用低成本非配对数据集。且部署时需要触觉传感器作为 RL 输入，增加系统成本和复杂性。


## Method

- **触觉自监督模块 T(θ)**：
  - 输入：500 帧时序触觉序列 X∈{0,1}^{500×20}（20 个传感器，0.2V 二值化）
  - 编码器：2 层 LSTM（256→128），最后一帧隐藏状态作为编码表示
  - 解码器：2 层 LSTM（128→256）+ dense layer 重建输入序列
  - L2 重建损失训练
- **视觉预训练模块 V(θ)**：
  - 基于 MAE（Masked Autoencoder），随机 mask 图像 patches 后重建
  - 冻结视觉编码器提取视觉特征 Fv
- **RL 策略**：PPO 算法，状态 S = {Fv, P}（视觉特征 + 本体感觉）
- **触觉感知奖励**：
  - Rtactile = ‖Tsim - T̂sim‖²（仿真触觉序列经触觉自编码器的重建误差）
  - Ragent = Rjoint + Rdistance（任务进度 + 距离奖励）
  - R = -1·Rtactile + 1·Ragent（α=-1, β=1）
- **数据集**：视觉数据 5 人 2032 序列/182 物体/565k 图像；触觉数据 触觉手套 3 任务/300 序列/150k 帧


## Experiments

- **BottleCap Turning**：seen 85.1% unseen 81.9%（V-Pretrain-Treward）vs VT-JointPretrain 83.7%/81.3%
- **Faucet Screwing**：seen 80.5% unseen 72.4%（V-Pretrain-Treward）vs VT-JointPretrain 80.1%/73.6%
- **Lever Sliding**：seen 88.7% unseen 79.1%（V-Pretrain-Treward）vs VT-JointPretrain 89.3%/79.6%
- **平均**：seen 84.8% unseen 77.8%（vs VT-JointPretrain 84.4%/78.2%）
- **对比视觉预训练**：比 V-Pretrain 提升 30%+（52.2%→84.8% seen）
- **对比无预训练**：比 Base 提升 48%（36.9%→84.8% seen）
- **消融**：LSTM 2 层最优，触觉阈值 1 最优（sim-real 域间隙影响）
- **真实实验**：Shadow Hand 成功完成 3 个任务，验证 sim-to-real 可行性


## Limitations

1. 触觉重建奖励受仿真-真实触觉域间隙影响（需要仔细调节阈值）
2. 仅在 3 个任务上验证（瓶盖旋转、水龙头拧动、杠杆滑动）
3. 视觉编码器在 RL 训练期间冻结，无法在线适应
4. 触觉数据仍需触觉手套采集，虽然不需要配对
5. 真实实验仅展示性质，无定量对比


## Key Takeaways

- 非配对视觉-触觉数据通过奖励函数融合可以逼近配对预训练的效果
- 触觉信息通过奖励信号（而非输入）影响策略，是降低部署成本的有效方案
- LSTM 适合建模时序触觉信号的依赖关系（2 层最优，过深过拟合）
- 重建误差作为奖励本质上提供了"类人操控模式"的引导信号
- 非配对数据策略大幅降低数据采集门槛（可用互联网视频+独立触觉手套数据）

## 相关概念

- [[robotic-manipulation]]
- [[reinforcement-learning]]
- [[tactile-sensing]]
- [[grasping]]

## 相关研究者

- [[han|Han, Guwen]]
