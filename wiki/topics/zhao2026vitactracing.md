---
title: "ViTac-tracing: Visual-tactile imitation learning of deformable object tracing"
tags: [manipulation, imitation, sim-to-real, DLO, tactile]
created: "2026-05-11"
updated: "2026-05-11"
type: "literature"
status: "done"
summary: "提出基于视觉-触觉模仿学习的统一策略框架，通过局部中心损失和全局任务损失实现 1D/2D 可变形物体追踪，在 ABB YuMi 双臂平台上达到 80%（已知物体）和 65%（未知物体）成功率。"
authors: "Zhao, Yongqiang; Luo, Haining; Wang, Yupeng; Papastavridis, Emmanouil Spyrakos; Demiris, Yiannis et al."
year: "2026"
venue: "arXiv Preprint"
zotero_key: "CGA938PW"
---
## 摘要

Deformable objects often appear in unstructured configurations. Tracing deformable objects helps bringing them into extended states and facilitating the downstream manipulation（操控） tasks. Due to the requirements for object-specific modeling or sim-to-real（仿真到真实迁移） transfer, existing tracing methods either lack generalizability across different categories of deformable objects or struggle to complete tasks reliably in the real world. To address this, we propose a novel visual-tactile（触觉） imitation learning（模仿学习） method to achieve one-dimensional (1D) and two-dimensional (2D) deformable object（可变形物体） tracing with a unified model. Our method is designed from both local and global perspectives based on visual and tactile（触觉） sensing. Locally, we introduce a weighted loss that emphasizes actions maintaining contact near the center of the tactile（触觉） image, improving fine-grained adjustment. Globally, we propose a tracing task loss that helps the policy to regulate task progression. On the hardware side, to compensate for the limited features extracted from visual information, we integrate tactile（触觉） sensing into a low-cost teleoperation system considering both the teleoperator and the robot. Extensive ablation and comparative experiments on diverse 1D and 2D deformable objects demonstrate the effectiveness of our approach, achieving an average success rate of 80% on seen objects and 65% on unseen objects.

## 中文简述

提出基于模仿学习的操控方法，具有仿真到真实迁移特点。

**研究方向**: 机器人操控、模仿学习、仿真到真实迁移、可变形物体操控、触觉感知

## 关键贡献

1. **统一视觉-触觉 IL 框架**：首次提出用单一策略模型同时处理 1D 和 2D 可变形物体追踪，无需物体特定建模或 Sim-to-Real 迁移
2. **低成本视觉-触觉遥操作系统**：集成 GelSight Wedge 触觉传感器到双臂遥操作系统中，同时为遥操作者提供视觉+触觉+振动多模态反馈
3. **局部中心损失 + 全局任务损失**：两个新损失函数分别约束局部接触稳定性和全局任务进度，消融实验证明各自贡献
## 结构化提取

- Problem: 1D/2D 可变形物体追踪——从非结构化构型通过沿物体边缘滑动夹爪将其转变为展开状态，现有方法缺乏跨类别泛化能力
- Method: 基于 ACT 的视觉-触觉模仿学习，加入局部中心损失（触觉接触点位置加权）和全局任务损失（完成指数预测分支），使用 EE 位姿作为本体感知表示
- Tasks: 1D 可变形物体追踪（缆线、绳索）和 2D 可变形物体追踪（毛巾、布料），统一策略
- Sensors: ZED 2 立体相机（俯视 RGB），GelSight Wedge 视觉触觉传感器（安装在夹爪手指），机器人关节编码器
- Robot Setup: 双臂 ABB YuMi，3D 打印运动学遥操作模型，Nvidia Jetson Orin 边缘计算
- Metrics: 成功率（接触点到达末端 5% 范围内并保持抓取）、碰撞率、提前停止率、过度追踪率、物体脱落率、成功时间、完成比率
- Limitations: 碰撞失败、视觉遮挡导致终止判断失误、2D 物体受重力影响脱落率高、未知物体终止精度差、局部直线假设、实验规模有限（每物体仅 10-20 次）
- Evidence Notes:

  - 触觉信息显著减少物体脱落（消融：8/40 → 1/40）
  - 视觉信息主要影响任务终止精度（消融：过度追踪 0/40 → 8/40）
  - 中心损失有效减少物体脱落（消融：9/40 → 1/40）
  - 任务损失改善终止精度（消融：过度追踪 7/40 → 3/40）
  - Cartesian 空间优于关节空间（70% → 80%）
  - 多物体统一训练无性能下降
  - 未知物体成功率 65%（vs 已知 80%），终止相关失败增多
  - 1D 物体成功率整体高于 2D 物体
