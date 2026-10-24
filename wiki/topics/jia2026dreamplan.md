---
title: "DreamPlan: Efficient reinforcement fine-tuning of vision-language planners via video world models"
tags: [manipulation, imitation, VLM, RL, DLO]
created: "2026-05-11"
updated: "2026-05-11"
type: "literature"
status: "done"
summary: "通过零样本 VLM 采集探索数据训练 action-conditioned 视频世界模型，再在想象中用 ORPO 对 VLM 规划器做强化微调，在绳/布/软体任务上将 Qwen3-VL-8B 平均得分从 0.33 提升至 0.60，推理仅需约 1 秒。"
authors: "Jia, Emily Yue-Ting; Yuan, Weiduo; Shi, Tianheng; Guizilini, Vitor; Mao, Jiageng et al."
year: "2026"
venue: "arXiv Preprint"
zotero_key: "U9QDNEKA"
---
## 摘要

Robotic manipulation（机器人操控） requires sophisticated commonsense reasoning, a capability naturally possessed by large-scale Vision-Language Models (VLMs). While VLMs show promise as zero-shot（零样本） planners, their lack of grounded physical understanding often leads to compounding errors and low success rates when deployed in complex real-world environments, particularly for challenging tasks like deformable object（可变形物体） manipulation（操控）. Although Reinforcement Learning（强化学习） (RL) can adapt these planners to specific task dynamics, directly fine-tuning VLMs via real-world interaction is prohibitively expensive, unsafe, and sample-inefficient. To overcome this bottleneck, we introduce DreamPlan, a novel framework for the reinforcement fine-tuning of VLM planners via video world models. Instead of relying on costly physical rollouts, DreamPlan first leverages the zero-shot（零样本） VLM to collect exploratory interaction data. We demonstrate that this sub-optimal data is sufficient to train an action-conditioned video generation model, which implicitly captures complex real-world physics. Subsequently, the VLM planner is fine-tuned entirely within the "imagination" of this video world model using Odds Ratio Policy Optimization (ORPO). By utilizing these virtual rollouts, physical and task-specific knowledge is efficiently injected into the VLM. Our results indicate that DreamPlan bridges the gap between semantic reasoning and physical grounding, significantly improving manipulation（操控） success rates without the need for large-scale real-world data collection. Our project page is https://psi-lab.ai/DreamPlan/.

## 中文简述

提出基于强化学习的操控方法，具有零样本泛化特点。

**研究方向**: 机器人操控、模仿学习、视觉-语言模型、强化学习、可变形物体操控

## 关键贡献

1. **DreamPlan 框架**：提出完全在视频世界模型想象中完成 VLM 规划器强化微调的闭环管线，无需大规模真实交互数据。
2. **Best-of-K + ORPO 高效策略**：将昂贵的视频扩散推理与策略优化解耦——通过 Best-of-K 采样构建偏好对，再用 ORPO 进行对比优化，避免在优化循环中反复查询世界模型。
3. **DLO 实验验证**：在绳索拉直、布料折叠、软体玩具手臂重定位三个真实世界 DLO 任务上验证，平均得分近乎翻倍（0.33→0.60），推理时间仅 ~1.12 秒。
## 结构化提取

- **Problem**: 零样本 VLM 规划器在 DLO 操控中缺乏物理接地导致低成功率；真实世界 RL 微调代价高昂；DLO 高保真仿真困难。
- **Method**: 三阶段框架：(1) 零样本 VLM 自动采集探索数据；(2) ControlNet-conditioned 视频扩散世界模型学习 DLO 动力学；(3) Best-of-K 采样 + ORPO 偏好优化进行 VLM 强化微调。
- **Tasks**: Rope Straightening, Cloth Folding, Toy Arm Repositioning（均为真实世界 DLO 任务）。
- **Sensors**: 第三视角 RealSense D435i RGB 相机（960×540, 30Hz）。
- **Robot Setup**: 双臂 Franka FR3，对置安装，间距 140cm，Cartesian 末端执行器控制 30Hz，32GB RTX 5090 GPU。
- **Metrics**: 人工评分 {0, 0.5, 1}，每任务 10 次随机初始状态试验取平均。
- **Limitations**: 单步评价、任务特定世界模型、依赖 GPT-4o 验证器、离散 keypoint 动作空间受限、仅 3 个任务、统计样本量小。
- **Evidence Notes**: 全文可获取，所有主要实验结果均有数据支撑。缺失：世界模型数据规模消融、K 值敏感性分析、跨任务世界模型迁移实验。
## 本地引用关系

