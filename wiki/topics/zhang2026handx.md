---
title: "HandX: Scaling bimanual motion and interaction generation"
tags: [imitation, VLM, RL, diffusion, bimanual]
created: "2026-05-06"
updated: "2026-05-06"
type: "literature"
status: "done"
summary: "构建 HandX 大规模双臂手部运动数据集（54.2h / 485.7K 文本对），提出运动学特征解耦+LLM 推理的自动标注策略，并基准测试扩散模型与自回归模型的 scaling 趋势。"
authors: "Zhang, Zimu; Zhang, Yucheng; Xu, Xiyan; Wang, Ziyin; Xu, Sirui et al."
year: "2026"
venue: "arXiv Preprint"
zotero_key: "CHS5F3S3"
---
## 摘要

Synthesizing human motion has advanced rapidly, yet realistic hand motion and bimanual（双臂） interaction remain underexplored. Whole-body models often miss the fine-grained cues that drive dexterous（灵巧） behavior, finger articulation, contact timing, and inter-hand coordination, and existing resources lack high-fidelity bimanual（双臂） sequences that capture nuanced finger dynamics and collaboration. To fill this gap, we present HandX, a unified foundation spanning data, annotation, and evaluation. We consolidate and filter existing datasets for quality, and collect a new motion-capture dataset targeting underrepresented bimanual（双臂） interactions with detailed finger dynamics. For scalable annotation, we introduce a decoupled strategy that extracts representative motion features, e.g., contact events and finger flexion, and then leverages reasoning from large language models to produce fine-grained, semantically rich descriptions aligned with these features. Building on the resulting data and annotations, we benchmark diffusion（扩散） and autoregressive models with versatile conditioning modes. Experiments demonstrate high-quality dexterous（灵巧） motion generation, supported by our newly proposed hand-focused metrics. We further observe clear scaling trends: larger models trained on larger, higher-quality datasets produce more semantically coherent bimanual（双臂） motion. Our dataset is released to support future research.

## 中文简述

提出基于扩散模型的双臂方法，具有接触丰富特点。

**研究方向**: 模仿学习、视觉-语言模型、强化学习、扩散模型、双臂操控

## 关键贡献

1. **HandX 数据集**：整合 5 个公开数据集 + 新采集动捕数据，总计 54.2 小时、590 万帧、485.7K 细粒度文本描述，是迄今最大规模的双臂手部运动-文本数据集
2. **解耦式自动标注框架**：先提取 6 类运动学特征（手指弯曲、手指间距、指-指距离、掌-掌关系、指-掌距离、腕轨迹）转为结构化 JSON，再用 LLM 生成 5 级粒度描述，实现可扩展高质量标注
3. **扩散模型与自回归模型双基准**：在统一数据上基准测试两种生成范式，支持多种条件控制（text-to-motion、motion in-betweening、keyframe generation、wrist trajectory、hand-reaction synthesis、long-horizon）
4. **Scaling trend 分析**：揭示了数据量与模型容量的正 scaling 趋势，R-Precision 与 FLOPs 呈近似 log-linear 关系（相关系数 0.96）
5. **新接触指标**：提出 Contact Precision / Recall / F1，细分为 intra-hand 和 inter-hand 接触评估
## 结构化提取

- **Problem**: 双臂手部运动生成缺乏大规模高质量数据、细粒度标注和专门评估指标
- **Method**: 数据整合+动捕采集构建 HandX 数据集；解耦式运动学特征提取+LLM 推理自动标注；扩散模型和 FSQ 自回归模型双基准
- **Tasks**: Text-to-motion, Motion in-betweening, Keyframe generation, Wrist trajectory generation, Hand-reaction synthesis, Long-horizon generation
- **Sensors**: 36 摄像头 OptiTrack 光学动捕系统，每只手 25 个 3mm 红外反光标记点
- **Robot Setup**: 类人机器人平台配备灵巧手（demo 展示，非实验主体）
- **Metrics**: R-Precision (Top 1/2/3), FID, Diversity, Multimodal Distance, Contact Precision/Recall/F1 (intra-hand + inter-hand)
- **Limitations**: 数据集有限多样性、聚合数据固有噪声、未涉及手-物交互生成、模型 scaling 存在饱和点
- **Evidence Notes**: 扩散模型 12 层 + 全量数据为最优配置（R-Prec Top1=0.427, Intra-hand CF1=0.641）；R-Precision 与 FLOPs 呈 log-linear 关系（R=0.96）；用户研究确认 scaling 趋势的感知有效性
## 本地引用关系

-
## 证据元数据

- Fulltext Quality: fulltext
- Evidence Coverage: high（主体 + 补充材料全部读取）
- Confidence: high
- Summary: 构建 HandX 大规模双臂手部运动数据集（54.2h / 485.7K 文本对），提出运动学特征解耦+LLM 推理的自动标注策略，并基准测试扩散模型与自回归模型的 scaling 趋势。


## Problem

现有双臂手部运动生成面临三大瓶颈：
1. **数据稀缺**：现有数据集要么缺乏手部细节（如 Motion-X、InterAct），要么仅关注单手-物体交互（如 ARCTIC、H2O），缺少高保真双臂接触丰富动作序列
2. **标注粗粒度**：大多数数据集只有 coarse 或 action-level 标注，无法支持从细粒度自然语言生成运动
3. **评估缺失**：缺少专门评估手部接触保真度和双臂协调性的度量


## Method

