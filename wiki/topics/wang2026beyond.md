---
title: "Beyond short-horizon: VQ-memory for robust long-horizon manipulation in non-markovian simulation benchmarks"
tags: [manipulation, imitation, VLM, diffusion, planning]
created: "2026-05-08"
updated: "2026-05-08"
type: "literature"
status: "done"
summary: "提出 RuleSafe 非马尔可夫关节物体操控基准和 VQ-Memory 时序记忆模块，用 VQ-VAE 将历史关节状态离散化为紧凑 token 并经聚类降噪，在 π0/DP3/RDT/CogACT 四种 VLA 架构上持续提升长时序规划成功率。"
authors: "Wang, Honghui; Jing, Zhi; Ao, Jicong; Song, Shiji; Li, Xuelong et al."
year: "2026"
venue: "arXiv Preprint"
zotero_key: "ANW6IMEA"
---
## 摘要

The high cost of collecting real-robot data has made robotic simulation a scalable platform for both evaluation and data generation. Yet most existing benchmarks concentrate on simple manipulation（操控） tasks such as pick-and-place, failing to capture the non-Markovian characteristics of real-world tasks and the complexity of articulated object interactions. To address this limitation, we present RuleSafe, a new articulated manipulation（操控） benchmark built upon a scalable LLM-aided simulation framework. RuleSafe features safes with diverse unlocking mechanisms, such as key locks, password locks, and logic locks, which require different multi-stage reasoning and manipulation（操控） strategies. These LLM-generated rules produce non-Markovian and long-horizon（长时序） tasks that require temporal modeling and memory-based reasoning. We further propose VQ-Memory, a compact and structured temporal representation that uses vector-quantized variational autoencoders (VQ-VAEs) to encode past proprioceptive states into discrete latent tokens. This representation filters low-level noise while preserving high-level task-phase context, providing lightweight yet robust temporal cues that are compatible with existing Vision-Language-Action models (VLA). Extensive experiments on state-of-the-art（现有最优方法） VLA models and diffusion（扩散） policies show that VQ-Memory consistently improves long-horizon（长时序） planning, enhances generalization to unseen configurations, and enables more efficient manipulation（操控） with reduced computational cost. Project page: vqmemory.github.io

## 中文简述

提出基于扩散模型的操控方法，具有泛化能力特点。

**研究方向**: 机器人操控、模仿学习、视觉-语言模型、扩散模型、运动规划

## 关键贡献

1. **RuleSafe 基准**：基于 LLM 辅助的可扩展仿真框架，构建包含 20 条锁规则、10 种保险箱的非马尔可夫长时序操控 benchmark。规则涵盖 part-phase（关节状态依赖）和 task-phase（任务进度依赖）两类解锁机制，包括钥匙锁、密码锁和逻辑锁。
2. **VQ-Memory 模块**：利用 VQ-VAE 将连续关节状态序列编码为离散隐 token，再通过 K-means 聚类去除冗余码本条目，形成紧凑且语义一致的记忆表示。该设计在过滤低层噪声的同时保留高层任务阶段上下文。
3. **模型无关性验证**：在四种不同架构（π0、DP3、RDT、CogACT）上验证 VQ-Memory 的通用性，证明其作为即插即用模块可显著提升长时序规划和泛化能力。
## 结构化提取

- **Problem**: 现有仿真 benchmark 任务短视且缺乏非马尔可夫特性；VLA 模型在视觉相似但语义不同的操控阶段间无法区分，需要轻量且鲁棒的时序记忆机制。
- **Method**: RuleSafe（LLM 辅助生成非马尔可夫长时序操控 benchmark）+ VQ-Memory（VQ-VAE 离散化关节状态历史 → K-means 聚类降噪 → 紧凑 token 注入 VLA 模型）。
- **Tasks**: 20 条锁规则（钥匙锁/密码锁/逻辑锁），涵盖 part-phase 和 task-phase 依赖；单任务和多任务设置。
- **Sensors**: RGB 图像（第一/第三人称视角）、点云、关节状态（本体感知）。
- **Robot Setup**: Unitree H1-2 人形机器人，Inspire 手（每臂 7 DoF + 每手 6 DoF = 13 维动作空间），SAPIEN 仿真引擎。
- **Metrics**: Success Rate (SR)、Process Score (PS)。
- **Limitations**: 低层操控精度不足（56.3% 平均 SR）；仅仿真验证未做 Sim-to-Real；记忆来源单一（仅关节状态）；固定 token 映射方式。
- **Evidence Notes**: 全文实验数据完整，包含单任务/多任务/消融三类实验。多任务平均 SR 从 25.0% 提升到 56.3%（+31.3%），四种 VLA 架构均有一致提升。最优配置为聚类数 4、记忆长度 40。失败原因主要为精细操作精度不足而非时序推理错误。
## 本地引用关系

