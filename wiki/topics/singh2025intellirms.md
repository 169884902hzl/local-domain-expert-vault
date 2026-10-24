---
title: "IntelliRMS: A Robotic Manipulation System for Domain-Specific Tasks Using Vision and Language Foundational Models"
tags: [manipulation, VLM]
created: "2026-04-25"
updated: "2026-04-25"
type: "literature"
status: "done"
summary: "提出 IntelliRMS，基于 LLM+VLM 的端到端工业机器人操控系统架构。核心组件：(1) General Perception（Mask R-CNN 开放词汇检测）；(2) Task Planner（GPT 系列指令分类+任务规划+规则验证）；(3) Robotic Controller（行为树编排 3 种复合技能：DIPS/IRIS/ATCS）；(4) User Interface。应用于零售 bin-picking 订单履行，30 条指令测试集（Easy/Medium/Hard），规划准确率 100%，执行成功率 98.75%（无重试）/92.50%（有重试），单次拾取约 27s 周期"
authors: "Singh, Chandan Kumar; Kumar, Devesh; Sanap, Vipul; Khandelwal, Mayank; Sinha, Rajesh"
year: "2025"
venue: "2025 IEEE International Conference on Robotics and Automation (ICRA)"
zotero_key: "3Q3P3287"
---
## 摘要

Recent advancements in large language models (LLMs) have significantly enhanced machines’ ability to understand and follow human instructions. In many tasks, LLMs have demonstrated performance that rivals human-level common sense. However, directly applying LLMs to domainspecific use cases, such as robotic pick-and-place, remains a challenge. Tasks that are intuitive for humans, who rely on prior knowledge and skills, become complex for robots. Industrial robotic applications like pick-and-place require a high degree of accuracy, often exceeding 90%. In response to these challenges in domain-specific applications, we propose IntelliRMS, a novel system-oriented architecture for instruction-following robotic manipulation（机器人操控）. The IntelliRMS synergizes the linguistic and open-vocabulary visual capabilities of foundational models to arrive at an accurate, robust and scalable system. Further, we demonstrate the effectiveness of IntelliRMS in a realworld industrial Bin-picking scenario within the retail sector, validating its performance with a comprehensive dataset.


## 中文简述

提出基于大语言模型的操控方法。

**研究方向**: 机器人操控、视觉-语言模型

## 关键贡献

1. 端到端系统架构：集成 LLM 任务规划 + VLM 感知 + 行为树控制
2. 指令分类五级体系：Valid/Invalid/General/ADR/SIQ
3. 复合技能设计：DIPS（无监督拾取）+ IRIS（实例检索拾取）+ ATCS（自动工具切换）
4. 工业级验证：零售 bin-picking 场景，98.75% 成功率
## 结构化提取

- **Problem**: LLM+VLM 驱动的工业级机器人操控系统
- **Method**: IntelliRMS — LLM 任务规划 + Mask R-CNN 感知 + 行为树控制
- **Tasks**: 零售 bin-picking 订单履行（3 种复合技能）
- **Sensors**: Intel RealSense D455（RGB-D）
- **Robot Setup**: UR-5（主机器人）+ UR-10（次机器人）+ Robotiq 2F-85/Epick gripper
- **Metrics**: 规划准确率 + 执行成功率 + 延迟
- **Limitations**: 网络 LLM 延迟、单一场景、手工行为树
- **Evidence Notes**: 全文读取，Tables I-X 提供完整系统评估
## 本地引用关系

- [[ao2025llmasbtplanner]]
- [[garcia2025generalizable]]
- [[liu820enhancing]]
- [[qiu2025wildlma]]
## 证据元数据

