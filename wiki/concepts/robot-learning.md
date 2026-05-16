---
title: "Robot Learning"
tags: [concept, robot-learning]
created: "2026-04-25"
updated: "2026-04-26"
type: "concept"
status: "done"
summary: "机器人学习是感知表征到策略学习的端到端范式，当前趋势是大规模预训练+数据驱动泛化"
aliases: ["robot learning", "robotic learning"]
---

## Definition

机器人学习：使机器人通过数据驱动方法习得技能的交叉领域

## Key Ideas

- 机器人学习覆盖从感知表征到策略学习、规划和控制的端到端或模块化方法。
- 数据来源可以是真机、仿真、视频、遥操作、语言或多模态传感器。
- 评价时必须同时看算法指标和机器人执行约束，如延迟、鲁棒性和安全性。
- 大规模策略蒸馏是 robot learning 的实用路线：[[dalal2025local]] 蒸馏 3500+ RL 专家为通用策略，[[collaboration2025open]] OXE 统一数据格式。数据规模正在成为关键变量。
- 闭环反馈是自主学习的核心：[[nazarczuk2025closed]] CLIER 的闭环交互推理（每帧重规划）在需要物理属性测量的任务中展示了 robot learning 的完整闭环。
- 多模态感知（视觉+触觉+力觉）正成为 robot learning 的标准输入：[[zhao2025polytouch]] 三模态、[[liu2025forcemimic]] 力-位混合控制。

## Method Families

- 机器人操控路径：本地有 9 篇相关文献，代表论文包括 [[chi2024diffusion]]、[[do2025watch]]、[[lee2025diffdagger]]、[[liu2025forcemimic]]。
- 模仿学习路径：本地有 6 篇相关文献，代表论文包括 [[chi2024diffusion]]、[[lee2025diffdagger]]、[[liu2025forcemimic]]、[[shah2025acoustic]]。
- 扩散模型路径：本地有 4 篇相关文献，代表论文包括 [[chi2024diffusion]]、[[lee2025diffdagger]]、[[zhao2025polytouch]]、[[zhu2024scaling]]。
- 视觉-语言模型路径：本地有 3 篇相关文献，代表论文包括 [[brohan2023rt2]]、[[chi2024diffusion]]、[[smith2024steer]]。
- 仿真到真实迁移路径：本地有 1 篇相关文献，代表论文包括 [[do2025watch]]。

## Key Papers

- [[chi2024diffusion]]：DDPM 条件扩散策略 + 闭环动作序列预测 + 视觉条件化 + 时序扩散 Transformer；证据：任务成功率、IoU（Push-T）、覆盖率（Sauce）。
- [[brohan2023rt2]]：Vision-Language-Action (VLA) 模型；动作表示为文本 token；co-fine-tune；证据：任务成功率。
- [[zhu2024scaling]]：ScaleDP — AdaLN条件融合（替代cross-attention）+ 非因果自注意力 + ViT式模型配置（10M→1B）；证据：成功率（20 trials/任务），训练损失收敛曲线。
- [[zhao2025polytouch]]：PolyTouch三模态传感器（VHB/硅胶弹性体+荧光照明+曲面镜）+ Tactile-Diffusion Policy（T3+CLIP+AST+Cross-At...；证据：平均任务进度（3-7阶段）、平均任务成功率、弹性体耐久性（小时）。
- [[shah2025acoustic]]：Physics-informed autoencoder + Latent PDE + MPC；证据：能量集中/消除比、计算时间。
- [[nazarczuk2025closed]]：CLIER — 符号程序生成 + 场景图 + Transformer 动作规划 + 闭环原语执行；证据：任务成功率 + 物理属性测量准确性。
- [[liu2025forcemimic]]：ForceCapture（手持力-位采集）+ HybridIL（扩散策略输出 wrench+pose + 混合力-位控制）；证据：运动正确率、>10cm 连续皮成功率。
- [[lee2025diffdagger]]：Diff-DAgger — 扩散 loss 作为不确定性估计 + 分位数阈值 + 连续 K 步验证；证据：F1（失败预测）、成功率（100/20 episodes）、wall-clock 时间。
- [[do2025watch]]：RL + 变阻抗控制 + 在线策略蒸馏 + 观测历史；证据：成功率。
- [[smith2024steer]]：STEER — 密集语言标注 + RT-1 训练 + VLM/人类编排；证据：任务成功率 + 可引导性。

## Evidence Map

- 本地证据规模：当前概念页连接 10 篇 literature notes，其中 10 篇为 `status: done`。
- 代表性证据链：[[chi2024diffusion]]、[[brohan2023rt2]]、[[zhu2024scaling]]、[[zhao2025polytouch]]、[[shah2025acoustic]]。
- 主要交叉主题：机器人操控(9)、模仿学习(6)、扩散模型(4)、视觉-语言模型(3)、仿真到真实迁移(1)。
- 可核查实验结果主要来自：[[chi2024diffusion]]、[[brohan2023rt2]]、[[zhu2024scaling]]、[[zhao2025polytouch]]、[[shah2025acoustic]]；回答具体性能问题时应回到这些论文笔记核对指标。