-
## 证据元数据

- Fulltext Quality: fulltext
- Evidence Coverage: complete（全文通过 arXiv HTML 获取，包含所有章节、实验表格和附录）
- Confidence: high
- Summary: 提出 RuleSafe 非马尔可夫关节物体操控基准和 VQ-Memory 时序记忆模块，用 VQ-VAE 将历史关节状态离散化为紧凑 token 并经聚类降噪，在 π0/DP3/RDT/CogACT 四种 VLA 架构上持续提升长时序规划成功率。


## Problem

现有机器人仿真基准存在两个核心局限：
1. **任务短视化**：大多数 benchmark（如 pick-and-place）只关注短时序、简单操控，无法捕捉真实世界任务的非马尔可夫特性（当前观测不足以推断任务阶段）。
2. **关节物体交互复杂性不足**：现有关节物体 benchmark（SAPIEN、GAPartNet、UniDoorManip）仅评估单关节运动或跨物体泛化能力，缺少多关节依赖和长时序推理。
3. **时序建模缺陷**：VLA 模型仅依赖当前视觉帧，在视觉相似但语义不同的操控阶段间无法区分；引入视觉历史虽可缓解但计算开销大；原始关节状态历史虽轻量但易受噪声干扰和过拟合。


## Method

### RuleSafe 基准设计

**锁定机制生成**：
- **Part-Phase**：将关节物体的运动状态离散化（如 open/closed），基于关节配置定义顺序依赖（如 chained key-lock: knob open → handle open → door open）。
- **Task-Phase**：更高级的抽象，跟踪多步任务进度，支持密码锁（需按特定规则操作部件输入密码序列）和逻辑锁（如旋钮和把手切换次数乘积等于 4）。
- **LLM 辅助设计**：给定少量参考示例，LLM 生成规则描述和可执行的解锁判断程序，大幅减少人工设计成本。

**数据生成**：
- 基于 HumanoidGen 框架扩展，使用 LLM 规划器将操控任务分解为原子操作序列。
- 手操作（pinch、grasp、rotate）+ 臂运动（约束优化 + OMPL 运动规划）。
- 空间标注：通过关键点和轴约束确保手与物体的几何一致性。

**仿真配置**：
- SAPIEN 引擎，Unitree H1-2 人形机器人 + Inspire 手（每臂 7 DoF，每手 6 DoF，13 维动作空间）。
- 采集 RGB 图像（第一/第三人称视角）和点云。
- 环境 100 Hz，数据采集 10 Hz。平均 demo 成功率 71.7%，平均轨迹长度 638 帧。

### VQ-Memory 模块

**核心思路**：将历史关节状态序列 → VQ-VAE 编码 + 量化 → K-means 聚类 → 离散 token 序列，作为记忆 token 注入 VLA 模型。

**VQ-VAE 离散化**：
- 输入：关节状态轨迹 Q_t = {q_{t-W+1}, ..., q_t}，窗口 W=50，步长 20（约 20× 压缩比）。
- 编码器映射到隐空间 → 量化到最近码本条目 → 解码器重建。
- 训练损失：L_recon + λ·L_commit（λ=4）。
- 与 VQ-VLA 的区别：VQ-VLA 用 VQ-VAE 做 action tokenizer（小窗口，低压缩比）；VQ-Memory 仅作辅助时序输入，无需精确重建，可用大窗口高压缩比。

**K-means 聚类**：
- 对训练后的码本 {e_k} 做 K-means 聚类，合并冗余码本条目。
- 将码本从 K=256 聚类到 J=4，每个原始码重新分配到最近聚类中心。
- 聚类后的 token 强调跨轨迹共享的高层语义模式，而非低层变化。

**集成方式**：
- DP3：添加小型卷积网络将离散 token 映射为隐嵌入。
- 其他模型（π0、RDT、CogACT）：将离散 token 映射到 VLM 词表尾部的特殊语言 token，与现有语言 token 拼接后送入 Transformer encoder。
- 配置：词表大小 4（从 256 聚类而来），记忆 token 长度 40。


## Experiments

### 实验设置
- 评估指标：Success Rate (SR) 和 Process Score (PS)
- 单任务设置：100 条 demo 训练，聚焦 rule_001（3 步）和 rule_020（8 步）
- 多任务设置：20 个任务共 1000 条轨迹（每任务 50 条）
- 硬件：4× NVIDIA A100 GPU

### 单任务结果（Table 1 & 2）

