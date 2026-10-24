---
title: "CoRAL: Contact-Rich Adaptive LLM-based Control for Robotic Manipulation"
tags: [manipulation, imitation, VLM, sim-to-real, planning]
created: "2026-05-06"
updated: "2026-05-06"
type: "literature"
status: "done"
summary: "提出 CoRAL 模块化框架，用 LLM 作为 MPPI 代价函数设计器（非直接控制器），结合 VLM 语义物理先验、在线系统辨识和 RAG 记忆单元，实现接触丰富操控的零样本规划，在 6 项仿真/真实任务上超越 OpenVLA 和 π₀.5 等 VLA 基线。"
authors: "Çiçek, Berk; Er, Mert K.; Öğüz, Özgür S."
year: "2026"
venue: "arXiv Preprint"
zotero_key: "47G6ZGW2"
---
## 摘要

While Large Language Models (LLMs) and Vision-Language Models (VLMs) demonstrate remarkable capabilities in high-level reasoning and semantic understanding, applying them directly to contact-rich（接触丰富） manipulation（操控） remains a challenge due to their lack of explicit physical grounding and inability to perform adaptive control. To bridge this gap, we propose CoRAL (Contact-Rich（接触丰富） Adaptive LLM-based control), a modular framework that enables zero-shot（零样本） planning by decoupling high-level reasoning from low-level control. Unlike black-box policies, CoRAL uses LLMs not as direct controllers, but as cost designers that synthesize context-aware objective functions for a sampling-based motion planner (MPPI). To address the ambiguity of physical parameters in visual data, we introduce a neuro-symbolic adaptation loop: a VLM provides semantic priors for environmental dynamics, such as mass and friction estimates, which are then explicitly refined in real time via online system identification, while the LLM iteratively modulates the cost-function structure to correct strategic errors based on interaction feedback. Furthermore, a retrieval-based memory unit allows the system to reuse successful strategies across recurrent tasks. This hierarchical architecture ensures real-time control stability by decoupling high-level semantic reasoning from reactive execution, effectively bridging the gap between slow LLM inference and dynamic contact requirements. We validate CoRAL on both simulation and real-world hardware across challenging and novel tasks, such as flipping objects against walls by leveraging extrinsic contacts. Experiments demonstrate that CoRAL outperforms state-of-the-art（现有最优方法） VLA and foundation-model-based planner baselines by boosting success rates over 50% on average in unseen contact-rich（接触丰富） scenarios, effectively handling sim-to-real（仿真到真实迁移） gaps through its adaptive physical understanding.

## 中文简述

提出基于视觉-语言的操控方法，具有仿真到真实迁移特点。

**研究方向**: 机器人操控、模仿学习、视觉-语言模型、仿真到真实迁移、运动规划

## 关键贡献

1. **LLM 作为代价函数设计器**：首次将 LLM 用作 MPPI 采样式运动规划器的上下文感知代价函数生成器，而非直接控制器或策略网络，实现零样本接触丰富操控规划
2. **神经符号自适应闭环**：VLM 提供语义物理先验（质量、摩擦），在线系统辨识实时修正，LLM 基于交互反馈迭代调整代价函数结构和接触策略
3. **分层控制架构**：三层频率（1kHz 阻抗控制 / 10Hz MPPI / ~1Hz LLM），将高层语义推理与低层反应式执行解耦，解决 LLM 推理延迟问题
4. **RAG 记忆单元**：基于检索增强生成存储成功经验，实现跨任务的策略复用，为终身学习奠定基础
## 结构化提取

- Problem: 接触丰富机器人操控中，VLA 模型缺乏物理接地和自适应控制能力，现有 LLM+规划器方法无法在线修正物理参数偏差
- Method: 模块化神经符号框架，LLM 生成 MPPI 代价函数和接触策略，VLM 提供语义物理先验，在线系统辨识修正参数，RAG 记忆复用经验
- Tasks: 推+抓砧板、抓取盒子、杂乱环境抓取放置、恒力推送、翻转盒子、墙壁翻转（6 项仿真 + 6 项真实）
- Sensors: RGB-D 固定相机、关节本体感受、力/力矩传感器、Vicon 动捕（真实世界）
- Robot Setup: Franka Emika Panda 7-DoF + 平行爪夹持器，i9-13900K + RTX 4060 Ti
- Metrics: Success Rate（10 次试验二值成功率）、平均执行时间
- Limitations: 依赖世界模型保真度、通用 LLM 代价函数质量不保证、推理延迟、需要已知 3D 模型、复杂任务仍低于专家设计
- Evidence Notes: 完整全文精读，包含主文实验表格（Table I/II）、消融分析、鲁棒性分析、附录中 LLM prompt 模板和代码示例
## 本地引用关系