-
## 证据元数据

- Fulltext Quality: fulltext
- Evidence Coverage: complete (all sections including method, experiments, ablations)
- Confidence: high
- Summary: 通过零样本 VLM 采集探索数据训练 action-conditioned 视频世界模型，再在想象中用 ORPO 对 VLM 规划器做强化微调，在绳/布/软体任务上将 Qwen3-VL-8B 平均得分从 0.33 提升至 0.60，推理仅需约 1 秒。


## Problem

零样本 VLM 规划器具备常识推理能力但缺乏物理接地，在 DLO 操控等接触密集任务中成功率低。直接用真实世界 RL 微调 VLM 代价极高且不安全，而 DLO 的高保真仿真难以构建，sim-to-real gap 严重。现有视频世界模型多限于刚体交互，无法可靠预测可变形物体的动力学行为。


## Method

### 整体流程（三阶段）

**Stage 1: 零样本 VLM 提案**
- 输入当前观测图像 $o_t$ 和目标图像 $g$
- 用 SAM2 提取物体 mask，Farthest Point Sampling 提取关键点集合 $\mathcal{K}_t$ 和 $\mathcal{K}_g$
- VLM（Qwen3-VL-8B）选择 source keypoint（抓取位置）和 target keypoint（放置位置），输出离散动作 $a_t = (k_s^i, k_g^j)$
- 通过零样本执行自动采集 ~2056 条轨迹（约 4 小时真实交互）

**Stage 2: 世界模型学习**
- 基于 CogVideoX-5B (image-to-video) 微调，引入 ControlNet 架构注入渲染的机器人手臂轨迹作为 action conditioning
- 关键设计：训练模型预测裁剪后的**物体独占视频**（白色背景），避免重建无关细节（光照、机械臂、背景）
- 噪声预测公式：$\hat{\epsilon} = \epsilon_\theta(\mathbf{x}_t, t, c) + \Delta_\phi(\mathbf{x}_t, t, \mathbf{r})$，其中 $\mathbf{r} = \text{render}(a_{0:H-1})$
- 损失函数为标准去噪目标 $\mathcal{L}_{\text{diff}}$

**Stage 3: 世界模型引导的 RL 对齐**
- 对每个训练样本 $(o_0, g)$，从 VLM 采样 K 个候选动作
- 用世界模型预测每个动作的物理结果
- GPT-4o 对比预测结果与目标图像，选出最优动作 $a^*$ 作为正样本，其余为负样本
- 用 ORPO 优化：$\mathcal{L}_{\text{ORPO}} = \log \sigma(\log \pi_\theta(a^*|s) - \log \pi_\theta(a^-|s))$
- ORPO 直接最大化偏好动作的对数几率比，无需单独的价值函数

### 动作表示

离散 keypoint 动作空间：$a_t = (k_s^{i_t}, k_g^{j_t})$，source keypoint 定义抓取位置，target keypoint 定义放置位置。2D 像素坐标通过深度相机反投影到 3D 笛卡尔空间，由固定运动序列执行。


## Experiments

### 硬件设置
- 双臂 Franka FR3，对置安装，间距 140cm
- RealSense D435i（960×540 RGB, 30Hz）
- Cartesian 末端执行器位姿控制 30Hz
- 工作站：32GB NVIDIA RTX 5090

