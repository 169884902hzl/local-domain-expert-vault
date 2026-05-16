---
title: "Scaling diffusion policy in transformer to 1 billion parameters for robotic manipulation"
tags: [manipulation, imitation, diffusion, robot-learning]
created: "2026-04-25"
updated: "2026-04-25"
type: "literature"
status: "done"
summary: "发现Diffusion Policy在Transformer架构(DP-T)中因大梯度问题无法有效扩展，提出ScaleDP通过AdaLN替代cross-attention融合条件+非因果注意力机制，成功将参数从10M扩展到1B，MetaWorld 50任务平均提升21.6%，7个真机任务单臂提升36.25%、双臂提升75%。"
authors: "Zhu, Minjie; Zhu, Yichen; Li, Jinming; Wen, Junjie; Xu, Zhiyuan et al."
year: "2024"
venue: "arXiv Preprint"
zotero_key: "CVTP6AFE"
---
## 摘要

Diffusion Policy（扩散策略） is a powerful technique tool for learning end-to-end（端到端） visuomotor robot control. It is expected that Diffusion Policy（扩散策略） possesses scalability, a key attribute for deep neural networks, typically suggesting that increasing model size would lead to enhanced performance. However, our observations indicate that Diffusion Policy（扩散策略） in transformer architecture (DP-T) struggles to scale effectively; even minor additions of layers can deteriorate training outcomes. To address this issue, we introduce Scalable Diffusion（扩散） Transformer Policy for visuomotor learning. Our proposed method, namely ScaleDP, introduces two modules that improve the training dynamic of Diffusion Policy（扩散策略） and allow the network to better handle multimodal（多模态） action distribution. First, we identify that DPT suffers from large gradient issues, making the optimization of Diffusion Policy（扩散策略） unstable. To resolve this issue, we factorize the feature embedding of observation into multiple affine layers, and integrate it into the transformer blocks. Additionally, our utilize non-causal attention which allows the policy network to “see” future actions during prediction, helping to reduce compounding errors. We demonstrate that our proposed method successfully scales the Diffusion Policy（扩散策略） from 10 million to 1 billion parameters. This new model, named ScaleDP, can effectively scale up the model size with improved performance and generalization. We benchmark ScaleDP across 50 different tasks from MetaWorld and find that our largest ScaleDP outperforms DP-T with an average improvement of 21.6%. Across 7 real-world robot tasks, our ScaleDP demonstrates an average improvement of 36.25% over DP-T on four single-arm tasks and 75% on three bimanual（双臂） tasks. We believe our work paves the way for scaling up models for visuomotor learning. The project page is available at https://scaling-diffusion-policy.github.io/.


## 中文简述

提出基于扩散策略的双臂方法，具有泛化能力特点。

**研究方向**: 机器人操控、模仿学习、扩散模型、机器人学习

## 关键贡献

1. **诊断DP-T可扩展性失败根因**：定位到大梯度问题源于cross-attention条件融合机制
2. **AdaLN条件融合**：用Adaptive Layer Norm替代cross-attention，从timestep+observation回归scale/shift参数，稳定训练动态
3. **非因果注意力**：移除self-attention中的mask，允许动作token看到未来轨迹，减少复合误差
4. **成功扩展到1B参数**：ScaleDP-Ti(10M)→ScaleDP-S(33M)→ScaleDP-B(130M)→ScaleDP-L(457M)→ScaleDP-H(1B)
## 结构化提取

- Problem: Diffusion Policy在Transformer架构中因大梯度无法有效扩展模型规模
- Method: ScaleDP — AdaLN条件融合（替代cross-attention）+ 非因果自注意力 + ViT式模型配置（10M→1B）
- Tasks: MetaWorld 50仿真任务 + 7真机任务（关笔记本/翻杯子/堆叠方块/放网球/网球入袋/扫垃圾/双臂堆叠）
- Sensors: 多视角RGB相机（ZED×2/RealSense×3），本体感觉（6D位姿）
- Robot Setup: Franka 7-DOF单臂 + 双臂UR5（14-DOF），100条人遥操作轨迹/任务
- Metrics: 成功率（20 trials/任务），训练损失收敛曲线
- Limitations: 推理延迟、干扰物鲁棒性有限、光照大幅变化难处理、嵌入式部署未讨论
- Evidence Notes: 全文6301词，4张表，6张图，arXiv 2024，项目页scaling-diffusion-policy.github.io
## 本地引用关系

- [[chen2025coordinated]]
- [[keunknowndiffuser]]
- [[lee2025diffdagger]]
- [[wu2025discrete]]
- [[xia2024cage]]
- [[zhao2025polytouch]]
## 证据元数据

- Fulltext Quality: fulltext
- Evidence Coverage: 完整全文（~6301 词），含 Table I-IV、Figure 1-6，50个MetaWorld仿真任务+7个真实机器人任务，消融实验
- Confidence: high — 全文可读，arXiv 2024，华东师大+美的AI研究中心+北京人形机器人创新中心，仿真+真机实验充分
- Summary: 发现Diffusion Policy在Transformer架构(DP-T)中因大梯度问题无法有效扩展，提出ScaleDP通过AdaLN替代cross-attention融合条件+非因果注意力机制，成功将参数从10M扩展到1B，MetaWorld 50任务平均提升21.6%，7个真机任务单臂提升36.25%、双臂提升75%。


