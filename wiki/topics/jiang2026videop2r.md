---
title: "VIDEOP2R: Video understanding from perception to reasoning"
tags: [imitation, VLM, RL]
created: "2026-05-08"
updated: "2026-05-08"
type: "literature"
status: "done"
summary: "提出 VideoP2R 框架，将视频推理显式分解为感知和推理两个独立过程，通过三步 CoT 管线构建 162K 过程感知数据集，并设计 PA-GRPO 算法为两个过程分别提供奖励信号，在 7 个视频推理/理解基准中的 6 个上达到 SotA。"
authors: "Jiang, Yifan; Wang, Yueying; Zhao, Rui; Parag, Toufiq; Chen, Zhimin et al."
year: "2026"
venue: "arXiv Preprint"
zotero_key: "9DMBD249"
---
## 摘要

Reinforcement fine-tuning (RFT), a two-stage framework consisting of supervised fine-tuning (SFT) and reinforcement learning（强化学习） (RL) has shown promising results on improving reasoning ability of large language models (LLMs). Yet extending RFT to large video language models (LVLMs) remains challenging. We propose VideoP2R, a novel process-aware video RFT framework that enhances video reasoning by modeling perception and reasoning as distinct processes. In the SFT stage, we develop a three-step pipeline to generate VideoP2R-CoT-162K, a high-quality, process-aware chain-of-thought (CoT) dataset for perception and reasoning. In the RL stage, we introduce a novel process-aware group relative policy optimization (PA-GRPO) algorithm that supplies separate rewards for perception and reasoning. Extensive experiments show that VideoP2R achieves state-of-the-art（现有最优方法） (SotA) performance on six out of seven video reasoning and understanding benchmarks. Ablation studies further confirm the effectiveness of our process-aware modeling and PA-GRPO and demonstrate that model's perception output is information-sufficient for downstream reasoning. Our project page is available at https://videop2r.github.io/videop2r/.

## 中文简述

提出基于强化学习的操控方法。

**研究方向**: 模仿学习、视觉-语言模型、强化学习

## 关键贡献

1. **VideoP2R 框架**：首个将视频推理显式建模为感知和推理两个独立过程的 RFT 框架
2. **PA-GRPO 算法**：GRPO 的过程感知变体，为感知和推理 token 段分别计算奖励和归一化 advantage，实现细粒度信用分配
3. **VideoP2R-CoT-162K 数据集**：通过三步管线（生成→验证→感知充分性验证）构建的大规模过程感知 CoT 数据
4. **全面的实验验证**：在 7 个基准上达到 6 个 SotA，消融实验系统验证了每个组件的贡献
## 结构化提取

- Problem: 视频推理中感知和推理过程混合导致信用分配模糊、训练效率低、Think-Answer Mismatch
- Method: VideoP2R 框架——SFT 阶段用三步管线生成过程感知 CoT 数据（VideoP2R-CoT-162K），RL 阶段用 PA-GRPO 为感知和推理分别计算奖励
- Tasks: 视频问答（VQA）——多选、数值、OCR、自由形式、回归五类任务
- Sensors: 视频输入（训练时 16 frames @ 128×28×28，推理时 32 frames @ 256×28×28）
- Robot Setup: 无机器人实验；纯视频理解/推理任务
- Metrics: 各基准的准确率/ACC/MRA；ROUGE、WER、exact match 用于 CoT 验证；Think-Answer Mismatch rate 用于分析
- Limitations: 缺乏领域知识导致 MMVU 下降；固定长度奖励在长描述场景反效果；依赖 Claude 3.7 作 judge；仅验证视频 QA
- Evidence Notes: 完整消融实验（Tab.2）证明过程感知建模和 PA-GRPO 各组件贡献；感知有效性实验证明 VideoP2R 感知文本可替代视频输入；PA-GRPO 相比 GRPO 减少 advantage collapse 和 think-answer mismatch
## 本地引用关系

-
## 证据元数据

