---
title: "Learning versatile humanoid manipulation with touch dreaming"
tags: [manipulation, imitation, VLM, tactile, grasping]
created: "2026-04-30"
updated: "2026-04-30"
type: "literature"
status: "done"
summary: "提出人形机器人全身操控系统 HTD，通过 RL 下肢控制器 + VR 遥操作数据采集 + 触觉做梦辅助行为克隆，在 5 个接触丰富任务上相比 ACT 基线成功率提升 90.9%。"
authors: "Niu, Yaru; Fang, Zhenlong; Chen, Binghong; Zhou, Shuai; Senthilkumaran, Revanth Krishna et al."
year: "2026"
venue: "arXiv Preprint"
zotero_key: "SC6M8HB9"
---
## 摘要

Humanoid robots promise general-purpose assistance, yet real-world humanoid loco-manipulation（操控） remains challenging because it requires whole-body stability, end-effector dexterity, and contact-aware interaction under frequent contact changes. In this work, we study dexterous（灵巧）, contact-rich（接触丰富） humanoid loco-manipulation（操控）. We first develop an RL-based lower-body controller that serves as the stability backbone for whole-body execution during complex manipulation（操控）. Built on this controller, we develop a VR-based whole-body humanoid data collection system that integrates dexterous（灵巧） hands and tactile（触觉） sensing for contact-rich（接触丰富） manipulation（操控）. We then propose Humanoid Transformer with Touch Dreaming (HTD), a multimodal（多模态） encoder--decoder Transformer that models touch as a core modality alongside multi-view vision and proprioception. HTD is trained in a single stage with behavioral cloning（行为克隆） augmented by touch dreaming: in addition to predicting action chunks, the policy predicts future hand-joint forces and future tactile（触觉） latents, with tactile（触觉）-latent targets provided by an exponential moving average target encoder without requiring a separate tactile（触觉） pretraining（预训练） stage. This encourages the policy to learn contact-aware representations for dexterous manipulation（灵巧操控）. Across five real-world contact-rich（接触丰富） tasks, HTD achieves a 90.9% relative improvement in average success rate over the stronger baseline. Ablation results further show that latent-space tactile（触觉） prediction is more effective than raw tactile（触觉） prediction, yielding a 30% relative gain in success rate. These results demonstrate that our touch-dreaming-enhanced learning system enables versatile, high-dexterity humanoid manipulation（操控） in the real world. More information and open-source materials are available at: humanoid-touch-dream.github.io.

## 中文简述

提出基于行为克隆的灵巧手方法，具有接触丰富特点。

**研究方向**: 机器人操控、模仿学习、视觉-语言模型、触觉感知、抓取

## 关键贡献

1. **触觉使能的全身人形操控系统**：开发了一个整合 RL 下肢控制器、VR 遥操作、灵巧手重定向和分布式触觉感知的完整系统，用于稳定、灵巧、接触丰富的真实世界操控
2. **Humanoid Transformer with Touch Dreaming (HTD)**：提出多模态 encoder-decoder Transformer，将触觉作为核心模态，通过单阶段行为克隆 + touch dreaming（未来手关节力预测 + EMA 监督的触觉 latent 预测）学习接触感知表征
3. **五任务实证验证**：在 Insert-T、Book Organization、Towel Folding、Cat Litter Scooping、Tea Serving 五个真实世界任务上，HTD 相比更强 ACT 基线平均成功率提升 90.9%，latent 触觉预测相比 raw 触觉预测成功率提升 30%
## 结构化提取

- Problem: 人形机器人接触丰富的全身灵巧操控，需要同时满足全身稳定性、灵巧手控制和接触感知交互
- Method: HTD (Humanoid Transformer with Touch Dreaming) — 多模态 encoder-decoder Transformer，行为克隆 + touch dreaming 辅助目标（future force prediction + EMA latent tactile prediction），单阶段训练
- Tasks: Insert-T (3.5mm 公差插入), Book Organization (推-抓-放书), Towel Folding (毛巾折叠), Cat Litter Scooping (猫砂铲工具使用), Tea Serving (双杯端茶行走)
- Sensors: 双目头相机 RGB、腕部相机 RGB、关节本体感知、每关节力反馈 (dexterous hand)、分布式触觉 (每手 1062 维, 17 区域覆盖手指和手掌)
- Robot Setup: Unitree G1 人形机器人 + Inspire-Robots 灵巧手, RL-based 15-DoF 下肢控制器, IK 上肢求解, DexPilot 手重定向
- Metrics: Score rate (部分进度评分, mean±SEM, 20 trials), Success rate (严格完成率)
- Limitations: 论文无显式 Limitations 章节；推断：仅 VR 遥操作数据、开环 touch dreaming 预测、单平台验证、无推理时触觉规划、结构化场景、无跨任务泛化
- Evidence Notes:

  - LBC 对比 FALCON/AMO：多数 tracking error 指标最优（Table II）
  - HTD vs ACT(V+P)：5 任务平均成功率提升 90.9%（相对），task score 提升 31.1%
  - HTD vs ACT(V+P+T)：说明简单加触觉输入不如 touch dreaming
  - 消融 w/o TD vs w/o Touch&TD：触觉输入 alone 不一致有益
  - 消融 Dream Raw vs Dream Latent：latent 空间成功率相对提升 30%
  - 定性：dreamed force 轨迹跟踪接触事件时序和幅度；latent 相似度在持续接触时高、突变时暂时下降