## 本地引用关系

-
## 证据元数据

- Fulltext Quality: fulltext
- Evidence Coverage: 95%（全文从 arXiv HTML 获取，含完整实验表格、消融分析和参考文献；图表仅以文字描述形式获取，未直接查看图像数据）
- Confidence: high
- Summary: 提出基于视觉-触觉模仿学习的统一策略框架，通过局部中心损失和全局任务损失实现 1D/2D 可变形物体追踪，在 ABB YuMi 双臂平台上达到 80%（已知物体）和 65%（未知物体）成功率。


## Problem

可变形物体（1D 线性物体如缆线、绳索；2D 平面物体如毛巾、布料）常以非结构化构型出现（如打结的鞋带、皱褶的毛巾）。Tracing 任务是将物体从非结构化状态滑到展开状态的基础步骤，可简化下游操控（如缆线插入、衣物折叠）。现有方法的局限：
1. **基于模型控制**：需要精确的物体状态和动力学建模，难以跨不同物体类别泛化
2. **强化学习**：依赖仿真中精确的可变形物体建模和精心设计的奖励函数，存在 Sim-to-Real gap
3. **此前方法只处理单类物体**：没有统一处理 1D 和 2D 的方法


## Method

### 整体框架
基于 ACT (Action Chunking Transformer) 的模仿学习框架，输入为机器人运动学（EE 位姿 6D）、视觉图像（ZED 2 俯视图 480×480）和触觉图像（GelSight Wedge 480×480），输出为未来 k=60 步的动作序列。

### 触觉-视觉遥操作系统
- **机器人端**：双臂 ABB YuMi，ZED 2 立体相机俯视，GelSight Wedge 触觉传感器安装在夹爪手指上，Nvidia Jetson Orin 运行驱动，ROS Noetic + Docker
- **遥操作端**：3D 打印运动学模型作为 leader，显示器实时流式传输视觉和触觉图像，振动电机（DAOKAI DC 5V Mini）安装在 leader 夹爪上用于奇异位形告警（基于 Yoshikawa 可操作度指数，阈值 λ_w=0.2）
- **数据采集**：30Hz 采样，记录视觉图像、触觉图像、机器人状态、运动学模型状态（作为动作标签）

### 网络架构
- 视觉和触觉各用独立 ResNet18 backbone 提取特征
- 运动学输入通过 MLP 提取特征
- 三路特征拼接后输入 Transformer 策略网络
- 附加一个完成指数预测分支（MLP 头）用于全局任务损失

### 损失函数
1. **局部中心损失 L_center**：从触觉图像中定位接触点（灰度→阈值→高斯滤波→轮廓提取→椭圆拟合/PCA），计算接触点到传感器中心的距离，以此构造权重 w_t = exp(-||p_t^tac - c|| / c)，加权 MAE 损失使策略优先学习"接触点保持在传感器中心"的动作
2. **KL 散度损失 L_reg**：ACT 原有的正则化损失（λ_reg=100）
3. **全局任务损失 L_task**：通过触觉图像定位接触点 → 转换到世界坐标系 → 计算完成指数 I = clamp(||p_t - p_0||_2 / ||p_T - p_0||_2, 0, 1)，用 MSE 训练完成指数预测分支（λ_task=100）

### 推理
- 工作站：AMD Ryzen Threadripper Pro 5965WX + RTX 4090，训练 15000 epochs
- 推理机：Intel i9 (24 cores) + 32GB RAM
- EE 位姿输出需转换为关节角度后执行


## Experiments

### 数据集
- 已知物体：扁平鞋带、编织缆线、面巾、超细纤维布（2×1D + 2×2D），每物体 25 次演示，共 100 次演示
- 未知物体：合成绳索（1D）、棉质餐巾（2D）

