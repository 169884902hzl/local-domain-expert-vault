---
title: "Hand-Object Interaction Pretraining from Videos"
tags: [manipulation, RL]
created: "2026-04-25"
updated: "2026-04-25"
type: "literature"
status: "done"
summary: "提出 HOP（Hand-Object interaction Pretraining），从野外视频中学习通用机器人操控先验。方法：(1) MCC-HO + HaMeR 从单目视频提取 3D 手-物体轨迹；(2) Simulator-in-the-loop retargeting：优化器将人类手部关键点映射到机器人关节角度，在 IsaacGym 中验证物理可行性；(3) Transformer (GPT-2) 在约 70K 重定向轨迹上预训练 next-action 预测。微调：RL (PPO) 或 BC 均可。真实 Grasp & Lift 0.65 vs 最佳基线 0.35。仿真 RL 微调 25× 样本效率提升，3× 鲁棒性提升，2× 泛化性提升"
authors: "Singh, Himanshu Gaurav; Loquercio, Antonio; Sferrazza, Carmelo; Wu, Jane; Qi, Haozhi et al."
year: "2025"
venue: "2025 IEEE International Conference on Robotics and Automation (ICRA)"
zotero_key: "BC3J5XAL"
---
## 摘要

We present an approach to learn general robot manipulation（机器人操控） priors from 3D hand-object interaction trajectories. We build a framework to use in-the-wild videos to generate sensorimotor robot trajectories. We do so by lifting both the human hand and the manipulated object in a shared 3D space and retargeting human motions to robot actions. Generative modeling on this data gives us a task-agnostic base policy. This policy captures a general yet flexible manipulation（操控） prior. We empirically demonstrate that finetuning this policy, with both reinforcement learning（强化学习） (RL) and behavior cloning (BC), enables sample-efficient adaptation to downstream tasks and simultaneously improves robustness and generalizability compared to prior approaches. Qualitative experiments are available at: https://hgaurav2k.github.io/hop/.


## 中文简述

提出基于强化学习的操控方法，具有泛化能力特点。

**研究方向**: 机器人操控、强化学习

## 关键贡献

1. Simulator-in-the-loop retargeting：将噪声 3D 手-物体数据转化为高质量机器人轨迹
2. 任务无关操控先验：从非结构化视频中学习的 Transformer 表示
3. RL/BC 双路微调：25× 样本效率提升
4. 手-物体联合先验优于纯手部先验：更鲁棒、更灵活
## 结构化提取

- **Problem**: 从野外视频学习通用机器人操控先验
- **Method**: HOP — 3D 手-物体提取 + Simulator-in-the-loop retargeting + Transformer 预训练
- **Tasks**: Grasp & Drop/Pour/Lift（真实），Grasp & Lift/Throw/Open Cabinet（仿真）
- **Sensors**: Zed-2 立体相机（真实深度），GT 点云（仿真）
- **Robot Setup**: xArm7 + 16-DoF Allegro Hand（IsaacGym 仿真 + 真实）
- **Metrics**: 任务成功率 + 样本效率 + 鲁棒性 + 泛化性
- **Limitations**: 单物体、忽略动力学、小数据量
- **Evidence Notes**: 全文读取，Table I + Figures 2-4 提供完整对比
## 本地引用关系

- [[chen2025vividex]]
- [[gao2025must]]
- [[han2025upvital]]
- [[patel2024getzero]]
- [[shi2025zeromimic]]
## 证据元数据

- **Fulltext Quality**: fulltext
- **Evidence Coverage**: 读取了全文，包括 abstract、introduction (Sec I)、method (Sec II)、experiments (Sec III-IV)、related work (Sec V)、figures (1-4)
- **Confidence**: high — 全文完整，ICRA 2025，UC Berkeley，xArm7 + Allegro 16-DoF 灵巧手，约 450 视频→70K 轨迹预训练，真实 3 任务 + 仿真 3 任务，RL 微调 25× 样本效率提升
- **Summary**: 提出 HOP（Hand-Object interaction Pretraining），从野外视频中学习通用机器人操控先验。方法：(1) MCC-HO + HaMeR 从单目视频提取 3D 手-物体轨迹；(2) Simulator-in-the-loop retargeting：优化器将人类手部关键点映射到机器人关节角度，在 IsaacGym 中验证物理可行性；(3) Transformer (GPT-2) 在约 70K 重定向轨迹上预训练 next-action 预测。微调：RL (PPO) 或 BC 均可。真实 Grasp & Lift 0.65 vs 最佳基线 0.35。仿真 RL 微调 25× 样本效率提升，3× 鲁棒性提升，2× 泛化性提升


