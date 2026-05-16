---
title: "The grasp loop signature: A topological representation for manipulation planning with ropes and cables"
tags: [manipulation, DLO, bimanual, planning]
created: "2026-04-27"
updated: "2026-04-27"
type: "literature"
status: "done"
summary: "提出 GL-signature 表征双臂+DLO+障碍物的拓扑关系，用于指导重抓取规划。在 Pulling/Untangling/Threading 三个仿真任务和真实双臂穿缆任务上验证。使用 GL-signature 的方法成功率最高（Untangling 22/25, Threading 42/50），规划时间最短。"
authors: "Mitrano, Peter; Berenson, Dmitry"
year: "2024"
venue: "arXiv Preprint"
zotero_key: "Z89GT82J"
---
## 摘要

Robotic manipulation（机器人操控） of deformable, one-dimensional objects (DOOs) like ropes or cables has important potential applications in manufacturing, agriculture, and surgery. In such environments, the task may involve threading through or avoiding becoming tangled with objects like racks or frames. Grasping（抓取） with multiple grippers can create closed loops between the robot and DOO, and If an obstacle lies within this loop, it may be impossible to reach the goal. However, prior work has only considered the topology of the DOO in isolation, ignoring the arms that are manipulating it. Searching over possible grasps to accomplish the task without considering such topological information is very inefficient, as many grasps will not lead to progress on the task due to topological constraints. Therefore, we propose a grasp loop signature which categorizes the topology of these grasp loops and show how it can be used to guide planning. We perform experiments in simulation on two DOO manipulation（操控） tasks to show that using the signature is faster and succeeds more often than methods that rely on local geometry or finite-horizon planning. Finally, we demonstrate using the signature in the real world to manipulate a cable in a scene with obstacles using a dual-arm（双臂） robot.

## 中文简述

提出 GL-signature 拓扑表征，计算双臂机器人+DLO 形成的 grasp loop 与环境 obstacle loop 之间的拓扑链接数。基于 h-signature 扩展，用于 MPPI+采样式重抓取规划中过滤拓扑不当的抓取候选和黑名单策略。在 Untangling（22/25）和 Threading（42/50）任务上成功率显著优于不使用拓扑信息的方法。

**研究方向**: DLO 拓扑规划、双臂操控、运动规划

## 关键贡献

1. **GL-signature**：紧凑地表示 grasp loop（机器人+DLO 形成的闭环）与 obstacle loop（环境障碍物形成的闭环）之间的拓扑链接关系。基于 h-signature（Bhattacharya et al. 2011）扩展到 DLO 操控场景。
2. **基于 GL-signature 的规划算法**：MPPI 控制当前抓取 + 采样式重抓取规划 + GL-signature 用于（a）惩罚/过滤拓扑不当的抓取候选（b）blocklist 避免重复失败拓扑。
3. **三个仿真环境 + 真实世界验证**：Pulling（25/25）、Untangling（22/25 vs 基线 10-15/25）、Threading（42/50 vs 基线 12-21/50）。
## 结构化提取

- **Problem**: 双臂操控 DLO（绳/缆）时，机器人+DLO 形成闭环可能与环境障碍物拓扑纠缠，导致目标不可达。先前工作忽略机械臂对拓扑的影响，规划效率低。
- **Method**: GL-signature 基于 h-signature 计算机器人-DLO 闭环与障碍物闭环的拓扑链接关系。用于 MPPI + 采样式重抓取规划中过滤/黑名单拓扑不当的抓取候选。三个环境：Pulling（无障碍物，测地距离驱动）、Untangling（计算机架场景，无目标 GL）、Threading（穿缆，有目标 GL 序列）。
- **Tasks**: Pulling（25/25 拉缆到目标）、Untangling（22/25 从机架解缆）、Threading（42/50 穿缆通过 fixture 序列）。
- **Sensors**: 仿真中完整状态（关节角+DLO 点云）；真实中 CDCPD2 追踪 DOL + 手内相机视觉伺服。
- **Robot Setup**: 双臂 7-DOF + 2-DOF 躯干 + 平行夹爪（仿真），真实双臂机器人（具体型号未注明）。
- **Metrics**: 成功率（试验数）、墙钟时间（含规划）、仿真时间（不含规划）。
- **Limitations**: 需完整环境几何模型；仅处理点到达/穿缆；真实验证仅单次演示；不处理 DLO 自缠绕；MPPI 陷入后恢复不完全。
- **Evidence Notes**: 仿真实验有定量表格（Tab. I, II），GL-signature vs 4 种基线/消融对比充分。真实世界仅为定性演示（Fig. 1），无多次试验定量数据。GL-signature 计算复杂度 O((na-1)·ns·ls·la)，Python 实现 ≤10ms。整体证据强度：仿真部分强，真实部分弱。
## 本地引用关系

- [[li2025routing]]
- [[liu2025autonomous]]
- [[wang2025implicit]]
## 证据元数据

- **Zotero Key**: Z89GT82J
- **Citekey**: mitrano2024grasp
- **Authors**: Mitrano Peter, Berenson Dmitry
- **Affiliation**: University of Michigan, Department of Robotics
- **Venue**: arXiv preprint, 2024-03 (RA-L投稿)
- **Paper Type**: Methods paper (topological representation + planning)
- **Fulltext Quality**: Complete, 8 pages with algorithms, tables, and figures
- **Evidence Coverage**: High for planning method and simulation experiments; Medium for real-world validation (single demo)
- **Confidence**: High on simulation results (quantitative tables); Medium on real-world generalizability
- **Summary**: 提出 GL-signature 表征双臂+DLO+障碍物的拓扑关系，用于指导重抓取规划。在 Pulling/Untangling/Threading 三个仿真任务和真实双臂穿缆任务上验证。使用 GL-signature 的方法成功率最高（Untangling 22/25, Threading 42/50），规划时间最短。


