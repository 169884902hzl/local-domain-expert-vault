---
title: "MuST: Multi-Head Skill Transformer for Long-Horizon Dexterous Manipulation with Skill Progress"
tags: [manipulation]
created: "2026-04-25"
updated: "2026-04-25"
type: "literature"
status: "done"
summary: "提出 MuST（Multi-Head Skill Transformer），在 Octo 骨干上增加 N+1 个 head（N 个技能 head + 1 个进度 head），通过进度引导的技能选择器 ProGSS 确定执行顺序，Pick-n-Pack 任务完成率从 Octo 基线 32.5% 提升至 90%，真实世界 88%"
authors: "Gao, Kai; Wang, Fan; Aduh, Erica; Randle, Dylan; Shi, Jane"
year: "2025"
venue: "2025 IEEE International Conference on Robotics and Automation (ICRA)"
zotero_key: "PCN4I2LM"
---
## 摘要

Robot picking and packing tasks require dexterous manipulation（灵巧操控） skills, such as rearranging objects to establish a good grasping（抓取） pose, or placing and pushing items to achieve tight packing. These tasks are challenging for robots due to the complexity and variability of the required actions. To tackle the difficulty of learning and executing long-horizon（长时序） tasks, we propose a novel framework called the Multi-Head Skill Transformer (MuST). This model is designed to learn and sequentially chain together multiple motion primitives (skills), enabling robots to perform complex sequences of actions effectively. MuST introduces a “progress value” for each skill, guiding the robot on which skill to execute next and ensuring smooth transitions between skills. Additionally, our model is capable of expanding its skill set and managing various sequences of sub-tasks efficiently. Extensive experiments in both simulated and real-world environments demonstrate that MuST significantly enhances the robot’s ability to perform long-horizon（长时序） dexterous manipulation（灵巧操控） tasks.

## 中文简述

提出基于Transformer的抓取方法，具有长时序任务特点。

**研究方向**: 机器人操控

## 证据元数据

- **Fulltext Quality**: fulltext
- **Evidence Coverage**: 读取了全文，包括 abstract、introduction、related work、method (Sec III-IV)、experiments (Sec V)、tables (I-VI)、figures (1-9)
- **Confidence**: high — 全文完整，ICRA 2025 正式发表，仿真和真实世界 Pick-n-Pack 任务系统评估充分
- **Summary**: 提出 MuST（Multi-Head Skill Transformer），在 Octo 骨干上增加 N+1 个 head（N 个技能 head + 1 个进度 head），通过进度引导的技能选择器 ProGSS 确定执行顺序，Pick-n-Pack 任务完成率从 Octo 基线 32.5% 提升至 90%，真实世界 88%
## 关键贡献

1. MuST 架构：Octo backbone + N 个技能 head + 1 个进度 head，共享骨干
2. ProGSS 技能选择器：基于进度值（0-1）选择当前应执行的技能
3. 以物体为中心的进度标注：仅在机器人与物体接触期间更新进度值
4. 技能集扩展能力：支持异步训练新技能、冻结骨干微调、动态扩展
## 结构化提取

- **Problem**: 长时序灵巧操控中的技能链式管理和进度追踪
- **Method**: MuST — Octo 骨干 + 多技能 head + 进度 head + ProGSS 选择器
- **Tasks**: Pick-n-Pack（翻转→抓取→打包→推动）
- **Sensors**: RGB 相机 + 机器人本体感觉
- **Robot Setup**: Isaac Sim（仿真）+ 真实机械臂 + 吸盘夹爪
- **Metrics**: 任务完成率、技能完成率、执行时间
- **Limitations**: OOD 物体泛化差、开环控制、单一任务族
- **Evidence Notes**: 全文读取，Tables I-VI 提供仿真/真实/多序列/物体泛化完整结果
## 本地引用关系

- [[gao2024prime]]
- [[hartz2024art]]
- [[lee2025diffdagger]]
- [[zhu2024scaling]]
## Problem

长时序灵巧操控任务需要链式组合多种技能（翻转、抓取、打包、推动），现有单策略方法（如 Octo）在技能序列管理上成功率低，缺乏对技能执行进度的理解。


## Method

- **架构**：Octo-Base（93M 参数）预训练骨干 + L1 action head 解码
- **多头设计**：每个技能 head 预测该技能的动作序列 P^(i)，进度 head 估计所有技能的进度向量 ν
- **进度标注**：技能执行期（首次接触到最后一次接触）进度从 α 线性增至 1，非执行期设为 α 或 1
- **ProGSS 选择逻辑**：选择进度值低于终止阈值 θ 的第一个技能；支持多序列演示
- **训练**：交替训练每个技能（batch 中仅更新对应 head + 骨干 + 进度 head）
- **目标条件**：支持语言指令或目标图像作为目标指示


## Experiments

- **仿真 Pick-n-Pack**：
  - 语言条件：MuST 80-90% vs Octo 32.5%（平均 87.5% vs 55%）
  - 图像条件：MuST 80-90% vs Octo 无数据
  - 执行时间：MuST 平均比 Octo 快 23.7-38.4%
- **物体泛化**：训练物体 90%+，OOD 物体（瓶子）~40%
- **多序列处理**：正确选择技能序列 96.2%（边界情况）
- **真实世界**：Couscous Box 16/20 成功，Overshoot 对象 88% 总体
- **扰动恢复**：能根据进度值自动回退或跳过技能


## Limitations

1. 进度估计对物体形状泛化有限（球形瓶推技能 ~40%）
2. 开环控制在真实世界中精度受限
3. 终止阈值 θ 是超参数，需手动调节
4. 仅在 Pick-n-Pack 任务族上验证
5. 训练需要每种技能的独立演示数据


## Key Takeaways

- 多头设计 + 进度估计比单策略方法在长时序任务上提升巨大（32.5%→90%）
- 技能进度值比 one-hot 技能分类提供更丰富的状态信息
- ProGSS 在扰动后能自动恢复（回退或跳过），具有鲁棒性
- 共享骨干使训练高效，冻结骨干微调不影响已有技能
- 推技能在 OOD 物体上泛化最差，形状差异是主要挑战

## 相关概念

- [[robotic-manipulation]]
- [[grasping]]

## 相关研究者

- [[gao-kai|Gao, Kai]]
