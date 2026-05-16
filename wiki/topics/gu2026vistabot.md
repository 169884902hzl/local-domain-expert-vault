---
title: "VistaBot: View-robust robot manipulation via spatiotemporal-aware view synthesis"
tags: [manipulation, diffusion, robot-learning, planning]
created: "2026-04-29"
updated: "2026-04-29"
type: "literature"
status: "done"
summary: "VistaBot 通过融合前馈几何模型（VGGT）与视频扩散模型（CogVideoX），将任意视角观测投影回训练视角并在潜空间中执行策略，实现无需相机标定的跨视角闭环操控，VGS 提升 ACT 2.79×、π₀ 2.63×。"
authors: "Gu, Songen; Zheng, Yuhang; Li, Weize; Zheng, Yupeng; Feng, Yating et al."
year: "2026"
venue: "arXiv Preprint"
zotero_key: "FXDXFRHQ"
---
## 摘要

Recently, end-to-end（端到端） robotic manipulation（机器人操控） models have gained significant attention for their generalizability and scalability. However, they often suffer from limited robustness to camera viewpoint changes when training with a fixed camera. In this paper, we propose VistaBot, a novel framework that integrates feed-forward geometric models with video diffusion（扩散） models to achieve view-robust closed-loop（闭环） manipulation（操控） without requiring camera calibration at test time. Our approach consists of three key components: 4D geometry estimation, view synthesis latent extraction, and latent action learning. VistaBot is integrated into both action-chunking (ACT) and diffusion（扩散）-based ($π_0$) policies and evaluated across simulation and real-world tasks. We further introduce the View Generalization Score (VGS) as a new metric for comprehensive evaluation of cross-view generalization. Results show that VistaBot improves VGS by 2.79$\times$ and 2.63$\times$ over ACT and $π_0$, respectively, while also achieving high-quality novel view synthesis. Our contributions include a geometry-aware synthesis model, a latent action planner, a new benchmark metric, and extensive validation across diverse environments. The code and models will be made publicly available.

## 中文简述

提出基于扩散模型的操控方法，具有泛化能力特点。

**研究方向**: 机器人操控、扩散模型、机器人学习、运动规划

## 关键贡献

1. **4D 时空一致潜表示学习**：将前馈几何模型（VGGT）与视频扩散模型（CogVideoX）适配到机器人闭环控制中，无需相机位姿输入即可生成新视角的 4D 时空一致潜表示
2. **潜空间动作规划器**：策略直接在 VDM 潜特征上操作，利用扩散模型中已有的物体级和几何理解，省去 VAE 解码和视觉编码开销
3. **View Generalization Score (VGS)**：新评估指标，量化策略在视角变化下的鲁棒性，填补现有 benchmark 空白
4. **跨框架验证**：在 specialist（ACT）和 generalist（π₀）框架上、仿真和真实环境中均进行广泛验证
## 结构化提取

- **Problem**: 端到端操控策略对相机视角变化缺乏鲁棒性，视角偏移导致视觉特征分布偏移（OOD），闭环推理中误差累积使策略失效
- **Method**: VistaBot — 三阶段流水线：①VGGT 估计深度+相对位姿 → 点云反投影到训练视角 → ②CogVideoX 视频扩散模型进行视角合成潜特征提取（含空间插值+时序记忆） → ③在 VDM 潜空间直接学习闭环动作
- **Tasks**: RLBench 8 任务（仿真） + Franka FR3 4 任务（真实）：包括开合容器、按钮、堆叠、拔插等桌面操控
- **Sensors**: 仅 RGB 相机（训练时单视角，测试时任意视角），无需深度相机或相机标定
- **Robot Setup**: 仿真（RLBench）；真实 Franka FR3 7-DoF + parallel gripper + 3× RealSense D435
- **Metrics**: Average Success Rate (Avg. S.R.), View Generalization Score (VGS = avg S(θᵢ)/S(θ₀)), FVD, FID, SSIM, PSNR, LPIPS
- **Limitations**: 严重遮挡场景合成质量差；推理速度 ~3 Hz 限制高速任务；几何估计精度仍有提升空间；未测试超过 ±45° 的视角变化；未讨论 DLO/柔性物体场景
- **Evidence Notes**: 所有定量数据来自论文 Table I-IV，仿真每视角 25 次评估，真实机器人每视角 25 次评估。消融实验在 ACT 框架上进行。未提供 π₀ 框架的消融数据。
## 本地引用关系

