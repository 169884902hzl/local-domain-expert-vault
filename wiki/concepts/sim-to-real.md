---
title: "Sim-to-Real Transfer"
tags: [concept, sim-to-real]
created: "2026-04-25"
updated: "2026-04-26"
type: "concept"
status: "done"
summary: "Sim-to-Real 的核心张力是仿真保真度与多样性的权衡，当前三条路线——域随机化、高保真渲染、模型+RL 混合——各有适用场景但尚无统一方案"
aliases: [sim-to-real, "sim to real", simulation-to-real]
---

## Definition

仿真到真实迁移：将仿真环境训练的策略迁移到真实机器人

## Key Ideas

- Sim-to-Real 的根本矛盾是**仿真保真度 vs 多样性**：高保真仿真（3DGS 照片级渲染）缩小视觉差距但牺牲实时性和泛化范围；域随机化提升鲁棒性但可能引入不真实的行为。[[li2025routing]] 证明"多样性 > 保真度"（单层 mesh+随机材质优于更真实 mesh），但 [[qureshi2025splatsim]] 证明高保真 3DGS 渲染可实现 86.25% 零样本迁移。
- **Real-to-Sim-to-Real** 正在成为新范式：不再是纯仿真训练，而是先用真实数据构建仿真环境再训练策略。[[patel2025realtosimtoreal]] 的 IKER 用 BundleSDF 重建物体→IsaacGym 训练→真实验证，[[qureshi2025splatsim]] 用 3DGS 扫描构建仿真。
- 接触丰富的任务是 Sim-to-Real 最难的场景：物理参数（摩擦、刚度、阻尼）的仿真建模仍不精确。[[li2025routing]] 的摩擦随机化（0.12–1.2）是关键策略，[[do2025watch]] 的变阻抗控制在仿真和真实中使用相同控制接口以缩小 gap。
- **模型+RL 混合**在 sim-to-real 中表现突出：[[marougkas2025integrating]] 用势场模型策略+残差 RL（仅稀疏奖励），训练 2-3h 即超越纯 RL 方法 IndustReal；[[liu2025autonomous]] 用 RL 初始化 Jacobian 再切换 AC。
- PseudoTouch 代表了一种仿真缺失时的替代方案思路：[[röfer2025pseudotouch]] 用深度 patch 预测触觉信号，绕过了触觉仿真建模的困难。类似的思路可扩展到其他难以仿真的传感器模态。

## Method Families

- **域随机化 + RL**：在仿真中随机化物理/视觉参数提升策略鲁棒性。[[li2025routing]] 摩擦随机化+拉伸惩罚；[[liu2025autonomous]] PPO+域随机化；[[dalal2025local]] 3500+ RL 专家蒸馏。策略鲁棒但可能过度保守。
- **高保真渲染**：用照片级渲染缩小视觉域差距。[[qureshi2025splatsim]] 3DGS 渲染（86.25% 零样本迁移）；[[wu2025rlgsbridge]] Soft Mesh Binding GS（抓取 avg↓6.6%）。渲染速度是瓶颈（~9.3 FPS）。
- **模型+RL 混合**：用经典控制先验引导 RL 策略。[[marougkas2025integrating]] 势场+残差 RL；[[liu2025autonomous]] RL→Jacobian 切换；[[do2025watch]] RL+变阻抗+在线蒸馏。训练效率高且 sim-to-real 稳定。
- **自监督/质量评估**：不直接迁移策略，而是评估迁移质量。[[wu2025imperfect]] SSDF 用自监督预训练+质量分数加权 BC；[[yang2025simtoreal]] SMMS 级联解决运动模糊引起的感知退化。
- **Real-to-Sim-to-Real**：从真实场景构建仿真再训练。[[patel2025realtosimtoreal]] VLM 生成奖励+BundleSDF 重建；[[qureshi2025splatsim]] 3DGS 扫描。需要真实场景扫描但无需人工标注奖励。

## Key Papers

- [[qureshi2025splatsim]]：SplatSim 是高保真渲染路线的代表作。用 3DGS 替代 mesh 作为渲染原语，零样本 Sim2Real 平均 86.25%（vs real2real 97.5%），证明视觉保真度的重要性。
- [[patel2025realtosimtoreal]]：IKER 提出 Real-to-Sim-to-Real 完整循环。VLM 生成关键点奖励函数→IsaacGym PPO 训练→真实部署，无需真实演示。是 VLM 辅助 sim-to-real 的先驱。
- [[marougkas2025integrating]]：势场+残差 RL 混合架构的代表作。2-3h 训练超越纯 RL（IndustReal 8-10h），真实 48/50（已知物体），证明模型先验的价值。
- [[li2025routing]]：DLO routing 的两阶段 RL→Diffusion。摩擦随机化将高摩擦场景成功率提升 44%，是域随机化在接触丰富任务中的定量证据。
- [[do2025watch]]：RL+变阻抗控制+在线策略蒸馏。关键发现：变阻抗控制是 sim-to-real 关键（移除后下降 40%），"看少感多"的力控制策略比视觉策略更易迁移。
- [[yang2025simtoreal]]：ICRA Sim2Real 竞赛冠军方案。SMMS 四步级联解决运动模糊，Type III PI 反馈线性化解决控制非线性。工程性强但依赖 ArUco 标记。
- [[wu2025rlgsbridge]]：RL-GSBridge 用 Soft Mesh Binding GS 缩小视觉差距，抓取 Sim-to-Real 仅 avg↓6.6%，Pick-and-Place 反而↑4%。
- [[wu2025imperfect]]：SSDF 处理不完美专家演示的自监督方法。仿真 85.6%/真实平均 45%，质量分数加权是亮点。
- [[liu2025autonomous]]：RLAC 框架在 DLO 操控中验证 sim-to-real。真实双臂 UR5 成功率 91/100，展示 RL→经典控制切换的迁移优势。
- [[dalal2025local]]：ManipGen 大规模 RL 蒸馏+VLM 任务分解。50 真实任务 76% 成功率，局部策略设计是 sim-to-real 成功的关键。