### 任务与评价
- **三个任务**：Rope Straightening, Cloth Folding, Toy Arm Repositioning
- 每任务 10 次试验（随机初始状态）
- 单步评价（单次动作原语后评分）：{0, 0.5, 1}

### 主结果（Table I）

| Method | Rope ↑ | Cloth ↑ | Toy Arm ↑ | Avg ↑ |
|--------|--------|---------|-----------|-------|
| Qwen3-VL-4B | 0.10 | 0.15 | 0.40 | 0.22 |
| Qwen3-VL-8B | 0.20 | 0.10 | 0.70 | 0.33 |
| Qwen3-VL-32B | 0.30 | 0.05 | 0.70 | 0.35 |
| GPT-4o | 0.30 | 0.00 | 0.55 | 0.28 |
| **DreamPlan** (Qwen3-VL-8B + RL) | **0.60** | **0.35** | **0.85** | **0.60** |

### 效率对比（Table III）

| Method | Avg Score ↑ | Time (s) ↓ | TFLOPs ↓ |
|--------|-------------|------------|----------|
| 显式验证 N=4 | 0.48 | 926.32 | 7.82×10⁴ |
| 显式验证 N=8 | 0.50 | 2605.56 | 1.56×10⁵ |
| **DreamPlan** | **0.60** | **1.12** | **15.14** |

### 消融实验

**世界模型预测质量（Table II）**：
- Full-Scene 预测 PSNR: 24.70
- Object-Only 预测 PSNR: 26.25（+1.55）

**缺失证据**：未报告世界模型训练数据规模消融、不同 K 值的敏感性分析、跨任务泛化能力（是否需每个任务单独训练世界模型）。


## Limitations

1. **单步评价**：每次试验只执行一个动作原语，未展示多步序列操控能力
2. **任务特定世界模型**：每个 DLO 任务需要单独训练世界模型（~4h 数据采集 + 微调），跨任务迁移未验证
3. **依赖 GPT-4o 作为验证器**：训练阶段需要 GPT-4o 做偏好排序，引入外部 API 依赖和成本
4. **离散 keypoint 动作空间**：受限于预设的抓取-放置模式，无法表达复杂操控策略（如缠绕、扭转）
5. **SAM2 需手动初始化**：首次需要手动提供 bounding box 启动 SAM2 mask 传播
6. **仅 3 个任务**：实验规模有限，每个任务仅 10 次试验，统计显著性受限
7. **DLO 类型局限**：绳索和布料之外的 DLO（如线缆、链条）未测试


## Key Takeaways

1. **次优数据足够训练世界模型**：零样本 VLM 采集的失败/次优数据（~2000 条轨迹）即可训练可靠的 DLO 视频世界模型，降低数据采集门槛
2. **Object-Only 视频预测是关键**：裁剪物体区域、白色背景训练视频模型可显著提升变形预测质量
3. **Best-of-K + ORPO 解耦范式**：将视频生成与策略优化分离，实现 ~800 倍推理加速（1.12s vs 926s），对实时部署至关重要
4. **RL 微调 VLM 在 DLO 上有巨大增益**：仅 RL 微调即可将 8B 模型超越 32B 零样本模型，说明物理接地比模型规模更重要
5. **Action Conditioning via ControlNet + Rendered Trajectory**：将机器人运动渲染为视频作为 ControlNet 输入，比文本条件更精准地编码动作信号

## 相关概念

- [[robotic-manipulation]]
- [[imitation-learning]]
- [[vision-language-model]]
- [[reinforcement-learning]]
- [[deformable-linear-object]]
- [[bimanual-manipulation]]
- [[grasping]]

## 相关研究者

- [[jia-emily-yue-ting|Jia, Emily Yue-Ting]]
- [[yuan-weiduo|Yuan, Weiduo]]
- [[shi-tianheng|Shi, Tianheng]]
- [[guizilini-vitor|Guizilini, Vitor]]
