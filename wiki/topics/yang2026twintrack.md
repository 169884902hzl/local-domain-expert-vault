---
title: "TwinTrack: Bridging Vision and Contact Physics for Real-Time Tracking of Unknown Objects in Contact-Rich Scenes"
tags: [manipulation, sim-to-real, DLO, grasping]
created: "2026-05-07"
updated: "2026-05-07"
type: "literature"
status: "done"
summary: "提出融合视觉与接触物理的 Real2Sim/Sim2Real 框架 TwinTrack，通过学习几何残差和物理参数实现未知刚体物体在接触丰富场景中的实时 6-DoF 位姿追踪（>20Hz）"
authors: "Yang, Wen; Xie, Zhixian; Wang, Yiting; Tadepalli, Abhijit; Amor, Heni Ben et al."
year: "2026"
venue: "arXiv Preprint"
zotero_key: "TF6T2MFI"
---
## 摘要

Real-time tracking of previously unseen, highly dynamic objects in contact-rich（接触丰富） scenes, such as during dexterous（灵巧） in-hand manipulation（操控）, remains a major challenge. Pure vision-based approaches often fail under heavy occlusions due to frequent contact interactions and motion blur caused by abrupt impacts. We propose Twintrack, a physics-aware perception system that enables robust, real-time 6-DoF pose tracking of unknown dynamic objects in contact-rich（接触丰富） scenes by leveraging contact physics cues. At its core, Twintrack integrates Real2Sim and Sim2Real. Real2Sim combines vision and contact physics to jointly estimate object geometry and physical properties: an initial reconstruction is obtained from vision, then refined by learning a geometry residual and simultaneously estimating physical parameters (e.g., mass, inertia, and friction) based on contact dynamics consistency. Sim2Real achieves robust pose estimation by adaptively fusing a visual tracker with predictions from the updated contact dynamics. Twintrack is implemented on a GPU-accelerated, customized MJX engine to guarantee real-time performance. We evaluate our method on two contact-rich（接触丰富） scenarios: object falling with environmental contacts and multi-fingered in-hand manipulation（操控）. Results show that, compared to baselines, Twintrack delivers significantly more robust, accurate, and real-time tracking in these challenging settings, with tracking speeds above 20 Hz. Project page: https://irislab.tech/TwinTrack-webpage/

## 中文简述

提出基于学习方法的绳索操控方法，具有仿真到真实迁移特点。

**研究方向**: 机器人操控、仿真到真实迁移、可变形物体操控、抓取

## 关键贡献

1. **Real2Sim/Sim2Real 闭环架构**：Real2Sim（后端）从 RGB-D 序列重建物体几何并学习接触动力学模型，Sim2Real（前端）利用学到的物理模型辅助视觉追踪，两个模块持续交换信息
2. **基于几何残差的视觉-物理几何融合**：先用 Gaussian Splatting 从关键帧重建视觉几何并转为神经 SDF，再通过可学习的几何残差 δ 修正视觉几何误差，使碰撞检测更贴近真实
3. **GPU 加速的实时实现**：基于定制化 MJX 物理引擎，使用 CEM 采样优化（避免不可微接触动力学导致的梯度问题），整体 >20Hz 实时性能
4. **自适应融合策略**：Sim2Real 通过特征匹配质量自适应调整视觉追踪与物理预测的权重，在遮挡严重时自动依赖物理预测
## 结构化提取

