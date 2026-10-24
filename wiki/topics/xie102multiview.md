---
title: "Multi-View Registration of Partially Overlapping Point Clouds for Robotic Manipulation"
tags: [manipulation, RL]
created: "2026-04-25"
updated: "2026-04-25"
type: "literature"
status: "done"
summary: "提出基于 point-to-plane 模型和 pose graph 的多视角部分重叠点云注册方法。关键技术：(1) 在配对注册目标函数中引入 robust kernel 减少误匹配点影响；(2) 增强欧几里得聚类（平滑阈值分割）提取目标物体点云；(3) pose graph 全局优化建立非相邻帧位姿约束减少累积误差。Stanford 3D 数据集：E(R) 降低 13.54%/E(t) 降低 18.72% vs NDT。30% 重叠率即可成功注册。UR10 + Leap Motion 真实机器人抓取实验 98.9% 成功率"
authors: "Xie, Yuzhen; Song, Aiguo"
year: "2022"
venue: "IEEE Robotics and Automation Letters"
zotero_key: "499SDFTU"
---
## 摘要

Point cloud（点云） registration is a fundamental task in intelligent robots, aiming to achieve globally consistent geometric structures and providing data support for robotic manipulation（机器人操控）. Due to the limited view of measurement devices, it is necessary to collect point clouds from multiple views to construct a complete model. Previous multi-view registration methods rely on sufﬁcient overlap and registering all pairs of point clouds, resulting in slow convergence and high cumulative errors. To solve these challenges, we present a multi-view registration method based on the point-to-plane model and pose graph. We introduce a robust kernel into the objective function to diminish registration errors caused by mismatched points. Additionally, an enhanced Euclidean clustering method is proposed for extracting object point clouds. Subsequently, by establishing pose constraints on non-adjacent frames of point clouds, the cumulative error is reduced, achieving global optimization based on the pose graph. Experimental results demonstrate the robustness of our method with respect to overlap ratios, successfully registering point clouds with overlap ratio exceeding 30%. In comparison to other techniques, our method can reduce the E (R) of multi-view registration by 13.54% and E (t) by 18.72%, effectively reducing the cumulative error.


## 中文简述

提出基于点云的操控方法。

**研究方向**: 机器人操控、强化学习

## 关键贡献

1. Robust kernel 配对注册：point-to-plane 模型 + robust kernel 减少误匹配
2. 增强欧几里得聚类：平滑阈值条件减少过分割/欠分割
3. Pose graph 全局优化：非相邻帧约束减少累积误差
4. 完整系统：注册 + 物体提取 + 全局优化 + 机器人抓取验证
## 结构化提取

- **Problem**: 多视角部分重叠点云注册的误匹配、物体提取和累积误差问题
- **Method**: Point-to-plane + robust kernel + 增强聚类 + pose graph 全局优化
- **Tasks**: Stanford 3D 多视角注册 + UR10 真实机器人抓取
- **Sensors**: Leap Motion Camera（眼在手 RGB-D）
- **Robot Setup**: UR10 + parallel gripper
- **Metrics**: E(R)/E(t)（-13.54%/-18.72%）+ 抓取成功率（98.9%）
- **Limitations**: 大旋转误差、点密度敏感、依赖初始精度、推理速度
- **Evidence Notes**: 全文读取，Tables I-XI 提供完整对比和消融
## 本地引用关系

- [[boerdijk2025autonomous]]
- [[huang2025match]]
- [[wang2023multistage]]
## 证据元数据

