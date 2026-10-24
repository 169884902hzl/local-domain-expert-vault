---
title: "Plan in sandbox, navigate in open worlds: Learning physics-grounded abstracted experience for embodied navigation"
tags: [imitation, VLM, RL, robot-learning, physics-simulation]
created: "2026-05-15"
updated: "2026-05-15"
type: "literature"
status: "done"
summary: "提出 SAGE 框架，通过物理沙盒生成合成经验（Genesis）、非对称自适应裁剪 RL 训练（Evolution）、检索增强导航（Navigation）三阶段，将 VLM 高层语义推理蒸馏为可执行导航策略，在 A-EQA 上达到 53.21% SR†（+9.7%），并成功部署到 Qizhi ROS 实体机器人。"
authors: "Shen, Zhixuan; Du, Jiawei; Guo, Ziyu; Luo, Han; Peng, Lilan et al."
year: "2026"
venue: "arXiv Preprint"
zotero_key: "K7I382M8"
---
## 摘要

Vision-Language Models (VLMs) have demonstrated exceptional general reasoning capabilities. However, their performance in embodied navigation remains hindered by a scarcity of aligned open-world vision and robot control data. Despite simulators providing a cost-effective alternative for data collection, the inherent reliance on photorealistic simulations often limits the transferability of learned policies. To this end, we propose \textit{\textbf{S}andbox-\textbf{A}bstracted \textbf{G}rounded \textbf{E}xperience} (\textbf{\textit{SAGE}}), a framework that enables agents to learn within a physics-grounded semantic abstraction rather than a photorealistic simulation, mimicking the human capacity for mental simulation where plans are rehearsed in simplified physics abstractions before execution. \textit{SAGE} system operates via three synergistic phases: (1) \textit{Genesis}: constructing diverse, physics-constrained semantic environments to bootstrap experience; (2) \textit{Evolution}: distilling experiences through Reinforcement Learning（强化学习） (RL), utilizing a novel asymmetric adaptive clipping mechanism to stabilize updates; (3) \textit{Navigation}: bridging the abstract policy to open-world control. We demonstrate that \textit{SAGE} significantly improves planner-assisted embodied navigation, achieving a 53.21\% LLM-Match Success Rate on A-EQA (+9.7\% over baseline), while showing encouraging transfer to physical indoor robot deployment.

## 中文简述

提出基于强化学习的导航方法。

**研究方向**: 模仿学习、视觉-语言模型、强化学习、机器人学习、物理仿真

## 关键贡献

1. **生成式经验驱动学习范式**：提出全新的生成式经验驱动学习范式，利用物理沙盒自主合成任务和抽象经验来解决数据稀缺和真实世界迁移问题
2. **Genesis 阶段**：在物理约束的语义沙盒中自主合成多样化任务，将 VLM 高层推理能力蒸馏为结构化具身经验（任务元组 + IF-THEN 经验规则）
3. **非对称自适应裁剪（AAC）**：在 Evolution 阶段提出混合提示增强采样和 AAC 机制，使策略能在稳健吸收经验先验的同时保持训练稳定性——增强样本使用放宽的 ε_exp 上界，标准样本使用保守的 ε_std 下界
4. **Navigation 阶段**：通过 Frontier/Memory Buffer 分解高层意图为几何规划器可执行的子目标，桥接语义推理与低层控制的间隙
## 结构化提取

- Problem: VLM 在具身导航中受数据稀缺和语义-控制断层限制，RL 从零学习样本效率极低
- Method: 三阶段框架——Genesis（沙盒合成任务+经验规则）、Evolution（混合提示增强采样+非对称自适应裁剪 RL）、Navigation（检索增强的 Frontier/Memory Buffer 选择+几何规划执行）
- Tasks: 具身问答导航（A-EQA）、多模态终身导航（GOAT-Bench）
- Sensors: RGB-D 相机（Kinect v2），深度 512×424，RGB 1920×1080
- Robot Setup: Qizhi ROS 机器人，相机高 1.5m，客户端-服务器架构（RTX 4090 推理），WiFi 通信
- Metrics: LLM-Match SR†、LLM-Match SPL†（A-EQA）；标准 SR、SPL（GOAT-Bench，1.0m 阈值）
- Limitations: 仅室内、准静态假设、非端到端控制、真实世界证据规模有限
- Evidence Notes:

  - Table 1: SAGE (2B) 在 A-EQA 上 SR† 53.21%（超 3D-Mem GPT-4o），SAGE (4B) 达 60.2% SOTA
  - Figure 5: MIX 数据策略最优；12.5% 数据即达 44.75% SR†
  - Figure 4: 动态 η 调度优于固定值；ε_exp=1.0 最优
  - Table 3: 组件逐步叠加均带来正向增益，C_ret 在训练后策略上产生协同效应
  - Table 4: 训练内化先验（+6.29%）+ 推理时检索联合使用效果最佳
  - Appendix J: Qizhi ROS 实体机器人成功完成室内导航-问答循环
