---
title: "ForceVLA2: Unleashing Hybrid Force-Position Control with Force Awareness for Contact-Rich Manipulation"
tags: [manipulation, VLM, RL, robot-learning]
created: "2026-05-07"
updated: "2026-05-07"
type: "literature"
status: "done"
summary: "ForceVLA2 在 VLA 框架中引入 force prompt 驱动的长时推理和 Cross-Scale MoE 实现混合力-位姿控制，在5个接触丰富任务上平均成功率66%，超过π0和π0.5分别48%和35%。"
authors: "Li, Yang; Zhaxizhuoma; Jiang, Hongru; Xia, Junjie; Zhang, Hongquan et al."
year: "2026"
venue: "arXiv Preprint"
zotero_key: "BMTE3CDB"
---
## 摘要

Embodied intelligence for contact-rich（接触丰富） manipulation（操控） has predominantly relied on position control, while explicit awareness and regulation of interaction forces remain under-explored, limiting stability, precision, and robustness in real-world tasks. We propose ForceVLA2, an end-to-end（端到端） vision-language-action framework that equips robots with hybrid force-position control and explicit force awareness. ForceVLA2 introduces force-based prompts into the VLM expert to construct force-aware task concepts across stages, and employs a Cross-Scale Mixture-of-Experts (MoE) in the action expert to adaptively fuse these concepts with real-time interaction forces for closed-loop（闭环） hybrid force-position regulation. To support learning and evaluation, we construct ForceVLA2-Dataset, containing 1,000 trajectories over 5 contact-rich（接触丰富） tasks, including wiping, pressing, and assembling, with multi-view images, task prompts, proprioceptive state, and force signals. Extensive experiments show that ForceVLA2 substantially improves success rates and reliability in contact-rich（接触丰富） manipulation（操控）, outperforming pi0 and pi0.5 by 48.0% and 35.0%, respectively, across the 5 tasks, and mitigating common failure modes such as arm overload and unstable contact, thereby actively advancing force-aware interactive physical intelligence in VLAs. The project page is available at https://sites.google.com/view/force-vla2/home.

## 中文简述

提出基于视觉-语言的操控方法，具有闭环控制特点。

**研究方向**: 机器人操控、视觉-语言模型、强化学习、机器人学习

## 关键贡献

1. **首个端到端混合力-位姿控制 VLA 框架**：通过 Force Prompt 驱动 VLM 推理构建力感知任务概念，通过 Cross-Scale MoE 在 action expert 中自适应融合视觉、状态、力信息，实现闭环混合力-位姿控制
2. **ForceVLA2-Dataset**：首个包含 force prompt（任务分解标注）和力控制监督的数据集，1000 条轨迹、5 个接触丰富任务、约 500K 同步时间步
3. **显著性能提升**：5 个任务平均成功率 66%，比 π0 提升 48%，比 π0.5 提升 35%，在 Assemble gears 任务上超越次优方法 50 个百分点
## 结构化提取

- **Problem**: 现有 VLA 仅支持位姿控制，力作为辅助感知输入而非主动控制信号，controllability index 仅 0.5，无法在接触丰富任务中独立调节力
- **Method**: 双层架构——Force Prompt 驱动 PaliGemma VLM 长时推理 + Cross-Scale MoE（3 个模态专家）短时反应控制 + Flow Matching 生成混合力-位姿动作 [Δp, f, ι]
- **Tasks**: Press bottle, Clean vase, Clean board, Retrieve plate, Assemble gears（5 个接触丰富操控任务）
- **Sensors**: 3× RGB 相机（2× Intel D455 第三人称视角 + 1× D435 腕部视角，480×640）、6D 力/力矩传感器（300 Hz）、EE 6D 位姿
- **Robot Setup**: 7-DOF Flexiv Rizon 4s 机械臂 + DH Robotics AG-95 自适应夹爪，GELLO 力反馈遥操作采集
- **Metrics**: 成功率（每任务 20 次独立试验）
- **Limitations**: 仅 5 任务/单臂/20 trials per task，Force Prompt 依赖预定义子任务列表（非零样本），附录内名混用
- **Evidence Notes**:

  - 主实验：5 baseline 对比 + 5 任务完整成功率数据（Table 1）
  - 模块消融：FP/ME/CM 逐步添加，单调提升（Table 2）
  - 模态融合消融：VM 和 FM 贡献相当（Table 3）
  - 力注入位置消融：VLM pathway 严重退化至 5%（Table 5）
  - 理论分析附录：证明纯位姿控制的 controllability rank deficiency（Appendix A）
  - 数据集统计附录：力/力矩分布、技能分布（Appendix B）
  - 动态扰动和重抓取定性测试（Fig. 5-6）
