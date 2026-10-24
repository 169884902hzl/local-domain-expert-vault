---
title: "Routing Manipulation of Deformable Linear Object Using Reinforcement Learning and Diffusion Policy"
tags: [DLO, manipulation, RL, imitation, diffusion]
created: "2026-04-25"
updated: "2026-04-25"
type: "literature"
status: "done"
summary: "提出 DLO routing 方法，先用 RL（SAC）分别训练 rope insertion 和 pulling 策略，摩擦系数随机化（0.12-1.2）实现 gentle motion（最小化绳索拉伸），再收集 RL rollouts 作为专家演示训练闭环扩散策略。仿真 fixed θ+high friction 80.39%（RL）/70.33%（Diffusion），真实 90.48%。扩散策略在干扰下最鲁棒（58.24% vs open-loop 48.35%）"
authors: "Li, Mingen; Yu, Houjian; Choi, Changhyun"
year: "2025"
venue: "2025 IEEE International Conference on Robotics and Automation (ICRA)"
zotero_key: "7L3PG3N9"
---
## 摘要

Zotero 未提供摘要；详见下方精读分析。

## 中文简述

提出基于扩散策略的可变形物体方法。

**研究方向**: 可变形物体操控、机器人操控、强化学习、模仿学习、扩散模型

## 证据元数据

- **Fulltext Quality**: fulltext
- **Evidence Coverage**: 读取了全文，包括 abstract、introduction、related work (Sec II)、method (Sec III)、experiments (Sec IV)、tables (I-III)、figures (1-7)
- **Confidence**: high — 全文完整，ICRA 2025 论文，SoftGym 仿真 + 真实 Franka/ViperX 验证，91 场景评估，消融实验完备
- **Summary**: 提出 DLO routing 方法，先用 RL（SAC）分别训练 rope insertion 和 pulling 策略，摩擦系数随机化（0.12-1.2）实现 gentle motion（最小化绳索拉伸），再收集 RL rollouts 作为专家演示训练闭环扩散策略。仿真 fixed θ+high friction 80.39%（RL）/70.33%（Diffusion），真实 90.48%。扩散策略在干扰下最鲁棒（58.24% vs open-loop 48.35%）
## 关键贡献

1. 完整 DLO routing 框架：insertion + pulling 两个子任务的 RL 策略
2. 摩擦系数随机化训练 gentle motion：负奖励惩罚过度拉伸，适应 0.12-1.2 摩擦范围
3. 两阶段流程：open-loop RL expert → closed-loop diffusion policy，兼顾数据效率和鲁棒性
4. 仿真 + 真实验证，多种 DLO（nylon/iron wire/power cable）和摩擦条件
## 结构化提取

- **Problem**: 高摩擦环境下 DLO routing（穿过孔洞 + 拉出），需 gentle 且鲁棒的操控
- **Method**: 两阶段 — SAC RL（摩擦随机化+拉伸惩罚）→ DDIM 扩散策略（闭环）
- **Tasks**: DLO insertion + pulling（SoftGym 仿真 + 真实 Franka/ViperX）
- **Sensors**: RGB-D 相机（RealSense D415）+ SAM 分割
- **Robot Setup**: SoftGym 仿真 + Franka（insertion）+ ViperX 300S（pulling）
- **Metrics**: 成功率（91 场景）、目标距离（cm）
- **Limitations**: 仅状态观测、2D 约束、已知灵活度、insertion 错误传播
- **Evidence Notes**: 全文读取，Tables I-III 提供完整仿真+真实结果
## 本地引用关系

- [[chen2025deformpam]]
- [[han2025upvital]]
- [[karim2024davil]]
- [[liu2025autonomous]]
- [[scheikl620movement]]
## Problem

DLO routing through a hole 涉及频繁接触和未知摩擦参数。现有方法假设光滑接触或低张力，忽略粗糙表面的影响。高摩擦下 pulling 导致绳索卡住或过度拉伸。环境干扰（孔位置/角度变化）进一步增加难度，需要闭环自适应策略。


## Method

- **RL for DLO Pulling（SAC）**：
  - 观察：DLO 粒子位置 p1:n、DLO 灵活度、夹爪位置/朝向、环位置/角度/半径
  - 动作：3D 笛卡尔运动 + 1D 旋转 + 抓取指示（2D 约束为 3D）
  - 运动基元：预训练 insertion → pulling 初始化 → PD 控制器线性拉取
  - 奖励：r = γ·rdist + β·rstretch（γ=50, β=-100）
  - rdist：成功拉出 15cm 时正奖励（3·(1-0.15/dT)）
  - rstretch：粒子间距超过阈值（λ=1.4·linit）时负奖励
  - 摩擦随机化：fixed θ [0.12, 1.2]，rand θ [0.12, 0.5]
- **专家演示收集**：
  - RL 策略 rollout 收集 state-action 对
  - 预处理：移除零动作数据点，保留终止步
- **闭环扩散策略**：
  - DDIM 框架，UNet 架构
  - 观察窗口 Ts=7，预测窗口 Ta=1，去噪迭代 g=2
  - 条件：观察序列 s(t-Ts):t，输出未来动作
  - 训练：MSE loss（噪声预测）


## Experiments

- **仿真（SoftGym，91 场景）**：
  - fixed θ, μ=0.12：RL 98.53%（w/o rand μ 100%），Diffusion 94.50%，MLP 74.72%，Transformer 62.63%
  - fixed θ, μ=0.12-1.2：RL w/ rand μ 80.39%（w/o rand μ 55.88%），Diffusion 70.33%
  - rand θ, μ=0.12-0.5：RL w/ rand μ 60.78%，Diffusion 48.35%
  - 带干扰：fixed θ 位移 58.24%（Diffusion）vs 48.35%（RL），rand θ 角度变化 60.43%（Diffusion）vs 67.03%（RL）
- **真实（Franka + ViperX）**：
  - RL w/ rand μ：90.48% vs Visual Baseline 80.95%
  - 多种绳索：nylon、铁丝、电源线
  - SAM 分割关键点，MoveIt 规划轨迹
- **关键发现**：
  - 摩擦随机化在变摩擦环境下提升 14-24% 成功率
  - 扩散策略在干扰下比 open-loop RL 更鲁棒
  - 单层 mesh + 随机材质优于更真实的 Cloth3D mesh


## Limitations

1. 仅状态观测（非图像），需 SAM 分割作为预处理
2. 2D 平面约束，未扩展到完整 3D
3. DLO 灵活度假设已知
4. 运动基元为开环，insertion 错误会传播到 pulling
5. 真实实验仅在固定角度场景验证


## Key Takeaways

- 摩擦随机化是高摩擦 DLO 操控的关键：不随机化性能下降 44%
- 两阶段 RL→Diffusion 流程有效：RL 生成高质量专家演示，Diffusion 提供闭环鲁棒性
- 过度拉伸惩罚（rstretch）引导 gentle motion，避免绳索损坏
- 在干扰场景中闭环扩散策略显著优于开环 RL
- 多样性 > 保真度：单层 mesh + 随机材质优于更真实的 mesh

## 相关概念

- [[deformable-linear-object]]
- [[robotic-manipulation]]
- [[reinforcement-learning]]
- [[imitation-learning]]
- [[diffusion-model]]
- [[grasping]]

## 相关研究者

- [[li-mingen|Li, Mingen]]
- [[yu-houjian|Yu, Houjian]]
- [[choi-changhyun|Choi, Changhyun]]
