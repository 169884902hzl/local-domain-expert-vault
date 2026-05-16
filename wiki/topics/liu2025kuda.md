---
title: "KUDA: Keypoints to unify dynamics learning and visual prompting for open-vocabulary robotic manipulation"
tags: [manipulation, VLM]
created: "2026-04-25"
updated: "2026-04-25"
type: "literature"
status: "done"
summary: "提出 KUDA，用关键点统一 VLM 视觉提示和动力学学习。SAM 分割 → FPS 采样关键点 → VLM(GPT-4o) 生成代码式目标规范（关键点空间关系）→ 转换为 cost function → 神经动力学模型+MPPI 规划。6 任务总成功率 80%（vs MOKA/VoxPoser 13.3%），Top-K 提示库+检索机制提升 VLM 性能，双层闭环控制（低层 MPPI+高层 VLM 重规划）"
authors: "Liu, Zixian; Zhang, Mingtong; Li, Yunzhu"
year: "2025"
venue: "arXiv Preprint"
zotero_key: "N7TE5Z54"
---
## 摘要

With the rapid advancement of large language models (LLMs) and vision-language models (VLMs), significant progress has been made in developing open-vocabulary robotic manipulation（机器人操控） systems. However, many existing approaches overlook the importance of object dynamics, limiting their applicability to more complex, dynamic tasks. In this work, we introduce KUDA, an open-vocabulary manipulation（操控） system that integrates dynamics learning and visual prompting through keypoints, leveraging both VLMs and learning-based neural dynamics models. Our key insight is that a keypoint-based target specification is simultaneously interpretable by VLMs and can be efficiently translated into cost functions for model-based planning. Given language instructions and visual observations, KUDA first assigns keypoints to the RGB image and queries the VLM to generate target specifications. These abstract keypointbased representations are then converted into cost functions, which are optimized using a learned dynamics model to produce robotic trajectories. We evaluate KUDA on a range of manipulation（操控） tasks, including free-form language instructions across diverse object categories, multi-object interactions, and deformable or granular objects, demonstrating the effectiveness of our framework. The project page is available at http: //kuda-dynamics.github.io.

## 中文简述

提出基于视觉-语言的操控方法。

**研究方向**: 机器人操控、视觉-语言模型

## 证据元数据

- **Fulltext Quality**: fulltext
- **Evidence Coverage**: 读取了全文，包括 abstract、introduction、related work (Sec II)、method (Sec III)、experiments (Sec IV)、tables (I-III)、figures (1-4)
- **Confidence**: high — 全文完整，arXiv 2025 预印本，6 任务 4 类物体（rope/cubes/granular/T-shape），60 次试验，对比 MOKA 和 VoxPoser
- **Summary**: 提出 KUDA，用关键点统一 VLM 视觉提示和动力学学习。SAM 分割 → FPS 采样关键点 → VLM(GPT-4o) 生成代码式目标规范（关键点空间关系）→ 转换为 cost function → 神经动力学模型+MPPI 规划。6 任务总成功率 80%（vs MOKA/VoxPoser 13.3%），Top-K 提示库+检索机制提升 VLM 性能，双层闭环控制（低层 MPPI+高层 VLM 重规划）
## 关键贡献

1. 关键点作为统一中间表示：同时可被 VLM 解释和转换为 cost function
2. VLM 生成代码式目标规范（p = r + [dx, dy, dz]），可翻译为 MPPI 优化目标
3. Top-K 提示库 + CLIP 检索机制，自动选择最优 few-shot 示例
4. 双层闭环控制：低层 MPPI + 高层 VLM 重规划（修正不完美目标规范）
## 结构化提取