- [[iek2026coral]]
## 证据元数据

- Fulltext Quality: fulltext
- Evidence Coverage: 100%（全文通过 arXiv 获取并完整阅读，包含主文、附录、代码示例和 prompt 模板）
- Confidence: high
- Summary: 提出 CoRAL 模块化框架，用 LLM 作为 MPPI 代价函数设计器（非直接控制器），结合 VLM 语义物理先验、在线系统辨识和 RAG 记忆单元，实现接触丰富操控的零样本规划，在 6 项仿真/真实任务上超越 OpenVLA 和 π₀.5 等 VLA 基线。


## Problem

现有 VLA 模型（如 OpenVLA、π₀）通过模仿学习将视觉-语言输入映射为低层动作，但在接触丰富（contact-rich）操控任务上表现差。这些任务（如利用墙壁翻转物体、维持恒定推力）要求精确调控外部接触力，而非简单的碰撞避免。核心挑战：
1. VLA 缺乏显式物理接地，无法进行自适应控制
2. 基于模仿学习的方法依赖大量遥操作数据，泛化性差
3. 现有 LLM+规划器方法（如 L2R）使用静态代价函数，无法在线修正物理参数偏差


## Method

### 整体架构
CoRAL 由四个核心模块组成：Vision Pipeline、LLM Task Formulation、MPPI Controller（Inner Loop）、LLM Online Adaptation（Outer Loop），辅以 Memory Unit。

### A. 环境感知与世界模型初始化
- **位姿估计**：FoundationPose 从 RGB-D 图像估计并跟踪物体 6-DoF 位姿（真实世界用 Vicon 动捕替代）
- **语义物理先验**：VLM（GPT-4o）基于视觉输入和任务描述推断物理属性（质量、摩擦系数），作为信念初始化参数 θ

### B. LLM 驱动的任务规划与记忆检索
- **记忆检索**：RAG 机制，用任务描述和世界参数检索历史成功经验（代价函数 J_mem + 接触策略 C_mem）
- **从头规划**：
  - 生成 MPPI 代价函数 J₀：LLM 自由构造由状态、位姿、动作变量组成的加权代价项（不限于固定项集合），支持多阶段任务通过阶段条件切换代价函数
  - 生成接触策略 C₀：LLM 输出语义接触区域（中心点 c_ref + 空间扩展因子 r），程序化构建椭球体并在物体表面流形上采样候选接触点，以软代价吸引子方式引导 MPPI 采样

### C. 反应式规划与执行（内循环）
- **MPPI 控制器**：10Hz 运行，采样 K=256 条扰动轨迹，规划时域 H=32 步，通过指数加权平均更新控制序列
- **自适应温度 λ**：基于有效样本量（ESS）目标在线调节，通过二分法求解，避免固定温度的脆弱性
- **反应式控制增强**：最终指令 δ_t = u_t + Kf·(x_des - x_measured)，融合力/力矩传感器反馈

### D. 在线自适应（外循环）
- 当内循环连续失败 N_retry 次后触发
- **世界模型修正**：LLM 作为系统辨识代理，分析交互历史修正质量/摩擦参数
- **策略精化**：LLM 重写代价函数代码，调整权重或提出全新接触策略
- 输出自然语言诊断解释 + 修正后的参数/代码

### E. 三层控制频率
- Tier 1（硬件层）：1kHz 关节阻抗控制，保证安全和柔顺性
- Tier 2（轨迹层）：10Hz MPPI 重规划
- Tier 3（推理层）：~1Hz LLM 异步更新代价结构


## Experiments

### 实验设置
- **仿真平台**：robosuite/MuJoCo，Franka Emika Panda 7-DoF + 平行爪夹持器
- **真实平台**：同型号物理机器人，Vicon 6 摄像头动捕替代 FoundationPose
- **传感器**：RGB-D 固定相机、本体感受、力/力矩（仿真/真实均有）
- **LLM/VLM**：均为 GPT-4o
- **硬件**：i9-13900K + 64GB RAM + RTX 4060 Ti
- **评估方式**：每任务 10 次试验，随机化物体初始位姿、质量、摩擦系数和尺寸

### 六项任务
| Task | 描述 | 类型 |
|------|------|------|
| T1 | Push + Pick Cutting Board | 多阶段接触丰富 |
| T2 | Pick Box | 标准抓取 |
| T3 | Pick and Place in Clutter | 杂乱环境抓取 |
| T4 | Push with Constant Force | 恒力控制 |
| T5 | Flip Box | 动态翻转 |
| T6 | Flip with Wall | 多接触墙壁翻转 |

