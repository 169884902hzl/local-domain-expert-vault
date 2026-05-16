---
title: "VLBiMan: Vision-Language Anchored One-Shot Demonstration Enables Generalizable Bimanual Robotic Manipulation"
tags: [manipulation, imitation, VLM, robot-learning, bimanual]
created: "2026-05-06"
updated: "2026-05-06"
type: "literature"
status: "done"
summary: "提出 VLBiMan 框架，通过一次人类示范的任务感知分解和 VLM 锚定的场景适应，实现无需重训练的可泛化双臂操控，在 10 个任务上以显著优于基线的成功率验证了跨物体实例和跨具身的泛化能力。"
authors: "Zhou, Huayi; Jia, Kui"
year: "2026"
venue: "arXiv Preprint"
zotero_key: "XHZXQ7FS"
---
## 摘要

Achieving generalizable bimanual manipulation（双臂操控） requires systems that can learn efficiently from minimal human input while adapting to real-world uncertainties and diverse embodiments. Existing approaches face a dilemma: imitation policy learning demands extensive demonstrations to cover task variations, while modular methods often lack flexibility in dynamic scenes. We introduce VLBiMan, a framework that derives reusable skills from a single human example through task-aware decomposition, preserving invariant primitives as anchors while dynamically adapting adjustable components via vision-language grounding. This adaptation mechanism resolves scene ambiguities caused by background changes, object repositioning, or visual clutter without policy retraining, leveraging semantic parsing and geometric feasibility constraints. Moreover, the system inherits human-like hybrid control capabilities, enabling mixed synchronous and asynchronous use of both arms. Extensive experiments validate VLBiMan across tool-use and multi-object tasks, demonstrating: (1) a drastic reduction in demonstration（示范数据） requirements compared to imitation baselines, (2) compositional generalization through atomic skill splicing for long-horizon（长时序） tasks, (3) robustness to novel but semantically similar objects and external disturbances, and (4) strong cross-embodiment（具身） transfer, showing that skills learned from human demonstrations can be instantiated on different robotic platforms without retraining. By bridging human priors with vision-language anchored adaptation, our work takes a step toward practical and versatile dual-arm manipulation（双臂操控） in unstructured settings.

## 中文简述

提出基于模仿学习的双臂方法，具有泛化能力特点。

**研究方向**: 机器人操控、模仿学习、视觉-语言模型、机器人学习、双臂操控

## 关键贡献

1. **VLBiMan 框架**：提出基于视觉-语言锚定的一次示范双臂操控框架，无需重训练即可泛化到新场景。
2. **任务感知分解与适应机制**：将示范分解为不变原子技能和可变模块，通过 VLM 提取的物体中心锚点进行几何适应，支持从人类示范到不同机器人具身的跨具身迁移。
3. **大规模实验验证**：在 10 个多样化双臂任务（6 个基础技能 + 2 个长时序组合 + 2 个工具使用）上验证，相比 5 个强基线方法显著领先。
## 结构化提取

- Problem: 端到端模仿学习数据效率低、泛化差，模块化方法依赖脆弱 prompt 且双臂协调不可靠 → 如何从单次示范实现泛化双臂操控
- Method: 三阶段管线——任务感知分解（时空分割 + 原子技能提取 → 不变/可变模块）→ VLM 锚定适应（Florence-2 + SAM2 分割 → 表征点位置差 + 图像矩方向差 → 几何适应）→ 自主轨迹合成（渐进 IK 精化 + 动态碰撞补偿）
- Tasks: 10 个双臂任务——6 个基础（plugpen, inserting, unscrew, pouring, pressing, reorient）+ 2 个长时序组合（reorient+unscrew, unscrew+pouring）+ 2 个工具使用（tool-use spoon, tool-use funnel）
- Sensors: 第三人称双目相机（Kingfisher R-6000, 960×540 RGB），关节编码器提供 6-DoF 末端位姿，二值夹爪状态
- Robot Setup: Aubo-i5 双臂（固定基座，对向配置，880mm 臂展）+ DH-Robotics 平行夹爪（80mm 最大开度）+ Kingfisher R-6000 双目相机；跨具身：Rokae xMate CR7 双臂（人形配置，988mm 臂展）
- Metrics: 成功率（每设置 25 次试验）
- Limitations: 仅刚体；无运行时异常恢复；固定基座无力/触觉传感；人在回路路点精化；需一次物理回放调参
- Evidence Notes: 完整全文精读。核心实验证据来自 Table 1（基础任务成功率）和 Table 2（长时序任务成功率），消融实验 Table 3 量化了 VLM 类型、抓取适应、IK 精化、碰撞避免各自的贡献。错误分析 Fig. 7 提供了失败模式统计。跨具身为定性展示（Fig. 6），无定量成功率数据。
## 本地引用关系

