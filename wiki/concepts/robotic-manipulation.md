---
title: "Robotic Manipulation"
tags: [concept, manipulation]
created: "2026-04-25"
updated: "2026-04-26"
type: "concept"
status: "done"
summary: "机器人操控是最顶层的概念页，涵盖从抓取到精细装配的完整操控链条，学习型方法已成为主流"
aliases: [manipulation, "robot manipulation", "robotic manipulation"]
---

## Definition

机器人操控：使机器人与物理世界交互完成任务的领域

## Key Ideas

- 关注机器人如何感知、规划并执行对物体的物理操作。
- 常见任务包括抓取、推动、插入、装配、双臂协作和灵巧手操作。
- 评价重点通常是成功率、泛化能力、接触稳定性和真实机器人可部署性。
- 学习型方法已取代手工设计成为操控策略的主流：[[chi2024diffusion]] Diffusion Policy、[[zhao2023finegrained]] ACT、[[team2024octo]] Octo 都展示了端到端学习在真实操控中的可行性。
- 大规模预训练+跨机器人泛化是当前前沿：[[collaboration2025open]] OXE+RT-X 在 22 个机器人上训练，[[kim2024openvla]] 开源 7B VLA。但精细操控和双臂协调仍是弱点。
- 从刚性物体到可变形物体的扩展正在进行：[[chen2025deformpam]]、[[li2025routing]]、[[collins2025shapespace]] 都在挑战可变形物体操控这一更难的问题。

## Method Families

- 模仿学习路径：本地有 31 篇相关文献，代表论文包括 [[chen2025coordinated]]、[[chen2025deformpam]]、[[chen2025effective]]、[[chen2025vividex]]。
- 强化学习路径：本地有 14 篇相关文献，代表论文包括 [[chen2025vividex]]、[[han2025upvital]]、[[jiang2024manipulation]]、[[karim2024davil]]。
- 视觉-语言模型路径：本地有 14 篇相关文献，代表论文包括 [[chi2024diffusion]]、[[dalal2025local]]、[[garcia2025generalizable]]、[[kim2024openvla]]。
- 扩散模型路径：本地有 12 篇相关文献，代表论文包括 [[chen2025coordinated]]、[[chen2025deformpam]]、[[chen2025vividex]]、[[chi2024diffusion]]。
- 机器人学习路径：本地有 9 篇相关文献，代表论文包括 [[chi2024diffusion]]、[[do2025watch]]、[[lee2025diffdagger]]、[[liu2025forcemimic]]。

## Key Papers

- [[chi2024diffusion]]：DDPM 条件扩散策略 + 闭环动作序列预测 + 视觉条件化 + 时序扩散 Transformer；证据：任务成功率、IoU（Push-T）、覆盖率（Sauce）。
- [[zhao2023finegrained]]：Action Chunking with Transformers (ACT)；CVAE 训练；Temporal Ensembling；证据：Task success rate (%)。
- [[fu2024mobile]]：Mobile ALOHA 硬件系统（$32k）+ 静态 ALOHA 数据 co-training + ACT/Diffusion Policy/VINN；证据：任务成功率（20 次评估），子任务成功率。
- [[team2024octo]]：Block-structured Transformer + Diffusion Action Head；在 Open X-Embodiment 上预训练；证据：任务成功率。
- [[kim2024openvla]]：开源 7B VLA（Prismatic VLM + 动作 token）；Open X-Embodiment 训练；LoRA 微调；证据：任务成功率。
- [[collaboration2025open]]：OXE 数据集（22 机器人/1M+ episodes）+ RT-X 模型家族；RLDS 统一格式；证据：任务成功率（零样本/微调）。
- [[zhu2024scaling]]：ScaleDP — AdaLN条件融合（替代cross-attention）+ 非因果自注意力 + ViT式模型配置（10M→1B）；证据：成功率（20 trials/任务），训练损失收敛曲线。
- [[zhi2025closedloop]]：COME-robot — GPT-4V + 三级开放词汇感知 + 分层闭环反馈恢复（物体/局部/全局级）；证据：成功率(SR)、步骤成功率(SSR)、恢复率(RR)。
- [[zhao2025polytouch]]：PolyTouch三模态传感器（VHB/硅胶弹性体+荧光照明+曲面镜）+ Tactile-Diffusion Policy（T3+CLIP+AST+Cross-At...；证据：平均任务进度（3-7阶段）、平均任务成功率、弹性体耐久性（小时）。
- [[zhang2025tissue]]：外部永磁体(UR16e)操控体内磁夹，YOLO V5+PCA角度检测，改进最速下降导航算法；证据：操控时间（最大/最小/平均）、角度误差、末端执行器轨迹。

## Evidence Map

- 本地证据规模：当前概念页连接 79 篇 literature notes，其中 79 篇为 `status: done`。
- 代表性证据链：[[chi2024diffusion]]、[[zhao2023finegrained]]、[[fu2024mobile]]、[[team2024octo]]、[[kim2024openvla]]。
- 主要交叉主题：模仿学习(31)、强化学习(14)、视觉-语言模型(14)、扩散模型(12)、机器人学习(9)。
- 可核查实验结果主要来自：[[chi2024diffusion]]、[[zhao2023finegrained]]、[[fu2024mobile]]、[[team2024octo]]、[[kim2024openvla]]；回答具体性能问题时应回到这些论文笔记核对指标。

