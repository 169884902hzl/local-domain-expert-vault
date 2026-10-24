---
title: "LangForce: Bayesian decomposition of vision language action models via latent action queries"
tags: [manipulation, imitation, VLM, RL]
created: "2026-05-16"
updated: "2026-05-16"
type: "literature"
status: "done"
summary: "揭示 VLA 模型在目标驱动数据集上的\"视觉捷径\"病理（语言条件互信息坍缩为零），提出基于贝叶斯分解的双分支框架 LangForce，通过 Latent Action Queries 和最大化 Pointwise Mutual Information 强制语言指令参与动作决策，在 SimplerEnv OOD 场景提升 11.3%。"
authors: "Lian, Shijie; Yu, Bin; Lin, Xiaopeng; Yang, Laurence T.; Shen, Zhaolong et al."
year: "2026"
venue: "arXiv Preprint"
zotero_key: "V3BN6W6X"
---
## 摘要

Vision-Language-Action (VLA) models have shown promise in robot manipulation（机器人操控） but often struggle to generalize to new instructions or complex multi-task（多任务） scenarios. We identify a critical pathology in current training paradigms where goal-driven data collection creates a dataset bias. In such datasets, language instructions are highly predictable from visual observations alone, causing the conditional mutual information between instructions and actions to vanish, a phenomenon we term Information Collapse. Consequently, models degenerate into vision-only policies that ignore language constraints and fail in out-of-distribution (OOD) settings. To address this, we propose LangForce, a novel framework that enforces instruction following via Bayesian decomposition. By introducing learnable Latent Action Queries, we construct a dual-branch architecture to estimate both a vision-only prior $p(a \mid v)$ and a language-conditioned posterior $π(a \mid v, \ell)$. We then optimize the policy to maximize the conditional Pointwise Mutual Information (PMI) between actions and instructions. This objective effectively penalizes the vision shortcut and rewards actions that explicitly explain the language command. Without requiring new data, LangForce significantly improves generalization. Extensive experiments across on SimplerEnv and RoboCasa demonstrate substantial gains, including an 11.3% improvement on the challenging OOD SimplerEnv benchmark, validating the ability of our approach to robustly ground language in action.

## 中文简述

提出基于视觉-语言的操控方法，具有泛化能力特点。

**研究方向**: 机器人操控、模仿学习、视觉-语言模型、强化学习

## 关键贡献

1. **识别并实证验证"视觉捷径"病理**：通过三组实验证明标准 VLA 模型在目标驱动数据上普遍忽略语言指令，退化为视觉策略
2. **提出 LangForce 框架**：利用 Latent Action Queries 和双分支贝叶斯目标，从有偏数据中恢复真正的语言条件化策略，无需新数据
3. **SOTA 性能**：SimplerEnv OOD 提升 11.3%（55.2%→66.5%），LIBERO Goal 99.4%，RoboCasa 52.6%
## 结构化提取

- Problem: VLA 模型在目标驱动数据集上学习视觉捷径，忽略语言指令，导致 OOD 泛化失败和灾难性遗忘
- Method: LangForce——基于贝叶斯分解的双分支训练框架，引入 Latent Action Queries（64 个可学习 token）作为 VLM-DiT 瓶颈，最大化动作与语言的条件 PMI（LLR 目标）
- Tasks: 桌面物体操控（pick-and-place, stacking, articulated object manipulation）
- Sensors: 单目 RGB 相机（视觉观测）
- Robot Setup: WidowX 机器人（SimplerEnv）、Franka Panda（LIBERO）、GR1 人形机器人（RoboCasa）
- Metrics: 成功率（Avg@480 for SimplerEnv, Avg@500 for LIBERO, Avg@50 for RoboCasa）
- Limitations: 训练计算开销（双分支），多模态理解退化，仅在仿真和 4B 模型验证
- Evidence Notes: 三组实验系统性验证视觉捷径（§2.1-2.3），条件熵定量分析（Table 3），消融实验确认各组件贡献（Table 5-8），通用能力保持的定性证据（Fig 4-5）
## 本地引用关系

-
## 证据元数据