- **Problem**: 接触丰富动态场景中未知物体的实时 6-DoF 位姿追踪，纯视觉方法在遮挡和运动模糊下失效
- **Method**: Real2Sim（Gaussian Splatting 几何重建 + 神经 SDF + 几何残差 + CEM 物理参数学习）与 Sim2Real（SAM2/SuperPoint/LightGlue 特征追踪 + 自适应视觉-物理融合）的闭环架构
- **Tasks**: 物体自由落体碰撞追踪、灵巧手内操控物体追踪
- **Sensors**: 单目 RGB-D（Intel RealSense D435i）、机器人关节状态（灵巧手场景）
- **Robot Setup**: LEAP 四指灵巧手，Ryzen 5955WX + RTX 4090 计算平台
- **Metrics**: ADD [cm]、ADD-S [cm]、单步预测误差、质量估计精度、帧率 [Hz]
- **Limitations**: 仅单刚体、均匀残差、需第一帧提示、长时域预测不可靠、参数可辨识性问题
- **Evidence Notes**: Table I 证明几何残差有效降低预测误差；Table III 证明 proposed 方法在所有物体上优于 baseline 和消融变体；Fig. 6 视觉证据显示含 δ 的仿真轨迹与真实运动吻合；质量估计部分准确部分偏差较大（Table II），作者归因于可观测性不足和模型简化偏差
## 本地引用关系

- [[yang2026twintrack]]
## 证据元数据

- Fulltext Quality: fulltext
- Evidence Coverage: complete（全文含方法、实验、消融、限制讨论）
- Confidence: high
- Summary: 提出融合视觉与接触物理的 Real2Sim/Sim2Real 框架 TwinTrack，通过学习几何残差和物理参数实现未知刚体物体在接触丰富场景中的实时 6-DoF 位姿追踪（>20Hz）


## Problem

在接触丰富的动态场景（如灵巧手内操控、物体自由落体碰撞）中，对未知物体进行实时 6-DoF 位姿追踪是一个关键挑战。纯视觉方法在面对频繁遮挡和运动模糊时会失效，而接触物理线索可以弥补视觉退化的不足。核心难题在于：（1）如何从单目 RGB-D 输入联合估计未知物体的几何、物理属性（质量、惯性、摩擦）和位姿；（2）如何在实时约束下实现视觉与物理模拟的有效融合。


## Method

### 整体架构（Section III-V）

**Real2Sim（后端，异步运行）**：

Phase 1 - 视觉几何重建（Section IV-A）：
- 使用 Gaussian Splatting (GS) 表示物体空间模型
- 联合优化 GS 模型 𝒢_gs 和关键帧位姿 {𝐪_i}（光度残差 + 几何损失）
- 从渲染深度图学习神经 SDF 表示 SDF_vision(p)

Phase 2 - 接触动力学与几何补偿（Section IV-B, C）：
- 基于 MJX 物理引擎构建接触动力学模型，定制约碰撞检测以支持神经 SDF
- 碰撞几何 SDF_collision(p) = SDF_vision(p) - δ(p)，其中 δ 为可学习几何残差
- 待估计参数 θ = {m_obj, diag[I_x, I_y, I_z]_obj, μ, δ}
- 使用 softmax 加权 CEM（类 MPPI）进行采样优化，最小化单步预测损失
- 实际实现中 δ 采用常数残差（而非神经网络），避免过拟合

**Sim2Real（前端，在线运行）**：

特征追踪器（Section V-A）：
- SAM2 分割物体区域 → SuperPoint 提取特征 → LightGlue 匹配 → RANSAC 过滤
- 关键帧缓冲区作为位姿锚点，避免长期漂移

自适应融合（Section V-B）：
- min_{q_k} w_k * L_vision(q_k) + (1-w_k) * L_dynamics(q_k)
- L_vision：特征对应点距离损失
- L_dynamics：接触动力学单步预测损失
- w_k 基于特征匹配对数量自适应设置（sigmoid 函数）

### 关键技术细节
- 物理引擎：MJX（JAX 实现，GPU 并行）
- 几何表示：Gaussian Splatting → 神经 SDF → 碰撞 SDF
- 优化方法：CEM 采样优化（避免接触动力学不可微问题）
- 特征提取：SAM2 + SuperPoint + LightGlue


## Experiments

