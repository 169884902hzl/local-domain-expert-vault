---
title: "Hierarchical Policy"
tags: [reinforcement-learning, manipulation, planning]
created: "2026-05-11"
updated: "2026-05-11"
type: "concept"
status: "done"
summary: "分层策略架构，高层负责全局规划/调度，低层负责精细执行，降低单一策略的学习难度"
---

## Definition

Hierarchical Policy is maintained here as an evidence-linked concept. 分层策略架构，高层负责全局规划/调度，低层负责精细执行，降低单一策略的学习难度

## Key Ideas

- Direct local evidence currently comes from [[fang2026dexdrummer]].
- The concept is tracked with local tags: reinforcement-learning, manipulation, planning.
- Treat this page as a map into local readings, not as external ground truth.
- Claims should be checked against the linked `status: done` topic notes before use in proposals.
- When evidence is sparse, use the broader-context papers below only for comparison, not as proof of the concept.

## Method Families

- Direct paper-specific method: inspect the direct evidence papers listed below.
- Robot learning context: compare how the concept changes policy learning, evaluation, or deployment.
- Planning/control context: check whether the concept affects temporal abstraction, constraints, or execution feedback.
- Representation context: check whether the concept changes visual, language, tactile, or geometric state representation.
- Evaluation context: prefer papers with explicit baseline, metric, ablation, and failure analysis.

## Key Papers

- [[fang2026dexdrummer]] (direct evidence): 提出分层式灵巧鼓手机器人框架 DexDrummer，高层用参数化运动基元+残差 RL 实现鼓棒轨迹跟踪，低层用接触靶向奖励（指尖接触、支点奖励、手臂能量惩罚、接触课程）训练手...
- [[yuan2026prefmoe]] (broader context): 提出 PrefMoE，通过在多模态 Transformer 奖励模型的跨模态融合层引入 Mixture-of-Experts 轨迹级软路由，显式建模众包/合成偏好标注中的异构...
- [[yang2026ultradexgrasp]] (broader context): 提出面向双臂灵巧手的通用抓取框架，通过优化抓取合成+规划示范生成构建 2000 万帧多策略数据集，点云策略实现 84% 仿真成功率和 81.2% 真实零样本迁移
- [[wu2026continually]] (broader context): 提出 Stellar VLA，利用 Dirichlet Process 建模非参数知识空间，通过自进化学习联合优化任务表征与知识分布，在 MoE 路由中引入知识引导实现无参数...
- [[vo2026codegraphvlp]] (broader context): 提出层次化框架 CodeGraphVLP，通过持久化语义图状态 + LLM 合成的可执行代码规划器 + 去噪视觉语言提示，解决 VLA 模型在非马尔可夫长时序操控任务中的局限...
- [[luo2026selfimproving]] (broader context): 提出 SILVR 框架，让领域内视频生成模型通过自收集轨迹的迭代微调持续改进对新任务的视觉规划能力，结合 IPA 评分组合引入互联网视频先验，在 MetaWorld 12 个...
- [[li2026hierarchical]] (broader context): 提出层次化 DLO routing 框架，高层 VLM 通过 in-context learning 生成路由计划并检测恢复失败，低层 RL 策略执行精准 insertion...
- [[iek2026coral]] (broader context): 提出 CoRAL 模块化框架，用 LLM 作为 MPPI 代价函数设计器（非直接控制器），结合 VLM 语义物理先验、在线系统辨识和 RAG 记忆单元，实现接触丰富操控的零样...

## Evidence Map

- Direct evidence papers: [[fang2026dexdrummer]].
- Broader local evidence context: [[fang2026dexdrummer]], [[yuan2026prefmoe]], [[yang2026ultradexgrasp]], [[wu2026continually]], [[vo2026codegraphvlp]].
- Evidence level is strongest when a linked topic is both directly connected and `status: done`.
- If a paper is marked broader context, use it to define baselines or contrasts rather than to claim novelty.

## Open Problems

- Which assumptions are specific to the source paper, and which transfer to DLO, tactile, bimanual, VLA, or Sim-to-Real settings?
- What baseline would falsify the usefulness of this concept in a small pilot?
- Which metrics separate real improvement from easier evaluation conditions or data leakage?
- Does the concept still help under distribution shift, long-horizon execution, or contact-rich failure cases?
- What similar work already covers the same mechanism under a different name?

## Related Concepts

- [[residual-rl]]
- [[skill-composition]]
- [[reinforcement-learning]]
- [[planning]]
- [[robotic-manipulation]]
- [[robot-learning]]

## Related Papers

- [[fang2026dexdrummer]]
- [[yuan2026prefmoe]]
- [[yang2026ultradexgrasp]]
- [[wu2026continually]]
- [[vo2026codegraphvlp]]
- [[luo2026selfimproving]]
- [[li2026hierarchical]]
- [[iek2026coral]]
