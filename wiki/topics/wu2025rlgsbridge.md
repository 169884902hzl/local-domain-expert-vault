---
title: "RL-GSBridge: 3D gaussian splatting based Real2Sim2Real method for robotic manipulation learning"
tags: [manipulation, RL, sim-to-real]
created: "2026-04-25"
updated: "2026-04-25"
type: "literature"
status: "done"
summary: "提出 RL-GSBridge，基于 3D Gaussian Splatting 的 Real2Sim2Real 框架用于视觉 RL 机器人操控。核心创新：(1) Soft Mesh Binding GS：放宽 GaMeS 的硬网格约束，允许高斯单元沿法线方向浮动，提升渲染质量（SSIM 0.964-0.989 vs GaMeS 0.894-0.989）；(2) 物理动力学 GS 编辑：同步 PyBullet 物理状态与 GS 渲染，保持视觉一致性；(3) SACwB：SAC + 轻量基线控制器引导探索。KUKA iiwa 零样本 Sim-to-Real，抓取成功率平均仅下降 6.6%（RL-sim 下降 80%），Pick-and-Place 68.75→71.87%"
authors: "Wu, Yuxuan; Pan, Lei; Wu, Wenhua; Wang, Guangming; Miao, Yanzi et al."
year: "2025"
venue: "arXiv Preprint"
zotero_key: "BYE8U5AD"
---
## 摘要

Sim-to-Real（仿真到真实迁移） refers to the process of transferring policies learned in simulation to the real world, which is crucial for achieving practical robotics applications. However, recent Sim2real methods either rely on a large amount of augmented data or large learning models, which is inefficient for specific tasks. In recent years, with the emergence of radiance field reconstruction methods, especially 3D Gaussian splatting, it has become possible to construct realistic real-world scenes. To this end, we propose RL-GSBridge, a novel real-to-sim-to-real（仿真到真实迁移） framework which incorporates 3D Gaussian Splatting into the conventional RL simulation pipeline, enabling zero-shot（零样本） simto-real transfer for vision-based deep reinforcement learning（强化学习）. We introduce a mesh-based 3D GS method with soft binding constraints, enhancing the rendering quality of mesh models. Then utilizing a GS editing approach to synchronize the rendering with the physics simulator, RL-GSBridge could reflect the visual interactions of the physical robot accurately. Through a series of sim-to-real（仿真到真实迁移） experiments, including grasping（抓取） and pickand-place tasks, we demonstrate that RL-GSBridge maintains a satisfactory success rate in real-world task completion during sim-to-real（仿真到真实迁移） transfer. Furthermore, a series of rendering metrics and visualization results indicate that our proposed mesh-based 3D GS reduces artifacts in unstructured objects, demonstrating more realistic rendering performance.


## 中文简述

提出基于强化学习的抓取方法，具有仿真到真实迁移特点。

**研究方向**: 机器人操控、强化学习、仿真到真实迁移

## 关键贡献

1. Soft Mesh Binding GS：放宽硬网格约束提升渲染质量和灵活性
2. 物理动力学 GS 编辑：实时同步仿真物理状态与 GS 渲染
3. RL-GSBridge Real2Sim2Real 框架：用消费级相机重建场景即可构建训练环境
4. SACwB：带基线控制器引导的 SAC 加速稀疏奖励 RL 训练
## 结构化提取

- **Problem**: 通过 3D Gaussian Splatting 构建照片级仿真实现零样本 Sim-to-Real
- **Method**: RL-GSBridge — Soft Mesh Binding GS + 物理动力学 GS 编辑 + SACwB RL
- **Tasks**: 桌面抓取（6 场景）+ Pick-and-Place
- **Sensors**: 俯视 RGB 相机（RealSense D435i，眼在手）
- **Robot Setup**: KUKA iiwa + Robotiq 2F-140 gripper
- **Metrics**: 成功率（抓取 Sim-to-Real avg ↓6.6%，Pick-and-Place ↑4%）
- **Limitations**: 仅桌面任务、渲染速度、有限随机范围
- **Evidence Notes**: 全文读取，Tables I-IV 提供完整 Sim-to-Real 对比和渲染指标
## 本地引用关系

- [[liu2025autonomous]]
- [[marougkas2025integrating]]
- [[patel2025realtosimtoreal]]
- [[qureshi2025splatsim]]
- [[wang2023multistage]]
## 证据元数据