- Fulltext Quality: fulltext
- Evidence Coverage: complete（全文含正文、附录、消融实验）
- Confidence: high
- Summary: 揭示 VLA 模型在目标驱动数据集上的"视觉捷径"病理（语言条件互信息坍缩为零），提出基于贝叶斯分解的双分支框架 LangForce，通过 Latent Action Queries 和最大化 Pointwise Mutual Information 强制语言指令参与动作决策，在 SimplerEnv OOD 场景提升 11.3%。


## Problem

当前 VLA 模型在目标驱动数据集（goal-driven dataset）上训练时，语言指令与视觉观测之间存在近乎确定性的映射（看到一个柜子几乎总是意味着"打开柜子"），导致条件互信息 $I(\ell; a|v)$ 坍缩为零——作者称之为 **Information Collapse**。结果是模型退化为纯视觉策略 $p(a|v)$，忽略语言约束，在 OOD 环境和模糊场景中灾难性失败。

三个实证证据：
1. **ID 测试中的视觉捷径**（RoboCasa）：Vision-Only 模型成功率 44.6%，接近语言条件化基线的 47.8%
2. **模糊场景失败**（LIBERO Goal）：同一视觉场景对应多个任务时，Vision-Only 从 97.4% 暴跌到 9.8%
3. **OOD 泛化失败**（SimplerEnv）：在 BridgeDataV2 上训练损失相当（0.13 vs 0.08），但 OOD 评测成功率接近 0%


## Method

### 核心思想：贝叶斯分解

最优策略可分解为：
$$\pi(a|v,\ell) = \frac{p(\ell|a,v) \cdot p(a|v)}{p(\ell|v)}$$

当 $p(\ell|v)$ 足够尖锐（目标驱动数据集），似然项坍缩，策略退化为先验 $p(a|v)$。

### 解决方案：最大化 Log-Likelihood Ratio

$$\mathcal{L}_{LLR} = \log \frac{\pi(a|v,\ell)}{p(a|v)} = \log p(\ell|a,v) - \log p(\ell|v)$$

等价于最大化动作与指令之间的条件 Pointwise Mutual Information (PMI)。

### 架构：Latent Action Queries

- 在 VLM 词表中添加 K=64 个可学习 token $\mathcal{Q}$
- 这些 token 作为 VLM 与 DiT 动作头之间的瓶颈接口
- 通过改变 $\mathcal{Q}$ 在输入序列中的位置，利用因果注意力掩码精确控制信息流向

### 双分支训练

1. **Priori Branch**（视觉先验）：输入 $[v, \mathcal{Q}, \ell]$，$\mathcal{Q}$ 只能看到视觉信息，学习 $p(a|v)$
   - 梯度 detach $\mathbf{H}_\mathcal{Q}^{prior}$，防止共享 VLM 骨干学到视觉捷径
2. **Posteriori Branch**（后验策略）：输入 $[v, \ell, \mathcal{Q}]$，$\mathcal{Q}$ 可以看到视觉+语言，学习 $\pi(a|v,\ell)$
3. **LLR 目标**：$\mathcal{L}_{LLR} = \log p(\ell|v, \mathbf{H}_\mathcal{Q}^{prior}) - \text{sg}(\log p(\ell|v))$
   - stop-gradient 防止模型通过降低 baseline 来走捷径

### 总损失

$$\mathcal{L}_{total} = (1-\lambda)\mathcal{L}_{FM}(\mathbf{H}_\mathcal{Q}^{post}) + \lambda\mathcal{L}_{FM}(\mathbf{H}_\mathcal{Q}^{prior}) - \beta\mathcal{L}_{LLR}$$

其中 $\lambda=0.3$，$\beta=0.1$，使用 Rectified Flow Matching 作为动作预测损失。

### 推理

仅使用 Posteriori Branch，无额外计算开销。


## Experiments

### SimplerEnv（OOD 泛化）
- 训练数据：BridgeDataV2 + Fractal，8×H100，50k steps，batch 16/device
- 评测：4 个操控任务，480 次独立试验