## 本地引用关系

- [[shen2026plan]]
## 证据元数据

- Fulltext Quality: fulltext (arXiv HTML 全文，含正文和附录)
- Evidence Coverage: high (覆盖完整方法、实验、消融、Real-World 部署、Limitations)
- Confidence: high
- Summary: 提出 SAGE 框架，通过物理沙盒生成合成经验（Genesis）、非对称自适应裁剪 RL 训练（Evolution）、检索增强导航（Navigation）三阶段，将 VLM 高层语义推理蒸馏为可执行导航策略，在 A-EQA 上达到 53.21% SR†（+9.7%），并成功部署到 Qizhi ROS 实体机器人。


## Problem

VLM 虽具备强大的语义推理能力，但在具身导航中受限于：
1. **数据稀缺**：缺乏大规模对齐的开放世界视觉-机器人控制数据
2. **Sim2Real 鸿沟**：依赖真实感仿真的策略迁移性差，像素级仿真与真实场景的模态鸿沟大
3. **语义-控制断层**：VLM 的语义推理空间与机器人连续执行空间之间存在巨大间隙，策略部署到噪声环境时脆弱
4. **RL 样本效率低**：缺少结构化先验时，RL 代理受困于冷启动和严重样本低效


## Method

### 整体框架：三阶段 SAGE

**阶段 1：Genesis（创世）**
- 基于大规模室内数据集（HM3D + InteriorGS）构建物理约束语义沙盒环境 E_S
- 连续空间解析为离散可导航节点图，状态转移动力学 P 严格遵循碰撞约束
- 自动化任务合成流水线：
  1. 随机采样起点-终点对，A* 计算最优测地轨迹 τ*
  2. 离散化为 T 个关键点，每个关键点渲染 3 视角中间观测（前、左120°、右120°）
  3. 正前方观测作为 ground-truth 动作 a*
  4. 将检测到的物体投影到语义场景图
  5. VLM 基于轨迹终点和可见实体合成自然语言指令 I 和对应答案
- **经验规则合成**：对轨迹中每步，提示 VLM 解释为什么选择正前方而非其他 frontier，形成 IF-THEN 推理规则，存入向量数据库 D_exp

**阶段 2：Evolution（进化）**
- 基于 Group Relative Policy Optimization (GRPO) 的 RL 训练
- **奖励设计**：格式合规性 + 语义对齐的加权和（格式指示器 + 正确选择逻辑 + 文本相似度 - 错误惩罚）
- **混合提示增强采样**：
  - 动态控制器以时变概率 η_t 注入检索到的经验 K_ret
  - η_t 随验证集奖励提升而退火：η_t = max(η_min, η_init · (1 - min(R_val, R_target)/R_target))
  - Bernoulli 采样决定是否注入经验（m=1 为增强样本，m=0 为标准样本）
- **同质组优势估计**：确保组内所有样本使用相同 mask，避免增强样本高奖励偏移标准样本基线
- **非对称自适应裁剪（AAC）**：
  - 下界统一使用保守 ε_std（防止策略崩塌）
  - 上界根据样本类型动态调整：增强样本使用放宽 ε_exp >> ε_std，标准样本使用 ε_std
  - 核心洞察：增强样本允许激进更新以快速内化经验，标准样本保守更新保持稳定

**阶段 3：Navigation（导航）**
- 检索增强的具身导航范式
- **感知**：RGB-D 观测 → 动态 3D 场景图 + 占据地图 → Memory Buffer M_t（已见物体/地标）+ Frontier Buffer F_t（未探索边界）
- **经验增强**：从向量数据库 D_exp 检索最相关经验 C_ret，与当前观测合成为复合提示
- **规划与执行**：VLM 策略 π_θ 从 F_t ∪ M_t 选择目标节点 → 几何规划器执行导航（仿真用 Habitat follower，真实用 ROS navigation stack）
- 每步最大移动距离 δ_max = 1.0m，到达目标节点 0.5m 邻域内终止


## Experiments

### 评估基准
1. **A-EQA**：557 个自然语言问题，63 个真实室内场景，验证集 184 题。指标：LLM-Match SR† 和 SPL†（使用 Qwen3-235B-A22B 作为自动评估器）
2. **GOAT-Bench**：5-10 个连续子任务，Val Unseen 子集 278 个子任务，36 个场景。指标：标准 SR 和 SPL（1.0m 成功阈值）

