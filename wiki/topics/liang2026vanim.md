---
title: "VAnim: Rendering-aware sparse state modeling for structure-preserving vector animation"
tags: [imitation, VLM, RL, planning]
created: "2026-05-10"
updated: "2026-05-10"
type: "literature"
status: "done"
summary: "VAnim 提出基于 Sparse State Update 的 LLM 框架实现文本驱动的 SVG 动画生成，通过 Identification-First Motion Planning 将语义指令锚定到 SVG DOM 节点，再用 GRPO 强化学习对齐渲染视觉反馈，在自建 SVGAnim-134k 基准上语义对齐和结构保真度全面超越 GPT-5.2、Gemini 3 Pro 和 LiveSketch。"
authors: "Liang, Guotao; Wang, Zhangcheng; Wang, Chuang; Hu, Juncheng; Zhou, Haitao et al."
year: "2026"
venue: "arXiv Preprint"
zotero_key: "I7DSXJ7W"
---
## 摘要

Scalable Vector Graphics (SVG) animation generation is pivotal for professional design due to their structural editability and resolution independence. However, this task remains challenging as it requires bridging discrete code representations with continuous visual dynamics. Existing optimization-based methods often destroy topological consistency, while general-purpose LLMs rely on rigid CSS/SMIL transformations, failing to model geometry-level non-rigid deformations. To address these limitations, we present VAnim, the first LLM-based framework for open-domain text-to-SVG animation. We reconceptualize animation not as sequence generation, but as Sparse State Updates (SSU) on a persistent SVG DOM tree. This paradigm compresses sequence length by over 9.8x while preserving the SVG DOM structure and non-participating elements by construction. To enable precise control, we propose an Identification-First Motion Planning mechanism that grounds textual instructions in explicit visual entities. Furthermore, to overcome the non-differentiable nature of SVG rendering, we employ Rendering-Aware Reinforcement Learning（强化学习） via Group Relative Policy Optimization (GRPO). By leveraging a hybrid reward（奖励） from a state-of-the-art（现有最优方法） video perception encoder, we align discrete code updates with high-fidelity visual feedback. We also introduce SVGAnim-134k, the first benchmark for vector animation. Extensive experiments demonstrate that VAnim significantly outperforms state-of-the-art（现有最优方法） baselines in semantic alignment and structural validity, with additional appendix metrics further validating motion quality and identity preservation.

## 中文简述

提出基于强化学习的操控方法。

**研究方向**: 模仿学习、视觉-语言模型、强化学习、运动规划

## 关键贡献

1. **SVGAnim-134k 数据集**：首个大规模矢量动画数据集（134k 样本），包含专业设计的 UI 图标、加载指示器和叙事插画，通过拓扑规范化管线确保 SVG DOM 结构一致性。
2. **Sparse State Update (SSU) 范式**：将动画建模为持久 SVG DOM 树上的稀疏属性差分更新，而非逐帧完整生成，序列长度压缩 9.8×（86k → 9.2k tokens）。
3. **Identification-First Motion Planning**：两阶段推理——先通过 Structure-Bound CoT 将语义实体锚定到 SVG ID 并规划运动，再执行稀疏更新，从结构上保证非参与元素不变。
4. **Rendering-Aware RL (GRPO)**：通过 PE-Core 视频感知编码器提供混合奖励（语义对齐 + 格式有效性），弥合离散代码生成与连续视觉感知的鸿沟。
## 结构化提取

- Problem: 文本驱动的 SVG 矢量动画自动生成，需同时保证语义对齐和拓扑结构一致性
- Method: 基于 Qwen3-VL-8B 的两阶段框架——SFT + GRPO，核心为 Sparse State Update 和 Identification-First Motion Planning
- Tasks: Text-to-SVG Animation（开放域文本到矢量动画生成）
- Sensors: SVG 代码输入 + 渲染光栅图像（视觉编码器 EV）
- Robot Setup: 不适用（非机器人论文）；计算环境：8× NVIDIA H100 GPU
- Metrics: Semantic Alignment (PE-Core cosine sim), Success Rate, InternVideo2, Mean Flow Magnitude, Flow-tLPIPS, SSIM, User Study (5-point Likert)
- Limitations: 固定 DOM 拓扑假设；Lottie 域特定；RL 推理开销大；不支持交互行为
- Evidence Notes:

  - Table 1 主实验：VAnim GRPO 在 Semantic Alignment (0.281) 和 Success Rate (100%) 上全面领先
  - Table S1 扩展评估：在独立指标 InternVideo2 (0.202)、运动幅度 (1.711)、时序平滑 (0.0117) 上均为最优
  - Table 2 消融：CoT 移除影响最大 (-0.026)，RL 移除次之 (-0.013)
  - Table S2 用户研究：VAnim 在 Visual Integrity (4.62) 上大幅领先第二名 Gemini (3.42)
  - Table S1 附录消融：No SSU 基线成功率仅 62.3%，验证稀疏表示的必要性
  - GRPO Group Size 扫描 (G=4/8/16)：更大 G 提升语义对齐但略降 SSIM
