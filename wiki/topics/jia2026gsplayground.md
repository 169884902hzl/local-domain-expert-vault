---
title: "GS-playground: A high-throughput photorealistic simulator for vision-informed robot learning"
tags: [manipulation, imitation, sim-to-real, robot-learning]
created: "2026-04-29"
updated: "2026-04-29"
type: "literature"
status: "done"
summary: "提出基于 3D Gaussian Splatting 的高吞吐量并行仿真框架 GS-Playground，在 640×480 分辨率下达到 10⁴ FPS 渲染吞吐，结合自研 velocity-impulse 物理引擎和自动化 Real2Sim 流水线，在四足/人形运动、导航和操控任务上实现有效 Sim-to-Real 迁移。"
authors: "Jia, Yufei; Zhang, Heng; Zhang, Ziheng; Wu, Junzhe; Yu, Mingrui et al."
year: "2026"
venue: "arXiv Preprint"
zotero_key: "A8TNG2G6"
---
## 摘要

Embodied AI research is undergoing a shift toward vision-centric perceptual paradigms. While massively parallel simulators have catalyzed breakthroughs in proprioception-based locomotion, their potential remains largely untapped for vision-informed tasks due to the prohibitive computational overhead of large-scale photorealistic rendering. Furthermore, the creation of simulation-ready 3D assets heavily relies on labor-intensive manual modeling, while the significant sim-to-real（仿真到真实迁移） physical gap hinders the transfer of contact-rich（接触丰富） manipulation（操控） policies. To address these bottlenecks, we propose GS-Playground, a multi-modal（多模态） simulation framework designed to accelerate end-to-end（端到端） perceptual learning. We develop a novel high-performance parallel physics engine, specifically designed to integrate with a batch 3D Gaussian Splatting (3DGS) rendering pipeline to ensure high-fidelity synchronization. Our system achieves a breakthrough throughput of 10^4 FPS at 640x480 resolution, significantly lowering the barrier for large-scale visual RL. Additionally, we introduce an automated Real2Sim workflow that reconstructs photorealistic, physically consistent, and memory-efficient environments, streamlining the generation of complex simulation-ready scenes. Extensive experiments on locomotion, navigation, and manipulation（操控） demonstrate that GS-Playground effectively bridges the perceptual and physical gaps across diverse embodied tasks. Project homepage: https://gsplayground.github.io.

## 中文简述

提出基于学习方法的导航方法，具有仿真到真实迁移特点。

**研究方向**: 机器人操控、模仿学习、仿真到真实迁移、机器人学习

## 关键贡献

1. **通用型嵌入式仿真平台**：从零开发跨平台（Windows/Linux/macOS）并行物理引擎，支持 GPU 和 CPU 后端，提供 RGB 相机、LiDAR、力/接触传感器等多模态感知，支持四足、人形、机械臂等多种机器人形态。
2. **内存高效的 Batch 3DGS 渲染**：针对刚体环境优化的点云剪枝策略，在单块 GPU 上实现 640×480 分辨率下 10⁴ FPS 的突破性吞吐量，显著扩展了基于视觉的 RL 规模。
3. **自动化"Image-to-Physics" Real2Sim 流水线**：从单张 RGB 图像自动生成物理一致的 sim-ready 数字孪生，包含自动分割、重建和亚毫米级姿态对齐。
## 结构化提取

