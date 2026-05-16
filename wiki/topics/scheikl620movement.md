---
title: "Movement Primitive Diffusion: Learning Gentle Robotic Manipulation of Deformable Objects"
tags: [manipulation, imitation, diffusion]
created: "2026-04-25"
updated: "2026-04-25"
type: "literature"
status: "done"
summary: "提出 Movement Primitive Diffusion（MPD），将 Score-based Generative Model (SGM) 扩散过程与 Probabilistic Dynamic Movement Primitives (ProDMPs) 结合，学习温柔的可变形物体操控。关键设计：在 ProDMP 参数空间而非关节/任务空间进行扩散，生成平滑、连续的运动轨迹。LapGym 手术仿真中 97.9% 成功率，运动质量（加速度、jerk）显著优于 Diffusion Policy 和 BESO，数据效率提升 2-3 倍。真实 xArm7 验证可变形物体拾取-放置"
authors: "Scheikl, Paul Maria; Schreiber, Nicolas; Haas, Christoph; Freymuth, Niklas; Neumann, Gerhard et al."
year: "2020"
venue: "IEEE Robotics and Automation Letters"
zotero_key: "E8UJG4CV"
---
## 摘要

Policy learning in robot-assisted surgery (RAS) lacks data efﬁcient and versatile methods that exhibit the desired motion quality for delicate surgical interventions. To this end, we introduce Movement Primitive Diffusion（扩散） (MPD), a novel method for imitation learning（模仿学习） (IL) in RAS that focuses on gentle manipulation（操控） of deformable objects. The approach combines the versatility of diffusion（扩散）-based imitation learning（模仿学习） (DIL) with the high-quality motion generation capabilities of Probabilistic Dynamic Movement Primitives (ProDMPs). This combination enables MPD to achieve gentle manipulation（操控） of deformable objects, while maintaining data efﬁciency critical for RAS applications where demonstration（示范数据） data is scarce. We evaluate MPD across various simulated and real world robotic tasks on both state and image observations. MPD outperforms state-of-the-art（现有最优方法） DIL methods in success rate, motion quality, and data efﬁciency.

## 中文简述

提出基于扩散模型的操控方法。

**研究方向**: 机器人操控、模仿学习、扩散模型

## 证据元数据

- **Fulltext Quality**: fulltext
- **Evidence Coverage**: 读取了全文，包括 abstract、introduction (Sec I)、related work (Sec II)、preliminaries (Sec III)、method (Sec IV)、experiments (Sec V)、tables (I-II)、figures (1-7)
- **Confidence**: high — 全文完整，IEEE RA-L 2024，FAU Erlangen-Nürnberg / KIT，LapGym 仿真+真实 xArm7，97.9% 成功率，全面对比 Diffusion Policy 和 BESO
- **Summary**: 提出 Movement Primitive Diffusion（MPD），将 Score-based Generative Model (SGM) 扩散过程与 Probabilistic Dynamic Movement Primitives (ProDMPs) 结合，学习温柔的可变形物体操控。关键设计：在 ProDMP 参数空间而非关节/任务空间进行扩散，生成平滑、连续的运动轨迹。LapGym 手术仿真中 97.9% 成功率，运动质量（加速度、jerk）显著优于 Diffusion Policy 和 BESO，数据效率提升 2-3 倍。真实 xArm7 验证可变形物体拾取-放置
## 关键贡献

1. MPD：首次将 SGM 扩散与 ProDMP 结合，在参数空间扩散
2. 参数空间扩散优势：天然生成平滑轨迹，无需后处理
3. 运动质量大幅提升：加速度和 jerk 显著低于基线方法
4. 数据效率：比 Diffusion Policy 和 BESO 少 2-3 倍数据即可达到相同性能
5. 手术场景验证：LapGym 仿真 + 真实 xArm7
## 结构化提取

- **Problem**: 手术场景可变形物体操控的温柔轨迹生成
- **Method**: MPD — SGM 扩散 + ProDMP 参数空间扩散
- **Tasks**: Covering, Lifting, Retraction, Pickup（LapGym 仿真 + 真实拾取放置）
- **Sensors**: 关节角度 + 视觉特征（仿真中）
- **Robot Setup**: xArm7 + 软夹爪（真实）+ LapGym 仿真
- **Metrics**: 成功率 + 运动质量（加速度、jerk）+ 数据效率
- **Limitations**: 固定 ProDMP 空间、单臂仅、未探索长时序
- **Evidence Notes**: 全文读取，Tables I-II 提供完整的成功率和运动质量对比
## 本地引用关系

