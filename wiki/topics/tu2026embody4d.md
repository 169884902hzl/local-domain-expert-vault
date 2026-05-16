---
title: "Embody4D: A generalist 4D world model for embodied AI"
tags: [manipulation, imitation, diffusion, robot-learning, planning]
created: "2026-05-08"
updated: "2026-05-08"
type: "literature"
status: "done"
summary: "提出 Embody4D，一种面向具身智能的视频到视频 4D 世界模型，通过组合式数据合成管线、置信度自适应噪声注入和交互感知注意力机制，从单目视频生成任意新视角视频，在 VBench 和真实机器人抓取任务中均达到 SOTA"
authors: "Tu, Peiyan; Zhu, Hanxin; Sun, Jingwen; Ren, Shaojie; Wang, Cong et al."
year: "2026"
venue: "arXiv Preprint"
zotero_key: "PHG4K89T"
---
## 摘要

World models have made significant progress in modeling dynamic environments; however, most embodied world models are still restricted to 2D representations, lacking the comprehensive multi-view information essential for embodied spatial reasoning. Bridging this gap is non-trivial, primarily due to challenges from severe scarcity of paired multi-view data, the difficulty of maintaining spatiotemporal consistency in generated 3D geometries, and the tendency to hallucinate manipulation（操控） details. To address these challenges, we propose Embody4D, a dedicated video-to-video world model for embodied scenarios, capable of synthesizing arbitrary novel views from a monocular video. First, to tackle data scarcity, we introduce a 3D-aware compositional synthesis pipeline to curate a heterogeneous dataset compositing cross-embodiment（具身） robotic arms with diverse backgrounds, guaranteeing broad generalization. Second, to enforce geometric stability, we devise an adaptive noise injection strategy; by leveraging confidence disparities across image regions, this method selectively regularizes the diffusion（扩散） process to ensure strict spatiotemporal consistency. Finally, to guarantee manipulation（操控） fidelity, we incorporate an interaction-aware attention mechanism that explicitly attends to the robotic interaction regions. Extensive experiments demonstrate that Embody4D achieves state-of-the-art（现有最优方法） performance, serving as a robust world model that synthesizes high-fidelity, view-consistent videos to empower downstream robotic planning and learning.

## 中文简述

提出基于扩散模型的操控方法，具有泛化能力特点。

**研究方向**: 机器人操控、模仿学习、扩散模型、机器人学习、运动规划

## 关键贡献

1. **Embody4D 框架**：首个面向具身场景的视频到视频 4D 世界模型，从单目具身视频合成任意新视角视频
2. **组合式 4D 数据合成管线**：从 MuJoCo Menagerie 选取 30 种跨形态机械臂（人形、单臂、双臂、夹爪），与 DL3DV 真实背景组合，构建 23K 对 4D 训练样本，解决数据稀缺
3. **置信度自适应噪声注入策略**：基于点云重投影的置信度图，对高置信区域施加低噪声（纹理锁定），对低置信区域施加高噪声（给生成自由度），平衡结构保持与视觉修复
4. **交互感知注意力机制**：利用分割掩码作为运动归纳偏置，将注意力解耦为全局路径和交互引导路径，通过课程学习融合，保持操控区域几何一致性
5. **真实机器人验证**：在 FR3 + Robotiq 2F-85 上用 π0.5 VLA 验证，5 个 pick-and-place 任务成功率 74%（单视角基线 32%），OOD 任务优势尤其显著
## 结构化提取

- Problem: 具身世界模型局限于 2D，缺乏多视角信息支持空间推理；2D→4D 提升面临数据稀缺、时空不一致和操控细节幻觉三大瓶颈
- Method: 基于 Wan2.1-T2V-1.3B 的 Flow Matching 视频生成模型，采用 warp-then-inpaint 范式，包含三个核心模块：(1) 组合式 4D 数据合成管线（MuJoCo 30 种机械臂 + DL3DV 背景 + 3D 锚点追踪），(2) 置信度自适应噪声注入（σ_low=1.0, σ_high=0.85），(3) 交互感知双路径注意力（课程学习融合）
- Tasks: 视频新视角合成（4D 生成），下游 pick-and-place 机器人操控（5 个桌面任务）
- Sensors: 单目 RGB 相机（输入），双固定外部相机 + 腕部相机（真实机器人评估），MuJoCo 虚拟相机（数据合成）
- Robot Setup: Franka Research 3 + Robotiq 2F-85 夹爪，桌面 pick-and-place 场景，水果类物体
- Metrics: VBench（Subject/Background Consistency, Temporal Flickering, Motion Smoothness, Imaging Quality），Q-Align Visual Quality，PSNR/SSIM/LPIPS/FVD（消融），真实抓取成功率（5 任务×10 次试验）
- Limitations: 大视角变化退化；固定视角直接合成质量受限；推理慢（49 帧/2 分钟）；未涉及 DLO 或软体物体
- Evidence Notes: 全文精读完成。实验充分，含主实验（5 基线×6 指标）、消融实验（4 变体×4 指标）、真实机器人实验（带/不带腕部相机两组各 5 任务×10 试验）。附录含更多实现细节、可视化对比和消融分析。无证据缺失。
## 本地引用关系

