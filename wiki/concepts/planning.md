---
title: "Planning"
tags: [concept, planning]
created: "2026-04-25"
updated: "2026-04-26"
type: "concept"
status: "done"
summary: "机器人规划正从传统几何/运动学规划向学习型+语言引导规划演化，核心挑战是长时序、安全性和失败恢复"
aliases: [planning, "motion planning", "task planning"]
---

## Definition

运动规划：在任务、几何和动力学约束下生成可执行机器人行为的过程

## Key Ideas

- 规划负责把高层目标转成可执行动作序列或轨迹。
- 常与学习策略结合，用于处理长时序、约束和安全性。
- 机器人场景中要同时考虑可达性、碰撞、接触、实时性和失败恢复。
- LLM 正在成为任务规划的通用接口：[[styrud2025automatic]] 用 LLM+PDDL 自动生成行为树，[[singh2025intellirms]] 用 LLM+行为树控制移动操控。但 LLM 的可靠性依赖于 few-shot 示例质量。
- 闭环规划是实用性关键：[[zhi2025closedloop]] 的三级闭环恢复、[[nazarczuk2025closed]] 的每帧重规划都证明了开环规划在真实场景中不可行。
- 形式化安全约束开始融入规划：[[pallar2025optimal]] 用 CBF+凸多面体建模保证避碰安全性。但 DLO 场景的连续变形使得传统碰撞检测失效。

## Method Families

- 机器人操控路径：本地有 32 篇相关文献，代表论文包括 [[baumeister2025incremental]]、[[chen2025effective]]、[[chi2024diffusion]]、[[chuang2025active]]。
- 视觉-语言模型路径：本地有 12 篇相关文献，代表论文包括 [[ao2025llmasbtplanner]]、[[chi2024diffusion]]、[[dalal2025local]]、[[garcia2025generalizable]]。
- 模仿学习路径：本地有 11 篇相关文献，代表论文包括 [[chen2025effective]]、[[chi2024diffusion]]、[[chuang2025active]]、[[gao2024prime]]。
- 扩散模型路径：本地有 5 篇相关文献，代表论文包括 [[chi2024diffusion]]、[[lee2025diffdagger]]、[[li2025routing]]、[[wang2025transdiff]]。
- 强化学习路径：本地有 5 篇相关文献，代表论文包括 [[karim2024davil]]、[[li2025routing]]、[[liu820enhancing]]、[[wang2023hierarchical]]。

## Key Papers

- [[chi2024diffusion]]：DDPM 条件扩散策略 + 闭环动作序列预测 + 视觉条件化 + 时序扩散 Transformer；证据：任务成功率、IoU（Push-T）、覆盖率（Sauce）。
- [[zhi2025closedloop]]：COME-robot — GPT-4V + 三级开放词汇感知 + 分层闭环反馈恢复（物体/局部/全局级）；证据：成功率(SR)、步骤成功率(SSR)、恢复率(RR)。
- [[zhang2025tissue]]：外部永磁体(UR16e)操控体内磁夹，YOLO V5+PCA角度检测，改进最速下降导航算法；证据：操控时间（最大/最小/平均）、角度误差、末端执行器轨迹。
- [[wu2025tacdiffusion]]：TacDiffusion — DDPM 6D wrench 输出 + 动态系统滤波器 + 阻抗控制前馈力；证据：成功率（零样本迁移平均 95.7%）+ 执行时间。
- [[wang2025transdiff]]：TransDiff — DDPM + 多条件引导（语义/边缘/法线）+ RVCDB 损失；证据：RMSE/MAbs（深度）+ 抓取成功率（仿真 87.5%）。
- [[tang2025kalie]]：KALIE — ControlNet affordance-aware 合成 + CogVLM-17B LoRA 微调 + 关键点 affordance；证据：任务成功率 (15 trials × 3 物体集) + MSE 关键点预测。
- [[styrud2025automatic]]：BETR-XP-LLM — LLM 目标解释 + PDDL 规划器 + LLM 失败解决 + BT 永久更新；证据：目标解释准确率 + 失败场景解决率 + 参数推理合理性。
- [[so2025evaluating]]：联网电子任务板 + 自动遥测 + 比赛模式；证据：执行时间 + 完成任务数 + 成功率。
- [[singh2025intellirms]]：IntelliRMS — LLM 任务规划 + Mask R-CNN 感知 + 行为树控制；证据：规划准确率 + 执行成功率 + 延迟。
- [[qiu2025wildlma]]：WildLMa — VR 遥操作 + CLIP 交叉注意力 IL + 层次化 LLM 规划；证据：单技能成功率 + 长时序任务成功率。