**π0 在 rule_001/rule_020 上的表现**：
| Method | rule_001 SR | rule_001 PS | rule_020 SR | rule_020 PS |
|--------|------------|------------|------------|------------|
| π0 (无记忆) | 30.0% | 56.7% | 0.0% | 10.6% |
| π0 + raw memory | 55.0% | 70.1% | 0.0% | 16.3% |
| π0 + VQ-Memory | **80.0%** | **89.3%** | **45.0%** | **67.3%** |

**不同模型在 rule_020 上的表现**：
| Method | SR | PS |
|--------|-----|-----|
| DP3 → +VQ-Memory | 5.0% → **45.0%** | 14.1% → 70.4% |
| RDT → +VQ-Memory | 0.0% → **35.0%** | 13.6% → 61.2% |
| CogACT → +VQ-Memory | 0.0% → **20.0%** | 9.7% → 50.4% |
| π0 → +VQ-Memory | 0.0% → **45.0%** | 10.6% → 67.3% |

关键发现：raw memory 在短任务 rule_001 上有一定帮助，但在长时序 rule_020 上完全失效（过拟合）；VQ-Memory 在所有模型上一致提升。

### 多任务结果（Table 3）
- π0 平均 SR：25.0% → 56.3%（+31.3%）
- π0 平均 PS：48.8% → 76.5%（+27.7%）
- 简单任务（rule_002/003）基线已较高，VQ-Memory 仍带来边际提升
- 复杂任务（rule_006/010/018）从接近 0% 提升到 30-60%
- 失败原因分析：高层规划正确但低层动作执行精度不足（手指偏位、滑落、旋转不完整）

### 消融实验（Table 4，rule_020）

**聚类数**：
| Clusters | SR | PS |
|----------|-----|-----|
| 256（无聚类） | 20.0% | 47.5% |
| 32 | 35.0% | 57.5% |
| **4** | **45.0%** | **67.3%** |
| 2 | 30.0% | 54.4% |

**记忆长度**：
| Length | SR | PS |
|--------|-----|-----|
| 20 | 25.0% | 53.8% |
| **40** | **45.0%** | **67.3%** |
| 60 | 40.0% | 65.4% |

最优配置：聚类数 4，记忆长度 40。过度聚类（2）会丢失阶段区分信息；过短记忆无法捕获长期依赖，过长收益递减。


## Limitations

1. **低层操控精度瓶颈**：多任务平均 SR 仅 56.3%，主要失败原因是手指偏位、滑落等精细操作不足，受限于每种保险箱的 demo 数量。
2. **仿真局限**：RuleSafe 仅在仿真中验证，未涉及 Sim-to-Real 迁移。
3. **记忆来源单一**：VQ-Memory 仅编码关节状态历史，未融合视觉、语言等其他模态的历史信息。
4. **固定 token 映射**：将离散 token 映射到 VLM 词表尾部，未探索更灵活的跨模态对齐方式。
5. **规则生成依赖 LLM**：虽然 LLM 辅助设计提高了效率，但生成质量仍取决于 LLM 能力和参考示例质量。


## Key Takeaways

1. **VQ-VAE + 聚类是有效的时序记忆方案**：将连续关节状态离散化并聚类为极少量 token（仅 4 个），在大幅压缩的同时保留了任务阶段信息，对抗噪声和过拟合效果显著。这一思路可借鉴到 DLO 操控中的时序状态表示。
2. **非马尔可夫任务是 VLA 的核心挑战**：当前 VLA 模型在仅依赖当前观测时，对视觉相似但语义不同的阶段（如"接近把手时该拉还是该转"）几乎无法区分，需要显式的时序记忆机制。
3. **轻量时序记忆优于视觉历史**：与维护多帧视觉观察相比，基于关节状态的离散 token 记忆几乎不增加计算开销，且效果更稳健。对于实时性要求高的 DLO 操控场景，这种轻量方案极具参考价值。
4. **LLM 辅助 benchmark 设计**：用 LLM 从少量示例生成多样化规则，是构建可扩展仿真 benchmark 的有效范式，可推广到 DLO 相关的复杂任务设计。
5. **与 DLO 操控的关联**：DLO 操控同样具有非马尔可夫特性（绳索构型历史影响当前操控策略），VQ-Memory 的离散化时序表示思路可直接迁移——用 VQ-VAE 编码 DLO 的形变历史状态作为策略输入。

## 相关概念

- [[robotic-manipulation]]
- [[imitation-learning]]
- [[vision-language-model]]
- [[diffusion-model]]
- [[planning]]
- [[deformable-linear-object]]
- [[grasping]]

## 相关研究者

- [[wang-honghui|Wang, Honghui]]
- [[jing-zhi|Jing, Zhi]]
- [[ao|Ao, Jicong]]
- [[song-shiji|Song, Shiji]]
