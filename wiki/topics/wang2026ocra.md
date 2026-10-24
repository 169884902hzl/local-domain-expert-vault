---
title: "OCRA: Object-centric learning with 3D and tactile priors for human-to-robot action transfer"
tags: [manipulation, imitation, VLM, diffusion, diffusion-model]
created: "2026-05-08"
updated: "2026-05-08"
type: "literature"
status: "done"
summary: "提出OCRA框架，通过多视角RGB重建物体中心3D表征、百万级触觉图像预训练触觉编码器、ResFiLM融合模块和扩散策略，实现从人类示范视频到机器人的动作迁移，在7项真实世界操控任务中达到85%-90%成功率。"
authors: "Wang, Kuanning; Fan, Ke; Fu, Yuqian; Lin, Siyu; Luo, Hu et al."
year: "2026"
venue: "arXiv Preprint"
zotero_key: "IZUQQFG6"
---
## 摘要

We present OCRA, an Object-Centric framework for video-based human-to-Robot Action transfer that learns directly from human demonstration（示范数据） videos to enable robust manipulation（操控）. Object-centric learning emphasizes task-relevant objects and their interactions while filtering out irrelevant background, providing a natural and scalable way to teach robots. OCRA leverages multi-view RGB videos, the state-of-the-art（现有最优方法） 3D foundation model VGGT, and advanced detection and segmentation models to reconstruct object-centric 3D point clouds, capturing rich interactions between objects. To handle properties not easily perceived by vision alone, we incorporate tactile（触觉） priors via a large-scale dataset of over one million tactile（触觉） images. These 3D and tactile（触觉） priors are fused through a multimodal（多模态） module (ResFiLM) and fed into a Diffusion Policy（扩散策略） to generate robust manipulation（操控） actions. Extensive experiments on both vision-only and visuo-tactile（触觉） tasks show that OCRA significantly outperforms existing baselines and ablations, demonstrating its effectiveness for learning from human demonstration（示范数据） videos.

## 中文简述

提出基于扩散策略的绳索操控方法。

**研究方向**: 机器人操控、模仿学习、视觉-语言模型、扩散模型、扩散模型

## 关键贡献

1. **多视角物体中心学习**：从多视角人类示范视频中提取物体中心3D表征，通过VGGT重建+GroundingDINO/SAM2分割过滤背景干扰，捕捉物体间交互
2. **3D与触觉先验融合**：结合VGGT生成的3D物体中心表征和百万级触觉图像预训练的触觉编码器，通过ResFiLM融合模块和扩散策略生成精确操控动作
3. **大规模实验验证**：在4项纯视觉任务和3项视觉-触觉任务上验证，显著优于baselines和消融变体
## 结构化提取

- Problem: 从人类示范视频（非遥操作）直接学习机器人操控策略，需要解决视角差异、3D几何缺失和触觉感知不足的问题
- Method: OCRA框架——多视角RGB + VGGT 3D重建 + GroundingDINO/SAM2物体中心分割 + 百万级MAE预训练触觉编码器 + ResFiLM融合 + SE(3)扩散策略
- Tasks: 7项真实世界操控任务——Stacking, Scooping Ball, Pouring Water, Sweeping（纯视觉）; Move Fragile Cup, Weight Sorting, Texture Sorting（视觉-触觉）
- Sensors: 2×RealSense D455 RGB相机（第三人称多视角）+ 自研光学触觉传感器（类GelSight，嵌入示踪粒子）
- Robot Setup: FAIRINO Robot 5（5-DOF）+ Jodell平行夹爪（配备触觉传感器）
- Metrics: 10次试验成功率（人工判定）；失败分类为过程失败（轨迹不完整）和结果失败（轨迹完整但结果错误）
- Limitations: 刚体运动假设（不适用DLO）、需文本提示指定物体、仅5-DOF机器人验证、推理延迟未评估、触觉传感器迁移性未讨论
- Evidence Notes: 全文可获取。所有实验结果均来自真实世界操控（非仿真）。Tab.I-V提供定量结果，Fig.3/5/6提供定性可视化。消融实验验证了触觉预训练和ResFiLM融合模块的必要性。视角泛化实验（10/10成功）和深度对比实验（VGGT优于GT深度）提供了额外证据。
## 本地引用关系

-
## 证据元数据

- Fulltext Quality: fulltext
- Evidence Coverage: 完整覆盖方法论、实验结果、消融分析；补充实验含视角泛化、深度对比、示教效率
- Confidence: high
- Summary: 提出OCRA框架，通过多视角RGB重建物体中心3D表征、百万级触觉图像预训练触觉编码器、ResFiLM融合模块和扩散策略，实现从人类示范视频到机器人的动作迁移，在7项真实世界操控任务中达到85%-90%成功率。


## Problem

如何直接从人类示范视频（而非遥操作数据）学习鲁棒的机器人操控策略？现有方法面临三个核心挑战：
1. **接口限制**：基于专用接口（如UMI）的方法受限于第一人称视角；基于6-DOF姿态的方法需要物体先验知识，限制可操控物体范围
2. **3D几何缺失**：单目RGB缺乏空间几何信息，无法捕捉物体间丰富交互
3. **视觉盲区**：仅靠视觉无法感知物体的触觉属性（纹理、重量、脆弱性），限制了精细操控能力


## Method

### 整体流程
1. **数据采集**：使用2个外部RGB相机（RealSense D455）捕捉第三人称多视角人类示范视频；使用3D打印便携式触觉夹爪采集触觉数据
2. **物体中心3D先验提取**：
   - 使用VGGT从多视角RGB重建3D场景（深度图、点云图、像素级跟踪）
   - 通过双视角度量深度预测校准尺度模糊性
   - GroundingDINO生成初始帧目标框 → SAM2进行实时分割跟踪
   - 分割为被操控物体掩码（M_manip）和上下文物体掩码（M_ctx）
   - 反投影得到3D物体点云 P_manip/P_ctx
   - 使用DP3风格的Geometric Encoder提取点云特征
   - ICP算法计算相邻帧间SE(3)变换
