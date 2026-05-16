---
title: "Learning Coordinated Bimanual Manipulation Policies Using State Diffusion and Inverse Dynamics Models"
tags: [manipulation, imitation, diffusion]
created: "2026-04-25"
updated: "2026-04-25"
type: "literature"
status: "done"
summary: "将模仿学习分解为状态预测扩散模型和逆动力学模型两步，通过预测物体未来状态来指导双臂协调动作生成，在 Push-L（79.3% SR）、衣物清理（15/15 p1）、水果持握、杂乱货架拾取等双臂任务上显著优于 Diffusion Policy"
authors: "Chen, Haonan; Xu, Jiaming; Sheng, Lily; Ji, Tianchen; Liu, Shuijing et al."
year: "2025"
venue: "2025 IEEE International Conference on Robotics and Automation (ICRA)"
zotero_key: "ALKJ64N7"
---
## 摘要

When performing tasks like laundry, humans naturally coordinate both hands to manipulate objects and anticipate how their actions will change the state of the clothes. However, achieving such coordination in robotics remains challenging due to the need to model object movement, predict future states, and generate precise bimanual（双臂） actions. In this work, we address these challenges by infusing the predictive nature of human manipulation（操控） strategies into robot imitation learning（模仿学习）. Speciﬁcally, we disentangle task-related state transitions from agent-speciﬁc inverse dynamics（逆动力学） modeling to enable effective bimanual（双臂） coordination. Using a demonstration（示范数据） dataset, we train a diffusion model（扩散模型） to predict future states given historical observations, envisioning how the scene evolves. Then, we use an inverse dynamics（逆动力学） model to compute robot actions that achieve the predicted states. Our key insight is that modeling object movement can help learning policies for bimanual（双臂） coordination manipulation（操控） tasks. Evaluating our framework across diverse simulation and real-world manipulation（操控） setups, including multimodal（多模态） goal conﬁgurations, bimanual manipulation（双臂操控）, deformable objects, and multi-object setups, we ﬁnd that it consistently outperforms state-of-the-art（现有最优方法） state-to-action mapping policies. Our method demonstrates a remarkable capacity to navigate multimodal（多模态） goal conﬁgurations and action distributions, maintain stability across different control modes, and synthesize a broader range of behaviors than those present in the demonstration（示范数据） dataset.

## 中文简述

提出基于扩散模型的双臂方法。

**研究方向**: 机器人操控、模仿学习、扩散模型

## 证据元数据

- **Fulltext Quality**: fulltext
- **Evidence Coverage**: 读取了全文，包括 abstract、introduction、related work、method (Sec III)、simulation experiments (Sec IV)、real-world experiments (Sec V)、tables (I-IV)、figures (1-7)、conclusion
- **Confidence**: high — 全文完整，仿真+真实实验充分，消融实验详尽
- **Summary**: 将模仿学习分解为状态预测扩散模型和逆动力学模型两步，通过预测物体未来状态来指导双臂协调动作生成，在 Push-L（79.3% SR）、衣物清理（15/15 p1）、水果持握、杂乱货架拾取等双臂任务上显著优于 Diffusion Policy
## 关键贡献

1. 提出将模仿学习分解为扩散状态预测模型 + 逆动力学模型的新框架
2. 通过显式建模物体运动（而非直接 action 映射），更好地捕获双臂协调失败
3. 在仿真（Block Push、Franka Kitchen、Push-L）和真实世界（洗衣、水果、货架）全面验证
## 结构化提取

- **Problem**: 双臂协调操控中端到端 action 映射难以处理多模态目标和协调失败检测
- **Method**: 状态预测扩散模型 + 逆动力学模型，分解式模仿学习框架
- **Tasks**: Push-L（推 L 型块）、Laundry Cleanup（枕头移篮）、Fruit Holding（双臂持果）、Cluttered Shelf Picking（货架拾取）
- **Sensors**: 点云（3D 任务）、关键点位姿（Push-L）、RGB（可选）
- **Robot Setup**: 双臂 UR5e（Gello 遥操作采集），圆形末端执行器（Push-L）
- **Metrics**: 成功率、p1-p5（完成任务数）、IoU
- **Limitations**: 训练慢、数据收集耗时、状态空间大
- **Evidence Notes**: 全文读取，Table I-IV + Fig 4-6 提供定量对比，Push-L sim-to-real + 3 个真实双臂任务
## 本地引用关系

- [[chen2025deformpam]]
- [[lee2025diffdagger]]
- [[scheikl620movement]]
- [[wu2025discrete]]
## Problem

双臂协调操控任务中，端到端 state-to-action 映射难以处理多模态目标配置和未见交互。物体掉落时 action loss 小但 state loss 大，导致协调失败被掩盖。


## Method

- **State Diffusion Model**：DDPM 变体，输入历史 Ts 步状态序列，预测未来 Tp 步世界状态
- **Inverse Dynamics Model**：MLP，输入历史 Th 步 + 未来 Tf 步状态，输出当前动作
- **联合训练**：L = β·L_pred + (1-β)·L_InvDyn
- **关键洞察**：建模物体状态 > 直接建模动作，因为物体掉落的 state loss 远大于 action loss


## Experiments

- **仿真**：Block Push（XArm）、Franka Kitchen（7 任务）、Push-L（长时序多阶段）
- **真实**：Push-L 零样本 sim-to-real（9/12 vs IDP 2/12）、Laundry Cleanup（双 UR5e，p1=15/15）、Fruit Holding（p4=8/15 vs 5/15）、Cluttered Shelf Picking（14/15 vs 5/15）
- **数据效率**：100 demos 时 SR=0.32 vs IDP 0.17
- **消融**：去掉逆动力学模型 SR 从 79.3% 降至 61.3%


## Limitations

1. 状态空间大于动作空间，训练时间更长
2. 真实世界数据收集耗时
3. 200 demonstrations/任务


## Key Takeaways

- 状态预测 + 逆动力学的分解式架构优于端到端动作预测
- 物体状态建模是双臂协调的关键信号
- 在多模态目标配置下表现稳定
- 能综合出超越训练数据范围的行为

## 相关概念

- [[robotic-manipulation]]
- [[imitation-learning]]
- [[diffusion-model]]
- [[vision-language-model]]
- [[deformable-linear-object]]
- [[bimanual-manipulation]]

## 相关研究者

- [[chen-haonan|Chen, Haonan]]
