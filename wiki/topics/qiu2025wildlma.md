---
title: "WildLMa: Long Horizon Loco-Manipulation in the Wild"
tags: [manipulation, VLM, imitation]
created: "2026-04-25"
updated: "2026-04-25"
type: "literature"
status: "done"
summary: "提出 WildLMa 框架用于四足机器人野外长时序 loco-manipulation。三组件：(1) VR 遥操作全身控制器（减少演示成本 26.9%）；(2) WildLMa-Skill：CLIP+MaskCLIP 重参数化 + 图像-文本交叉注意力 + ACT 模仿学习，30-60 演示/技能；(3) WildLMa-Planner：层次化 LLM 规划器（粗→细搜索）。技能平均成功率 71.2%（vs ACT 40.8%、VBC 46.9%），O.O.D. grasping 75%（vs ACT 19.4%）。长时序：Pipeline 7/10，Shelf 3/10"
authors: "Qiu, Ri-Zhao; Song, Yuchen; Peng, Xuanbin; Suryadevara, Sai Aneesh; Yang, Ge et al."
year: "2025"
venue: "2025 IEEE International Conference on Robotics and Automation (ICRA)"
zotero_key: "MC8EAFJB"
---
## 摘要

In-the-wild’ mobile manipulation（移动操控） aims to deploy robots in diverse real-world environments, which requires the robot to (1) have skills that generalize across object configurations; (2) be capable of long-horizon（长时序） task execution in diverse environments; and (3) perform complex manipulation（操控） beyond pick-and-place. Quadruped robots with manipulators hold promise for extending the workspace and enabling robust locomotion, but existing results do not investigate such a capability. This paper proposes WildLMa with three components to address these issues: (1) adaptation of learned lowlevel controller for VR-enabled whole-body teleoperation and traversability; (2) WildLMa-Skill — a library of generalizable visuomotor skills acquired via imitation learning（模仿学习） or heuristics and (3) WildLMa-Planner — an interface of learned skills that allow LLM planners to coordinate skills for long-horizon（长时序） tasks. We demonstrate the importance of high-quality training data by achieving higher grasping（抓取） success rate over existing RL baselines using only tens of demonstrations. WildLMa exploits CLIP for language-conditioned imitation learning（模仿学习） that empirically generalizes to objects unseen in training demonstrations. Besides extensive quantitative evaluation, we qualitatively demonstrate practical robot applications, such as cleaning up trash in university hallways or outdoor terrains, operating articulated objects, and rearranging items on a bookshelf.

## 中文简述

提出基于模仿学习的抓取方法，具有泛化能力特点。

**研究方向**: 机器人操控、视觉-语言模型、模仿学习

## 证据元数据

- **Fulltext Quality**: fulltext
- **Evidence Coverage**: 读取了全文，包括 abstract、introduction (Sec I)、related work (Sec II)、method (Sec III)、experiments (Sec IV)、tables (I-VI)、figures (1-4)
- **Confidence**: high — 全文完整，ICRA 2025，UCSD+MIT，Unitree B1+Z1 四足操控机器人，3 技能×2 设置（I.D./O.O.D.）+ 2 长时序任务，全面对比 ACT/Mobile ALOHA/OpenTV/VBC/GeFF 基线
- **Summary**: 提出 WildLMa 框架用于四足机器人野外长时序 loco-manipulation。三组件：(1) VR 遥操作全身控制器（减少演示成本 26.9%）；(2) WildLMa-Skill：CLIP+MaskCLIP 重参数化 + 图像-文本交叉注意力 + ACT 模仿学习，30-60 演示/技能；(3) WildLMa-Planner：层次化 LLM 规划器（粗→细搜索）。技能平均成功率 71.2%（vs ACT 40.8%、VBC 46.9%），O.O.D. grasping 75%（vs ACT 19.4%）。长时序：Pipeline 7/10，Shelf 3/10
## 关键贡献

1. VR 遥操作全身控制：减少跨具身差距，提高数据采集效率 26.9%
2. CLIP + 交叉注意力语言条件 IL：显著提升 O.O.D. 泛化（75% vs 19.4%）
3. 层次化 LLM 规划器：粗分解+细搜索实现长时序任务
4. 完整的四足 loco-manipulation 框架：从数据采集到部署
## 结构化提取