-
## 证据元数据

- Fulltext Quality: fulltext (arXiv PDF 完整转换)
- Evidence Coverage: 高 — 包含完整的 Method/Experiments/Ablation/Real-World 实验细节，所有表格数据可读
- Confidence: high
- Summary: VistaBot 通过融合前馈几何模型（VGGT）与视频扩散模型（CogVideoX），将任意视角观测投影回训练视角并在潜空间中执行策略，实现无需相机标定的跨视角闭环操控，VGS 提升 ACT 2.79×、π₀ 2.63×。


## Problem

端到端机器人操控策略（如 ACT、π₀）在固定相机视角下训练后，面对测试时相机视角变化会出现严重性能下降。核心问题：视角变化导致视觉特征分布偏移（OOD），使策略预测动作偏离正确轨迹，闭环推理中误差累积导致任务失败。现有方案要么依赖多相机标定（重建方法），要么缺乏动作学习且推理效率低（生成方法）。


## Method

### 整体架构（Fig. 2）
三模块流水线：4D Geometry Estimation → View Synthesis Latent Extraction → Closed-loop Action Learning

### 1. 4D Geometry Estimation
- 使用 VGGT（Visual Geometry Grounded Transformer）预测相对位姿 Tn→t 和深度图 Dn
- 在仿真和真实数据上微调 VGGT，解决类别特定物体（机械臂/夹爪）的几何估计问题
- 将新视角图像反投影为点云 Pn，变换到训练视角坐标系得到 Pt，再渲染为图像 Ir
- 关键公式：Pt = Tn→t · proj⁻¹(In, Dn, K)

### 2. Spatial-temporal Latent Feature Extraction
基于 CogVideoX（3D VAE + DiT），三个子模块：
- **Point Rendering Inpainting**：点云渲染图 Ir 有孔洞，用投影掩码 Mr 标记缺失区域，条件化 VDM 进行修复
- **Spatial Viewpoint Interpolation**：在新旧视角间插值相机位姿（T = tTn + (1-t)Tt），逐帧渲染生成平滑过渡序列，提供空间上下文
- **Temporal Memory Reference**：缓存上一步推理的观测帧，用 3D VAE 编码为时间 token；通过 cross-attention DiT block（空间 token 为 Q，时间 token 为 KV）注入历史信息，实现闭环时序一致性

### 3. Closed-loop Action Learning
- 不使用解码后的合成图像，直接从 VDM 最终 DiT block 的 adaptive layer norm 后提取场景特征 Fobs
- 替换 ACT 中的 ResNet-50 特征，保留原有机器人状态特征 Fstate 和 action chunks
- 好处：①VDM 潜空间已包含物体级语义和几何理解 ②省去 VAE 解码 + 视觉编码两步开销

### 问题设定
- 训练：仅使用固定相机位姿 Tt 下的 RGB 观测 {It}
- 推理：从任意新位姿 Tn¹, Tn², ..., Tnᵐ 进行闭环操控，无需相机标定或位姿信息


## Experiments

### 仿真实验（RLBench）
- **任务**：8 个代表性任务（close box, close laptop, meat on grill, open box, push buttons, stack wine, take lid off, toilet seat down）
- **数据**：每任务 50 demonstrations，仅前摄像头 RGB
- **测试**：±30° 和 ±45° 视角变化，每视角 25 次评估
- **基线性能下降**：ACT 平均成功率从 0.83 降至 0.13（-45°），降幅约 84%

