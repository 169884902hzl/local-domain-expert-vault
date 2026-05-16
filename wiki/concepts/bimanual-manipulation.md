---
title: "Bimanual Manipulation"
tags: [concept, bimanual]
created: "2026-04-25"
updated: "2026-04-26"
type: "concept"
status: "done"
summary: "双臂操控的核心挑战是时空协调与接触同步，当前方法从固定协调模式向自适应协调演化，但数据效率和成功率仍是瓶颈"
aliases: ["bimanual manipulation", "dual-arm manipulation", "two-arm manipulation"]
---

## Definition

双臂操控：通过两只机械臂协同完成单臂难以完成的接触丰富任务

## Key Ideas

- 双臂操控的核心难点不是"两个单臂"，而是**时空协调**：两臂必须在正确的时刻执行互补动作。[[grotz2025twin]] 的 TWIN 基准显示，即使最强的 PerAct-LF 在 13 个双臂任务上平均成功率仅 23.3%，说明当前方法远未解决协调问题。
- 协调类型决定方法选择：对称同步任务（推拉、搬运）适合共享策略；非对称分工任务（一臂固定一臂操作）需要显式角色分配。[[wang2025oneshot]] 提出了 4 种双臂协调范式（Act-Act/Stabilize-Act/Rearrange-Act/Rearrange-Rearrange）。
- 分解式架构优于端到端双臂策略：[[chen2025coordinated]] 证明状态预测扩散+逆动力学模型的分解架构在 Push-L 任务上达到 79.3% SR，而直接动作映射方法因"物体掉落但 action loss 小"的信号遮蔽问题而失败。
- 动作块（Action Chunking）是双臂 IL 的关键设计：[[zhao2023finegrained]] 的 ACT 通过 CVAE+Temporal Ensembling 处理多模态动作分布，[[fu2024mobile]] 的 ALOHA 系统在此基础上通过 co-training 突破单任务限制。
- 视角问题在双臂场景中尤为突出：固定相机无法同时观察双臂工作空间和接触区域。[[chuang2025active]] 的 AV-ALOHA 证明主动视觉在遮挡/精度任务上显著优于固定相机，但增加了动作空间维度。

## Method Families

- **动作块/扩散策略 IL**：从遥操作演示学习双臂协调。[[zhao2023finegrained]] ACT 开创了 action chunking 范式；[[chi2024diffusion]] 用扩散策略处理多模态动作分布；[[zhu2024scaling]] ScaleDP 将参数规模推至 1B。共同限制是需要大量演示数据且推理延迟高。
- **分解式架构**：将双臂策略分解为子模块。[[chen2025coordinated]] 状态预测+逆动力学模型；[[wang2025oneshot]] 3 阶段视觉伺服；[[wang2023hierarchical]] HCLM 层次化策略（push/pick/place 原语）。优势是模块可解释，劣势是接口设计增加工程复杂度。
- **RL/混合控制**：通过仿真训练双臂策略。[[karim2024davil]] DA-VIL 用 RL 预测阻抗参数 K；[[wang2023hierarchical]] HCLM 用 HRL 训练高层策略；[[liu2025autonomous]] RLAC 用 RL 初始化 Jacobian 再切换 AC。共同挑战是 sim-to-real gap 和采样效率。
- **VLA/通用策略**：大规模预训练的视觉-语言-动作模型。[[team2024octo]] Octo 在 OXE 上预训练含双臂数据；[[kim2024openvla]] OpenVLA 仅支持单臂（已知限制）；[[collaboration2025open]] RT-X 展示跨机器人迁移。双臂零样本性能仍然有限。
- **LLM 层次规划**：用 LLM 做任务分解，底层策略执行原子技能。[[styrud2025automatic]] BETR-XP-LLM 自动扩展行为树；[[qiu2025wildlma]] WildLMa 层次化 LLM 规划。适合长时序但依赖预定义技能库。
- **基准与系统**：[[grotz2025twin]] TWIN 仿真基准（13 任务/23 变体，自动数据生成）；[[fu2024mobile]] ALOHA/ALOHA 2 硬件系统（$32k）；[[chuang2025active]] AV-ALOHA 主动视觉系统。

## Key Papers

