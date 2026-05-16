---
title: "DOT-sim: Differentiable optical tactile simulation with precise real-to-sim physical calibration"
tags: [imitation, RL, sim-to-real, DLO, tactile]
created: "2026-05-01"
updated: "2026-05-01"
type: "literature"
status: "done"
summary: "提出 DOT-Sim，基于 MPM 可微物理仿真 + 残差光学渲染的光学触觉传感器仿真框架，仅用 19 段演示即可在数分钟内完成物理参数标定，实现零样本 Sim-to-Real 迁移（分类 85%+、肿瘤检测 90%、轨迹跟踪误差 <0.9mm）"
authors: "You, Yang; Do, Won Kyung; Swann, Aiden; Antonova, Rika; Kennedy, Monroe et al."
year: "2026"
venue: "arXiv Preprint"
zotero_key: "SDBMXRCQ"
---
## 摘要

Simulating optical tactile（触觉） sensors presents significant challenges due to their high deformability and intricate optical properties. To address these issues and enable a physically accurate simulation, we propose DOT-Sim: Differentiable Optical Tactile（触觉） Simulation. Unlike prior simulators that rely on simplified models of deformable sensors, DOT-Sim accurately captures the physical behavior of soft sensors by modeling them as elastic materials using the Material Point Method (MPM). DOT-Sim enables rapid calibration of optical tactile（触觉） sensor simulation using a small number of demonstrations within minutes, which is substantially faster than existing methods. Compared to current baselines, our approach supports much larger and non-linear deformations. To handle the optical aspect, we propose a novel approach to simulating optical responses by learning a residual image relative to the real-world idle state. We validate the physical and visual realism of our method through a series of zero-shot（零样本） sim-to-real（仿真到真实迁移） tasks. Our experiments show that DOT-Sim (1) accurately replicates the physical dynamics of a DenseTact optical tactile（触觉） sensor in reality, (2) generates realistic optical outputs in contact-rich（接触丰富） scenarios, (3) enables direct deployment of simulation-trained classifiers in the real world, achieving 85% classification accuracy on challenging objects and 90% accuracy in embedded tumor-type detection, and (4) allows precise trajectory following with a policy trained from demonstrations in simulation, with an average error of less than 0.9 mm.

## 中文简述

提出基于触觉感知的绳索操控方法，具有仿真到真实迁移特点。

**研究方向**: 模仿学习、强化学习、仿真到真实迁移、可变形物体操控、触觉感知

## 关键贡献

1. **MPM 可微物理仿真**：首次将 Material Point Method (MPM) 用于光学触觉传感器的物理建模，支持比 FEM 更大的非线性变形，并通过可微仿真实现快速物理参数标定
2. **残差光学渲染**：提出基于 ResNet 的残差图像预测方法，不直接回归触觉图像，而是预测与 idle 帧的差值，显著提升渲染精度（PSNR 提升 17.34%）
3. **高效标定流程**：仅需 19 段真实演示视频，在单张 A5000 GPU 上数分钟内完成 E/ν 标定，比 DiffTactile 等方法快一个数量级
4. **全流程 Sim-to-Real 验证**：在分类（in-domain 90.48%、out-of-domain 81.18%）、肿瘤检测（最高 96.55%）、轨迹跟踪（误差 <0.9mm）和 RL 任务上验证零样本迁移
## 结构化提取

- **Problem**: 光学触觉传感器的高保真仿真，包括大变形物理建模和复杂光学渲染，以支持零样本 Sim-to-Real 迁移
- **Method**: 两阶段框架：(1) MPM 可微物理仿真 + Chamfer distance 标定 E/ν；(2) 虚拟相机渲染深度/法线 + DeepLabV3 ResNet50 残差图像预测
- **Tasks**: 压头分类（6 类）、嵌入式肿瘤检测（二分类）、轨迹跟踪（6-DoF）、盒子重定位（RL, 旋转 10°）
- **Sensors**: DenseTact 2.0 光学触觉传感器（半球形硅胶凝胶，随机图案表面，反射涂层）
- **Robot Setup**: xArm 7 机械臂 + OptiTrack marker 追踪系统
- **Metrics**:
- **Limitations**: OOD 几何泛化差；计算开销大（3 FPS）；依赖 Abaqus 商用软件；仅验证 DenseTact 2.0
- **Evidence Notes**: 全文可获取，所有关键数据均来自论文正文表格。DiffTactile 的对比数据因其代码问题可能不完全公平，论文已注明。

  - 物理：L2 CD、Sig. L2 CD、EMD、F-Score@1mm
  - 光学：PSNR、Mean L2、Sig. Pixel L2
  - 下游：分类准确率、肿瘤检测准确率、轨迹误差 (mm)
