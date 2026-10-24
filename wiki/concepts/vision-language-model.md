---
title: "Vision-Language Model"
tags: [concept, VLM]
created: "2026-04-25"
updated: "2026-04-26"
type: "concept"
status: "done"
summary: "VLM 在机器人中的核心价值是开放词汇感知和任务分解，但空间精度和实时性仍是部署瓶颈"
aliases: [VLM, "vision-language model", "vision language model"]
---

## Definition

视觉-语言模型：融合视觉和语言理解的多模态模型

## Key Ideas

- VLM 在机器人中的价值链是：语言指令 → 开放词汇感知 → affordance/关键点推理 → 任务分解 → 奖励/目标生成。[[zhi2025closedloop]] 的三级感知+闭环恢复是这条链的完整实现。
- VLA（Vision-Language-Action）模型试图端到端地桥接 VLM 和控制，但存在"语言精度 vs 动作精度"的根本矛盾：[[brohan2023rt2]] 将动作离散化为文本 token（1-3Hz），[[kim2024openvla]] 用 7B 参数仅达 ~6Hz，都不适合需要 50Hz 的精细操控。
- 关键点/affordance 是 VLM 与低层控制的优雅接口：[[liu2025kuda]] 用关键点统一 VLM 和动力学学习（80% 总成功率），[[tang2025kalie]] 用 affordance-aware 合成数据微调 VLM。
- VLM 最强的应用是**任务分解和失败恢复**，而非直接动作生成：[[styrud2025automatic]] 用 LLM 解释目标+解决失败，[[dalal2025local]] 用 GPT-4o 分解长时序任务，[[zhi2025closedloop]] 用 GPT-4V 做分层闭环恢复。
- STEER 展示了 VLM 引导的密集语言标注对机器人策略的价值：[[smith2024steer]] 用 RT-1+VLM/人类编排实现策略可引导性，是 VLM 作为策略监督信号的先驱工作。

## Method Families

- **VLA 端到端模型**：VLM 直接输出动作。[[brohan2023rt2]] RT-2（55-305B）；[[kim2024openvla]] OpenVLA（7B，开源）；[[dey2025revla]] ReVLA。控制频率低，不适合高频任务。
- **VLM 任务规划**：VLM 做高层规划，底层执行由专用策略负责。[[zhi2025closedloop]] GPT-4V+三级闭环；[[styrud2025automatic]] LLM+PDDL+BT；[[singh2025intellirms]] LLM+行为树。模块化但依赖预定义技能。
- **VLM 奖励/目标生成**：VLM 为 RL/规划器生成奖励函数。[[patel2025realtosimtoreal]] IKER（VLM→关键点奖励→PPO）；[[liu2025kuda]] KUDA（VLM→关键点目标→MPPI）。是 VLM+sim-to-real 的桥梁。
- **VLM Affordance 推理**：VLM 预测物体上的操作区域/关键点。[[tang2025uad]] UAD（DINOv2+GPT-4o+FiLM）；[[tang2025kalie]] KALIE（ControlNet 合成+CogVLM 微调）；[[nasiriany2025rtaffordance]]。
- **VLM 引导的感知/操控**：VLM 做开放词汇检测和位姿估计。[[dalal2025local]] GPT-4o+SAM；[[ryu2025curricullm]] LLM 课程学习。

## Key Papers

- [[brohan2023rt2]]：RT-2 开创了 VLA 范式，将动作表示为文本 token。证明了 VLM 知识可迁移到机器人操控，但控制频率 1-3Hz 且模型巨大（55-305B）限制了实际部署。
- [[kim2024openvla]]：首个开源 7B VLA。Prismatic VLM+动作 token+LoRA 微调，使 VLA 可在单 GPU 上训练。但 ~6Hz 和单臂限制仍是瓶颈。
- [[zhi2025closedloop]]：COME-robot 实现了 VLM 驱动的三级闭环恢复（物体/局部/全局级）。GPT-4V 做开放词汇感知+失败诊断+恢复规划，是 VLM 在操控中最完整的应用之一。
- [[liu2025kuda]]：KUDA 用关键点统一 VLM 和动力学学习。VLM(GPT-4o) 生成代码式目标规范→cost function→MPPI，6 任务 80% 总成功率。证明了 VLM+动力学的可行性。
- [[styrud2025automatic]]：BETR-XP-LLM 用 LLM 自动生成和扩展行为树。目标解释 Easy/Medium 100%，失败场景 10/10 正确识别。ABB YuMi 双臂验证。
- [[tang2025uad]]：UAD 用 DINOv2+GPT-4o 实现 affordance 蒸馏到 FiLM 解码器，affordance 作为观察辅助 IL。在 AGD20K 和真实任务上验证。
- [[tang2025kalie]]：KALIE 用 ControlNet 合成 affordance-aware 数据微调 CogVLM-17B。解决 VLM 微调数据不足的问题。
- [[singh2025intellirms]]：IntelliRMS 展示 LLM+感知+行为树在室内移动操控中的实用性。规划准确率和执行成功率的系统性评估。
- [[patel2025realtosimtoreal]]：IKER 用 VLM 生成关键点奖励函数，实现 Real-to-Sim-to-Real 循环。是 VLM 辅助 sim-to-real 的代表。
- [[dalal2025local]]：ManipGen 用 GPT-4o 做任务分解+SAM 感知，50 真实任务 76% 成功率。VLM 在大规模长时序操控中的系统验证。

