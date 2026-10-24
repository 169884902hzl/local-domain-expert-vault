---
title: "Tactile Sensing"
tags: [concept, tactile]
created: "2026-04-25"
updated: "2026-04-26"
type: "concept"
status: "done"
summary: "触觉感知补充视觉的接触状态盲区，在精细装配和力控任务中不可替代，但仿真建模和跨物体泛化仍是瓶颈"
aliases: [tactile, "touch sensing", "haptic sensing"]
---

## Definition

触觉感知：通过接触、力或表面形变信号辅助机器人操控的方法

## Key Ideas

- 触觉信号能补充视觉遮挡和接触状态不可见的问题。
- 常用于抓取稳定性、滑移检测、材料/形状识别和精细装配。
- 主要挑战是传感器标定、仿真建模、数据规模和跨物体泛化。
- 触觉信号对接触丰富任务（精密装配、力控）不可替代：[[wu2025tacdiffusion]] 输出 6D wrench 实现零样本 95.7% 成功率，[[han2025upvital]] 的触觉重建误差作为 RL 奖励信号。
- 触觉仿真是当前瓶颈：真实触觉传感器标定复杂，仿真建模困难。[[röfer2025pseudotouch]] 的 PseudoTouch 用深度 patch 预测触觉信号，是绕过仿真瓶颈的替代方案。
- 多模态触觉融合（视觉+力+触觉）是趋势：[[zhao2025polytouch]] 三模态传感器、[[george2024vital]] VITaL 多模态对比预训练。单一触觉模态的泛化能力有限。

## Method Families

- 机器人操控路径：本地有 12 篇相关文献，代表论文包括 [[chi2024diffusion]]、[[collins2025shapespace]]、[[funk2024evetac]]、[[george2024vital]]。
- 模仿学习路径：本地有 5 篇相关文献，代表论文包括 [[chi2024diffusion]]、[[george2024vital]]、[[liu2025forcemimic]]、[[wu2025tacdiffusion]]。
- 机器人学习路径：本地有 4 篇相关文献，代表论文包括 [[chi2024diffusion]]、[[liu2025forcemimic]]、[[nazarczuk2025closed]]、[[zhao2025polytouch]]。
- 扩散模型路径：本地有 3 篇相关文献，代表论文包括 [[chi2024diffusion]]、[[wu2025tacdiffusion]]、[[zhao2025polytouch]]。
- 视觉-语言模型路径：本地有 1 篇相关文献，代表论文包括 [[chi2024diffusion]]。

## Key Papers

- [[chi2024diffusion]]：DDPM 条件扩散策略 + 闭环动作序列预测 + 视觉条件化 + 时序扩散 Transformer；证据：任务成功率、IoU（Push-T）、覆盖率（Sauce）。
- [[zhao2025polytouch]]：PolyTouch三模态传感器（VHB/硅胶弹性体+荧光照明+曲面镜）+ Tactile-Diffusion Policy（T3+CLIP+AST+Cross-At...；证据：平均任务进度（3-7阶段）、平均任务成功率、弹性体耐久性（小时）。
- [[wu2025tacdiffusion]]：TacDiffusion — DDPM 6D wrench 输出 + 动态系统滤波器 + 阻抗控制前馈力；证据：成功率（零样本迁移平均 95.7%）+ 执行时间。
- [[röfer2025pseudotouch]]：PseudoTouch — 深度 patch → MLP → ReSkin 15D 触觉信号预测；证据：预测 MSE、cosine similarity、识别准确率、抓取稳定性准确率。
- [[nazarczuk2025closed]]：CLIER — 符号程序生成 + 场景图 + Transformer 动作规划 + 闭环原语执行；证据：任务成功率 + 物理属性测量准确性。
- [[liu2025forcemimic]]：ForceCapture（手持力-位采集）+ HybridIL（扩散策略输出 wrench+pose + 混合力-位控制）；证据：运动正确率、>10cm 连续皮成功率。
- [[han2025upvital]]：UpViTaL — LSTM 触觉自编码器 + MAE 视觉预训练 + 触觉重建误差奖励 + PPO；证据：成功率（100 次评估 × 4 seeds）。
- [[collins2025shapespace]]：Shape-Space Deformer — 统一潜在表示 + 超网络条件化 + 变形场表面渲染；证据：Chamfer Distance（CD↓）。
- [[george2024vital]]：VITaL — 时间感知多模态对比预训练 + ACT/DP 框架集成；证据：成功率（20 次试验）、平均应变。
- [[funk2024evetac]]：Evetac — 事件相机 + 标记阵列 + 异步处理 + 数据驱动滑移检测；证据：标记追踪精度、振动检测频率、滑移检测 F1、抓取成功率。

