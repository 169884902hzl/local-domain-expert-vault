---
title: "Multi-stage reinforcement learning for non-prehensile manipulation"
tags: [manipulation, RL]
created: "2026-04-25"
updated: "2026-04-25"
type: "literature"
status: "done"
summary: "提出 MRLM（Multi-stage RL for Manipulation），4 阶段课程式强化学习框架用于非预抓取操控（先 push 后 grasp）。关键技术：(1) 点云状态-目标融合（将目标物体点云与场景点云拼接作为状态表示）；(2) 空间可达距离（spatially-reachable distance）作为奖励函数核心指标；(3) 自动缓冲区压缩（automatic buffer compaction）解决课程 RL 中阶段转换的经验不匹配问题；(4) 自动域随机化（ADR）增强 Sim-to-Real 迁移。仿真远距离抓取 100%，近距离 95%；真实零样本远距离 95%，近距离 67.5%"
authors: "Wang, Dexin; Chang, Faliang; Liu, Chunsheng"
year: "2023"
venue: "arXiv Preprint"
zotero_key: "HRWPGT7R"
---
## 摘要

Manipulating objects without grasping（抓取） them enables more complex tasks, known as non-prehensile manipulation（操控）. Most previous methods only learn one manipulation（操控） skill, such as reach or push, and cannot achieve flexible object manipulation（操控）. In this work, we introduce MRLM, a Multi-stage Reinforcement Learning（强化学习） approach for non-prehensile Manipulation（操控） of objects. MRLM divides the task into multiple stages according to the switching of object poses and contact points. At each stage, the policy takes the point cloud（点云）-based stategoal fusion representation as input, and proposes a spatiallycontinuous action that including the motion of the parallel gripper pose and opening width. To fully unlock the potential of MRLM, we propose a set of technical contributions including the state-goal fusion representation, spatially-reachable distance metric, and automatic buffer compaction. We evaluate MRLM on an Occluded Grasping（抓取） task which aims to grasp the object in configurations that are initially occluded. Compared with the baselines, the proposed technical contributions improve the success rate by at least 40% and maximum 100%, and avoids falling into local optimum. Our method demonstrates strong generalization to unseen object with shapes outside the training distribution. Moreover, MRLM can be transferred to real world with zero-shot（零样本） transfer, achieving a 95% success rate. Code and videos can be found at https://sites.google.com/view/mrlm.


## 中文简述

提出基于强化学习的抓取方法，具有零样本泛化特点。

**研究方向**: 机器人操控、强化学习

## 关键贡献

1. 4 阶段课程式 RL 训练：reach→push→grasp→lift，逐阶段继承和微调策略
2. 点云状态-目标融合：将目标物体点云与场景点云拼接，提供更好的目标感知
3. 空间可达距离奖励：基于末端执行器与目标的空间可达性设计稠密奖励
4. 自动缓冲区压缩：在课程阶段转换时清理不兼容的 replay buffer 经验
5. ADR 自动域随机化：自适应调节仿真参数随机化范围以促进 Sim-to-Real
## 结构化提取

- **Problem**: 非预抓取操控的多阶段 RL 训练与 Sim-to-Real 迁移
- **Method**: MRLM — 4 阶段课程 RL (reach→push→grasp→lift) + 点云状态-目标融合 + 空间可达距离 + 自动缓冲区压缩 + ADR
- **Tasks**: 桌面物体 push+grasp（远/近距离）
- **Sensors**: RGB-D 相机（仿真+真实）
- **Robot Setup**: UR5e + Robotiq 2F-140 gripper
- **Metrics**: 抓取成功率（仿真/真实）
- **Limitations**: 仅桌面场景、近距离成功率有限、固定课程结构
- **Evidence Notes**: 全文读取，Tables I-III 提供消融对比
## 本地引用关系

- [[gao2024prime]]
- [[karim2024davil]]
- [[li2025routing]]
- [[liu2025oneshot]]
- [[wang2023hierarchical]]
## 证据元数据