### 仿真结果（Table I）
| Method | T1 | T2 | T3 | T4 | T5 | T6 |
|--------|-----|-----|-----|-----|-----|-----|
| CoRAL | **5/10** | **10/10** | **10/10** | **9/10** | **9/10** | **7/10** |
| OpenVLA-OFT | 0/10 | 10/10 | 9/10 | 0/10 | 1/10 | 0/10 |
| π₀.5 | 0/10 | 10/10 | 8/10 | 0/10 | 3/10 | 0/10 |
| L2R | 0/10 | 10/10 | 9/10 | 5/10 | 4/10 | 1/10 |
| Expert(FSM) | 8/10 | 10/10 | 10/10 | 10/10 | 10/10 | 9/10 |
| Expert(single) | 0/10 | 10/10 | 10/10 | 9/10 | 9/10 | 3/10 |

### 真实世界结果（Table II）
| Task | 成功率 | 平均执行时间 |
|------|--------|-------------|
| T1 | 4/10 | 21.6±5.5s |
| T2 | 10/10 | 16.7±1.1s |
| T3 | 10/10 | 22.0±1.5s |
| T4 | 9/10 | 11.7±1.9s |
| T5 | 7/10 | 9.2±2.6s |
| T6 | 6/10 | 25.3±4.9s |

### 消融实验关键发现
- **w/o Pose Tracking**：全部任务 0/10，VLM 无法替代专用位姿估计器
- **w/o Refinement**：T1 从 5/10 降至 0/10，在线自适应对多阶段任务至关重要
- **w/o Memory**：T1 从 5/10 降至 2/10，记忆单元显著提升经验复用
- **Unified VLM**：几乎所有复杂任务失败，证明 VLM/LLM 角色分离的必要性

### 鲁棒性分析
- **接触策略引导**：LLM 引导 vs 无引导在 T6 上，效率提升 83.9%（32 vs 199 步），路径缩短 63.9%（1.33m vs 3.69m）
- **在线参数适应**：初始质量偏差 8 倍（2.0kg vs 0.25kg）时，LLM 能通过迭代修正收敛至真实值
- **力调节**：T4 真实世界力曲线显示 MPPI 能将接触力稳定在 ~5N 目标范围内


## Limitations

1. **内部世界模型保真度**：框架依赖仿真规划世界的准确性，VLM 幻觉（如误判材料导致质量估计严重偏差）可能导致规划器无法收敛
2. **通用 LLM 的局限**：使用通用 GPT-4o 生成代价函数，对于完全新颖或抽象任务的代价函数质量不保证，未来需针对机器人控制微调专用 LLM
3. **推理延迟**：LLM 推理速度（~1Hz）限制了高层策略的更新频率
4. **依赖已知 3D 模型**：FoundationPose 需要已知物体几何模型，限制了完全未见物体的处理能力
5. **简单任务与专家差距**：在 T1 上（5/10）仍明显低于 Expert(FSM)（8/10），表明 LLM 生成的代价函数还有优化空间


## Key Takeaways

1. **LLM 做规划器而非控制器是可行路径**：将 LLM 定位为代价函数设计者而非直接输出动作的策略，避免了端到端 VLA 在接触丰富任务上的脆弱性，且提供了可解释性
2. **在线系统辨识是关键**：通过 LLM 分析交互历史修正物理参数信念，是从零样本走向自适应的可行方案，对 DLO 操控中参数不确定性问题有启发
3. **VLM/LLM 角色必须分离**：统一 VLM 处理感知+规划的消融几乎全面失败，证明专用模块的必要性
4. **对 DLO 操控的启发**：CoRAL 的接触策略生成（语义区域→几何采样→软代价吸引子）可适配 DLO 的抓取点选择；在线参数适应可处理 DLO 的材料属性不确定性；分层控制架构可解决 DLO 长时域任务
5. **局限性明确**：需要已知 3D 模型、依赖 VLM 物理先验质量、LLM 推理延迟，这些在 DLO 场景中可能更突出（DLO 无固定几何）

## 相关概念

- [[robotic-manipulation]]
- [[imitation-learning]]
- [[vision-language-model]]
- [[sim-to-real]]
- [[planning]]
- [[deformable-linear-object]]
- [[grasping]]

## 相关研究者

- [[cicek|Çiçek, Berk]]
- [[er-mert|Er, Mert K.]]
- [[oguz|Öğüz, Özgür S.]]
