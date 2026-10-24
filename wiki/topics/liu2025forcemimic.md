---
title: "ForceMimic: Force-centric imitation learning with force-motion capture system for contact-rich manipulation"
tags: [manipulation, imitation, robot-learning]
created: "2026-04-25"
updated: "2026-04-25"
type: "literature"
status: "done"
summary: "提出 ForceMimic 系统：(1) ForceCapture 手持力-位数据采集设备（六轴力传感器+SLAM相机+RGB-D，$50，0.8kg），5 分钟采集 vs 遥操作 13 分钟；(2) HybridIL 力中心模仿学习算法：扩散策略同时预测 wrench+pose，根据预测力值切换 IK 位置控制或混合力-位控制原语。西葫芦削皮：运动正确率 100%（vs Raw DP 80%），>10cm 连续皮 85%（vs 55%），力分布更均匀（~9N vs dataset ~10N）"
authors: "Liu, Wenhai; Wang, Junbo; Wang, Yiming; Wang, Weiming; Lu, Cewu"
year: "2025"
venue: "arXiv Preprint"
zotero_key: "U5XH9QX3"
---
## 摘要

In most contact-rich（接触丰富） manipulation（操控） tasks, humans apply time-varying forces to the target object, compensating for inaccuracies in the vision-guided hand trajectory. However, current robot learning algorithms primarily focus on trajectory-based policy, with limited attention given to learning force-related skills. To address this limitation, we introduce ForceMimic, a force-centric robot learning system, providing a natural, force-aware and robot-free robotic demonstration（示范数据） collection system, along with a hybrid force-motion imitation learning（模仿学习） algorithm for robust contact-rich（接触丰富） manipulation（操控）. Using the proposed ForceCapture system, an operator can peel a zucchini in 5 minutes, while force-feedback teleoperation takes over 13 minutes and struggles with task completion. With the collected data, we propose HybridIL to train a force-centric imitation learning（模仿学习） model, equipped with hybrid force-position control primitive to fit the predicted wrench-position parameters during robot execution. Experiments demonstrate that our approach enables the model to learn a more robust policy under the contact-rich（接触丰富） task of vegetable peeling, increasing the success rates by 54.5% relatively compared to state-ofthe-art pure-vision-based imitation learning（模仿学习）. Hardware, code, data and more results can be found on the project website at https://forcemimic.github.io.

## 中文简述

提出基于模仿学习的操控方法，具有接触丰富特点。

**研究方向**: 机器人操控、模仿学习、机器人学习

## 证据元数据

- **Fulltext Quality**: fulltext
- **Evidence Coverage**: 读取了全文，包括 abstract、introduction、related work (Sec II)、method (Sec III)、experiments (Sec IV)、table (I)、figures (1-7)
- **Confidence**: high — 全文完整，arXiv 2025 预印本（v3），15 根西葫芦 438 段 30199 动作序列，4 种方法对比，20 次测试
- **Summary**: 提出 ForceMimic 系统：(1) ForceCapture 手持力-位数据采集设备（六轴力传感器+SLAM相机+RGB-D，$50，0.8kg），5 分钟采集 vs 遥操作 13 分钟；(2) HybridIL 力中心模仿学习算法：扩散策略同时预测 wrench+pose，根据预测力值切换 IK 位置控制或混合力-位控制原语。西葫芦削皮：运动正确率 100%（vs Raw DP 80%），>10cm 连续皮 85%（vs 55%），力分布更均匀（~9N vs dataset ~10N）
## 关键贡献

1. ForceCapture：低成本（$50）、手持、无机器人的力-位数据采集系统
2. HybridIL：力中心模仿学习——扩散策略输出 wrench+pose 参数 + 混合力-位控制原语
3. 正交力-位控制：力控制方向与运动方向正交，实现同时跟踪
4. 西葫芦削皮任务验证：100% 运动成功率，54.5% 相对提升 vs SOTA 视觉方法
## 结构化提取

- **Problem**: 接触丰富操控中力技能学习不足 + 力数据采集困难
- **Method**: ForceCapture（手持力-位采集）+ HybridIL（扩散策略输出 wrench+pose + 混合力-位控制）
- **Tasks**: 西葫芦削皮（Flexiv Rizon 4 双臂）
- **Sensors**: 六轴 F/T 传感器 + SLAM 相机（T265）+ RGB-D（L515）
- **Robot Setup**: 双臂 Flexiv Rizon 4
- **Metrics**: 运动正确率、>10cm 连续皮成功率
- **Limitations**: 简单 MLP、单一技能、力作为输入效果差
- **Evidence Notes**: 全文读取，Table I 提供完整 4 方法对比，Fig 6 可视化削皮结果
## 本地引用关系