3. **触觉先验提取**：
   - 光学触觉传感器（类GelSight）：弹性体+示踪粒子，通过DIS光流算法提取位移场，U-Net解耦为3D力向量
   - 百万级触觉图像数据集：覆盖多样物体、抓取力、姿态和任务
   - ViT-based触觉编码器：MAE自监督预训练（不使用自然图像预训练权重）
4. **ResFiLM融合模块**：
   - 点云特征f_pc和触觉特征f_t投影到公共隐空间
   - 基于视觉特征生成FiLM参数(γ, β)调制触觉特征：f_t' = γ·f_t + β
   - 门控残差连接：f_oc = f_pc + α(γ⊙f_t + β)，α为可学习缩放系数
5. **扩散策略**：
   - 在SE(3)变换空间建模未来物体运动分布
   - 预测物体刚体运动而非关节空间动作，解耦机器人构型
   - 条件输入为融合后的物体中心特征f_oc
6. **机器人控制**：
   - 利用外部相机外参将物体运动从相机坐标系转到机器人坐标系
   - SE(3)变换传递到夹爪
   - PID力控制器：以示范中预测的接触力为参考，触觉反馈维持稳定抓取


## Experiments

### 硬件配置
- GPU: NVIDIA RTX 6000 Ada（策略训练/评估），NVIDIA A800（触觉编码器预训练）
- 机器人: FAIRINO Robot 5 + Jodell Gripper
- 相机: 2× RealSense D455
- 每个任务采集20-40个人类示范

### 纯视觉任务（Tab. I）
| 任务 | OCRA | DP(RGB) | DP(w/o OC) |
|------|------|---------|------------|
| Stacking | 100% | 0% | 10% |
| Scooping | 70% | 0% | 0% |
| Pouring | 70% | 0% | 30% |
| Sweeping | 100% | 90% | 50% |
| **平均** | **85.0%** | **22.5%** | **22.5%** |

OCRA完全消除了过程失败（process failures），而baselines主要受困于此。

### 视觉-触觉任务（Tab. II）
| 任务 | OCRA(含触觉) | OCRA(无触觉) |
|------|-------------|-------------|
| Fragile Cup | 90% | 60% |
| Weight Sort | 90% | 30% |
| Texture Sort | 90% | 30% |
| **平均** | **90%** | **40%** |

### 消融实验（Tab. III, Texture Sort任务）
| 变体 | 成功率 | 过程失败 | 结果失败 |
|------|--------|---------|---------|
| OCRA完整 | 90% | 0% | 10% |
| 无触觉预训练 | 30% | 20% | 50% |
| 无ResFiLM融合 | 30% | 40% | 30% |

### 视角泛化
更换一台相机为未见视角，Stacking任务10/10成功，即使物体部分超出视野仍保持稳定。

### 深度对比（Tab. V）
| 任务 | OCRA(VGGT重建) | GT深度 |
|------|---------------|--------|
| Stack | 100% | 60%(单视角) |
| Texture Sort | 90% | 50%(双视角) |

VGGT重建的深度反而优于GT深度，因GT深度图存在空洞和噪声。

### 示教效率（Tab. IV）
人类示范每任务仅需~8秒（触觉任务~5秒），遥操作需~20秒，且遥操作无法完成Scoop/Pour/触觉任务。


## Limitations

1. 仅使用双目相机，更多视角的扩展性未验证
2. 物体分割依赖GroundingDINO的文本提示，需要人工指定目标物体
3. ICP配准假设刚体运动，不适用于DLO等可变形物体
4. 每个任务仍需20-40次示范，few-shot能力有限
5. 实验仅在低自由度机器人（FAIRINO 5，5-DOF）上验证，未在更复杂的双臂或高自由度平台测试
6. 扩散策略推理延迟问题未讨论，实时性未知
7. 触觉传感器的可泛化性未讨论——仅用一种自研传感器，迁移到其他触觉传感器的能力不明确
8. 对动态/快速运动场景的鲁棒性未评估


## Key Takeaways

### 对DLO操控的启示
- OCRA的ICP变换估计假设刚体运动，**不直接适用于DLO**。但物体中心分割+3D重建的范式可借鉴：对DLO进行分段建模（将DLO视为多个刚体段的连接）可能是一种扩展方向
- 多视角重建 + 扩散策略的组合已被验证对非刚性物体（如倒水）有效，这对DLO操控有间接参考价值

### 对VLM-based控制的启示
- GroundingDINO + SAM2 的开放世界检测/分割链路可替代VLM作为物体识别前端，成本更低
- ResFiLM融合模块（视觉特征生成调制参数，触觉特征作为残差修正）是轻量级多模态融合的好设计，可推广到视觉+力传感器/视觉+语言指令等场景

### 对Sim-to-Real的启示
- VGGT生成的重建深度优于GT深度，说明3D基础模型的几何先验可弥补传感器噪声——这在Sim-to-Real中可减少sim-real感知差距
- 人类示范采集仅需8秒/次，远快于遥操作，可大幅降低数据采集成本

## 相关概念

- [[robotic-manipulation]]
- [[imitation-learning]]
- [[vision-language-model]]
- [[diffusion-model]]
- [[deformable-linear-object]]
- [[tactile-sensing]]
- [[bimanual-manipulation]]
- [[grasping]]

## 相关研究者

- [[wang-kuanning|Wang, Kuanning]]
- [[fu-yuqian|Fu, Yuqian]]