### 数据构建
- **公开数据整合**：整合 GigaHands、HOT3D、ARCTIC、H2O、HoloAssist，统一为 21 关节骨骼拓扑，标准化全局坐标系
- **新动捕采集**：使用 36 摄像头 OptiTrack 系统，每只手 25 个反光标记点，重建包含 25 标记点的手部骨骼，通过腕关节优化（最小化 MCP-腕骨长度误差）处理软组织伪影
- **强度感知过滤**：基于关节角速度的 action intensity metric，过滤静态/低活跃片段（阈值 τ_hand=25, τ_avg=30），只保留双臂均有有意义运动的 60 帧（2s@30FPS）clips

### 自动标注（Section 4）
1. **运动学特征提取**：
   - 6 类描述子 → 事件分割（状态变化 + 稳态区间）
   - 状态量化区间定义：如 Finger-Finger Distance < 2cm = "Contact", Finger Flexing > 60° = "Fully bent"
   - 输出结构化 JSON 格式
2. **LLM 语义推理**：
   - 将 JSON 输入 LLM，生成覆盖左手、右手、双手间关系的描述
   - 要求报告关键运动事件（接触、分离、过伸）
   - 生成 5 级粒度描述（concise → comprehensive）
   - Prompt 设计确保时间顺序保留

### 扩散模型（Section 5.1）
- **运动表示**：3D 坐标 + rotation scalar（手指弯曲在掌平面垂直方向的投影角度）→ x^i ∈ R^{2J×4}
- **架构**：MLP encoder → Transformer decoder with cross-attention → MLP decoder
- **关键设计**：左手/右手/双手间文本分别编码，独立 cross-attention 后残差连接融合，避免混淆左右手动作
- **条件生成**：masked partial denoising，在推理时通过 soft interpolation 控制指定关节/帧，支持 in-betweening、keyframe、wrist trajectory、hand-reaction、long-horizon

### 自回归模型（Section 5.2）
- **运动表示**：局部坐标（相对腕关节），包含腕-腕相对向量、腕速度、腕朝向、局部关节位置/速度、rotation scalar
- **FSQ tokenizer**：有限标量量化，sigmoid + round 量化到 L 个均匀级别
- **Text-prefix AR**：文本 token 前缀 + 因果 attention 的运动 token 自回归预测
- 确定性解码（greedy）

### 评估器训练
- 联合训练文本编码器和手部运动编码器
- 使用 InfoNCE 对比学习目标（非分类式训练）
- T5 backbone


## Experiments

### 主要结果（扩散模型，Table 4）
| Data Ratio | Layers | R-Prec (Top1) | FID↓ | Intra-hand CF1↑ |
|------------|--------|---------------|------|------------------|
| 5% | 4 | 0.142 | 2.574 | 0.523 |
| 5% | 12 | 0.343 | 1.837 | 0.618 |
| 20% | 12 | 0.357 | 1.140 | 0.606 |
| 100% | 12 | **0.427** | 1.349 | **0.641** |
| 100% | 16 | 0.382 | 1.675 | 0.624 |

- 最优配置：12 层 + 100% 数据
- 16 层（260.97M 参数）出现性能下降，表明存在饱和点

### 自回归模型结果（Table 5）
| Model Size | Codebook | R-Prec (Top1) | FID↓ | Intra-hand CF1↑ |
|------------|----------|---------------|------|------------------|
| 29.63M | 512 | 0.210 | 4.683 | 0.545 |
| 92.27M | 2048 | 0.182 | 2.949 | 0.574 |
| 215.31M | 4096 | 0.281 | 1.721 | 0.605 |

- 单独增大 codebook 不一定改善性能，需要与模型容量匹配增长

### Scaling Trend
- R-Precision 与 FLOPs 满足 log-linear 关系：Rprec = 0.4391 × log10(FLOPs) - 3.8707（R=0.96）
- 数据量和模型容量同时增长时，文本对齐和接触精度一致改善

### 用户研究
- 标注质量：解耦策略显著优于直接用 Gemini 3 Pro 标注渲染视频
- 运动质量：HandX 优于 GigaHands 和 HoloAssist
- 100% 数据模型获 48% 投票，20% 获 19%，5% 获 33%

### 机器人 Demo
- 将学习到的灵巧技能迁移到配备灵巧手的类人机器人平台（Figure 1）


## Limitations

1. 数据集规模和多样性仍然有限，无法穷尽人类灵巧性的完整谱系
2. 聚合数据存在固有质量问题（轻微抖动或运动学不合理），无法完全消除
3. 未涉及与物体交互的双臂运动生成（仅手-手交互）
4. 扩散模型 scaling 超过 16 层后出现饱和
5. AR 模型使用确定性解码，未探索采样策略的影响
6. 仅在手部运动空间操作，未涉及全身运动或场景理解


## Key Takeaways

1. **对 DLO 操控的启发**：HandX 的双臂协调生成框架（分离编码左右手 + 交互文本）可借鉴到 DLO 操控中，将 DLO 形变状态作为"第三类文本条件"
2. **Scaling law 在运动生成的适用性**：log-linear 关系表明运动生成领域也存在类似 LLM 的 scaling law，但对机器人操控需验证是否同样成立
3. **接触感知评估的重要性**：Contact Precision/Recall/F1 指标设计可用于评估 DLO 操控中手-物体接触的准确性
4. **解耦标注策略的价值**：运动学特征 → LLM 推理的两阶段标注方法，可扩展到机器人操控数据集的自动标注
5. **Masked partial denoising** 的通用条件生成策略，可直接应用到机器人运动规划中的约束满足问题

## 相关概念

- [[imitation-learning]]
- [[vision-language-model]]
- [[reinforcement-learning]]
- [[diffusion-model]]
- [[bimanual-manipulation]]
- [[deformable-linear-object]]
- [[tactile-sensing]]
- [[grasping]]

## 相关研究者

- [[zhang-zimu|Zhang, Zimu]]