| Method | Avg |
|--------|-----|
| RT-1-X | 1.1% |
| Octo-Small | 26.7% |
| OpenVLA-OFT | 41.8% |
| π₀ | 53.1% |
| π₀.₅ | 57.1% |
| Isaac-GR00T N1.6 | 57.1% |
| **QwenGR00T (Baseline)** | **55.2%** |
| **LangForce** | **66.5%** |

核心结果：比同框架基线提升 **+11.3%**，在 "Put Carrot on Plate" (+13.8%) 和 "Put Eggplant" (+25.0%) 上改进最大。

### LIBERO（ID 性能）
- 一个策略训练 4 个子集

| Method | Spatial | Object | Goal | Long | Avg |
|--------|---------|--------|------|------|-----|
| VisionOnly | 90.2 | 99.6 | 9.8 | 86.0 | 71.4 |
| QwenGR00T | 97.8 | 98.8 | 97.4 | 92.0 | 96.5 |
| **LangForce** | **99.2** | **99.6** | **99.4** | **95.2** | **98.4** |

Goal 子集（有模糊性）提升 +2.0%。条件熵分析：LangForce 的 NLL 9.47 vs baseline 8.51，PPL 12964.9 vs 4964.1，证明模型保持了 $H(\ell|v)$ 的不确定性。

### RoboCasa（24 个桌面任务）
- 评测：50 次独立试验/任务

| Method | Avg |
|--------|-----|
| VisionOnly | 44.7% |
| QwenGR00T | 47.8% |
| QwenOFT | 48.8% |
| **LangForce** | **52.6%** |

Vision-Only 44.7% vs 基线 47.8% 再次证实视觉捷径的普遍性。

### 通用能力保持
- 标准 QwenGR00T 精调后丧失文本对话能力（灾难性遗忘）
- LangForce 通过 LLR 目标保持了 VLM 的文本推理能力

### 消融实验
- **贝叶斯分解 vs 纯架构**：+Action Query 57.5% → +LLR 66.5%（+9.0%），核心提升来自贝叶斯目标
- **λ 消融**：即使 λ=0（不直接监督先验分支），LLR 目标仍带来 63.3%（vs baseline 55.2%）
- **β 消融**：β=0 时双分支架构本身已达 61.3%，加入 LLR 后 66.5%
- **Query 数量**：64 个 query 为最优（16→49.7%, 32→56.2%, 64→57.5%, 128→57.5%）


## Limitations

1. **训练计算开销**：双分支需要同时计算先验和后验（但通过 prefix prefill 策略可大幅缓解）
2. **视觉-语言联合能力退化**：文本推理能力保持，但多模态（图像+文本）理解仍有退化
3. **实验局限**：仅在仿真环境中验证，尚未进行真实机器人实验；仅在 4B 模型上验证，未测试更大模型
4. **数据集依赖**：理论分析假设目标驱动数据集的 $H(\ell|v) \approx 0$，对于多模态数据（如人类视频）的分析不够深入
5. **与 BayesVLA 无法直接对比**：BayesVLA 未开源代码


## Key Takeaways

1. **视觉捷径是 VLA 训练中的系统性问题**：不是个别模型的缺陷，而是目标驱动数据收集方式的根本性偏差
2. **贝叶斯视角提供优雅的理论框架**：通过分解策略为先验和后验，可以用信息论工具诊断和修复模型行为
3. **Latent Action Queries 是通用架构组件**：作为 VLM 和动作头之间的瓶颈，不仅服务于 LangForce，还能降低 DiT 的计算复杂度从 $O(N^2)$ 到 $O(K^2)$
4. **对数据收集的启示**：应在模糊场景中收集数据（同一场景多个任务），以自然增加 $H(\ell|v)$
5. **与 DLO 操控的关联**：DLO 操控任务通常具有高度视觉相似性（同一根绳子不同目标构型），语言消歧能力至关重要，LangForce 的思路可以直接迁移

## 相关概念

- [[robotic-manipulation]]
- [[imitation-learning]]
- [[vision-language-model]]
- [[reinforcement-learning]]
- [[deformable-linear-object]]

## 相关研究者

- [[lian|Lian, Shijie]]
- [[yang-laurence|Yang, Laurence T.]]
