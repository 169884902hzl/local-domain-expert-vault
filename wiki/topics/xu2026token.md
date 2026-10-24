---
title: "RL Token: Bootstrapping Online RL with Vision-Language-Action Models"
tags: [manipulation, imitation, VLM, RL, robot-learning]
created: "2026-04-30"
updated: "2026-04-30"
type: "literature"
status: "done"
summary: "提出用 RL token 作为 VLA 到在线 RL 的轻量接口，并在真实机器人装配任务上训练小型 actor-critic head。"
authors: "Xu, Charles; Springenberg, Jost Tobias; Equi, Michael; Amin, Ali; Esmail, Adnan et al."
year: "2026"
venue: "arXiv Preprint"
zotero_key: "CBQPRK6I"
---
## 摘要

Vision-language-action (VLA) models can learn to perform diverse manipulation（操控） skills from pretraining（预训练）, but real-world deployment often needs task-specific improvements in precision, speed, and contact timing. RL Token proposes a lightweight online RL fine-tuning interface for pretrained VLAs. The paper adapts the VLA so it exposes an "RL token", a compact representation readout intended to preserve task-relevant pretrained knowledge, then trains a small actor-critic head on that token while anchoring the learned policy to the original VLA behavior. The method is evaluated on four real-robot manipulation（机器人操控） tasks: screw installation, zip tie fastening, charger insertion, and Ethernet insertion.

## 中文简述

这篇论文的核心不是重新训练一个 VLA，而是把 VLA 的内部表征暴露成一个可供在线 RL 使用的接口。RL token 提供任务相关的压缩状态，小型 actor-critic head 在这个接口上学习动作修正，同时通过 VLA anchoring 限制策略不要偏离预训练模型太远。它的意义在于把“基础模型负责泛化，RL 负责真实任务的精细修正”做成一个工程上可训练、样本效率较高的闭环。

**研究方向**: 机器人操控、VLA、在线 RL、actor-critic、真实机器人微调

## 关键贡献

1. **RL token 作为 VLA 到 RL 的接口**：论文将 VLA 中任务相关的 readout representation 显式作为 RL policy 的输入，使在线 RL 不必直接微调整个大模型。
2. **小型 actor-critic head**：RL 部分主要训练轻量策略/价值头，用于修正动作和提高接触密集任务的速度、精度与成功率。
3. **VLA anchoring**：训练时保留对原始 VLA 行为的约束，降低在线探索把策略带离预训练技能分布的风险。
4. **真实机器人在线练习**：实验覆盖 screw installation、zip tie fastening、charger insertion、Ethernet insertion，强调分钟到小时量级的真实世界 RL fine-tuning。
5. **对专精轨道的价值**：它把 VLA online RL 的问题收敛为接口设计问题，可以进一步追问 token 位置、head 容量、anchor 强度、reward 设计和低成本复现路径。

## 结构化提取

- Problem: 预训练 VLA 已能完成多类操控技能，但真实任务需要更高精度、速度和接触时机；直接对大 VLA 做在线 RL 微调成本高且不稳定。
- Method: 暴露 VLA 内部的 RL token 作为紧凑表征接口，在该 token 上训练小型 actor-critic head 来细化动作，并用 VLA anchoring 约束策略不要偏离预训练行为。
- Tasks: screw installation, zip tie fastening, charger insertion, Ethernet insertion；均为真实机器人接触密集装配/插入类任务。
- Sensors: PDF pass 1 确认 RL policy 输入使用 RL token、proprioception、VLA reference action chunk；RL token 来自 two wrist cameras + one base camera。screw task 使用 joint position，zip tie / Ethernet / charger 使用 end-effector pose。具体相机型号、标定和低层控制仍需代码/作者材料核验。
- Robot Setup: Physical Intelligence 真实机器人平台；PDF pass 1 确认 50 Hz 控制、14 维单步动作、C=10 action chunk（140 维 chunk），以及 screw / zip tie / Ethernet / charger 四类真实任务。机械臂型号、夹爪细节、控制器和 reset protocol 仍未在本地证据中核实。
- Metrics: 成功率、throughput（successes per 10 minutes）、episode length / hardest-phase speed、critical-phase 与 full-task 两种设置。PDF 摘要报告 up to 3x speedup 和若干成功率提升趋势；具体每任务数值仍需图表数据或人工读图后再用于正式 claim。
- Limitations: 目前是少数真实装配任务上的系统验证；低成本复现需要替代 VLA、替代环境和奖励；扩展到触觉/DLO/双臂不能只说加传感器，必须证明 RL token 接口能承载新增状态。
- Evidence Notes: 已有本地 candidate 记录、arXiv abstract/HTML、官方 PDF 入口，以及 2026-04-30 的 PDF pass 1 抽取。当前已覆盖 token/head/action/reward/task 关键实现字段；硬件、精确超参数、代码仓库和图表数值仍标记为未验证。

