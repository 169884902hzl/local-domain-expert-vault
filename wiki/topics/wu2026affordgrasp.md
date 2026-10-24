---
title: "AffordGrasp: Cross-modal diffusion for affordance-aware grasp synthesis"
tags: [diffusion, robot-learning, grasping]
created: "2026-05-06"
updated: "2026-05-06"
type: "literature"
status: "done"
summary: "利用可供性作为跨模态中间表示，结合双条件扩散模型和分布调整模块，实现语言指令引导的人手抓取姿态合成，在四个基准数据集上达到 SOTA。"
authors: "Wu, Xiaofei; Zhang, Yi; Liu, Yumeng; Ma, Yuexin; Shi, Yujiao et al."
year: "2026"
venue: "arXiv Preprint"
zotero_key: "D73AVAKA"
---
## 摘要

Generating human grasping（抓取） poses that accurately reflect both object geometry and user-specified interaction semantics is essential for natural hand-object interactions in AR/VR and embodied AI. However, existing semantic grasping（抓取） approaches struggle with the large modality gap between 3D object representations and textual instructions, and often lack explicit spatial or semantic constraints, leading to physically invalid or semantically inconsistent grasps. In this work, we present AffordGrasp, a diffusion（扩散）-based framework that produces physically stable and semantically faithful human grasps with high precision. We first introduce a scalable annotation pipeline that automatically enriches hand-object interaction datasets with fine-grained structured language labels capturing interaction intent. Building upon these annotations, AffordGrasp integrates an affordance（可供性）-aware latent representation of hand poses with a dual-conditioning diffusion（扩散） process, enabling the model to jointly reason over object geometry, spatial affordances, and instruction semantics. A distribution adjustment module further enforces physical contact consistency and semantic alignment. We evaluate AffordGrasp across four instruction-augmented benchmarks derived from HO-3D, OakInk, GRAB, and AffordPose, and observe substantial improvements over state-of-the-art（现有最优方法） methods in grasp quality, semantic accuracy, and diversity.

## 中文简述

提出基于扩散模型的抓取方法，具有接触丰富特点。

**研究方向**: 扩散模型、机器人学习、抓取

## 关键贡献

1. **AffordGrasp 框架**：基于 diffusion 的语义抓取生成框架，无需 test-time adaptation 即可生成物理稳定且语义一致的抓取姿态。
2. **Affordance 作为跨模态桥梁**：提出利用物体可供性（affordance）作为互补引导，弥合语言语义与几何表示之间的鸿沟。
3. **Distribution Adjustment Module (DAM)**：后采样阶段的轻量级精炼模块，通过双残差机制和多注意力头在保持扩散采样稳定性的同时强制物理和语义约束。
4. **全面 SOTA**：在 OakInk、GRAB、HO-3D、AffordPose 四个基准上全面超越现有方法。
## 结构化提取

- Problem: 语义驱动的手-物交互抓取生成，需同时满足物理合理性和语言语义一致性
- Method: Affordance Generator (LASO) + Cross-Modal Latent Diffusion (RoBERTa + PointNet + VAE + U-Net) + Distribution Adjustment Module (双残差 MHA+MLP)
- Tasks: 语义引导的人手抓取姿态合成（MANO 参数预测）
- Sensors: 无传感器（纯几何输入：物体点云 + 文本指令）
- Robot Setup: 无机器人训练（ShadowHand 仅用于下游仿真验证）
- Metrics: 穿透体积、接触比率、重力位移、聚类熵、平均簇大小、语义准确度 (ACC)
- Limitations: 未建模重力/摩擦等物理先验；依赖 AffordPose 冷启动标注；失败案例存在
- Evidence Notes:

  - 完整的 arXiv HTML 全文已获取，涵盖正文和附录
  - 表格数值因 HTML 格式限制部分缺失，但消融结论和定性对比完整
  - 仿真和真实机器人实验结果已记录
## 本地引用关系

-
## 证据元数据

- Fulltext Quality: fulltext (arXiv HTML)
- Evidence Coverage: high (正文 + 附录完整获取；表格数值因 HTML 格式化问题部分缺失，但定性结论和消融分析完整)
- Confidence: high
- Summary: 利用可供性作为跨模态中间表示，结合双条件扩散模型和分布调整模块，实现语言指令引导的人手抓取姿态合成，在四个基准数据集上达到 SOTA。


## Problem

现有语义抓取生成方法存在两个核心问题：
1. **模态鸿沟**：3D 物体几何表示与文本指令之间存在巨大模态差距，直接融合难以实现细粒度的几何-语义对齐（如区分"抓把手"和"握杯沿"）。
2. **约束缺失**：当前 diffusion pipeline 缺乏显式的空间约束和指令驱动约束，导致生成的抓取在物理上不合理或语义不一致。

此外，基于 VLM 的多轮问答标注管线存在不一致性和可控性不足的问题。


## Method

AffordGrasp 由三个核心组件构成：

### 3.1 Affordance Generator
- 输入：物体点云 $P_g$ + 文本指令 $I$
- 输出：点级可供性概率图 $P_a$，高亮与指令语义相关的物体区域
- 架构：基于 LASO 网络
- 训练策略：
  - 在 AffordPose 上冷启动训练
  - 自训练循环为 OakInk/GRAB 生成伪标签（扩大物体几何多样性）
  - 使用 Focal Loss + Dice Loss 处理类别不平衡

