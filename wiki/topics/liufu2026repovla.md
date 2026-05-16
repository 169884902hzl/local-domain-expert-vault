---
title: "RePO-VLA: Recovery-driven policy optimization for vision-language-action models"
tags: [manipulation, imitation, VLM, RL, bimanual]
created: "2026-05-16"
updated: "2026-05-16"
type: "literature"
status: "done"
summary: "提出两阶段恢复驱动策略优化框架 RePO-VLA，通过历史重置初始化消除因果混淆、学习进度感知语义价值函数赋予失败轨迹稠密标签、价值条件化精炼引导策略偏好高进展动作，使 VLA 在对抗扰动下双臂操控成功率从 20% 提升至 75%。"
authors: "Liufu, Weijia; Guo, Xiaoyu; Chen, Ruiyi; Liu, Jingzhi; Zhang, Kaidong et al."
year: "2026"
venue: "arXiv Preprint"
zotero_key: "ZPFMJBVU"
---
## 摘要

Vision-Language-Action (VLA) models remain brittle in long-horizon（长时序）, contact-rich（接触丰富） manipulation（操控） because success-only imitation provides little supervision for execution drift, while failed rollouts are often discarded. We introduce RePO-VLA, a recovery-driven policy optimization framework that assigns distinct roles to success, recovery, and failure trajectories. RePO-VLA first applies Recovery-Aware Initialization (RAI), slicing recovery segments and resetting history so corrective actions depend on the current adverse state rather than the preceding failure. It then learns a Progress-Aware Semantic Value Function (PAS-VF), aligning spatiotemporal trajectory features with instructions and successful references. The resulting labels salvage useful failure prefixes via reliability decay, while low-value labels mark drift and terminal breakdowns, teaching differences among nominal, failed, and corrective actions. The data engine turns adverse states into planner-generated or human-collected corrective rollouts, teaching recovery to the success manifold. Value-Conditioned Refinement (VCR) trains the policy to prefer high-progress actions. At deployment, a fixed high value ($v=1.0$) biases actions toward the learned success manifold without online failure detectors or heuristic retries. We introduce FRBench, with standardized error injection and recovery-focused evaluation. Across simulated and real-world bimanual（双臂） tasks, RePO-VLA improves robustness, raising adversarial success from 20% to 75% on average and up to 80% in scaled real-world trials.

## 中文简述

提出基于模仿学习的双臂方法，具有长时序任务特点。

**研究方向**: 机器人操控、模仿学习、视觉-语言模型、强化学习、双臂操控

## 关键贡献

1. **RePO-VLA 框架**：两阶段课程——Phase I (RAI) 通过 TSHR 消除因果混淆，Phase II (VCR) 通过 PAS-VF 稠密标签和价值条件化训练让策略学会区分名义动作、失败漂移和纠正恢复。
2. **Progress-Aware Semantic Value Function (PAS-VF)**：基于冻结 V-JEPA 编码器 + 轻量适配器，在共享语义空间中用成功轨迹自参照估计任务进度，无需人工标注。通过可靠性衰减（α=3）保留失败轨迹的有效前缀同时快速抑制终端崩溃。
3. **FRBench**：首个以恢复为一等公民的双臂操控基准，包含分阶段评估协议（Nominal → Error → Recovery）、4 类标准化错误注入（E1–E4）、23,453 模拟 episode 覆盖 46 个任务。
4. **恢复数据缩放趋势**：实验表明 RePO-VLA 的性能随恢复数据密度增加持续提升（1x → 4x），证明恢复数据覆盖度是关键瓶颈。
## 结构化提取

- Problem: VLA 模型在长时序接触丰富操控中面对执行漂移时缺乏恢复能力；成功-only 模仿学习丢弃失败轨迹、恢复轨迹的因果混淆、稀疏二值奖励无法区分行为质量
- Method: 两阶段课程——Phase I RAI（TSHR 消除因果混淆）+ Phase II VCR（PAS-VF 稠密价值标签 + 价值条件化训练）；基于 π0.5 flow-matching 骨干
- Tasks: 双臂操控——Blocks Ranking RGB/Size、Hang Mug、Lift Pot、Move Stapler、Open Laptop、Place Bread/Can/Mouse、Press Stapler（仿真）；Pour Water、Cook Vegetable、Tidy Desk、Fold Towel（真实）
- Sensors: 相机（视觉观测），本体感觉（关节状态）
- Robot Setup: ALOHA-Agilex（仿真 RoboTwin）、Dobot X-Trainer 双臂（真实世界）
- Metrics: 成功率（%），分标准/对抗两种条件；恢复成功率（条件于验证不良状态后）
- Limitations: 依赖代表性失败模式、真实恢复数据昂贵、FRBench-Sim 不含流体/高变形物体、1x 数据下 VCR 不稳定
- Evidence Notes: 全文证据充分，实验覆盖模拟（46 任务 23453 episodes）和真实（4 任务对抗评估），有完整消融（历史重置、价值引导、衰减率）和数据缩放实验（1x→4x）。唯一缺失：FRBench-Sim 到 FRBench-Real 的定量迁移分析。
## 本地引用关系

