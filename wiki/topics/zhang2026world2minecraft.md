---
title: "World2Minecraft: Occupancy-driven simulated scenes construction"
tags: [imitation, VLM, RL, robot-learning]
created: "2026-05-01"
updated: "2026-05-01"
type: "literature"
status: "done"
summary: "提出 World2Minecraft 框架，通过 3D 语义占据预测将真实场景转换为可编辑的 Minecraft 环境，并构建 MinecraftOcc 大规模占据数据集和 MinecraftVLN 导航数据集，在 VLN 下游任务中验证了重建场景的实用性。"
authors: "Zhang, Lechao; Xu, Haoran; Gong, Jingyu; Wang, Xuhong; Xie, Yuan et al."
year: "2026"
venue: "arXiv Preprint"
zotero_key: "VJ6IFZ2I"
---
## 摘要

Embodied intelligence requires high-fidelity simulation environments to support perception and decision-making, yet existing platforms often suffer from data contamination and limited flexibility. To mitigate this, we propose World2Minecraft to convert real-world scenes into structured Minecraft environments based on 3D semantic occupancy prediction. In the reconstructed scenes, we can effortlessly perform downstream tasks such as Vision-Language Navigation(VLN). However, we observe that reconstruction quality heavily depends on accurate occupancy prediction, which remains limited by data scarcity and poor generalization in existing models. We introduce a low-cost, automated, and scalable data acquisition pipeline for creating customized occupancy datasets, and demonstrate its effectiveness through MinecraftOcc, a large-scale dataset featuring 100,165 images from 156 richly detailed indoor scenes. Extensive experiments show that our dataset provides a critical complement to existing datasets and poses a significant challenge to current SOTA methods. These findings contribute to improving occupancy prediction and highlight the value of World2Minecraft in providing a customizable and editable platform for personalized embodied AI research. Project page:https://world2minecraft.github.io/.

## 中文简述

提出基于视觉-语言的导航方法，具有泛化能力特点。

**研究方向**: 模仿学习、视觉-语言模型、强化学习、机器人学习

## 关键贡献

1. **World2Minecraft 管线**：基于 3D 语义占据预测，将真实世界场景端到端转换为结构化 Minecraft 环境，成本低且可编辑
2. **MinecraftVLN 数据集**：1,059 条重建场景样本 + 2,483 条社区场景样本，定义 Next-View 和 Next-Action 两个子任务，用于 VLN 验证
3. **自动化占据数据生成管线 + MinecraftOcc 数据集**：100,165 张图片、156 个室内场景、1,452 个语义类别的大规模占据预测基准，暴露现有 SOTA 方法的泛化缺陷，同时可作为有效的数据增强资源
## 结构化提取

- **Problem**: 真实场景→可编辑仿真环境的转换缺乏既保真又可交互的方法；3D 语义占据预测受数据稀缺限制
- **Method**: 多视角单目占据预测 → 体素融合（3D 卷积密度图 + DBSCAN 聚类）→ 模板匹配检索 → Minecraft 建造指令；VLN 通过 Qwen2.5-VL SFT/RFT 和 Gemini-2.5-Pro 实现
- **Tasks**: 3D 语义占据预测、Vision-Language Navigation（Next-View / Next-Action）
- **Sensors**: 虚拟第一人称 RGB 相机 + 位姿记录 mod（Screen with Coordinates）；真实场景使用 EmbodiedOcc-ScanNet RGB-D 数据
- **Robot Setup**: 虚拟 Minecraft 智能体，无物理机器人
- **Metrics**: 占据预测用 IoU / mIoU；VLN 用 Accuracy；图像质量用 NIQE / PIQE / LV；重建对比用 OOB Rate / Collision / Semantic Integrity / Visual Realism / Completeness / Aesthetic
- **Limitations**: 占据预测精度不足需人工精修；SOTA 方法在大规模 MinecraftOcc 上泛化差；VLN 数据集规模有限；未涉及动态/可变形物体
- **Evidence Notes**: 完整全文证据支撑。核心实验 Table 2-7 均有具体数值，ablation 包括不同数据规模（8k/50k/100k）、不同微调策略（SFT/RFT）、不同数据集组合（Base/Extend/Combined）。与 LayoutGPT/I-Design/LayoutVLM 的对比实验和效率分析提供了充分基线。
## 本地引用关系