**Table I 核心结果**：
| Base Policy | Setting | Avg. VGS |
|---|---|---|
| ACT | Default (无 VistaBot) | 0.24 |
| ACT | Ours | **0.67** |
| π₀ | Default | 0.33 |
| π₀ | Ours | **0.87** |

### 真实机器人实验
- **平台**：Franka FR3 7-DoF 机械臂 + RealSense D435 ×3
- **任务**：box on shelf, place banana, push cube, unplug charger
- **训练**：每任务 50 trajectories，前摄像头
- **测试**：左右摄像头（±45°），每视角 25 次
- **推理速度**：~3 Hz

**Table III 核心结果**：
| Base Policy | Setting | Avg. VGS |
|---|---|---|
| ACT | Default | 0.21 |
| ACT | Ours | **0.72** |
| π₀ | Default | 0.27 |
| π₀ | Ours | **0.79** |

### 视角合成质量（Table II）
与 AnySplat（4 视角输入）和 LangScene-X 对比：
| Method | FVD↓ | FID↓ | SSIM↑ | PSNR↑ | LPIPS↓ |
|---|---|---|---|---|---|
| AnySplat | 825.83 | 102.71 | 0.27 | 12.07 | 0.23 |
| LangScene-X | 551.91 | 118.34 | 0.44 | 15.02 | 0.17 |
| **Ours** | **471.04** | **69.56** | **0.59** | **18.34** | **0.09** |

### 消融实验（Table IV）
| Method | VGS |
|---|---|
| ACT baseline | 0.24 |
| VistaBot (ours) | 0.67 |
| w/ GT Depth and extr. | 0.79 |
| w/o Memory | 0.48 |

GT 几何比估计几何高 0.12 VGS，说明几何估计仍有改进空间；Memory 模块贡献 0.19 VGS，对闭环控制至关重要。

### 特征分布分析（Fig. 8）
用 InceptionV3 + PCA 可视化：新视角特征（红）显著偏离训练视角（蓝），VistaBot 生成的视角特征（绿）紧密对齐训练分布，从 OOD 角度解释了性能提升的机理。


## Limitations

1. **严重遮挡**：在遮挡严重的场景下，无法生成高质量的合成视角
2. **推理速度**：~3 Hz 限制了对高速操控任务的适用性
3. **几何估计精度**：估计几何与 GT 几何之间仍有 0.12 VGS 差距（消融实验显示）
4. **视角范围**：仅测试了 ±45° 范围，更大视角偏移的效果未知
5. **未讨论**：对不同光照/纹理变化的鲁棒性；DLO 等柔性物体操控场景


## Key Takeaways

1. **核心思路——视角归一化**：不改变策略本身，而是通过"新视角→训练视角"的几何+扩散合成，将分布外观测拉回训练分布，思路简洁有效
2. **潜空间策略 > 解码后策略**：直接在 VDM 潜空间学习动作，比先解码再视觉编码更高效且语义更丰富，这个设计可推广到其他生成模型辅助的操控框架
3. **Memory 机制对闭环至关重要**：消融证明 cross-attention 历史注入贡献 0.19 VGS，这是时序一致性的关键
4. **VGS 指标设计简洁实用**：VGS = avg(S(θᵢ)/S(θ₀))，直接衡量"策略在视角变化下保留了多少性能"，适合作为视角鲁棒性的标准评估指标
5. **与我们研究的相关性**：VistaBot 的视角归一化思路可用于 DLO 操控中的多相机部署场景，但 DLO 的严重形变和遮挡会挑战几何估计和视角合成质量
6. **视频扩散模型的新用途**：CogVideoX 不用于生成视频预测未来，而是作为"视角翻译器"的潜空间编码器，为生成模型在机器人中的角色提供了新范式

## 相关概念

- [[robotic-manipulation]]
- [[diffusion-model]]
- [[robot-learning]]
- [[planning]]
- [[deformable-linear-object]]
- [[grasping]]

## 相关研究者

- [[gu|Gu, Songen]]
- [[zheng-yuhang|Zheng, Yuhang]]
- [[zheng-yupeng|Zheng, Yupeng]]