- Problem: 现有并行仿真器在视觉保真度和渲染效率之间存在矛盾，无法同时满足大规模视觉 RL 和真实感渲染的需求；sim-ready 3D 资产创建依赖手工建模
- Method: 自研并行物理引擎（velocity-impulse formulation + PGS solver）+ Batch 3DGS 渲染（点云剪枝 + RLGK）+ 自动化 Image-to-Physics Real2Sim 流水线（Grounding DINO + SAM + SAM3D + AnySplat + Speedy-splat）
- Tasks: 四足运动（Unitree Go1/Go2）、人形运动（Unitree G1）、视觉导航（Go2 目标追踪）、视觉操控（Airbot Play 方块抓取）
- Sensors: RGB 相机、深度相机、Batch-LiDAR（光线投射）、多点接触力/力矩传感器
- Robot Setup: Unitree Go1/Go2（四足）、Unitree G1（人形，23-DoF）、Airbot Play（机械臂）
- Metrics: FPS（渲染/物理）、PSNR/SSIM/LPIPS（视觉质量）、奖励曲线（RL 训练）、Sim-to-Real 成功率（90% 抓取）
- Limitations: 3DGS 无法处理随机光照/阴影；仅支持刚体不支持可变形物体；GPU 后端仍在优化
- Evidence Notes: 全文从 arXiv 获取。物理稳定性通过 Newton's Cradle、Spot 静止站立、密集货架三组实验验证，对比 MuJoCo/Genesis/MjWarp。渲染吞吐在三种 GPU（4090/6000Ada/A100）上超过 Isaac Sim。Sim-to-Real 在四足、人形、导航、操控四类任务上验证。操控仅限简单方块抓取，无复杂任务验证。
## 本地引用关系

-
## 证据元数据

- Fulltext Quality: fulltext
- Evidence Coverage: 90%（从 arXiv 全文读取，图表数据仅文字描述，无原始数值表格）
- Confidence: high
- Summary: 提出基于 3D Gaussian Splatting 的高吞吐量并行仿真框架 GS-Playground，在 640×480 分辨率下达到 10⁴ FPS 渲染吞吐，结合自研 velocity-impulse 物理引擎和自动化 Real2Sim 流水线，在四足/人形运动、导航和操控任务上实现有效 Sim-to-Real 迁移。


## Problem

现有大规模并行仿真器（Isaac Gym、Isaac Lab、Genesis）在推进本体感受式运动学习方面取得了突破，但在视觉信息驱动的任务上面临两个核心瓶颈：

1. **渲染开销过高**：高分辨率真实感渲染与策略学习产生严重的资源竞争，常导致 OOM 错误，迫使用户在视觉保真度和仿真吞吐量之间妥协。
2. **资产构建耗时费力**：创建同时满足视觉和物理高保真度的"sim-ready" 3D 资产依赖繁重的手工建模，且仿真与真实之间的物理鸿沟阻碍了接触密集型操控策略的迁移。


## Method

### 1. 物理引擎（Velocity-Impulse Formulation）
- 基于广义坐标的速度-脉冲公式，实现严格互补性约束和显式摩擦限速钳位
- 通过 MCP（Mixed Complementarity Problem）求解接触和摩擦，使用 PGS 求解器
- **关键工程优化**：
  - Constraint Islands 并行化：动态构建约束依赖图，将不相连的刚体系统分派到多核 CPU 线程并行求解
  - Temporal Coherence Warm-Starting：通过 Contact Manifold Tracking 持久化跨帧接触约束，将 PGS 迭代次数从 50+ 降至 <10

### 2. Batch 3DGS 渲染
- **高效剪枝策略**：受 Speedy-splat、Mini-splatting 启发，减少 90%+ Gaussians，PSNR 下降 < 0.05
- **吞吐量扩展**：同时渲染 2048 场景（640×480），总吞吐达 10K FPS
- **Rigid-Link Gaussian Kinematics (RLGK)**：将 3DGS 聚类绑定到对应刚体，实现"零开销"姿态同步

### 3. Real2Sim 流水线（Image-to-Physics）
- **分割**：Grounding DINO 检测 + SAM1/SAM2 分割，自动去重（mask IoU + 双准则规则）
- **修复**：LaMa 顺序修复背景
- **重建**：SAM3D 重建物体级 3DGS/mesh，AnySplat 生成背景 3DGS
- **对齐**：深度图对齐 + 像素占用缩放匹配
- **压缩**：Speedy-splat 剪枝减少内存占用