- Focus Extraction: [[core-paper-extraction-checklist|RL Token Core Paper Extraction Checklist]]
## 本地引用关系

- [[brohan2023rt2]]
- [[collaboration2025open]]
- [[dong2025vitavla]]
- [[jie2026omnivlarl]]
- [[kim2024openvla]]
- [[patel2025realtosimtoreal]]
## 证据元数据

- Fulltext Quality: arXiv HTML + official PDF pass 1; no local PDF snapshot stored in this note.
- Evidence Coverage: abstract, method core, token extraction mechanism, actor-critic setup, action chunking, observation inputs, reward style, four real-robot tasks, reported headline speed/success claims, local candidate metadata.
- Confidence: high for method mechanism, action-chunk setup, task list, and actor/critic scale; medium for original hardware/control details; low for exact per-task numeric values until plot data or code is checked.
- Primary Source: [arXiv:2604.23073v1](http://arxiv.org/abs/2604.23073v1)
- PDF Source: [Physical Intelligence PDF](https://www.pi.website/download/rlt.pdf)
- Local Candidate: `projects/arxiv-daily/2026-04-29-candidates.jsonl`

## 复现判断

- **第一阶段**：不从真实机器人开始，先用 frozen VLA / frozen visual-language encoder 的 hidden state 做 token readout，接小型 actor-critic head，在 LIBERO / ManiSkill / simplified insertion environment 上测试样本效率。
- **必须对照**：全模型微调、action head only、no-anchor RL head、BC-only head、random projection token。
- **关键变量**：token 层位、token pooling、head 容量、anchor loss 权重 `beta`、reference-action dropout、reward 稀疏度、action chunk 长度、真实或仿真接触扰动。
- **失败判据**：如果 RL head 只记住任务 ID 或 reward hack，而没有利用 VLA 表征，则不能把结果解释为 RL token 有效。

## 对本轨道的开放问题

1. RL token 已确认是 final-layer VLA embeddings 上的 learned special-token readout；但 encoder/decoder 深度、heads、optimizer 和训练细节仍未核实。
2. actor-critic head 的论文级容量已大致确认；但低成本复现中多小的 head 仍足以做精细修正、又不覆盖 VLA 先验，仍需实验。
3. anchor regularization 已确认是对 VLA reference action chunk 的 L2 action penalty；但 `beta`、固定 Gaussian std 和 drift 安全阈值仍未核实。
4. 低成本仿真任务能否预测真实插入/装配任务中的样本效率？
5. 触觉、力控或 DLO 状态加入后，是进入 VLA 输入、RL token readout，还是作为 head 的并联状态？

## 相关概念

- [[robotic-manipulation]]
- [[imitation-learning]]
- [[vision-language-model]]
- [[reinforcement-learning]]
- [[robot-learning]]
- [[deformable-linear-object]]
- [[bimanual-manipulation]]
- [[grasping]]

## 相关研究者

- [[xu-charles|Xu, Charles]]