- **Fulltext Quality**: fulltext
- **Evidence Coverage**: 读取了全文，包括 abstract、introduction (Sec I)、related work (Sec II)、method (Sec III-IV)、experiments (Sec V)、tables (I-III)、figures (1-8)
- **Confidence**: high — 全文完整，arXiv 2023，Shandong University，UR5e + Robotiq 2F-140，4 阶段课程 RL（reach→push→grasp→lift），点云状态-目标融合+空间可达距离+自动缓冲区压缩+ADR，仿真 100% 远抓取/95% 近抓取，真实零样本 Sim-to-Real 95%/67.5%
- **Summary**: 提出 MRLM（Multi-stage RL for Manipulation），4 阶段课程式强化学习框架用于非预抓取操控（先 push 后 grasp）。关键技术：(1) 点云状态-目标融合（将目标物体点云与场景点云拼接作为状态表示）；(2) 空间可达距离（spatially-reachable distance）作为奖励函数核心指标；(3) 自动缓冲区压缩（automatic buffer compaction）解决课程 RL 中阶段转换的经验不匹配问题；(4) 自动域随机化（ADR）增强 Sim-to-Real 迁移。仿真远距离抓取 100%，近距离 95%；真实零样本远距离 95%，近距离 67.5%


## Problem

非预抓取操控（如先推动再抓取）需要长时序策略协调多种原语。现有 RL 方法要么仅学习单一原语，要么缺乏有效的课程训练机制，无法从仿真高效迁移到真实世界。


## Method

- **观察空间**：
  - 场景点云（RGB-D → 点云）
  - 目标物体点云（分割后）
  - 两者拼接为状态表示
- **动作空间**：末端执行器 6D 位姿增量
- **4 阶段课程**：
  - Stage 1 (Reach)：移动到目标附近
  - Stage 2 (Push)：推动目标到可抓取位置
  - Stage 3 (Grasp)：抓取目标
  - Stage 4 (Lift)：举起目标
  - 每阶段继承上一阶段的策略参数和部分经验
- **空间可达距离**：
  - 综合考虑末端执行器与目标距离+可达性约束
  - 提供比纯欧氏距离更有效的稠密奖励信号
- **自动缓冲区压缩**：
  - 阶段转换时清理与新阶段不兼容的经验
  - 防止旧分布经验干扰新阶段策略学习
- **ADR（自动域随机化）**：
  - 自适应调节仿真参数（物体属性、光照、相机位姿等）的随机化范围
  - 基于策略在已随机化环境中的表现动态扩大范围
- **RL 算法**：SAC（Soft Actor-Critic）


## Experiments

- **仿真实验**（PyBullet，UR5e + Robotiq 2F-140）：
  - 远距离抓取：100%（100/100）
  - 近距离抓取：95%（95/100）
  - 对比方法：单一 RL 策略、无课程多阶段、无缓冲区压缩
  - 缓冲区压缩提升 ~10% 成功率
  - 空间可达距离奖励优于纯距离奖励
- **真实世界实验**（零样本 Sim-to-Real）：
  - 远距离抓取：95%（19/20）
  - 近距离抓取：67.5%（27/40）
  - ADR 对真实世界迁移至关重要
  - 无 ADR 时真实成功率大幅下降


## Limitations

1. 仅在桌面抓取-推动场景验证，未扩展到更复杂操控任务
2. 近距离抓取真实成功率（67.5%）仍有提升空间
3. 依赖物体分割获取目标点云，分割失败影响整体性能
4. 固定 4 阶段课程，不适应所有任务结构
5. 未与其他 Sim-to-Real 方法（如 RCAN）进行对比


## Key Takeaways

- 多阶段课程式 RL 有效分解非预抓取操控：push+grasp 组合优于端到端策略
- 点云状态-目标融合提供清晰的目标感知：比单一 RGB/D 更适合目标导向任务
- 自动缓冲区压缩解决课程 RL 的分布偏移：简单的经验清理即可显著提升性能
- ADR 是 Sim-to-Real 迁移的关键：自适应随机化优于固定范围随机化
- 空间可达距离比纯距离更适合操控奖励设计：考虑运动学约束

## 相关概念

- [[robotic-manipulation]]
- [[reinforcement-learning]]
- [[bimanual-manipulation]]
- [[grasping]]

## 相关研究者

- [[wang-dexin|Wang, Dexin]]