## Evidence Map

- **本地证据规模**：26 篇 status:done 文献，覆盖域随机化（7 篇）、高保真渲染（3 篇）、模型+RL 混合（5 篇）、Real-to-Sim-to-Real（3 篇）、基准/评估（8 篇）。
- **强证据问题**（本地证据充分支持）：
  - 域随机化在接触丰富任务中的定量效果：[[li2025routing]] 量化了 44% 的提升。
  - 模型+RL 混合 vs 纯 RL 的训练效率对比：[[marougkas2025integrating]] 有完整消融。
  - 3DGS 高保真渲染的零样本迁移效果：[[qureshi2025splatsim]] 86.25% 有说服力。
  - 变阻抗控制对 sim-to-real 的关键性：[[do2025watch]] 移除后下降 40%。
- **弱证据问题**（本地证据不足或缺失）：
  - Sim-to-Real 在 DLO 双臂操控场景的系统性评估（本地仅有 [[liu2025autonomous]]）。
  - 大规模预训练策略（VLA）的 sim-to-real 性能（[[team2024octo]]、[[kim2024openvla]] 未系统测试 sim-to-real）。
  - 仿真到真实迁移失败案例的系统性分析（本地无专门文献）。

## Open Problems

- **DLO 双臂操控的 Sim-to-Real**：这是本研究方向的核心场景，但本地仅有 [[liu2025autonomous]] 和 [[li2025routing]] 直接验证。DLO 的接触动力学（摩擦、缠绕、张力）远比刚体复杂，仿真器保真度不足。
- **高保真渲染的速度-质量权衡**：[[qureshi2025splatsim]] 的 9.3 FPS 和 [[wu2025rlgsbridge]] 的渲染速度都限制了在线训练效率。如何在保持视觉质量的同时提升渲染速度？
- **VLA 模型的 Sim-to-Real 闭环**：当前 VLA（Octo、OpenVLA）主要在真实数据上训练，如何利用仿真数据扩展其能力并保证 sim-to-real 迁移质量仍是未解问题。
- **Sim-to-Real 失败的自动检测和恢复**：策略迁移失败时如何自动检测（而非等到任务完全失败）并切换到安全模式？本地无专门文献。

## Related Concepts

- [[deformable-linear-object]]
- [[robotic-manipulation]]
- [[grasping]]
- [[vision-language-model]]
- [[reinforcement-learning]]
- [[imitation-learning]]
- [[bimanual-manipulation]]
- [[robot-learning]]
- [[diffusion-model]]
- [[planning]]
- [[tactile-sensing]]
- [[flow-matching]]
- [[collision-avoidance]]
- [[novel-view-synthesis]]
## Related Papers

- [[antonova2021bayesian]]
- [[baumeister2025incremental]]
- [[blancomulero2024benchmarking]]
- [[chen2026adacleargrasp]]
- [[chen2026craft]]
- [[choi2026rankq]]
- [[consortium2026openhembodiment]]
- [[dalal2025local]]
- [[deshpande2026molmob0t]]
- [[do2025watch]]
- [[du2024embedded]]
- [[fang2026dexdrummer]]
- [[fu2026capx]]
- [[haldar2026point]]
- [[hou2026world]]
- [[huang2026flexitac]]
- [[huang2026kinder]]
- [[iek2026coral]]
- [[jia2026gsplayground]]
- [[jiang2026world4rl]]
- [[jin2026grounding]]
- [[kang2026coenv]]
- [[kuroki2025gendom]]
- [[levy2026simulation]]
- [[li2026lehome]]
- [[lips2024keypoints]]
- [[liu2025autonomous]]
- [[liu2025oneshot]]
- [[luijkx2026llmguided]]
- [[luo2026flash]]
- [[ma2026semanticcontact]]
- [[mahboob2026betting]]
- [[marougkas2025integrating]]
- [[moroncelli2026jumpstart]]
- [[patel2025realtosimtoreal]]
- [[qureshi2025splatsim]]
- [[röfer2025pseudotouch]]
- [[saad2026hybrid]]
- [[sakamoto2026e3vsbench]]
- [[sha2026efficient]]
- [[shen2026plan]]
- [[shi2026agile]]
- [[singh2025handobject]]
- [[sun2026maniparena]]
- [[tan2026fsunav]]
- [[tong2026uncovering]]
- [[wang2026phys2real]]
- [[wang2026visionlanguageaction]]
- [[wei2026navol]]
- [[wu2025imperfect]]
- [[wu2025rlgsbridge]]
- [[wu2026affordgrasp]]
- [[wu2026reliable]]
- [[xiao2026worldenv]]
- [[xu2026r2rgen]]
- [[xu2026roboagent]]
- [[xu2026twinrlvla]]
- [[yan2026tac2real]]
- [[yang2025simtoreal]]
- [[yang2026asyncshield]]
- [[yang2026automated]]
- [[yang2026physforge]]
- [[yang2026twintrack]]
- [[yang2026ultradexgrasp]]
- [[ye2026generation]]
- [[yin2026genie]]
- [[you2026dotsim]]
- [[yu2026atrs]]
- [[zhang2026visionlanguageaction]]
- [[zhao2026rosclaw]]
- [[zhao2026vitactracing]]
- [[zheng2026pokevla]]
- [[zhou2025oneshot]]
- [[zhou2026sim1]]