### 4. 用户界面
- 多模态传感器：RGB、深度、Batch-LiDAR（光线投射）、接触力/力矩
- MuJoCo MJCF 格式兼容
- 跨平台开发工作流：本地原型（Win/Mac/Linux）→ 大规模训练（Linux GPU 集群）


## Experiments

### A. 物理稳定性
- **Newton's Cradle**：相比 MuJoCo 更好地保持冲击时序和摆动幅度，能量衰减更少
- **Spot 10ms 时间步**：基座位移更小，漂移更少
- **密集货架堆叠**：在复杂多接触约束下稳定收敛，MuJoCo 出现抖动和接触引起的漂移
- **复杂度扩展**：N=50 人形时 GS-Playground(CPU) 1015 FPS，MuJoCo 32x 慢，MjWarp 600x 慢；Genesis 在 N=10 时已不收敛

### B. 视觉保真度
- 3DGS 剪枝：30% Gaussians 保留，PSNR 26.87（原始 27.15），SSIM 0.80（原始 0.83）
- 渲染吞吐：在 RTX 4090/RTX 6000 Ada/A100 上全面超过 Isaac Sim ray-tracing，尤其在 1280×720 时 Isaac Sim 出现 OOM
- 定性渲染与真实照片高度一致

### C. 运动学习
- **Unitree Go1 平坦/崎岖地形**：d=1（单个物理子步）下达到 IsaacLab d=4 的终端奖励，收敛更快
- **Sim-to-Real 部署**：
  - Go2 四足：1024 并行环境，10 分钟收敛
  - G1 人形：2048 并行环境，6 小时收敛

### D. 视觉导航
- Unitree Go2 + 自我中心 RGB，层级 RL（高层视觉策略 + 低层运动控制）
- 零样本部署成功追踪目标锥

### E. 视觉操控
- Airbot Play 机械臂方块抓取，Raw RGB + 本体状态 → 6-DoF 关节动作
- Real2Sim 重建数字孪生 + 相机/光照域随机化
- **90% 零样本真实世界成功率**

### F. Bridge-GS 数据集
- 基于 Bridge-v2 数据集，通过 Real2Sim 流水线生成 3DGS 增强数据集
- 单张图像处理端到端 < 5 分钟


## Limitations

1. **光照限制**：3DGS 无法处理随机化光照和阴影，资产生成依赖源图像光照条件，需要算法化重光照来解耦物体外观与环境光照
2. **仅刚体**：RLGK 假设刚体，无法表示可变形物体（布料、流体）或软体操控，计划集成 PBD/MPIM 粒子动力学
3. **GPU 后端仍在优化**：文中提到 GPU 内核融合和内存管理策略仍在改进中


## Key Takeaways

1. **对 DLO 操控的直接关联有限但前景广阔**：论文明确提到可变形/软体是未来工作方向（计划集成粒子动力学），一旦实现将为 DLO RL 训练提供高吞吐视觉仿真环境
2. **Real2Sim 流水线的实用价值**：从单张 RGB 图像自动生成 sim-ready 资产的流水线（<5 min/场景），可加速构建 DLO 操控实验环境
3. **渲染-物理同步设计值得借鉴**：RLGK 将 3DGS 聚类绑定到刚体的"零开销"同步方案，是解决动态场景渲染一致性的好思路
4. **物理引擎选型的启示**：velocity-impulse + PGS 在接触密集场景比 optimization-centric solver（如 MuJoCo）更稳定，这对于接触丰富的 DLO 操控任务很重要
5. **90% 操控 Sim-to-Real 成功率**：视觉操控的零样本迁移效果显著，但仅限简单抓取任务，DLO 等复杂任务的迁移效果未知

## 相关概念

- [[robotic-manipulation]]
- [[imitation-learning]]
- [[sim-to-real]]
- [[robot-learning]]
- [[vision-language-model]]
- [[deformable-linear-object]]
- [[grasping]]

## 相关研究者

- [[jia-yufei|Jia, Yufei]]
- [[zhang-heng|Zhang, Heng]]
