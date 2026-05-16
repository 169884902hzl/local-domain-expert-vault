---
title: "Evaluating Human-Robot Skill Gaps in Electrical Circuit Inspection: A New Electronic Task Board for Benchmarking Manipulation"
tags: [manipulation]
created: "2026-04-25"
updated: "2026-04-25"
type: "literature"
status: "done"
summary: "提出基于联网电子任务板的机器人操控基准，用于评估电气电路检查（万用表使用）的人机技能差距。6 个子任务：定位任务板+按键→读取屏幕+调整滑块→插入探针插头→开门+探针电路→缠绕电缆→按键停止。Robothon Grand Challenge 2023：16 团队参赛，9 队完成全部任务。最佳机器人（UR5e + Robotiq HAND-E + RealSense D435i）比最佳人类慢 29 秒（57.0s vs 44.7s 剔除 ST1），但缠绕电缆子任务优于人类。80 块任务板全球部署，5262 次试验数据库"
authors: "So, Peter; Swikir, Abdalla; Abu-Dakka, Fares J.; Haddadin, Sami"
year: "2025"
venue: "2025 IEEE International Conference on Robotics and Automation (ICRA)"
zotero_key: "AGJLRFZD"
---
## 摘要

Robot manipulation（机器人操控） researchers reference human performance as a goal for their work, however, human data is seldom present in robotics benchmarks. We introduce a realworld benchmark targeting manipulation（操控） skills for performing electrical circuit inspection with a multimeter using an Internetconnected electronic task board. We present timing study results and an exemplary robot solution across six different tasks from the Robothon Grand Challenge at the automatica conference in 2023. Contributions from 16 robot teams were collected using task boards we manufactured and distributed as part of the 30-day international competition as an initial performance database. Our work systematically highlights the skill gap between the winning robot solution and the best human performance from a group of 30 subjects. Our goal is to chronicle progress over time in robot manipulation（机器人操控） skills and provide a standardized, physical benchmark across the global community. Videos of the team submissions, the exemplary robot solution, as well as the project reproduction code are provided in the included repository.


## 中文简述

提出基于学习方法的操控方法。

**研究方向**: 机器人操控

## 关键贡献

1. 联网电子任务板基准：自动记录+上报+在线数据库
2. 6 个多样化操控子任务：涵盖定位、读取、插入、开门、缠绕
3. 30 人人类计时研究 vs 16 机器人团队对比
4. 开源硬件+软件+数据：全球社区可复现
## 结构化提取

- **Problem**: 机器人操控的标准化物理基准和人机技能差距评估
- **Method**: 联网电子任务板 + 自动遥测 + 比赛模式
- **Tasks**: 6 子任务（定位+按键、读取+滑块、插头插入、开门+探针、电缆缠绕、停止按钮）
- **Sensors**: RealSense D435i（RGB-D）+ ESP32 + IMU + I2C 传感器
- **Robot Setup**: UR5e + Robotiq HAND-E + 自定义 3D 打印工具
- **Metrics**: 执行时间 + 完成任务数 + 成功率
- **Limitations**: 单场景、样本量有限、作弊防护不足
- **Evidence Notes**: 全文读取，Figures 8-9 提供完整时间对比和分布
## 本地引用关系

- [[collins2025shapespace]]
- [[hartz2024art]]
- [[jiang2024manipulation]]
## 证据元数据

