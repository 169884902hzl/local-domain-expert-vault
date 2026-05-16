---
title: "Learning Fine-Grained Bimanual Manipulation with Low-Cost Hardware"
tags: [manipulation, bimanual]
created: "2026-04-26"
updated: "2026-04-26"
type: "literature"
status: "done"
summary: "提出 ALOHA 低成本双臂遥操作系统（<$20k）和 ACT 算法（action chunking + temporal ensemble + CVAE），10 分钟演示即可学习 6 种精细操控任务（80-96% 成功率），是模仿学习和双臂操控的里程碑工作"
authors: "Zhao, Tony; Kumar, Vikash; Levine, Sergey; Finn, Chelsea"
year: "2023"
venue: "Robotics: Science and Systems XIX"
zotero_key: "G4XHE2JY"
---
## 摘要

Zotero 未提供摘要；详见下方精读分析。

## 中文简述

提出基于学习方法的双臂方法。

**研究方向**: 机器人操控、双臂操控

## 关键贡献

1. **ALOHA 硬件**：低成本双臂遥操作系统（$20k），关节空间映射 + 3D打印机构，50Hz 控制，<2h 组装
2. **ACT 算法**：Action Chunking（预测 k=100 步动作序列，k 倍缩短有效视界）+ Temporal Ensembling（指数加权平均重叠预测）+ CVAE 训练（建模人类演示多模态性）
3. **系统整合**：10 分钟演示数据学习 6 种真机精细操控任务（成功率 80-96%）
## 结构化提取

- Problem: 低成本硬件上的精细双臂操控；模仿学习复合误差
- Method: Action Chunking with Transformers (ACT)；CVAE 训练；Temporal Ensembling
- Tasks: Slide Ziploc, Slot Battery, Open Cup, Thread Velcro, Prep Tape, Put On Shoe, Transfer Cube(sim), Bimanual Insertion(sim)
- Sensors: 4x Logitech C922x RGB cameras (top, front, left-wrist, right-wrist), 480x640
- Robot Setup: 2x ViperX 6-DoF (follower) + 2x WidowX (leader), bimanual, 14-DoF, 50Hz
- Metrics: Task success rate (%)
- Limitations: 多指操作/大力矩任务硬件不足；Thread Velcro 等感知困难任务成功率低；每任务需 50 演示单独训练
- Evidence Notes: ALOHA 是当前最流行的低成本双臂平台；ACT 是双臂操控标准基线；action chunking 思想被 Diffusion Policy 等后续工作采用
## 本地引用关系

- [[chi2024diffusion]]
- [[fu2024mobile]]
## 证据元数据

- Fulltext Quality: full (13037 words from Zotero PDF)
- Evidence Coverage: complete (full paper including appendices, all experiments and ablations covered)
- Confidence: high (full text read, all tables and ablations verified)
- Summary: 提出 ALOHA 低成本双臂遥操作系统（<$20k）和 ACT 算法（action chunking + temporal ensemble + CVAE），10 分钟演示即可学习 6 种精细操控任务（80-96% 成功率），是模仿学习和双臂操控的里程碑工作
- PDF available: Yes
- ArXiv: 2304.13705
- DOI: 10.15607/RSS.2023.XIX.016
## Problem

精细操控任务（如穿扎带、装电池）要求毫米级精度、丰富接触力感知和闭环视觉反馈。现有系统依赖昂贵硬件（>$100k）和精确传感器。能否用低成本硬件（<$20k）+ 学习实现精细操控？核心挑战：(1) 低成本硬件精度差（5-8mm repeatability）；(2) 模仿学习的复合误差在精细任务中尤为严重；(3) 人类演示具有多模态性和非平稳性。
## Method

- **Action Chunking**：策略 πθ(at:t+k|st) 预测未来 k 步动作，k=100 最佳，将复合误差的影响缩减 k 倍
- **Temporal Ensembling**：每步查询策略，对重叠预测做加权平均 wi=exp(-m*i)，无额外训练开销，使动作更平滑
- **CVAE 训练**：
  - Encoder：BERT-style Transformer → 样式变量 z（对角高斯）
  - Decoder（策略）：4x ResNet18 图像编码 → Transformer Encoder(4层) + Transformer Decoder(7层) → k x 14 动作
  - 测试时 z=0，确定性输出
  - L1 reconstruction loss + β*KL regularization
- **输入**：4 路 RGB 480x640 + 14 维关节位置
- **输出**：k x 14 维绝对关节位置
- **规模**：~80M 参数，训练 5h/RTX 2080 Ti，推理 0.01s
## Experiments

### 仿真（MuJoCo, 50 trials x 3 seeds）
- Transfer Cube: ACT 97%(script)/82%(human) vs BeT 60%/16%
- Bimanual Insertion: ACT 93%/76% vs BeT 21%/0%

### 真实（25 trials, 50 demos）
- Slide Ziploc: 88%, Slot Battery: 96%, Open Cup: 84%
- Put On Shoe: 92%, Prep Tape: 64%, Thread Velcro: 20%
- 所有基线（BeT/RT-1/VINN/BC-ConvMLP）在真实任务上几乎全部 0%

### 消融
- Action chunking 普遍有效（k=1: 1% → k=100: 44% 平均成功率）
- CVAE 对人类数据不可或缺（35.3% → 2%），对脚本数据无影响
- Temporal ensemble：ACT +3.3%, BC-ConvMLP +4%, VINN -20%
## Limitations

- 硬件：无法做多指操作（如开儿童药瓶推扣）、大力矩任务（拧密封水瓶）、需要指甲的任务
- 算法：解糖果包装（感知困难）、平躺密封袋（多阶段空中操控困难）失败
- 需要 50 次演示/任务，每个任务单独训练，缺乏多任务泛化
- Thread Velcro 成功率仅 20%，表明在低对比度小物体感知上仍有挑战
## Key Takeaways

1. Action chunking 是解决精细操控复合误差的高效方案，且对多种 IL 算法都有益
2. 50Hz 高频控制对精细操控至关重要（5Hz 完成时间慢 62%）
3. CVAE 对从人类演示学习是必要的，但仅对非确定性数据有影响
4. 低成本硬件 + 端到端学习可以替代昂贵系统执行精细任务
5. ACT 成为后续双臂操控的标准基线，action chunking 思想被广泛采纳

## 相关概念

- [[robotic-manipulation]]
- [[bimanual-manipulation]]
- [[vision-language-model]]
- [[diffusion-model]]

## 相关研究者

- [[zhao-tony|Zhao, Tony]]
- [[levine-sergey|Levine, Sergey]]
- [[finn|Finn, Chelsea]]
