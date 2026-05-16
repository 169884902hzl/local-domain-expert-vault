---
title: "Automatic Behavior Tree Expansion with LLMs for Robotic Manipulation"
tags: [manipulation, VLM]
created: "2026-04-25"
updated: "2026-04-25"
type: "literature"
status: "done"
summary: "提出 BETR-XP-LLM 方法，结合 LLM 和任务规划器自动生成和扩展行为树（BT）作为机器人操控策略。两阶段：(1) LLM 将自然语言目标解释为形式化目标条件 → PDDL 规划器生成 BT；(2) 规划/执行失败时，LLM 识别缺失前提条件或参数 → 自动永久更新 BT。改进 prompt + GPT-4 消除了 LLM-OBTEA 的反思反馈需求：目标解释 Easy 100%/Medium 100%/Hard 97%，远超 LLM-OBTEA (GPT-3.5) 的 84.7%/76.7%/59%。10 个失败场景（缺失前提/参数）全部正确识别。真实 ABB YuMi 验证"
authors: "Styrud, Jonathan; Iovino, Matteo; Norrlöf, Mikael; Björkman, Mårten; Smith, Christian"
year: "2025"
venue: "2025 IEEE International Conference on Robotics and Automation (ICRA)"
zotero_key: "RES5D85U"
---
## 摘要

Robotic systems for manipulation（操控） tasks are increasingly expected to be easy to configure for new tasks or unpredictable environments, while keeping a transparent policy that is readable and verifiable by humans. We propose the method BEhavior TRee（行为树） eXPansion with Large Language Models (BETR-XP-LLM) to dynamically and automatically expand and configure Behavior Trees as policies for robot control. The method utilizes an LLM to resolve errors outside the task planner’s capabilities, both during planning and execution. We show that the method is able to solve a variety of tasks and failures and permanently update the policy to handle similar problems in the future.


## 中文简述

提出基于大语言模型的操控方法。

**研究方向**: 机器人操控、视觉-语言模型

## 关键贡献

1. LLM 超越目标解释：用于解决规划器能力之外的错误（缺失前提条件、缺失参数）
2. 永久性策略更新：LLM 输出自动插入 BT 并由规划器扩展，保留透明性和反应性
3. 改进 prompt + GPT-4 消除反思反馈：一次 LLM 调用即可获得高精度目标解释
## 结构化提取

- **Problem**: 从自然语言自动生成可反应、可验证的行为树策略，并自动处理执行失败
- **Method**: BETR-XP-LLM — LLM 目标解释 + PDDL 规划器 + LLM 失败解决 + BT 永久更新
- **Tasks**: 咖啡馆 100 任务 + 10 失败场景 + 真实 4 任务
- **Sensors**: Azure Kinect (RGB-D) + YoloWorld + NanoSAM
- **Robot Setup**: ABB YuMi 双臂机器人
- **Metrics**: 目标解释准确率 + 失败场景解决率 + 参数推理合理性
- **Limitations**: 测试规模有限、技能库不完整、感知依赖
- **Evidence Notes**: 全文读取，Tables I-IV 提供完整对比
## 本地引用关系

- [[ao2025llmasbtplanner]]
- [[garcia2025generalizable]]
- [[liu820enhancing]]
- [[qiu2025wildlma]]
- [[singh2025intellirms]]
## 证据元数据

- **Fulltext Quality**: fulltext
- **Evidence Coverage**: 读取了全文，包括 abstract、introduction (Sec I)、background (Sec II)、method (Sec III)、experiments (Sec IV)、tables (I-IV)、figures (1-3)
- **Confidence**: high — 全文完整，ICRA 2025，KTH + ABB Robotics，ABB YuMi 真实机器人验证，GPT-4-1106，100 任务咖啡馆数据集，10 失败场景全部解决
- **Summary**: 提出 BETR-XP-LLM 方法，结合 LLM 和任务规划器自动生成和扩展行为树（BT）作为机器人操控策略。两阶段：(1) LLM 将自然语言目标解释为形式化目标条件 → PDDL 规划器生成 BT；(2) 规划/执行失败时，LLM 识别缺失前提条件或参数 → 自动永久更新 BT。改进 prompt + GPT-4 消除了 LLM-OBTEA 的反思反馈需求：目标解释 Easy 100%/Medium 100%/Hard 97%，远超 LLM-OBTEA (GPT-3.5) 的 84.7%/76.7%/59%。10 个失败场景（缺失前提/参数）全部正确识别。真实 ABB YuMi 验证


## Problem

工业机器人需要在不可预测环境中快速配置新任务策略，同时保持策略的可读性、可验证性和反应性。现有 LLM+BT 方法（LLM-OBTEA）需要多轮反思反馈，且无法处理规划器缺失知识导致的执行失败。


## Method

- **程序生成**：
  - 自然语言 → LLM (GPT-4-1106) → 形式化目标条件（BT 节点）
  - PDDL 风格规划器 → 行为树策略
  - Prompt 包含：场景物体列表、条件描述、示例、严格输出格式
- **失败解决**：
  - 检测失败（规划阶段仿真 or 执行阶段真实）
  - LLM 接收：错误消息 + 场景信息 + 可用条件列表
  - 输出：缺失的前提条件 or 参数值
  - 自动插入 BT 并由规划器扩展
  - 过程可迭代重复
- **关键设计**：
  - 条件描述避免歧义（如 "Active" vs "On"）
  - 严格指定仅使用列出的物体
  - Chain-of-thought 反而降低准确率（LLM 过度推理）


## Experiments

- **目标解释对比**（100 任务咖啡馆数据集）：
  - LLM-OBTEA (GPT-3.5, 0F): Easy 84.7%, Medium 76.7%, Hard 59.0%
  - LLM-OBTEA (GPT-3.5, 5F): Easy 90.7%, Medium 82.0%, Hard 65.0%
  - Ours (GPT-4, 0F): **Easy 100%, Medium 100%, Hard 97.0%**
- **缺失前提条件识别**（10 场景 × 10 次）：
  - 全部正确识别：如物体阻挡、杯子倒置、离心机关闭、柜子锁定等
- **缺失参数选择**（语义推理）：
  - 鸡蛋抓取力：5.3N，锤子：37.2N
  - 枕头速度：0.6m/s，急救包：1.5m/s，婴儿：0.1m/s
  - 沙子工具：铲子，洗盘子：海绵/刷子
- **真实机器人**：ABB YuMi + Azure Kinect + YoloWorld + NanoSAM
  - 4 个任务验证：立方体堆叠、杯子放置、抽屉离心机等


## Limitations

1. 测试规模有限（几十个物体和条件），大规模场景下 LLM 表现未验证
2. 技能库缺少必要动作时无法自动创建（需从低级原语组合）
3. 模糊指令的处理需要额外机制
4. 感知依赖 YoloWorld，堆叠物体识别困难
5. 未研究自我纠正（self-correction）对更困难问题的改善


## Key Takeaways

- 改进 prompt + 更强 LLM 可消除反思反馈：一次调用即可高精度
- BT 的透明性使 LLM 修改可验证：形式化验证仍可执行
- 永久性学习是关键：一次失败解决后 BT 自动处理类似问题
- 条件描述对 LLM 理解至关重要：避免歧义比 chain-of-thought 更有效
- 参数推理展示 LLM 的常识推理能力：力度、速度、工具选择

## 相关概念

- [[robotic-manipulation]]
- [[vision-language-model]]
- [[bimanual-manipulation]]
- [[grasping]]

## 相关研究者

- [[styrud|Styrud, Jonathan]]
