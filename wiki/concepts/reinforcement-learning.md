---
title: "Reinforcement Learning"
tags: [concept, RL]
created: "2026-04-25"
updated: "2026-04-26"
type: "concept"
status: "done"
summary: "RL 在操控中的核心价值是处理接触丰富和奖励稀疏任务，但样本效率和安全探索仍是瓶颈"
aliases: [RL, "reinforcement learning"]
---

## Definition

强化学习：通过与环境交互获得奖励信号来学习策略的方法

## Key Ideas

- RL 通过奖励函数优化策略，适合接触丰富和难以手写控制律的任务。
- 机器人场景常结合仿真、课程学习、离线数据或模仿学习来降低采样成本。
- 关键风险包括奖励设计、样本效率、sim-to-real 差距和安全探索。
- 模型+RL 混合架构在 sim-to-real 中表现突出：[[marougkas2025integrating]] 势场+残差 RL 仅 2-3h 训练超越纯 RL（IndustReal 8-10h）。
- RL 在 DLO 操控中展现了独特优势：[[li2025routing]] 的 SAC 用于 DLO routing，[[liu2025autonomous]] 的 PPO 用于 DLO Jacobian 初始化。RL 的探索能力在接触丰富任务中尤其有价值。
- 课程学习是样本效率的关键：[[marougkas2025integrating]] 的噪声+动作幅度课程、[[han2025upvital]] 的触觉重建误差奖励课程都显著提升了收敛速度。

## Method Families

- 机器人操控路径：本地有 14 篇相关文献，代表论文包括 [[chen2025vividex]]、[[han2025upvital]]、[[jiang2024manipulation]]、[[karim2024davil]]。
- 模仿学习路径：本地有 5 篇相关文献，代表论文包括 [[chen2025vividex]]、[[kim2024openvla]]、[[li2025routing]]、[[liu820enhancing]]。
- 仿真到真实迁移路径：本地有 4 篇相关文献，代表论文包括 [[liu2025autonomous]]、[[marougkas2025integrating]]、[[wu2025imperfect]]、[[wu2025rlgsbridge]]。
- 扩散模型路径：本地有 3 篇相关文献，代表论文包括 [[chen2025vividex]]、[[kim2024openvla]]、[[li2025routing]]。
- 视觉-语言模型路径：本地有 2 篇相关文献，代表论文包括 [[kim2024openvla]]、[[liu820enhancing]]。

## Key Papers

- [[kim2024openvla]]：开源 7B VLA（Prismatic VLM + 动作 token）；Open X-Embodiment 训练；LoRA 微调；证据：任务成功率。
- [[wu2025rlgsbridge]]：RL-GSBridge — Soft Mesh Binding GS + 物理动力学 GS 编辑 + SACwB RL；证据：成功率（抓取 Sim-to-Real avg ↓6.6%，Pick-and-Place ↑4%）。
- [[wu2025imperfect]]：SSDF — Transformer 自监督预训练 (MTP+TR+AA) + 特征相似度质量分数 + 加权 BC；证据：任务成功率（仿真 85.6%/88.0%/50.4%/29.6%/28.4%，真实平均 45%）。
- [[singh2025handobject]]：HOP — 3D 手-物体提取 + Simulator-in-the-loop retargeting + Transformer 预训练；证据：任务成功率 + 样本效率 + 鲁棒性 + 泛化性。
- [[marougkas2025integrating]]：势场模型策略 + 残差 RL（PPO）+ 自适应噪声课程；证据：插入成功率（仿真+真实）。
- [[liu2025autonomous]]：RLAC — PPO 训练 actor → 初始化 Jacobian → 缩放调整 → AC 精确收敛；证据：成功率、PER（路径效率比）。
- [[li2025routing]]：两阶段 — SAC RL（摩擦随机化+拉伸惩罚）→ DDIM 扩散策略（闭环）；证据：成功率（91 场景）、目标距离（cm）。
- [[han2025upvital]]：UpViTaL — LSTM 触觉自编码器 + MAE 视觉预训练 + 触觉重建误差奖励 + PPO；证据：成功率（100 次评估 × 4 seeds）。
- [[chen2025vividex]]：ViViDex — 参考轨迹提取 + trajectory-guided RL + 坐标变换增强的统一视觉策略；证据：成功率 SR10、SR3（3cm 阈值）、轨迹误差 Eo/Eh。
- [[karim2024davil]]：DA-VIL — RL（PPO 预测 K）+ QP 变阻抗控制器，距离约束保证协同；证据：轨迹跟踪误差（m）。

## Evidence Map

- 本地证据规模：当前概念页连接 15 篇 literature notes，其中 15 篇为 `status: done`。
- 代表性证据链：[[kim2024openvla]]、[[wu2025rlgsbridge]]、[[wu2025imperfect]]、[[singh2025handobject]]、[[marougkas2025integrating]]。
- 主要交叉主题：机器人操控(14)、模仿学习(5)、仿真到真实迁移(4)、扩散模型(3)、视觉-语言模型(2)。
- 可核查实验结果主要来自：[[kim2024openvla]]、[[wu2025rlgsbridge]]、[[wu2025imperfect]]、[[singh2025handobject]]、[[marougkas2025integrating]]；回答具体性能问题时应回到这些论文笔记核对指标。

## Open Problems

