---
title: "Uncovering linguistic fragility in vision-language-action models via diversity-aware red teaming"
tags: [manipulation, imitation, VLM, RL, robot-learning]
created: "2026-05-10"
updated: "2026-05-10"
type: "literature"
status: "done"
summary: "提出 DAERT 框架，利用基于 ROVER 的多样性感知强化学习训练 VLM 攻击者，自动生成语义保持但导致 VLA 执行失败的对抗指令，将 π₀ 成功率从 93.33% 降至 5.85%，且攻击可跨模型和跨域迁移。"
authors: "Tong, Baoshun; He, Haoran; Pan, Ling; Liu, Yang; Lin, Liang"
year: "2026"
venue: "arXiv Preprint"
zotero_key: "P8GAG2G2"
---
## 摘要

Vision-Language-Action (VLA) models have achieved remarkable success in robotic manipulation（机器人操控）. However, their robustness to linguistic nuances remains a critical, under-explored safety concern, posing a significant safety risk to real-world deployment. Red teaming, or identifying environmental scenarios that elicit catastrophic behaviors, is an important step in ensuring the safe deployment of embodied AI agents. Reinforcement learning（强化学习） (RL) has emerged as a promising approach in automated red teaming that aims to uncover these vulnerabilities. However, standard RL-based adversaries often suffer from severe mode collapse due to their reward（奖励）-maximizing nature, which tends to converge to a narrow set of trivial or repetitive failure patterns, failing to reveal the comprehensive landscape of meaningful risks. To bridge this gap, we propose a novel \textbf{D}iversity-\textbf{A}ware \textbf{E}mbodied \textbf{R}ed \textbf{T}eaming (\textbf{DAERT}) framework, to expose the vulnerabilities of VLAs against linguistic variations. Our design is based on evaluating a uniform policy, which is able to generate a diverse set of challenging instructions while ensuring its attack effectiveness, measured by execution failures in a physical simulator. We conduct extensive experiments across different robotic benchmarks against two state-of-the-art（现有最优方法） VLAs, including $π_0$ and OpenVLA. Our method consistently discovers a wider range of more effective adversarial instructions that reduce the average task success rate from 93.33\% to 5.85\%, demonstrating a scalable approach to stress-testing VLA agents and exposing critical safety blind spots before real-world deployment.

## 中文简述

提出基于强化学习的操控方法。

**研究方向**: 机器人操控、模仿学习、视觉-语言模型、强化学习、机器人学习

## 关键贡献

1. **问题形式化**：将 VLA 的语言鲁棒性测试形式化为"指令语言脆弱性"问题，建立了最小化 VLA 成功率与最大化指令多样性之间的优化目标（Eq. 1）
2. **多样性感知 RL 攻击器**：首次利用基于 ROVER（Random Policy Valuation）的多样性感知强化学习策略微调 VLM（Qwen3-VL-4B）生成对抗指令，有效避免模式坍缩
3. **级联物理约束奖励**：设计了三级门控奖励机制（结构有效性 → 语义保真 → 长度约束），确保生成的指令在物理上可行且语义保持
4. **强迁移性**：攻击策略在跨 VLA 架构（π₀ → OpenVLA）和跨域（LIBERO → CALVIN → SimplerEnv）零样本迁移中保持高效，攻击成功率比基线高 +59.7%
## 结构化提取

- **Problem**: VLA 模型对语义等价但措辞不同的语言指令极其脆弱，现有红队测试方法受模式坍缩限制无法全面揭示风险
- **Method**: DAERT 框架——用 Qwen3-VL-4B 作为攻击者，通过基于 ROVER 的多样性感知 RL 训练，结合级联门控奖励（结构有效性 + CrossEncoder 语义保真 + 长度约束），生成多样化对抗指令
- **Tasks**: 语言条件桌面操控（LIBERO: Object/Spatial/Goal/Long），跨域迁移到 CALVIN 和 SimplerEnv（Google Robot 场景）
- **Sensors**: 单目 RGB 图像（初始场景）+ 机器人本体感知状态
- **Robot Setup**: LIBERO 仿真环境（Franka Panda 机械臂），CALVIN（Franka Panda），SimplerEnv（Google Robot）
- **Metrics**: 任务成功率 Succ(↓)、CLIP 余弦距离 Cos(↑)、LLM-as-Judge 多样性评分 LLM(↑)、攻击性能（1 - success_rate）
- **Limitations**: 生成的指令偏向冗长/过度描述；未引入人工评估；仅在短时桌面任务验证；仅测试 π₀ 和 OpenVLA；未结合视觉扰动；π₀.5 因视觉主导而无法评估语言鲁棒性
- **Evidence Notes**: 全文可获取。主要实验结果（Table 2-3, Figure 2）来自 LIBERO/CALVIN/SimplerEnv 基准，支持核心声称。消融实验仅做了 KL 约束消融，缺少对 ρ、τ_sem、L_max 的系统消融。定性分析基于 PCA 可视化和 4 个案例，有说服力但非统计显著
## 本地引用关系

