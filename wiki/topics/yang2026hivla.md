---
title: "HiVLA: A visual-grounded-centric hierarchical embodied manipulation system"
tags: [manipulation, imitation, VLM, diffusion, flow-matching]
created: "2026-05-12"
updated: "2026-05-12"
type: "literature"
status: "done"
summary: "通过解耦 VLM 高层规划器与 DiT 低层动作专家，利用级联交叉注意力依次融合全局视觉、高分辨率局部裁剪和技能语言指令，在 RoboTwin 仿真和真实双臂平台上显著超越 π₀ 和 H-RDT。"
authors: "Yang, Tianshuo; Chen, Guanyu; Chen, Yutian; Liang, Zhixuan; Liu, Yitian et al."
year: "2026"
venue: "arXiv Preprint"
zotero_key: "NRBZRHI5"
---
## 摘要

While end-to-end（端到端） Vision-Language-Action (VLA) models offer a promising paradigm for robotic manipulation（机器人操控）, fine-tuning them on narrow control data often compromises the profound reasoning capabilities inherited from their base Vision-Language Models (VLMs). To resolve this fundamental trade-off, we propose HiVLA, a visual-grounded-centric hierarchical framework that explicitly decouples high-level semantic planning from low-level motor control. In high-level part, a VLM planner first performs task decomposition and visual grounding to generate structured plans, comprising a subtask instruction and a precise target bounding box. Then, to translate this plan into physical actions, we introduce a flow-matching Diffusion（扩散） Transformer (DiT) action expert in low-level part equipped with a novel cascaded cross-attention mechanism. This design sequentially fuses global context, high-resolution object-centric crops and skill semantics, enabling the DiT to focus purely on robust execution. Our decoupled architecture preserves the VLM's zero-shot（零样本） reasoning while allowing independent improvement of both components. Extensive experiments in simulation and the real world demonstrate that HiVLA significantly outperforms state-of-the-art（现有最优方法） end-to-end（端到端） baselines, particularly excelling in long-horizon（长时序） skill composition and the fine-grained manipulation（操控） of small objects in cluttered scenes.

## 中文简述

提出基于扩散模型的操控方法，具有零样本泛化特点。

**研究方向**: 机器人操控、模仿学习、视觉-语言模型、扩散模型、Flow Matching

## 关键贡献

1. **提出 HiVLA 框架**：以视觉定位为核心的层次化 VLA 架构，将 VLM 高层语义规划与 DiT 低层动作生成完全解耦，消除多任务操控中的灾难性遗忘，两个模块可独立改进。
2. **设计级联交叉注意力机制**：在 DiT 动作专家中依次注入全局视觉上下文、位置感知的高分辨率局部裁剪特征和技能级语言语义，使低层策略充分利用定位计划。
3. **全面验证**：在仿真（RoboTwin 2.0）和真实双臂平台上显著超越 SOTA VLA 模型（π₀、π₀.5、StarVLA、H-RDT），尤其在长时序技能组合和杂乱场景细粒度操控上表现突出。
## 结构化提取

- **Problem**: 端到端 VLA 模型在窄域操控数据上微调时灾难性遗忘 VLM 推理能力；现有层次化方法的视觉定位桥接丢失空间坐标或高分辨率细节
- **Method**: 层次化解耦架构；VLM Planner（Qwen3-VL 8B）输出子任务 + bbox；DiT Action Expert 用级联交叉注意力依次融合 Global Context → Position-Aware Local Crop → Language Skill；Conditional Flow Matching 训练
- **Tasks**: 15 种桌面操控任务（仿真 9 种评估 + 真实 7 类 16 子场景），涵盖单技能抓取/按压到多步序列（Stack 3 Blocks、Click 3 Bells）
- **Sensors**: 多视角相机（1080p 头部相机 + 720p 手腕相机）；本体感受（14 DoF 关节位置 + 夹爪状态）
- **Robot Setup**: Aloha-Agilex-1.0 双臂平台，14 DoF（每臂 6 DoF + 1 夹爪），仿真（RoboTwin 2.0 domain randomization）和真实世界
- **Metrics**: 任务成功率（100 trials/task，取最后 3 个 checkpoint 平均）；grounding mIoU；子任务准确率（strict exact-match）；鲁棒性（噪声注入后的成功率）
- **Limitations**: VLM 延迟高（1.9s/step）；仅验证刚体离散技能；真实数据量小（360 episodes）；未涉及动态/可变形物体；零样本 grounding 在新场景弱
- **Evidence Notes**: 所有结果均有具体数值和表格支撑。仿真数据集 HiVLA-HD 每任务约 1000 episodes，所有 baseline 在同一数据集上微调 150K steps，比较公平。消融实验系统覆盖了注入顺序、视觉组件、VLM 规模和历史上下文。真实世界实验数据量有限，多物体杂乱场景成功率偏低（6-7/30），但与 baseline 的差距显著。
## 本地引用关系

