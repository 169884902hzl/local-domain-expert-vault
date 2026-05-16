---
title: "ZeroMimic: Distilling robotic manipulation skills from web videos"
tags: [manipulation, imitation]
created: "2026-04-25"
updated: "2026-04-25"
type: "literature"
status: "done"
summary: "提出 ZeroMimic，从 EpicKitchens 自我中心人类视频中零样本蒸馏机器人操控技能。两阶段：(1) 抓取阶段：VRB（交互可供性预测）→ AnyGrasp（抓取选择）；(2) 后抓取阶段：HaMeR 手部追踪 + COLMAP SfM → 6D 腕部轨迹提取 → ACT 模仿学习策略。9 类技能（开/关抽屉/柜门、倒、取放、切、搅），零样本真实世界 Franka 71.0%/WidowX 65.0%，仿真 73.8%。超越 ReKep（开抽屉 8/10 vs 0/10）。失败分析：31.1% AnyGrasp、24.1% VRB、44.8% 后抓取策略"
authors: "Shi, Junyao; Zhao, Zhuolun; Wang, Tianyou; Pedroza, Ian; Luo, Amy et al."
year: "2025"
venue: "arXiv Preprint"
zotero_key: "B6GITSX9"
---
## 摘要

Many recent advances in robotic manipulation（机器人操控） have come through imitation learning（模仿学习）, yet these rely largely on mimicking a particularly hard-to-acquire form of demonstrations: those collected on the same robot in the same room with the same objects as the trained policy must handle at test time. In contrast, large pre-recorded human video datasets demonstrating manipulation（操控） skills in-the-wild already exist, which contain valuable information for robots. Is it possible to distill a repository of useful robotic skill policies out of such data without any additional requirements on robot-specific demonstrations or exploration? We present the first such system ZeroMimic, that generates immediately deployable image goalconditioned skill policies for several common categories of manipulation（操控） tasks (opening, closing, pouring, pick&place, cutting, and stirring) each capable of acting upon diverse objects and across diverse unseen task setups. ZeroMimic is carefully designed to exploit recent advances in semantic and geometric visual understanding of human videos, together with modern grasp affordance（可供性） detectors and imitation policy classes. After training ZeroMimic on the popular EpicKitchens dataset of ego-centric human videos, we evaluate its out-of-thebox performance in varied real-world and simulated kitchen settings with two different robot embodiments, demonstrating its impressive abilities to handle these varied tasks. To enable plug-and-play reuse of ZeroMimic policies on other task setups and robots, we release software and policy checkpoints of our skill policies.


## 中文简述

提出基于模仿学习的抓取方法，具有人类视频学习特点。

**研究方向**: 机器人操控、模仿学习

## 关键贡献

1. 首个从野外人类视频零样本蒸馏多技能机器人策略的系统
2. 两阶段分解（affordance 抓取 + 6D 腕部轨迹后抓取）有效桥接人机差距
3. SfM 相机校正是关键：解决自我中心视频的相机运动问题
4. 跨机器人平台验证：Franka + WidowX 均可部署
## 结构化提取

- **Problem**: 从野外人类视频零样本蒸馏机器人操控技能
- **Method**: ZeroMimic — VRB affordance + AnyGrasp 抓取 + HaMeR+COLMAP+SfM 轨迹提取 + ACT 策略
- **Tasks**: 9 类技能（开/关抽屉/柜门、倒、取放、切、搅）
- **Sensors**: Zed 2 立体相机/RealSense D435（RGB-D）
- **Robot Setup**: Franka Emika Panda + Robotiq 2F / WidowX 250S + 2F gripper
- **Metrics**: 零样本任务成功率（10 trials/场景）
- **Limitations**: 两阶段仅、无灵巧操控、依赖预训练模型上限
- **Evidence Notes**: 全文读取，Tables I-V 提供完整消融，Table IV 提供逐技能逐场景成功率
## 本地引用关系

- [[chen2025vividex]]
- [[dalal2025local]]
- [[nasiriany2025rtaffordance]]
- [[patel2025realtosimtoreal]]
- [[singh2025handobject]]
## 证据元数据

