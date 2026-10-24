---
title: "ManipArena: Comprehensive Real-world Evaluation of Reasoning-Oriented Generalist Robot Manipulation"
tags: [manipulation, VLM, RL, sim-to-real, robot-learning]
created: "2026-05-06"
updated: "2026-05-06"
type: "literature"
status: "done"
summary: "ManipArena 是面向推理导向通用机器人操控的标准化真实世界评测框架，包含 20 个任务、10812 条专家轨迹，通过绿幕控制环境、分层 OOD 设计和 Real2Sim 同步，系统诊断 VLA 和世界模型在执行推理、语义推理和移动操控上的能力边界。"
authors: "Sun, Yu; Cao, Meng; Yang, Ping; Xu, Rongtao; Yan, Yunxiao et al."
year: "2026"
venue: "arXiv Preprint"
zotero_key: "F4C2PZGX"
---
## 摘要

Vision-Language-Action (VLA) models and world models have recently emerged as promising paradigms for general-purpose robotic intelligence, yet their progress is hindered by the lack of reliable evaluation protocols that reflect real-world deployment. Existing benchmarks are largely simulator-centric, which provide controllability but fail to capture the reality gap caused by perception noise, complex contact dynamics, hardware constraints, and system latency. Moreover, fragmented real-world evaluations across different robot platforms prevent fair and reproducible comparison. To address these challenges, we introduce ManipArena, a standardized evaluation framework designed to bridge simulation and real-world execution. ManipArena comprises 20 diverse tasks across 10,812 expert trajectories emphasizing reasoning-oriented manipulation（操控） tasks requiring semantic and spatial reasoning, supports multi-level generalization through controlled out-of-distribution settings, and incorporates long-horizon（长时序） mobile manipulation（移动操控） beyond tabletop scenarios. The framework further provides rich sensory diagnostics, including low-level motor signals, and synchronized real-to-sim environments constructed via high-quality 3D scanning. Together, these features enable fair, realistic, and reproducible evaluation for both VLA and world model approaches, providing a scalable foundation for diagnosing and advancing embodied intelligence systems.

## 中文简述

提出基于视觉-语言的移动操控方法，具有泛化能力特点。

**研究方向**: 机器人操控、视觉-语言模型、强化学习、仿真到真实迁移、机器人学习

## 关键贡献

1. **标准化真实世界评测框架**：20 个多样化任务、10,812 条专家轨迹，涵盖执行推理（10）、语义推理（5）、移动操控（5）三类
2. **受控泛化评测**：绿幕封闭环境 + 系统化多样性设计 + 分层 OOD 评测（T1-T4 域内 → T5-T8 视觉偏移 → T9-T10 语义 OOD）
3. **丰富传感诊断**：提供 56D/62D 状态和动作向量，包含电机电流和关节速度（超出标准 LeRobot 格式）
4. **Real2Sim 同步**：使用 3D Gaussian Splatting 和 Hunyuan3D 构建物理一致的仿真对应环境
5. **服务端推理架构**：参与者提交单一 HTTP 端点，主办方统一评测，确保公平性和可复现性
6. **一站式模型规则**：一个模型处理所有任务，测试真正的推理和泛化能力而非任务特化过拟合
7. **基线诊断分析**：评估 π0.5-Single、π0.5-OneModel、DreamZero，揭示 VLA 与世界模型在五个能力维度上的互补性
## 结构化提取

- **Problem**: VLA 和世界模型缺乏标准化真实世界评测协议，仿真 benchmark 无法反映 reality gap，真实世界评测碎片化
- **Method**: 绿幕封闭环境 + 三层多样性设计 + 分层 OOD 评测 + 服务端推理 + Real2Sim（3DGS + Hunyuan3D + IsaacLab）
- **Tasks**: 20 个任务（执行推理 10 + 语义推理 5 + 移动操控 5），涵盖抓取、插入、倒水、分类、配对、导航操控等
- **Sensors**: 3 路 RGB 摄像头（face, left wrist, right wrist, 640×480, 20fps）+ 56D/62D 本体感受（关节位置/速度/电流 + 末端执行器位姿）
- **Robot Setup**: X2Robot 双臂系统（桌面 4 单元，6-DOF 双臂）；Quanta X1 移动机器人（麦克纳姆轮 + 可调升降柱 + 双臂 ARX 臂）
- **Metrics**: 子任务评分制（0-10/试验），总分 1500（15 桌面任务 × 10 试验）；成功率 SR 定义为单次 ≥9/10；泛化退化曲线
- **Limitations**: 移动任务基线未完成；单一平台；基线少（3 个模型）；绿幕不代表所有真实环境；DLO 任务未评测
- **Evidence Notes**:

  - Table 4 提供完整 15 任务基线结果（π0.5-Single 626.3, OneModel 640.5, DreamZero 500.3 /1500）
  - Figure 11 展示 OOD 退化曲线：VLA 崩溃式退化（-95%），WAM 平缓退化（-33%）
  - Figure 12 五维能力矩阵：三模型互补，无主导者
  - 4 个任务所有模型 <30 分（pour_water, insert_wireline, arrange_cup, put_stationery），标识为开放前沿
  - 移动操控 5 个任务评测 in progress，无定量结果