- [[chen2026lastr1]]
- [[jiang2026world4rl]]
- [[sun2026maniparena]]
## 证据元数据

- Fulltext Quality: fulltext
- Evidence Coverage: full (全文从 arXiv 获取，含正文 6 章 + 附录 A-D，含实验表格和消融实验)
- Confidence: high
- Summary: 提出 Embody4D，一种面向具身智能的视频到视频 4D 世界模型，通过组合式数据合成管线、置信度自适应噪声注入和交互感知注意力机制，从单目视频生成任意新视角视频，在 VBench 和真实机器人抓取任务中均达到 SOTA


## Problem

现有具身世界模型局限于 2D 表示，缺乏多视角信息，无法支持具身空间推理。从 2D 提升到 4D（单目视频→多视角动态 3D 场景）面临三大瓶颈：
1. **数据极度稀缺**：缺乏成对多视角具身数据集，尤其是涵盖多种机械臂形态和全局视角的动态序列
2. **时空不一致**：现有方法在视角转换时难以维持 3D 几何和时间一致性，产生严重视觉伪影
3. **操控细节幻觉**：生成模型在合成复杂动态交互的新视角时，容易幻觉关键物理细节（如接触点、物体变形），损害物理合理性


## Method

### 整体架构
基于 Wan2.1-T2V-1.3B 扩散 Transformer 微调，采用 **warp-then-inpaint** 范式：
- 输入源视频 → VGGT 重建点云 → 投影到目标视角 → 得到 warp 后 RGB + 占位掩码
- 经置信度模块自适应注入噪声 → 交互感知注意力主干 → 输出目标视角视频

### 模块 A：组合式 4D 数据合成（Sec 4.1）
1. 从 MuJoCo Menagerie 选 30 种机械臂模型（人形、单臂、双臂、小夹爪）
2. 前景：MuJoCo 中控制模型执行随机运动，双虚拟相机严格对齐 DL3DV 背景外参
3. 背景：DL3DV 数据集随机采样，GPT-4o 筛选中心可见性
4. 3D 锚点追踪：VGGT 估计深度→5 帧多点反投影→质心→投影回目标视角，确定机械臂在新视角中的精确位置

### 模块 B：置信度自适应噪声注入（Sec 4.2）
- 轻量网络 f 从 warp 特征 Z_warp 和几何掩码 M_geo 合成连续置信度图 C
- 空间噪声调度：σ_t = [σ_low + C ⊙ (σ_high - σ_low)] · t
  - σ_low = 1.0（低置信区域，允许最大随机性）
  - σ_high = 0.85（高置信区域，最小噪声保持结构）
- 联合优化：Flow Matching 速度场回归 + 辅助特征对齐损失（L_aux = L1 置信度监督 + L2 特征差异）

### 模块 C：交互感知注意力（Sec 4.3）
- 前景掩码获取：模拟数据直接渲染；真实数据用 MemFlow（光流）或 SAM3（视频分割）
- 双路径注意力：
  - 全局路径：标准缩放点积注意力 O_global
  - 引导路径：掩码生成 boost 偏置矩阵 B，注入注意力图 O_guided
- 融合：O = (1-α)·O_global + α·O_guided，α 采用课程学习递增

### 训练策略
- **Stage 1**：23K 组合式 4D 数据，33K iter，lr=1e-5
- **Stage 2**：冻结交互注意力块 + 24K 单目具身数据（AGIBOT/Rh20t/Robset/Bc-z/InterndataA1），66K iter，lr=2e-6
- 硬件：8×A100，batch=16（2/GPU）
- 分辨率 384×672，49 帧

### Flow Matching 框架（Sec 3）
采用 Rectified Flow：线性插值噪声与数据 x_t = t·x_1 + (1-t)·x_0，速度场 v_t = x_1 - x_0，训练目标为预测速度场的 MSE。


## Experiments

### 数据集
- 训练：23K 组合式 4D 样本 + 24K 单目具身数据（5 个开源数据集均匀采样）
- 测试：120 个单目视频（70 合成 + 50 真实），49 帧，384×672

### 基线
TrajectoryCrafter, ReCamMaster, Ex-4D, Reangle-A-Video

### 指标
VBench（Subject/Background Consistency, Temporal Flickering, Motion Smoothness, Imaging Quality）+ Q-Align Visual Quality