- **Fulltext Quality**: fulltext
- **Evidence Coverage**: 读取了全文，包括 abstract、introduction (Sec I)、related work (Sec II)、method (Sec III)、experiments (Sec IV)、tables (I-V)、figures (1-13)、appendix
- **Confidence**: high — 全文完整，arXiv 2025，University of Pennsylvania，Franka Panda + WidowX 250S 两种机器人，9 类技能×30 真实场景+4 仿真场景，零样本真实世界 71.0%，仿真 73.8%，超越 ReKep 基线
- **Summary**: 提出 ZeroMimic，从 EpicKitchens 自我中心人类视频中零样本蒸馏机器人操控技能。两阶段：(1) 抓取阶段：VRB（交互可供性预测）→ AnyGrasp（抓取选择）；(2) 后抓取阶段：HaMeR 手部追踪 + COLMAP SfM → 6D 腕部轨迹提取 → ACT 模仿学习策略。9 类技能（开/关抽屉/柜门、倒、取放、切、搅），零样本真实世界 Franka 71.0%/WidowX 65.0%，仿真 73.8%。超越 ReKep（开抽屉 8/10 vs 0/10）。失败分析：31.1% AnyGrasp、24.1% VRB、44.8% 后抓取策略


## Problem

机器人模仿学习依赖昂贵的同机器人同场景演示数据。大量野外人类操作视频（如 EpicKitchens）已存在，包含丰富的技能信息。如何仅从野外人类视频中蒸馏出可零样本部署的机器人操控技能策略，无需任何机器人特定数据？


## Method

- **抓取阶段**：
  - VRB（预训练于 EpicKitchens）→ 输入 RGB + 语言指令 → 输出像素级交互接触点
  - AnyGrasp → 在 VRB 推荐区域附近生成最佳抓取
  - 线性末端执行器轨迹执行抓取
- **后抓取阶段**：
  - 数据来源：EpicKitchens（100 小时，20M 帧）
  - HaMeR（3D 手部追踪）→ 腕部关节 6D 位姿
  - COLMAP + EPIC-Fields → 自我中心相机的世界坐标系外参
  - 腕部轨迹从像素坐标转换为世界 3D 坐标
  - ACT 策略：输入（当前图像 + 目标图像 + 当前腕部位姿）→ 输出（未来 n=10 步 6D 腕部位姿）
  - 相对动作表示（relT+relO）优于绝对表示
- **训练**：每技能独立训练 1000 epochs，约 18 小时/技能（RTX 3090）
- **部署**：直接将腕部轨迹重定向到机器人末端执行器


## Experiments

- **9 类技能零样本评估**（真实世界 Franka，30 场景×18 物体类别）：
  - Hinge Open: 6-9/10, Hinge Close: 4-10/10
  - Slide Open/Close: 6-10/10
  - Pouring: 4-8/10 (water/food/salt)
  - Picking: 4-7/10, Placing: 4-10/10
  - Cutting: 8/10 (tofu/banana/cake)
  - Stirring: 3-8/10
  - 总体：71.0%（Franka），65.0%（WidowX）
- **仿真评估**（RoboCasa，4 技能×20 随机场景）：73.8%
- **消融**：
  - SfM 相机信息：Open Drawer 10/10 vs 4/10（无 SfM）
  - Affordance 抓取 vs 直接 AnyGrasp：Drawer Handle 8/10 vs 0/10
  - 相对 vs 绝对动作：relT+relO 7/10 vs absT+absO 1/10
  - ACT vs Diffusion Policy：性能相当
- **对比 ReKep**：
  - Open Drawer: 8/10 vs 0/10
  - Close Drawer: 6/10 vs 6/10
  - Place Pasta: 8/10 vs 4/10
  - Pour: 8/10 vs 0/10


## Limitations

1. 仅支持预抓取+后抓取两阶段技能，不支持非预抓取交互
2. 直接重定向人类腕部运动，未考虑形态差异
3. 不支持灵巧手内操控、双臂任务
4. 依赖 VRB/AnyGrasp/HaMeR 等预训练模型的上限
5. 仅在 EpicKitchens（100 小时）上训练，可扩展到更大数据集


## Key Takeaways

- SfM 相机校正是从自我中心视频学习 3D 策略的关键
- 两阶段分解（affordance 抓取 + 轨迹后抓取）简化了问题
- 相对动作表示远优于绝对表示：7/10 vs 1/10
- 野外人类视频足以蒸馏出零样本可用的多技能策略
- 100 小时视频数据已能覆盖 9 类常见厨房操控技能

## 相关概念

- [[robotic-manipulation]]
- [[imitation-learning]]
- [[diffusion-model]]
- [[bimanual-manipulation]]
- [[grasping]]

## 相关研究者

- [[shi|Shi, Junyao]]