- Fulltext Quality: fulltext (via arXiv HTML, 包含正文全部章节和补充材料 Sec.7-8)
- Evidence Coverage: high（方法论、实验、消融、补充材料均已覆盖；补充材料 Sec.9-14 仅读取了目录和 Sec.7-8 细节）
- Confidence: high
- Summary: 提出 VideoP2R 框架，将视频推理显式分解为感知和推理两个独立过程，通过三步 CoT 管线构建 162K 过程感知数据集，并设计 PA-GRPO 算法为两个过程分别提供奖励信号，在 7 个视频推理/理解基准中的 6 个上达到 SotA。


## Problem

现有视频强化微调（RFT）框架将视觉推理中的 **感知（perception）** 和 **推理（reasoning）** 混合为单一过程，仅分配一个最终奖励，导致：

1. **信用分配模糊**：感知错误导致的推理错误无法被区分归因
2. **训练效率低下**：当推理奖励饱和时出现 advantage collapse，梯度信号消失
3. **Think-Answer Mismatch**：推理轨迹与最终答案不一致，但单一奖励无法惩罚不忠实的推理链


## Method

### 整体架构

VideoP2R 采用标准 RFT 两阶段框架：SFT → RL，但核心创新在于将视频推理建模为两个独立过程。

### CoT 模板设计

```
⟨observation⟩ ... ⟨/observation⟩  ← 感知过程：提取视觉证据
⟨think⟩ ... ⟨/think⟩              ← 推理过程：基于证据推理
⟨answer⟩ ... ⟨/answer⟩            ← 最终答案
```

### SFT 阶段：三步 CoT 生成管线

1. **过程感知 CoT 生成**：使用 Qwen2.5-VL-72B-Instruct 为 260K VQA 样本生成初始 CoT 轨迹
2. **CoT 验证**：使用任务特定指标（exact match、ROUGE、WER 等）过滤低质量样本（阈值 0.6）
3. **感知充分性验证**：将 ⟨observation⟩ 段 + 问题 + 答案输入 Claude 3.7 Sonnet，判断感知证据是否足以支撑正确推理

最终从 260K 样本中得到 **162K** 高质量过程感知 CoT 数据。

### RL 阶段：PA-GRPO

核心改进——将 GRPO 的单一奖励分解为独立的过程奖励：

- **感知准确率奖励 R_acc,P**：Claude 3.7 Sonnet 作为 LLM-Judge，判断 ⟨observation⟩ 是否包含充分视觉证据（二值）
- **推理准确率奖励 R_acc,R**：任务特定评估指标（exact match / ROUGE / WER / 相对误差）
- **格式奖励 R_form**：正则匹配检查模板合规性（二值）
- **长度奖励 R_len**：当准确率和格式奖励均非零时，根据段长度给予奖励（感知段 128-320 tokens，推理段 320-512 tokens）

每个过程独立归一化 advantage：
$$A_{i,k} = \frac{R_{i,k} - \text{mean}(\{R_{j,k}\})}{\text{std}(\{R_{j,k}\})}, \quad k \in \{P, R\}$$

仅将对应过程的 advantage 赋予该过程的 token 段。

### 训练配置

- 基础模型：Qwen2.5-VL-7B-Instruct
- 硬件：8× NVIDIA A100
- SFT：batch size 8，gradient accumulation 2，1 epoch
- RL：batch size 56（8 rollouts per sample），1000 steps
- 训练帧数：16 frames, 128×28×28
- 推理帧数：32 frames, 256×28×28


## Experiments

### 基准

7 个视频推理/理解基准：
- **视频推理**：VSI-Bench（空间推理）、VideoMMMU（专业知识）、MMVU（多学科）、VCR-Bench（链式推理）
- **视频理解**：MVBench（综合）、TempCompass（时序）、VideoMME（多模态）

### 主实验结果（Tab.1）

