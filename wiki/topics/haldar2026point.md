---
title: "Point bridge: 3D representations for cross domain policy learning"
tags: [manipulation, imitation, VLM, sim-to-real, robot-learning]
created: "2026-05-11"
updated: "2026-05-11"
type: "literature"
status: "done"
summary: "利用 VLM 引导的自动化点云提取管线和统一的 3D 点表示，实现零样本 Sim-to-Real 策略迁移，在 6 个真实世界操控任务中比图像基线提升最高 66%。"
authors: "Haldar, Siddhant; Johannsmeier, Lars; Pinto, Lerrel; Gupta, Abhishek; Fox, Dieter et al."
year: "2026"
venue: "arXiv Preprint"
zotero_key: "M6ECK8AK"
---
## 摘要

Robot foundation models are beginning to deliver on the promise of generalist robotic agents, yet progress remains constrained by the scarcity of large-scale real-world manipulation（操控） datasets. Simulation and synthetic data generation offer a scalable alternative, but their usefulness is limited by the visual domain gap between simulation and reality. In this work, we present Point Bridge, a framework that leverages unified, domain-agnostic point-based representations to unlock synthetic datasets for zero-shot（零样本） sim-to-real（仿真到真实迁移） policy transfer, without explicit visual or object-level alignment. Point Bridge combines automated point-based representation extraction via Vision-Language Models (VLMs), transformer-based policy learning, and efficient inference-time pipelines to train capable real-world manipulation（操控） agents using only synthetic data. With additional co-training on small sets of real demonstrations, Point Bridge further improves performance, substantially outperforming prior vision-based sim-and-real co-training methods. It achieves up to 44% gains in zero-shot（零样本） sim-to-real（仿真到真实迁移） transfer and up to 66% with limited real data across both single-task and multitask settings. Videos of the robot are best viewed at: https://pointbridge3d.github.io/

## 中文简述

提出基于视觉-语言的操控方法，具有仿真到真实迁移特点。

**研究方向**: 机器人操控、模仿学习、视觉-语言模型、仿真到真实迁移、机器人学习

## 关键贡献

1. **Point Bridge 框架**：提出统一领域无关的点云表示，实现零样本 sim-to-real 策略迁移，无需显式视觉或物体级对齐
2. **VLM 引导的点提取管线**：结合 Gemini（物体识别）→ Molmo（定位）→ SAM2（分割追踪）→ FoundationStereo（深度估计）→ 最远点采样，自动化提取任务相关 3D 点
3. **多种推理时深度策略**：支持 FoundationStereo 立体匹配、RGB-D 传感器、双 RGB 相机三角化（MAST3R + Co-Tracker），灵活适配不同硬件
4. **强实验验证**：单任务零样本迁移提升 39%，多任务提升 44%；co-training 后分别提升 61% 和 66%
5. **系统消融分析**：覆盖深度估计策略、相机视角对齐、背景干扰物、未见物体、点数、动作表示等关键设计选择
## 结构化提取

- **Problem**: 仿真数据因视觉域间隙无法直接用于真实世界策略训练；现有方法需精心对齐仿真与真实
- **Method**: Point Bridge — VLM 引导的自动化 3D 点云提取 + PointNet/BAKU transformer 策略 + 多种推理时深度方案
- **Tasks**: 6 个真实操控任务（bowl on plate, mug on plate, stack bowls, fold towel, close drawer, put bowl in oven）
- **Sensors**: ZED 2i 立体相机（FoundationStereo 深度），Intel RealSense RGB-D
- **Robot Setup**: Franka Research 3 单臂 + Franka Hand 夹爪，Deoxys 20Hz 控制器
- **Metrics**: 成功率（每配置 10 rollouts × 3 object pairs = 30 次评估）
- **Limitations**: 依赖 VLM 准确性；需相机标定对齐；丢失场景上下文；控制频率 5Hz 较低
- **Evidence Notes**: 1410 次真实 rollout；单任务零样本提升 39%，多任务 44%；co-training 后分别 61%/66%；real-only soft/articulated 物体 85%；VLM 管线 60 次测试仅 2 次失败；未见物体 97% 成功率
## 本地引用关系

- [[chi2024diffusion]]
## 证据元数据

- Fulltext Quality: fulltext (via arXiv HTML)
- Evidence Coverage: 完整覆盖主文和附录，包括方法、实验、消融分析
- Confidence: high
- Summary: 利用 VLM 引导的自动化点云提取管线和统一的 3D 点表示，实现零样本 Sim-to-Real 策略迁移，在 6 个真实世界操控任务中比图像基线提升最高 66%。

## Problem

机器人基础模型的进展受限于大规模真实世界操控数据集的稀缺性。仿真数据生成是可扩展的替代方案，但仿真与真实之间存在显著的视觉域间隙（visual domain gap），导致直接迁移失败。图像表示策略在零样本 sim-to-real 设置下几乎完全失败。现有的关键点方法（如 Point Policy）依赖人工标注，难以扩展到多任务场景。