- [[chen2025effective]]
- [[hartz2024art]]
- [[lee2025diffdagger]]
- [[wu2025imperfect]]
- [[wu2025tacdiffusion]]
- [[zhao2025polytouch]]
## Problem

接触丰富操控任务（如削皮）中，人类利用时变力补偿视觉引导轨迹的不精确性。当前机器人学习算法主要关注轨迹策略，力相关技能学习不足。力数据采集困难——遥操作不自然且慢，人类视频无力数据。


## Method

- **ForceCapture 硬件**：
  - 六轴 F/T 传感器（end-effector 与手柄之间）
  - SLAM 相机（T265，记录位姿）
  - RGB-D 相机（L515，外部固定，记录环境）
  - 齿条-小齿轮夹爪（可选）+ 单向自锁机构
  - 重力补偿：准静态假设，最小二乘估计质心和重量
  - 数据对齐：1000Hz（力）+ 200Hz（SLAM）+ 30Hz（RGB-D）→ 30Hz
- **数据转换（robot-free → pseudo-robot）**：
  - SLAM 位姿 → 机器人 TCP 位姿
  - RGB-D → 点云（voxelized 10000）
  - 力数据 → 补偿后的交互 wrench
- **HybridIL 策略学习**：
  - 扩散策略框架（DDIM）
  - 输入：点云 MLP 编码 + TCP 位姿
  - 输出：未来 20 步的 pose + wrench 序列
  - MSE loss（pose + wrench 分别计算）
- **混合力-位控制原语**：
  - 预测力 < 6N：IK 关节位置控制
  - 预测力 ≥ 6N 连续步：混合力-位控制
  - 正交化：运动方向 d̂ 从 pose 轨迹计算，力投影到运动正交平面
  - 初始接触：反向力控制方向按压实现稳定接触
  - Flexiv RDK 实现


## Experiments

- **数据采集效率**：
  - 人类直接：2.9 分钟/西葫芦
  - ForceCapture：4.5 分钟（无需训练）
  - 遥操作：13 分钟（需要训练 + 3 次中断）
- **西葫芦削皮（Flexiv Rizon 4）**：
  - HybridIL：100% 运动正确（20/20），85% >10cm 连续皮
  - Raw DP：80% 运动正确（16/20），55% >10cm 连续皮
  - Force DP：60% 运动正确（6/10），10% >10cm
  - Force+Hybrid DP：80% 运动正确（8/10），20% >10cm
- **力分析**：
  - HybridIL 平均力 ~9N（接近数据集 ~10N），削皮均匀
  - Raw DP 平均力 ~20N（峰值 >40N），过度施力
  - Force DP/Force+Hybrid DP：力输入导致预测混乱（力分布不匹配）
- **关键发现**：将力作为输入反而降低性能（Force DP 60% < Raw DP 80%），因为部署时的力分布与训练数据不一致


## Limitations

1. 简单 MLP 表示点云/力/位姿，缺乏高级多模态融合
2. 仅两种控制原语（IK + 混合力-位），扩展空间大
3. 仅验证单一削皮技能，泛化性未验证
4. 力作为输入的效果反直觉地差——sim-to-real 力分布不匹配
5. 削皮失败的 case：力-位参数过早结束导致控制原语切换中断


## Key Takeaways

- 力中心学习的关键不是将力作为输入，而是作为输出（策略预测力-位参数 + 低层力控制）
- 正交力-位控制是有效的控制原语：力控制方向与运动方向解耦
- 手持设备比遥操作更适合力数据采集：更自然、更快速、无需机器人
- 力数据 sim-to-real gap 的本质：部署时的力分布与训练时不一致
- 重力补偿 + 准静态假设足以获取纯交互力

## 相关概念

- [[robotic-manipulation]]
- [[imitation-learning]]
- [[robot-learning]]
- [[vision-language-model]]
- [[diffusion-model]]
- [[bimanual-manipulation]]
- [[grasping]]

## 相关研究者

- [[liu-wenhai|Liu, Wenhai]]
- [[lu|Lu, Cewu]]
