---
title: "Deformable Linear Object"
tags: [concept, DLO]
created: "2026-04-25"
updated: "2026-04-26"
type: "concept"
status: "done"
summary: "DLO 操控的核心矛盾是形状精度与鲁棒性的权衡，方法路线从基于模型到 RL/扩散策略到 VLM 引导逐步演化"
aliases: [DLO, "deformable linear object", "deformable object"]
---

## Definition

可变形线性物体：绳索、线缆等一维可变形物体

## Key Ideas

- DLO 的状态空间是连续无限维的：一根绳索的形状可用粒子位置序列描述，但真实世界中遮挡、自交和柔性变形使完整状态估计极其困难。[[collins2025shapespace]] 表明即使是物体级变形建模，统一潜在表示也需要超网络条件化才能跨物体泛化。
- 操控核心矛盾是"形状精度 vs 鲁棒性"：基于模型的方法（Jacobian、PDE）在已知参数下精确，但物理参数未知时崩溃；学习方法（RL、扩散策略）鲁棒但精度不足。[[liu2025autonomous]] 的 RLAC 框架通过 RL→Jacobian 切换首次尝试调和这一矛盾。
- 接触动力学是 DLO 操控的隐藏瓶颈：[[li2025routing]] 证明摩擦随机化（0.12–1.2）可将高摩擦场景成功率提升 44%，说明摩擦建模是 sim-to-real 的关键因素。
- VLM 为 DLO 操控提供了新的任务规范路径：[[liu2025kuda]] 用关键点作为 VLM 与动力学模型的桥梁，使语言指令能驱动 rope straightening 等任务，但空间推理精度仍受限于俯视视角。
- 形状表示正在从粒子/关键点转向潜在空间：[[collins2025shapespace]] 的 Shape-Space Deformer 和 [[wang2025implicit]] 的轨迹图都暗示，直接在高维粒子空间操作不如学习紧凑的物理感知潜空间。

## Method Families

- **基于模型的操控**：利用物理先验（Jacobian、PDE、CBF）进行精确控制。[[liu2025autonomous]] 用 Jacobian-based adaptive control 实现精确收敛（91/100 真实成功率）；[[pallar2025optimal]] 用 CBF+凸多面体建模保证避碰安全性；[[shah2025acoustic]] 用 latent PDE+MPC 控制波传播。共同限制是依赖已知/可辨识的物理参数。
- **RL + Sim-to-Real**：在仿真中训练策略并迁移。[[li2025routing]] 两阶段 SAC→Diffusion，摩擦随机化实现 gentle motion；[[liu2025autonomous]] PPO→Jacobian 初始化；[[do2025watch]] RL+变阻抗+在线蒸馏。共同挑战是接触建模精度和 sim-to-real gap。
- **扩散策略 / 模仿学习**：从专家演示学习多模态动作分布。[[chen2025coordinated]] 分解为状态预测扩散+逆动力学模型；[[chen2025deformpam]] 用偏好学习引导扩散策略的 action selection；[[scheikl620movement]] 用于运动规划。适合数据充足但奖励难设计的场景。
- **VLM/语言引导操控**：用 VLM 提供开放词汇目标规范。[[liu2025kuda]] 关键点+GPT-4o 代码生成+MPPI；[[qiu2025wildlma]] VR 遥操作+LLM 层次规划；[[dalal2025local]] GPT-4o 任务分解+局部策略。在 DLO 场景中仍局限于简单形状任务。
- **形状表示与感知**：解决 DLO 状态估计问题。[[collins2025shapespace]] 统一潜在表示+超网络；[[wang2025implicit]] 隐式物理感知+轨迹图 SysID；[[nazarczuk2025closed]] 场景图+物理属性测量。这是所有下游操控任务的基础。

## Key Papers

