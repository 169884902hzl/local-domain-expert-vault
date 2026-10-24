---
title: "Open-H-embodiment: A large-scale dataset for enabling foundation models in medical robotics"
tags: [manipulation, imitation, VLM, RL, robot-learning]
created: "2026-04-29"
updated: "2026-04-29"
type: "literature"
status: "done"
summary: "发布医疗机器人领域最大开源多具身数据集（770小时，20平台，49+机构），并基于此训练 GR00T-H（首个开源手术 VLA 基座模型）和 Cosmos-H-Surgical-Simulator（首个多具身动作条件化世界模型）"
authors: "Consortium, Open-H-Embodiment; :; Nelson, Nigel; Chen, Juo-Tung; Haworth, Jesse et al."
year: "2026"
venue: "arXiv Preprint"
zotero_key: "GJXCPAGS"
---
## 摘要

Autonomous medical robots hold promise to improve patient outcomes, reduce provider workload, democratize access to care, and enable superhuman precision. However, autonomous medical robotics has been limited by a fundamental data problem: existing medical robotic datasets are small, single-embodiment（具身）, and rarely shared openly, restricting the development of foundation models that the field needs to advance. We introduce Open-H-Embodiment（具身）, the largest open dataset of medical robotic video with synchronized kinematics to date, spanning more than 49 institutions and multiple robotic platforms including the CMR Versius, Intuitive Surgical's da Vinci, da Vinci Research Kit (dVRK), Rob Surgical BiTrack, Virtual Incision's MIRA, Moon Surgical Maestro, and a variety of custom systems, spanning surgical manipulation（操控）, robotic ultrasound, and endoscopy procedures. We demonstrate the research enabled by this dataset through two foundation models. GR00T-H is the first open foundation vision-language-action model for medical robotics, which is the only evaluated model to achieve full end-to-end（端到端） task completion on a structured suturing benchmark (25% of trials vs. 0% for all others) and achieves 64% average success across a 29-step ex vivo suturing sequence. We also train Cosmos-H-Surgical-Simulator, the first action-conditioned world model to enable multi-embodiment（具身） surgical simulation from a single checkpoint, spanning nine robotic platforms and supporting in silico policy evaluation and synthetic data generation for the medical domain. These results suggest that open, large-scale medical robot data collection can serve as critical infrastructure for the research community, enabling advances in robot learning, world modeling, and beyond.

## 中文简述

提出基于视觉-语言的操控方法，具有端到端特点。

**研究方向**: 机器人操控、模仿学习、视觉-语言模型、强化学习、机器人学习

## 关键贡献

1. **Open-H-Embodiment 数据集**：迄今最大开源医疗机器人数据集，119 个数据集、770 小时配对视频+运动学数据、49+ 机构、20 种机器人平台、33 个任务族、5 种环境类型
2. **GR00T-H**：首个开源手术 VLA 基座模型，基于 GR00T-N1.6-3B，在 SutureBot 上是唯一实现完整端到端缝合的模型（25% vs 其他模型 0%），ex vivo 29 步缝合序列 64% 平均成功率
3. **Cosmos-H-Surgical-Simulator (C-H-S-S)**：首个多具身动作条件化手术世界模型，基于 Cosmos-Predict 2.5 (2B 参数)，支持 9 种机器人平台，单 checkpoint 即可生成任意训练分布内的手术视频轨迹
4. 统一数据格式（LeRobot v2.1）+ 结构化 README 模板，解决多机构异构数据的可用性问题
## 结构化提取