-
## 证据元数据

- Fulltext Quality: fulltext
- Evidence Coverage: complete（全文通过 arXiv HTML 页面获取，含所有章节、表格、公式和参考文献）
- Confidence: high
- Summary: 提出两阶段恢复驱动策略优化框架 RePO-VLA，通过历史重置初始化消除因果混淆、学习进度感知语义价值函数赋予失败轨迹稠密标签、价值条件化精炼引导策略偏好高进展动作，使 VLA 在对抗扰动下双臂操控成功率从 20% 提升至 75%。


## Problem

VLA 模型在长时序、接触丰富的双臂操控中表现脆弱。核心问题有三层：
1. **成功-only 模仿学习的盲区**：纯 SFT 仅模仿成功示范，失败轨迹被丢弃，但失败轨迹的前期通常包含有效的运动先验（正确的接近、接触准备），直接丢弃浪费了有价值信号。
2. **恢复轨迹的因果混淆**：恢复示范同时包含失败历史、不良状态和纠正动作。直接模仿整条序列会让策略把"先失败"当作"恢复"的必要触发条件（causal confusion），导致部署时无法应对突然出现的扰动。
3. **稀疏二值奖励的不足**：无法区分有用的接近阶段、暂时停滞、主动恢复和终端崩溃。


## Method

### 整体架构

基于 π0.5 flow-matching VLA 骨干的两阶段课程：

**Phase I: Recovery-Aware Initialization (RAI)**
- **Trajectory Slicing with History Reset (TSHR)**：给定恢复起始点 t_rec，丢弃失败前缀，提取纠正段 τ'={(o_t, a_t)}_{t=t_rec}^{T}，并在纠正段首帧清空观测历史缓冲区。
- 目的：让策略学习"状态条件化的恢复技能"而非"特定失败回放"，消除因果混淆。
- 训练目标：L_SFT = L_expert + λ * L_rec_reset，混合专家示范和重置恢复数据。

**Phase II: Value-Conditioned Refinement (VCR)**
1. **PAS-VF 学习**：
   - 冻结 V-JEPA 时空编码器 E_v 提取轨迹动态特征，冻结文本编码器 E_t 编码语言指令
   - 轻量适配器 f_θ 和 g_ϕ 投射到共享语义空间 Z
   - 训练：在成功轨迹上做单调进度对齐 L_align，使余弦相似度追踪归一化时间进度 t/T_τ
   - 推理：自参照进度估计 V(τ_fail) = max_{z∈C_ref} CosSim(z_τ^v, z)，用成功嵌入簇作为参考

2. **Progress-Aware Hindsight Labeling**：
   - 成功轨迹和有效恢复后缀：v_t = 1.0
   - 偏离恢复前缀（错误段）：v_t = 0.0
   - 纯失败轨迹：v_t = V(τ_fail) · (1 - t/T)^α，α=3.0（可靠性衰减）

3. **Value-Conditioned Training**：
   - 在 π0.5 策略中注入价值 token e_val = MLP_val(v_t)
   - Transformer 同时 attend 视觉、语言、历史和价值 token
   - 部署时固定 v=1.0，无需在线失败检测器或启发式重试

### 数据引擎

两种互补来源：
- **拦截式合成注入**：挂钩专家规划器执行节点，在抓取/提升等关键段注入 E1–E4 错误，再用层级规划器生成纠正动作
- **策略诱导回放**：收集已训练基础策略的闭环失败，让专家规划器介入，产生分布内恢复数据

### 错误分类体系 (E1–E4)
- E1: premature_close — 接近阶段提前闭合夹爪
- E2: grasp_slip — 提升阶段强制打开夹爪 30 帧
- E3: grasp_position_offset — 厘米级平移偏移
- E4: grasp_orientation_mismatch — 大角度旋转失配 + 横向稳定偏移


## Experiments

