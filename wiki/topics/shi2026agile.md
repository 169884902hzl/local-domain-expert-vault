---
title: "AGILE: Hand-object interaction reconstruction from video via agentic generation"
tags: [manipulation, imitation, VLM, sim-to-real, robot-learning]
created: "2026-05-11"
updated: "2026-05-11"
type: "literature"
status: "done"
summary: "提出 VLM 引导的 agentic 生成管线，从单目视频重建手-物体交互的水密网格和 6D 轨迹，用 anchor-and-track 策略替代脆弱的 SfM 初始化，实现 100% 成功率和 SOTA 几何精度。"
authors: "Shi, Jin-Chuan; Ye, Binhong; Liu, Tao; Liu, Xiaoyang; Xu, Yangjinhui et al."
year: "2026"
venue: "arXiv Preprint"
zotero_key: "JHBF2C49"
---
## 摘要

Reconstructing dynamic hand-object interactions from monocular videos is critical for dexterous manipulation（灵巧操控） data collection and creating realistic digital twins for robotics and VR. However, current methods face two prohibitive barriers: (1) reliance on neural rendering often yields fragmented, non-simulation-ready geometries under heavy occlusion, and (2) dependence on brittle Structure-from-Motion (SfM) initialization leads to frequent failures on in-the-wild footage. To overcome these limitations, we introduce AGILE, a robust framework that shifts the paradigm from reconstruction to agentic generation for interaction learning. First, we employ an agentic pipeline where a Vision-Language Model（视觉-语言模型） (VLM) guides a generative model to synthesize a complete, watertight object mesh with high-fidelity texture, independent of video occlusions. Second, bypassing fragile SfM entirely, we propose a robust anchor-and-track strategy. We initialize the object pose at a single interaction onset frame using a foundation model and propagate it temporally by leveraging the strong visual similarity between our generated asset and video observations. Finally, a contact-aware optimization integrates semantic, geometric, and interaction stability constraints to enforce physical plausibility. Extensive experiments on HO3D, DexYCB, ARCTIC, and in-the-wild videos reveal that AGILE outperforms baselines in global geometric accuracy while demonstrating exceptional robustness on challenging sequences where prior arts frequently collapse. By prioritizing physical validity, our method produces simulation-ready assets validated via real-to-sim retargeting for robotic applications. Project page: https://agile-hoi.github.io.

## 中文简述

提出基于模仿学习的灵巧手方法，具有接触丰富特点。

**研究方向**: 机器人操控、模仿学习、视觉-语言模型、仿真到真实迁移、机器人学习

## 关键贡献

1. **首个 agentic HOI 管线**：VLM（Gemini 3 Pro）作为智能监督者，引导多视角生成+rejection sampling，产出与视频一致的水密网格，独立于遮挡
2. **Anchor-and-Track 策略**：完全绕过 SfM，仅在单个交互起始帧（IOF）用 FoundationPose 锚定物体姿态，通过语义+几何对齐实现时序传播
3. **Contact-Aware 优化**：集成语义（DINOv3）、几何（mask）和交互稳定性（SDF-based）约束，确保物理合理性
4. **全流程验证**：单手（HO3D, DexYCB）、双手（ARCTIC）、野外视频均达 SOTA；Real-to-Sim retargeting 验证仿真可用性
## 结构化提取

- **Problem**: 从单目视频重建手-物体交互的 4D 轨迹，产出仿真可用的 3D 资产，克服神经渲染几何碎片化和 SfM 初始化脆弱两大障碍
- **Method**: VLM-guided agentic 生成（关键帧选择 + 多视角合成 + rejection sampling + 3D 提升 + 纹理精炼）+ SfM-free anchor-and-track（单帧 FoundationPose 锚定 + 时序 DINO/mask/interaction loss 传播）
- **Tasks**: 手-物体交互 3D 重建、物体 6D pose 追踪、Real-to-Sim retargeting
- **Sensors**: 单目 RGB 相机（固定相机假设，仅 IOF 检测用）
- **Robot Setup**: Isaac Gym 仿真 + Shadow Hand（运动学 retargeting 验证，非实际机器人）
- **Metrics**: Chamfer Distance (CD, cm²), F-score (F@5mm, F@10mm), Hand-relative CD (CDh, cm²), MPJPE (mm), Success Rate (SR)
- **Limitations**: 继承基础模型限制（透明/反光物体）、IOF 检测需静态相机、仅运动学 retargeting、仅刚性物体、非实时（30-50s/frame）
- **Evidence Notes**: 全文含完整实验表格（Table 1-3）、消融实验（7 个变体）、实现细节（Appendix A-H）、VLM prompt 完整展示。SIGGRAPH 2026 接收论文。
## 本地引用关系

- [[shi2026agile]]
## 证据元数据