## Evidence Map

- 本地证据规模：当前概念页连接 34 篇 literature notes，其中 34 篇为 `status: done`。
- 代表性证据链：[[chi2024diffusion]]、[[zhi2025closedloop]]、[[zhang2025tissue]]、[[wu2025tacdiffusion]]、[[wang2025transdiff]]。
- 主要交叉主题：机器人操控(32)、视觉-语言模型(12)、模仿学习(11)、扩散模型(5)、强化学习(5)。
- 可核查实验结果主要来自：[[chi2024diffusion]]、[[zhi2025closedloop]]、[[zhang2025tissue]]、[[wu2025tacdiffusion]]、[[wang2025transdiff]]；回答具体性能问题时应回到这些论文笔记核对指标。

## Open Problems

- [[chi2024diffusion]] 暴露的限制：继承行为克隆局限（需充足演示数据）；推理延迟高于简单方法（如 LSTM-GMM）；不适合极高频控制任务。
- [[zhi2025closedloop]] 暴露的限制：GPT-4V误检、抓取位置不利、API延迟成本、单环境测试。
- [[zhang2025tissue]] 暴露的限制：仅仿真（无噪声/软组织）、仅pitch角、PCA偶有误算、未做临床验证。
- [[wu2025tacdiffusion]] 暴露的限制：仅插入任务、依赖专家策略、模型大小需权衡。
- [[wang2025transdiff]] 暴露的限制：推理慢、合成数据依赖、仅抓取验证。
- [[tang2025kalie]] 暴露的限制：单臂桌面、开源 VLM 差距、仅 few-shot。

## Related Concepts

- [[deformable-linear-object]]
- [[robotic-manipulation]]
- [[vision-language-model]]
- [[imitation-learning]]
- [[grasping]]
- [[reinforcement-learning]]
- [[bimanual-manipulation]]
- [[diffusion-model]]
- [[robot-learning]]
- [[sim-to-real]]
- [[flow-matching]]
- [[tactile-sensing]]
- [[test-time-scaling]]
- [[contact-implicit-trajectory-optimization]]
- [[trajectory-optimization]]
## Related Papers

- [[aida2026cortex]]
- [[bang2026environmental]]
- [[baumeister2025incremental]]
- [[chen2026abotphysworld]]
- [[chen2026elasticflow]]
- [[das2026dart]]
- [[enwerem2026variational]]
- [[fang2026dexdrummer]]
- [[gu2026vistabot]]
- [[hou2026world]]
- [[huang2026kinder]]
- [[huang2026mimic]]
- [[iek2026coral]]
- [[jauhri2026wholebody]]
- [[jiang2026videop2r]]
- [[jiang2026world4rl]]
- [[kim2026agenticcache]]
- [[kumar122constraining]]
- [[lee2026implicit]]
- [[levy2026simulation]]
- [[li2026ets]]
- [[li2026hierarchical]]
- [[li2026impact]]
- [[liang2026vanim]]
- [[liu2026longhorizon]]
- [[luijkx2026llmguided]]
- [[luo2026selfimproving]]
- [[missal2026ropedreamer]]
- [[mitrano2024grasp]]
- [[narendra2026knowledgeguided]]
- [[puthumanaillam2026muninn]]
- [[saad2026hybrid]]
- [[sakamoto2026e3vsbench]]
- [[schperberg2026mobius]]
- [[shah2025acoustic]]
- [[spieler2026slotmpc]]
- [[stambaugh2026mixeddensity]]
- [[sundaralingam2026curobov2]]
- [[tan2026fsunav]]
- [[tu2026embody4d]]
- [[vo2026codegraphvlp]]
- [[wang2026adagamma]]
- [[wang2026any2any]]
- [[wang2026beyond]]
- [[wei2026libravla]]
- [[wei2026navol]]
- [[wu2026continually]]
- [[xu2026roboagent]]
- [[yang2026ultradexgrasp]]
- [[yu2026atrs]]
- [[yuan2026prefmoe]]
- [[zeng2026recapa]]
- [[zhang2026prts]]
- [[zhou2025oneshot]]
- [[zhou2026rcnf]]