## Problem

Diffusion Policy在Transformer架构(DP-T)中存在可扩展性瓶颈：
1. **大梯度问题**：增加层数导致梯度标准差增大（8层→12层→14层），训练不稳定，性能下降（80.1%→78.4%→74.6%）
2. **Cross-attention融合不稳定**：传统方式将timestep和observation embedding拼接后通过cross-attention融合，深度增加时梯度爆炸
3. **因果注意力限制**：masked attention阻止模型"看到"未来动作，增加累积误差


## Method

### ScaleDP架构
- **输入**：多视角RGB图像（ResNet50编码）+ 本体感觉信息（6D位姿：xyz+rpy）
- **条件融合**：AdaLN(x) = (γ(k,o)+1)·x + β(k,o)，γ和β从timestep k和observation o的embedding和回归
- **Transformer块**：替代原始cross-attention块，每个块包含AdaLN + 非因果多头自注意力 + FFN
- **输出**：去噪后的动作序列

### 模型配置（Table I）
| 变体 | 层数 | 隐藏维度 | 头数 | 参数量 |
|------|------|---------|------|--------|
| ScaleDP-Ti | 8 | 256 | 4 | 10M |
| ScaleDP-S | 12 | 384 | 6 | 33M |
| ScaleDP-B | 12 | 768 | 12 | 130M |
| ScaleDP-L | 24 | 1024 | 16 | 457M |
| ScaleDP-H | 32 | 1280 | 16 | 1B |


## Experiments

### 仿真实验（MetaWorld 50任务）
- **ScaleDP-Ti vs DP-T**：所有难度等级均优于DP-T（Easy/Medium/Hard/Very Hard）
- **模型扩展**：随模型增大成功率持续提升（Ti→S→B→L→H），证明可扩展性
- **数据扩展**：大模型从更多数据中获益更大，小模型提前饱和
- **收敛速度**：大模型收敛更快、训练损失更低

### 真机实验（7任务）

**单臂Franka（Table II）**：
| 模型 | 关笔记本 | 翻杯子 | 堆叠方块 | 放网球 | 平均 |
|------|---------|--------|---------|--------|------|
| DP-T | 80 | 70 | 50 | 5 | 51.25 |
| ACT | 90 | 70 | 55 | 50 | 66.25 |
| ScaleDP-L | 95 | 80 | 70 | 50 | 73.75 |
| ScaleDP-H | 95 | 95 | 90 | 70 | 87.50 |

**双臂UR5（Table III）**：
| 模型 | 网球入袋 | 扫垃圾 | 双臂堆叠 | 平均 |
|------|---------|--------|---------|------|
| DP-T | 20 | 50 | 0 | 23.33 |
| ScaleDP-L | 100 | 80 | 90 | 90.00 |
| ScaleDP-H | 100 | 95 | 100 | 98.33 |

### 消融实验（Table IV）
- 非因果注意力对ScaleDP-L提升最大（+23.34%），双臂堆叠从20%→90%
- ScaleDP-S也受益（+20%），ScaleDP-B适中（+6.67%）

### 视觉泛化
- 外观泛化（物体颜色变化）：ScaleDP-L成功，DP-T失败
- 物体泛化（不同形状物体）：ScaleDP-L可处理，DP-T不能
- 光照泛化（弱光）：ScaleDP-L可处理轻微变化
- 干扰物泛化：ScaleDP-L比DP-T更鲁棒，但仍有限制


## Limitations

1. 大模型推理延迟增加（1B参数实时性待优化）
2. 干扰物泛化仍有缺陷（添加鼠标即可能导致失败）
3. 光照大幅变化难以处理
4. 仅用100条轨迹训练，数据效率讨论不足
5. 未讨论1B模型在嵌入式设备上的部署可行性


## Key Takeaways

1. DP-T的可扩展性瓶颈是工程问题（大梯度）而非原理问题，通过AdaLN即可解决
2. 非因果注意力让模型"看到未来"，对长轨迹预测任务提升显著（双臂堆叠+70%）
3. 模型越大越能从数据中获益——验证了scaling law在机器人策略学习中的适用性
4. 视觉泛化（颜色/形状/光照）是大模型的涌现属性，小模型不具备
5. 来自华东师大+美的AI研究中心+北京人形机器人创新中心，Chaomin Shen组

## 相关概念

- [[robotic-manipulation]]
- [[imitation-learning]]
- [[diffusion-model]]
- [[robot-learning]]
- [[vision-language-model]]
- [[bimanual-manipulation]]

## 相关研究者

- [[zhu-minjie|Zhu, Minjie]]
- [[zhu|Zhu, Yichen]]
- [[li|Li, Jinming]]
- [[wen|Wen, Junjie]]