## Evidence Map

- **本地证据规模**：32 篇 status:done 文献，覆盖 VLA（3 篇）、任务规划（5 篇）、奖励生成（3 篇）、affordance（3 篇）、感知/操控（18 篇）。
- **强证据问题**（本地证据充分支持）：
  - VLA 的控制频率和部署限制：RT-2 和 OpenVLA 有详细定量数据。
  - VLM 任务分解+层次规划的实用性：[[styrud2025automatic]]、[[zhi2025closedloop]]、[[dalal2025local]] 有完整的真实世界验证。
  - 关键点作为 VLM-控制接口的有效性：[[liu2025kuda]] 有消融实验。
- **弱证据问题**（本地证据不足或缺失）：
  - VLM 在 DLO 操控场景中的表现（仅 [[liu2025kuda]] 的 rope straightening）。
  - VLM 的实时性改进方案（本地无专门文献讨论如何将 VLM 推理降至 <100ms）。
  - VLM 幻觉对机器人安全的定量影响。

## Open Problems

- **VLM 空间精度不足**：VLM 擅长语义理解但对精确 3D 空间推理有限。[[zhi2025closedloop]] 的 GPT-4V 误检、[[liu2025kuda]] 的感知错误 10% 都暴露了这个问题。DLO 操控需要毫米级精度，VLM 尚无法满足。
- **VLM + DLO 操控**：本地仅 [[liu2025kuda]] 在 rope straightening 上验证，DLO 的连续变形、自遮挡和接触动力学远超 VLM 的感知能力。需要新的中间表示。
- **VLA 控制频率 vs 精度的权衡**：[[brohan2023rt2]] 1-3Hz、[[kim2024openvla]] ~6Hz 都远低于 ALOHA 的 50Hz。如何在不损失语言理解能力的前提下提升控制频率？
- **VLM 在双臂场景的角色**：当前 VLA 仅支持单臂。VLM 能否为双臂协调提供有用的角色分配和时序规划？[[styrud2025automatic]] 在 YuMi 上的验证是初步尝试。

## Related Concepts

- [[deformable-linear-object]]
- [[robotic-manipulation]]
- [[imitation-learning]]
- [[grasping]]
- [[reinforcement-learning]]
- [[bimanual-manipulation]]
- [[diffusion-model]]
- [[robot-learning]]
- [[sim-to-real]]
- [[planning]]
- [[tactile-sensing]]
- [[flow-matching]]
- [[collision-avoidance]]
- [[test-time-scaling]]
- [[dynamical-systems]]
- [[proximity-sensing]]
- [[novel-view-synthesis]]
- [[physical-reasoning]]
## Related Papers

