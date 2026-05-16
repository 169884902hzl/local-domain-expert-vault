---
title: "Your vision-language-action model already has attention heads for path deviation detection"
tags: [imitation, VLM, RL]
created: "2026-04-27"
updated: "2026-04-27"
type: "literature"
status: "done"
summary: "发现冻结 VLA 模型（NaVILA）中存在少量 Navigation Heads（Hnav），3 个 attention head 即可实现 44.6% 偏航检测率（FPR 11.7%），无需额外训练。结合 RL 避障策略（87.3% 成功率）实现 rollback 恢复。在 VLN-CE R2R 和真实移动机器人上验证。"
authors: "Jeong, Jaehwan; Zhu, Evelyn; Lin, Jinying; Jaimes, Emmanuel; Vu, Tuan-Anh et al."
year: "2026"
venue: "arXiv Preprint"
zotero_key: "WZPS3LLB"
---
## 摘要

Vision-Language-Action (VLA) models have demonstrated strong potential for predicting semantic actions in navigation tasks, demonstrating the ability to reason over complex linguistic instructions and visual contexts. However, they are fundamentally hindered by visual-reasoning hallucinations that lead to trajectory deviations. Addressing this issue has conventionally required training external critic modules or relying on complex uncertainty heuristics. In this work, we discover that monitoring a few attention heads within a frozen VLA model can accurately detect path deviations without incurring additional computational overhead. We refer to these heads, which inherently capture the spatiotemporal causality between historical visual sequences and linguistic instructions, as Navigation Heads. Using these heads, we propose an intuitive, training-free anomaly-detection framework that monitors their signals to detect hallucinations in real time. Surprisingly, among over a thousand attention heads, a combination of just three is sufficient to achieve a 44.6 % deviation detection rate with a low false-positive rate of 11.7 %. Furthermore, upon detecting a deviation, we bypass the heavy VLA model and trigger a lightweight Reinforcement Learning（强化学习） (RL) policy to safely execute a shortest-path rollback. By integrating this entire detection-to-recovery pipeline onto a physical robot, we demonstrate its practical robustness. All source code will be publicly available.

## 中文简述

提出基于强化学习的导航方法。

**研究方向**: 模仿学习、视觉-语言模型、强化学习

## 关键贡献

1. **Navigation Heads（Hnav）发现**：首次识别冻结 VLA（NaVILA/VILA-8B，32层×32头=1024头）中一小撮 attention heads 天然跟踪视觉-语言时空对齐。3 个头足以实现有效偏航检测。
2. **Training-free 异常检测框架**：基于 Hnav 的注意力熵比值 Rt 监测偏航，通过 SpatioTemporal alignment score（Idiag）+ Cohen's d 敏感性筛选头。零额外参数、零额外推理开销。
3. **RL 避障 rollback 策略**：PPO 训练的轻量级 actor-critic，输入 128×128 costmap + 相对目标，输出速度命令（v, ω），87.3% 避障成功率。
4. **层次化 VLA+RL 部署**：VLA 0.3Hz 高层导航 + RL 10Hz 低层控制，ROS 2 实现在 Jetson AGX Orin 上。
## 结构化提取

- **Problem**: VLA 模型（如 NaVILA）在视觉-语言导航中因 LLM 幻觉导致轨迹偏航。现有检测方法要么简单启发式漏检率高（>60%），要么需要额外训练模块或调用外部 LLM 增加计算开销。
- **Method**: 发现冻结 VLA 中 3 个 Navigation Heads（attention heads）天然跟踪视觉-语言时空对齐。基于 attention entropy ratio Rt 的 training-free 异常检测 + PPO 训练的 RL 避障 rollback 策略。层次化架构：VLA 0.3Hz 高层 + RL 10Hz 低层。
- **Tasks**: VLN-CE R2R 导航偏航检测（episode-level + step-level）；IsaacLab 避障导航（2048 episodes）；真实移动机器人导航。
- **Sensors**: 仿真 RGB 图像 + LiDAR costmap + IMU；真实 ZED 2i 相机 + RS-LiDAR + AprilTag。Fast-LIVO2 CPU 多传感器融合定位。
- **Robot Setup**: 仿真 IsaacLab 轮式机器人；真实 AgileX Scout 2.0 移动机器人 + NVIDIA Jetson AGX Orin 64GB。
- **Metrics**: Episode Detection Rate (EDR)、False Episode Rate (FER)、Gap (EDR-FER)、Step-level Precision/Recall/F1、RL Success Rate (SR)、Collision Rate (CR)、Terminate Rate (TR)。
- **Limitations**: 仅修正物理轨迹不同步 VLA 内部上下文（导致重复错误）；检测率上限~45%；仅验证导航 VLA 未验证操控 VLA；真实世界仅定性演示；超参数网格搜索泛化性未充分验证。
- **Evidence Notes**: 偏航检测在 R2R train/val 上有定量表格（Tab. 1-2），与 Stagnation/Act.Failure 基线对比充分。9000 组网格搜索消融（Fig. 6-7）可复现。RL 避障与 4 种经典方法对比，87.3% SR 可信（Fig. 8）。真实世界仅 Fig. 9 定性展示，无多次试验定量数据。Navigation Head 发现的 Cohen's d > 1.2 统计分离度可信。整体证据强度：仿真检测部分强，RL 避障强，真实部分弱。
## 本地引用关系

