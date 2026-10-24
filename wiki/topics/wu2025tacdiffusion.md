---
title: "TacDiffusion: Force-domain diffusion policy for precise tactile manipulation"
tags: [manipulation, imitation, diffusion]
created: "2026-04-25"
updated: "2026-04-25"
type: "literature"
status: "done"
summary: "提出 TacDiffusion，首个力域扩散策略用于高精度触觉机器人插入。DDPM 从触觉观测（外力/内力/末端速度）生成 6D wrench 动作，替代传统运动域动作。关键创新：(1) 力域扩散策略：扩散模型直接输出 wrench 而非位姿；(2) 动态系统滤波器：解决扩散模型推理频率（141.8Hz）与实时控制（1000Hz）的频率失配问题，F̈ff = α(β(Fdf - Fff) - Ḟff)；(3) 阻抗控制+前馈力执行。从单一任务（Cuboid）演示学习，零样本迁移到 4 个新物体，成功率 95.7%（DF3），超越基线 129.5%"
authors: "Wu, Yansong; Chen, Zongxie; Wu, Fan; Chen, Lingyun; Zhang, Liding et al."
year: "2025"
venue: "arXiv Preprint"
zotero_key: "W8IPB7XU"
---
## 摘要

Assembly（装配） is a crucial skill for robots in both modern manufacturing and service robotics. However, mastering transferable insertion skills that can handle a variety of high-precision assembly（装配） tasks remains a significant challenge. This paper presents a novel framework that utilizes diffusion（扩散） models to generate 6D wrench for high-precision tactile（触觉） robotic insertion tasks. It learns from demonstrations performed on a single task and achieves a zero-shot（零样本） transfer success rate of 95.7% across various novel high-precision tasks. Our method effectively inherits the self-adaptability demonstrated by our previous work. In this framework, we address the frequency misalignment between the diffusion policy（扩散策略） and the real-time control loop with a dynamic system-based filter, significantly improving the task success rate by 9.15%. Furthermore, we provide a practical guideline regarding the trade-off between diffusion（扩散） models’ inference ability and speed.


## 中文简述

提出基于扩散策略的插入方法，具有零样本泛化特点。

**研究方向**: 机器人操控、模仿学习、扩散模型

## 关键贡献

1. 首个力域扩散策略：DDPM 直接生成 6D wrench 动作
2. 动态系统滤波器：解决扩散推理频率与实时控制频率的失配
3. 从行为树专家策略蒸馏：继承触觉自适应能力（原始切换逻辑）
4. 模型大小-推理速度权衡分析：提供实践指导
## 结构化提取

- **Problem**: 扩散模型与力控制结合实现高精度可迁移的触觉插入
- **Method**: TacDiffusion — DDPM 6D wrench 输出 + 动态系统滤波器 + 阻抗控制前馈力
- **Tasks**: 5 个紧公差插入（Cuboid/Key/Cyl-S/Cyl-L/Prism, 0.02-0.1mm clearance）
- **Sensors**: 关节力矩传感器（外部/内部 wrench）+ 末端执行器速度
- **Robot Setup**: Franka Emika Panda + parallel gripper
- **Metrics**: 成功率（零样本迁移平均 95.7%）+ 执行时间
- **Limitations**: 仅插入任务、依赖专家策略、模型大小需权衡
- **Evidence Notes**: 全文读取，Tables I-III 提供完整性能对比和消融
## 本地引用关系

- [[lee2025diffdagger]]
- [[liu2025forcemimic]]
- [[marougkas2025integrating]]
- [[wu2025discrete]]
- [[zhao2025polytouch]]
## 证据元数据