- **Fulltext Quality**: fulltext
- **Evidence Coverage**: 读取了全文，包括 abstract、introduction (Sec I)、method (Sec II)、experiments (Sec III)、tables (I-XI)、figures (1-9)
- **Confidence**: high — 全文完整，IEEE RA-L 2024，Southeast University，point-to-plane 模型 + robust kernel + pose graph 全局优化 + 增强欧几里得聚类，30% 重叠率即可注册，E(R) 降低 13.54%/E(t) 降低 18.72%，UR10 + Leap Motion 真实抓取 98.9% 成功率
- **Summary**: 提出基于 point-to-plane 模型和 pose graph 的多视角部分重叠点云注册方法。关键技术：(1) 在配对注册目标函数中引入 robust kernel 减少误匹配点影响；(2) 增强欧几里得聚类（平滑阈值分割）提取目标物体点云；(3) pose graph 全局优化建立非相邻帧位姿约束减少累积误差。Stanford 3D 数据集：E(R) 降低 13.54%/E(t) 降低 18.72% vs NDT。30% 重叠率即可成功注册。UR10 + Leap Motion 真实机器人抓取实验 98.9% 成功率


## Problem

多视角点云注册存在三个挑战：(1) 部分重叠导致误匹配点；(2) 目标物体提取困难；(3) 顺序注册的累积误差。现有方法要么需要高重叠率、要么注册所有帧对导致效率低。


## Method

- **配对注册**：
  - Point-to-plane 模型：目标函数 min Σ[(Rp+t-q)^T·n]^2
  - Robust kernel：ρ(r) 替代平方误差，梯度增长更慢 → 减少异常值影响
  - IRLS（迭代重加权最小二乘）求解
  - ANN 最近邻匹配，O(N log N) 复杂度
- **物体提取**：
  - Pass-through 滤波 → RANSAC 去地面 → Kd-tree 去噪
  - 增强欧几里得聚类：平滑阈值 s = ||Σ(Xi-Xj)|| / (N·||Xi||) 区分边缘点
  - 减少 over-segmentation 和 under-segmentation
- **多视角全局优化**：
  - Pose graph：节点=位姿 Ti，边=注册误差
  - 关键帧选择：旋转/平移超过阈值时选择
  - 非相邻帧约束：loop closure（如帧1-4, 1-7, 4-7）
  - Lie 代数表示 + Gauss-Newton 优化
  - 最小化全局注册误差


## Experiments

- **配对注册（Stanford 3D）**：
  - Clean (overlap 0.7)：MSE(R) 0.012, MSE(t) 0.067
  - Noisy：SOTA 性能，优于 ICP/Generalized-ICP/DCP/PR-Net/FMR
  - Noise+Outlier (15% outliers)：仍保持高精度
  - Low overlap (0.3-0.6)：overlap >0.3 即可成功注册
- **多视角注册**：
  - vs NDT：E(R) -13.54%, E(t) -20.48%
  - vs Con2Fin：E(R) -17.16%, E(t) -18.72%
  - 高斯噪声下更鲁棒（低 SNR 仍保持精度）
  - ModelNet40/3DMatch 通用性验证
- **消融**：三个组件（R+O+PG）均有贡献
- **机器人抓取**：
  - UR10 + Leap Motion 眼在手相机
  - 9 个物体，90 次抓取，98.9% 成功率
  - 完整的 3D 重建 → 抓取规划流程


## Limitations

1. Point-to-plane 模型在旋转误差较小时效果好，大旋转误差可能不收敛
2. 增强聚类对点密度变化敏感
3. Pose graph 优化依赖配对注册初始精度
4. 推理速度慢于 PCL 优化版 ICP
5. 未考虑动态场景或变形物体


## Key Takeaways

- Robust kernel 有效减少误匹配影响：point-to-plane + robust kernel 是低重叠注册的有效组合
- Pose graph 全局优化是减少累积误差的关键：非相邻帧约束显著提升多视角注册精度
- 30% 重叠率即可注册：低于大多数现有方法的要求
- 完整的感知-操控管线可行：注册→3D重建→抓取规划，98.9% 真实成功率
- 非学习方法仍有竞争力：在特定任务上可与深度学习方法匹敌

## 相关概念

- [[robotic-manipulation]]
- [[reinforcement-learning]]
- [[grasping]]

## 相关研究者

- [[xie|Xie, Yuzhen]]
