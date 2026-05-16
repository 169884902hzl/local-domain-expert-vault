---
title: "Mobile ALOHA: Learning bimanual mobile manipulation with low-cost whole-body teleoperation"
tags: [manipulation, imitation, bimanual]
created: "2026-04-26"
updated: "2026-04-26"
type: "literature"
status: "done"
summary: "Stanford 提出低成本全身遥操作系统 Mobile ALOHA（$32k），将 ALOHA 扩展到移动双臂操控，发现与静态 ALOHA 数据集 co-training 可将成功率提升最高 90%，仅用 50 个演示即可学会擦酒、乘电梯、收纳锅具等复杂任务"
authors: "Fu, Zipeng; Zhao, Tony Z.; Finn, Chelsea"
year: "2024"
venue: "arXiv Preprint"
zotero_key: "VMJYIEYV"
---
## 摘要

Imitation learning（模仿学习） from human demonstrations has shown impressive performance in robotics. However, most results focus on table-top manipulation（操控）, lacking the mobility and dexterity necessary for generally useful tasks. In this work, we develop a system for imitating mobile manipulation（移动操控） tasks that are bimanual（双臂） and require whole-body control. We first present Mobile ALOHA, a low-cost and whole-body teleoperation system for data collection. It augments the ALOHA system [104] with a mobile base, and a whole-body teleoperation interface. Using data collected with Mobile ALOHA, we then perform supervised behavior cloning and find that co-training with existing static ALOHA datasets boosts performance on mobile manipulation（移动操控） tasks. With 50 demonstrations for each task, co-training can increase success rates by up to 90%, allowing Mobile ALOHA to autonomously complete complex mobile manipulation（移动操控） tasks such as sauteing and serving a piece of shrimp, opening a two-door wall cabinet to store heavy cooking pots, calling and entering an elevator, and lightly rinsing a used pan using a kitchen faucet.

## 中文简述

提出基于模仿学习的双臂方法。

**研究方向**: 机器人操控、模仿学习、双臂操控

## 关键贡献

1. **Mobile ALOHA 硬件系统**：$32k 低成本全身遥操作系统，AgileX Tracer 移动基座 + ALOHA 双臂，支持同步控制基座和双臂
2. **全身遥操作接口**：操作者通过腰带连接到移动基座，通过反驱车轮实现基座移动，双手控制 ALOHA leader 手臂
3. **Co-training 策略**：与静态 ALOHA 数据集（825 episodes）联合训练，零填充基座动作维度，显著提升移动操控性能
4. **多算法兼容**：验证了 ACT、Diffusion Policy、VINN 三种 IL 方法均受益于 co-training
## 结构化提取

- Problem: 模仿学习局限于桌面操控，缺乏低成本全身遥操作硬件和有效学习方法
- Method: Mobile ALOHA 硬件系统（$32k）+ 静态 ALOHA 数据 co-training + ACT/Diffusion Policy/VINN
- Tasks: 7 个真实世界移动双臂操控任务（擦酒/炒虾/洗锅/收纳锅/乘电梯/推椅子/击掌）
- Sensors: 3x RGB 摄像头（2 腕部 + 1 顶部，480x640@50Hz）+ 关节位置
- Robot Setup: Mobile ALOHA（2x ViperX 300 + AgileX Tracer 基座），16-DOF 动作空间
- Metrics: 任务成功率（20 次评估），子任务成功率
- Limitations: 占地面积大（90x135cm）；固定手臂高度限制低处操作；仅单任务学习；Cook Shrimp（长时域）成功率低
- Evidence Notes: Mobile ALOHA 证明了低成本全身遥操作的可行性；co-training 是从静态数据到移动操控迁移的有效范式
## 本地引用关系

- [[chi2024diffusion]]
- [[zhao2023finegrained]]
## 证据元数据

- Fulltext Quality: full (from Zotero PDF, ~11437 words)
- Evidence Coverage: complete (full text including hardware design, co-training method, 7 tasks, ablations, user study)
- Confidence: high (full text read, hardware specs, training details, and all experiments verified)
- Summary: Stanford 提出低成本全身遥操作系统 Mobile ALOHA（$32k），将 ALOHA 扩展到移动双臂操控，发现与静态 ALOHA 数据集 co-training 可将成功率提升最高 90%，仅用 50 个演示即可学会擦酒、乘电梯、收纳锅具等复杂任务


## Problem

