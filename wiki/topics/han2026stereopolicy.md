---
title: "StereoPolicy: Improving robotic manipulation policies via stereo perception"
tags: [manipulation, imitation, VLM, diffusion, robot-learning]
created: "2026-05-12"
updated: "2026-05-12"
type: "literature"
status: "done"
summary: "提出 StereoPolicy 框架，通过 Stereo Transformer 融合双目图像对实现隐式 3D 几何推理，无需显式 3D 重建，在扩散策略和 VLA 模型上均一致优于 RGB/RGB-D/点云/多视角基线。"
authors: "Han, Evans; Jiang, Yunfan; Wang, Yingke; Xiao, Haoyue; Huang, Huang et al."
year: "2026"
venue: "arXiv Preprint"
zotero_key: "P8U4S2PB"
---
## 摘要

Recent advances in robot imitation learning（模仿学习） have yielded powerful visuomotor policies capable of manipulating a wide variety of objects directly from monocular visual inputs. However, monocular observations inherently lack reliable depth cues and spatial awareness, which are critical for precise manipulation（操控） in cluttered or geometrically complex scenes. To address this limitation, we introduce StereoPolicy, a new visuomotor policy learning framework that directly leverages synchronized stereo image pairs to strengthen geometric reasoning, without requiring explicit 3D reconstruction or camera calibration. StereoPolicy employs pretrained 2D vision encoders to process each image independently and fuses the resulting representations through a Stereo Transformer. This design implicitly captures spatial correspondence and disparity cues. The framework integrates seamlessly with diffusion（扩散）-based and pretrained vision-language-action (VLA) policies, delivering consistent improvements over RGB, RGB-D, point cloud（点云）, and multi-view baselines across three simulation benchmarks: RoboMimic, RoboCasa, and OmniGibson. We further validate StereoPolicy on real-robot experiments spanning both tabletop and bimanual（双臂） mobile manipulation（移动操控） settings. Our results underscore stereo vision as a scalable and robust modality that bridges 2D pretrained representations with 3D geometric understanding for robotic manipulation（机器人操控）.

## 中文简述

提出基于扩散模型的双臂方法。

**研究方向**: 机器人操控、模仿学习、视觉-语言模型、扩散模型、机器人学习

## 关键贡献

1. **StereoPolicy 框架**：首个直接消费同步双目图像对的视觉运动策略学习框架，无需显式 3D 重建或相机标定
2. **Stereo Transformer**：基于交替 self-attention 和 cross-attention 的双目特征融合模块，配合 2D RoPE 实现跨视角对应学习
3. **VLA 集成**：与扩散策略和预训练 VLA 模型（Pi0.5、GR00T N1.5）无缝集成，证明双目视觉可作为可扩展的模态
4. **硬件指导**：系统分析相机角度、双目基线距离比，发现最优基线约为目标距离的 10%（r ∈ [0.09, 0.13]）
5. **全面比较**：在 3 个仿真 benchmark 和 7 个真实任务上对比 RGB、RGB-D、点云、多视角基线
## 结构化提取

- **Problem**: 单目视觉运动策略缺乏可靠深度线索，显式 3D 表示（深度图/点云）噪声敏感、计算昂贵且泛化性差
- **Method**: 双目图像经共享权重 2D 编码器提取特征 → DINOv2 嵌入增强（仅外部视角）→ Stereo Transformer（交替 self/cross attention + 2D RoPE）隐式融合 → 拼接本体感知后输入策略骨干
- **Tasks**: 桌面操控（pick-and-place, insert, hang）+ 双臂移动操控（物体搬运, 设备操作）+ 仿真 benchmark 任务
- **Sensors**: ZED Mini 双目相机（外部视角 + wrist 视角）
- **Robot Setup**: Franka Emika 7-DoF 臂（桌面）、Galaxea R1 Pro（双臂移动操控）
- **Metrics**: 成功率 (Success Rate)，真实 20 次试验取平均，仿真每 50/250 epoch 做 50 次 rollout 取最高
- **Limitations**: 训练规模小，透明/反射物体成功率低，光照敏感，未在大规模数据集验证，wrist 视角 DINOv2 不兼容
- **Evidence Notes**: 全文实验证据完整，包含 3 仿真 benchmark + 7 真实任务，消融覆盖骨干选择/硬件配置/模块去除，延迟分析可复现。缺失：未测试相机振动场景，未在 Droid 等大规模数据集验证
## 本地引用关系

-
## 证据元数据

- Fulltext Quality: fulltext (arXiv HTML 2605.09989v1)
- Evidence Coverage: 完整覆盖（正文、附录、消融实验、硬件分析）
- Confidence: high
- Summary: 提出 StereoPolicy 框架，通过 Stereo Transformer 融合双目图像对实现隐式 3D 几何推理，无需显式 3D 重建，在扩散策略和 VLA 模型上均一致优于 RGB/RGB-D/点云/多视角基线。


## Problem

单目视觉输入在机器人模仿学习中缺乏可靠的深度线索和空间感知能力，导致在杂乱或几何复杂场景中操控精度不足。现有方法依赖显式 3D 表示（深度图、点云），但面临三大问题：
1. 显式 3D 表示对传感器噪声、标定误差和物体属性敏感，深度图丢失语义细节，点云受物体变形影响
2. 预训练 3D 视觉编码器远不如 2D 成熟，缺乏大规模 3D 数据集和可扩展的 3D 骨干架构
3. 显式 3D 重建引入大量计算开销，与实时控制需求矛盾