## 本地引用关系

-
## 证据元数据

- Fulltext Quality: fulltext (HTML 全文，含正文、附录表格和图表描述)
- Evidence Coverage: 完整覆盖正文 1-4 节和附录 5-8 节；移动操控基线实验尚未完成（论文明确标注 in progress）
- Confidence: high
- Summary: ManipArena 是面向推理导向通用机器人操控的标准化真实世界评测框架，包含 20 个任务、10812 条专家轨迹，通过绿幕控制环境、分层 OOD 设计和 Real2Sim 同步，系统诊断 VLA 和世界模型在执行推理、语义推理和移动操控上的能力边界。


## Problem

VLA 模型和世界模型在通用机器人智能方面展现了潜力，但其进展受到**评测协议不足**的制约：

1. **仿真-真实鸿沟**：现有 benchmark（RLBench、LIBERO、CALVIN、VLABench）以仿真为中心，无法反映感知噪声、复杂接触动力学、硬件约束和系统延迟导致的 reality gap
2. **真实世界评测碎片化**：各研究团队使用不同机器人平台和环境，无法公平对比和复现
3. **缺乏推理导向评测**：现有 benchmark 缺乏需要语义/空间推理的操控任务，多为简单 pick-and-place


## Method

### 核心设计原则（5 条）
1. **推理导向**：所有任务都需要推理，没有简单 pick-and-place 基线；仅推理瓶颈位置不同
2. **多层泛化**：通过受控 OOD 设置测试 Level 1（外观泛化）→ Level 2（空间泛化）→ Level 3（语义泛化）
3. **移动操控**：超越桌面，包含长时序导航 + 全身控制
4. **丰富传感**：电机电流作为力矩代理，关节速度捕获动态运动特征
5. **Real2Sim 同步**：3DGS 重建 + Hunyuan3D 物体生成，基于 IsaacLab 的仿真环境

### 竞赛架构
- 服务端推理：参与者暴露 HTTP 端点，主办方控制机器人、收集数据、评分
- 一模型通吃：单一模型评测所有任务，禁止任务特化
- 10 次试验/任务，子任务评分制（0-10 分/试验），15 个桌面任务总分 1500

### 受控评测环境
- **绿幕封闭环境**：统一 chroma-key 墙壁和天花板，固定人工照明（恒定色温、恒定强度）
- 三个关键属性：变量隔离、受控照明、可复现/可移植
- 未来可通过 chroma-key 合成自然场景背景，研究视觉鲁棒性

### 系统化多样性设计（三层）
- **Level 1 — 物理属性多样性**：材质、颜色、尺寸变化（感知泛化）
- **Level 2 — 空间配置多样性**：物体位置和朝向随机化（空间泛化）
- **Level 3 — 语义组合多样性**：不同物体组合、排序、类别分配（语义泛化，仅语义推理任务）
- 每任务 2-7 个显式控制的多样性维度，收集约 500 条轨迹/任务

### 分层 OOD 评测设计
- **T1-T4**：域内（训练分布物体 + 变化位置）
- **T5-T8**：视觉偏移（同分布内外观变化，如不同形状/颜色）
- **T9-T10**：语义 OOD（训练中未见过的物体）
- 语义距离分级：near-OOD（安全护目镜）→ medium-OOD（蓝牙耳机）→ far-OOD（颈挂式耳机 + 白色）

### 机器人平台
- **桌面**：X2Robot 双臂系统，4 个单元，每个配 6-DOF 双臂 + 主从遥操作接口 + 3 摄像头（face, left wrist, right wrist）
- **移动**：Quanta X1，麦克纳姆轮全向底盘 + 高度可调升降柱 + 双臂 ARX 臂，~3m×3m 绿幕空间
- 统一 embodiment 消除硬件差异

### 传感和动作空间
- **桌面任务**：56D/帧（末端执行器位姿 14D + 关节位置 14D + 关节速度 14D + 关节电流 14D）
- **移动任务**：62D/帧（56D + 头部旋转 2D + 升降高度 1D + 底盘速度 3D）
- 3 路 RGB 摄像头（640×480, 20fps）：face, left wrist, right wrist
- 数据格式：LeRobot v2.1

### Real2Sim
- IsaacLab + IsaacLab-Arena 平台
- 3D Gaussian Splatting 重建物理工作空间
- Hunyuan3D 生成高质量 3D 物体资产
- 轨迹级对齐：在仿真中重放真实机器人关节轨迹


## Experiments

### 基线模型
| 模型 | 类型 | 描述 |
|------|------|------|
| π0.5-Single | 任务特化 VLA | 每任务独立微调，15 个专家 |
| π0.5-OneModel | 统一多任务 VLA | 单一模型联合训练 15 个桌面任务 |
| DreamZero | 世界动作模型 | 自回归视频扩散，"做梦"未来帧后提取动作 |