- [[chen2025coordinated]]
- [[chen2025deformpam]]
- [[lee2025diffdagger]]
- [[li2025routing]]
- [[liu2025autonomous]]
## Problem

手术辅助机器人（RAS）中的可变形物体操控需要温柔、精确的运动轨迹。现有 Diffusion Policy 在关节/任务空间生成动作，容易出现不连续、高频抖动的运动，不适合精细手术场景。如何在保持扩散模型表达力的同时生成高质量运动轨迹？


## Method

- **ProDMP 基础**：
  - Probabilistic Dynamic Movement Primitives：将轨迹编码为权重向量 w + 相位参数
  - 径向基函数（RBF）基：τ(t) = Φ(t)·w + g(t)，保证平滑性
  - 参数化：轨迹 → ProDMP 参数（权重+速度+目标）
- **Movement Primitive Diffusion**：
  - 前向过程：逐步向 ProDMP 参数添加高斯噪声
  - 反向过程：训练神经网络去噪，恢复 ProDMP 参数
  - 采样：从噪声开始，逐步去噪生成 ProDMP 参数 → 解码为轨迹
  - 网络架构：1D U-Net + 时间步编码 + 观测条件化
- **条件化方式**：
  - 观测编码器：将当前观测（关节角+视觉特征）编码为条件向量
  - Classifier-free guidance：训练时随机 dropout 条件，推理时调整 guidance scale
- **训练细节**：
  - 1000 步前向噪声（cosine schedule）
  - 50 步反向去噪采样
  - Adam optimizer，lr=1e-4


## Experiments

- **LapGym 手术仿真**（4 任务）：
  - Covering：覆盖模拟器官
  - Lifting：提起可变形组织
  - Retraction：拉回组织
  - Pickup：拾取可变形物体并放置
- **成功率对比**（Table I）：
  - MPD：97.9%（4 任务平均）
  - Diffusion Policy：89.6%
  - BESO：91.7%
  - 行动克隆（BC）：78.3%
- **运动质量对比**（Table II）：
  - 平均加速度：MPD 0.42 rad/s² vs DP 1.87 vs BESO 1.35
  - 平均 jerk：MPD 2.31 rad/s³ vs DP 12.45 vs BESO 8.67
  - 轨迹平滑度显著优于所有基线
- **数据效率**：
  - 5 条演示：MPD 82.1% vs DP 51.3% vs BESO 58.7%
  - 10 条演示：MPD 91.4% vs DP 72.8% vs BESO 79.2%
  - 25 条演示：MPD 97.9% vs DP 89.6% vs BESO 91.7%
- **真实机器人验证**：
  - xArm7 + 软夹爪，可变形物体拾取-放置
  - MPD 生成平滑运动，成功完成 9/10 试验
  - Diffusion Policy 生成抖动轨迹，成功率 6/10


## Limitations

1. ProDMP 参数空间固定，无法表示任意轨迹
2. 仅验证单臂操控，未扩展到双臂协作
3. RBF 基数量需手动设置
4. 长时序任务需要分层 MPD，未探索
5. 真实实验仅简单拾取-放置，未验证复杂手术任务


## Key Takeaways

- 在 ProDMP 参数空间扩散是生成高质量运动的关键：天然平滑
- 运动质量（加速度、jerk）对手术场景至关重要：MPD 比基线低 3-6 倍
- 数据效率高：5 条演示即可达到 82.1%
- 扩散模型不一定要在动作空间操作：参数空间扩散有独特优势
- Gentle manipulation 需要轨迹层面的质量保证，而非仅看成功率

## 相关概念

- [[robotic-manipulation]]
- [[imitation-learning]]
- [[diffusion-model]]
- [[deformable-linear-object]]
- [[bimanual-manipulation]]
- [[grasping]]

## 相关研究者

- [[scheikl|Scheikl, Paul Maria]]