- [[zhang2026world2minecraft]]
## 证据元数据

- Fulltext Quality: fulltext
- Evidence Coverage: complete（全文从 arXiv 获取，包含正文、附录、实验表格）
- Confidence: high
- Summary: 提出 World2Minecraft 框架，通过 3D 语义占据预测将真实场景转换为可编辑的 Minecraft 环境，并构建 MinecraftOcc 大规模占据数据集和 MinecraftVLN 导航数据集，在 VLN 下游任务中验证了重建场景的实用性。


## Problem

具身智能研究需要高保真、可编辑的仿真环境，但现有平台存在以下矛盾：
1. **基于真实扫描的平台**（如 Habitat）依赖 RGB-D 扫描数据，存在视觉伪影和几何缺陷，且场景不可编辑
2. **原生 Minecraft** 虽然可定制，但像素化风格与真实场景存在巨大的视觉域差
3. **NeRF / 3DGS 等方法** 生成照片级视图但不可编辑，缺乏物理属性
4. **CAD 方法** 需要精确实例分割和尺度对齐，难以直接用于下游任务
5. **3D 语义占据预测** 是核心瓶颈——受限于标注数据稀缺和泛化能力差


## Method

### 核心：Reality → Minecraft 转换管线

**Stage 1: 多视角语义占据预测**
- 单目预测器 `F_mono` 对每帧 RGB 图像生成 3D 语义占据网格 `O_mono[i]`
- 利用相机外参 `E`，通过 embodied 模型 `F_embodied` 将多帧预测融合为统一 3D 语义场 `O_scene`

**Stage 2: 体素融合与过滤**
- 将多类语义网格转为二值占据网格，3D 卷积计算密度图 `D`
- 密度阈值 `τ` 提取候选物体中心 `C`
- **按语义类别独立进行 DBSCAN 聚类**，合并冗余中心点
- 基于家具库的检索匹配（IoU 最大化的旋转模板匹配）确保几何保真度

**Stage 3: 虚拟世界生成**
- 将优化后的中心点转化为 Minecraft 建造指令执行

### VLN in Minecraft

- 在重建场景中构建 **MinecraftVLN** 数据集：
  - **Next-View Prediction**：给定指令和 3 张历史图像，预测下一步视图
  - **Next-Action Prediction**：给定指令和当前视图，预测下一步动作（前进/左转等）
- 微调 Qwen2.5-VL (3B/7B)，使用 SFT（LLaMA Factory）和 RFT（EasyR1/GRPO）
- 部署 Gemini-2.5-Pro 作为实时导航控制器

### MinecraftOcc 数据集构建

- 利用 Minecraft mods（Screen with Coordinates、WorldEdit、TMEO 纹理包）实现自动化管线
- 基于玩家视角 yaw 角分 axis-aligned 和 diagonal 两种情况定义 3D 体积
- 视角感知回退策略处理对角视角的体素丢失
- 通过 WorldEdit 从地图数据提取语义标签，构建体素级语义占据表示


## Experiments

### 数据集统计
| 数据集 | 图片数 | 场景数 | 语义类数 | 图像分辨率 |
|--------|--------|--------|----------|-----------|
| NYUv2 | 1,449 | 464 | 13 | 640×480 |
| OccScanNet | 65,119 | 674 | 13 | 640×480 |
| **MinecraftOcc** | **100,165** | **156 (~1000 rooms)** | **1,452** | **1920×1129** |