## Open Problems

- [[chi2024diffusion]] 暴露的限制：继承行为克隆局限（需充足演示数据）；推理延迟高于简单方法（如 LSTM-GMM）；不适合极高频控制任务。
- [[zhao2023finegrained]] 暴露的限制：多指操作/大力矩任务硬件不足；Thread Velcro 等感知困难任务成功率低；每任务需 50 演示单独训练。
- [[fu2024mobile]] 暴露的限制：占地面积大（90x135cm）；固定手臂高度限制低处操作；仅单任务学习；Cook Shrimp（长时域）成功率低。
- [[team2024octo]] 暴露的限制：控制频率 ~6Hz（不如 ALOHA 的 50Hz）；双臂任务零样本性能有限；仅用 RGB 不用深度；预训练计算量大。
- [[kim2024openvla]] 暴露的限制：控制频率 ~6Hz；仅支持单臂；动作离散化损失精度；不支持双臂。
- [[collaboration2025open]] 暴露的限制：数据质量不均匀；某些数据集任务单一；缺乏精细操控数据；动作空间统一化有精度损失。

## Related Concepts

- [[deformable-linear-object]]
- [[grasping]]
- [[vision-language-model]]
- [[imitation-learning]]
- [[bimanual-manipulation]]
- [[reinforcement-learning]]
- [[diffusion-model]]
- [[robot-learning]]
- [[sim-to-real]]
- [[planning]]
- [[tactile-sensing]]
- [[flow-matching]]
- [[dynamical-systems]]
- [[collision-avoidance]]
- [[test-time-scaling]]
- [[contact-implicit-trajectory-optimization]]
- [[trajectory-optimization]]
- [[physical-reasoning]]
## Related Papers

