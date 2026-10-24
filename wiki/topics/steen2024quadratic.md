---
title: "Quadratic Programming-based Reference Spreading Control for Dual-Arm Robotic Manipulation with Planned Simultaneous Impacts"
tags: [manipulation]
created: "2026-04-25"
updated: "2026-04-25"
type: "literature"
status: "done"
summary: "提出基于二次规划（QP）的 Reference Spreading（RS）控制框架，用于双臂机器人在名义同时冲击场景下的跟踪控制。核心设计：三种控制模式（ante-impact、interim、post-impact），通过 VIVE 遥操作获取冲击一致的参考轨迹，interim 模式使用混合参数 γ 在 ante/post 参考间平滑过渡并减少速度反馈。双臂 Franka 抓取实验：90% 成功率 vs 无 RS 80%、无速度反馈 40%、无 interim 85%。600+ 实验证实框架在物体偏移 ±30mm 下有效降低输入力峰值和阶跃"
authors: "Steen, Jari van; Brandt, Gijs van den; Wouw, Nathan van de; Kober, Jens; Saccon, Alessandro"
year: "2024"
venue: "IEEE Transactions on Robotics"
zotero_key: "YZ5LNUW8"
---
## 摘要

With the aim of further enabling the exploitation of intentional impacts in robotic manipulation（机器人操控）, a control framework is presented that directly tackles the challenges posed by tracking control of robotic manipulators that are tasked to perform nominally simultaneous impacts. This framework is an extension of the reference spreading control framework, in which overlapping ante- and post-impact references that are consistent with impact dynamics are defined. In this work, such a reference is constructed starting from a teleoperation-based approach. By using the corresponding ante- and post-impact control modes in the scope of a quadratic programming control approach, peaking of the velocity error and control inputs due to impacts is avoided while maintaining high tracking performance. With the inclusion of a novel interim mode, we aim to also avoid input peaks and steps when uncertainty in the environment causes a series of unplanned single impacts to occur rather than the planned simultaneous impact. This work in particular presents for the first time an experimental evaluation of reference spreading control on a robotic setup, showcasing its robustness against uncertainty in the environment compared to three baseline control approaches.


## 中文简述

提出基于学习方法的双臂方法。

**研究方向**: 机器人操控

## 关键贡献

1. 首次在物理多自由度双臂机器人上实验验证 RS 控制框架
2. 新型 interim 模式设计：在 ante/post-impact 参考间平滑混合（blending），避免模式切换时的输入阶跃
3. 基于遥操作的冲击一致参考轨迹生成方法：低增益阻抗控制 + QP 框架
4. 定制硅胶末端执行器减少冲击力峰值
## 结构化提取

- **Problem**: 双臂机器人同时冲击跟踪控制中的误差峰值和输入峰值消除
- **Method**: QP-based Reference Spreading + 三模式控制（ante/interim/post）+ 遥操作参考生成
- **Tasks**: 双臂抓取（米箱/包裹/饮料瓶，4 种物体）
- **Sensors**: 关节编码器 + 外部力矩估计（momentum observer）+ Optitrack 运动捕捉
- **Robot Setup**: 2 × Franka Emika 7-DoF + 定制硅胶末端执行器
- **Metrics**: 成功抓取率 + 平均力矩范数 + 最大提升高度差
- **Limitations**: 预定义 interim 持续时间、依赖遥操作、缺少稳定性证明
- **Evidence Notes**: 全文读取，Tables I-II + Figures 8-11 提供完整实验对比
## 本地引用关系

- [[chuang2025active]]
- [[karim2024davil]]
- [[wang2025oneshot]]
## 证据元数据

- **Fulltext Quality**: fulltext
- **Evidence Coverage**: 读取了全文，包括 abstract、introduction (Sec I)、reference generation (Sec III)、control approach (Sec IV)、experiments (Sec V)、tables (I-II)、figures (1-11)
- **Confidence**: high — 全文完整，IEEE TRO 2024，Eindhoven University of Technology + Delft University of Technology (Kober)，双 Franka Emika 7-DoF 机器人，600+ 实验验证，首次在物理多自由度机器人上验证 Reference Spreading 框架
- **Summary**: 提出基于二次规划（QP）的 Reference Spreading（RS）控制框架，用于双臂机器人在名义同时冲击场景下的跟踪控制。核心设计：三种控制模式（ante-impact、interim、post-impact），通过 VIVE 遥操作获取冲击一致的参考轨迹，interim 模式使用混合参数 γ 在 ante/post 参考间平滑过渡并减少速度反馈。双臂 Franka 抓取实验：90% 成功率 vs 无 RS 80%、无速度反馈 40%、无 interim 85%。600+ 实验证实框架在物体偏移 ±30mm 下有效降低输入力峰值和阶跃