- Problem: 医疗机器人缺乏大规模、多具身、开源数据集，限制了 foundation model 的发展；通用 VLA 在手术任务上全部失败
- Method: 构建最大开源医疗机器人数据集 Open-H（LeRobot v2.1 格式），在其上 post-train GR00T-H（VLA, GR00T-N1.6-3B）和 Cosmos-H-Surgical-Simulator（2B 视频扩散 transformer）
- Tasks: 缝合（pick up, handover, throw, extract, knot tie）、Peg Transfer、needle pickup、超声扫描、内窥镜导航、完整临床手术
- Sensors: 内窥镜视频（单目/立体）、腕部相机、RGB-D、超声 B-mode、眼动追踪（120Hz）、仿真中深度图/光流/分割
- Robot Setup: dVRK, da Vinci Si/Xi, CMR Versius, Rob Surgical BiTrack, Virtual Incision MIRA, Moon Surgical Maestro, KUKA LBR iiwa, Franka Panda, UR5e, USTC Torin 等 20 种平台
- Metrics: 端到端完成率、子任务成功率（Clopper-Pearson CI）、Fisher exact test + Holm-Bonferroni 校正、L1 (MAE)、SSIM
- Limitations: 整体成功率低（25% 端到端），无活体评估，无异常检测，缺乏失败数据，L1/SSIM 非领域专用指标
- Evidence Notes:

  - GR00T-H 是唯一在 SutureBot 上实现端到端缝合的模型（25%, 5/20），其他模型全部失败（证据来自 Fig.3）
  - 33% 数据即可匹配 ACT 全量性能（47% vs 47%），全量数据进一步提升至 73%（证据来自 Fig.4）
  - GR00T-H 对硬件磨损更具韧性：器械线缆老化和相机更换后 ACT 性能低于原始报告，GR00T-H 仍保持 25%（证据来自 Discussion）
  - Ex vivo 29 步缝合 64% 平均成功率，结构化原语接近完美，切割步骤仅 20-30%（证据来自 Fig.6）
## 本地引用关系

- [[consortium2026openhembodiment]]
## 证据元数据

- Fulltext Quality: fulltext
- Evidence Coverage: high（已完整阅读全文所有章节：Summary, Introduction, Results, Discussion, Materials and Methods）
- Confidence: high
- Summary: 发布医疗机器人领域最大开源多具身数据集（770小时，20平台，49+机构），并基于此训练 GR00T-H（首个开源手术 VLA 基座模型）和 Cosmos-H-Surgical-Simulator（首个多具身动作条件化世界模型）


## Problem

医疗机器人自主化面临根本性数据瓶颈：现有手术机器人数据集规模小、单具身、很少开源共享，无法支撑 foundation model 的发展。通用 VLA 模型（OpenVLA、GR00T-N1、π₀）在手术任务（如缝合）上全部失败，原因在于手术任务涉及可变形粘弹性组织、复杂内窥镜视觉、多步骤不可逆操作，与通用操控差距过大。


## Method

### Open-H 数据集
- **数据格式**：统一为 LeRobot v2.1 格式（Parquet + MP4），存储效率比 RLDS/HDF5 提升 98%
- **文档规范**：每个数据集附带结构化 README，包含平台类型、采集方式、操作者技能水平、同步策略、运动学表示等
- **临床标注**：Versius-500 提供初始标注（器械/解剖分割、动作分类、手术阶段标注），使用 LemonFM 生成自动标签
- **多样性**：
  - 具身：手术系统 620h、工业臂 40h、柔性内窥镜 30h、仿真 83h、手动器械 1h
  - 任务：缝合/打结 57h、组织操控 19h、技能基准 25h、超声 43h、内窥镜 30h
  - 传感：71 个数据集有多视角，52 个有立体视觉，31 个有腕部相机，27 个有深度传感
  - 环境：仿真 84h、台面/体模 119h、ex vivo 65h、in vivo 3h、临床 499h

### GR00T-H 训练
- **基础模型**：GR00T-N1.6-3B VLA（Cosmos-2B VLM backbone）
- **Post-training 数据**：601 小时手术子集（排除超声/内窥镜/仿真）
- **关键设计**：
  - 相对末端执行器（EEF）控制 + 6D 旋转矩阵，统一跨具身动作空间
  - 每个 robot configuration 独立 action head（MLP 投影），避免线缆驱动机器人个体差异的混叠
  - Z-score 归一化 [-5, 5] 裁剪，加权 moment matching 合并数据集统计
  - Versius-500 采样上限 20%，防止单一具身主导
- **训练配置**：65,000 步，global batch size 1,024
- **Fine-tuning**：冻结 VLM backbone，仅训练 action prediction 组件
- **Checkpoint 选择**：使用 Cosmos-Surg-dVRK 自动化评估管线（世界模型生成 rollout + V-JEPA 2 标注成功率）筛选

### Cosmos-H-Surgical-Simulator
- **基础模型**：Cosmos-Predict 2.5-2B（latent video diffusion transformer）
- **训练数据**：32 个数据集，9 种机器人具身，10+ 机构
- **动作空间**：统一 44 维，zero-padding 适配不同具身
- **输入/输出**：1 帧 context + 12 个动作向量 → 生成 12 帧；自回归 rollout 生成完整轨迹
- **训练配置**：42,000 步，64×A100 80GB，global batch 1,024，lr 1.6e-4
- **视频分辨率**：512×288