- [[Reactive Motion Generation via Phase-varying Neural Potential Functions]]
- [[aida2026cortex]]
- [[antonova2021bayesian]]
- [[baumeister2025incremental]]
- [[blancomulero2024benchmarking]]
- [[boerdijk2025autonomous]]
- [[chang2026partially]]
- [[chen2025benchmarking]]
- [[chen2025coordinated]]
- [[chen2025deformpam]]
- [[chen2025effective]]
- [[chen2025vegetable]]
- [[chen2025vividex]]
- [[chen2026abotphysworld]]
- [[chen2026adacleargrasp]]
- [[chen2026craft]]
- [[chen2026elasticflow]]
- [[chen2026lastr1]]
- [[chen2026posterior]]
- [[chen2026ropa]]
- [[chen2026rotridiff]]
- [[chi2024diffusion]]
- [[chuang2025active]]
- [[collaboration2025open]]
- [[collins2025shapespace]]
- [[consortium2026openhembodiment]]
- [[cui2026aharobot]]
- [[dai2024racer]]
- [[dalal2025local]]
- [[das2026dart]]
- [[deshpande2026molmob0t]]
- [[do2025watch]]
- [[dong2025vitavla]]
- [[dong2026faster]]
- [[du2024embedded]]
- [[du2026bioprovlaagent]]
- [[fan2026xr1]]
- [[fang2026dexdrummer]]
- [[fang2026force]]
- [[feng2026demystifying]]
- [[feng2026see]]
- [[fu2024mobile]]
- [[fu2026capx]]
- [[funk2024evetac]]
- [[gao2024prime]]
- [[gao2025must]]
- [[gao2026driftbased]]
- [[garcia2025generalizable]]
- [[george2024vital]]
- [[ghosh2026reducing]]
- [[giacomuzzo2024blackbox]]
- [[grotz2025twin]]
- [[gu2026refinedp]]
- [[gu2026vistabot]]
- [[guan2026dssp]]
- [[guzey2025bridging]]
- [[haldar2026point]]
- [[han2025upvital]]
- [[han2026stereopolicy]]
- [[hartz2024art]]
- [[he2026exploratory]]
- [[hu2026arvla]]
- [[huang2025match]]
- [[huang2026kinder]]
- [[huang2026mimic]]
- [[iek2026coral]]
- [[jauhri2026wholebody]]
- [[ji2026recovering]]
- [[jia2026dreamplan]]
- [[jia2026gsplayground]]
- [[jiang2024manipulation]]
- [[jiang2026world4rl]]
- [[jin2026grounding]]
- [[kang2026coenv]]
- [[kappel2026qdtraj]]
- [[karim2024davil]]
- [[kim2024openvla]]
- [[kordia2025optimize]]
- [[kumar122constraining]]
- [[kuroki2025gendom]]
- [[lee2025diffdagger]]
- [[levy2026simulation]]
- [[li2025routing]]
- [[li2026affordsim]]
- [[li2026egolive]]
- [[li2026forcevla2]]
- [[li2026gazevla]]
- [[li2026h2r]]
- [[li2026hierarchical]]
- [[li2026impact]]
- [[li2026lehome]]
- [[li2026realvlgr1]]
- [[lian2026langforce]]
- [[lin2026hifvla]]
- [[lips2024keypoints]]
- [[liu2025autonomous]]
- [[liu2025forcemimic]]
- [[liu2025kuda]]
- [[liu2025oneshot]]
- [[liu2026longhorizon]]
- [[liu820enhancing]]
- [[liufu2026repovla]]
- [[longhini2026behavioral]]
- [[lu2026unified]]
- [[luijkx2026llmguided]]
- [[luo2024humanagent]]
- [[luo2026flash]]
- [[luo2026selfimproving]]
- [[ma2025running]]
- [[ma2026human]]
- [[ma2026semanticcontact]]
- [[missal2026ropedreamer]]
- [[mitrano2024grasp]]
- [[moletta2026preference]]
- [[moroncelli2026jumpstart]]
- [[mosbach2025promptresponsive]]
- [[narendra2026knowledgeguided]]
- [[nasiriany2025rtaffordance]]
- [[nazarczuk2025closed]]
- [[nie820smaller]]
- [[niu2026boosting]]
- [[niu2026versatile]]
- [[ozdamar820pushing]]
- [[pallar2025optimal]]
- [[park2026acg]]
- [[park2026demodiffusion]]
- [[patankar2025synthesizing]]
- [[patel2025realtosimtoreal]]
- [[patil2026youve]]
- [[peters2026coordinated]]
- [[puthumanaillam2026muninn]]
- [[qi2026compose]]
- [[qiu2025wildlma]]
- [[qureshi2025splatsim]]
- [[röfer2025pseudotouch]]
- [[saad2026hybrid]]
- [[sagar2026robomd]]
- [[scheikl620movement]]
- [[schperberg2026mobius]]
- [[sha2026efficient]]
- [[shah2025acoustic]]
- [[shi2025zeromimic]]
- [[shi2026agile]]
- [[singh2025handobject]]
- [[singh2025intellirms]]
- [[smith2024steer]]
- [[so2025evaluating]]
- [[spieler2026slotmpc]]
- [[steen2024quadratic]]
- [[styrud2025automatic]]
- [[sun2026maniparena]]
- [[sundaralingam2026curobov2]]
- [[tang2025kalie]]
- [[tang2025uad]]
- [[team2024octo]]
- [[tong2024ovalprompt]]
- [[tong2026uncovering]]
- [[tu2026embody4d]]
- [[vo2026codegraphvlp]]
- [[wang2023hierarchical]]
- [[wang2023multistage]]
- [[wang2025implicit]]
- [[wang2026adagamma]]
- [[wang2026beyond]]
- [[wang2026discretertc]]
- [[wang2026evolvable]]
- [[wang2026ocra]]
- [[wang2026offline]]
- [[wang2026phys2real]]
- [[wang2026radar]]
- [[wang2026vlathinker]]
- [[wang2026while]]
- [[wei2026libravla]]
- [[wu2025discrete]]
- [[wu2025imperfect]]
- [[wu2025rlgsbridge]]
- [[wu2025tacdiffusion]]
- [[wu2026continually]]
- [[wu2026large]]
- [[xia2024cage]]
- [[xiao2026avavla]]
- [[xiao2026m2vla]]
- [[xiao2026worldenv]]
- [[xie102multiview]]
- [[xie2026humanintention]]
- [[xu2026expertgen]]
- [[xu2026fingereye]]
- [[xu2026movethenoperate]]
- [[xu2026r2rgen]]
- [[xu2026token]]
- [[xu2026twinrlvla]]
- [[xue2026tube]]
- [[yan2026tac2real]]
- [[yang2026hivla]]
- [[yang2026rise]]
- [[yang2026twintrack]]
- [[yang2026ultradexgrasp]]
- [[ye2026reinforcement]]
- [[yin2026genie]]
- [[yokomizo2026physquantagent]]
- [[yuan2026embodiedr1]]
- [[yuan2026prefmoe]]
- [[zhang2021dair]]
- [[zhang2025tissue]]
- [[zhang2026forceflow]]
- [[zhang2026joyaira]]
- [[zhang2026prts]]
- [[zhang2026safevla]]
- [[zhang2026touchguide]]
- [[zhang2026visionlanguageaction]]
- [[zhao2023finegrained]]
- [[zhao2025polytouch]]
- [[zhao2026rosclaw]]
- [[zhao2026visualtactile]]
- [[zhao2026vitactracing]]
- [[zheng120dottip]]
- [[zheng2026pokevla]]
- [[zhi102unifying]]
- [[zhi2025closedloop]]
- [[zhong2026vlaopd]]
- [[zhou2025oneshot]]
- [[zhou2026ego]]
- [[zhou2026rcnf]]
- [[zhou2026sim1]]
- [[zhou2026vlbiman]]
- [[zhu2024scaling]]
- [[zhu2026nsvla]]
- [[ziakas2026aligning]]