## 本地引用关系

-
## 证据元数据

- Fulltext Quality: fulltext
- Evidence Coverage: high (全文通过 arXiv HTML 获取，含正文、实验表格、消融、附录)
- Confidence: high
- Summary: 提出 DOT-Sim，基于 MPM 可微物理仿真 + 残差光学渲染的光学触觉传感器仿真框架，仅用 19 段演示即可在数分钟内完成物理参数标定，实现零样本 Sim-to-Real 迁移（分类 85%+、肿瘤检测 90%、轨迹跟踪误差 <0.9mm）


## Problem

光学触觉传感器（如 GelSight、DenseTact）的仿真面临两大挑战：
1. **物理形变建模难**：传感器的柔性凝胶在大变形和非线性接触下行为复杂，现有方法（Tacto 用解析几何、Taxim 用查找表、DiffTactile 用 FEM）要么精度不足，要么难以处理大变形
2. **光学渲染难**：凝胶内部光传输涉及非均匀着色、内反射等复杂光学效应，简化模型无法生成足够真实的触觉图像

这导致在仿真中训练的策略难以直接迁移到真实世界——多数现有工作只能依赖 marker 而非完整光学信号作为策略输入。


## Method

### 两阶段框架

**阶段 1：物理仿真与标定 (Section III-A)**
- 使用 MPM 将传感器建模为粒子集合，每个粒子携带体积、质量、位置、速度、变形梯度等物理量
- 物理参数 θ = (E, ν)（杨氏模量和泊松比）通过可微仿真优化
- 标定流程：
  - 收集 19 段真实压痕视频（OptiTrack 追踪压头位置）
  - 用 Abaqus FEA 生成伪真值网格变形（因直接采集形变点云受遮挡和噪声影响）
  - 通过最小化 Chamfer distance 进行可微优化，取所有序列的中位数
  - 优化参数：学习率 0.1，30 次迭代，对 E 取 log 参数化
- MPM 后端使用 NVIDIA Warp，支持 GPU 加速

**阶段 2：光学渲染 (Section III-B)**
- 从仿真传感器中放置虚拟相机，渲染深度图和表面法线图
- 将法线+深度（4 通道）输入 DeepLabV3 ResNet50 网络
- 核心创新：预测**残差图像**（接触帧 - idle 帧），而非直接回归接触图像
- 最终输出 = 残差图像 + 真实 idle 帧
- 训练：ℓ2 loss，batch size 8，lr 3e-4，weight decay 1e-4，Adam，100 epochs

### RL 扩展 (Section IV-D)
- 在可微 DenseTact 环境中训练 PPO agent（SKRL 库）
- 离散 2-DoF 动作空间（9 个平面速度命令）
- ResNet-18 编码光学图像，策略/价值头共享 backbone
- 15 分钟内收敛


## Experiments

### 传感器与硬件
- **传感器**：DenseTact 2.0（半球形硅胶凝胶，表面有随机图案和反射涂层）
- **机械臂**：xArm 7
- **追踪系统**：OptiTrack marker tracking
- **GPU**：A5000（标定）、A6000（仿真运行）
- **压头**：6 个不同几何形状的压头

### 实验 1：物理形变精度 (Table II)
对比 DOT-Sim、Tacto、Taxim 与 DenseTact 真实点云的偏差（Medium 设置，所有压头）：

| Method | L2 CD (mm↓) | Sig. L2 CD (mm↓) | EMD (mm↓) | F-Score@1mm↑ |
|--------|-------------|-------------------|------------|---------------|
| Tacto | 1.77 | 4.21 | 1.33 | 63.59 |
| Taxim | 1.74 | 3.97 | 1.31 | 64.69 |
| DOT-Sim | **1.71** | **3.82** | **1.29** | **69.89** |