## 本地引用关系

-
## 证据元数据

- Fulltext Quality: fulltext
- Evidence Coverage: complete（含正文12页 + 附录18页，完整实验表格、消融、用户研究）
- Confidence: high
- Summary: VAnim 提出基于 Sparse State Update 的 LLM 框架实现文本驱动的 SVG 动画生成，通过 Identification-First Motion Planning 将语义指令锚定到 SVG DOM 节点，再用 GRPO 强化学习对齐渲染视觉反馈，在自建 SVGAnim-134k 基准上语义对齐和结构保真度全面超越 GPT-5.2、Gemini 3 Pro 和 LiveSketch。


## Problem

如何从自然语言文本指令自动生成结构保真的 SVG 矢量动画？现有方法存在两个核心障碍：
1. **上下文爆炸与身份漂移**：逐帧自回归生成完整 SVG 代码导致 token 序列过长（~86k tokens/24帧），且重生成静态属性引入随机不一致，导致对象身份闪烁或坍塌。
2. **非刚性变形的表达瓶颈**：现有 LLM（GPT-5.2、Gemini 3 Pro）偏向 CSS/SMIL 仿射变换（平移、旋转、缩放），无法建模路径级非刚性变形（如弯曲、形变）；优化方法（LiveSketch）基于可微光栅化，拓扑不稳定且延迟高。


## Method

### 核心架构
基于 Qwen3-VL-8B-Thinking 多模态 LLM，双阶段训练：

**Stage I: 结构化 SFT**
- 在 SVGAnim-SFT（123k 样本）上进行全参数微调
- 学习 SVG 语法、DOM 层级感知、Structure-Bound CoT 格式和 YAML 差分预测
- 最大序列长度 25k tokens，DeepSpeed ZeRO-3，8×H100，2 epochs

**Stage II: Rendering-Aware RL (GRPO)**
- 在 SVGAnim-RL（10k 高复杂度样本）上使用 GRPO 优化
- 每个输入采样 G=8 个候选输出，渲染为视频后用混合奖励评估
- 混合奖励 = λ_align · R_align + λ_fmt · R_fmt（均等权重 1.0）
  - R_align：PE-Core 视频编码器余弦相似度（文本指令 vs 渲染视频）
  - R_fmt：二值奖励（语法可解析 + 帧数匹配 + ID 有效）

### 推理流程（粗到细）
1. **Director 阶段**：模型接收 (I₀, S₀, P)，生成 Structure-Bound CoT C——先识别实体（"蓝色圆对应 ID 05"），再规划时序逻辑
2. **Animator 阶段**：基于 C 生成稀疏状态更新序列 D，仅修改发生变化的属性差分

### 数据管线
1. 从 Flaticon 获取 Lottie 文件，渲染为 ID-anchored SVG DOM 树
2. 提取稀疏状态更新（仅保留帧间变化的属性差分）
3. 用 Doubao-Seed-1.6 VLM 生成双流标注：用户指令 P + Structure-Bound CoT C
4. 严格 ID 一致性过滤（引用不存在 ID 的样本直接丢弃）


## Experiments

### 数据集
- SVGAnim-134k：123k SFT + 10k RL + 1k Test
- 来源：Flaticon 专业设计 Lottie 动画
- 覆盖 UI 组件、有机非刚性实体、复杂拓扑与分组

### 主实验（Table 1, SVGAnim-Test）
| 方法 | Semantic Alignment ↑ | Success Rate ↑ |
|------|---------------------|----------------|
| LiveSketch | 0.158 | 100.0% |
| GPT-5.2 | 0.234 | 88.5% |
| Gemini 3 Pro | 0.243 | 86.2% |
| VAnim (SFT-only) | 0.268 | 95.2% |
| **VAnim (GRPO)** | **0.281** | **100.0%** |