- [[kim2024openvla]] 暴露的限制：控制频率 ~6Hz；仅支持单臂；动作离散化损失精度；不支持双臂。
- [[wu2025rlgsbridge]] 暴露的限制：仅桌面任务、渲染速度、有限随机范围。
- [[wu2025imperfect]] 暴露的限制：需专家数据、计算开销大、仅桌面任务。
- [[singh2025handobject]] 暴露的限制：单物体、忽略动力学、小数据量。
- [[marougkas2025integrating]] 暴露的限制：需 3D 模型、仅 top-down、小物体跟踪。
- [[liu2025autonomous]] 暴露的限制：单一任务、2D、固定接触、手动参数。

## Related Concepts

- [[deformable-linear-object]]
- [[vision-language-model]]
- [[robotic-manipulation]]
- [[grasping]]
- [[imitation-learning]]
- [[bimanual-manipulation]]
- [[diffusion-model]]
- [[sim-to-real]]
- [[robot-learning]]
- [[planning]]
- [[tactile-sensing]]
- [[flow-matching]]
- [[collision-avoidance]]
- [[test-time-scaling]]
- [[dynamical-systems]]
- [[proximity-sensing]]
## Related Papers

- [[bang2026environmental]]
- [[chang2026partially]]
- [[chen2025benchmarking]]
- [[chen2025vividex]]
- [[chen2026adacleargrasp]]
- [[chen2026craft]]
- [[chen2026lastr1]]
- [[chen2026posterior]]
- [[choi2026rankq]]
- [[consortium2026openhembodiment]]
- [[cui2026aharobot]]
- [[das2026dart]]
- [[dong2026faster]]
- [[fang2026dexdrummer]]
- [[fu2026capx]]
- [[gao2026driftbased]]
- [[ghosh2026reducing]]
- [[gu2026refinedp]]
- [[han2025upvital]]
- [[he2026generative]]
- [[hou2026world]]
- [[huang2026flexitac]]
- [[huang2026kinder]]
- [[jauhri2026wholebody]]
- [[jeong2026your]]
- [[ji2026recovering]]
- [[jia2026dreamplan]]
- [[jiang2024manipulation]]
- [[jiang2026blockr1]]
- [[jiang2026break]]
- [[jiang2026videop2r]]
- [[jiang2026world4rl]]
- [[jie2026omnivlarl]]
- [[jin2026grounding]]
- [[kang2026coenv]]
- [[kappel2026qdtraj]]
- [[karim2024davil]]
- [[khan2026discrete]]
- [[kim2024openvla]]
- [[kohlbrenner2026egocentric]]
- [[lee2026implicit]]
- [[levy2026simulation]]
- [[li2025routing]]
- [[li2026affordsim]]
- [[li2026ets]]
- [[li2026forcevla2]]
- [[li2026hierarchical]]
- [[li2026hpedit]]
- [[li2026lehome]]
- [[li2026realvlgr1]]
- [[lian2026langforce]]
- [[liang2026vanim]]
- [[liu2025autonomous]]
- [[liu820enhancing]]
- [[liufu2026repovla]]
- [[longhini2026behavioral]]
- [[lu2026unified]]
- [[luijkx2026llmguided]]
- [[luo2026selfimproving]]
- [[mahboob2026betting]]
- [[marougkas2025integrating]]
- [[moroncelli2026jumpstart]]
- [[narendra2026knowledgeguided]]
- [[park2026demodiffusion]]
- [[patil2026youve]]
- [[peters2026coordinated]]
- [[saad2026hybrid]]
- [[sagar2026robomd]]
- [[schperberg2026mobius]]
- [[sha2026efficient]]
- [[shen2026plan]]
- [[singh2025handobject]]
- [[spieler2026slotmpc]]
- [[stambaugh2026mixeddensity]]
- [[sun2026maniparena]]
- [[tan2026fsunav]]
- [[tong2026uncovering]]
- [[wang2023hierarchical]]
- [[wang2023multistage]]
- [[wang2026adagamma]]
- [[wang2026any2any]]
- [[wang2026evolvable]]
- [[wang2026offline]]
- [[wang2026phys2real]]
- [[wang2026stepnft]]
- [[wang2026vlathinker]]
- [[wang2026while]]
- [[wei2026navol]]
- [[wu2025imperfect]]
- [[wu2025rlgsbridge]]
- [[wu2026large]]
- [[wu2026reliable]]
- [[xiao2026worldenv]]
- [[xie102multiview]]
- [[xu2026expertgen]]
- [[xu2026roboagent]]
- [[xu2026token]]
- [[xu2026twinrlvla]]
- [[yan2026tac2real]]
- [[yang2026asyncshield]]
- [[yang2026automated]]
- [[yang2026rise]]
- [[ye2026generation]]
- [[ye2026reinforcement]]
- [[yin2026genie]]
- [[you2026dotsim]]
- [[yu2026atrs]]
- [[yuan2026embodiedr1]]
- [[yuan2026prefmoe]]
- [[zhang2021dair]]
- [[zhang2026handx]]
- [[zhang2026prts]]
- [[zhang2026recurrent]]
- [[zhang2026safevla]]
- [[zhang2026world2minecraft]]
- [[zhao2026rosclaw]]
- [[zhao2026visualtactile]]
- [[zhong2026vlaopd]]
- [[zhou2026characterizing]]
- [[zhou2026ego]]
- [[zhu2026nsvla]]
- [[ziakas2026aligning]]