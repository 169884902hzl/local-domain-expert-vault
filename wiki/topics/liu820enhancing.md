---
title: "Enhancing the LLM-Based Robot Manipulation Through Human-Robot Collaboration"
tags: [manipulation, VLM, RL, imitation]
created: "2026-04-25"
updated: "2026-04-25"
type: "literature"
status: "done"
summary: "提出 LLM+HRC 框架：GPT-4 分解高层指令为子任务序列→选择运动函数→结合 YOLOv5 感知的环境信息生成可执行代码。对于 LLM 无法处理的复杂轨迹（如水平铰链烤箱门），通过 VR 遥操作+DMP 学习人演示轨迹并存储到 DMP 库供复用。7 任务平均成功率 79.5%，可执行率 99.4%，可行性 97.5%。DMP 库使原不可行任务（开烤箱 0%→100%）变为可行"
authors: "Liu, Haokun; Zhu, Yaonan; Kato, Kenji; Tsukahara, Atsushi; Kondo, Izumi et al."
year: "2020"
venue: "IEEE Robotics and Automation Letters"
zotero_key: "3NT8KIFC"
---
## 摘要

Large Language Models (LLMs) are gaining popularity in the ﬁeld of robotics. However, LLM-based robots are limited to simple, repetitive motions due to the poor integration between language models, robots, and the environment. This letter proposes a novel approach to enhance the performance of LLMbased autonomous manipulation（操控） through Human-Robot Collaboration (HRC). The approach involves using a prompted GPT-4 language model to decompose high-level language commands into sequences of motions that can be executed by the robot. The system also employs a YOLO-based perception algorithm, providing visual cues to the LLM, which aids in planning feasible motions within the speciﬁc environment. Additionally, an HRC method is proposed by combining teleoperation and Dynamic Movement Primitives (DMP), allowing the LLM-based robot to learn from human guidance. Real-world experiments have been conducted using the Toyota Human Support Robot for manipulation（操控） tasks. The outcomes indicate that tasks requiring complex trajectory planning and reasoning over environments can be efﬁciently accomplished through the incorporation of human demonstrations.

## 中文简述

提出基于GPT的操控方法。

**研究方向**: 机器人操控、视觉-语言模型、强化学习、模仿学习

## 证据元数据

- **Fulltext Quality**: fulltext
- **Evidence Coverage**: 读取了全文，包括 abstract、introduction、related work (Sec II)、methods (Sec III)、experiments (Sec IV)、tables (I-II)、figures (1-6)
- **Confidence**: high — 全文完整，IEEE RA-L 2024，Toyota HSR 真实机器人，7 任务×23 trials=161 trials，层次规划+HRC框架
- **Summary**: 提出 LLM+HRC 框架：GPT-4 分解高层指令为子任务序列→选择运动函数→结合 YOLOv5 感知的环境信息生成可执行代码。对于 LLM 无法处理的复杂轨迹（如水平铰链烤箱门），通过 VR 遥操作+DMP 学习人演示轨迹并存储到 DMP 库供复用。7 任务平均成功率 79.5%，可执行率 99.4%，可行性 97.5%。DMP 库使原不可行任务（开烤箱 0%→100%）变为可行
## 关键贡献

1. GPT-4 层次任务规划：长时序任务自动分解为子任务+运动函数序列
2. YOLOv5 环境感知集成：提供物体位置信息给 LLM 用于运动规划
3. HRC 框架：VR 遥操作+DMP 学习人类演示，扩充运动库
4. 障碍物识别算法：三角检测空间自动识别并移除障碍物
## 结构化提取

- **Problem**: LLM 机器人系统复杂轨迹规划不足 + 人类持续监督渠道缺乏
- **Method**: GPT-4 层次规划 + YOLOv5 感知 + VR 遥操作 + DMP 学习
- **Tasks**: 厨房 7 任务（zero-shot + one-shot DMP）
- **Sensors**: ASUS Xtion 深度相机 + Oculus VR
- **Robot Setup**: Toyota Human Support Robot (HSR)
- **Metrics**: 可执行率、可行性、成功率
- **Limitations**: 2D 视觉、DMP 扩展性、厨房场景、Prompt 工作量大
- **Evidence Notes**: 全文读取，Tables I-II 提供完整性能评估
## 本地引用关系

- [[ao2025llmasbtplanner]]
- [[gao2024prime]]
- [[kordia2025optimize]]
- [[liu2025forcemimic]]
- [[luo2024humanagent]]
## Problem

LLM 机器人系统局限于简单重复运动，难以处理复杂轨迹规划和长时序任务。运动函数库有限，代码生成方式无法处理受约束运动。人类持续监督渠道不足。


## Method

- **LLM 规划（GPT-4 Turbo）**：
  - 基本库：move_to_position()、base_cycle_move()、close_move()、gripper_control()
  - DMP 库：存储遥操作学习的运动序列
  - 层次策略：长任务→子任务→运动函数序列
  - Prompt 设计：引入任务分类、可执行代码格式约束
- **环境感知（YOLOv5）**：
  - Xtion 深度相机 → YOLOv5 检测
  - 坐标转换：像素→相机→世界坐标
  - 算法 1：同类别物体左右排序标注
  - 算法 2：三角检测空间识别障碍物
- **HRC 模块**：
  - Oculus VR 设备遥操作
  - DMP 学习演示轨迹（15 个高斯基函数）
  - 通过 UI 修改运动函数并存储到 DMP 库
  - LLM 自动命名（动作+目标组合，如 open_oven_handle）


## Experiments

- **Toyota HSR 真实机器人**：
  - 7 任务，每任务 23 trials（共 161 trials）
  - 可执行率：99.4%（仅 1 次失败）
  - 可行性：97.5%
  - 平均成功率：79.5%
- **Zero-shot 任务**：Put&Stack、Open(Microwave)、Warm Up、Clean Table
- **One-shot DMP 任务**：Open Oven、Close Oven、Open Cabinet（需要 HRC）
  - Open Oven：0%（basic library）→ 100%（HRC+DMP）
  - Open Cabinet：0% → 100%
- **失败分析**：YOLO 检测精度导致定位误差（0.0095-0.0122m），长时序任务误差累积


## Limitations

1. 仅依赖 2D 视觉输入（YOLOv5），精度受限
2. DMP 库需要手动遥操作学习，扩展性有限
3. 仅在厨房场景验证
4. Prompt 设计工作量大
5. 长时序任务误差累积


## Key Takeaways

- LLM + 运动函数库是实用的机器人操控框架：可执行率接近 100%
- HRC 是解决 LLM 能力边界的有效手段：将不可行任务变为可行
- DMP 提供了从人类演示到可复用运动函数的简洁路径
- 层次规划避免长序列错误：子任务分解减少单次规划复杂度
- YOLO 检测精度是系统瓶颈：0.01m 误差可导致高精度任务失败

## 相关概念

- [[robotic-manipulation]]
- [[vision-language-model]]
- [[reinforcement-learning]]
- [[imitation-learning]]
- [[grasping]]

## 相关研究者

- [[liu-haokun|Liu, Haokun]]