- [[zhao2023finegrained]]：ACT（Action Chunking with Transformers）是双臂 IL 的基础范式。CVAE 处理多模态 + Temporal Ensembling 平滑预测，在 ALOHA 硬件上验证了 10+ 双臂任务，后续大量工作以此为基线。
- [[fu2024mobile]]：Mobile ALOHA 将双臂 IL 推向移动平台。通过静态+移动 ALOHA 数据 co-training 突破单任务限制，$32k 成本使双臂系统可复制。是当前最广泛使用的双臂遥操作平台之一。
- [[chi2024diffusion]]：Diffusion Policy 证明扩散模型比 CVAE/GMM 更好地处理多模态动作分布。在 Push-T（IoU）、双臂 Sauce 任务上显著优于基线。推理延迟仍是限制。
- [[chen2025coordinated]]：分解式架构（状态预测扩散+逆动力学模型）的代表作。核心洞察是物体掉落的 state loss >> action loss，因此建模物体状态比直接建模动作更适合双臂协调。
- [[grotz2025twin]]：TWIN 基准是评估双臂操控方法的重要工具。13 任务/23 变体覆盖 prehensile/non-prehensile/混合类型。关键发现：所有方法平均成功率 <25%，双臂操控远未解决。
- [[zhu2024scaling]]：ScaleDP 将扩散策略从 10M 扩展到 1B 参数，用 AdaLN 替代 cross-attention 实现条件融合。展示了规模效应在双臂策略中的潜力。
- [[wang2025oneshot]]：ODIL 实现单样本双臂 IL，提出 4 种协调范式和 3 阶段视觉伺服。ABB YuMi 验证了零样本泛化能力。
- [[chuang2025active]]：AV-ALOHA 引入主动视觉解决双臂遮挡问题。VR 控制相机视角+ACT 学习 AV 策略，在遮挡任务上显著提升。
- [[styrud2025automatic]]：BETR-XP-LLM 用 LLM+PDDL 自动生成和扩展双臂行为树，在 ABB YuMi 上验证。是 LLM 层次规划在双臂操控中的代表性工作。
- [[wu2025discrete]]：Discrete Policy 用 VQ-VAE 量化动作 + 离散潜空间扩散，在 MT-12 任务上达 66.3%。为双臂高频控制提供了更快的推理方案。

## Evidence Map

- **本地证据规模**：32 篇 status:done 文献，覆盖硬件平台（ALOHA/YuMi/UR5e）、学习方法（IL/RL/VLA/LLM）、任务类型（刚性/可变形物体）。
- **强证据问题**（本地证据充分支持）：
  - Action Chunking vs 逐步预测在双臂 IL 中的效果：ACT/Diffusion Policy 有系统性对比。
  - 分解式架构 vs 端到端在双臂协调中的优劣：[[chen2025coordinated]] 的 Push-L 消融实验。
  - 双臂操控的基准性能和难度：[[grotz2025twin]] 提供了完整的基线评估。
  - 移动+固定数据 co-training 的效果：[[fu2024mobile]] 定量验证。
- **弱证据问题**（本地证据不足或缺失）：
  - 双臂力/力矩协调的显式建模（本地仅有 [[karim2024davil]] 的变阻抗和 [[liu2025autonomous]] 的 Jacobian AC）。
  - 双臂 DLO 操控中的张力控制和协调策略（仅有 [[chen2025coordinated]]、[[liu2025autonomous]] 涉及）。
  - 双臂操控的安全保证和碰撞避免（本地无专门文献）。
  - 超过 10 步的长时序双臂任务的闭环恢复。

## Open Problems

- **双臂时空协调的自动学习**：当前方法要么依赖大量人类演示（ACT/DP），要么依赖预定义原语（HCLM/BETR）。如何让机器人自主学习新的协调模式仍是开放问题。[[grotz2025twin]] 显示所有方法的平均成功率 <25%。
- **双臂 DLO 操控**：双臂+DLO 是本研究方向的核心场景，但本地仅有 [[chen2025coordinated]]、[[chen2025deformpam]]、[[liu2025autonomous]] 等少量工作直接涉及。两臂如何分配力/位控制以维持 DLO 张力尚未有系统研究。
- **数据效率和可扩展性**：[[zhao2023finegrained]] 每任务需 50 演示，[[chen2025coordinated]] 需 200 演示。[[wang2025oneshot]] 的单样本学习是方向之一，但精度有限（77.2%）。
- **双臂安全与碰撞避免**：两臂共享工作空间时碰撞风险高。本地文献中仅 [[pallar2025optimal]] 用 CBF 做形式化安全约束，但未在双臂场景验证。
- **VLA 模型的双臂支持**：[[kim2024openvla]] 和 [[team2024octo]] 明确指出双臂零样本性能有限，当前 VLA 架构主要针对单臂设计。

## Related Concepts

- [[robotic-manipulation]]
- [[deformable-linear-object]]
- [[grasping]]
- [[imitation-learning]]
- [[vision-language-model]]
- [[diffusion-model]]
- [[reinforcement-learning]]
- [[robot-learning]]
- [[sim-to-real]]
- [[planning]]
- [[tactile-sensing]]
- [[flow-matching]]
- [[collision-avoidance]]
- [[dynamical-systems]]
- [[novel-view-synthesis]]
## Related Papers