- 输入：3 路摄像头 + 本体感受状态
- 输出：14D 末端执行器位姿动作
- 推理延迟：π0.5 ~110ms/步（~9Hz），DreamZero ~4-8s/步（50-70× 慢于 VLA）
- 成功标准：单次试验 ≥9/10 分

### 整体结果（Table 4）
| 指标 | π0.5-Single | π0.5-OneModel | DreamZero |
|------|------------|--------------|-----------|
| 总分 /1500 | 626.3 | **640.5** | 500.3 |

- benchmark 远未饱和：最佳总分仅 42.7%
- 无单一模型主导：OneModel 赢 7/15 任务，Single 赢 3，DreamZero 赢 4
- 模型间低相关性（r=0.34-0.74），不同任务优势差异显著
- 4 个任务所有模型均低于 30 分：pour_water(19)、insert_wireline(24)、arrange_cup(25)、put_stationery(26)

### Single vs. Multi-Task VLA 对比
- **多任务增益**：语义识别跨任务迁移提升 ++109%（sort_headphone）、++145%（pair_up_items）
- **多任务代价**：任务特化程序性知识遗忘 -73%（press_button）、-79%（put_items_drawer）
- 结论：多任务训练增强跨任务视觉识别，但稀释任务特化程序记忆

### VLA vs. 世界模型
1. **粗粒度成功，细粒度失败**：DreamZero 在粗放 pick-place 任务主导（pick_items: 97.8），但精细操控失败（put_glasses: 37 vs OneModel 87）
2. **语义理解差距**：语言指令完全指定目标时 WAM 可竞争；需从视觉场景推断具体计划时 VLA 更强
3. **OOD 鲁棒性**：DreamZero 退化更平缓（sort_headphone: -33% vs OneModel -95%），空间不变性更好（basket 位置: -8% vs -44%）
4. **空间配置敏感性**：VLA 的 OOD"泛化"可能是偶然的空间配置对齐而非真正的物体理解

### 五维能力边界（Figure 12）
| 能力维度 | 最强模型 | 证据 |
|---------|---------|------|
| 粗放操控 | DreamZero | pick_items: 97.8 vs OneModel 37 |
| 精细操控 | OneModel | put_glasses: 87 vs DreamZero 37 |
| 序列推理 | π0.5-Single | press_button: 48 vs OneModel 13 vs DreamZero 3 |
| 语义理解 | OneModel | 4 任务均值 70.4 |
| 空间鲁棒性 | DreamZero | 位置偏移 -8% vs VLA -44%~-57% |

### 关键发现总结
1. 多任务 VLA 训练：语义识别增益 (+109%) vs 程序记忆遗忘 (-73%) 的权衡
2. WAM 与 VLA 互补：WAM 空间不变性和 OOD 鲁棒性更优，但仅适用于粗放操控
3. 力敏感精细操控（倒水、插入、拉链）是共同前沿，最佳得分 26/100


## Limitations

1. **移动操控评测未完成**：5 个移动任务的基线实验标注为 "in progress"，是重大缺失
2. **单一机器人平台**：仅 X2Robot，无法评估跨 embodiment 迁移
3. **基线数量有限**：仅 3 个模型（π0.5 两种配置 + DreamZero），未涵盖 OpenVLA、RT-2 等其他主流 VLA
4. **绿幕环境局限**：受控环境不代表所有真实世界条件（如自然光照、杂乱背景），尽管论文讨论了未来通过 chroma-key 合成解决
5. **严格成功阈值**：≥9/10 为成功可能过于严格，但论文论证 partial credit 提供更细粒度诊断
6. **DLO 任务覆盖有限**：移动任务 put_clothes_in_hamper 涉及衣物（可变形物体），但尚未评测
7. **数据量**：每任务约 500 条轨迹，对于大规模 VLA 训练可能不够


## Key Takeaways

1. **评测框架设计思路**：绿幕封闭环境 + 分层多样性 + 分层 OOD 的三层设计是可复用的 benchmark 设计范式，对 DLO 操控评测也有借鉴价值
2. **VLA vs WAM 互补性**：对双臂 DLO 操控有启发——VLA 的精细动作预测适合精确操控，WAM 的物理推理和空间不变性适合应对 DLO 的形变不确定性
3. **力感知是前沿**：论文提供的电机电流数据（force proxy）是 DLO 操控中感知接触力的重要信号来源
4. **多任务训练权衡**：在 DLO 场景中需要平衡跨物体泛化与任务特化操控策略的保留
5. **Real2Sim 路线**：3DGS + Hunyuan3D 的 Real2Sim 流水线可借鉴用于构建 DLO 操控的仿真环境
6. **服务器评测架构**：HTTP 端点 + 统一硬件的评测模式降低了参与门槛，保证了公平性

## 相关概念

- [[robotic-manipulation]]
- [[vision-language-model]]
- [[reinforcement-learning]]
- [[sim-to-real]]
- [[robot-learning]]
- [[deformable-linear-object]]
- [[bimanual-manipulation]]
- [[grasping]]

## 相关研究者

- [[sun-yu|Sun, Yu]]