### 3.2 Cross-Modal Latent Diffusion Model
- 三元条件 $\mathcal{C} = \{I, P_g, P_a\}$
- 编码器：RoBERTa（文本）、两个独立 PointNet（物体点云 + affordance 点云）
- 手部表示：预训练 Autoencoder 将 MANO 手部顶点编码到紧凑潜空间 $h_z$
- 扩散过程：标准 Latent Diffusion，U-Net 预测噪声
- 解码：潜空间 → MANO 参数（61维）→ 手部网格

### 3.3 Distribution Adjustment Module (DAM)
- 轻量级单次前向精炼，在 DDIM 采样后应用
- 从 diffusion 噪声预测近似恢复潜空间表示：$\hat{h}_z = \frac{1}{\sqrt{\alpha_t}}(z^t - \sqrt{1-\alpha_t}\epsilon_\theta(z^t, f, t))$
- 空间融合：$f_{spatial} = \text{Norm}(f_{pg} + f_{pa}) + \hat{h}_z$
- 双残差机制：
  1. MHA 后保留指令语义：$f_{align} = \text{Attention}(f_I, f_{spatial}, f_{spatial}) + f_I$
  2. MLP 后保留手部表示：$\tilde{h}_z = \text{Norm}(\text{MLP}(f_{align}) + \hat{h}_z)$
- 训练时冻结 diffusion 模型，仅训练 DAM
- 损失函数：重建损失（MANO 参数 MSE + Chamfer Distance）+ 物理约束（consistency + contact map + penetration）

### 3.4 数据标注管线
- 第一阶段：语义可供性预测（PointBERT 分类器，10 类 affordance）
- 自训练扩展：高置信度伪标签 → 人工验证 → 迭代精炼
- 第二阶段：LLM（Qwen2）基于 affordance 标签和物体类别生成语言指令

### 3.5 推理
- DDIM 采样 → DAM 精炼 → Decoder + MANO Layer → 手部网格
- 无需 test-time adaptation


## Experiments

### 数据集
| 数据集 | 用途 | 规模 |
|--------|------|------|
| GRAB | in-domain 训练+测试 | 51 物体, 10 受试者 |
| OakInk | in-domain 训练+测试 | 1700 物体, 12 受试者 |
| HO-3D | out-of-domain (zero-shot) | - |
| AffordPose | out-of-domain (zero-shot) | 10 类 affordance 标注 |

### 评估指标
- **物理合理性**：穿透体积（1mm³ 体素化）、接触比率
- **抓取稳定性**：仿真中物体质心重力位移
- **多样性**：K-means (k=20) 聚类熵值、平均簇大小
- **语义准确度 (ACC)**：10 类 affordance 分类器准确率

### 主要结果（定性）
- **In-domain (OakInk + GRAB)**：所有指标全面领先 FastGrasp、D-VQVAE、ControlNet、SemGrasp、Text2Grasp
- **Out-of-domain (HO-3D + AffordPose)**：语义准确度和物理泛化能力显著优于基线，物体穿透明显减少
- **DAM vs ControlNet**：DAM 更轻量且效果更优

### 消融实验
- **去掉 Affordance**：位移距离略优但穿透体积增大，说明 affordance 帮助捕捉空间细节
- **去掉 DAM**：簇更大（多样性高但约束弱），DAM 使输出分布更集中、语义一致
- **DAM 注意力头数量**：1/2/4 头均有实验（Tab. 9）

### 下游应用
- RaiSim 物理仿真：通过 D-Grasp 和 CrossDex 框架执行动态抓取轨迹
- 成功率与 CrossDex 相当，MPJDR=0.161, FOL=0.235
- 真实机器人：ShadowHand 平台上验证，不同指令产生不同执行结果

### 具体数值注意
表格具体数值因 HTML 提取格式限制未完整保留（Tab. 1-3）。论文声称在所有指标上全面超越 SOTA。


## Limitations

1. **物理先验缺失**：未显式建模重力和摩擦等物理先验，某些真实世界效果无法充分反映
2. **数据依赖**：数据标注管线依赖 AffordPose 数据集的 affordance 标注作为冷启动
3. **MANO 限制**：基于 MANO 参数化，无法处理非标准手型或工具使用场景
4. **跨物体泛化**：附录 Fig. 16 展示了失败案例


## Key Takeaways

1. **Affordance 作为中间表示**：将可供性作为跨模态融合的中间桥梁是有效策略，可启发 DLO 操控中的"可操作区域识别"。
2. **后采样精炼优于在线优化**：DAM 的单次后处理比 TTA 或梯度优化更高效，推理开销极小，这对实时操控系统有实际价值。
3. **自训练标注管线**：从有限标注出发通过自训练扩展伪标签的方法具有可扩展性，适用于 DLO 数据稀缺场景。
4. **双残差设计**：MHA + MLP 的双残差连接有效平衡了语义保持和空间精炼，可作为跨模态融合的设计参考。
5. **与 DLO 操控的关联**：affordance-aware 的空间表示思路可用于 DLO 的抓取点选择和操控策略规划，尤其是结合语言指令确定操控方式（如"打结"vs"解开"）。
6. **从人手到机器手**：论文展示了从 MANO 人手到 ShadowHand 的映射（通过 CrossDex），这种 sim-to-real 路径对 DLO 机器人操控有参考价值。

## 相关概念

- [[diffusion-model]]
- [[robot-learning]]
- [[grasping]]
- [[vision-language-model]]
- [[sim-to-real]]
- [[deformable-linear-object]]

## 相关研究者

- [[wu-xiaofei|Wu, Xiaofei]]