### 主实验（Tab 1）
| 方法 | Subject↑ | Background↑ | Temporal↑ | Motion↑ | Imaging↑ | Q-Align↑ |
|------|----------|-------------|-----------|---------|----------|----------|
| ReCamMaster | 0.8981 | 0.8976 | 0.9717 | 0.9841 | 0.5914 | 3.4938 |
| Ex-4D | 0.8088 | 0.8906 | 0.9213 | 0.9742 | 0.5732 | 2.8585 |
| Reangle-A-Video | 0.9152 | 0.9224 | 0.9711 | 0.9879 | 0.6437 | 3.6916 |
| TrajectoryCrafter | 0.9202 | 0.9388 | 0.9714 | 0.9911 | 0.6257 | 3.8954 |
| **Ours** | **0.9477** | **0.9408** | **0.9751** | **0.9945** | **0.6994** | **3.9970** |

### 消融实验（Tab 2）
| 方法 | PSNR↑ | SSIM↑ | LPIPS↓ | FVD↓ |
|------|-------|-------|--------|------|
| Baseline | 24.09 | 0.766 | 0.139 | 42.09 |
| w/o 组合数据 | 24.72 | 0.777 | 0.131 | 37.89 |
| w/o 噪声注入 | 24.23 | 0.782 | 0.137 | 41.95 |
| w/o 交互注意力 | 24.81 | 0.782 | 0.134 | 37.12 |
| **Full** | **24.89** | **0.798** | **0.119** | **36.83** |

关键发现：
- 组合数据对跨形态泛化至关重要（移除后几何幻觉增加）
- 噪声注入主要提升 FVD（-5.27）和 SSIM（+0.016）
- 交互注意力主要降低 LPIPS（-0.015）和 FVD（-0.27）
- 三个模块协同增益显著

### 真实机器人实验（Tab 3 + Tab 4）
设置：Franka Research 3 + Robotiq 2F-85，100 条人类演示轨迹，π0.5 VLA policy

**带腕部相机（Tab 3）**：
| 方法 | T1(葡萄→碗) | T2(葡萄→盘) | T3(芒果→碗) | T4(柠檬→碗) | T5(香蕉→盘) | 总SR |
|------|-------------|-------------|-------------|-------------|-------------|------|
| 单视角 | 5/10 | 5/10 | 4/10 | 1/10 | 1/10 | 32% |
| ReCamMaster | 4/10 | 5/10 | 2/10 | 2/10 | 2/10 | 30% |
| TrajCrafter | 6/10 | 6/10 | 4/10 | 0/10 | 7/10 | 46% |
| **Embody4D** | **8/10** | **8/10** | **9/10** | **6/10** | **6/10** | **74%** |

**不带腕部相机（Tab 4）**：Embody4D 14/50 vs 单视角 8/50, ReCamMaster 6/50, TrajCrafter 10/50

关键发现：
- 多视角增强数据使 OOD 任务（T4、T5）成功率从 10% 提升到 60%（带腕部相机）
- ReCamMaster 因相机抖动导致性能下降（30% < 32% 基线）
- 即使有腕部相机，第三人称新视角仍显著提升性能


## Limitations

1. **大视角变化退化**：生成模型固有限制，视角变化过大时生成质量下降
2. **固定视角生成挑战**：当前 4D 范式依赖时间连续性，需要为下游任务直接合成目标视角（非平滑过渡），时空不连续性影响质量
3. **推理效率**：生成 49 帧约需 2 分钟，无法满足实时部署需求
4. **未见论文明确讨论 DLO 或软体物体**的操控场景


## Key Takeaways

1. **4D 世界模型作为数据引擎**：Embody4D 证明了从单目视频生成多视角数据可以显著提升下游 VLA policy 性能（32%→74%），尤其在 OOD 场景
2. **组合式数据合成的可行性**：MuJoCo 前景 + 真实背景的组合策略是解决具身 4D 数据稀缺的有效方案，支持 30 种机械臂形态
3. **置信度引导的噪声调度**：在 warp-then-inpaint 范式中，基于点云投影置信度自适应调节噪声是保持时空一致性的关键技术
4. **交互区域显式建模**：通过分割掩码显式解耦前景操控区域和背景，对操控细节保真至关重要
5. **对 DLO 操控的启示**：虽然本文未涉及 DLO，但其 4D 世界模型框架和组合式数据合成策略可迁移至 DLO 操控场景的多视角数据增强；DLO 的形变细节在视角转换中更容易产生幻觉，交互感知注意力可能对 DLO 细节保持尤为重要
6. **Flow Matching 在视频生成中的优势**：相比传统扩散模型，Rectified Flow 的直线轨迹设计在视频时空一致性上表现更优

## 相关概念

- [[robotic-manipulation]]
- [[imitation-learning]]
- [[diffusion-model]]
- [[robot-learning]]
- [[planning]]
- [[deformable-linear-object]]
- [[bimanual-manipulation]]
- [[grasping]]

## 相关研究者

- [[tu|Tu, Peiyan]]
- [[zhu-hanxin|Zhu, Hanxin]]