## 本地引用关系

- [[brohan2023rt2]]
- [[collaboration2025open]]
- [[kim2024openvla]]
## 证据元数据

- Fulltext Quality: fulltext（完整 arXiv 预印本，含正文 + 4 个附录）
- Evidence Coverage: high（完整方法描述、5 任务实验、3 组消融、理论分析附录）
- Confidence: high
- Summary: ForceVLA2 在 VLA 框架中引入 force prompt 驱动的长时推理和 Cross-Scale MoE 实现混合力-位姿控制，在5个接触丰富任务上平均成功率66%，超过π0和π0.5分别48%和35%。


## Problem

现有 VLA 模型（π0、π0.5、OpenVLA 等）依赖纯末端执行器位姿控制，力仅作为辅助感知输入而非主动控制信号。这导致在接触丰富的操控任务中存在以下限制：
1. **力不可控**：纯位姿控制下，力是环境动力学的被动输出（controllability index 仅 0.5），无法独立调节
2. **缺乏力感知的任务推理**：视觉-语言信息不足以表达接触阶段的物理状态（如航天插头插入、齿轮装配）
3. **子任务转换缺乏物理依据**：现有 VLA 依赖先验或视觉判断阶段切换，无法利用力信号判断子任务完成度


## Method

### 整体架构：双层设计（仿人运动控制系统）

ForceVLA2 基于 π0 框架扩展，采用受人类感知运动控制启发的双层设计：

**长时推理层（Long-Horizon Force Awareness via Prompting）**：
- 输入：多视角 RGB 图像 + 任务文本 prompt + Force Prompt
- Force Prompt：文本形式编码当前子任务状态，每个任务预定义子任务列表，Force Prompt 作为离散状态机决定是否维持或转换子任务
- VLM 采用 PaliGemma（SigLIP 视觉编码器），输出融合上下文 token E ∈ R^{(N_v+N_t+N_s)×D}

**短时反应层（Short-Horizon Force-to-Control Loop）**：
- EE 6D 位姿 p ∈ R^7 经线性层编码为 E_p
- 原始 6D 力/力矩 f_raw ∈ R^6 经线性映射编码为 E_f
- 力编码走两条路径：
  1. **长时路径**：E_state = [E_p; E_f] 经 cross-attention 与 VLM 特征交互，注入全局任务语义
  2. **短时反应路径**：E_f 直接旁路至 MoE，保留梯度保真度实现快速力反馈

**Cross-Scale MoE（自适应模态路由）**：
- 3 个模态专家：视觉专家、状态专家、力专家（各为轻量 MLP）
- 动态门控网络逐 token 计算路由权重，自适应选择当前操控阶段的主导模态
- 自由空间运动侧重视觉推理，接触阶段侧重力/位姿信号

**Flow Matching 策略头**：
- 从噪声迭代去噪生成混合动作：a_t = [Δp_t, f_t, ι_t]
  - Δp_t ∈ R^7：EE 位姿变化
  - f_t ∈ R^6：预测接触力
  - ι_t ∈ [0,1]：子任务转换概率
- 子任务转换概率建模：基于方向对齐度 Θ（Beta 分布）、剩余距离 ρ（指数分布）、接触力 F（均匀分布）的联合概率

### 训练配置
- 8× A100 GPU，batch size 32，30K steps，约 10 小时
- 推理速度：15 Hz（4090 GPU，chunk size 30）
- 优化器：AdamW + Cosine Decay，EMA 0.99


## Experiments

### 数据集
ForceVLA2-Dataset：
- 5 个任务：Press bottle（按压瓶子）、Clean vase（擦拭花瓶）、Clean board（擦拭板）、Retrieve plate（取盘）、Assemble gears（装配齿轮）
- 每任务 200 条轨迹，共约 500K 时间步
- 技能分布：Explore 45.62%，Wipe、Push、Grasp、Rotate 分布其余
- 数据采集：GELLO 力反馈遥操作

### 主要结果（Table 1，每任务 20 次试验）

