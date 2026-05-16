---
title: "DART: Learning-enhanced model predictive control for dual-arm non-prehensile manipulation"
tags: [manipulation, RL, DLO, bimanual, grasping]
created: "2026-04-29"
updated: "2026-04-29"
type: "literature"
status: "done"
summary: "DART 提出双臂托盘非抓取操控框架，将非线性 MPC、阻抗控制和三类托盘-物体动力学模型结合，用于在仿真中控制物体在托盘上滑动到目标位置。"
authors: "Das, Autrio; Bollimuntha, Shreya; Jeevesh, Madala Venkata Renu; Patra, Keshab; Ghosh, Tashmoy et al."
year: "2026"
venue: "arXiv Preprint"
zotero_key: "4BUM6CV7"
---
## 摘要

What appears effortless to a human waiter remains a major challenge for robots. Manipulating objects nonprehensilely on a tray is inherently difficult, and the complexity is amplified in dual-arm（双臂） settings. Such tasks are highly relevant to service robotics in domains such as hotels and hospitality, where robots must transport and reposition diverse objects with precision. We present DART, a novel dual-arm（双臂） framework that integrates nonlinear Model Predictive Control (MPC) with an optimization-based impedance controller to achieve accurate object motion relative to a dynamically controlled tray. The framework systematically evaluates three complementary strategies for modeling tray-object dynamics as the state transition function within our MPC formulation: (i) a physics-based analytical model, (ii) an online regression based identification model that adapts in real-time, and (iii) a reinforcement learning（强化学习）-based dynamics model that generalizes across object properties. Our pipeline is validated in simulation with objects of varying mass, geometry, and friction coefficients. Extensive evaluations highlight the trade-offs among the three modeling strategies in terms of settling time, steady-state error, control effort, and generalization across objects. To the best of our knowledge, DART constitutes the first framework for non-prehensile dual-arm manipulation（双臂操控） of objects on a tray. Project Link: https://dart-icra.github.io/dart/

## 中文简述

提出基于强化学习的绳索操控方法，具有泛化能力特点。

**研究方向**: 机器人操控、强化学习、可变形物体操控、双臂操控、抓取

## 关键贡献

1. 提出 DART 框架，将双臂协调和托盘上物体非抓取操控统一为 MPC 控制问题。
2. 比较三类状态转移模型：physics-based analytical model、online regression-based identification model 和 reinforcement-learning-based dynamics model。
3. 将 RL 学到的动力学模型嵌入 MPC，用于提升跨物体几何、质量和摩擦属性的泛化。
4. 在 MuJoCo 仿真中系统比较 settling time、steady-state error 和 control effort 等指标。
## 结构化提取

- Problem: 双臂机器人通过托盘倾斜间接移动托盘上的物体，属于双臂非抓取式操控。
- Method: 非线性 MPC + optimization-based impedance controller；MPC 中比较解析物理、在线回归和 RL 学习三种托盘-物体动力学模型。
- Tasks: 托盘上刚体物体定位和滑动控制。
- Sensors: 仿真中使用物体与托盘状态；真实传感器未验证。
- Robot Setup: 双 xArm7 持托盘，MuJoCo 仿真。
- Metrics: settling time、steady-state error、control effort。
- Limitations: 无真机、无 DLO、简单刚体、状态估计假设理想。
- Evidence Notes: arXiv HTML 全文；主要结论来自 Abstract、Method、Experiments、Results 和 Conclusion/Future Work。
## 本地引用关系

- [[lee2025diffdagger]]
- [[li2025routing]]
## 证据元数据

- Fulltext Quality: fulltext (arXiv HTML)
- Evidence Coverage: high; method, task setup, controller structure, evaluation metrics and main qualitative trade-offs are available; some table values were not copied verbatim into this fallback note.
- Confidence: medium-high
- Summary: DART 提出双臂托盘非抓取操控框架，将非线性 MPC、阻抗控制和三类托盘-物体动力学模型结合，用于在仿真中控制物体在托盘上滑动到目标位置。
## Problem

论文关注双臂机器人共同持托盘，通过调整托盘姿态让托盘上的刚体物体滑动到目标位置。这是典型的 dual-arm non-prehensile manipulation：机器人不直接抓取目标物体，而是通过托盘倾斜、摩擦和惯性间接控制物体。难点包括：双臂协同会影响托盘姿态，托盘-物体接触动力学随质量、几何和摩擦变化，且服务机器人场景需要对不同物体有泛化能力。
## Method

整体结构是两层控制。高层是非线性 MPC，输出托盘 roll/pitch 等倾斜控制，用预测模型估计托盘上物体的未来状态。低层是 optimization-based impedance controller，把高层托盘姿态指令转化为双臂机器人执行所需的关节力矩或控制指令，并处理双臂与托盘之间的协调。

三种动力学模型分别承担 MPC 的状态转移函数。PMPC 使用解析物理模型和摩擦建模，依赖较准确的物体参数。RMPC 使用在线回归识别，执行时适配未建模动力学。LMPC 使用 PPO 学习动力学相关参数或状态转移表示，并在训练中用 domain randomization 覆盖不同物体属性。
## Experiments

实验在 MuJoCo 中完成，平台为双 xArm7 持托盘。任务是在托盘上移动 cube、cylinder、sphere 等物体，覆盖不同质量和摩擦系数。指标包括 settling time、steady-state error 和 control effort。论文报告三类方法各有取舍：物理模型在已知参数和规则接触下可较稳定，在线回归能自适应但可能有初期误差，RL 模型在多配置中泛化较好但控制代价可能更高。
## Limitations

1. 仅在仿真中验证，没有真实双臂机器人实验。
2. 任务对象是简单刚体，不涉及 DLO、布料或复杂堆叠物体。
3. 假设状态估计较干净，真实系统中的视觉/触觉噪声和托盘状态估计误差尚未验证。
4. 与我们的 DLO 方向相关性主要来自 dual-arm coordination、contact-rich dynamics 和 MPC+learning hybrid，而不是 DLO 本体。
## Key Takeaways

1. 对双臂 DLO 操控有启发的是“learning-enhanced MPC”范式：用学习模型补偿难建模接触动力学，再由 MPC 保持约束和稳定性。
2. DART 暴露了一个 idea 方向：DLO 操控也可以用不确定性或触觉事件触发 MPC/策略切换，而不是完全依赖开环 action chunk。
3. DART 不是 DLO 工作，不能直接当作 DLO baseline；更适合作为 dual-arm non-prehensile / hybrid control 证据。

## 相关概念

- [[robotic-manipulation]]
- [[reinforcement-learning]]
- [[deformable-linear-object]]
- [[bimanual-manipulation]]
- [[grasping]]
- [[planning]]

## 相关研究者

- [[das|Das, Autrio]]
- [[bollimuntha|Bollimuntha, Shreya]]
