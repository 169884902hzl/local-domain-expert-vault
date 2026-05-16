---
title: "NS-VLA: Towards neuro-symbolic vision-language-action models"
tags: [manipulation, imitation, VLM, RL]
created: "2026-05-03"
updated: "2026-05-03"
type: "literature"
status: "done"
summary: "将 VLA 拆分为符号化原语规划 + 稀疏化视觉求解器 + 在线 RL 优化的三层框架，在 LIBERO 1-shot 和 LIBERO-Plus 扰动环境下均达到 SOTA"
authors: "Zhu, Ziyue; Wu, Shangyang; Zhao, Shuai; Zhao, Zhiqiu; Li, Shengjie et al."
year: "2026"
venue: "arXiv Preprint"
zotero_key: "RKPH4WDK"
---
## 摘要

Vision-Language-Action (VLA) models are formulated to ground instructions in visual context and generate action sequences for robotic manipulation（机器人操控）. Despite recent progress, VLA models still face challenges in learning related and reusable primitives, reducing reliance on large-scale data and complex architectures, and enabling exploration beyond demonstrations. To address these challenges, we propose a novel Neuro-Symbolic Vision-Language-Action (NS-VLA) framework via online reinforcement learning（强化学习） (RL). It introduces a symbolic encoder to embedding vision and language features and extract structured primitives, utilizes a symbolic solver for data-efficient（数据高效） action sequencing, and leverages online RL to optimize generation via expansive exploration. Experiments on robotic manipulation（机器人操控） benchmarks demonstrate that NS-VLA outperforms previous methods in both one-shot（单样本） training and data-perturbed settings, while simultaneously exhibiting superior zero-shot（零样本） generalizability, high data efficiency and expanded exploration space. Our code is available.

## 中文简述

提出基于强化学习的操控方法，具有零样本泛化特点。

**研究方向**: 机器人操控、模仿学习、视觉-语言模型、强化学习

## 关键贡献

1. **Neuro-Symbolic Encoding**：引入符号编码器（Symbolic Classifier），从 VLM token 特征中提取结构化原语计划（primitive plan），通过单调计划指针（monotone plan pointer）约束原语切换，实现结构化任务分解
2. **Symbolic Solver**：设计 query-driven 视觉 token 稀疏化（Soft Top-K），将 N 个视觉 token 压缩为单个上下文向量；使用因果 Transformer 生成 H 步动作 chunk，降低计算冗余
3. **NS-GRPO 在线 RL 优化**：提出原语分段奖励（primitive-segmented reward）和 KL 锚定策略，在保持 BC 参考策略稳定性的同时实现广泛环境探索
4. **全面的实验验证**：在 LIBERO（1-shot）、LIBERO-Plus（扰动泛化）、CALVIN（零样本 ABC→D）三个基准上均达到 SOTA
## 结构化提取

- **Problem**: 端到端 VLA 模型缺乏结构感知、数据依赖严重、探索空间有限
- **Method**: 神经-符号 VLA 框架（NS-VLA）：符号编码器提取结构化原语 → 符号求解器生成动作 chunk → 在线 RL（NS-GRPO）优化
- **Tasks**: 机器人桌面操控（pick-place, open/close, turn on, 等）
- **Sensors**: RGB 图像 + 本体感知状态
- **Robot Setup**: 仿真环境（LIBERO/LIBERO-Plus/CALVIN），Franka Panda 机器人
- **Metrics**: Success Rate (SR%), 5-Task Success Rate (CALVIN), Average Sequence Length
- **Limitations**: 手工定义原语、仅仿真验证、单调指针约束对动态任务灵活性不足
- **Evidence Notes**:

  - LIBERO 1-shot: NS-VLA 69.1% avg SR，超越所有 7B 级 baseline
  - LIBERO-Plus: 79.4% avg SR，最小性能衰减（19.2%）
  - CALVIN ABC→D: 91.2% 5-task SR，比 VLA-Adapter 高 11.2%
  - 消融显示 Primitive Classifier 贡献最大（移除后 SR 降 18.9%）
  - 不同 backbone 规模（2B/4B/8B）性能接近，验证符号先验的数据效率