- [[kim2024openvla]]
## 证据元数据

- Fulltext Quality: fulltext
- Evidence Coverage: 完整覆盖方法、实验、消融、定性分析和附录
- Confidence: high
- Summary: 提出 DAERT 框架，利用基于 ROVER 的多样性感知强化学习训练 VLM 攻击者，自动生成语义保持但导致 VLA 执行失败的对抗指令，将 π₀ 成功率从 93.33% 降至 5.85%，且攻击可跨模型和跨域迁移。


## Problem

当前 VLA 模型（如 π₀、OpenVLA）在机器人操控中取得了显著成功，但对语言指令的变化极其脆弱——即使语义等价但措辞不同的指令也能导致灾难性执行失败。现有自动化红队测试方法（如基于 GPT-4o 的 ERT）依赖冻结的 LLM 提示，缺乏适应性；而标准 RL 方法（如 GRPO）因奖励最大化特性导致严重的模式坍缩（mode collapse），只能发现狭窄、重复的失败模式，无法揭示完整的风险图谱。


## Method

### 整体架构

DAERT 由三个核心组件构成：

1. **攻击者策略**（Attacker Policy）：基于 Qwen3-VL-4B 的 VLM，接收原始任务指令 + 初始场景 RGB 图像，输出语义保持但具有攻击性的改写指令
2. **多样性感知 RL 训练**：基于 ROVER 的隐式 Actor-Critic，避免标准 GRPO 的模式坍缩
3. **级联奖励设计**：三级门控确保生成指令的有效性和语义一致性

### 多样性感知训练（核心创新）

标准 RL 目标（Eq. 2-3）虽然有熵正则化项，但在稀疏二元奖励下仍容易坍缩到单一模式。DAERT 引入了 ROVER 式的均匀策略评估：

- **隐式 Q 参数化**（Eq. 4）：Q_θ(a_t|s_t) = ρ(log p_θ(a_t|s_t) - log p_θ_old(a_t|s_t))，无需额外训练 Critic
- **多样性感知目标**（Eq. 5）：Q̂(a_t|s_t) = r̃ + (1/|V|)Σ Q_θ(a_{t+1}|s_{t+1})，用均匀平均后继值替代贪婪最大值，惩罚尖锐概率峰
- **组相对训练**：每组采样 n 个改写，标准化奖励 r̃_i = r_i - mean(r)，缓解稀疏奖励的不稳定性
- **最终损失**（Eq. 6）：最小化 Bellman 误差，带 stop-gradient

### 级联奖励设计

三级顺序门控：

1. **可执行格式门**：拒绝换行符、元前缀（"Rewrite:"）、非英文字符 → r_struct = -0.2
2. **动作意图保持门**：CrossEncoder（stsb-roberta-large）语义相似度 ≥ τ_sem = 0.6 → 不满足则惩罚 r_sem = -max(0, τ_sem - ϕ)
3. **简洁控制门**：词数超过 L_max 时线性惩罚 r_len = -η · max(0, |l|/L_max - 1)

最终奖励（Eq. 11）：R = f(l_attack) · Π(1-I_k) + Σ(I_k · r_k · Π(1-I_j))，其中 f(l_attack) = 1 - 𝟙_succ 为攻击成功指示器

### 训练配置

- 优化框架：VERL
- 优化步数：100，组大小 6，batch size 8
- 学习率：1e-6，KL 系数 0.01，熵系数 0.001，温度 ρ=1.0
- 语义阈值 τ_sem=0.6，最大长度 50 词
- 硬件：RTX Pro 6000（训练）+ RTX 5090（评估）


## Experiments

### 评估设置

- **目标 VLA**：π₀（开源版，无额外微调）和 OpenVLA（LIBERO 微调版）
- **主要基准**：LIBERO（语言条件桌面操控），含 Object、Spatial、Goal、Long 等 suite
- **迁移基准**：CALVIN（3D-Diffuser Actor）和 SimplerEnv（OpenVLA-7B，Google Robot 场景）
- **攻击者**：Qwen3-VL-4B-Instruct

### 语言依赖性诊断（Table 1）

用 "no action" 替换任务指令测试 VLA 是否真正依赖语言：
- π₀：成功率大幅下降 → 功能性依赖语言指导
- π₀.5：保持高成功率 → 退化为视觉主导策略，不适合语言鲁棒性研究
- 结论：选择 π₀ 作为主要目标