| 模型 | VSI. | VideoMMMU | MMVU | VCR. | MV. | TempCom. | VideoMME | Avg |
|------|------|-----------|------|------|-----|----------|----------|-----|
| Qwen2.5-VL-7B (base) | 30.1 | 48.1 | 60.0 | 44.3 | 59.0 | 72.6 | 56.6 | 52.9 |
| Video-R1 | 35.8 | 52.3 | 63.8 | 49.0 | 63.9 | 73.2 | 59.3 | 56.8 |
| VideoRFT | 36.8 | 51.1 | 68.5 | 49.6 | 62.1 | 73.7 | 59.8 | 57.4 |
| **VideoP2R (Ours)** | **36.8** | **55.0** | 65.4 | **51.0** | **68.1** | **74.5** | **60.0** | **58.7** |

- 6/7 基准 SotA（MMVU 上 VideoRFT 更优）
- 相比 base 平均提升 +5.8%
- 相比前 SotA 平均提升 +1.3%

### 消融实验（Tab.2）

**两阶段训练**：
- SFT-only: +2.7%（55.6%）
- RL-only: +3.1%（56.0%）
- 两阶段组合: +5.8%（58.7%）→ 证明两阶段互补

**过程感知建模**：
- 过程感知 SFT vs 过程不可知 SFT: +2.1%
- 过程感知 RL (PA-GRPO) vs 过程不可知 RL (GRPO): +2.3%

**奖励设计**：
- 移除推理奖励 R_R: -3.4%（最关键）
- 移除感知奖励 R_P: -2.3%（第二重要）
- 移除长度奖励 R_L: -1.0%
- 移除分离赋权（将两个奖励赋给所有 token）: -1.3%

### 感知有效性实验（Sec.5.3）

- 仅用 VideoP2R 的感知文本（无视频输入）+ 问题 → 55.5%，超过直接用视频输入的 52.9%
- VideoP2R 的感知描述比 Qwen 原始感知描述在两种模态下均更优

### PA-GRPO vs GRPO 优势分析（Sec.5.4）

1. **减少 Advantage Collapse**：PA-GRPO 在训练过程中始终比 GRPO 有更少的 advantage collapse 样本
2. **缓解 Think-Answer Mismatch**：VideoP2R 的 mismatch rate 显著低于 Video-R1（≥16%）和 VideoRFT（≥16%）


## Limitations

1. **领域知识缺失**：在 MMVU 上表现不佳，主要因为训练数据缺乏特定领域知识（如化学摩尔体积等）
2. **长度奖励的反效果**：VSI-Bench 的空间推理问题需要长而详细的感知描述，固定的长度奖励反而有害；作者提出未来采用动态长度奖励
3. **外部模型依赖**：感知奖励依赖 Claude 3.7 Sonnet 作为 judge，引入外部 API 依赖（虽然消融显示对 judge 模型鲁棒）
4. **仅验证视频 QA 场景**：未扩展到视频生成、视频摘要等其他视频任务
5. **训练数据覆盖**：仅使用 Video-R1 的 260K VQA 数据源，数据多样性有限


## Key Takeaways

1. **过程分解的思想可迁移到机器人控制**：将"感知 DLO 状态"和"推理操控动作"显式分离，并分别设计奖励，可能改善 Sim-to-Real 和 DLO 操控中的信用分配问题
2. **PA-GRPO 的独立奖励归一化机制值得借鉴**：在机器人 RL 中，视觉感知质量和动作策略质量通常具有不同的奖励尺度，分别归一化可避免一个过程主导优化
3. **LLM-as-Judge 作为感知质量评估器**：可用于评估 VLM 对机器人场景的感知是否充分
4. **三步 CoT 管线的质量控制**：生成→验证→跨模态验证的流程可用于生成机器人操控的过程感知训练数据

## 相关概念

- [[imitation-learning]]
- [[vision-language-model]]
- [[reinforcement-learning]]
- [[deformable-linear-object]]
- [[planning]]

## 相关研究者

- [[jiang-yifan|Jiang, Yifan]]
- [[wang-yueying|Wang, Yueying]]
- [[zhao-rui|Zhao, Rui]]