## 本地引用关系

- [[zhu2026nsvla]]
## 证据元数据

- Fulltext Quality: fulltext
- Evidence Coverage: 完整覆盖主体（Introduction → Conclusion）和附录（Appendix A-H），含所有表格、公式和实验结果
- Confidence: high
- Summary: 将 VLA 拆分为符号化原语规划 + 稀疏化视觉求解器 + 在线 RL 优化的三层框架，在 LIBERO 1-shot 和 LIBERO-Plus 扰动环境下均达到 SOTA


## Problem

当前 VLA 模型面临三大挑战：
1. **缺乏结构感知**：端到端 VLA 直接生成动作序列，无法捕获任务间共享的可复用原语（primitives），导致泛化能力差
2. **数据依赖严重**：成功高度依赖大规模数据和复杂架构，为每个任务收集大量 demonstration 不现实
3. **探索空间有限**：基于 SFT 的方法仅模仿专家轨迹，限制了环境探索能力


## Method

NS-VLA 框架由三个紧密耦合的组件构成：

### 4.1 Neuro-Symbolic Encoder
- **输入**：预训练 VLM（Qwen3-VL）编码当前观测 $o_t = \{I_t, S_t\}$（图像 + 本体感知）和语言指令 $x$
- **计划生成**：episode 开始时，VLM 生成原语序列 $p = (u^{(1)}, ..., u^{(M)})$，每个原语 $u^{(m)} \in \mathcal{U}$ 描述"操作什么"和"怎么操作"
- **Symbolic Classifier**：MLP $g_\phi$ 将池化后的 VLM 特征映射为原语分布；推理时通过单调指针约束 $\mathcal{K}(m_{t-1}) = \{m_{t-1}, \min(m_{t-1}+1, M)\}$ 限制切换选择
- **监督**：分段端窗口交叉熵损失 $\mathcal{L}_{cls}$，聚焦原语切换边界帧

### 4.2 Symbolic Solver
- **视觉 Token 稀疏化**：
  - 原语嵌入作为 query，计算与 N 个视觉 token 的相关性分数
  - 训练时用可微 Soft Top-K（sigmoid + 温度 $\tau$），推理时用硬 Top-K
  - 加权聚合得到单个紧凑上下文向量 $\mathbf{c}_t$
- **Action Generator**：
  - 拼接 $e_t = [\mathbf{c}_t; \text{Embed}(\hat{u}_t); S_t]$
  - 因果 Transformer 处理历史 $e_{0:t}$，输出 H 步动作 chunk $\mathbf{A}_t$

### 4.3 Online RL（NS-GRPO）
- **POMDP 建模**：历史 $\mathcal{H}_t = (x, o_{0:t}, a_{0:t-1})$，分层策略 $\pi_\Theta(u_t, \mathbf{A}_t | \mathcal{H}_t)$
- **Primitive-Segmented Reward**：
  - $r_t^{seg} = b_t$（分段完成奖励）
  - $r_t^{prog} = \gamma\Phi_{t+1} - \Phi_t$（段内进度塑造，基于参考原型最近距离）
  - $r_t = r_t^{task} + \lambda_{seg} r_t^{seg} + \lambda_{prog} r_t^{prog}$
- **GRPO + KL 锚定**：
  - G 条 rollout 组内标准化 advantage
  - KL 散度惩罚约束策略偏离 BC 参考策略，提升稀疏奖励下的稳定性
- **冻结模块**：VLM encoder 和计划生成器冻结，仅更新 lightweight 模块（classifier $\phi$ + action generator $\theta$）


## Experiments

### 数据集
- **LIBERO**（Liu et al., 2023）：4 个子集（Spatial/Object/Goal/Long），1-shot 训练（每任务 1 条 demonstration）
- **LIBERO-Plus**（Fei et al., 2025b）：7 维扰动（光照/纹理/空间布局等），用完整 LIBERO 训练集训练
- **CALVIN**（Mees et al., 2022）：ABC→D 零样本泛化，5-task 连续成功率