### FRBench-Sim（RoboTwin 模拟，10 个任务，每任务 50 rollouts）

| 条件 | π0.5 Clean | π0.5 Rand | RePO-VLA Clean | RePO-VLA Rand |
|------|-----------|-----------|---------------|--------------|
| 标准执行 | 27.4% | 33.6% | 44.6% (Phase I) | 44.0% (Phase I) |
| 注入失败 | 15.0% | 15.4% | **37.0%** | **43.0%** |

- Phase I 在随机化下稳定性好（44.6→44.0），而 π0 大幅下降（33.9→12.9）
- 注入失败下 Full RePO-VLA 比 π0.5 提升 +22.0%（Clean）和 +27.6%（Random）
- 提升最大的任务是需要真正重新抓取或重新对齐的任务

### FRBench-Real（Dobot X-Trainer 双臂，4 任务，每任务 10 trials）

| 条件 | π0 | π0.5 | Phase I | Full (1x) |
|------|-----|------|---------|-----------|
| 标准（无扰动） | 27.5% | 25.0% | 42.5% | 40.0% |
| 对抗（有扰动） | 12.5% | 20.0% | 37.5% | 30.0% |

- 标准 Phase I (42.5%) > Full 1x (40.0%)，揭示数据密度瓶颈
- 对抗 Phase I (37.5%) > Full 1x (30.0%)，1x 恢复数据不足以支撑 VCR 的价值景观

### 恢复数据缩放（Pour Water + Fold Towel）

| 条件 | π0.5 | Phase I | Full 1x | Full 2x | Full 4x |
|------|------|---------|---------|---------|---------|
| 标准 | 35% | 50% | 40% | 70% | **80%** |
| 对抗 | 20% | 40% | 30% | 65% | **75%** |

- 4x 恢复数据下标准平均 80%（+45 vs π0.5），对抗平均 75%（+55 vs π0.5）
- 明确的数据缩放趋势，恢复数据覆盖度是关键因子

### 消融实验
- **历史重置**：无 TSHR 的原始恢复数据导致因果混淆，恢复成功率大幅下降
- **价值引导 vs 启发式重试**：同样训练数据下，价值条件化 > 简单重试
- **衰减率 α**：α=3 最优；α=1 欠惩罚终端失败，α=10 过度丢弃有用前期动作


## Limitations

1. **错误类型覆盖有限**：依赖观察到的代表性失败模式，超出分类体系的未见错误会降低零样本恢复能力（如流体泄漏、大变形物体）
2. **真实世界恢复数据昂贵**：Phase II 真实数据需要遥操作采集，接触动力学/摩擦/变形难以仿真
3. **FRBench-Sim 范围限制**：尚不涵盖流体和高度可变形物体
4. **1x 数据下 VCR 不稳定**：数据密度不足时 Full 模型甚至不如 Phase I，需要 4x 以上恢复数据才稳定超越
5. **增量迭代但非通用**：当前迭代数据循环可吸收新失败类型，但向未见物理故障的泛化仍是开放问题


## Key Takeaways

1. **失败轨迹是可利用资源**：失败轨迹的有效前缀提供运动先验，终端区域提供"不该做什么"的信号。不应丢弃，而应分解利用。
2. **历史重置消除因果混淆是关键技术**：直接模仿恢复序列会让策略把失败当作恢复的必要条件。TSHR 切断时间因果链，让恢复技能纯粹状态条件化。
3. **稠密价值标签 > 稀疏二值奖励**：PAS-VF 提供连续进度信号，能区分同一轨迹中的有用阶段和崩溃阶段。
4. **部署时 v=1.0 是简洁有效的"恢复吸引子"**：无需在线检测器或重试逻辑，固定高价值条件即可在漂移时激活纠正分支。
5. **恢复数据密度是关键瓶颈**：RePO-VLA 的性能与恢复数据量呈正相关，这对 DLO 操控等需要大量失败模式的场景有重要启示。
6. **对 DLO 操控的启示**：DLO 任务天然具有更多失败模式（缠绕、滑移、形变过度），RePO-VLA 的恢复数据引擎和价值标签框架可能特别适合。

## 相关概念

- [[robotic-manipulation]]
- [[imitation-learning]]
- [[vision-language-model]]
- [[reinforcement-learning]]
- [[bimanual-manipulation]]
- [[deformable-linear-object]]
- [[grasping]]

## 相关研究者

- [[liufu|Liufu, Weijia]]
- [[guo-xiaoyu|Guo, Xiaoyu]]