- **Fulltext Quality**: fulltext
- **Evidence Coverage**: 读取了全文，包括 abstract、introduction (Sec I)、related work (Sec II)、method (Sec III)、experiments (Sec IV)、tables (I-IV)、figures (1-6)
- **Confidence**: high — 全文完整，arXiv 2025，Shanghai Jiao Tong University，Soft Mesh Binding GS + PyBullet SACwB，KUKA iiwa + Robotiq 2F-140，抓取 Sim-to-Real 平均仅下降 6.6%（vs RL-sim 80%），Pick-and-Place 68.75→71.87%
- **Summary**: 提出 RL-GSBridge，基于 3D Gaussian Splatting 的 Real2Sim2Real 框架用于视觉 RL 机器人操控。核心创新：(1) Soft Mesh Binding GS：放宽 GaMeS 的硬网格约束，允许高斯单元沿法线方向浮动，提升渲染质量（SSIM 0.964-0.989 vs GaMeS 0.894-0.989）；(2) 物理动力学 GS 编辑：同步 PyBullet 物理状态与 GS 渲染，保持视觉一致性；(3) SACwB：SAC + 轻量基线控制器引导探索。KUKA iiwa 零样本 Sim-to-Real，抓取成功率平均仅下降 6.6%（RL-sim 下降 80%），Pick-and-Place 68.75→71.87%


## Problem

Sim-to-Real 迁移的关键瓶颈是仿真视觉与真实世界的外观差距。现有方法要么依赖大量域随机化数据，要么训练大规模通用模型。能否通过 3D Gaussian Splatting 构建照片级真实感仿真环境，实现高效的零样本 Sim-to-Real？


## Method

- **Real2Sim 阶段**：
  - 消费级相机采集视频 → COLMAP 位姿估计 → SAM-track 分割
  - openMVS 构建 mesh 先验
  - Soft Mesh Binding GS：μ = α1v1 + α2v2 + α3v3 + αn·vn（允许法线方向浮动）
  - 渲染指标：SSIM 0.964-0.989，PSNR 28-37
- **Sim2Real 训练阶段**：
  - PyBullet 物理仿真 + GS 渲染器提供视觉观测
  - 读取仿真器中物体位姿 → 实时编辑 GS 模型 → 渲染第一人称图像
  - SACwB：概率 λ 执行基线控制器，概率 1-λ 选择基线/actor 较优输出
  - 图像增强（噪声+属性随机化）增强 Sim-to-Real 鲁棒性
- **零样本部署**：
  - 直接将 actor 网络部署到真实机器人
  - 真实第一人称相机图像作为输入


## Experiments

- **抓取任务（6 场景）**：
  - RL-sim: Small cube 96.88→12.50 (↓87%), Bear 93.75→25.00 (↓73%)
  - RL-GSBridge: Small cube 96.88→96.88 (0%), Bear 87.50→100% (↑14%)
  - 跨多种物体和背景（Foam Pad/Tablecloth）：平均下降仅 6.6%
- **Pick-and-Place**：
  - Cake→Plate: 68.75%→71.87% (↑4%)
- **渲染质量**：
  - Soft Binding 全面优于 GaMeS（SSIM +0.005-0.095, PSNR +1.06-8.93）
  - 减少 unstructured 物体的渲染伪影
- **非刚性物体编辑**：Soft Binding 支持非刚性变形的 GS 编辑


## Limitations

1. 仅在桌面级抓取和放置任务验证，未扩展到更复杂操控
2. GS 渲染速度 ~9 FPS（非实时），策略训练后离线渲染
3. PyBullet 物理仿真与 GS 渲染的同步可能有延迟
4. 物体初始位置随机范围有限（30×30cm）
5. 未与其他 Sim-to-Real 方法（如域随机化）进行系统对比


## Key Takeaways

- 3D GS 构建照片级仿真环境有效：消费级相机即可重建，渲染质量远超传统 mesh shading
- Soft Mesh Binding 是关键改进：放宽硬约束提升渲染质量和灵活性
- 视觉一致性是 Sim-to-Real 的核心：RL-GSBridge 仅下降 6.6% vs RL-sim 80%
- 物理仿真+GS 渲染解耦是合理架构：物理精度和视觉保真度分别保证
- 零样本迁移可行：无需真实数据微调

## 相关概念

- [[robotic-manipulation]]
- [[reinforcement-learning]]
- [[sim-to-real]]
- [[grasping]]

## 相关研究者

- [[wu-yuxuan|Wu, Yuxuan]]
- [[wang-guangming|Wang, Guangming]]