### 主要结果

**LIBERO 1-shot（SR%）**：

| Method | Spatial | Object | Goal | Long | Avg |
|--------|---------|--------|------|------|-----|
| NS-VLA (2B) | **85.7** | **75.3** | **70.7** | **45.2** | **69.1** |
| VLA-Adapter (0.5B) | 80.6 | 71.6 | 69.8 | 39.2 | 65.3 |
| OpenVLA (7B) | 47.4 | 46.0 | 44.3 | 4.9 | 35.7 |
| π₀ (3B) | 48.6 | 47.2 | 33.2 | 20.4 | 37.4 |

**LIBERO-Plus（SR%，完整训练）**：

| Method | Spatial | Object | Goal | Long | Avg |
|--------|---------|--------|------|------|-----|
| NS-VLA (2B) | **88.1** | **79.0** | **70.2** | **80.3** | **79.4** |
| OpenVLA-OFT (7B) | 84.0 | 66.5 | 63.0 | 66.4 | 69.6 |
| RIPT-VLA (7B) | 85.8 | 64.3 | 58.0 | 67.5 | 68.4 |

**CALVIN ABC→D**：
- NS-VLA: 91.2% 5-task SR, 4.72 avg length
- VLA-Adapter: 80.0%, 4.50

### 消融实验
- 移除 Primitive Classifier: 98.6% → 79.7%（影响最大）
- 移除 Vision Extractor: 98.6% → 90.1%
- 移除 Action Generator: 98.6% → 85.2%
- 移除 RL: 98.6% → 91.6%
- NS-GRPO vs 标准 GRPO：收敛更快、最终成功率更高

### 数据效率
- 不同 VLM backbone（2B/4B/8B Qwen3-VL）下 SR 和原语准确率均接近（98.6%-98.9% SR, 94.1%-95.5% 准确率）
- 1-shot vs full-demo 训练差距小，符号计划先验作为强归纳偏置显著降低数据需求


## Limitations

1. **原语需手工定义**：当前原语集 $\mathcal{U}$ 和标注需要人工设计（如 pickplace_on, pickplace_in, close, turn_on 等），未来方向包括自动原语发现
2. **仅在仿真环境验证**：实验全部在 LIBERO/LIBERO-Plus/CALVIN 仿真基准上完成，尚未进行 Sim-to-Real 验证
3. **可扩展性待验证**：符号化方法在更复杂、原语更多样的真实场景下的扩展能力尚未证明
4. **VLM 冻结策略**：预训练 VLM encoder 和计划生成器在 RL 阶段冻结，可能限制端到端优化效果
5. **原语分段假设**：单调指针约束假设任务严格按预定义原语序列执行，对动态/反应性任务（如 DLO 操控中的连续形变）可能不够灵活


## Key Takeaways

1. **对 DLO 操控的启示**：神经-符号分层架构将高层原语规划与低层动作生成分离的思路，可借鉴到 DLO 操控中——将"抓取端点"、"穿过环"、"打结"等定义为原语，通过符号计划约束序列，但 DLO 的连续形变特性可能需要放松单调约束
2. **视觉稀疏化的价值**：query-driven Top-K 稀疏化方法，以当前原语为 query 动态选择相关视觉区域，在 DLO 操控中可用于聚焦于绳子末端、交叉点等关键视觉特征，降低背景干扰
3. **在线 RL 探索**：NS-GRPO 在稀疏奖励下通过 KL 锚定实现稳定优化，这种策略可应用于 DLO 操控的 RL fine-tuning，特别是当任务奖励稀疏时
4. **数据效率**：符号计划先验使 2B 模型在 1-shot 下超越 7B 模型，表明结构化知识可以弥补规模差距，这对 DLO 数据稀缺场景有重要意义

## 相关概念

- [[robotic-manipulation]]
- [[imitation-learning]]
- [[vision-language-model]]
- [[reinforcement-learning]]
- [[deformable-linear-object]]
- [[grasping]]

## 相关研究者

- [[zhu-ziyue|Zhu, Ziyue]]
