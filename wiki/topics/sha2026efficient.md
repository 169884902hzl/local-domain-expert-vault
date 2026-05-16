---
title: "Efficient and Reliable Teleoperation through Real-to-Sim-to-Real Shared Autonomy"
tags: [manipulation, imitation, RL, sim-to-real]
created: "2026-05-07"
updated: "2026-05-07"
type: "literature"
status: "done"
summary: "提出基于 kNN 人类代理和残差 RL 的 real-to-sim-to-real 共享自主框架，用少于5分钟遥操作数据训练残差 copilot，在齿轮啮合、螺母旋拧和销钉插入三类精密接触任务中显著提升新手和熟手的操控表现，并改善下游模仿学习数据质量。"
authors: "Sha, Shuo; Wang, Yixuan; Huang, Binghao; Loquercio, Antonio; Li, Yunzhu"
year: "2026"
venue: "arXiv Preprint"
zotero_key: "3KBN8UVR"
---
## 摘要

Fine-grained, contact-rich（接触丰富） teleoperation remains slow, error-prone, and unreliable in real-world manipulation（操控） tasks, even for experienced operators. Shared autonomy offers a promising way to improve performance by combining human intent with automated assistance, but learning effective assistance in simulation requires a faithful model of human behavior, which is difficult to obtain in practice. We propose a real-to-sim-to-real（仿真到真实迁移） shared autonomy framework that augments human teleoperation with learned corrective behaviors, using a simple yet effective k-nearest-neighbor (kNN) human surrogate to model operator actions in simulation. The surrogate is fit from less than five minutes of real-world teleoperation data and enables stable training of a residual copilot policy with model-free reinforcement learning（强化学习）. The resulting copilot is deployed to assist human operators in real-world fine-grained manipulation（操控） tasks. Through simulation experiments and a user study with sixteen participants on industry-relevant tasks, including nut threading, gear meshing, and peg insertion, we show that our system improves task success for novice operators and execution efficiency for experienced operators compared to direct teleoperation and shared-autonomy baselines that rely on expert priors or behavioral-cloning pilots. In addition, copilot-assisted teleoperation produces higher-quality demonstrations for downstream imitation learning（模仿学习）.

## 中文简述

提出基于强化学习的插入方法，具有仿真到真实迁移特点。

**研究方向**: 机器人操控、模仿学习、强化学习、仿真到真实迁移

## 关键贡献

1. 提出 real-to-sim-to-real 共享自主管线，支持多种高精度接触丰富装配任务的遥操作辅助
2. 证明轻量级 kNN 模型（用不到5分钟人类遥操作数据构建）可作为 model-free RL 仿真训练中有效的人类代理
3. 实验证明系统同时提升新手操作者的成功率和熟手操作者的执行效率，并产生更高质量的下游模仿学习数据
## 结构化提取

- Problem: 精密接触丰富的遥操作任务（齿轮啮合/螺母旋拧/销钉插入）中人类难以提供持续精确的低级控制，现有共享自主方法依赖专家先验或大规模人类数据
- Method: Real-to-sim-to-real 残差 copilot 学习；kNN 人类代理 + PPO 训练残差策略 + 导纳控制 + 域随机化 Sim-to-Real
- Tasks: Gear Meshing, Nut Threading, Peg Insertion（NIST Board #1，径向间隙 <1mm）
- Sensors: RealSense D455 RGB-D（FoundationPose 位姿估计）+ 腕部力矩传感器 + 本体感受（关节角、末端位姿）
- Robot Setup: UFactory xArm7（7-DOF）+ GELLO 遥操作臂，桌面固定安装，15Hz 控制频率
- Metrics: 成功率、完成时间、NASA-TLX 工作负荷、用户满意度、任务进展度（1-e/e_max）、下游 DP 性能
- Limitations: 共适应假设未建模；仿真构建需手动数字化；仅评价 NIST Board 任务；用户可能因 copilot 存在而改变行为
- Evidence Notes: 全文精读，含主文+附录+表格。Q1 用户研究含16人、20+小时试验。Q2 交叉代理泛化仿真实验（1000 trials/条件）。Q3 下游模仿学习对比（matched attempts + matched successes）。附录提供完整 RL 超参数、域随机化参数、奖励设计和 Diffusion Policy 训练细节。
## 本地引用关系