## Method

### 核心架构

**双目图像编码**：每个图像由 2D 视觉编码器 V_i(·) 独立处理，生成单视角特征图。左右编码器共享权重以保持几何一致性。对外部视角额外拼接 DINOv2 嵌入以增强几何推理（wrist 视角不拼接，因域不匹配会损害性能）。

**双目特征融合**：Stereo Transformer 采用交替注意力机制——self-attention 计算像素间注意力，cross-attention 计算左右图像间注意力。在 cross-attention 的 query/key 投影中应用 2D RoPE，鼓励显式跨视角对应学习。

**多视角聚合**：每个相机视角独立进行双目融合，结果嵌入与本体感知特征拼接后输入策略骨干网络。

### 两种变体

- **StereoPolicy-DP**：集成到扩散策略中从头训练。UNet 作为扩散骨干，ResNet18 + FPN 作为视觉编码器，BatchNorm 替换为 GroupNorm
- **StereoPolicy-VLA**：在预训练 VLA 模型（Pi0.5、GR00T N1.5）上微调，将单目视觉嵌入替换为双目感知表示

### 训练细节
- Diffusion Policy：batch size 64，lr 1e-4，观察 2 步，预测 16 步
- VLA 微调：8×H100，60K-80K 步
- Stereo Transformer：2 层，8 注意力头
- DINOv2 冻结，其余端到端训练


## Experiments

### 环境
- **仿真**：RoboMimic（ToolHang, Square, Transport），RoboCasa（24 厨房任务），OmniGibson（4 自定义任务）
- **真实桌面**：5 任务（Banana PnP, Toast Insert, Cup Hang, Steel Cup Hang, Glass Cup Hang），Franka 臂，200 demos/任务
- **真实双臂移动**：2 任务（Turn on Radio, PnP Toast），Galaxea R1 Pro，75 demos/任务

### 主要结果

**Q1: StereoPolicy-DP vs 其他视觉模态**
- 真实桌面：在所有 5 个任务上一致优于 RGB、RGB-D、点云、多视角
- 仿真：在 RoboMimic 和 OmniGibson 上全面领先
- 点云方法在真实环境中表现最差——深度噪声大，玻璃杯完全丢失
- RGB-D 和 PCD 在 Glass Cup Hang 上失败率 100%，StereoPolicy 显著更鲁棒
- 比 RGB 更数据高效：OmniGibson 上用更少 demo 达到更高 SR
- 超过多视角策略（验证 Stereo Transformer 的有效性，而非简单增加视角数量）

**Q2: StereoPolicy-VLA 增强**
- Pi0.5：300 demos 时 SR 从 70.31%→74.40%，30 demos 时 48.71%→51.72%
- GR00T N1.5：同样一致提升
- 移动操控：仿真和真实均优于单目基线，RGB 策略在精确操作（如手柄插入、按钮按压）上失败

**Q3: 硬件因素**
- 最优基线距离比 r = baseline/distance ∈ [0.09, 0.13]
- 典型桌面场景（0.6-0.8m 距离）：6cm 基线最佳
- 正面视角增益最大（+18%），侧面视角增益较小
- 移除 wrist 相机时 StereoPolicy 性能保持，RGB/RGB-D 立即下降

**Q4: 架构消融**
- 移除 Stereo Transformer：SR 从 0.94 降至 0.85
- 低数据场景下大预训练 VL 骨干（OpenCLIP-B/16, SigLIP-SO400M/14）显著优于 ResNet18
- 多尺度特征（FPN）对 Stereo Transformer 有益
- 推理延迟：仅增加 1.12×（从 621.66ms 到 698ms）


## Limitations

1. 训练规模较小，仅限桌面和移动操控场景
2. 透明/反射物体上绝对成功率仍然较低
3. 对光照条件敏感，强反射或不良照明下性能不稳定
4. 尚未在大型机器人数据集（如 Droid）上验证可扩展性
5. DINOv2 嵌入对 wrist 视角有负面影响（域不匹配），需要视角特异处理
6. 推理延迟虽仅增 12%，但在高频控制场景下仍需优化


## Key Takeaways

1. **隐式 > 显式 3D**：Stereo Transformer 隐式学习视差对应，避免了显式深度估计/点云重建的噪声敏感性，特别是在透明/反射物体上
2. **2D 预训练红利可迁移**：直接复用 2D 预训练编码器的泛化能力，无需大规模 3D 预训练数据
3. **对 DLO 操控的启发**：双目视觉对线状/柔性物体的深度感知可能优于单目，隐式融合避免了 DLO 表面重建困难
4. **硬件设计准则**：基线≈10% 目标距离的经验法则可直接应用于双臂 DLO 操控系统的相机配置
5. **模态轻量可集成**：Stereo Transformer 仅 2 层，可直接嵌入现有 diffusion policy 和 VLA 流水线

## 相关概念

- [[robotic-manipulation]]
- [[imitation-learning]]
- [[vision-language-model]]
- [[diffusion-model]]
- [[robot-learning]]
- [[deformable-linear-object]]
- [[bimanual-manipulation]]

## 相关研究者

- [[han-evans|Han, Evans]]
- [[wang-yingke|Wang, Yingke]]