### 主要结果（Table 1）
| 方法 | A-EQA SR† | A-EQA SPL† | GOAT-Bench SR | GOAT-Bench SPL |
|------|-----------|------------|---------------|----------------|
| SenseAct-NN (RL) | 14.62 | 5.73 | 27.34 | 14.53 |
| LLaVA-7B (VLM) | 19.35 | 8.21 | 31.65 | 17.32 |
| 3D-Mem (GPT-4o) | 50.50 | 32.80 | 49.28 | 32.50 |
| 3D-Mem (Qwen2-VL-2B) | 43.49 | 16.16 | 31.95 | 16.16 |
| **SAGE (Qwen3-VL-2B)** | **53.21** | **37.07** | **42.27** | **30.59** |
| 3D-Mem (Qwen2-VL-4B) | 48.28 | 19.00 | 37.94 | 19.00 |
| **SAGE (Qwen3-VL-4B)** | **60.20** | **42.05** | **44.96** | **34.84** |

关键发现：
- SAGE (2B) 在 A-EQA SR† 上超过 3D-Mem (GPT-4o) 2.71 个百分点，证明开源小模型经沙盒蒸馏后可匹敌闭源巨头
- 相同 backbone 下，SAGE (2B) vs 3D-Mem (2B)：A-EQA +8.9%，GOAT-Bench +10.3%，SPL 接近翻倍
- SAGE (4B) 在 A-EQA 上达到 60.2% 新 SOTA

### 消融实验

**合成数据组成（Figure 5a）**：MIX（HM3D+InteriorGS）策略最优（SR† 53.21%），单一数据源次之，证明场景多样性对泛化关键

**数据规模（Figure 5b）**：14,526 条轨迹（100%）为最优；仅 12.5% 数据即可达 SR† 44.75%，确认框架在少量数据下也有效；边际收益递减但 SPL† 持续提升

**经验注入概率（Figure 4a-b）**：固定 η 大小均不如动态调度；动态调度在早期保留经验引导，随验证性能提升逐渐退火

**裁剪上界（Figure 4c-d）**：保守 ε_exp=0.4 导致欠拟合；激进 ε_exp=1.2 在 100 步后不稳定；最优 ε_exp=1.0 平衡吸收与稳定

**视觉上下文长度（Table 2）**：v_t=4 帧最优，2 帧不足，5 帧冗余注意力稀释

**组件消融（Table 3）**：
- 零样本 + C_ret：+1.74%（4B），验证沙盒知识质量
- + Task：主驱动力，2B 达 50.71%
- + Exp & AAC：额外 +1.17%（2B），+1.89%（4B）
- + C_ret（完整 SAGE）：策略学会"如何推理"，实时检索提供"推理什么"

### Real-World 部署（Appendix J）
- 机器人：Qizhi ROS 平台 + Kinect v2 RGB-D（深度 512×424, RGB 1920×1080）
- 相机高度 1.5m，pitch=0°
- 客户端-服务器架构：机器人端压缩图像至 256×256 通过 WiFi 传输，服务器端 NVIDIA RTX 4090 推理
- 成功完成 "What is the object on the table beside the large wooden door?" 查询的完整导航-回答循环
- 注意：真实世界证据规模有限，主要验证可行性


## Limitations

1. **仅限室内**：沙盒语义先验（房间连接性、物体 affordance）不能直接迁移到非结构化户外或大规模城市导航
2. **准静态环境假设**：VLM 推理延迟（Table 14）造成实时反应动态实体的瓶颈，可通过模型量化缓解
3. **非端到端控制**：SAGE 是 planner-assisted 高层语义导航，依赖可靠的 frontier 生成、占据地图和几何执行
4. **真实世界证据有限**：主要在室内准静态条件下验证可行性，规模较小


## Key Takeaways

1. **语义抽象 > 真实感仿真**：SAGE 证明使用物理约束的语义抽象环境（而非真实感仿真）合成经验，迁移效果更好——这与我们 DLO 操控中"简化物理、强调结构"的思路一致
2. **VLM 蒸馏到 RL 策略的有效范式**：通过沙盒经验规则将 VLM 高层推理蒸馏为低层策略，绕过了直接在真实世界探索的冷启动问题
3. **非对称裁剪的通用价值**：AAC 策略对不同质量样本使用不同约束强度，可能适用于任何混合数据源的 RL 训练场景
4. **检索增强导航**：将经验规则存入向量数据库并在推理时检索的范式，与 RAG 思路一致但应用于机器人决策
5. **数据效率**：12.5% 数据即可达到相当性能（44.75%），说明沙盒经验质量比数量更重要

## 相关概念

- [[imitation-learning]]
- [[vision-language-model]]
- [[reinforcement-learning]]
- [[robot-learning]]
- [[sim-to-real]]
- [[deformable-linear-object]]

## 相关研究者

- [[shen-zhixuan|Shen, Zhixuan]]