现有模仿学习大多局限于桌面操控，缺乏执行真实世界任务所需的移动性和双臂协调能力。两大障碍：(1) 缺乏低成本、即插即用的全身遥操作硬件；(2) 尚未证明高性能的双臂移动操控可通过模仿学习实现。如何以低成本构建可学习复杂移动操控任务的系统？


## Method

- **硬件设计**：
  - 移动基座：AgileX Tracer AGV，差速驱动，最高 1.6m/s，负载 100kg，成本 $7000
  - 双臂：2x ViperX 300（6-DOF），每臂负载 750g
  - 电池：1.26kWh（14kg），续航 12 小时
  - 计算：消费级笔记本 + RTX 3070 Ti（8GB VRAM）
  - 传感器：3x Logitech C922x RGB 摄像头（480x640@50Hz），2 个腕部 + 1 个顶部
  - 总成本：$32k（含车载电源和计算）
- **动作空间**：16-DOF = 14 DOF 关节位置（双臂含夹爪）+ 2 DOF 基座速度（线速度 + 角速度）
- **Co-training 训练目标**：
  - L = E_{D_mobile}[L(a_arms, a_base, π(o))] + E_{D_static}[L(a_arms, [0,0], π(o))]
  - 静态 ALOHA 数据的基座动作零填充，前向相机忽略以匹配 3 摄像头设置
  - 50/50 采样比例，batch size 16
- **Action Chunking**：所有方法使用动作分块（ACT 默认 chunk=45，Diffusion Policy chunk=64）
  - 处理基座延迟：执行 chunk 中前 k-d 步手臂动作和后 k-d 步基座动作


## Experiments

### Co-training 提升 ACT 性能（7 个真实世界任务，每个 20 次评估）
| 任务 | Co-train | No Co-train | 提升 | 演示数 |
|------|----------|-------------|------|--------|
| Wipe Wine | 95% | 50% | +45% | 50 |
| Cook Shrimp | 40% | 20% | +20% | 20 |
| Rinse Pan | 80% | 0% | +80% | 50 |
| Use Cabinet | 85% | 85% | 0% | 50 |
| Call Elevator | 95% | 0% | +95% | 50 |
| Push Chairs | 80% | 0% | +80% | 50 |
| High Five | 85% | 85% | 0% | 20 |

- Co-training 在 5/7 任务上显著提升，特别是需要精确操控的子任务（Press Button、Turn On Faucet）
- 对泛化有帮助：Push Chairs 第 4/5 椅子（OOD）co-training 分别提升 15% 和 89%

### 多算法兼容（Wipe Wine + Push Chairs）
- ACT + co-train：Wipe Wine 95%，Push Chairs 80%
- Diffusion Policy + co-train：Wipe Wine 65%，Push Chairs 100%
- VINN + Chunking + co-train：Wipe Wine 15%，Push Chairs 60%

### 消融实验
- **数据效率**（Wipe Wine）：35 demos + co-train（70%）> 50 demos 无 co-train（50%）
- **数据混合比例**：30%/50%/70% co-training 采样率均达到 90-95%，对比例不敏感
- **Co-training vs Pre-training**：co-training（95%）>> pre-training（40%）≈ 无 co-training（50%）

### 用户研究
- 8 名参与者（4 女 4 男，21-26 岁），5 次试验后接近专家速度
- 完成时间下降：Wipe Wine 46s→28s（-39%），Use Cabinet 75s→36s（-52%）


## Limitations

- 占地面积 90x135cm，可能过窄无法通过某些路径
- 固定高度的双臂无法操作低处柜子、烤箱、洗碗机
- 仅展示单任务模仿学习，不支持多任务或自主改进
- Cook Shrimp（75 秒长时域任务）仅 40% 成功率，需更多演示数据
- 基座速度控制存在随机性，开环回放误差 >10cm
- 所有演示由 2 名专家操作者采集，未处理次优演示


## Key Takeaways

1. 低成本全身遥操作系统可实现高质量移动双臂操控数据采集
2. 与静态桌面数据的 co-training 是提升移动操控性能和数据效率的关键，即使任务和形态不同
3. Co-training 优于 pre-training，联合训练可避免灾难性遗忘
4. 简单的动作空间拼接（关节位置+基座速度）使现有 IL 算法几乎无需修改即可应用
5. Action chunking 对移动操控至关重要，可处理手臂和基座的延迟差异

## 相关概念

- [[robotic-manipulation]]
- [[imitation-learning]]
- [[bimanual-manipulation]]
- [[diffusion-model]]
- [[grasping]]

## 相关研究者

- [[fu|Fu, Zipeng]]
- [[finn|Finn, Chelsea]]