## Problem

学习可复用的传感器运动操控表示需要大规模数据。人类视频包含丰富的操控技能，但缺乏运动信息。如何从野外视频中提取手-物体交互轨迹并转化为机器人传感器运动先验？


## Method

- **3D 手-物体轨迹提取**：
  - MCC-HO + HaMeR → 单目 RGB → 3D 手+物体点云序列
  - 跳过 CAD 模型精化以提高泛化性
  - 时间平滑：锚定到时间平滑的手部检测
- **Simulator-in-the-loop retargeting**：
  - 优化目标：min ½‖xh[k+1] - f(a[k])‖² + λ‖a[k] - φ[k]‖²
  - f = 前向运动学，xh = 人类手部关键点 3D 坐标
  - 在 IsaacGym 高保真仿真器中约束，确保物理可行
  - 每视频 700 次优化（随机化场景布局+初始状态）
  - 修剪：保留追踪误差 < 3cm + 无碰撞的轨迹
- **数据集**：DexYCB (250 视频) + 100 Days of Hands (200 视频) → 约 70K 机器人轨迹
- **Transformer 预训练**：
  - GPT-2 架构，输入：过去 16 步本体感觉 + 观测（深度/点云）
  - 损失：L1 动作预测（非自回归）
  - 预测未来关节角度（相对当前状态）
- **微调**：
  - RL (PPO)：小探索噪声(0.1)，值函数 warm-up 200 步，共享 tokenizer
  - BC：与预训练相同目标，在少量任务演示上微调


## Experiments

- **真实机器人（xArm7 + Allegro Hand）**（3 任务×20 trials）：
  - Grasp & Drop: HOP 0.80, Diff.Policy 0.90, ImageNet-F 0.80, R3M 0.0
  - Grasp & Pour: HOP 1.0, Diff.Policy 0.20, ImageNet-F 0.70, R3M 1.0
  - Grasp & Lift: HOP 0.65, Diff.Policy 0.30, ImageNet-F 0.35, R3M 0.0
  - 多物体任务（Grasp & Lift）优势最明显：+30pp over ImageNet-F
- **仿真 RL 微调**（3 任务×256 环境×3 seeds）：
  - Grasp & Lift: HOP ~60% vs PPO scratch ~10% (25× sample efficiency)
  - Grasp & Throw: HOP 远超 DAPG/AMP 基线
  - Open Cabinet: HOP 显著优于从零训练
- **鲁棒性**（力学干扰）：HOP 3× 优于从零训练
- **泛化性**（未见 YCB 物体）：HOP 2× 优于从零训练
- **消融**：
  - 手-物体联合先验 vs 纯手部先验：鲁棒性和灵活性均提升
  - 无物体轨迹 → 性能下降（尤其 Grasp & Throw）


## Limitations

1. 仅建模单物体交互，未考虑多物体场景
2. 忽略物体动力学（不放物体动力学到优化中）
3. 约 450 视频的预训练数据量相对较小
4. 真实实验任务相对简单（单物体操控）
5. 灵巧手特定，未扩展到简单夹爪


## Key Takeaways

- Simulator-in-the-loop retargeting 是桥接人类视频和机器人轨迹的关键
- 手-物体联合先验优于纯手部先验：物体轨迹提供可供性和直观物理信息
- 450 个视频即可学到有价值的操控先验
- 预训练先验使 RL 探索更高效：25× 样本效率提升
- 微调过程复用预训练信息，即使任务不在训练数据中

## 相关概念

- [[robotic-manipulation]]
- [[reinforcement-learning]]
- [[sim-to-real]]
- [[grasping]]

## 相关研究者

- [[singh|Singh, Himanshu Gaurav]]
- [[loquercio|Loquercio, Antonio]]