## Experiments

### 1. End-to-End Suturing (SutureBot, n=20)
| Model | Pickup | Handover | Throw | Extract | Knot Tie | Full Completion |
|-------|--------|----------|-------|---------|----------|-----------------|
| GR00T-H | 20/20 | 20/20 | 12/20 | - | - | 5/20 (25%) |
| GR00T-N1.6 | 20/20 | 16/20 | 4/20 | - | - | 0/20 (0%) |
| ACT | 20/20 | - | 4/20 | - | - | 0/20 (0%) |
| LingBot-VA | - | 12/20 | 1/20 | - | - | 0/20 (0%) |

### 2. Generalization (OOD, unseen wound + varied lighting, n=10/subtask)
- GR00T-H: 54% avg success（Pick Up+Handover 70%, Throw+Extract 42.5%）
- GR00T-N1.6: 30%
- ACT: 5%（仅 Pick Up+Handover 15%，其余全部失败）

### 3. Data Efficiency (SutureBot, 33% vs 100% fine-tuning data)
| Data | GR00T-H | ACT | GR00T-N1.6 |
|------|---------|-----|------------|
| 33% | ≈47% | ≈47% | ≈20% |
| 100% | ≈73% | ≈50% | ≈37% |

### 4. Multi-Embodiment (3 platforms)
- GR00T-H 在 Versius (Peg Transfer)、MIRA (needle pickup)、dVRK-Si (SutureBot) 上均显著优于 GR00T-N1.6 (p < 0.001)

### 5. Ex Vivo Suturing (pork belly, 29 subtasks × 10 trials)
- Overall: 64% avg success
- Near-perfect: needle pickup (10/10), handover (9-10/10), set-down (10/10), knot tying (10/10 ×3)
- Weakest: readjust (4/10), open wound (4/10), cut suture (2/10, 3/10)

### 6. Cosmos-H-Surgical-Simulator (L1 & SSIM on 25 datasets)
- Benchtop scenes: 低 L1、高 SSIM，72 帧内仅缓慢退化
- Tissue-based scenes: 更高 L1、更低 SSIM（内窥镜光照变化、器械遮挡、湿组织反光、可变形解剖）
- 种子间方差：benchtop 窄，tissue-based 较宽


## Limitations

1. 整体成功率远未达临床可靠性（SutureBot 仅 25% 端到端，ex vivo 64%）
2. 尚未在活体组织上评估（活体组织会出血、运动、刚度变化）
3. 无异常事件检测/响应能力（组织撕裂、器械故障、患者运动）
4. 切割步骤成功率极低（20-30%）
5. 长序列误差累积，限制端到端完成率
6. 数据集以成功演示为主，缺乏失败轨迹（对世界模型训练不利）
7. L1/SSIM 非手术领域专用指标，不反映器械位置正确性或工具-组织交互物理合理性
8. LingBot-VA 仅用 50h 数据（对比 GR00T-H 的 601h），且推理参数未充分调优，对比不完全公平
9. 需要动物模型 pre-clinical 评估才能推进到人体应用


## Key Takeaways

1. **跨具身数据共享是手术机器人突破的关键**：Open-X-Embodiment 在通用机器人领域的成功验证了这一点，Open-H 将此范式带入医疗领域
2. **领域特定 post-training 显著提升 VLA 性能**：GR00T-H 在 601h 手术数据上的 post-training 使其从完全失败变为可完成缝合
3. **相对 EEF 动作 + 具身特定 action head 是多具身学习的好实践**：避免学习正运动学，提升跨平台泛化
4. **世界模型可用于 in silico 策略评估**：C-H-S-S 支持策略部署前的低成本验证，减少物理机器人时间
5. **可变形组织操控仍是核心难题**：ex vivo 中精细接触和切割步骤成功率最低，这与我们 DLO 操控研究中的挑战一致
6. **数据规模和多样性显著改善鲁棒性**：GR00T-H 对硬件磨损和相机更换表现出更强韧性，暗示大尺度预训练使策略更稳定

## 相关概念

- [[robotic-manipulation]]
- [[imitation-learning]]
- [[vision-language-model]]
- [[reinforcement-learning]]
- [[robot-learning]]
- [[sim-to-real]]
- [[deformable-linear-object]]

## 相关研究者

- [[consortium|Consortium, Open-H-Embodiment]]