- [[zhou2026vlbiman]]
## 证据元数据

- Fulltext Quality: fulltext
- Evidence Coverage: 完整覆盖主体（引言、方法、实验、结论）和附录核心部分（任务设计、实现细节、消融分析）
- Confidence: high
- Summary: 提出 VLBiMan 框架，通过一次人类示范的任务感知分解和 VLM 锚定的场景适应，实现无需重训练的可泛化双臂操控，在 10 个任务上以显著优于基线的成功率验证了跨物体实例和跨具身的泛化能力。


## Problem

双臂操控面临"数据效率 vs. 泛化能力"的两难困境：端到端模仿学习（如 ALOHA、π0）需要大量遥操作示范数据覆盖任务变化，且新物体/任务需重新采集和训练；模块化方法（如 ReKep、MOKA）虽利用 foundation model 泛化感知能力，但依赖脆弱的 prompt 工程和模糊的中间表征，在复杂双臂协调任务中执行可靠性不足。本文解决的核心问题是：如何从单次人类示范出发，设计一个无需重训练即可泛化到新物体位置、新实例乃至新机器人的双臂操控框架。


## Method

### 整体架构
VLBiMan 包含三个阶段，基于一次示范 `(T, D)` 和新场景 `S_new` 合成可执行双臂轨迹：

### 阶段一：任务感知双臂分解（Task-Aware Bimanual Decomposition）
- **时空分割**：以第三人称双目相机 10 FPS 采集双臂 6-DoF 末端位姿 + 夹爪状态，通过运动动力学变化（速度不连续、加速度尖峰）和状态切换（夹爪开闭）检测关键路点，将轨迹切分为时间片段 `τ_i`。
- **人在回路精化**：人工检查和调整路点的时序和空间分布，确保分割策略 `π_seg` 的鲁棒性。
- **原子技能提取**：对每个片段评估物体-机器人耦合关系——若物体被刚性抓取且几何与示范一致，标记为 **不变模块** `M_inv`（如抬起、双臂对齐）；否则标记为 **可变模块** `M_var`（如接近物体的抓取动作）。

### 阶段二：视觉-语言锚定适应（Vision-Language Anchored Adaptation）
- **VLM 场景理解**：从任务描述提取语义 prompt → Florence-2 + SAM2 获得高质量 2D 语义分割掩码 `M_k^2D`。
- **VFM 几何可行性**（三步）：
  1. 计算"表征点"（2D 掩码质心或桌面接触点）的 3D 位置差 `Δx = p_new - p_demo`
  2. 通过图像二阶矩估计物体主轴方向差 `Δθ`（用于方向敏感物体如笔、勺、横躺瓶子）
  3. 测量类别级形状变化（高度/宽度差异），调整垂直放置或双臂间距
- **设计选择**：不使用 6-DoF 位姿估计（依赖 CAD 模型）或抓取检测（非语义提议脆弱），而是用轻量级图像矩方法提取方向，与 VLM 分割完全兼容。

### 阶段三：自主轨迹合成（Autonomous Trajectory Composition）
- 按原始时序组装不变模块和适应后的可变模块。
- **渐进式 IK 精化**：对初始抓取运动，迭代求解 IK + 样条插值，支持闭环纠偏（物体位移时重新计算目标位姿）。
- **动态碰撞补偿**：在抓取接近阶段添加近端补偿 `δ_base` 和垂直补偿 `δ_z`，减少过早接触风险。
- 执行一次物理回放观察碰撞并调整运动计划。
- 模块化设计支持跨任务模块组装和工具使用任务组合。


## Experiments

### 实验设置
- **平台**：固定基座双臂平台（两个 Aubo-i5 机械臂，平行夹爪，对向配置）+ Kingfisher R-6000 双目相机（第三人称视角）
- **跨具身平台**：Rokae xMate CR7 双臂（人形配置）
- **10 个任务**：plugpen（插笔盖）、inserting（插笔入杯）、unscrew（拧瓶盖）、pouring（倒水）、pressing（按压泵瓶）、reorient（翻转勺子）、reorient+unscrew（扶正瓶子+拧盖）、unscrew+pouring（拧盖+倒水）、tool-use spoon（勺子舀水）、tool-use funnel（漏斗倒水）
- **每个任务至少 2 个类别级物体实例**，测试新位置和新实例泛化
- **评估协议**：每个设置 25 次试验，报告成功率；包含有无动态干扰两种条件