| Method | Press bottle | Clean vase | Clean board | Retri. plate | Assem. gears | Avg. |
|--------|:-----------:|:----------:|:-----------:|:-----------:|:-----------:|:----:|
| π0 | 35.0 | 20.0 | 35.0 | 0.0 | 0.0 | 18.0 |
| π0.5 | 45.0 | 30.0 | 45.0 | 15.0 | 20.0 | 31.0 |
| ACP | 25.0 | 30.0 | 25.0 | 0.0 | 0.0 | 16.0 |
| π0 w/ F | 30.0 | 25.0 | 20.0 | 10.0 | 0.0 | 17.0 |
| ForceVLA | 70.0 | 25.0 | 55.0 | 15.0 | 10.0 | 35.0 |
| **ForceVLA2** | **80.0** | **75.0** | **70.0** | **35.0** | **70.0** | **66.0** |

### 消融研究

**模块消融（Table 2）**——在 π0 基础上逐步添加模块：
- +Force Prompt (FP)：+9%（18% → 27%）
- +FP +Multimodal Encoder (ME)：+13%（27% → 40%）
- +FP +ME +Cross-Scale MoE (CM)：+26%（40% → 66%），Cross-Scale MoE 贡献最大

**MoE 模态融合消融（Table 3）**：
- 仅状态：36% → +VM：50%（+14）→ +VM+FM：66%（+16）
- 视觉和力模态贡献相当，均为必要输入

**力注入位置消融（Table 5）**：
- VLM pathway 注入：5%（严重退化）
- Multimodal Encoder 注入：58%
- State Fusion（最终方案）：66%
- 结论：力信息不应注入 VLM pathway，会破坏预训练 VLM 表示

### 额外定性测试
- 动态力跟踪：突然降低底座时，ForceVLA2 快速适应新接触构型完成按压
- 擦拭鲁棒性：花瓶旋转致法线偏移时，ForceVLA2 沿表面滑动维持接触
- 重抓取探索：Retrieve plate 中力引导探测实现自主重试


## Limitations

1. **任务覆盖有限**：仅 5 个接触丰富任务，Retrieve plate 成功率仅 35%，泛化能力未验证
2. **单平台测试**：仅在 Flexiv Rizon 4s 单臂上评估，未跨机器人验证
3. **统计量有限**：每任务仅 20 次试验，统计置信区间较宽
4. **简单力任务性能退化**：对力需求简单的任务（如 Press bottle），额外 force token 可能略微降低性能（Table 3 中仅 VM 时 85% vs VM+FM 时 80%）
5. **无仿真基准**：全部为真实世界实验，无可复现仿真环境
6. **名称混用**：附录中多处出现"Foca-VLA"/"Foca-Dataset"等内部代号，与正文 ForceVLA2 不一致
7. **Force Prompt 依赖预定义子任务**：每个任务需人工定义子任务列表，限制了零样本泛化能力


## Key Takeaways

1. **力必须作为主动控制信号**：论文从控制理论证明纯位姿控制的 controllability index 仅 0.5，混合力-位姿控制可扩展可达集。DLO 操控中柔性物体交互力同样关键，应考虑混合控制而非仅位姿输出
2. **双路径设计有效**：长时推理（VLM+Force Prompt）+ 短时反应（force bypass to MoE）的分层设计适合需要高层规划和低层精细控制的场景
3. **Force Prompt 作为任务分解机制**：将子任务状态编码为文本 prompt 输入 VLM，比端到端隐式推理更可控、可解释
4. **Cross-Scale MoE 自适应模态选择**：在自由空间运动和接触阶段自动切换主导模态，值得借鉴到 DLO 操控中（自由空间靠视觉、接触阶段靠力/触觉）
5. **力注入位置至关重要**：力信息不应注入 VLM pathway（会破坏预训练表示），应在 action expert 层面融合
6. **GELLO 遥操作数据采集**：力反馈遥操作方案可考虑用于 DLO 数据集构建
7. **12 维混合动作空间**：位姿增量(7D)+力(6D)-1D转换指标=12D，比传统 6D 位姿动作空间提供更大控制自由度

## 相关概念

- [[robotic-manipulation]]
- [[vision-language-model]]
- [[reinforcement-learning]]
- [[robot-learning]]
- [[deformable-linear-object]]
- [[grasping]]

## 相关研究者

- [[li-yang|Li, Yang]]
- [[zhaxizhuoma|Zhaxizhuoma]]
