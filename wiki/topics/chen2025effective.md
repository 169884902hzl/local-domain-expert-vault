---
title: "Towards effective utilization of mixed-quality demonstrations in robotic manipulation via segment-level selection and optimization"
tags: [manipulation, imitation]
created: "2026-04-25"
updated: "2026-04-25"
type: "literature"
status: "done"
summary: "提出 S2I 框架，将混合质量演示在片段级别进行分割、对比学习选择高质量片段、贪心轨迹优化低质量片段，仅用 3 条专家演示即可为多种下游策略（BC-RNN/DP/ACT/RISE）平均提升 ~21% 成功率"
authors: "Chen, Jingjing; Fang, Hongjie; Fang, Hao-Shu; Lu, Cewu"
year: "2025"
venue: "arXiv Preprint"
zotero_key: "YEWQNYBQ"
---
## 摘要

Data is crucial for robotic manipulation（机器人操控）, as it underpins the development of robotic systems for complex tasks. While high-quality, diverse datasets enhance the performance and adaptability of robotic manipulation（机器人操控） policies, collecting extensive expert-level data is resource-intensive. Consequently, many current datasets suffer from quality inconsistencies due to operator variability, highlighting the need for methods to utilize mixed-quality data effectively. To mitigate these issues, we propose “Select Segments to Imitate” (S2I), a framework that selects and optimizes mixed-quality demonstration（示范数据） data at the segment level, while ensuring plug-and-play compatibility with existing robotic manipulation（机器人操控） policies. The framework has three components: demonstration（示范数据） segmentation dividing origin data into meaningful segments, segment selection using contrastive learning to find high-quality segments, and trajectory optimization to refine suboptimal segments for better policy learning. We evaluate S2I through comprehensive experiments in simulation and real-world environments across six tasks, demonstrating that with only 3 expert demonstrations for reference, S2I can improve the performance of various downstream policies when trained with mixed-quality demonstrations. Project website: https://tonyfang.net/s2i/.

## 中文简述

提出基于学习方法的操控方法。

**研究方向**: 机器人操控、模仿学习

## 证据元数据

- **Fulltext Quality**: fulltext
- **Evidence Coverage**: 读取了全文（含附录），包括 abstract、introduction、method (Sec III)、experiments (Sec IV + 附录 A-I)、tables (I-X)、conclusion
- **Confidence**: high — 全文完整，6 个任务验证（3 仿真 + 3 真实），消融实验详尽
- **Summary**: 提出 S2I 框架，将混合质量演示在片段级别进行分割、对比学习选择高质量片段、贪心轨迹优化低质量片段，仅用 3 条专家演示即可为多种下游策略（BC-RNN/DP/ACT/RISE）平均提升 ~21% 成功率
## 关键贡献

1. 提出片段级（segment-level）选择策略，保留高质量片段同时优化低质量片段
2. 对比学习 + 距离加权投票的片段质量评估方法
3. 贪心轨迹优化 + 动作重标注，充分利用低质量数据
4. Plug-and-play，兼容 BC-RNN、Diffusion Policy、ACT、RISE 等多种策略
## 结构化提取

- **Problem**: 混合质量演示数据的有效利用，避免丢弃有价值的低质量数据
- **Method**: S2I — 启发式分割 + 对比学习片段选择 + 贪心轨迹优化 + 动作重标注
- **Tasks**: Lift/Can/Square（仿真）、Tissue/Cup/Pen（真实）
- **Sensors**: RGB-D 相机（RealSense D435）、状态向量（仿真）
- **Robot Setup**: Flexiv Rizon + DH AG-95 夹爪（真实）、RoboSuite 仿真环境
- **Metrics**: 成功率、数据利用率、平均增益
- **Limitations**: 复杂旋转处理困难、规模有限
- **Evidence Notes**: 全文读取，Table I-X 提供完整定量结果，含详细消融和真实实验
## 本地引用关系

- [[chen2025deformpam]]
- [[lee2025diffdagger]]
- [[wu2025imperfect]]
## Problem

机器人操控数据收集代价高，混合质量数据集（不同操作者技能水平）普遍存在。现有方法在演示级别丢弃低质量数据导致利用率低，在状态-动作对级别选择丢失上下文。


## Method

三步流程：
1. **演示分割**：启发式关键帧发现（抓取状态变化/速度趋零），将演示分为语义一致的片段
2. **片段选择**：对比学习训练片段表示模型（ResNet50 + MLP），距离加权投票分类高质量/低质量片段
3. **轨迹优化**：贪心算法去除低质量片段中的偏离路径点 + 动作重标注保持数据利用率


## Experiments

- **仿真**：RoboMimic（Lift/Can/Square），BC-RNN 平均增益 +21.16%，DP +6~11%
- **真实**：Flexiv Rizon + 大环 AG-95 + RealSense D435，Tissue/Cup/Pen 三任务
- **关键结果**：S2I 数据利用率 100%，L2D 仅 51.59%（丢弃低质量数据）
- **消融**：片段级 > 演示级选择；轨迹优化+动作重标注缺一不可


## Limitations

1. 难以处理复杂旋转轨迹
2. 仅在 6 个任务上验证
3. 片段表示依赖少量专家演示
4. 未扩展到大规模数据集


## Key Takeaways

- 片段级粒度是处理混合质量数据的最佳平衡点
- 即使低质量数据也包含有价值的状态空间探索信息
- 对比学习 + 距离加权投票是有效的质量评估方法
- Plug-and-play 设计使 S2I 具有广泛适用性

## 相关概念

- [[robotic-manipulation]]
- [[imitation-learning]]
- [[diffusion-model]]
- [[grasping]]

## 相关研究者

- [[chen-jingjing|Chen, Jingjing]]
- [[fang|Fang, Hongjie]]
- [[fang-hao-shu|Fang, Hao-Shu]]
- [[lu|Lu, Cewu]]