- [[li2025routing]]：DLO routing 的代表性工作。两阶段 RL→Diffusion 框架揭示了摩擦随机化和过度拉伸惩罚对 gentle motion 的关键作用，是当前唯一在高摩擦场景验证的 DLO 布线方法。
- [[wang2025implicit]]：首次系统研究软体工具（绳索）动态操控刚体。隐式物理感知（短时探针 SysID + 轨迹图）为未知物理参数的 DLO 操控提供了新思路，但成功率 62.5% 说明仍有显著改进空间。
- [[liu2025kuda]]：关键点统一 VLM 和动力学学习的代表作。在 rope straightening 任务上达到 80% 总成功率（vs MOKA 13.3%），证明 VLM+动力学是 DLO 开放词汇操控的可行路径。
- [[liu2025autonomous]]：RLAC 框架首次展示 RL+经典控制的混合架构在 DLO 精确操控中的优势。RL 负责快速逼近，Jacobian AC 负责精确收敛，真实双臂 UR5 成功率 91/100。
- [[chen2025deformpam]]：DeformPAM 针对长时序可变形物体操控的分布偏移问题，用偏好学习引导扩散策略的 action selection，在绳子塑形等任务上显著提升质量。
- [[collins2025shapespace]]：Shape-Space Deformer 提出跨物体的统一变形表示，力泛化 CD 从 300.5 降至 0.872，为 DLO 形状表示提供了新的潜在空间方案。
- [[nazarczuk2025closed]]：CLIER 的神经符号闭环方法（场景图+符号程序+Transformer 动作规划）为需要物理属性测量的 DLO 交互任务提供了可解释的规划框架。
- [[chen2025coordinated]]：状态预测扩散+逆动力学模型的分解式架构，通过显式建模物体运动而非直接动作映射，更好地捕获双臂协调中的 DLO 状态变化。
- [[pallar2025optimal]]：CBF+凸多面体建模为 DLO 绕障路径提供了安全保证，是少数在 DLO 场景中引入形式化安全约束的工作。
- [[qiu2025wildlma]]：WildLMa 的 VR 遥操作+LLM 层次规划展示了 DLO 操控中遥操作数据采集和语言驱动规划的实用路径。

## Evidence Map

- **本地证据规模**：24 篇 status:done 文献，覆盖 DLO routing（3 篇）、形状表示（2 篇）、双臂协调（4 篇）、VLM 引导（3 篇）、RL/sim-to-real（4 篇）、感知/基准（8 篇）。
- **强证据问题**（本地证据充分支持）：
  - DLO routing 中摩擦随机化的效果：[[li2025routing]] 量化了 44% 的性能提升。
  - RL+经典控制混合架构的可行性：[[liu2025autonomous]] 在真实双臂上验证。
  - 扩散策略在 DLO 任务中的多模态建模能力：[[chen2025coordinated]]、[[chen2025deformpam]] 提供了系统性对比。
  - VLM+关键点作为 DLO 操控中间表示的有效性：[[liu2025kuda]] 有完整的消融实验。
- **弱证据问题**（本地证据不足或缺失）：
  - 3D DLO 操控（本地文献几乎都限制在 2D/俯视）。
  - 打结/解结任务（本地无专门文献）。
  - 长绳索（>1m）操控的 Scalability。
  - DLO 操控的闭环安全保证（仅 [[pallar2025optimal]] 涉及）。
  - 双臂 DLO 协同中的力/位姿协调定量分析（仅有定性描述）。

## Open Problems

- **3D DLO 操控**：本地文献几乎都限制在俯视/2D 场景。[[liu2025kuda]] 和 [[wang2025implicit]] 均指出俯视相机无法处理复杂 3D 空间关系。如何实现完整的 3D DLO 感知和操控是双臂 DLO 工作的前提。
- **双臂 DLO 协同的力/位协调**：本地有 [[chen2025coordinated]]、[[liu2025autonomous]]、[[li2025routing]] 涉及双臂，但没有文献系统研究双臂在 DLO 操控中的力分配和张力控制策略。
- **Sim-to-Real 中的接触建模**：[[li2025routing]] 暴露摩擦建模的关键性，[[wang2025implicit]] 暴露软体工具的隐式物理难迁移。当前仿真器（SoftGym、SOFA）的接触建模仍不够真实。
- **长时序 DLO 任务的误差恢复**：[[chen2025deformpam]] 显示分布偏移在长时序 DLO 任务中严重，[[nazarczuk2025closed]] 的闭环重规划是方向之一，但 DLO 状态不可观测使得失败检测本身就很困难。
- **VLM 在 DLO 场景中的空间精度**：[[liu2025kuda]] 总成功率 80% 但错误主要来自感知（10%），说明 VLM 对 DLO 这种细长、自遮挡物体的空间理解仍不成熟。

## Related Concepts

- [[robotic-manipulation]]
- [[vision-language-model]]
- [[imitation-learning]]
- [[grasping]]
- [[bimanual-manipulation]]
- [[reinforcement-learning]]
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
- [[contact-implicit-trajectory-optimization]]
- [[trajectory-optimization]]
- [[novel-view-synthesis]]
- [[physical-reasoning]]
## Related Papers