- **Problem**: 开放词汇操控中动力学缺失 + 语言到 cost function 的映射
- **Method**: KUDA — SAM+FPS关键点 → VLM(GPT-4o)代码目标规范 → cost function → 神经动力学+MPPI
- **Tasks**: Rope/Cubes/Granular/T-shape（桌面 6 任务）
- **Sensors**: RGB-D 相机（俯视）
- **Robot Setup**: 桌面机械臂（未指定型号）
- **Metrics**: 成功率（Chamfer distance 阈值）
- **Limitations**: 俯视相机、sim-to-real gap、依赖分割质量
- **Evidence Notes**: 全文读取，Tables I-III 提供完整对比和消融结果
## 本地引用关系

- [[ao2025llmasbtplanner]]
- [[dalal2025local]]
- [[garcia2025generalizable]]
- [[lips2024keypoints]]
- [[patel2025realtosimtoreal]]
## Problem

开放词汇机器人操控系统中，现有方法（VoxPoser、MOKA）忽视物体动力学，仅适用于刚体粗粒度操控。学习型动力学模型可预测复杂物体行为但需要预定义目标/cost function，无法直接从自然语言指令推断。


## Method

- **关键点采样与标注**：SAM 分割 → Farthest Point Sampling → 标注在 RGB 图像上
- **VLM 目标规范**：GPT-4o 为每个关键点 k 指定目标位置 p = r + [dx,dy,dz]（r 为参考点）
- **Top-K 提示库**：
  - CLIP 编码观察+指令和库中示例
  - 匹配分数：S = fI(s)·fI(obs) + λ·fT(L)·fT(q)（λ=0.6）
  - 选择 Top-K（K=3 最佳）作为 few-shot 输入
- **Cost Function**：C(z|L) = Σ‖oi - pi‖₂，从关键点目标规范投影到 3D 空间
- **规划**：MPPI 算法 + 神经动力学模型（图网络/MLP）
- **双层闭环**：
  - 低层：每步 MPPI 重规划
  - 高层：若干步后 VLM 重新查询更新目标规范


## Experiments

- **定量结果（10 trials/task，6 tasks）**：
  - Rope Straightening：8/10 vs MOKA 2/10, VoxPoser 0/10
  - Cube Collection：6/10 vs MOKA 0/10, VoxPoser 3/10
  - Cube Movement：10/10 vs MOKA 6/10, VoxPoser 3/10
  - Granular Collection：10/10 vs MOKA 0/10, VoxPoser 1/10
  - Granular Movement：6/10 vs MOKA 0/10, VoxPoser 1/10
  - T Movement：8/10 vs MOKA 0/10, VoxPoser 0/10
  - **Total：80.0% vs 13.3% vs 13.3%**
- **错误分析（60 trials）**：
  - 感知错误 10%（主要失败源）：重叠物体、相邻物体混淆
  - VLM 目标规范不足 3.3%
  - 跟踪失败 3.3%
  - 动力学模型失败 1.7%
- **Top-K 消融**：K=3 最佳（10/10），K=0（零样本 2/10），K=5（引入无关示例 7/10）


## Limitations

1. 仅用俯视相机，难以处理复杂 3D 空间关系
2. 动力学模型在仿真中训练，存在 sim-to-real gap
3. 依赖 SAM 分割质量
4. VLM 可能生成不可行的目标规范
5. 仅在桌面场景验证


## Key Takeaways

- 关键点是连接 VLM 和动力学模型的优雅桥梁：VLM 理解空间关系，动力学模型预测物理结果
- 代码式目标规范比直接输出动作更适合复杂操控：允许近似目标→优化即可
- Few-shot 示例的质量 > 数量（K=3 > K=5）
- 双层闭环是关键：低层动力学修正执行误差，高层 VLM 修正规划误差
- 动力学知识是开放词汇操控超越简单 pick-place 的关键

## 相关概念

- [[robotic-manipulation]]
- [[vision-language-model]]
- [[deformable-linear-object]]

## 相关研究者

- [[liu-zixian|Liu, Zixian]]
- [[li-yunzhu|Li, Yunzhu]]