## Problem

DLO 操控规划需要考虑机器人、DLO 和环境的拓扑关系。当双臂抓取 DLO 时，机器人+DLO 形成闭环（grasp loop），如果障碍物在这个闭环内，可能无法到达目标。先前工作只考虑 DLO 自身的拓扑（如打结），忽略了操控它的机械臂。不使用拓扑信息的规划方法会尝试很多不可能成功的抓取配置，效率极低。


## Method

### GL-signature 计算
1. **状态图构建**：以机器人基座、夹爪、附着点为顶点，以路径为边
2. **循环提取**：提取所有含夹爪的 3-顶点循环（fan graph，na 臂产生 na-1 个循环）
3. **Grasp loop 构建**：将循环的边拼接为 3D 路径
4. **h-signature 计算**：对每个 grasp loop τi 与每个 obstacle loop Sj 计算链接数 h(τi, Sj)
5. **GL(s)** = {h(τi, S)} 的多重集

### DOO Point Reaching 算法（Alg 1）
- MPPI 控制当前抓取，目标代价函数包含：关键点到目标距离 + 夹爪趋近目标 + 碰撞惩罚 + 速度正则化
- 陷入检测（trap detection）：关节变化率的滑动窗口比
- 重抓取规划：采样 ~50 个候选，代价函数包含可行性 + GL-signature 匹配/黑名单 + 测地距离 + 状态变化
- 黑名单策略：若无法找到更接近关键点的抓取 → 将当前 GL-signature 加入黑名单

### Threading 算法（Alg 2）
- 分阶段：一系列目标 GL-signature GL1,...,GLN
- 每阶段用磁场代价引导关键点穿过 fixture
- 穿过 disc 检测后切换到下一子目标
- 交替单臂抓取加速规划


## Experiments

### Untangling 环境
| 方法 | 成功率 | 墙钟时间(min) | 仿真时间(min) |
|------|--------|-------------|-------------|
| GL-signature (ours) | **22/25** | 12(5) | 1.4(1.1) |
| Always Blocklist | 22/25 | 14(7) | 1.3(1.0) |
| No GL-signature | 10/25 | 20(10) | 2.0(1.3) |
| TAMP50 | 15/25 | 142(116) | 2.4(1.7) |
| TAMP5 | 9/25 | 34(22) | 1.8(1.2) |

### Threading 环境
| 方法 | 成功率 | 墙钟时间(min) | 仿真时间(min) |
|------|--------|-------------|-------------|
| GL-signature (ours) | **42/50** | 8(2) | 1.3(0.4) |
| TAMP5 | 21/50 | 17(3) | 1.3(0.6) |
| Wang et al. [15] | 12/50 | 8(3) | 1.0(0.8) |

### Pulling 环境
- 25/25 成功（无障碍物，无 GL-signature 变化）

### 真实世界
- 双臂机器人 + 穿缆任务 + 框架障碍物
- CDCPD2 追踪 DLO + 手内相机视觉伺服引导抓取
- 成功演示穿缆（无定量成功率报告）


## Limitations

1. **需要完整环境几何模型**：假设已知骨架化环境表示，依赖手动指定或 medial axis transform，感知误差未系统性评估。
2. **仅处理点到达和穿缆任务**：不支持打结/解结（作者声明与 knot-tying 工作互补）、长时序多步操控、或其他 DLO 任务（如弯曲、打环）。
3. **真实世界验证有限**：仅展示单次简化版穿缆演示，无多次试验的定量成功率，使用 CDCPD2 追踪 + 手动调参仿真。
4. **MPPI 陷入后恢复不完全**：失败模式是关节配置导致一臂阻挡另一臂抓取 DLO 末端，无法自动恢复。
5. **抓取策略采样随机性**：~50 候选采样，无学习或记忆机制跨试验复用成功策略。
6. **不处理 DLO 自身拓扑变化**：只考虑 robot-DLO-obstacle 的拓扑关系，不考虑 DLO 自缠绕或打结。


## Key Takeaways

1. **拓扑信息对双臂 DLO 规划至关重要**：不使用 GL-signature 的方法在 Untangling 仅 10/25 成功率（贪心重抓取导致拓扑不可达），使用后提升到 22/25。这证明了拓扑约束在 DLO 操控中的核心地位。
2. **GL-signature 是通用拓扑工具**：可扩展到无人机吊运大物体、双臂搬运等场景（Fig. 5），不限于 DLO。
3. **对本研究方向的启示**：双臂 DLO 操控的规划层需要拓扑信息。GL-signature 可作为 [[li2025routing]] 的 DLO routing 的互补：Li et al. 用 RL+Diffusion 执行动作，GL-signature 提供拓扑约束过滤不可行的抓取候选。也可与 [[liu2025autonomous]] 的 RLAC 框架结合。
4. **与本地概念页的关联**：填补 [[deformable-linear-object]] 概念页中"双臂 DLO 拓扑规划"的空白，是本地首篇直接在真实双臂机器人上验证 DLO 拓扑操控的工作。

## 相关概念

- [[robotic-manipulation]]
- [[deformable-linear-object]]
- [[bimanual-manipulation]]
- [[planning]]
- [[grasping]]

## 相关研究者

- [[mitrano|Mitrano, Peter]]
- [[berenson|Berenson, Dmitry]]