- [[Reactive Motion Generation via Phase-varying Neural Potential Functions]]
- [[aida2026cortex]]
- [[antonova2021bayesian]]
- [[bang2026environmental]]
- [[blancomulero2024benchmarking]]
- [[boerdijk2025autonomous]]
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
- [[chen2026rotridiff]]
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
- [[fu2026capx]]
- [[gao2026driftbased]]
- [[george2024vital]]
- [[ghosh2026reducing]]
- [[giacomuzzo2024blackbox]]
- [[grotz2025twin]]
- [[gu2026refinedp]]
- [[gu2026vistabot]]
- [[guan2026dssp]]
- [[haldar2026point]]
- [[han2026stereopolicy]]
- [[hartz2024art]]
- [[he2026exploratory]]
- [[he2026generative]]
- [[hou2026world]]
- [[hu2026arvla]]
- [[huang2026flexitac]]
- [[huang2026kinder]]
- [[huang2026mimic]]
- [[iek2026coral]]
- [[jauhri2026wholebody]]
- [[jeong2026your]]
- [[ji2026recovering]]
- [[jia2026dreamplan]]
- [[jia2026gsplayground]]
- [[jiang2026blockr1]]
- [[jiang2026break]]
- [[jiang2026videop2r]]
- [[jiang2026world4rl]]
- [[jie2026omnivlarl]]
- [[jin2026grounding]]
- [[kang2026coenv]]
- [[khan2026discrete]]
- [[kohlbrenner2026egocentric]]
- [[kumar122constraining]]
- [[kuroki2025gendom]]
- [[lee2026implicit]]
- [[levy2026simulation]]
- [[li2025routing]]
- [[li2026affordsim]]
- [[li2026ets]]
- [[li2026forcevla2]]
- [[li2026gazevla]]
- [[li2026h2r]]
- [[li2026hierarchical]]
- [[li2026hpedit]]
- [[li2026impact]]
- [[li2026lehome]]
- [[li2026realvlgr1]]
- [[lian2026langforce]]
- [[lin2026hifvla]]
- [[liu2025autonomous]]
- [[liu2025kuda]]
- [[liu2026longhorizon]]
- [[liufu2026repovla]]
- [[longhini2026behavioral]]
- [[lu2026unified]]
- [[luijkx2026llmguided]]
- [[luo2026flash]]
- [[luo2026selfimproving]]
- [[ma2025running]]
- [[ma2026human]]
- [[ma2026semanticcontact]]
- [[mahboob2026betting]]
- [[missal2026ropedreamer]]
- [[mitrano2024grasp]]
- [[moletta2026preference]]
- [[moroncelli2026jumpstart]]
- [[narendra2026knowledgeguided]]
- [[nazarczuk2025closed]]
- [[niu2026boosting]]
- [[niu2026versatile]]
- [[ortegakral2026rio]]
- [[ozdamar820pushing]]
- [[pallar2025optimal]]
- [[park2026acg]]
- [[park2026demodiffusion]]
- [[patil2026youve]]
- [[peters2026coordinated]]
- [[puthumanaillam2026muninn]]
- [[qi2026compose]]
- [[qiu2025wildlma]]
- [[saad2026hybrid]]
- [[sagar2026robomd]]
- [[sakamoto2026e3vsbench]]
- [[scheikl620movement]]
- [[schperberg2026mobius]]
- [[sha2026efficient]]
- [[shah2025acoustic]]
- [[shen2026plan]]
- [[shi2026agile]]
- [[so2025evaluating]]
- [[spieler2026slotmpc]]
- [[stambaugh2026mixeddensity]]
- [[sun2026maniparena]]
- [[sundaralingam2026curobov2]]
- [[tan2026fsunav]]
- [[team2024octo]]
- [[tong2024ovalprompt]]
- [[tong2026uncovering]]
- [[tu2026embody4d]]
- [[vo2026codegraphvlp]]
- [[wang2025implicit]]
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
- [[wei2026navol]]
- [[wu2026affordgrasp]]
- [[wu2026continually]]
- [[wu2026contrastive]]
- [[wu2026large]]
- [[wu2026reliable]]
- [[xiao2026avavla]]
- [[xiao2026worldenv]]
- [[xie2026humanintention]]
- [[xu2026expertgen]]
- [[xu2026fingereye]]
- [[xu2026r2rgen]]
- [[xu2026roboagent]]
- [[xu2026token]]
- [[xu2026twinrlvla]]
- [[xue2026tube]]
- [[yan2026tac2real]]
- [[yang2026asyncshield]]
- [[yang2026automated]]
- [[yang2026hivla]]
- [[yang2026physforge]]
- [[yang2026rise]]
- [[yang2026twintrack]]
- [[yang2026ultradexgrasp]]
- [[ye2026generation]]
- [[ye2026reinforcement]]
- [[yin2026genie]]
- [[yin2026multiple]]
- [[yokomizo2026physquantagent]]
- [[you2026dotsim]]
- [[yu2026atrs]]
- [[yuan2026embodiedr1]]
- [[yuan2026prefmoe]]
- [[zeng2026recapa]]
- [[zhang2021dair]]
- [[zhang2026generative]]
- [[zhang2026handx]]
- [[zhang2026joyaira]]
- [[zhang2026prts]]
- [[zhang2026recurrent]]
- [[zhang2026safevla]]
- [[zhang2026touchguide]]
- [[zhang2026visionlanguageaction]]
- [[zhang2026world2minecraft]]
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
- [[zhu2026nsvla]]
- [[ziakas2026aligning]]