- [[brohan2023rt2]]
- [[dai2024racer]]
- [[ma2025running]]
## 证据元数据

- **Zotero Key**: WZPS3LLB
- **Citekey**: jeong2026your
- **Authors**: Jeong Jaehwan, Zhu Evelyn, Lin Jinying, Jaimes Emmanuel, Vu Tuan-Anh, Joo Jungseock, Kim Sangpil, Jawed M. Khalid
- **Affiliation**: Korea University + UCLA + NVIDIA
- **Venue**: arXiv preprint, 2026-03
- **Paper Type**: Discovery/Methods paper (attention analysis + training-free anomaly detection)
- **Fulltext Quality**: Complete, 15 pages with detailed method, figures, tables, and supplementary
- **Evidence Coverage**: High for Navigation Head discovery and anomaly detection (Tab. 1-2, Fig. 6-7); High for RL obstacle avoidance (Fig. 8); Low for real-world validation (Fig. 9, qualitative only)
- **Confidence**: High on simulation detection metrics; Medium on real-world robustness (limited quantitative real data)
- **Summary**: 发现冻结 VLA 模型（NaVILA）中存在少量 Navigation Heads（Hnav），3 个 attention head 即可实现 44.6% 偏航检测率（FPR 11.7%），无需额外训练。结合 RL 避障策略（87.3% 成功率）实现 rollback 恢复。在 VLN-CE R2R 和真实移动机器人上验证。


## Problem

VLA 模型在视觉-语言导航任务中继承了 LLM 的幻觉问题，导致轨迹偏航。现有偏航检测方法要么依赖简单运动启发式（如碰撞检测、位置停滞），要么需要训练额外检测模块（SMNA、Speaker-Follower），要么调用外部 LLM API（SayNav），前者漏检率高，后两者计算开销大。核心问题：能否直接从冻结的 VLA 模型内部获取偏航检测信号，无需额外训练？


## Method

### 轨迹相位分类（Sec 3.2）
- 基于参考路径跟踪：N（正常）→ A（异常），单向状态机 + patience p
- N 步中位偏移 0.13-0.16m，A 步 2.38-2.97m（Cohen's d > 1.2）

### Navigation Heads 选择（Sec 3.3）
1. **时空对齐分数 Idiag(h)**：在 SPL=1.0 的完美轨迹上计算
   - Suniform：帧能量均匀性（确保所有帧被关注）
   - Speak：指令聚焦锐度（确保集中关注特定指令段）
   - Sdiag：对角线空间接近度（视觉-指令时序对齐）
   - Sshift：平滑转移（随导航进展注意力逐步后移）
2. **异常敏感性**：Cohen's d 评估 N/A 阶段 Speak 分布分离度
3. **最终 Hnav**：排名前 10 的头中选 K=3 个（如 L16H1, L21H12, L6H78）

### 偏航检测（Sec 3.4）
- Rt = Et / rolling_avg(Et)，其中 Et = Hnav 中头的平均注意力熵
- Rt > τ 持续 P 步 → 判定为异常，触发 rollback
- 超参数（K=3, W=10, P=9, τ=0.95）在 train split 网格搜索

### RL 避障策略（Sec 3.5）
- PPO 训练，CNN 编码 costmap + MLP 编码相对目标
- 250m×200m 虚拟环境，2000 个随机障碍物
- 课程学习：目标距离 5m → 20m
- 14 项密集奖励（目标到达、安全、平滑）

