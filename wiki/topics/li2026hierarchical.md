---
title: "Hierarchical DLO routing with reinforcement learning and in-context vision-language models"
tags: [manipulation, VLM, RL, DLO, planning]
created: "2026-05-10"
updated: "2026-05-10"
type: "literature"
status: "done"
summary: "提出层次化 DLO routing 框架，高层 VLM 通过 in-context learning 生成路由计划并检测恢复失败，低层 RL 策略执行精准 insertion 原语，在 3-5 clip 长时序场景中实现仿真 92% 和真机 62.5% 成功率。"
authors: "Li, Mingen; Yu, Houjian; Huang, Yixuan; Hong, Youngjin; Ye, Hantao et al."
year: "2026"
venue: "arXiv Preprint"
zotero_key: "25JFW37X"
---
## 摘要

Long-horizon（长时序） routing tasks of deformable linear objects (DLOs), such as cables and ropes, are common in industrial assembly（装配） lines and everyday life. These tasks are particularly challenging because they require robots to manipulate DLO（可变形物体） with long-horizon（长时序） planning and reliable skill execution. Successfully completing such tasks demands adapting to their nonlinear dynamics, decomposing abstract routing goals, and generating multi-step plans composed of multiple skills, all of which require accurate high-level reasoning during execution. In this paper, we propose a fully autonomous hierarchical framework for solving challenging DLO（可变形物体） routing tasks. Given an implicit or explicit routing goal expressed in language, our framework leverages vision-language models~(VLMs) for in-context high-level reasoning to synthesize feasible plans, which are then executed by low-level skills trained via reinforcement learning（强化学习）. To improve robustness over long horizons, we further introduce a failure recovery mechanism that reorients the DLO（可变形物体） into insertion-feasible states. Our approach generalizes to diverse scenes involving object attributes, spatial descriptions, implicit language commands, and \myred{extended 5-clip settings}. It achieves an overall success rate of 92\% across long-horizon（长时序） routing scenarios. Please refer to our project page: https://icra2026-dloroute.github.io/DLORoute/

## 中文简述

提出基于强化学习的可变形物体方法，具有泛化能力特点。

**研究方向**: 机器人操控、视觉-语言模型、强化学习、可变形物体操控、运动规划

## 关键贡献

1. **层次化框架**：首次将 VLM 高层推理与 RL 底层技能结合，用于任意排列、多样属性的 DLO 长时序 routing
2. **失败感知机制**：VLM 检测执行失败、推理原因并触发 Flatten 恢复技能，显著提升长时序成功率
3. **强泛化能力**：从 3-clip 泛化到 4/5-clip 设置，支持隐式指令、空间描述、颜色属性等多种指令模式，整体仿真成功率 92%
## 结构化提取

- Problem: 长时序 DLO routing——将可变形线性物体（缆线/绳子）按语言指令指定的顺序穿过多个夹子，需要高层语义规划与底层精准操控的结合
- Method: 层次化框架——GPT-5 VLM（in-context learning + CoT）做高层规划/失败推理，SAC RL 策略执行 insertion 运动原语，预定义 Pull/Flatten 原语辅助
- Tasks: DLO routing（单臂桌面上穿 clip），支持 3-5 clip、隐式/显式语言指令、颜色/空间属性描述
- Sensors: 腕装 Intel RealSense D415 RGB-D 相机（俯视 + 放大视图），仿真中用粒子状态
- Robot Setup: Franka Emika Panda 单臂机器人，ROS + MoveIt，NVIDIA 5090 运行 SAM2 分割
- Metrics: 成功率 SR（全部 clip 按正确顺序穿过），平均穿过 clip 数，平均 episode 长度
- Limitations: VLM 规划偶发错误/次优决策；真机 SR 显著低于仿真；技能集固定无法自动扩展；2D 动作空间限制；Flatten 恢复过于简单
- Evidence Notes: 完整实验数据——仿真 4 种 routing 设置 × 15 trials × 5 种方法，真机 8 种配置 × 4 任务；消融实验验证失败推理和 RL 策略各自的贡献；失败案例分析覆盖 3 种典型失败模式
## 本地引用关系

- [[li2025routing]]
## 证据元数据

- Fulltext Quality: fulltext
- Evidence Coverage: 完整覆盖（Introduction, Related Works, Method, Experiments, Limitations, Conclusion 均已精读）
- Confidence: high
- Summary: 提出层次化 DLO routing 框架，高层 VLM 通过 in-context learning 生成路由计划并检测恢复失败，低层 RL 策略执行精准 insertion 原语，在 3-5 clip 长时序场景中实现仿真 92% 和真机 62.5% 成功率。


## Problem

长时序 DLO（可变形线性物体）routing 任务要求机器人将缆线/绳子按指定顺序穿过多个夹子（clips），这在工业装配和日常生活中很常见。核心挑战包括：
1. DLO 的非线性动力学和欠驱动特性使底层控制困难
2. 需要将抽象的语言指令分解为多步技能序列
3. 长时序执行中错误会累积，需要推理、重规划和失败恢复
4. 现有方法（如模仿学习 [Luo et al. 2024]）泛化性差，从 3-clip 扩展到 4-clip 时性能骤降


## Method

### 整体架构
层次化框架分为两层：
- **高层 VLM 规划器**：接收俯视场景图像 + 语言指令 + 技能定义，通过 in-context learning 生成路由计划（clip 顺序、技能选择、任务完成判断）
- **底层技能集**：Insert（RL 训练）、Pull（预定义运动原语）、Flatten（预定义运动原语）