- [[sha2026efficient]]
## 证据元数据

- Fulltext Quality: fulltext
- Evidence Coverage: complete（含主文、附录、表格、参考文献全部内容）
- Confidence: high
- Summary: 提出基于 kNN 人类代理和残差 RL 的 real-to-sim-to-real 共享自主框架，用少于5分钟遥操作数据训练残差 copilot，在齿轮啮合、螺母旋拧和销钉插入三类精密接触任务中显著提升新手和熟手的操控表现，并改善下游模仿学习数据质量。


## Problem

精细接触丰富的遥操作任务（如齿轮啮合、螺母旋拧、销钉插入）在实际操控中仍然缓慢、易错且不可靠，即使对有经验操作者也是如此。现有共享自主方法存在两个根本局限：
1. **依赖专家先验**：需要预先获得足够强大的自主策略，而获取这种策略本身往往比遥操作问题更难
2. **人类代理模型难获取**：copilot 学习方法需要在仿真中替代人类进行训练，但参数化行为克隆代理在低数据量下脆弱且难以应对 copilot 探索导致的分布偏移


## Method

### 整体框架
将共享自主建模为 POMDP：状态 $x_t = (s_t, g)$，其中 $s_t$ 为环境状态，$g$ 为人类操作者的隐式目标。copilot 观测 $o_t = (s_t, a^h_t)$，输出残差修正动作，最终动作为 $a_t = a^h_t \oplus \alpha a^{res}_t$。

### kNN Pilot（人类代理）
- **核心思想**：非参数 kNN 检索，从真实遥操作数据中直接查找最相似动作，避免分布外推
- **距离度量**：基于本体感受的末端执行器命令空间上的加权距离（平移、旋转、夹爪）
- **动作分块（Action Chunking）**：检索时输出短序列连续动作，保持时间一致性
- **平滑局部扰动**：通过 Bernoulli 门控注入时间相关噪声，扩展经验数据覆盖范围
- **数据效率**：仅需不到5分钟真实遥操作数据

### 残差 Copilot 训练
- 使用 PPO（actor-critic，LSTM + MLP backbone，高斯策略头）
- 奖励设计：$R = R_{general} + R_{success}$，包含终止惩罚、接触力惩罚、对齐塑形、动作正则化和稀疏成功奖励
- 观测空间：35D（末端位姿、速度、相对物体位姿、基动作、前一残差动作）
- 动作空间：7D 残差（平移增量 + 轴角旋转增量 + 夹爪增量）

### 导纳控制
使用虚拟弹簧-质量-阻尼模型实现任务空间柔顺控制，末端执行器在接触时可以顺应外力同时跟踪目标命令。

### Real-to-Sim-to-Real 管线
- **Real-to-Sim**：数字化人类代理（kNN）和任务环境；系统辨识包括关节空间 PID 增益、任务空间导纳增益、摩擦系数和物体质心
- **Sim-to-Real**：域随机化覆盖控制器参数、物体位姿观测和初始配置


## Experiments

### 实验设置
- **任务**：NIST Board #1 上三类精密装配任务（径向间隙 <1mm）
  - Gear Meshing（齿轮啮合）：拾取齿轮→插入轴→啮合
  - Nut Threading（螺母旋拧）：M32 螺母旋紧至少180°
  - Peg Insertion（销钉插入）：8mm 销钉插入底座