### LIBERO 主要结果（Table 2）

| 方法 | Succ(↓) | Cos(↑) | LLM(↑) |
|------|---------|--------|--------|
| Original | 93.33% | - | - |
| ERT | 48.57% | 10.56 | 5.83 |
| GRPO | 24.69% | 7.05 | 4.58 |
| DAERT | **5.85%** | **12.23** | **8.48** |

DAERT 同时实现最低成功率和最高多样性。GRPO 模式坍缩严重（Cos=7.05, LLM=4.58）。

### 跨 VLA 迁移（Table 3, LIBERO → OpenVLA）

| 方法 | OpenVLA Succ |
|------|-------------|
| Original | 76.50% |
| ERT | 32.15% |
| GRPO | 17.00% |
| DAERT | **6.25%** |

### 跨域迁移

- **CALVIN + 3D-Diffuser**（Figure 2a）：DAERT 达到 ~60% 攻击性能 + 最高多样性，优于 GRPO（~45%）和 ERT（~45%），即使从 2D 图像策略迁移到 3D 点云策略
- **SimplerEnv + OpenVLA-7B**（Figure 2b）：DAERT 攻击性能 82%，优于 ERT（69.2%）和 GRPO（59.5%）。GRPO 反而不如 ERT，说明缺乏多样性约束时标准 RL 在分布偏移下过拟合

### 定性分析

- ERT 主要做词汇替换（"red milk carton"→"red beverage box"），保留视觉先验，对 Spatial 任务效果有限（78.4% 成功率）
- DAERT 引入组合约束和细粒度行为要求（"orient it correctly"、"without disturbing other objects"），暴露了 VLA 在组合理解和几何推理上的根本脆弱性
- PCA 可视化：GRPO 形成紧密簇（模式坍缩），ERT 占据有限区域，DAERT 展现最宽的语义分布

### 消融实验

- **KL 约束消融**：移除 KL 项后攻击更激进但模式坍缩加剧；KL 正则化有助于多样性但不足以完全解决多模态搜索问题


## Limitations

1. **指令自然度**：DAERT 生成的指令偏向冗长和过度描述（如 "precisely orient it... without disturbing any other objects"），与人类简短自然的指令风格有差距（"Translationese" 现象）
2. **自动化验证局限**：语义保真度依赖 CrossEncoder 阈值，可能无法捕获所有边缘情况；尚未引入 Human-in-the-Loop 评估
3. **任务复杂度**：仅在短时桌面操控任务上验证，未测试长时序、复杂操作（作者在 Conclusion 中指出这一限制）
4. **VLA 覆盖面**：仅测试了 π₀ 和 OpenVLA，未涵盖更新或更多样的 VLA 架构
5. **视觉扰动未结合**：仅测试了纯语言攻击路径，未探索语言+视觉联合扰动
6. **π₀.5 不适用**：语言依赖性诊断发现 π₀.5 几乎不依赖语言指令，说明更先进的 VLA 可能通过视觉主导"绕过"语言脆弱性


## Key Takeaways

1. **VLA 语言脆弱性是真实且严重的**：在不改变视觉输入的前提下，仅通过语义等价的指令改写就能将成功率从 93% 降至 6%，说明当前 VLA 依赖表面语言模式而非真正的组合理解
2. **"no action" 诊断测试实用价值高**：用一个简单的空指令测试就能判断 VLA 是否真正使用语言，这对我们选择和评估 VLA 控制器有直接指导意义
3. **多样性感知 RL 避免模式坍缩**：ROVER 的均匀策略评估思路（用均匀平均替代贪婪最大值）是一个简洁有效的多样性机制，可推广到其他需要多样输出的 RL 场景
4. **级联门控奖励设计**：结构 → 语义 → 长度的级联过滤是保证对抗样本物理可行性的好范式，在 DLO 操控的安全测试中可参考
5. **跨域迁移性揭示共享脆弱性**：不同 VLA 架构共享类似的语言 grounding 薄弱环节，这对我们设计更鲁棒的 VLA 控制系统有警示意义
6. **DLO 操控启示**：如果将 VLA 应用于 DLO 任务，用户可能用多种方式描述同一操控目标（"把线拉直" vs "将缆线整理为直线形态"），这类语言变化很可能导致执行失败

## 相关概念

- [[robotic-manipulation]]
- [[imitation-learning]]
- [[vision-language-model]]
- [[reinforcement-learning]]
- [[robot-learning]]
- [[sim-to-real]]
- [[deformable-linear-object]]

## 相关研究者

- [[tong-baoshun|Tong, Baoshun]]
- [[he-haoran|He, Haoran]]
- [[pan-ling|Pan, Ling]]
- [[lin-liang|Lin, Liang]]