- **Problem**: 野外四足机器人泛化技能 + 长时序操控
- **Method**: WildLMa — VR 遥操作 + CLIP 交叉注意力 IL + 层次化 LLM 规划
- **Tasks**: Tabletop/Ground Grasping, Button Press, Door, Pipeline, Shelf Rearrangement
- **Sensors**: Azure Kinect（头）+ D405（腕）+ LIVOX MID-360（LiDAR）
- **Robot Setup**: Unitree B1 四足 + Z1 臂 + 3D 打印夹爪
- **Metrics**: 单技能成功率 + 长时序任务成功率
- **Limitations**: 预标注航点、每技能独立训练、长时序成功率偏低
- **Evidence Notes**: 全文读取，Tables I-VI 提供完整对比和消融
## 本地引用关系

- [[chen2025effective]]
- [[chuang2025active]]
- [[liu2025autonomous]]
- [[liu820enhancing]]
## Problem

野外移动操控需要：(1) 泛化到未见物体/环境的技能；(2) 长时序任务执行能力；(3) 超越 pick-and-place 的复杂操控。现有模块化方法仅限简单拾取放置，端到端方法泛化性差且长时序累积误差。四足+机械臂平台有潜力扩展工作空间，但缺乏系统化的学习框架。


## Method

- **全身 VR 遥操作**：
  - Apple Vision Pro + OpenTV 框架
  - 右手 → 末端执行器位姿（线性缩放）
  - 左手 → 底座速度（虚拟摇杆，死区 5cm）
  - 捏合手势 → 夹爪开合
  - 学习型全身控制器（VBC）自动协调臂基运动
- **WildLMa-Skill（模仿学习）**：
  - CLIP ViT-B/16 + MaskCLIP 重参数化 → 特征图
  - 图像-文本交叉注意力：CROSSATT = g_visual · f_text / (||g||·||f||)（像素级余弦相似度）
  - 训练时 dropout 避免过度依赖注意力
  - 自主终止信号：最后 10 帧标记 'end'，滑动窗口检测连续 10 帧 > τ=0.8
- **WildLMa-Planner**：
  - 初始建图：LiDAR SLAM（FAST-LIO+DLO）+ GPT-4V 语义标注 + 层次场景图
  - 粗规划器：Chain-of-Thought 分解指令为子任务
  - 细规划器：BFS 搜索节点 + LLM 启发式评估 → 技能序列
  - 分析式导航：PD 路径跟踪（已知航点间）
- **硬件平台**：Unitree B1 四足 + Z1 臂 + 3D 打印软夹爪 + Azure Kinect（头）+ D405（腕）+ LIVOX MID-360（尾 LiDAR）


## Experiments

- **单技能评估**（3 技能 × I.D./O.O.D.）：
  - WildLMa: Tabletop Grasp 94.4%/75%, Button Press 80%/57.5%, Ground Grasp 60%/60%, Avg 71.2%
  - ACT (Mobile ALOHA): 77.8%/19.4%, 55%/25%, 60%/30%, Avg 40.8%
  - OpenTV (DinoV2): 88.9%/77.8%, 75%/25%, 50%/50%, Avg 64.4%
  - VBC (RL): 50%/50%, NA/NA, 43.8%/43.8%, Avg 46.9%
  - GeFF (zero-shot): 55.6%/55.6%, NA/NA, NA/NA, Avg 55.6%
- **长时序任务**（Pipeline=收垃圾放垃圾桶, Shelf=书架重排）：
  - WildLMa: 7/10, 3/10
  - ACT: 0/10, 0/10
- **消融**：
  - CLIP vs ResNet vs DinoV2：O.O.D. 分别 69.4%/19.4%/77.8%
  - 交叉注意力：+8.3% 平均提升（84.7% vs 76.4%）
  - 多相机 vs 单相机：遮挡任务显著受益（桌面抓取 94.4% vs 27.8%）
  - 全身控制 vs 解耦：减少平均时间，提高成功率（95% vs 40% 地面抓取）


## Limitations

1. 导航依赖预标注航点（非自主探索）
2. 每技能需独立训练权重（非统一策略）
3. 仅在室内+有限室外环境验证
4. LLM 规划器未充分探索重规划能力
5. 长时序 Shelf 任务成功率偏低（3/10）


## Key Takeaways

- 高质量演示数据比 RL 更有效：30-60 条演示即可超越 RL 基线
- CLIP 交叉注意力是泛化关键：使语言条件 IL 泛化到未见物体
- 全身控制器扩展工作空间：使四足机器人能操作地面到高处的物体
- 原子技能+LLM 组合优于端到端长时序策略：减少累积误差
- VR 遥操作降低数据采集门槛：全身控制使四足遥操作自然

## 相关概念

- [[robotic-manipulation]]
- [[vision-language-model]]
- [[imitation-learning]]
- [[deformable-linear-object]]
- [[bimanual-manipulation]]
- [[grasping]]

## 相关研究者

- [[qiu|Qiu, Ri-Zhao]]