-
## 证据元数据

- Fulltext Quality: fulltext（arXiv HTML 全文，含正文、附录、表格）
- Evidence Coverage: 完整覆盖方法、实验、消融、附录细节
- Confidence: high
- Summary: 通过解耦 VLM 高层规划器与 DiT 低层动作专家，利用级联交叉注意力依次融合全局视觉、高分辨率局部裁剪和技能语言指令，在 RoboTwin 仿真和真实双臂平台上显著超越 π₀ 和 H-RDT。


## Problem

端到端 VLA 模型在窄域操控数据上微调时会发生灾难性遗忘，损害基座 VLM 的推理能力。现有层次化方案（如 DexGraspVLA、RoboGround）在将视觉定位信息桥接到低层策略时，要么丢失空间坐标、要么丢失高分辨率细节，无法同时兼顾全局空间感知和细粒度视觉保真。


## Method

### 整体架构
HiVLA 采用层次化解耦设计，分为 **VLM Planner Agent**（高层）和 **DiT Action Expert**（低层）：

### 高层：VLM Planner Agent
- 基座模型：Qwen3-VL 8B，经 210K 对话数据微调
- 输入：当前视觉场景、上一动作前后的视觉历史、夹爪状态、上一子任务
- 输出：结构化 JSON 计划，包含子任务描述 `L_sub,t`、动作类型、目标物体名称、归一化 bounding box `B_t = [ymin, xmin, ymax, xmax]`
- VLM 作为 "agent" 使用 tool：bbox 触发 Image Crop tool，从原始 1920×1080 图像中裁剪高分辨率目标区域 `I^local_t`
- 解耦优势：VLM 不需要低层微调，保留零样本推理能力；可直接替换为更强的 VLM

### 低层：DiT Action Expert
- 基于 H-RDT 架构（LLaMA-style Transformer，RMSNorm + SwiGLU）
- 使用 **Conditional Flow Matching (CFM)** 训练：线性插值路径 z → A_t，L2 损失
- 架构规格：16 层，hidden 2176，GQA（16 head / 8 kv-head），action chunk size = 16
- **级联交叉注意力**（核心创新），每个 Transformer block 内依次执行 3 个 cross-attention：
  1. **Global Visual Context**：多视角图像经 DINOv2 + SigLIP 编码 → global tokens → cross-attention 提供全局场景理解
  2. **Position-Aware Local Features**：从 1080p 原图裁剪的高分辨率局部 patch → 同一视觉编码器 → 加入绝对正弦位置编码（来自原图坐标）→ cross-attention 提供精细视觉 + 空间定位
  3. **Subtask Language Guidance**：子任务文本经语言编码器 → cross-attention 注入技能语义（pick/place/push）
- AdaLN 融入扩散时间步 τ
- 初始化：从 H-RDT 在 EgoDex 上预训练的权重开始，global cross-attention 权重复制到 local cross-attention

### 训练
- 优化器：AdamW，lr=1e-4，warmup 500 steps
- 硬件：2×H200，batch size 64，BF16 混合精度，150K steps
- 数据集：HiVLA-HD（RoboTwin 2.0 Hard mode，15 任务，~1000 episodes/task，1080p head camera + 720p wrist camera）

### 推理
- VLM Planner：~1.9s/step（未优化）
- DiT Action Expert：0.162s/16-step action chunk
- 异步执行实现 8Hz 控制频率


## Experiments

### 仿真实验（RoboTwin 2.0）
9 个任务，分 4 个 Easy + 5 个 Hard，每个任务 100 trials，取最后 3 个 checkpoint 的平均成功率：

| Method | Easy Avg | Hard Avg | Total Avg |
|--------|----------|----------|-----------|
| π₀ | 54.3% | 38.6% | 45.6% |
| π₀.5 | 55.3% | 36.4% | 44.8% |
| StarVLA | 58.8% | 36.6% | 46.4% |
| H-RDT | 90.5% | 54.6% | 70.6% |
| HiVLA (w/o Skill) | 96.5% | 64.4% | 78.7% |
| **HiVLA** | **96.0%** | **73.2%** | **83.3%** |

关键结果：
- 比 H-RDT 提升 +12.7%（整体），比 π₀ 提升 +37.7%
- Hard 任务中 "Stack 3 Blocks" 从 H-RDT 20% → 37%，"Move Stapler" 从 34% → 60%
- 涌现错误修正能力：DiT 抓取失败时 VLM 识别子任务未完成，重新下发指令