### 基线方法
- **Mechanisms**（Mao et al. 2023）：单次操控策略学习（单臂方法适配）
- **MAGIC**（Liu et al. 2025b）：接触类比单次操控（单臂方法适配）
- **Robot-ABC**（Ju et al. 2024）：关键点 affordance 预测 + AnyGrasp
- **ReKep**（Huang et al. 2024b）：VFM + GPT-4o 关键点约束规划
- **ReKep+**：增强版 ReKep，注入 oracle 级初始抓取标签

### 主要结果（Table 1, 6 个基础任务平均成功率）

| 方法 | 新位置+同物体 | 新位置+新实例 | 同物体+干扰 | 新实例+干扰 |
|------|-------------|-------------|------------|------------|
| Mechanisms | 26.7% | 12.7% | 13.3% | 4.0% |
| MAGIC | 44.7% | 27.3% | 24.7% | 12.0% |
| Robot-ABC | 36.0% | 24.0% | 18.0% | 7.3% |
| ReKep | 43.3% | 29.3% | 22.7% | 15.3% |
| ReKep+ | 63.3% | 42.7% | 38.0% | 25.3% |
| **VLBiMan** | **85.3%** | **78.0%** | **69.3%** | **59.3%** |

### 长时序/工具使用任务（Table 2, 4 个任务平均成功率）

| 方法 | 同物体 | 新实例 | 同物体+干扰 | 新实例+干扰 |
|------|--------|--------|------------|------------|
| Mechanisms | 12.0% | 3.0% | 3.0% | 0.0% |
| ReKep+ | 34.0% | 19.0% | 24.0% | 12.0% |
| **VLBiMan** | **52.0%** | **41.0%** | **38.0%** | **24.0%** |

### 消融实验（Table 3, 基础任务, 新实例+干扰）
- 完整系统 vs. SAM+DINOv2 替代 VLM → 59.2% vs. 35.8%
- 完整系统 vs. AnyGrasp 替代抓取适应 → 59.2% vs. 31.7%
- 完整系统 vs. 无 IK 精化 → 59.2% vs. 29.2%
- 完整系统 vs. 无碰撞避免 → 59.2% vs. 34.2%

### 错误分析（Fig. 7）
- 最大误差来源：初始抓取执行（尽管计算相对可靠）
- 第二大误差：双臂协调（双臂任务核心挑战）
- VLM 感知和锚定占比较小，表明 VLM 分割对当前任务足够可靠

### 跨具身迁移
定性展示了在 Rokae xMate CR7 人形双臂平台上的 4 个任务成功迁移（Fig. 6），无需重训练。


## Limitations

1. **仅限刚体物体**：不处理布料、绳索等可变形物体，需不同的表征和控制方式。
2. **缺乏运行时异常检测和恢复**：对滑移、遮挡等执行错误敏感，无闭环纠偏机制。
3. **硬件限制**：固定基座限制可达工作空间，缺乏力/触觉传感。
4. **人在回路分割精化**：虽然作者声称负担可忽略，但路点精化仍需人工参与。
5. **一次物理回放调参**：新物体组合需要一次物理回放观察碰撞并调整，非完全零接触部署。


## Key Takeaways

1. **不变-可变分解思想对 DLO 操控的启示**：VLBiMan 将抓取后的刚性耦合运动标记为"不变"并跨场景复用，这一思想可迁移到 DLO 场景中——例如，双臂夹持 DLO 后的搬运阶段可视为不变模块，而接近 DLO 的抓取阶段需要适应 DLO 的形变状态。
2. **VLM 锚定 vs. 端到端学习**：本文证明在结构化双臂任务中，VLM 分割 + 轻量几何适应可以大幅超越端到端模仿学习方法（尤其在新实例泛化上），这对 DLO 操控中选择系统架构有参考价值——当任务具有清晰的物体-技能分解结构时，模块化方法可能比端到端更高效。
3. **跨具身迁移的可行路径**：技能的模块化存储使得从人类示范到不同机器人平台的迁移成为可能，这对 Sim-to-Real 场景下的技能迁移有启发。
4. **局限性与 DLO 场景的差距**：VLBiMan 的物体中心锚点（掩码质心、接触点）依赖刚体假设，DLO 的连续形变无法用离散锚点表征，但其"任务感知分解"的思想（哪些子动作可以复用、哪些需要在线适应）仍然适用。

## 相关概念

- [[robotic-manipulation]]
- [[imitation-learning]]
- [[vision-language-model]]
- [[robot-learning]]
- [[bimanual-manipulation]]
- [[deformable-linear-object]]
- [[grasping]]

## 相关研究者

- [[zhou|Zhou, Huayi]]
- [[jia|Jia, Kui]]