### 主要结果（Table I 消融）
| 方法 | 成功率 | 碰撞 | 提前停止 | 过度追踪 | 物体脱落 |
|------|--------|------|----------|----------|----------|
| Joint Space | 70.0% | 1/40 | 4/40 | 2/40 | 5/40 |
| w/o Vision | 65.0% | 4/40 | 2/40 | 8/40 | 0/40 |
| w/o Tactile | 60.0% | 2/40 | 5/40 | 1/40 | 8/40 |
| w/o Center Loss | 65.0% | 4/40 | 1/40 | 0/40 | 9/40 |
| w/o Task Loss | 67.5% | 3/40 | 3/40 | 7/40 | 0/40 |
| **Ours** | **80.0%** | 2/40 | 2/40 | 3/40 | 1/40 |

### 多物体训练（Table II）
- 单物体训练：鞋带 80%，缆线 90%，面巾 60%，布料 80%
- 分组训练（1D/2D）：与单物体训练性能相似
- 统一训练（全部）：无性能下降，证实统一策略可行性
- 1D 物体成功率整体高于 2D 物体（重力导致 2D 物体下垂脱落）

### 未知物体（Table III）
| 物体 | 成功率 | 碰撞 | 提前停止 | 过度追踪 | 物体脱落 |
|------|--------|------|----------|----------|----------|
| 绳索 | 70.0% | 0/20 | 4/20 | 0/20 | 2/20 |
| 餐巾 | 60.0% | 2/20 | 0/20 | 4/20 | 2/20 |

### 关键观察
1. 触觉信息对维持接触至关重要：去掉触觉后物体脱落率从 1/40 升至 8/40
2. 视觉信息主要影响任务终止判断：去掉视觉后过度追踪率从 3/40 升至 8/40
3. 中心损失有效减少物体脱落：去掉后脱落率从 1/40 升至 9/40
4. 任务损失改善终止精度：去掉后过度追踪率从 3/40 升至 7/40
5. 未知物体性能下降主要源于终止相关失败（提前停止和过度追踪更频繁）


## Limitations

1. **碰撞失败**：接触力过大或摩擦/缠绕导致机器人碰撞，占已知物体失败的 2/40
2. **视觉遮挡**：物体末端附近的视觉遮挡导致终止判断失误（提前停止/过度追踪）
3. **2D 物体受重力影响**：织物部分在夹爪外下垂，更容易从前开口滑出脱落，面巾成功率仅 60%
4. **未知物体终止精度差**：成功率从 80% 降至 65%，终止相关失败明显增多，说明视觉外观差异影响较大
5. **局部直线假设**：全局任务损失假设物体边缘在追踪过程中局部平直，对严重弯曲/缠绕场景可能不适用
6. **仅用成功的演示数据**：虽然演示者动作并非总是理想（接触不在中心），但只用成功 episode 训练，未利用失败信号
7. **实验规模有限**：每物体仅 10 次试验（已知）/ 20 次（未知），Wilson 95% CI 范围较宽


## Key Takeaways

1. **触觉对 DLO 追踪至关重要**：去掉触觉后脱落率从 1/40 跳到 8/40，视觉单独无法替代局部接触信息
2. **Cartesian 空间优于关节空间**：追踪任务本质上定义在任务空间，EE 位姿与任务目标对齐，减少关节空间的冗余和歧义
3. **中心损失的设计巧妙**：不需要完美演示数据，通过加权方式让策略自动学习更安全的接触保持动作
4. **多物体统一训练无性能损失**：1D 和 2D 物体可以在单一模型中联合训练，为跨类别泛化奠定基础
5. **遥操作系统的触觉反馈设计**：振动电机用于奇异位形告警、触觉图像实时显示，是低成本但有效的多模态反馈方案
6. **触觉纹理相似性支持泛化**：未知物体的触觉纹理与已知物体相似（图 6），可能是触觉感知提升泛化能力的一个原因

## 相关概念

- [[robotic-manipulation]]
- [[imitation-learning]]
- [[sim-to-real]]
- [[deformable-linear-object]]
- [[tactile-sensing]]
- [[vision-language-model]]
- [[bimanual-manipulation]]
- [[grasping]]

## 相关研究者

- [[zhao-yongqiang|Zhao, Yongqiang]]
- [[luo-haining|Luo, Haining]]