- Fulltext Quality: fulltext (arXiv HTML version, including main text + appendices A-H)
- Evidence Coverage: comprehensive (method details, full experiment tables, ablation study, implementation details, prompts)
- Confidence: high
- Summary: 提出 VLM 引导的 agentic 生成管线，从单目视频重建手-物体交互的水密网格和 6D 轨迹，用 anchor-and-track 策略替代脆弱的 SfM 初始化，实现 100% 成功率和 SOTA 几何精度。


## Problem

从单目视频重建动态手-物体交互（HOI）面临两个核心障碍：
1. **几何不完整**：神经渲染（NeRF/3DGS）依赖多视角一致性，手部遮挡导致碎片化、非水密的几何输出，无法用于物理仿真
2. **初始化脆弱**：现有方法依赖 SfM（如 COLMAP）做初始姿态估计，在纹理缺失物体、快速运动、严重遮挡场景下频繁崩溃，失败率高达 75%

现有生成式方法（MagicHOI）用扩散先验但产出过平滑网格且仍依赖 SfM；单视角方法（SAM3D）受限于信息丢失。核心矛盾：需要聚合视频多帧线索来补全遮挡区域，但 2D 扩散模型的随机性会产生幻觉。


## Method

### 3.1 Agentic Textured Object Generation

**目标**：从严重遮挡的单目视频中恢复完整的水密纹理网格。

**流程**（4步）：
1. **VLM 关键帧选择**：Gemini 3 Pro 从视频中选 N（1-4）个信息量最大的帧，最大化视角覆盖、最小化遮挡
2. **多视角生成**：Gemini 2.5 Flash 根据关键帧合成正交视角（前/后/左/右）
3. **VLM 质量审核**：VLM critic 对生成视角做 rejection sampling，按几何、纹理、材质一致性打分，低于阈值则丢弃重生成
4. **3D 提升 + 拓扑优化 + 纹理精炼**：
   - Hunyuan3D 2.0/2.5 将验证后的多视角图像提升为 3D 网格
   - Blender 自动 retopology（~10K 面）+ UV unwrapping
   - 纹理精炼：image-to-image 编辑模型 + VLM rejection sampling
   - 高质量纹理是下游 FoundationPose 初始化和 DINO 语义匹配的前提

**关键洞察**：VLM agent 解决了"生成模型幻觉 vs 视频证据一致性"的核心矛盾——不是简单生成，而是智能选择+严格过滤。

### 3.2 SfM-Free Initialization

**假设**：固定相机（仅用于 IOF 自动检测，核心管线对相机运动不敏感）。

**预处理**：
- MoGe-2 → metric depth + camera intrinsics
- SAM2 → 手/物体分割 mask

**手部初始化**：
- WiLoR → MANO 参数（β, θ, Rh, J2D）
- constrained ICP（固定 Rh）→ 手的全局 scale sh
- PnP → 逐帧平移 Th

**物体初始化**：
- constrained ICP → 物体全局 scale so
- 定义 Interaction Onset Frame（IOF）：物体 mask 开始显著位移的帧
- FoundationPose 在 IOF → 初始物体 pose（Ro^IOF, To^IOF）

### 3.3 Contact-Aware Optimization

**双向在线优化**：从 IOF 向视频首尾双向逐帧传播。

每帧两步：
1. **手部平移精修**：固定 Rh, sh，仅优化 Th，最小化 ℒ_joint（关节点重投影 MSE）
2. **交互感知物体追踪**：固定手部，优化物体 6D pose（Ro, To），前一帧结果作为初始化

**物体 loss**：
- ℒ_mask：渲染轮廓 vs GT mask 的 L2 距离
- ℒ_dino：DINOv3 语义特征对齐，3D-to-2D 对应关系 + 遮挡 mask，解决无纹理/运动模糊区域漂移
- ℒ_interact：SDF-based 交互稳定性约束
  - 将手部顶点映射到物体局部坐标系
  - SDF 距离 → soft gating weight（wi = 1 - tanh(σ·di), σ=40）
  - 约束相邻帧间接触区域手-物相对位置不变
  - 效果：物体"锁定"在抓握手部附近，防止无物理意义的滑移

**IOF 特殊处理**：联合优化手/物 pose + 物体各向异性 scale so。


## Experiments

### Datasets
- **HO3D-v3**：18 sequences，严重遮挡场景
- **DexYCB**：20 diverse trajectories，多物体类别
- **ARCTIC**：刚性物体子集，双手交互
- **In-the-Wild**：自采集 + 来自 HOLD 的序列，复杂几何/操控模式

### Baselines
- **HOLD** (Fan et al., 2024b)：隐式神经渲染
- **MagicHOI** (Wang et al., 2025b)：扩散先验 + NeRF
- **BIGS** (On et al., 2025)：3DGS 双手重建（ARCTIC 对比）