### Sim-to-Real（Sec 3.6）
- Fast-LIVO2 CPU 位姿估计 + AprilTag EKF 全局坐标
- 动作平滑器（低通滤波 + 加速度裁剪 + 死区屏蔽）


## Experiments

### 偏航检测（Tab. 2, R2R validation）
| 方法 | Val-Seen EDR | Val-Seen FER | Val-Seen Gap | Val-Unseen EDR | Val-Unseen FER |
|------|-------------|-------------|-------------|---------------|---------------|
| Stagnation | 24.5% | 4.8% | 19.7% | 29.6% | 5.9% |
| Act.Failure | 0.3% | 6.0% | -5.7% | 1.5% | 6.3% |
| **Ours** | **44.6%** | 11.7% | **32.9%** | **41.9%** | 9.6% |

- Step-level（Val-Unseen, N→A）：Precision 92.5%, Recall 65.1%, F1 76.4%
- K=3 头：Episode EDR 43.9%, FER 9.6%（train split 上最优）

### RL 避障（Fig. 8a）
| 方法 | SR | CR | TR |
|------|-----|------|------|
| APF | 57.4% | 7.8% | 34.5% |
| TEB | 55.4% | 37.5% | 6.9% |
| DWA | 24.1% | 73.1% | 0.7% |
| MPPI | 3.4% | 86.1% | 0.4% |
| **Ours** | **87.3%** | 10.6% | 2.0% |

- 2048 episodes，目标距离 5-20m

### 真实世界（Sec 4.4）
- AgileX Scout 2.0 + Jetson AGX Orin 64GB + ZED 2i + RS-LiDAR
- VLA 偏航检测 → RL rollback 定性演示（Fig. 9）
- 无定量成功率报告


## Limitations

1. **仅修正物理轨迹，不同步 VLA 内部上下文**：rollback 后 VLA 的语言-视觉对齐状态未重置，可能导致重复认知错误。作者指出需要 re-prompting 或 active replanning 来打破错误循环。
2. **检测率上限约 45%**：仅用 3 个 attention head 的 entropy ratio，无法捕获所有偏航模式。更高的检测率需要更多头但会增加误报。
3. **仅验证导航 VLA（NaVILA/VILA-8B）**：未验证其他 VLA 架构（如 π₀、RT-2）是否存在类似的 Navigation Heads。
4. **仅适用于导航任务**：VLN-CE R2R 数据集，未扩展到操控任务。VLA 操控中的"偏航"定义和 Navigation Heads 是否存在需进一步研究。
5. **真实世界验证仅定性**：Fig. 9 展示单次演示，无多次试验的定量成功率。
6. **超参数依赖网格搜索**：K, W, P, τ 在 train split 上搜索，跨数据集泛化性未充分验证。


## Key Takeaways

1. **VLA 内部已有偏航检测机制**：无需额外训练，冻结模型的 attention heads 天然编码了视觉-语言时空对齐信息。这是一个重要发现，表明 LLM/VLM 的 attention head 特化现象延伸到了具身 VLA 模型。
2. **与 [[dai2024racer]]（RACER）形成对比**：RACER 用外部 VLM 监督员检测操控失败并生成丰富语言纠正；本文直接从 VLA 内部 attention heads 读取偏航信号，零额外推理开销。两种路径互补：RACER 提供语言级纠正，Navigation Heads 提供隐式信号级检测。
3. **与 [[ma2025running]]（Running VLAs）互补**：Ma et al. 优化 VLA 推理速度至 30FPS，本文的 training-free 检测不增加推理开销，两者可叠加实现实时可靠 VLA 控制。
4. **对本研究方向的启示**：Navigation Heads 的发现启示——操控 VLA（如 π₀、ACT）中是否也存在类似的 attention heads 检测操控失败？如果能发现"Grasping Heads"或"Placement Heads"，则可在不增加推理开销的情况下实现操控偏航检测。这对双臂 DLO 操控的在线失败检测有重要参考价值。

## 相关概念

- [[imitation-learning]]
- [[vision-language-model]]
- [[reinforcement-learning]]
- [[deformable-linear-object]]
- [[bimanual-manipulation]]
- [[grasping]]

## 相关研究者

- [[jeong|Jeong, Jaehwan]]