## Problem

双臂机器人在执行同时冲击（simultaneous impacts）的操控任务时，由于不可避免的冲击时间不确定性和冲击速度跳变，传统跟踪控制会产生速度误差峰值和输入力矩峰值，可能导致系统不稳定或硬件损坏。现有 RS 框架仅经过 1-DOF 系统仿真验证，未在多自由度物理机器人上实现。


## Method

- **参考轨迹生成**（遥操作）：
  - HTC VIVE 手柄控制器 + QP 阻抗控制器
  - 低增益（K_r = diag(300,300,300,20,20,20)）让人补偿冲击
  - 记录末端执行器 6D 位姿、速度和期望力矩
  - 冲击检测：外力估计 + 速度方向三条件联合判断
- **Reference Extension**：
  - 在标称冲击时间 T_r 前后排除 ∆T_r 区间
  - Ante-impact 参考：常数保持（constant hold）
  - Post-impact 参考：常数保持
  - 位置通过速度积分扩展，保证一致性
- **三种 QP 控制模式**：
  - **Ante-impact**：高增益跟踪 ante-impact 扩展参考 + 力矩前馈
  - **Interim**（新设计）：混合参数 γ = (t-T_imp)/∆t_int，从 0 渐变到 1
    - γ=0 时：无速度反馈，等同 ante-impact 的前馈+位置反馈
    - γ=1 时：等同 post-impact 模式
    - 初始用测量速度 v_i 替代 ante 速度参考，消除不确定接触状态下的速度反馈
  - **Post-impact**：高增益跟踪 post-impact 扩展参考 + 力矩前馈
- **约束**：关节位置、速度、力矩限制


## Experiments

- **硬件**：2 × Franka Emika 7-DoF + 定制硅胶末端执行器
- **物体**：米箱(1.25kg)、单个包裹(0.64kg)、两个包裹(1.28kg)、饮料瓶组(2.12kg)
- **环境不确定性**：y 方向偏移 -30, -15, 0, +15, +30 mm
- **成功抓取率**（10 个参考 × 2 偏移 = 80 实验）：
  - No RS: 80%
  - No velocity feedback: 40%（振动导致物体掉落）
  - No interim: 85%
  - Proposed: **90%**
- **600 额外实验**（6 参考 × 5 偏移 × 5 重复 × 4 方法）：
  - 提出方法在所有偏移和物体组合中平均力矩范数最低
  - 即使 0mm 偏移（完美同时冲击），基线方法的输入力仍高于提出方法（因柔性导致有限过渡时间）
- **运动捕捉**：Optitrack Prime x22 × 4 相机，测量箱体最大提升高度作为接触建立速度指标


## Limitations

1. Interim 模式持续时间 ∆t_int 需预定义，依赖保守估计
2. 缺少接触完成检测器（contact-completion detector）
3. 参考轨迹依赖遥操作演示，未实现自主冲击感知运动规划
4. 未提供 RS 控制框架的形式化稳定性证明
5. 仅验证双臂抓取场景，未扩展到更复杂的冲击操控任务


## Key Takeaways

- Reference Spreading 是处理同时冲击场景的有效框架：通过分离 ante/post 参考避免误差峰值
- Interim 模式的混合设计是关键创新：平滑过渡 + 初始去除速度反馈 + 渐进恢复
- 遥操作生成冲击一致参考是实用方案：低增益让人自然补偿冲击
- 即使名义上同时冲击，实际冲击持续时间非零：RS 框架对此有内在鲁棒性
- QP 框架使 RS 可扩展到多任务+约束的复杂场景

## 相关概念

- [[robotic-manipulation]]
- [[bimanual-manipulation]]
- [[grasping]]

## 相关研究者

- [[steen|Steen, Jari van]]
- [[kober|Kober, Jens]]