- [[aida2026cortex]]
- [[antonova2021bayesian]]
- [[blancomulero2024benchmarking]]
- [[chen2025benchmarking]]
- [[chen2025coordinated]]
- [[chen2025deformpam]]
- [[chen2025vegetable]]
- [[chen2026abotphysworld]]
- [[chen2026craft]]
- [[chen2026lastr1]]
- [[chen2026posterior]]
- [[chen2026ropa]]
- [[chen2026rotridiff]]
- [[chi2024diffusion]]
- [[choi2026rankq]]
- [[chuang2025active]]
- [[collaboration2025open]]
- [[cui2026aharobot]]
- [[dai2024racer]]
- [[das2026dart]]
- [[dong2025vitavla]]
- [[du2026bioprovlaagent]]
- [[fan2026xr1]]
- [[fang2026dexdrummer]]
- [[feng2026demystifying]]
- [[feng2026see]]
- [[fu2024mobile]]
- [[fu2026capx]]
- [[gao2026driftbased]]
- [[grotz2025twin]]
- [[gu2026refinedp]]
- [[guan2026dssp]]
- [[han2026stereopolicy]]
- [[he2026exploratory]]
- [[hou2026world]]
- [[hu2026arvla]]
- [[huang2026flexitac]]
- [[huang2026kinder]]
- [[jauhri2026wholebody]]
- [[jeong2026your]]
- [[ji2026recovering]]
- [[jia2026dreamplan]]
- [[jin2026grounding]]
- [[kang2026coenv]]
- [[karim2024davil]]
- [[kim2024openvla]]
- [[kordia2025optimize]]
- [[kumar122constraining]]
- [[kuroki2025gendom]]
- [[li2026affordsim]]
- [[li2026gazevla]]
- [[li2026h2r]]
- [[liu2025autonomous]]
- [[liu2025forcemimic]]
- [[liu2026longhorizon]]
- [[liufu2026repovla]]
- [[luo2026flash]]
- [[ma2025running]]
- [[ma2026human]]
- [[mahboob2026betting]]
- [[missal2026ropedreamer]]
- [[mitrano2024grasp]]
- [[moletta2026preference]]
- [[narendra2026knowledgeguided]]
- [[niu2026boosting]]
- [[niu2026versatile]]
- [[ortegakral2026rio]]
- [[pallar2025optimal]]
- [[park2026acg]]
- [[patil2026youve]]
- [[peters2026coordinated]]
- [[qiu2025wildlma]]
- [[scheikl620movement]]
- [[shi2025zeromimic]]
- [[shi2026agile]]
- [[singh2025intellirms]]
- [[so2025evaluating]]
- [[steen2024quadratic]]
- [[styrud2025automatic]]
- [[sun2026maniparena]]
- [[sundaralingam2026curobov2]]
- [[team2024octo]]
- [[tong2024ovalprompt]]
- [[tu2026embody4d]]
- [[wang2023hierarchical]]
- [[wang2023multistage]]
- [[wang2025oneshot]]
- [[wang2025vlaadapter]]
- [[wang2026evolvable]]
- [[wang2026ocra]]
- [[wang2026radar]]
- [[wang2026visionlanguageaction]]
- [[wang2026vlathinker]]
- [[wang2026while]]
- [[wu2025discrete]]
- [[wu2025imperfect]]
- [[wu2026continually]]
- [[wu2026reliable]]
- [[xiao2026avavla]]
- [[xu2026expertgen]]
- [[xu2026fingereye]]
- [[xu2026r2rgen]]
- [[xu2026roboagent]]
- [[xu2026token]]
- [[xu2026twinrlvla]]
- [[yang2026hivla]]
- [[yang2026physforge]]
- [[yang2026rise]]
- [[yang2026ultradexgrasp]]
- [[ye2026generation]]
- [[ye2026reinforcement]]
- [[yin2026multiple]]
- [[yuan2026embodiedr1]]
- [[zhang2021dair]]
- [[zhang2026generative]]
- [[zhang2026handx]]
- [[zhang2026joyaira]]
- [[zhang2026prts]]
- [[zhang2026recurrent]]
- [[zhang2026safevla]]
- [[zhang2026touchguide]]
- [[zhao2023finegrained]]
- [[zhao2025polytouch]]
- [[zhao2026rosclaw]]
- [[zhao2026visualtactile]]
- [[zhao2026vitactracing]]
- [[zheng120dottip]]
- [[zhong2026vlaopd]]
- [[zhou2025oneshot]]
- [[zhou2026ego]]
- [[zhou2026sim1]]
- [[zhou2026vlbiman]]
- [[zhu2024scaling]]