- **硬件**：UFactory xArm7 + GELLO 遥操作 + RealSense D455 + 腕部力矩传感器
- **感知**：FoundationPose 进行物体位姿估计
- **仿真**：NVIDIA Isaac Lab + PhysX (TGS solver, 192 position iterations)
- **参与者**：16人（12新手 + 4熟手），总计超过20小时遥操作试验

### 主要结果

**用户研究（Q1 - Copilot 表现）**：
- 残差 copilot 在所有任务中一致优于直接遥操作
- Nut Threading：copilot 提升成功率高达30%，通过稳定旋转和放大有效旋转命令
- Gear Meshing：copilot 学习可靠的插入深度和微小旋转修正，减少低级对齐负担
- Peg Insertion：copilot 稳定预抓取姿态，提高抓取可靠性
- 主观评价：NASA-TLX 工作负荷降低，用户满意度提升

**人类代理分析（Q2 - kNN vs 其他代理）**：
- 交叉代理泛化实验（Table I）：kNN-based copilot 在分布内和分布外评价中均表现最佳
- Residual BC（使用 DP 作为代理）在分布偏移下失败率更高，收敛到局部最优
- GD Copilots（引导扩散）对代理模型高度敏感：GD Expert 在接触敏感任务中表现差（Nut Threading 进展不超过34%）
- GD 方法存在非对称性：测试时引导无法同时保证动作最优性和保留人类意图

**下游模仿学习数据质量（Q3）**：
- 在 matched attempts 条件下：
  - Copilot 数据：18/20 抓取成功，11/20 插入成功
  - 遥操作数据：7/20 抓取成功，1/20 插入成功
- 在 matched successes 条件下（控制成功示范数量）：
  - Copilot 数据：19/20 抓取成功，9/20 插入成功
  - 遥操作数据：6/20 抓取成功，0/20 插入成功
- 质量差异归因于 copilot 辅助产生的轨迹更一致：对齐、接触时机和接近策略更稳定

### 消融与额外实验
- 域随机化细节（Table IV）：控制器参数、物体位姿、初始配置、人类代理扰动
- 奖励设计细节（Table V）：R_general + R_success 分解
- RL 超参数（Table VI）：LSTM 2层1024单元，PPO clip ε=0.2，128 actors
- Diffusion Policy 训练细节（Table VII）：状态版和视觉版


## Limitations

1. **共适应假设**：假设用户在数据收集时的行为与 copilot 辅助下的行为一致，实际中用户可能因 copilot 存在而发展出新的策略，引入额外分布偏移
2. **未来方向**需要在线更新人类代理或学习联合考虑人类行为和 copilot 辅助的交互策略
3. 仿真构建需要手动数字化环境和系统辨识（虽然已有半自动化工具）
4. 评价局限于 NIST Board 任务，尚未扩展到更广泛的操控场景


## Key Takeaways

1. **残差策略架构**：残差公式自然分离人类意图（高层）和 copilot 修正（低层），对 DLO 操控中需要人类提供语义指导同时需要精确力控的场景有启发
2. **kNN 代理的数据效率**：非参数方法在低数据量下比参数化 BC 更稳定，避免分布外推——可用于建模 DLO 操控中的人类行为模式
3. **共享自主改善数据质量**：copilot 辅助遥操作产生的示范数据更适合下游模仿学习，这对 DLO 操控的数据收集管线设计有参考价值
4. **Real-to-sim-to-real 管线设计**：系统辨识+域随机化策略对接触丰富任务有效，可迁移到 DLO 的仿真构建中

## 相关概念

- [[robotic-manipulation]]
- [[imitation-learning]]
- [[reinforcement-learning]]
- [[sim-to-real]]
- [[diffusion-model]]
- [[deformable-linear-object]]
- [[grasping]]

## 相关研究者

- [[sha|Sha, Shuo]]
- [[wang-yixuan|Wang, Yixuan]]
- [[huang-binghao|Huang, Binghao]]
- [[loquercio|Loquercio, Antonio]]
- [[li-yunzhu|Li, Yunzhu]]