## 本地引用关系

- [[chi2024diffusion]]
- [[han2025upvital]]
- [[liu2025forcemimic]]
- [[wu2025tacdiffusion]]
- [[xu2026fingereye]]
- [[xue2026tube]]
- [[zhao2025polytouch]]
## 证据元数据

- Fulltext Quality: fulltext
- Evidence Coverage: 完整覆盖方法、实验、消融、附录
- Confidence: high
- Summary: 提出人形机器人全身操控系统 HTD，通过 RL 下肢控制器 + VR 遥操作数据采集 + 触觉做梦辅助行为克隆，在 5 个接触丰富任务上相比 ACT 基线成功率提升 90.9%。


## Problem

人形机器人在真实世界中的 loco-manipulation（移动-操控）仍然具有根本性挑战，因为它需要同时满足三个条件：
1. **全身稳定性**：人形机器人的操控与躯干姿态、底座运动、足地稳定性物理耦合，手-物体接触的不确定性不仅影响局部操控精度，还影响全身执行
2. **末端执行器灵巧性**：需要使用灵巧手进行精细操作（如紧公差插入、可变形物体处理）
3. **接触感知交互**：在频繁的接触变化下进行接触感知的交互，仅靠视觉无法充分观测接触状态

现有系统的关键缺口：几乎没有系统在单一平台中同时整合全身控制、全灵巧手控制和触觉感知/建模（Table I 中仅本文同时具备五项能力）。


## Method

### 系统架构（四阶段管线）
1. **下肢控制器 (LBC) 训练**：IsaacLab 大规模并行仿真中 PPO 训练 teacher → DAgger 蒸馏到 student。控制 15-DoF 下肢（2×6 腿 + 3 腰），输入为 base velocity、torso orientation (rpy)、height 命令。稳定工作空间：h ∈ [0.33, 0.80]m, ϕ ∈ [-0.38, 0.35]rad, θ ∈ [-0.92, 1.41]rad, ψ ∈ [-1.50, 1.34]rad
2. **VR 遥操作数据采集**：操作员头/腕/手运动变换到统一机器人参考系，分解为 LBC 躯干命令、IK 腕部目标、DexPilot 灵巧手重定向。记录双目头相机 + 腕部相机 RGB、本体感知、每关节力反馈、双手分布式触觉（每手 1062 维，17 个空间感知区域）
3. **HTD 策略学习**：核心方法
4. **部署**：策略 30Hz 输出 action chunk，LBC/IK/手重定向 50Hz 执行

### HTD 核心设计

**模态 Tokenizer**：
- 图像：ResNet backbone (finetuned) + cross-attention aggregation
- 状态（本体感知/力）：轻量 MLP
- 触觉：Per-Finger/Region Tactile Encoder — 按解剖结构分解为拇指/食指/中指/无名指/小指/手掌，每个 region 内进一步分为局部 patch（tip/top/palm-facing），各 patch 独立 CNN 分支处理后 MLP 融合

**Encoder-Decoder Transformer Trunk**：
- Encoder：融合所有模态 token
- Decoder：固定输出 token 序列，每个动作模态分配固定数量的 token

**Modular Action Experts**：每个 expert 通过 cross-attention 从 decoder 输出 token 读取，独立预测特定动作模态（末端位姿、躯干姿态、速度命令、手动作），支持不同维度和控制角色的自适应解码

**Touch Dreaming**（仅训练时使用）：
- **Future Hand Joint Force Prediction**：smooth L1 loss 监督未来力向量
- **Future Tactile Latent Prediction**：EMA target encoder 提供稳定 latent 目标，cosine direction loss + magnitude alignment loss 监督。EMA teacher 缓慢演化（θ_T ← αθ_T + (1-α)θ），stop gradient 防止 mode collapse
- 关键洞察：latent 空间触觉预测 >> raw 空间，因为 raw 传感器读数稀疏、高维、噪声大

