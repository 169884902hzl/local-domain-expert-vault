---
title: "SplatSim: Zero-Shot Sim2Real Transfer of RGB Manipulation Policies Using Gaussian Splatting"
tags: [manipulation, sim-to-real]
created: "2026-04-25"
updated: "2026-04-25"
type: "literature"
status: "done"
summary: "提出 SplatSim，用 3D Gaussian Splatting (3DGS) 替代传统 mesh 作为仿真渲染原语，实现 RGB manipulation policy 的零样本 Sim2Real transfer。方法：(1) 从真实场景扫描构建 Robot Splat Model + Object Splat Model；(2) 在 PyBullet 物理引擎中合成 Gaussian 点云，渲染仿真 RGB 观测；(3) 用 Diffusion Policy 在 SplatSim 仿真中训练策略，零样本部署到真实世界。4 个任务（T-Push, Pick-Up-Apple, Orange-On-Plate, Assembly）零样本 Sim2Real 平均 86.25%，接近 real2real 97.5%。渲染速度 ~9.3 FPS"
authors: "Qureshi, M. Nomaan; Garg, Sparsh; Yandun, Francisco; Held, David; Kantor, George et al."
year: "2025"
venue: "2025 IEEE International Conference on Robotics and Automation (ICRA)"
zotero_key: "6Q9T9MSN"
---
## 摘要

Zotero 未提供摘要；详见下方精读分析。

## 中文简述

提出基于学习方法的操控方法，具有仿真到真实迁移特点。

**研究方向**: 机器人操控、仿真到真实迁移

## 证据元数据

- **Fulltext Quality**: fulltext
- **Evidence Coverage**: 读取了全文，包括 abstract、introduction (Sec I)、related work (Sec II)、method (Sec III)、experiments (Sec IV)、tables (I-III)、figures (1-6)
- **Confidence**: high — 全文完整，ICRA 2025，Carnegie Mellon University，Franka Panda 真实机器人，4 操控任务，全面对比 real2real baseline，零样本 Sim2Real 86.25% vs real2real 97.5%
- **Summary**: 提出 SplatSim，用 3D Gaussian Splatting (3DGS) 替代传统 mesh 作为仿真渲染原语，实现 RGB manipulation policy 的零样本 Sim2Real transfer。方法：(1) 从真实场景扫描构建 Robot Splat Model + Object Splat Model；(2) 在 PyBullet 物理引擎中合成 Gaussian 点云，渲染仿真 RGB 观测；(3) 用 Diffusion Policy 在 SplatSim 仿真中训练策略，零样本部署到真实世界。4 个任务（T-Push, Pick-Up-Apple, Orange-On-Plate, Assembly）零样本 Sim2Real 平均 86.25%，接近 real2real 97.5%。渲染速度 ~9.3 FPS
## 关键贡献

1. SplatSim 框架：首次将 3DGS 作为仿真渲染原语与物理引擎结合
2. Robot Splat Model + Object Splat Model 分离设计：独立建模机器人和物体
3. 零样本 Sim2Real：无需任何真实数据训练，直接部署仿真策略
4. 高保真渲染：照片级仿真图像缩小视觉域差距
## 结构化提取

- **Problem**: RGB manipulation policy 的零样本 Sim2Real transfer
- **Method**: SplatSim — 3DGS 渲染原语 + PyBullet 物理 + Diffusion Policy
- **Tasks**: T-Push, Pick-Up-Apple, Orange-On-Plate, Assembly
- **Sensors**: 2× RGB 相机（固定视角）
- **Robot Setup**: Franka Emika Panda + PyBullet 仿真
- **Metrics**: 任务成功率（20 trials）
- **Limitations**: 渲染速度慢、需手动扫描、无动态效果
- **Evidence Notes**: 全文读取，Tables I-III 提供完整 Sim2Real 对比和消融
## 本地引用关系

- [[dalal2025local]]
- [[do2025watch]]
- [[lips2024keypoints]]
- [[patel2025realtosimtoreal]]
- [[wu2025rlgsbridge]]
## Problem

RGB-based 操控策略的 Sim2Real transfer 面临视觉域差距：传统仿真器渲染的图像与真实 RGB 观测差距大，需要大量 domain randomization 或 fine-tuning。3D Gaussian Splatting 可以生成照片级真实渲染，但无法直接与物理引擎结合用于机器人策略学习。如何将 3DGS 作为仿真渲染原语，实现零样本 Sim2Real？


## Method

- **场景扫描与建模**：
  - 用 Polycam 扫描真实场景构建 3DGS 模型
  - Robot Splat Model：对机器人各关节状态分别扫描，构建高斯点云集合
  - Object Splat Model：对目标物体扫描，记录 Gaussian 点云相对物体中心的偏移
- **仿真渲染流程**：
  - PyBullet 物理引擎驱动机器人和物体的位姿
  - 根据位姿合成 Gaussian 点云（变换到世界坐标）
  - 使用 3DGS 可微渲染管线生成 RGB 图像
  - 支持多相机视角渲染
- **策略训练**：
  - Diffusion Policy 架构：UNet + 2 观测窗口 + 16 动作预测步
  - 仅用仿真渲染的 RGB 图像训练
  - 输入：2 帧 RGB（240×320）+ 机器人本体感觉
  - 输出：末端执行器 Δpose（4 DoF: x, y, z, yaw）
- **Domain Randomization**：
  - 物体初始位置随机化
  - 相机轻微扰动
  - 无需传统 DR（光照/纹理随机化），3DGS 渲染已足够真实


## Experiments

- **4 个操控任务**（Franka Panda + 2 RGB 相机）：
  - T-Push：推动 T 形物体到目标位姿
  - Pick-Up-Apple：从碗中拾取苹果放到桌上
  - Orange-On-Plate：将橙子放到盘子上
  - Assembly：多步装配（拾取+放置+对接）
- **成功率对比**（20 trials/任务）：
  - Sim2Real（零样本）：T-Push 90%, Apple 85%, Orange 80%, Assembly 90%, Avg 86.25%
  - Real2Real：T-Push 95%, Apple 95%, Orange 95%, Assembly 95%, Avg 97.5%
  - 传统仿真（MuJoCo renderer）：显著低于 SplatSim
- **渲染性能**：~9.3 FPS（3DGS 渲染）
- **消融**：
  - 3DGS 渲染 vs 传统渲染：视觉质量大幅提升，策略性能提升 30%+
  - Robot Splat Model 分离 vs 整体：分离设计避免物体间高斯干涉
  - 多视角 vs 单视角：多视角提供更好空间理解


## Limitations

1. 渲染速度受限（~9.3 FPS），无法支持大规模并行仿真
2. 需要逐场景扫描构建 Splat Model，无法自动生成新场景
3. 3DGS 无法建模动态效果（透明、反光、流体）
4. 物理仿真与渲染解耦，接触变形等视觉反馈缺失
5. 仅验证简单桌面操控任务


## Key Takeaways

- 3DGS 作为渲染原语有效缩小 Sim2Real 视觉域差距
- 分离式 Robot/Object Splat Model 是关键设计：避免高斯点云干涉
- 零样本部署可行：无需真实训练数据即可达到 ~86% 成功率
- 渲染速度是主要瓶颈：9.3 FPS 限制了数据采集效率
- 物理仿真与渲染解耦是双刃剑：灵活但牺牲视觉-物理一致性

## 相关概念

- [[robotic-manipulation]]
- [[sim-to-real]]
- [[diffusion-model]]

## 相关研究者

- [[qureshi|Qureshi, M. Nomaan]]