## Method

### 整体流程
1. **数据生成**：少量人类演示 → MimicGen 扩展为大规模仿真数据集（5 demos × 4 object pairs → 1200 demos/task）
2. **点云提取**：
   - **仿真端**：直接从物体 mesh 采样，使用真实相机内外参投影以匹配真实视角，加 1cm 高斯噪声模拟传感器噪声
   - **真实端**：VLM 管线（Gemini-2.5-flash 识别物体 → Molmo-7B 定位像素 → SAM2 分割追踪 → FoundationStereo 深度 → 投影 3D → 最远点采样）
   - **机器人表示**：末端执行器姿态通过刚性变换生成多个关键点
3. **策略学习**：基于 BAKU 架构的 decoder-only transformer，PointNet 编码点云，MiniLM 编码语言指令，MSE 损失训练，action chunking + 指数时间平滑
4. **推理部署**：初始化时运行 VLM 管线（~9s），后续步骤仅 SAM2 追踪 + 深度估计（~0.115s/step）

### 关键设计细节
- 每个物体 128 个点（消融显示 64-128 均可，>86% 成功率）
- mask 收缩 20% 减少边界噪声
- FoundationStereo 对反光/透明物体优于 RGB-D
- 仿真-真实数据 co-training 比例 80:20

## Experiments

### 实验设置
- **机器人**：Franka Research 3 + Franka Hand
- **任务**：6 个真实任务（3 sim-to-real + 3 real-only）
  - Sim-to-real: bowl on plate, mug on plate, stack bowls
  - Real-only: fold towel, close drawer, put bowl in oven
- **数据**：每任务 1200 sim demos + 45 real demos（co-training）；real-only 任务 20 demos
- **传感器**：Intel RealSense RGB-D + ZED 2i 立体相机
- **总评估**：1410 次真实世界 rollout
- **控制频率**：Point Bridge 5 Hz，图像基线 15 Hz

### 主要结果

**单任务零样本 Sim-to-Real（Table 1）**：
- Point Bridge 相比最强基线提升 ~39%
- Co-training 后提升 ~61%
- 图像基线在零样本设置下基本失败（不报告）

**多任务零样本 Sim-to-Real（Table 2）**：
- Point Bridge 提升 ~44%
- Co-training 后提升 ~66%
- 多任务策略与单任务相当或更好

**Real-only 任务（Table 3）**：
- Soft/articulated 物体平均 85% 成功率
- 证明表示方法不限于刚性物体

### 消融分析（Table 4-10）
- **深度策略**：FoundationStereo > RGB-D > 三角化（MAST3R 噪声大，Co-Tracker 慢至 2.5 Hz）
- **相机视角**：匹配视角优于随机视角（~47% vs 更高），但随机视角仍可行
- **背景干扰**：BAKU-PCD 在有干扰物时 0% 成功率；Point Bridge 完全鲁棒
- **未见物体**：多任务 co-training 在完全未见物体上达 97% 成功率
- **点数**：10/64/128 均超 86%，64 最优
- **动作表示**：pose regression 与 point track prediction 表现相当（大数据集下差异不大）

### VLM 管线鲁棒性
- 3 任务 × 20 随机位置：仅 2 次失败（金属碗被夹爪遮挡 1 次，小碗未被 Molmo 定位 1 次）

## Limitations

1. **依赖 VLM/VFM**：受限于 Gemini、Molmo、SAM2 的失败模式，杂乱场景或多相似物体时错误率可能上升
2. **需相机姿态对齐**：仿真和真实的相机视角需一致，否则性能下降；可通过随机化仿真视角缓解
3. **丢失场景上下文**：点云抽象过滤掉背景信息，杂乱环境中表现受限
4. **低控制频率**：5 Hz vs 图像基线 15 Hz，可能限制动态场景表现

## Key Takeaways

1. **领域无关表示是 sim-to-real 的关键**：点云表示天然消除视觉域间隙，比域随机化或 photo-realistic 仿真更优雅
2. **VLM 管线替代人工标注**：Gemini+Molmo+SAM2 组合实现了全自动点云提取，是向可扩展迁移的重要一步
3. **FoundationStereo 对反光物体有效**：在操控场景中优于传统 RGB-D 深度
4. **对 DLO 操控的启示**：论文在 fold towel（soft object）上已展示 85% 成功率，表明点表示可能扩展到 DLO；但 VLM 管线对细长、可变形物体的分割和追踪仍是开放问题
5. **MimicGen + Point Bridge 组合**：少量人类演示即可生成大量仿真训练数据并直接迁移到真实，极大降低数据门槛

## 相关概念

- [[robotic-manipulation]]
- [[imitation-learning]]
- [[vision-language-model]]
- [[sim-to-real]]
- [[robot-learning]]
- [[deformable-linear-object]]
- [[grasping]]

## 相关研究者

- [[haldar-siddhant|Haldar, Siddhant]]
- [[pinto-lerrel|Pinto, Lerrel]]