### 实验设置（Section VI-A）
- **数据集**：自采集 RGB-D 视频（Intel RealSense D435i）
- **场景 I**：物体自由落体碰撞（两面墙+地面），6 种物体（snack box, tissue box, milk bottle, Spam can, 3D-printed duck, mustard bottle）
- **场景 II**：LEAP 四指灵巧手内操控，2 种物体（Spam can, 3D-printed duck）
- **Ground Truth**：Scaniverse 重建高质量网格 → FoundationPose 生成伪 GT 位姿
- **硬件**：Ryzen 5955WX CPU + RTX 4090 GPU

### Real2Sim 评估（Table I, II）
- **单步预测误差**：学习前 18.78/4.18（最差/最好），学习后 w/o δ 约 0.18-1.16，加入 δ 后进一步降至 0.13-0.70
- **质量估计**：部分物体准确（snack box 40g→38±3g），部分偏差较大（bottle 24g→32±10g），原因包括可观测性不足和 MJX 简化接触模型偏差
- **多步开环仿真**（Fig. 6）：加入 δ 的仿真轨迹与真实运动高度吻合，能捕捉碰撞、反弹、稳定行为

### Sim2Real 评估（Table III）
- **ADD 指标 [cm]**：Proposed 平均 1.23±0.65，Baseline (FoundationPose) 3.01±1.86，w/o dynamics 7.21±5.76
- **ADD-S 指标 [cm]**：Proposed 平均 0.59±0.31，Baseline 1.15±0.40
- **消融实验**：
  - random（随机物理参数）：大部分 >100cm，完全失败
  - w/o dynamics（无动力学，恒速预测）：某些情况下比 baseline 更差（bottle ADD 20.29cm）
  - w/o δ（无几何残差）：比 proposed 稍差，证明几何残差贡献显著
- **实时性能**：SAM2 12ms + SuperPoint 8ms + 动力学预测 5ms + 关键帧匹配 15ms + 融合优化 5ms + 其他 3ms ≈ 48ms/frame → >20Hz

### 关键发现
1. 接触动力学对接触丰富场景追踪至关重要（无动力学时追踪严重退化）
2. 几何残差 δ 有效修正视觉几何误差，提升碰撞建模精度
3. 长时域开环预测仍然困难（接触物理的混沌敏感性），但单步/少步预测与视觉反馈结合效果良好


## Limitations

1. **长时视觉缺失**：视觉长期不可用时，仅靠动力学预测会累积漂移
2. **初始化依赖**：需要合理的初始状态，初始化差会导致碰撞几何学习错误
3. **均匀几何残差**：当前 δ 为常数，无法处理空间变化的几何误差
4. **单刚体假设**：不支持多物体追踪或可变形物体
5. **单目 RGB-D**：依赖第一帧提示，无法处理完全不可见的情况
6. **参数可辨识性**：摩擦和质量存在耦合，不同试验收敛到不同值
7. **长时域预测局限**：接触物理的混沌特性使长时开环预测不可靠


## Key Takeaways

1. **Real2Sim/Sim2Real 闭环思路值得关注**：将物理模型学习和感知追踪耦合，物理模型在线学习后反馈增强感知，这种双向循环在 DLO 操控场景中也很有价值（DLO 的物理特性可在线学习以增强追踪）
2. **几何残差概念可迁移**：视觉重建的几何往往不精确，通过物理一致性学习几何修正项是一个轻量有效的思路，可考虑用于 DLO 形状重建
3. **采样优化替代可微仿真**：接触动力学的非光滑性使梯度方法困难，CEM/MPPI 类方法在 GPU 加速下可行且实用，这为涉及接触的 Sim-to-Real 提供了一种优化范式
4. **自适应融合权重设计**：根据视觉质量动态调整视觉/物理权重，这种自适应策略可用于任何多源信息融合场景
5. **局限性提示**：该方法目前仅适用于刚体，不可直接用于 DLO，但其 Real2Sim 架构和物理辅助追踪思路有借鉴价值

## 相关概念

- [[robotic-manipulation]]
- [[sim-to-real]]
- [[deformable-linear-object]]
- [[grasping]]

## 相关研究者

- [[yang-wen|Yang, Wen]]
