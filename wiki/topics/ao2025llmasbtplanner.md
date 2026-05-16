---
title: "LLM-as-BT-planner: Leveraging LLMs for behavior tree generation in robot task planning"
tags: [VLM]
created: "2026-04-25"
updated: "2026-04-25"
type: "literature"
status: "done"
summary: "提出利用 LLM 通过四种 in-context learning 方法和监督微调直接生成机器人装配任务的行为树（BT），在 Siemens 齿轮组装配任务和 FurnitureBench 上验证，human-in-the-loop 方法达到 16/17 成功率"
authors: "Ao, Jicong; Wu, Fan; Wu, Yansong; Swikir, Abdalla; Haddadin, Sami"
year: "2025"
venue: "arXiv Preprint"
zotero_key: "CY7PUSZG"
---
## 摘要

Robotic assembly（装配） tasks remain an open challenge due to their long horizon nature and complex part relations. Behavior trees (BTs) are increasingly used in robot task planning for their modularity and flexibility, but creating them manually can be effort-intensive. Large language models (LLMs) have recently been applied to robotic task planning for generating action sequences, yet their ability to generate BTs has not been fully investigated. To this end, we propose LLM-as-BT-Planner, a novel framework that leverages LLMs for BT generation in robotic assembly（装配） task planning. Four in-context learning methods are introduced to utilize the natural language processing and inference capabilities of LLMs for producing task plans in BT format, reducing manual effort while ensuring robustness and comprehensibility. Additionally, we evaluate the performance of fine-tuned smaller LLMs on the same tasks. Experiments in both simulated and real-world settings demonstrate that our framework enhances LLMs’ ability to generate BTs, improving success rate through in-context learning and supervised finetuning.

## 中文简述

提出基于大语言模型的操控方法。

**研究方向**: 视觉-语言模型

## 证据元数据

- **Fulltext Quality**: fulltext
- **Evidence Coverage**: 读取了全文，包括 abstract、introduction、related work、method (Sec III-IV)、experiments (Sec V)、tables (Table I-II)、figures (Fig 1-5)、limitations (Sec V.G)、conclusion
- **Confidence**: high — 全文完整，实验数据详实，方法描述清晰
- **Summary**: 提出利用 LLM 通过四种 in-context learning 方法和监督微调直接生成机器人装配任务的行为树（BT），在 Siemens 齿轮组装配任务和 FurnitureBench 上验证，human-in-the-loop 方法达到 16/17 成功率
## 关键贡献

1. 建立了 LLM-as-BT-Planner 框架，通过 LLM 直接生成可执行的行为树用于复杂机器人装配任务
2. 提出四种 in-context learning 方法（one-step、iterative、human-in-the-loop、recursive）和监督微调来提升 BT 生成性能
3. 系统评估了不同方法的性能，包括成功率、逻辑一致性、可执行性、时间和 token 消耗
## 结构化提取

- **Problem**: 机器人装配任务中行为树手动编程耗时，LLM 直接生成 BT 的能力未被系统研究
- **Method**: LLM-as-BT-Planner 框架，四种 in-context learning（one-step/iterative/human-in-the-loop/recursive）+ 监督微调生成 BT
- **Tasks**: 齿轮组装配（Siemens Challenge）、椅子/灯具装配（FurnitureBench）
- **Sensors**: 世界模型（关系图 + Neo4j），无视觉感知详细描述
- **Robot Setup**: Franka Panda 7-DoF 单臂 + 工具切换机制，笛卡尔自适应力阻抗控制
- **Metrics**: SR（成功率）、LC（逻辑一致性）、Exec（可执行性）、GD（生成时长）、TC（token 消耗）
- **Limitations**: 资源消耗大、小模型推理弱、深层 BT 冲突、仅单臂验证
- **Evidence Notes**: 全文完整读取，Table I-II 提供定量比较，Fig 5 展示真实机器人执行流程
## 本地引用关系

- [[liu820enhancing]]
- [[ryu2025curricullm]]
- [[smith2024steer]]
- [[styrud2025automatic]]
- [[zhi2025closedloop]]
## Problem

机器人装配任务是长时域（long-horizon）问题，零件关系复杂。行为树（BT）具有模块化和灵活性优势，但手动编程 BT 非常耗时。已有方法用 LLM 生成动作序列，但 LLM 直接生成 BT 的能力尚未被系统研究。


## Method

框架分三层：
- **高层**：LLM 将自然语言指令分解为子目标序列
- **中层**：LLM 基于子目标、世界状态、动作知识生成 BT
- **低层**：机器人执行 BT，技能库提供动作实现

四种 BT 生成方法：
1. **One-step generation**：直接生成完整 BT
2. **Iterative generation**：利用仿真反馈迭代修正 BT
3. **Human-in-the-loop**：用户反馈指导 BT 生成和修正，先生成 bullet plan 再生成 BT
4. **Recursive generation**：算法引导递归调用 MakePlan/MakeTree/PredictState 逐步展开 BT

微调任务类型：
- Unit-tree generation：单动作转 BT 子树
- One-step generation：完整 BT 生成


## Experiments

- **任务**：Siemens Robot Assembly Challenge 齿轮组装配（3 个轴 + 3 个齿轮 + 工具切换）、FurnitureBench 椅子和灯具装配
- **机器人**：Franka Emika Panda 7-DoF，配工具切换机制
- **LLM**：GPT-4（主力）、GPT-3.5、Mistral-7B、Llama-13B-chat
- **关键结果**：
  - Human-in-the-loop 方法最优：SR=16/17, LC=16/17, Exec=17/17
  - Recursive 方法逻辑一致性最高（17/17）但资源消耗大（231s, 50k tokens）
  - 非特定仿真反馈对性能无明显帮助（iterative vs one-step）
  - 微调显著提升小模型结构化输出能力（如 Mistral-7B Exec 从 7/10→10/10）
  - 微调无法提升小模型的推理能力（one-step SR 保持 0-1/10）


## Limitations

1. Recursive 方法资源消耗过大
2. 微调对小模型的推理能力提升有限
3. 深层嵌套 BT 节点可能冲突
4. 仅在单臂装配任务上验证


## Key Takeaways

- Human-in-the-loop 是 LLM 生成 BT 的最有效策略，精准的自然语言反馈可显著提升性能
- 小模型微调后能生成结构正确的 BT，但推理能力（依赖关系、嵌套逻辑）仍不足
- BT 作为任务规划表示比动作序列更具模块化和可重用性
- 行为树框架天然支持反馈驱动的重规划

## 相关概念

- [[vision-language-model]]

## 相关研究者

- [[ao|Ao, Jicong]]
- [[wu|Wu, Fan]]
- [[wu-yansong|Wu, Yansong]]
- [[swikir|Swikir, Abdalla]]
- [[haddadin|Haddadin, Sami]]