### 低层 RL Insertion 策略
- **状态空间**：粒子表示的 DLO 状态 p_{1:n}、夹子位姿和尺度、rope_in 二值指示器
- **动作空间**：3D 笛卡尔运动 p_g^t + 1D 旋转 q_g^t，限定在 0.16m × 0.16m 的局部空间
- **运动原语设计**：Insert 由抓取索引 i + 两个路径点组成（7 个参数），Pull 和 Flatten 为预定义运动
- **奖励函数**：
  - rope_in / rope_out 穿过指示（+0.5 权重）
  - collide 碰撞惩罚（β=-2）
  - r_hor 时间步惩罚（γ=-0.001）鼓励高效插入
  - r_dist 阶段特定距离奖励
  - r_flat 鼓励 DLO 前段保持平直（η=0.5）
- **训练**：SAC 算法，MLP 网络，IsaacSim + GarmentLab 仿真
- **课程学习**：先大 clip 开口（scale 1.0-2.2），后缩小到 0.9-1.5，训练 6.2k steps
- **坐标变换**：DLO 状态始终变换到目标 clip 局部坐标系

### 高层 VLM 规划器
- 使用 GPT-5（low reasoning effort）
- **输入**：俯视场景图 + 用户指令 + 场景描述（DLO/clip/环境属性）+ 放大视图
- **输出**：结构化决策（选择技能 + 目标 clip + 完成标志）
- **In-context learning**：2 个示例（insertion 和 pulling 场景）
- **Chain-of-thought prompting**：分析放大视图判断 DLO-clip 交互状态
- **跟踪 DLO 头部位置**：识别已穿过 clip 后的遮挡情况

### 失败恢复机制
- Flatten 技能将 DLO 重新初始化到"可插入"状态
- 连续 insertion 尝试计数器 + 步数上限
- 失败检测和恢复完全由 VLM 自主完成，无需人工干预


## Experiments

### 仿真实验（Table I - 低层 insertion 原语）
| 方法 | 成功率 |
|------|--------|
| Heuristic Policy | 较低（open-loop，无环境感知） |
| RL Policy（ours） | 显著高于 heuristic |

（具体数值在 Table I 中，但全文 HTML 中该表格式未完整呈现数值）

### 仿真长时序 routing（Table II）
| 高层规划器 | 低层策略 | Implicit SR | Fixed Spatial SR | Fixed Attr. SR | 4/5-Clip SR |
|-----------|---------|-------------|-----------------|---------------|-------------|
| VLM w/ Failure Reasoning | Heuristic | 13% | 7% | 0% | 7% |
| VLM w/o Failure Reasoning | RL | 47% | 7% | 7% | 47% |
| Fixed Order | RL | 53% | 13% | 13% | 60% |
| Symbolic Planner | RL | 68% | 53% | 53% | 100% |
| **VLM w/ Failure Reasoning** | **RL** | **80%** | **93%** | **93%** | **100%** |

SR = success rate (%), 每个设置 15 trials。

**关键发现**：
- Q1: 层次化框架显著优于 Fixed Order 和 Heuristic baselines
- Q2: 失败推理在所有设置中提升成功率，尤其在大转弯场景（Fixed Spatial/Attribute）
- Q3: 完美泛化到 4/5-clip（100% SR），而 VLM-only 和 Fixed Order 显著下降
- Q4: RL 底层策略 vs Heuristic：4/5-clip 从 7% 到 100%

### 真机实验（Table III）
- 硬件：Franka Emika Panda + Intel RealSense D415（腕装相机，1280×720）
- 感知：SAM2 分割 clip 和 DLO（NVIDIA 5090）
- 规划：MoveIt 生成连续轨迹
- 框架：ROS
- **Sim-to-Real**：无需额外微调或域适应
- 8 种 clip 配置，4 种任务类型：
  - Our method: 62.5% SR
  - Fixed Order baseline: 显著更差

### 失败案例分析（Figure 6）
1. **Early termination**：VLM 在最后一个 clip 未完成时提前终止
2. **错误 Flatten**：DLO 已穿入 clip 却仍执行 flatten，导致抓取失败和碰撞
3. **冗余 Insertion**：VLM 忽略已穿出的 DLO 段，误判为未完成而重复 insertion


## Limitations

1. VLM 规划器偶尔产生错误或次优决策（如不必要的 flatten、忽略已穿出段）
2. 真机成功率（62.5%）明显低于仿真（92%），受标定误差、感知噪声、sim-to-real gap 影响
3. 当前技能集固定为 3 种，不支持自动扩展
4. 2D 平面 + 1D 旋转的动作空间限制，未处理全 3D routing
5. 失败恢复依赖单一 Flatten 技能，无法处理所有失败模式


## Key Takeaways

1. **层次化 VLM+RL 架构对 DLO 操控非常有效**：VLM 负责语义推理和任务分解，RL 负责精准接触操控，两者解耦避免了端到端学习的困难
2. **失败推理是长时序 DLO 操控的关键**：没有失败恢复时，长时序任务中大转弯 clip 几乎无法完成（7% vs 93%）
3. **In-context learning 而非 fine-tuning**：仅用 2 个示例即可让 GPT-5 执行有效规划，降低部署成本
4. **课程学习 + 局部坐标系**是 RL insertion 成功的重要设计：先易后难训练，clip 局部坐标系消除朝向混淆
5. **预定义原语 vs 学习原语的平衡**：Insert 用 RL（需要适应性和精准性），Pull/Flatten 用固定原语（安全性高、简单高效）

## 相关概念

- [[robotic-manipulation]]
- [[vision-language-model]]
- [[reinforcement-learning]]
- [[deformable-linear-object]]
- [[planning]]
- [[grasping]]

## 相关研究者

- [[li-mingen|Li, Mingen]]
- [[yu-houjian|Yu, Houjian]]
- [[huang-yixuan|Huang, Yixuan]]
- [[hong-youngjin|Hong, Youngjin]]