**训练目标**：
L = Σ L_act,mi + λ_F · L_force + λ_Z · L_tact
单阶段行为克隆，不需要单独的触觉预训练阶段


## Experiments

### 下肢控制器评估（vs FALCON, AMO）
- 在 4096 并行仿真环境中评估 500 timesteps
- 本文 LBC 在大多数指标上最优：E_v=0.1420, E_h=0.0280, E_p=0.0126, E_r=0.0487
- 相比 AMO 在躯干高度和俯仰跟踪上更紧，对接触丰富全身操控至关重要

### 五任务真实世界评估（每任务 20 trials）
| 任务 | HTD vs ACT(V+P) | HTD vs ACT(V+P+T) |
|------|-----------------|-------------------|
| Insert-T (3.5mm 公差 T 形插入) | 显著提升 | 显著提升 |
| Book Organization (推-抓-放) | 一致提升 | 一致提升 |
| Towel Folding (毛巾折叠) | 显著提升 | 显著提升 |
| Cat Litter Scooping (猫砂铲) | 最大提升 | 最大提升 |
| Tea Serving (端茶双杯) | 显著提升 | 显著提升 |

- 平均成功率提升 90.9%（相对），task score 提升 31.1%（相对）
- 仅仅给 ACT 添加触觉输入不保证一致提升（ACT V+P+T 仅在部分任务优于 ACT V+P）

### 消融实验（四变体）
| 变体 | 触觉输入 | Touch Dreaming | 触觉预测空间 |
|------|---------|---------------|-------------|
| w/o Touch and TD | ✗ | ✗ | - |
| w/o TD | ✓ | ✗ | - |
| Dream Raw Tactile | ✓ | ✓ | raw sensor |
| Dream Latent Tactile (full) | ✓ | ✓ | latent space |

关键发现：
1. 触觉作为输入 alone 不一致有益（w/o TD vs w/o Touch & TD 差异小）
2. 预测性触觉目标超越被动触觉条件化（两种 Dream 变体均优于 w/o TD）
3. Latent 触觉预测 >> Raw 触觉预测，成功率相对提升 30%

### Touch Dreaming 定性分析
- 预测的未来力轨迹有效跟踪接触事件的时间和幅度
- 触觉 latent 相似度在持续接触期保持高
- 突发接触转换时相似度暂时下降（open-loop chunk 预测的自然发散）
- 轻接触时 latent 模式一致；丰富接触时激活为高强度区分模式
- Dreamed latent 比 raw sensor 读数更稳定、更与语义接触变化对齐


## Limitations

论文未设显式 Limitations 章节，但从内容可推断：
1. **仅 VR 遥操作演示**：数据采集依赖 VR 遥操作，对操作员技能有要求，且采集成本高
2. **Touch Dreaming 是开环预测**：future tactile latent chunk 是开环 rollout，在不可预测的接触突变时会偏离 ground truth
3. **仅在单一人形平台验证**：Unitree G1 + Inspire-Robots 灵巧手，未测试跨平台泛化
4. **无显式触觉 world model**：touch dreaming 仅作为辅助训练目标，不用于推理时规划或反应控制
5. **任务仍为结构化场景**：五个任务虽覆盖多样接触类型，但场景仍相对受控（固定桌面/地面），未测试完全非结构化环境
6. **每任务分别训练策略**：未展示单一策略跨任务泛化能力


## Key Takeaways

1. **Touch Dreaming 的核心洞察**：将触觉预测作为辅助目标（而非推理模块），通过 EMA teacher 在 latent 空间监督，能有效正则化 Transformer trunk 学习接触感知表征。这与 JEPA 系列的 latent prediction 思路一致
2. **对 DLO 操控的启发**：towel folding 任务表明 HTD 在可变形物体处理上有优势，touch dreaming 机制可能有助于 DLO 操控中的接触状态预测。但本文未涉及 DLO 特有的绳索拓扑/长程依赖问题
3. **模态分解设计**：per-finger tactile encoder + modular action experts 的设计思路可借鉴——不同模态和动作维度有不同统计特性，分离编码/解码比统一处理更有效
4. **仅加触觉输入不够**：消融表明单纯增加触觉传感器数据不保证性能提升，关键在于如何有效利用触觉信号（latent prediction > raw prediction > passive input）
5. **全身操控的系统工程价值**：LBC + VR 遥操作 + 触觉使能数据采集的完整管线对实际部署有重要参考价值

## 相关概念

- [[robotic-manipulation]]
- [[imitation-learning]]
- [[vision-language-model]]
- [[tactile-sensing]]
- [[grasping]]
- [[deformable-linear-object]]
- [[bimanual-manipulation]]

## 相关研究者

- [[niu|Niu, Yaru]]