- **Fulltext Quality**: fulltext
- **Evidence Coverage**: 读取了全文，包括 abstract、introduction (Sec I)、literature survey (Sec II)、system architecture (Sec III)、experiments (Sec IV)、tables (I-X)、figures (1-6)
- **Confidence**: high — 全文完整，ICRA 2025，TCS Research，UR-5 + UR-10 双臂工业平台，零售订单履行场景，30 指令测试集，规划准确率 100%，执行成功率 98.75%
- **Summary**: 提出 IntelliRMS，基于 LLM+VLM 的端到端工业机器人操控系统架构。核心组件：(1) General Perception（Mask R-CNN 开放词汇检测）；(2) Task Planner（GPT 系列指令分类+任务规划+规则验证）；(3) Robotic Controller（行为树编排 3 种复合技能：DIPS/IRIS/ATCS）；(4) User Interface。应用于零售 bin-picking 订单履行，30 条指令测试集（Easy/Medium/Hard），规划准确率 100%，执行成功率 98.75%（无重试）/92.50%（有重试），单次拾取约 27s 周期


## Problem

LLM 在通用场景展现强大能力，但直接应用于工业领域特定操控任务（如 bin-picking）仍有挑战。工业场景要求 >90% 准确率，且需处理领域规则、约束和边界情况。如何设计基于基础模型的系统架构实现可靠的工业级机器人操控？


## Method

- **General Perception**：
  - Mask R-CNN 检测 bin 中物体（SKU 数量较少时适用）
  - 大量 SKU 场景可切换到 CLIP 开放词汇检测
  - 提供物体类别、数量、bin 标识信息
- **Task Planner**：
  - LLM（GPT-3.5/4/4-Turbo）处理用户指令
  - 5 类指令分类：Valid（执行）、Invalid（不可执行）、General（闲聊）、ADR（需补充信息）、SIQ（系统信息查询）
  - 任务计划格式：技能序列 + 属性（物体名称/数量/位置）
  - 计划验证：规则基安全检查
  - Prompt 工程策略：占位符、域规则强调、递归自我改进
- **Robotic Controller**：
  - 基于 ROS2 Humble + Behavior Trees 实现
  - 3 种复合技能：DIPS（无监督域无关拾取，2F gripper）、IRIS（实例检索拾取，suction gripper）、ATCS（自动工具切换）
  - 局部 Re-Plan：控制器级别失败处理，减少向上层请求频率
- **User Interface**：
  - 文本/语音输入 + 执行状态实时显示
  - 失败分类 + 用户提示修复


## Experiments

- **LLM 成本对比**：GPT-3.5 最便宜但需最多 token；GPT-4 最贵但最准确
- **规划评估**（30 指令测试集）：
  - Easy: Precision 100%, Recall 100%, Plan 100%
  - Medium: Precision 98%, Recall 93%, Plan 100%
  - Hard: Precision 100%, Recall 100%, Plan 100%
- **技能可执行性测试**：
  - DIPS: 25 trials, 96%, 25s cycle
  - IRIS: 25 trials, 96%, 30s cycle
  - ATC: 25 trials, 100%, 30s cycle
- **整体系统性能**：
  - 无重试成功率：98.75%
  - 有重试成功率：92.50%
  - 单次拾取延迟约 27s
- **延迟分析**：Task Planner 9-23s（受网络影响），Perception 7-23s，Picking 12-44s


## Limitations

1. LLM 规划延迟依赖网络（OpenAI API），本地部署可改善
2. 仅验证 bin-picking 场景，未扩展到更复杂操控
3. Mask R-CNN 不适用于大量 SKU 场景
4. 行为树需手工设计技能逻辑
5. 真实失败模式包括感知位姿不良和物体掉落


## Key Takeaways

- 系统架构设计比单一模型更重要：分层解耦感知/规划/控制
- 指令分类是实用系统的关键：过滤不可执行/无关请求
- 行为树提供模块化和可解释性：优于端到端策略
- LLM 规划 + 规则验证组合确保安全：纯 LLM 不可靠
- 复合技能设计降低规划复杂度：高级原语比原子技能更易编排

## 相关概念

- [[robotic-manipulation]]
- [[vision-language-model]]
- [[bimanual-manipulation]]
- [[grasping]]

## 相关研究者

- [[singh-chandan-kumar|Singh, Chandan Kumar]]
