---
title: "Imitation Learning"
tags: [concept, imitation]
created: "2026-04-25"
updated: "2026-04-26"
type: "concept"
status: "done"
summary: "模仿学习的核心挑战是分布偏移和数据效率，Action Chunking 和扩散策略是当前主流范式"
aliases: ["imitation learning", "behavioral cloning", IL]
---

## Definition

模仿学习：从专家示范中学习策略的方法

## Key Ideas

- 分布偏移是模仿学习的根本问题：策略在自身预测上训练时偏离专家分布。[[chi2024diffusion]] 用闭环扩散策略部分缓解（每步重新预测），[[lee2025diffdagger]] 用 DAgger 主动收集修正数据。
- Action Chunking 是 IL 在操控中的关键设计：[[zhao2023finegrained]] ACT 用 CVAE+Temporal Ensembling 处理多模态分布，成为 ALOHA 系列的基础范式。
- 数据效率差异巨大：[[zhao2023finegrained]] 每任务需 50 演示，[[wang2025oneshot]] ODIL 仅需 1 次。单样本方法依赖视觉伺服而非策略学习，适用场景受限。
- 长时序 IL 的累积误差严重：[[chen2025deformpam]] 用偏好学习引导 action selection 缓解分布偏移，[[wu2025imperfect]] 用质量分数加权处理不完美演示。
- OXE 数据基础设施正在改变 IL 的规模：[[collaboration2025open]] 的统一格式（RLDS）使跨机器人数据共享成为可能，[[team2024octo]] 在此基础上训练的通用策略展示了跨迁移能力。但数据质量不均匀仍是问题。

## Method Families

- **Action Chunking / CVAE**：预测短时域动作块。[[zhao2023finegrained]] ACT 是代表。简单有效但 CVAE 容易模式坍缩。
- **扩散策略 IL**：用扩散模型学习动作分布。[[chi2024diffusion]]、[[zhu2024scaling]]、[[wu2025discrete]]。多模态处理更强但推理更慢。
- **主动学习 / DAgger**：部署时收集修正数据。[[lee2025diffdagger]] Diff-DAgger 用扩散 loss 做不确定性估计。
- **偏好/质量引导**：用额外模型评估动作质量。[[chen2025deformpam]] DPO 偏好+reward-guided selection；[[wu2025imperfect]] 质量分数+加权 BC。
- **单样本/少样本 IL**：[[wang2025oneshot]] ODIL 视觉伺服。依赖强先验。

## Key Papers

- [[chi2024diffusion]]：Diffusion Policy 是当前 IL 主流方案。DDPM+闭环动作序列预测，在 Push-T/Sauce 等任务上建立基线。
- [[zhao2023finegrained]]：ACT 开创 Action Chunking 范式。CVAE+Temporal Ensembling 在 ALOHA 上验证了 10+ 双臂任务。
- [[fu2024mobile]]：Mobile ALOHA 是最广泛的双臂 IL 平台。Co-training 策略是数据效率关键。
- [[lee2025diffdagger]]：Diff-DAgger 将扩散 loss 用作不确定性估计器。IL 主动学习的代表性工作。
- [[chen2025deformpam]]：针对可变形物体长时序 IL 的分布偏移，用偏好学习引导扩散策略。
- [[wu2025imperfect]]：处理不完美专家演示。Transformer 自监督预训练+质量分数加权。
- [[zhu2024scaling]]：ScaleDP 10M→1B。展示规模效应在 IL 中的潜力。
- [[wang2025oneshot]]：ODIL 单样本双臂 IL。3 阶段视觉伺服在 ABB YuMi 上验证。
- [[zhao2025polytouch]]：Tactile-Diffusion Policy 展示触觉信号对 IL 的增益。
- [[collaboration2025open]]：OXE 数据集+RT-X 模型是大规摸 IL 基础设施。

## Evidence Map

- **本地证据规模**：35 篇 status:done 文献，覆盖 Action Chunking（5）、扩散策略（13）、主动学习（2）、偏好引导（3）、少样本（2）、平台/基准（10）。
- **强证据问题**：Action Chunking vs 逐步预测有 ACT/DP 系统对比；扩散策略多模态优势有 [[chi2024diffusion]] 量化；数据混合 co-training 有 [[fu2024mobile]] 验证。
- **弱证据问题**：IL 在 DLO 双臂操控场景的系统性评估不足；IL 在线适应方案仅有 [[lee2025diffdagger]]；IL 安全保证（本地无专门文献）。

## Open Problems

- **双臂 DLO 操控的 IL**：本地 DLO IL 论文主要是单臂或简单双臂。双臂 DLO 协调需要新 IL 架构处理高维动作空间和协调约束。
- **长时序 IL 的误差恢复**：[[chen2025deformpam]] 的分布偏移、[[grotz2025twin]] 的 23.3% 平均成功率说明长时序 IL 远未解决。
- **IL + Sim-to-Real 的数据策略**：[[wu2025imperfect]] 处理不完美数据是方向之一。

## Related Concepts

- [[deformable-linear-object]]
- [[robotic-manipulation]]
- [[vision-language-model]]
- [[grasping]]
- [[bimanual-manipulation]]
- [[diffusion-model]]
- [[reinforcement-learning]]
- [[robot-learning]]
- [[sim-to-real]]
- [[planning]]
- [[tactile-sensing]]
- [[flow-matching]]
- [[dynamical-systems]]
- [[collision-avoidance]]
## Related Papers