### 扩展评估（Table S1, 独立指标）
| 方法 | InternVideo2 ↑ | Mean Flow Mag | Flow-tLPIPS ↓ | SSIM ↑ | SR ↑ |
|------|---------------|---------------|---------------|--------|------|
| AniClipart | 0.092 | 0.927 | 0.0376 | 0.9278 | 100% |
| FlipSketch | 0.137 | 1.696 | 0.1575 | 0.6786 | 100% |
| GPT-5.2 | 0.180 | 0.954 | 0.0148 | 0.9505 | 88.5% |
| Gemini 3 Pro | 0.182 | 0.804 | 0.0136 | 0.9634 | 86.2% |
| LiveSketch | 0.107 | 0.801 | 0.0612 | 0.9000 | 100% |
| **VAnim** | **0.202** | **1.711** | **0.0117** | **0.9719** | **100%** |

### 消融实验（Table 2）
| 变体 | Semantic Alignment | Success Rate |
|------|-------------------|--------------|
| Full VAnim | 0.281 | 100.0% |
| w/o Rendering-Aware RL | 0.268 (-0.013) | 95.2% (-4.8%) |
| w/o Structure-Bound CoT | 0.255 (-0.026) | 98.6% (-1.4%) |

### 附录消融（Table S1）
- No SSU（逐帧生成）：Success Rate 降至 62.3%，时序平滑性显著恶化（Flow-tLPIPS 0.2070 vs 0.0117）
- No Input Image：SSIM 从 0.9719 降至 0.9245
- No R_align 奖励：语义得分下降，运动幅度减小
- No R_fmt 奖励：可执行率降至 96.6%
- GRPO Group Size G=16 时语义对齐最高（0.207）但 SSIM 略降

### 用户研究（Table S2, 15人, 5点 Likert）
| 方法 | Visual Integrity ↑ | Motion Smoothness ↑ | Instruction Following ↑ |
|------|-------------------|--------------------|------------------------|
| LiveSketch | 2.15 | 2.43 | 2.12 |
| GPT-5.2 | 3.35 | 3.76 | 3.55 |
| Gemini 3 Pro | 3.42 | 3.85 | 3.68 |
| **VAnim** | **4.62** | **4.48** | **4.55** |


## Limitations

1. **DOM 结构固定**：假设 SVG DOM 树结构持久不变，不支持动画过程中节点的增删或动态拓扑变化。
2. **域特异性**：训练和评估数据均来自 Lottie 派生 SVG，对手绘或设计工具导出的 SVG 泛化能力未知。
3. **计算开销**：Rendering-Aware RL 阶段需对每个 prompt 采样并渲染多个候选动画，推理成本较高。
4. **交互行为缺失**：当前仅支持视觉动画生成，未涉及交互行为（如 JavaScript 触发器）和长叙事场景。


## Key Takeaways

### 与机器人操控的关联思考
1. **稀疏状态更新思想可迁移到机器人控制**：VAnim 将动画建模为 DOM 树上的稀疏属性差分，类似思想可应用于机器人的关节空间——只更新与当前任务相关的关节自由度，保持其余关节不变，减少维度爆炸。
2. **Identification-First 规划与视觉-语言操控的对偶性**：VAnim 先将语义实体锚定到 SVG ID，再规划运动；机器人操控中先将语言指令锚定到场景中的具体物体（grasping target），再规划动作，两者推理结构高度相似。
3. **GRPO 弥合不可微渲染的方法论启示**：SVG 渲染不可微，VAnim 用视觉编码器的反馈做 RL 奖励；机器人仿真中的接触动力学也常不可微，类似方法可用于从视觉反馈学习接触丰富操控。
4. **结构保真约束在 Sim-to-Real 中的类比**：VAnim 通过 SSU 约束输出空间为有效属性差分，确保拓扑一致性；Sim-to-Real 中对动作空间施加结构约束（如运动可行性、碰撞避免）同样关键。

### 核心技术洞察
- SFT 模型存在"保守运动偏差"（conservative motion bias），视觉奖励信号是克服此问题的关键。
- Structure-Bound CoT 的消融影响最大（-0.026），说明显式实体-标识符绑定是结构完整性的前提。
- 数据集中 30% 的更新涉及路径级 d 属性操作（非刚性变形），这远超简单仿射变换的范畴。

## 相关概念

- [[imitation-learning]]
- [[vision-language-model]]
- [[reinforcement-learning]]
- [[planning]]
- [[grasping]]

## 相关研究者

- [[liang|Liang, Guotao]]