### 鲁棒性测试（对 Planner 错误的容忍度）
| 扰动类型 | 0% → 100% 错误注入率 |
|---------|---------------------|
| BBox 噪声 | 83.3% → 57.0%（100% bbox 错误仍保留 57%） |
| 语言噪声 | 83.3% → 12.0%（线性退化，严格服从语言） |
| 两者同时 | 83.3% → 17.3% |

结论：低层策略对空间定位噪声有强鲁棒性（依赖 global context 自纠错），但严格服从语言指令。

### 真实世界实验
7 物体类别，16 子场景，360 episodes 遥操作数据，每任务 30 trials：

| Method | Click 1 Bell | Click 2 Bells | Pick&Place 1 Cup | Pick&Place 3 Cups | Pick&Place 1 Block | Pick&Place 3 Blocks |
|--------|-------------|--------------|-----------------|-------------------|-------------------|---------------------|
| H-RDT | 8/30 | 9/30 | 4/30 | 0/30 | 9/30 | 0/30 |
| HiVLA | 13/30 | 17/30 | 21/30 | 6/30 | 20/30 | 7/30 |

H-RDT 在多物体杂乱场景（3 Cups / 3 Blocks）完全失败（0/30），HiVLA 通过视觉定位成功处理。

### 消融实验

**A. 引导注入顺序**（交叉注意力层级联顺序）：
- Global → Local → Text = 83.3%（最优）
- Local → Global → Text = 74.1%
- Global → Text → Local = 78.3%
- 仅 Local → Text = 70.4%，仅 Global → Text = 70.6%
- "Coarse-to-Fine" 策略显著最优

**B. 视觉定位组件**：
- 去除高分辨率裁剪（降采样到 640×360）：75.2%（-8.1%），"Lift Pot" 下降最严重
- 去除绝对位置编码：76.8%（-6.5%），"Click 3 Bells" 下降最严重（无法区分同形物体）

### VLM Planner 分析
- 零样本：GPT-4o 子任务准确率 42.85%，但 mIoU 仅 3.45%；Qwen3-VL-32B mIoU 20.17%
- 微调后 Qwen3-VL-8B：mIoU 90.37%，子任务准确率 98.57%
- 视觉历史对子任务准确率贡献：+3.33%（98.57% vs 95.24%）


## Limitations

1. **VLM Planner 延迟高**：1.9s/step 未优化，依赖异步执行补偿，对需要快速反应的任务可能是瓶颈
2. **任务类型局限**：仅验证了 pick/place/push 等离散技能组合，未涉及连续操控（如 DLO 弯折、布料折叠）
3. **真实世界数据量小**：仅 360 episodes，多物体杂乱场景成功率仍有限（3 Cups 6/30，3 Blocks 7/30）
4. **依赖精确 bounding box**：虽然对噪声有鲁棒性，但 VLM Planner 在新场景的零样本 grounding 能力仍弱（GPT-4o mIoU 3.45%），需要领域微调
5. **未评估动态/可变形物体**：所有任务均为刚体操作
6. **Sim-to-Real gap**：从仿真 checkpoint 初始化后微调到真实世界，但泛化范围未充分评估


## Key Takeaways

1. **层次化解耦是有效范式**：将 VLM 推理与低层控制完全分离，避免了灾难性遗忘，这对我们设计 DLO 操控系统有直接参考价值——可以将 DLO 的拓扑/几何推理放在高层 VLM 中，低层策略专注连续动作生成。

2. **视觉定位作为中间表征的优势**：bounding box 比 dense segmentation mask 更轻量且 VLM 原生支持，高分辨率裁剪 + 绝对位置编码的组合解决了现有方法的"空间-细节"矛盾。对 DLO 操控可借鉴——用 bbox 或 keypoint 标注 DLO 的关键区域（抓取点、目标形态区域）。

3. **Coarse-to-Fine 级联注意力**的工程经验：全局→局部→语言的注入顺序优于其他排列，表明策略应先理解整体场景再聚焦目标再匹配技能。这一模式可能同样适用于 DLO 的形态感知→抓取点定位→操控技能选择。

4. **涌现错误修正**是一个有趣特性：VLM 作为独立语义监督者检测子任务失败并重试。在 DLO 操控中，可类似地让 VLM 检测 DLO 是否达到目标构型并触发重试。

5. **数据效率**：仅 360 episodes 真实数据即可在杂乱场景获得可观表现，表明层次化解耦有助于数据效率——对 DLO 数据稀缺问题有启发。

## 相关概念

- [[robotic-manipulation]]
- [[imitation-learning]]
- [[vision-language-model]]
- [[diffusion-model]]
- [[flow-matching]]
- [[deformable-linear-object]]
- [[bimanual-manipulation]]
- [[grasping]]

## 相关研究者

- [[yang-tianshuo|Yang, Tianshuo]]
- [[liang-zhixuan|Liang, Zhixuan]]