- [[Reactive Motion Generation via Phase-varying Neural Potential Functions]]
- [[aida2026cortex]]
- [[ao2025llmasbtplanner]]
- [[bang2026environmental]]
- [[brohan2023rt2]]
- [[chang2026partially]]
- [[chen2025benchmarking]]
- [[chen2025coordinated]]
- [[chen2025deformpam]]
- [[chen2026abotphysworld]]
- [[chen2026adacleargrasp]]
- [[chen2026craft]]
- [[chen2026elasticflow]]
- [[chen2026lastr1]]
- [[chen2026posterior]]
- [[chen2026ropa]]
- [[chi2024diffusion]]
- [[choi2026rankq]]
- [[consortium2026openhembodiment]]
- [[cui2026aharobot]]
- [[dai2024racer]]
- [[dalal2025local]]
- [[deshpande2026molmob0t]]
- [[dey2025revla]]
- [[dong2025vitavla]]
- [[dong2026faster]]
- [[du2026bioprovlaagent]]
- [[enwerem2026variational]]
- [[fan2026xr1]]
- [[fang2026force]]
- [[feng2026demystifying]]
- [[feng2026see]]
- [[fu2026capx]]
- [[gao2026driftbased]]
- [[garcia2025generalizable]]
- [[george2024vital]]
- [[ghosh2026reducing]]
- [[guan2026dssp]]
- [[haldar2026point]]
- [[han2026stereopolicy]]
- [[he2026exploratory]]
- [[he2026generative]]
- [[hou2026world]]
- [[hu2026arvla]]
- [[huang2026flexitac]]
- [[huang2026kinder]]
- [[huang2026mimic]]
- [[iek2026coral]]
- [[jeong2026your]]
- [[ji2026recovering]]
- [[jia2026dreamplan]]
- [[jia2026gsplayground]]
- [[jiang2024manipulation]]
- [[jiang2026blockr1]]
- [[jiang2026break]]
- [[jiang2026videop2r]]
- [[jie2026omnivlarl]]
- [[jin2026grounding]]
- [[kang2026coenv]]
- [[keunknowndiffuser]]
- [[khan2026discrete]]
- [[kim2024openvla]]
- [[kim2026agenticcache]]
- [[kohlbrenner2026egocentric]]
- [[lee2025diffdagger]]
- [[lee2026implicit]]
- [[lee2026modular]]
- [[levy2026simulation]]
- [[li2026affordsim]]
- [[li2026egolive]]
- [[li2026ets]]
- [[li2026forcevla2]]
- [[li2026gazevla]]
- [[li2026h2r]]
- [[li2026hierarchical]]
- [[li2026hpedit]]
- [[li2026realvlgr1]]
- [[lian2026langforce]]
- [[liang2026vanim]]
- [[lin2026hifvla]]
- [[liu2025forcemimic]]
- [[liu2025kuda]]
- [[liu2026longhorizon]]
- [[liu820enhancing]]
- [[liufu2026repovla]]
- [[longhini2026behavioral]]
- [[lu2026unified]]
- [[luijkx2026llmguided]]
- [[luo2026selfimproving]]
- [[ma2025running]]
- [[ma2026human]]
- [[ma2026semanticcontact]]
- [[moroncelli2026jumpstart]]
- [[mosbach2025promptresponsive]]
- [[narendra2026knowledgeguided]]
- [[nazarczuk2025closed]]
- [[niu2026boosting]]
- [[niu2026versatile]]
- [[ortegakral2026rio]]
- [[park2026acg]]
- [[patel2025realtosimtoreal]]
- [[peters2026coordinated]]
- [[puthumanaillam2026muninn]]
- [[qi2026compose]]
- [[qiu2025wildlma]]
- [[ryu2025curricullm]]
- [[saad2026hybrid]]
- [[sagar2026robomd]]
- [[sakamoto2026e3vsbench]]
- [[schperberg2026mobius]]
- [[shen2026plan]]
- [[shi2026agile]]
- [[singh2025intellirms]]
- [[smith2024steer]]
- [[stambaugh2026mixeddensity]]
- [[styrud2025automatic]]
- [[sun2026maniparena]]
- [[sundaralingam2026curobov2]]
- [[tan2026fsunav]]
- [[tang2025kalie]]
- [[tang2025uad]]
- [[tong2024ovalprompt]]
- [[tong2026uncovering]]
- [[vo2026codegraphvlp]]
- [[wang2025vlaadapter]]
- [[wang2026adagamma]]
- [[wang2026any2any]]
- [[wang2026beyond]]
- [[wang2026discretertc]]
- [[wang2026evolvable]]
- [[wang2026ocra]]
- [[wang2026offline]]
- [[wang2026phys2real]]
- [[wang2026radar]]
- [[wang2026stepnft]]
- [[wang2026visionlanguageaction]]
- [[wang2026vlathinker]]
- [[wang2026while]]
- [[wei2026libravla]]
- [[wei2026navol]]
- [[wu2025discrete]]
- [[wu2025imperfect]]
- [[wu2026affordgrasp]]
- [[wu2026continually]]
- [[wu2026contrastive]]
- [[wu2026large]]
- [[xiao2026avavla]]
- [[xiao2026m2vla]]
- [[xiao2026worldenv]]
- [[xie2026humanintention]]
- [[xu2026expertgen]]
- [[xu2026movethenoperate]]
- [[xu2026roboagent]]
- [[xu2026token]]
- [[xu2026twinrlvla]]
- [[xue2026tube]]
- [[yang2026asyncshield]]
- [[yang2026hivla]]
- [[yang2026physforge]]
- [[yang2026rise]]
- [[ye2026generation]]
- [[ye2026reinforcement]]
- [[yin2026genie]]
- [[yin2026multiple]]
- [[yokomizo2026physquantagent]]
- [[yuan2026embodiedr1]]
- [[yuan2026prefmoe]]
- [[zeng2026recapa]]
- [[zhang2026forceflow]]
- [[zhang2026generative]]
- [[zhang2026handx]]
- [[zhang2026joyaira]]
- [[zhang2026prts]]
- [[zhang2026recurrent]]
- [[zhang2026safevla]]
- [[zhang2026touchguide]]
- [[zhang2026visionlanguageaction]]
- [[zhang2026world2minecraft]]
- [[zhao2023finegrained]]
- [[zhao2025polytouch]]
- [[zhao2026rosclaw]]
- [[zhao2026vitactracing]]
- [[zheng2026pokevla]]
- [[zhi2025closedloop]]
- [[zhong2026vlaopd]]
- [[zhou2026characterizing]]
- [[zhou2026ego]]
- [[zhou2026rcnf]]
- [[zhou2026vlbiman]]
- [[zhu2024scaling]]
- [[zhu2026nsvla]]
- [[ziakas2026aligning]]