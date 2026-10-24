---
title: "PRIME: Scaffolding manipulation tasks with behavior primitives for data-efficient imitation learning"
tags: [manipulation, imitation]
created: "2026-04-25"
updated: "2026-04-25"
type: "literature"
status: "done"
summary: "提出 PRIME 框架，用行为基元分解长时序任务：通过自监督数据收集训练 IDM（逆动力学模型），用动态规划将演示解析为基元序列，再用模仿学习训练高层策略选择基元及其参数。仿真成功率 95%+（超越基线 10-34%），真实世界 68-90%（超越基线 20-48%），仅需 30 条演示"
authors: "Gao, Tian; Nasiriany, Soroush; Liu, Huihan; Yang, Quantao; Zhu, Yuke"
year: "2024"
venue: "arXiv Preprint"
zotero_key: "5W4WV4U8"
---
## 摘要

Imitation learning（模仿学习） has shown great potential for enabling robots to acquire complex manipulation（操控） behaviors. However, these algorithms suffer from high sample complexity in long-horizon（长时序） tasks, where compounding errors accumulate over the task horizons. We present PRIME (PRimitive-based IMitation with data Efficiency), a behavior primitive-based framework designed for improving the data efficiency of imitation learning（模仿学习）. PRIME scaffolds robot tasks by decomposing task demonstrations into primitive sequences, followed by learning a high-level control policy to sequence primitives through imitation learning（模仿学习）. Our experiments demonstrate that PRIME achieves a significant performance improvement in multi-stage manipulation（操控） tasks, with 10-34% higher success rates in simulation over state-of-the-art（现有最优方法） baselines and 20-48% on physical hardware.

## 中文简述

提出基于模仿学习的操控方法，具有长时序任务特点。

**研究方向**: 机器人操控、模仿学习

## 证据元数据

- **Fulltext Quality**: fulltext
- **Evidence Coverage**: 读取了全文，包括 abstract、introduction、related work、method (Sec III)、experiments (Sec IV)、tables (I-IV)、figures (1-6)
- **Confidence**: high — 全文完整，3 个仿真任务 + 2 个真实世界任务系统评估，消融充分
- **Summary**: 提出 PRIME 框架，用行为基元分解长时序任务：通过自监督数据收集训练 IDM（逆动力学模型），用动态规划将演示解析为基元序列，再用模仿学习训练高层策略选择基元及其参数。仿真成功率 95%+（超越基线 10-34%），真实世界 68-90%（超越基线 20-48%），仅需 30 条演示
## 关键贡献

1. 行为基元分解：将长时序任务分解为 reach/grasp/place/push 等基元序列，大幅缩短策略学习时序
2. 轨迹解析器：用 IDM + 动态规划自动将未分割演示解析为基元序列，无需人工标注
3. 自监督数据收集：随机执行基元获取 IDM 训练数据，不依赖人类演示
4. 步骤增强：利用后缀一致性假设扩充解析后的训练数据
## 结构化提取

- **Problem**: 长时序模仿学习中的高样本复杂度和复合误差
- **Method**: PRIME — 行为基元分解 + IDM 轨迹解析 + 高层策略模仿学习
- **Tasks**: PickPlace、NutAssembly、TidyUp、CleanUp
- **Sensors**: 手腕相机 + 第三人称相机 + 机器人本体感觉
- **Robot Setup**: Franka Panda（仿真 + 真实）
- **Metrics**: 成功率
- **Limitations**: 仅完全可分解任务、固定基元库、sim-to-real IDM
- **Evidence Notes**: 全文读取，Tables I-IV 提供仿真/真实/消融/IDM 泛化完整结果
## 本地引用关系

- [[chen2025effective]]
- [[chen2025vividex]]
- [[gao2025must]]
- [[hartz2024art]]
## Problem

模仿学习在长时序任务中面临高样本复杂度问题，复合误差随任务时序累积。直接预测低层动作的策略需要大量演示且泛化能力有限。


## Method

- **基元库**：4 种参数化基元（reach/grasp/place/push），参数为位姿和位移
- **IDM 训练**：自监督随机执行基元收集 1-5M 转移数据，训练 primitive IDM（类型分类）和 parameter IDM（参数回归）
- **轨迹解析**：动态规划最大化基元序列概率乘积，α=0.0001 惩罚 "other" 类别
- **策略学习**：分解为 primitive policy π(p|s) + parameter policy π(x|s,p)，用 ResNet18 编码器 + GMM 输出
- **预训练**：用 IDM 数据预训练策略，再用解析的基元序列微调


## Experiments

- **仿真**：PickPlace 96.7%、NutAssembly 95.6%、TidyUp 98.9%（vs BC-RNN ~50-80%）
- **真实世界**：CleanUp-Bin 90%、CleanUp-Stack 68.3%（vs BC-RNN 41.7%/48.3%）
- **消融**：
  - 无预训练：PickPlace 从 96.7% 降至 46.3%
  - 贪心替代 DP：NutAssembly 从 95.6% 降至 55.4%
- **IDM 泛化**：在未见环境 ABC 上训练的 IDM 在环境 D 上达 97.5%（vs IDM-D 98.9%）
- **轨迹解析有效性**：解析后基元序列重放成功率 >90%，平均序列长度 2-7 步（vs 演示 200-400 步）


## Limitations

1. 仅在完全可分解为基元的任务上验证
2. IDM 在仿真中训练，sim-to-real 转移可能引入误差
3. 基元库固定为 4 种，无法处理需要新基元的任务
4. 精度敏感任务（如 Stacking）中参数预测误差导致失败


## Key Takeaways

- 行为基元将长时序任务从数百步缩减至几步，从根本上解决复合误差问题
- 自监督 IDM + 动态规划是无标注演示分割的有效方案
- 策略预训练对数据效率至关重要（无预训练性能下降 50%+）
- 同一 IDM 可跨任务和跨环境泛化
- 基元参数预测是当前瓶颈而非基元类型选择

## 相关概念

- [[robotic-manipulation]]
- [[imitation-learning]]
- [[grasping]]

## 相关研究者

- [[gao|Gao, Tian]]
- [[nasiriany|Nasiriany, Soroush]]