DiffTactile 的 FEM 仿真过于刚性，无可见变形，无法进行有意义的对比。

### 实验 2：光学渲染精度 (Table III)
三种难度设置下的 PSNR 对比：

| Setting | DiffTactile | Tacto | DOT-Sim |
|---------|-------------|-------|---------|
| Easy | 28.73 | 26.97 | **32.12** |
| Medium | 22.89 | 26.35 | **31.39** |
| Hard | 21.31 | 26.79 | **30.48** |

DOT-Sim 平均 PSNR 比最强 baseline 提升 17.34%。

### 实验 3：消融 — 残差预测 (Table IV)
Hard 设置下残差预测 vs 直接回归：

| Method | PSNR↑ | Sig. L2 (×10⁻²)↓ |
|--------|-------|-------------------|
| w/o Residual | 28.89 | 5.39 |
| DOT-Sim | **30.48** | **4.53** |

### 实验 4：Sim-to-Real 压头分类 (Table V)

| Method | In-domain (%) | Out-of-domain (%) |
|--------|---------------|-------------------|
| DiffTactile | 65.88 | 52.94 |
| Tacto | 50.59 | 50.59 |
| DOT-Sim | **90.48** | **81.18** |

### 实验 5：肿瘤检测 (Table VI)

| Method | Skin 1 (%) | Skin 2 (%) | Skin 3 (%) |
|--------|------------|------------|------------|
| DiffTactile | 52.78 | 46.15 | 51.72 |
| Tacto | 38.89 | 46.15 | 44.83 |
| DOT-Sim | **80.56** | **92.31** | **96.55** |

### 实验 6：Sim-to-Real 轨迹跟踪
- 行为克隆训练 ResNet-18 策略，输出 6-DoF 速度指令
- 多线程部署：图像采集 25Hz、推理 ~3.9ms、笛卡尔控制 100Hz
- 10 次试验平均误差 0.896±0.031 mm

### 实验 7：RL 盒子重定位
- PPO agent，离散 2-DoF 动作空间（9 个平面速度）
- 目标：将盒子旋转至 10° 偏航角，误差 <2° 为成功
- 15 分钟内收敛

### 运行时间 (Table VII)
- 默认配置：~3.6 FPS（A6000）
- 可通过降低体素分辨率/子步数达到 ~17 FPS，PSNR 仅降低约 1 点


## Limitations

1. **OOD 几何泛化差**：对尖锐边缘和精细表面细节的压头，仿真与真实接触对齐仍有偏差
2. **计算开销大**：默认配置仅 ~3 FPS，限制实时控制应用（可通过参数调节至 ~17 FPS，但有精度损失）
3. **DiffTactile 对比不充分**：其开源代码的 FEM 仿真过于刚性，且缺少系统辨识实现，无法完整对比
4. **依赖 Abaqus**：物理标定需要商用 FEA 软件生成伪真值，增加了复现门槛
5. **仅验证 DenseTact 2.0**：未在 GelSight、DIGIT 等其他主流传感器上验证


## Key Takeaways

1. **MPM > FEM 用于触觉仿真**：MPM 天然支持大变形和非线性材料行为，比 FEM 更适合柔性触觉传感器建模，且可通过可微仿真高效标定
2. **残差预测是关键技巧**：触觉图像大部分区域在接触过程中保持静态，预测残差而非原始图像可显著提升渲染精度，这一思路可推广到其他视觉仿真场景
3. **对我们的 DLO 操控研究的启发**：
   - 如果将 DLO 与触觉传感结合，DOT-Sim 的物理+光学仿真框架可以作为基础
   - 残差预测的思路可应用于 DLO 的视觉仿真（DLO 接触场景中背景也大多静态）
   - 可微仿真 + 少量真实演示的标定范式与我们的 Sim-to-Real 目标高度契合
4. **零样本迁移能力强**：在 out-of-domain 分类上仍达到 81.18%，说明仿真保真度足够支撑策略迁移

## 相关概念

- [[imitation-learning]]
- [[reinforcement-learning]]
- [[sim-to-real]]
- [[deformable-linear-object]]
- [[tactile-sensing]]

## 相关研究者

- [[you|You, Yang]]
- [[swann|Swann, Aiden]]
- [[antonova|Antonova, Rika]]