### Key Results

**DexYCB（Table 1）**：
| Method | CD↓ (cm²) | F@5mm↑ | F@10mm↑ | CDh↓ (cm²) | MPJPE↓ (mm) | SR↑ |
|--------|-----------|---------|----------|-------------|-------------|------|
| HOLD | 2.94 | 0.216 | 0.478 | 589.00 | 23.00 | 45% |
| MagicHOI | 2.05 | 0.281 | 0.523 | 661.90 | 21.20 | 25% |
| **AGILE** | **0.52** | **0.659** | **0.880** | **94.60** | **19.06** | **100%** |

- CD 降低 75%（vs MagicHOI），SR 从 25-45% → 100%
- 注意：baseline 指标仅在成功子集上计算（survivor bias）

**HO3D-v3（Table 1）**：
| Method | CD↓ (cm²) | MPJPE↓ (mm) | SR↑ |
|--------|-----------|-------------|------|
| HOLD | 2.83 | 15.80 | 78% |
| MagicHOI | 3.39 | 20.00 | 67% |
| **AGILE** | **1.51** | **17.00** | **100%** |

**ARCTIC 双手（Table 2）**：AGILE 在所有指标上优于 HOLD 和 BIGS。

### Ablation Study (Table 3, HO3D)

| Variant | MPJPE↓ | CD↓ | CDh↓ |
|---------|--------|------|-------|
| (a) Full Model | **17.00** | **1.51** | **23.30** |
| (b) w/o Agentic Multi-view | 18.30 | 8.80 | 45.50 |
| (b1) Heuristic selection | 18.50 | 4.80 | 28.80 |
| (b2) w/o Multi-view synth | 18.60 | 5.70 | 34.90 |
| (c) w/o Texture Refine | 18.10 | 2.23 | 29.90 |
| (d) w/o ℒ_joint | 21.10 | 1.54 | 24.50 |
| (e) w/o ℒ_mask | 18.00 | 2.98 | 23.80 |
| (f) w/o ℒ_dino | 18.20 | 2.33 | 33.10 |
| (g) w/o ℒ_interact | 17.80 | 1.61 | 54.40 |

关键发现：
- 去掉 agentic 多视角生成 → CD 从 1.51 暴涨至 8.80（+483%）
- 去掉纹理精修 → CDh 从 23.30 至 29.90，证明纹理质量直接影响追踪稳定性
- 去掉 ℒ_interact → CDh 暴涨至 54.40，交互稳定性约束至关重要
- VLM 选择优于启发式最大 mask 选择（4.80 vs 8.80）

### Real-to-Sim Retargeting

- Isaac Gym + Shadow Hand
- 运动学映射（无物理仿真闭环）
- 验证生成资产可直接用于仿真器

### Runtime
- 单张 RTX 4090，200 帧序列 ~2.1-2.2 小时
- 比 HOLD（~25.1h）快 12x，与 MagicHOI（~2.4h）相当


## Limitations

1. **基础模型继承限制**：透明/高反光物体可能导致 scale drift 或局部追踪错误
2. **静态相机假设**：仅限于 IOF 自动检测，核心追踪对相机运动不敏感（可用 VLM 动作识别/MegaSaM 替代 IOF 检测扩展到动相机）
3. **Real-to-Sim 仅运动学**：无接触动力学闭环，策略学习留待未来工作
4. **仅刚性物体**：未扩展到铰接体或可变形物体（DLO）
5. **帧率**：每帧 30-50 秒优化时间，不适合实时应用


## Key Takeaways

1. **范式转换价值**：从"重建"转向"agentic 生成"，用 VLM 作为智能质检员桥接生成先验和视频证据，这对 DLO 操控的数据采集有启发——可以从 YouTube 视频大规模生成仿真资产
2. **Anchor-and-Track 的鲁棒性**：单帧锚定 + 时序传播的策略比 SfM 全局优化更鲁棒，失败率从 75% → 0%，这一思路可迁移到 DLO 状态估计
3. **SDF-based 交互约束**：ℒ_interact 用 SDF 距离做 soft gating，将接触区域"锁定"——这个思想可直接用于 DLO 的 hand-object 交互约束
4. **纹理质量的下游重要性**：高质量的纹理不是装饰，而是 FoundationPose 初始化和 DINO 匹配的硬性前提——在 DLO 场景中，纹理/外观质量同样影响视觉追踪

## 相关概念

- [[robotic-manipulation]]
- [[imitation-learning]]
- [[vision-language-model]]
- [[sim-to-real]]
- [[robot-learning]]
- [[diffusion-model]]
- [[deformable-linear-object]]
- [[bimanual-manipulation]]
- [[grasping]]

## 相关研究者

- [[shi-jin-chuan|Shi, Jin-Chuan]]