- **Fulltext Quality**: fulltext
- **Evidence Coverage**: 读取了全文，包括 abstract、introduction (Sec I)、related work (Sec II)、method (Sec III)、experiments (Sec IV)、tables (I-III)、figures (1-11)
- **Confidence**: high — 全文完整，arXiv 2025，Technical University of Munich (MIRMI)，DDPM 扩散模型输出 6D wrench + 动态系统滤波器 + 阻抗控制前馈力，Franka Panda 5 紧公差插入物体（Cuboid/Key/Cyl-S/Cyl-L/Prism），零样本迁移成功率 95.7%（DF3），动态系统滤波器提升 9.15%
- **Summary**: 提出 TacDiffusion，首个力域扩散策略用于高精度触觉机器人插入。DDPM 从触觉观测（外力/内力/末端速度）生成 6D wrench 动作，替代传统运动域动作。关键创新：(1) 力域扩散策略：扩散模型直接输出 wrench 而非位姿；(2) 动态系统滤波器：解决扩散模型推理频率（141.8Hz）与实时控制（1000Hz）的频率失配问题，F̈ff = α(β(Fdf - Fff) - Ḟff)；(3) 阻抗控制+前馈力执行。从单一任务（Cuboid）演示学习，零样本迁移到 4 个新物体，成功率 95.7%（DF3），超越基线 129.5%


## Problem

高精度装配（sub-millimeter 紧公差插入）需要同时控制运动和力。现有扩散策略仅在运动域输出动作，无法直接用于力控任务。如何将扩散模型与力控制结合实现高精度可迁移的触觉操控？


## Method

- **扩散模型**：
  - 输入：观测 o = (外力/力矩, 内力/力矩, 末端执行器速度) × 2 时间步
  - 输出：6D wrench (Fx,Fy,Fz,τx,τy,τz)
  - DDPM：50 步去噪，ResNet 噪声估计器
  - 训练：1500 条专家演示（行为树策略），1000Hz 采集
- **模型配置**（DF1-DF4，N=128-1024 neurons）：
  - DF3 (N=512)：推理 141.8Hz，loss 0.0716 → 最佳平衡
  - DF4 (N=1024)：推理 51.2Hz，loss 0.0288 → 频率太低
- **动态系统滤波器**：
  - F̈ff = α(β(Fdf - Fff) - Ḟff)，α=0.9, β=0.3
  - 将低频扩散输出平滑插值为 1000Hz 控制信号
- **阻抗控制+前馈力**：
  - τm = J^T[Fff + K·e + D·ė + M·ẍd] + 动力学补偿
  - 同时调节运动和力行为


## Experiments

- **性能测试（5 物体 × 50 随机位姿 × 2 次）**：
  - DF3: Cuboid 98%, Key 99%, Cyl-S 97%, Cyl-L 96%, Prism 91%, 平均 95.7%
  - Baseline: Cuboid 92%, Key 94%, Cyl-S 61%, Cyl-L 82%, Prism 96%, 平均 83.3%
  - DF3 效率指标提升 129.5%
- **模型大小权衡**：
  - DF1→DF3：成功率递增（77.5→95.7%），频率递减（503.8→141.8Hz）
  - DF4：频率过低（51.2Hz）导致性能反降（81.5%）
- **动态系统滤波器消融**：
  - 16/20 场景有滤波器更优
  - 平均成功率提升 9.15%
- **自适应行为继承**：扩散模型成功继承行为树的原始切换能力（wiggle 对齐 → push 插入 → stuck 解除）


## Limitations

1. 仅在紧公差插入任务验证，未扩展到其他力控任务
2. 训练数据来自行为树专家策略，依赖现有技能管线
3. 模型大小选择需人工权衡
4. 扩散推理频率仍低于实时控制要求，需滤波器补偿
5. 仅验证单任务训练→零样本迁移，未探索多任务学习


## Key Takeaways

- 力域扩散策略可行：DDPM 直接输出 wrench 比运动域输出更适合力控任务
- 频率失配是关键挑战：动态系统滤波器是简单有效的解决方案
- 扩散模型可继承专家策略的自适应能力：触觉原始切换逻辑被隐式学习
- 模型大小存在最优值：太大导致推理太慢，太小精度不足
- 零样本力控迁移可实现：95.7% 成功率远超传统方法

## 相关概念

- [[robotic-manipulation]]
- [[imitation-learning]]
- [[diffusion-model]]
- [[grasping]]

## 相关研究者

- [[wu-yansong|Wu, Yansong]]
- [[wu|Wu, Fan]]