- **Fulltext Quality**: fulltext
- **Evidence Coverage**: 读取了全文，包括 abstract、introduction (Sec I)、benchmark design (Sec II)、trial protocol (Sec III)、performance metrics (Sec IV)、exemplary solution (Sec V)、results (Sec VI)、tables (I-X)、figures (1-10)
- **Confidence**: high — 全文完整，ICRA 2025，TUM + MBZUAI + NYU Abu Dhabi，UR5e + Robotiq HAND-E，电子任务板基准，16 机器人团队+30 人类被试，最佳机器人比最佳人类慢 29 秒，5262 次试验数据库
- **Summary**: 提出基于联网电子任务板的机器人操控基准，用于评估电气电路检查（万用表使用）的人机技能差距。6 个子任务：定位任务板+按键→读取屏幕+调整滑块→插入探针插头→开门+探针电路→缠绕电缆→按键停止。Robothon Grand Challenge 2023：16 团队参赛，9 队完成全部任务。最佳机器人（UR5e + Robotiq HAND-E + RealSense D435i）比最佳人类慢 29 秒（57.0s vs 44.7s 剔除 ST1），但缠绕电缆子任务优于人类。80 块任务板全球部署，5262 次试验数据库


## Problem

机器人操控研究常以人类表现为目标，但缺乏标准化物理基准进行人机对比。需要设计可追溯、可重复、自动评分的真实世界基准来量化人机技能差距。


## Method

- **任务板设计**：
  - 3D 打印 ABS 外壳 + 商用组件 + ESP32 微控制器
  - I2C 传感器总线：滑块电位器、门角度传感器、光学传感器
  - WiFi 上报遥测数据到 KaaIoT 网页面板
  - 300mAh 锂电池（30 分钟无线操作）
- **6 个子任务**：
  - ST1: 定位任务板 + 按蓝色按钮
  - ST2: 读取 LED 屏幕随机目标 + 调整滑块到目标位置
  - ST3: 拾取探针插头 + 插入测试端口（peg-in-hole）
  - ST4: 用探针撬开门 + 探针电路终端块
  - ST5: 缠绕探针电缆围绕传感器化门柱（可变形物体操控）
  - ST6: 按停止按钮
- **示例机器人方案**：
  - UR5e + Robotiq HAND-E + RealSense D435i（腕部）
  - YOLOv8 检测任务板位置
  - 力控（3N 按钮按压）+ 螺旋搜索（插头插入）
  - 3D 打印钩形工具用于缠绕电缆
- **评估指标**：完成任务数、执行时间、系统复杂度、技能开发率、技能可迁移性


## Experiments

- **Robothon Grand Challenge 2023**：
  - 16 团队参赛（9 队完成全部任务）
  - 30 天开发期
  - 5262 次试验（4552 次机器人）
- **人机对比**：
  - 最佳人类：44.7s（完整流程）
  - 最佳机器人团队：57.0s → 差距 29s（因 ST1 人类有定位优势）
  - 优化后机器人：44.7s（去除 ST1 后计算）
  - 缠绕电缆子任务：机器人优于人类
- **失败率**：
  - ST2（滑块）和 ST5（缠绕）最困难
  - 机器人团队成功率 56%（单次试验）
  - 人类成功率 100%
- **观察**：
  - 系统复杂度与性能不相关（双臂平台表现不如单臂）
  - 力控方法比轨迹方法慢
  - BYOD 挑战：多样物体（电池、键盘、电源板、显示器）


## Limitations

1. 基准仅覆盖电路检查场景，不涵盖所有操控技能
2. 滑块任务存在作弊可能（不读屏幕直接推满）
3. 任务板位置需人工重新放置
4. WiFi 依赖可能影响遥测上报
5. 30 人人类样本可能不够代表性


## Key Takeaways

- 物理基准+自动评分比仿真基准更真实：真实接触力+可变形物体
- 人机差距主要集中在精细操控（滑块、缠绕）：力感知和可变形物体是瓶颈
- 缠绕电缆机器人可优于人类：规划+执行组合好时机器人有优势
- 开源+联网设计促进社区参与：80 块任务板全球部署
- 比赛模式加速技术进步：30 天内多团队并行开发

## 相关概念

- [[robotic-manipulation]]
- [[deformable-linear-object]]
- [[bimanual-manipulation]]

## 相关研究者

- [[so|So, Peter]]
- [[swikir|Swikir, Abdalla]]
- [[haddadin|Haddadin, Sami]]