- [[Reactive Motion Generation via Phase-varying Neural Potential Functions]]
- [[aida2026cortex]]
- [[bang2026environmental]]
- [[chang2026partially]]
- [[chen2025coordinated]]
- [[chen2025deformpam]]
- [[chen2025effective]]
- [[chen2025vividex]]
- [[chen2026craft]]
- [[chen2026elasticflow]]
- [[chen2026lastr1]]
- [[chen2026posterior]]
- [[chen2026ropa]]
- [[chen2026rotridiff]]
- [[chi2024diffusion]]
- [[chuang2025active]]
- [[collaboration2025open]]
- [[consortium2026openhembodiment]]
- [[cui2026aharobot]]
- [[dai2024racer]]
- [[deshpande2026molmob0t]]
- [[dey2025revla]]
- [[dong2025vitavla]]
- [[du2024embedded]]
- [[fan2026xr1]]
- [[fang2026force]]
- [[feng2026demystifying]]
- [[feng2026see]]
- [[fu2024mobile]]
- [[gao2024prime]]
- [[gao2026driftbased]]
- [[george2024vital]]
- [[grotz2025twin]]
- [[gu2026refinedp]]
- [[guan2026dssp]]
- [[haldar2026point]]
- [[han2026stereopolicy]]
- [[hartz2024art]]
- [[he2026exploratory]]
- [[hu2026arvla]]
- [[huang2025match]]
- [[huang2026kinder]]
- [[huang2026mimic]]
- [[iek2026coral]]
- [[jauhri2026wholebody]]
- [[jeong2026your]]
- [[ji2026recovering]]
- [[jia2026dreamplan]]
- [[jia2026gsplayground]]
- [[jiang2026videop2r]]
- [[jiang2026world4rl]]
- [[jie2026omnivlarl]]
- [[kang2026coenv]]
- [[keunknowndiffuser]]
- [[kim2024openvla]]
- [[kuroki2025gendom]]
- [[lee2025diffdagger]]
- [[lee2026implicit]]
- [[lee2026modular]]
- [[li2025routing]]
- [[li2026affordsim]]
- [[li2026egolive]]
- [[li2026gazevla]]
- [[li2026h2r]]
- [[li2026hpedit]]
- [[li2026realvlgr1]]
- [[lian2026langforce]]
- [[liang2026vanim]]
- [[lin2026hifvla]]
- [[liu2025forcemimic]]
- [[liu2026longhorizon]]
- [[liu820enhancing]]
- [[liufu2026repovla]]
- [[longhini2026behavioral]]
- [[luo2024humanagent]]
- [[luo2026flash]]
- [[luo2026selfimproving]]
- [[ma2026human]]
- [[ma2026semanticcontact]]
- [[mahboob2026betting]]
- [[missal2026ropedreamer]]
- [[moletta2026preference]]
- [[moroncelli2026jumpstart]]
- [[narendra2026knowledgeguided]]
- [[niu2026boosting]]
- [[niu2026versatile]]
- [[ortegakral2026rio]]
- [[park2026acg]]
- [[park2026demodiffusion]]
- [[patel2024getzero]]
- [[patil2026youve]]
- [[peters2026coordinated]]
- [[qi2026compose]]
- [[qiu2025wildlma]]
- [[sakamoto2026e3vsbench]]
- [[scheikl620movement]]
- [[schperberg2026mobius]]
- [[sha2026efficient]]
- [[shah2025acoustic]]
- [[shen2026plan]]
- [[shi2025zeromimic]]
- [[shi2026agile]]
- [[spieler2026slotmpc]]
- [[stambaugh2026mixeddensity]]
- [[sundaralingam2026curobov2]]
- [[tan2026fsunav]]
- [[tang2025uad]]
- [[team2024octo]]
- [[tong2024ovalprompt]]
- [[tong2026uncovering]]
- [[tu2026embody4d]]
- [[wang2025oneshot]]
- [[wang2025vlaadapter]]
- [[wang2026any2any]]
- [[wang2026beyond]]
- [[wang2026discretertc]]
- [[wang2026evolvable]]
- [[wang2026ocra]]
- [[wang2026offline]]
- [[wang2026radar]]
- [[wang2026visionlanguageaction]]
- [[wang2026vlathinker]]
- [[wang2026while]]
- [[wei2026navol]]
- [[wu2025imperfect]]
- [[wu2025tacdiffusion]]
- [[wu2026continually]]
- [[wu2026contrastive]]
- [[wu2026large]]
- [[wu2026reliable]]
- [[xia2024cage]]
- [[xiao2026avavla]]
- [[xiao2026m2vla]]
- [[xiao2026worldenv]]
- [[xie2026humanintention]]
- [[xu2026expertgen]]
- [[xu2026fingereye]]
- [[xu2026movethenoperate]]
- [[xu2026r2rgen]]
- [[xu2026token]]
- [[xu2026twinrlvla]]
- [[xue2026tube]]
- [[yang2026asyncshield]]
- [[yang2026automated]]
- [[yang2026hivla]]
- [[yang2026ultradexgrasp]]
- [[ye2026generation]]
- [[yin2026genie]]
- [[yin2026multiple]]
- [[you2026dotsim]]
- [[yu2026atrs]]
- [[yuan2026embodiedr1]]
- [[zhang2026forceflow]]
- [[zhang2026generative]]
- [[zhang2026handx]]
- [[zhang2026recurrent]]
- [[zhang2026touchguide]]
- [[zhang2026world2minecraft]]
- [[zhao2025polytouch]]
- [[zhao2026rosclaw]]
- [[zhao2026visualtactile]]
- [[zhao2026vitactracing]]
- [[zheng2026pokevla]]
- [[zhong2026vlaopd]]
- [[zhou2025oneshot]]
- [[zhou2026ego]]
- [[zhou2026rcnf]]
- [[zhou2026sim1]]
- [[zhou2026vlbiman]]
- [[zhu2024scaling]]
- [[zhu2026nsvla]]