## Open Problems

- [[chi2024diffusion]] 暴露的限制：继承行为克隆局限（需充足演示数据）；推理延迟高于简单方法（如 LSTM-GMM）；不适合极高频控制任务。
- [[brohan2023rt2]] 暴露的限制：控制频率低（1-3Hz）；无法执行精细操控；仅限单臂数据；模型巨大（55-305B 参数）。
- [[zhu2024scaling]] 暴露的限制：推理延迟、干扰物鲁棒性有限、光照大幅变化难处理、嵌入式部署未讨论。
- [[zhao2025polytouch]] 暴露的限制：VHB磁滞、多模态需更多数据、仅4任务验证、整体成功率偏低。
- [[shah2025acoustic]] 暴露的限制：2D 仅、简单散射体、未真实验证。
- [[nazarczuk2025closed]] 暴露的限制：复杂任务低成功率、依赖位姿精度、仅桌面场景。

## Related Concepts

- [[vision-language-model]]
- [[deformable-linear-object]]
- [[robotic-manipulation]]
- [[imitation-learning]]
- [[grasping]]
- [[bimanual-manipulation]]
- [[reinforcement-learning]]
- [[diffusion-model]]
- [[sim-to-real]]
- [[planning]]
- [[tactile-sensing]]
- [[flow-matching]]
- [[novel-view-synthesis]]
## Related Papers

- [[bang2026environmental]]
- [[brohan2023rt2]]
- [[chen2025benchmarking]]
- [[chen2026abotphysworld]]
- [[chen2026elasticflow]]
- [[chi2024diffusion]]
- [[choi2026rankq]]
- [[consortium2026openhembodiment]]
- [[cui2026aharobot]]
- [[dai2024racer]]
- [[do2025watch]]
- [[du2026bioprovlaagent]]
- [[fan2026xr1]]
- [[feng2026demystifying]]
- [[fu2026capx]]
- [[gu2026vistabot]]
- [[haldar2026point]]
- [[han2026stereopolicy]]
- [[hou2026world]]
- [[huang2026kinder]]
- [[jia2026gsplayground]]
- [[jie2026omnivlarl]]
- [[kim2026agenticcache]]
- [[lee2025diffdagger]]
- [[li2026egolive]]
- [[li2026forcevla2]]
- [[li2026gazevla]]
- [[li2026h2r]]
- [[li2026lehome]]
- [[li2026realvlgr1]]
- [[liu2025forcemimic]]
- [[liu2026longhorizon]]
- [[luo2026flash]]
- [[ma2025running]]
- [[ma2026human]]
- [[moletta2026preference]]
- [[narendra2026knowledgeguided]]
- [[nazarczuk2025closed]]
- [[ortegakral2026rio]]
- [[qi2026compose]]
- [[sakamoto2026e3vsbench]]
- [[shah2025acoustic]]
- [[shen2026plan]]
- [[shi2026agile]]
- [[smith2024steer]]
- [[sun2026maniparena]]
- [[tan2026fsunav]]
- [[tong2026uncovering]]
- [[tu2026embody4d]]
- [[wang2026evolvable]]
- [[wang2026radar]]
- [[wang2026stepnft]]
- [[wang2026visionlanguageaction]]
- [[wang2026vlathinker]]
- [[wu2026affordgrasp]]
- [[wu2026contrastive]]
- [[wu2026large]]
- [[xiao2026avavla]]
- [[xiao2026m2vla]]
- [[xie2026humanintention]]
- [[xu2026r2rgen]]
- [[xu2026roboagent]]
- [[xu2026token]]
- [[xue2026tube]]
- [[yan2026tac2real]]
- [[yang2026asyncshield]]
- [[yang2026physforge]]
- [[ye2026generation]]
- [[ye2026reinforcement]]
- [[yin2026multiple]]
- [[yuan2026embodiedr1]]
- [[yuan2026prefmoe]]
- [[zeng2026recapa]]
- [[zhang2026joyaira]]
- [[zhang2026prts]]
- [[zhang2026recurrent]]
- [[zhang2026touchguide]]
- [[zhang2026visionlanguageaction]]
- [[zhang2026world2minecraft]]
- [[zhao2025polytouch]]
- [[zhao2026visualtactile]]
- [[zheng2026pokevla]]
- [[zhong2026vlaopd]]
- [[zhou2026ego]]
- [[zhou2026sim1]]
- [[zhou2026vlbiman]]
- [[zhu2024scaling]]