## Evidence Map

- 本地证据规模：当前概念页连接 12 篇 literature notes，其中 12 篇为 `status: done`。
- 代表性证据链：[[chi2024diffusion]]、[[zhao2025polytouch]]、[[wu2025tacdiffusion]]、[[röfer2025pseudotouch]]、[[nazarczuk2025closed]]。
- 主要交叉主题：机器人操控(12)、模仿学习(5)、机器人学习(4)、扩散模型(3)、视觉-语言模型(1)。
- 可核查实验结果主要来自：[[chi2024diffusion]]、[[zhao2025polytouch]]、[[wu2025tacdiffusion]]、[[röfer2025pseudotouch]]、[[nazarczuk2025closed]]；回答具体性能问题时应回到这些论文笔记核对指标。

## Open Problems

- [[chi2024diffusion]] 暴露的限制：继承行为克隆局限（需充足演示数据）；推理延迟高于简单方法（如 LSTM-GMM）；不适合极高频控制任务。
- [[zhao2025polytouch]] 暴露的限制：VHB磁滞、多模态需更多数据、仅4任务验证、整体成功率偏低。
- [[wu2025tacdiffusion]] 暴露的限制：仅插入任务、依赖专家策略、模型大小需权衡。
- [[röfer2025pseudotouch]] 暴露的限制：单传感器类型、无动态触觉、非凸物体泛化有限。
- [[nazarczuk2025closed]] 暴露的限制：复杂任务低成功率、依赖位姿精度、仅桌面场景。
- [[liu2025forcemimic]] 暴露的限制：简单 MLP、单一技能、力作为输入效果差。

## Related Concepts

- [[grasping]]
- [[robotic-manipulation]]
- [[deformable-linear-object]]
- [[vision-language-model]]
- [[imitation-learning]]
- [[bimanual-manipulation]]
- [[diffusion-model]]
- [[reinforcement-learning]]
- [[robot-learning]]
- [[sim-to-real]]
- [[planning]]
- [[collision-avoidance]]
- [[proximity-sensing]]
- [[flow-matching]]
## Related Papers

- [[chen2025benchmarking]]
- [[chen2026ropa]]
- [[collins2025shapespace]]
- [[enwerem2026variational]]
- [[funk2024evetac]]
- [[george2024vital]]
- [[han2025upvital]]
- [[he2026exploratory]]
- [[huang2026flexitac]]
- [[kohlbrenner2026egocentric]]
- [[lee2026modular]]
- [[ma2026semanticcontact]]
- [[niu2026versatile]]
- [[ozdamar820pushing]]
- [[röfer2025pseudotouch]]
- [[wang2026ocra]]
- [[xu2026fingereye]]
- [[xue2026tube]]
- [[yan2026tac2real]]
- [[you2026dotsim]]
- [[zhang2026forceflow]]
- [[zhang2026handx]]
- [[zhang2026touchguide]]
- [[zhao2025polytouch]]
- [[zhao2026visualtactile]]
- [[zhao2026vitactracing]]
- [[zheng120dottip]]