### 图像质量对比（Table 3）
| 数据集 | NIQE↓ | PIQE↓ | LV↑ |
|--------|-------|-------|-----|
| NYUv2 | 14.96 | 47.40 | 57,369 |
| OccScanNet | 17.63 | 58.78 | 10,352 |
| **MinecraftOcc** | **9.97** | **45.23** | **274,305** |

### VLN 结果（Table 2, Accuracy）
- **Next-View** 最佳：Base 7B SFT 0.5854，Extend 3B SFT 0.7087，Combined 7B RFT 0.6753
- **Next-Action** 最佳：Base 7B SFT 0.8000，Extend 3B RFT 0.6667，Combined 3B RFT 0.6570
- SFT 对小模型更有效，RFT 在多样化数据上表现更好

### 占据预测（Table 4）
- 4 种方法（MonoScene, NDC-Scene, ISO, Symphonies）在 MinecraftOcc 上性能普遍较低
- 8k 规模下最佳 IoU 71.46（Symphonies），mIoU 仅 21.56
- 100k 规模下所有方法显著下降，表明大数据集对泛化构成挑战
- **联合训练实验**（Table 5）：Symphonies + MinecraftOcc 8k + NYUv2 → IoU +0.43, mIoU +0.21

### 与布局方法对比（Table 6）
- World2Minecraft 在 OOB Rate (0.024)、Semantic Integrity (0.913)、Visual Realism (6.145)、Completeness (5.186)、Aesthetic (6.022) 全面优于 LayoutGPT、I-Design、LayoutVLM

### 效率分析（Table 7）
- World2Minecraft + 人工精修：**70.38s/场景**，比从零建造 (482.00s) 快 **7.5×**
- 操作数从 340 降至 24.5（13.9× 减少）


## Limitations

1. **重建质量依赖占据预测精度**：当前模型预测精度有限，30 个重建场景中仅 15 个质量足够用于 VLN，仍需人工精修（删浮动伪影、补表面空洞、调朝向）
2. **占据预测泛化瓶颈**：SOTA 方法在 MinecraftOcc 上 mIoU 最高仅 21.56（8k 规模），100k 规模下降更明显，表明跨域泛化仍是核心难题
3. **VLN 数据集规模有限**：Base 仅 1,059 样本，指令偏短偏简单；Extend 使用社区场景增加多样性但不是真实重建
4. **语义映射粒度损失**：1,452 个 Minecraft 类别映射到 12 类标准类别时信息损失严重
5. **未涉及动态场景和 DLO 类物体**：聚焦静态室内场景，未考虑可变形物体或动态环境


## Key Takeaways

1. **占据预测作为 Real-to-Sim 中间表示**：离散体素结构天然对齐 Minecraft 方块，比 NeRF/3DGS 更适合可编辑仿真——这对 Sim-to-Real 研究有启发，但 DLO 的可变形性使占据表示难以直接迁移
2. **Minecraft 作为具身 AI 仿真平台**：通过 TMEO mod 等高保真纹理包缩小域差，且天然支持物理交互和程序化生成，是 Habitat 之外的低成本替代
3. **自动化数据管线的价值**：利用游戏内 mod 自动采集图像+位姿+语义标签，省去了昂贵的真实世界标注——类似思路可用于构建 DLO 操控的仿真数据集
4. **VLM 导航可行性验证**：Gemini-2.5-Pro 可在重建场景中实时完成 VLN，Qwen2.5-VL 7B SFT 在 Next-Action 上达 80% 准确率——验证了 VLM 在结构化仿真环境中的导航能力
5. **数据增强效果**：MinecraftOcc 作为辅助训练数据可提升真实世界基准性能（NYUv2 mIoU +0.21），表明仿真数据可跨域迁移

## 相关概念

- [[imitation-learning]]
- [[vision-language-model]]
- [[reinforcement-learning]]
- [[robot-learning]]
- [[deformable-linear-object]]

## 相关研究者

- [[zhang-lechao|Zhang, Lechao]]
