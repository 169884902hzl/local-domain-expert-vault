---
title: "3D generation for embodied AI and robotic simulation: A survey"
tags: [imitation, RL, sim-to-real, robot-learning, DLO]
created: "2026-04-30"
updated: "2026-04-30"
type: "literature"
status: "done"
summary: "首篇面向具身AI的3D生成综述，以\"数据生成器—仿真环境—Sim2Real桥梁\"三维角色组织文献，系统梳理122+方法，揭示从视觉逼真到仿真就绪的范式转移"
authors: "Ye, Tianwei; Mao, Yifan; Liao, Minwen; Liu, Jian; Guo, Chunchao et al."
year: "2026"
venue: "arXiv Preprint"
zotero_key: "TXX3S39B"
---
## 摘要

Embodied AI and robotic systems increasingly depend on scalable, diverse, and physically grounded 3D content for simulation-based training and real-world deployment. While 3D generative modeling has advanced rapidly, embodied applications impose requirements far beyond visual realism: generated objects must carry kinematic structure and material properties, scenes must support interaction and task execution, and the resulting content must bridge the gap between simulation and reality. This survey presents the first survey of 3D generation for embodied AI and organizes the literature around three roles that 3D generation plays in embodied systems. In \emph{Data Generator}, 3D generation produces simulation-ready objects and assets, including articulated, physically grounded, and deformable content for downstream interaction; in \emph{Simulation Environments}, it constructs interactive and task-oriented worlds, spanning structure-aware, controllable, and agentic scene generation; and in \emph{Sim2Real Bridge}, it supports digital twin reconstruction, data augmentation, and synthetic demonstrations for downstream robot learning and real-world transfer. We also show that the field is shifting from visual realism toward interaction readiness, and we identify the main bottlenecks, including limited physical annotations, the gap between geometric quality and physical validity, fragmented evaluation, and the persistent sim-to-real（仿真到真实迁移） divide, that must be addressed for 3D generation to become a dependable foundation for embodied intelligence. Our project page is at https://3dgen4robot.github.io.

## 中文简述

提出基于学习方法的绳索操控方法，具有仿真到真实迁移特点。

**研究方向**: 模仿学习、强化学习、仿真到真实迁移、机器人学习、可变形物体操控

## 关键贡献

1. **提出"仿真就绪"标准**：明确区分具身导向3D生成与传统3D生成，建立以几何有效性、物理参数化、运动学可执行性、仿真器兼容性为维度的评估框架
2. **首创三维角色分类法**：按"数据生成器"(Data Generator)、"仿真环境"(Simulation Environments)、"Sim2Real桥梁"(Sim2Real Bridge)三大角色组织文献，打通CV、CG、机器人、仿真系统等社区的研究脉络
3. **系统性方法梳理**：覆盖48个物体生成方法、35个场景生成方法、39个Sim2Real桥梁方法，含8个汇总表
4. **识别关键技术瓶颈**：物理标注稀缺、几何质量与物理有效性的差距、评估碎片化、Sim-to-Real鸿沟持续存在
## 结构化提取

- **Problem**: 具身AI缺乏可扩展、物理可靠、仿真兼容的3D资产生成方法，现有文献碎片化且缺乏统一视角
- **Method**: 综述，以"数据生成器—仿真环境—Sim2Real桥梁"三维角色组织122+方法，建立simulation readiness评估框架
- **Tasks**: 物体资产生成（铰接/物理接地/可变形）、场景生成（结构驱动/可控/智能体）、Sim2Real（数字孪生/数据增强/任务演示生成）
- **Sensors**: RGB-D、LiDAR/深度、视频序列、力/力矩传感器（部分方法）
- **Robot Setup**: 多平台（MuJoCo、Isaac Sim、Habitat、AI2-THOR、ManiSkill3、Genesis等），主要针对Franka Panda等单/双臂机器人
- **Metrics**: CD/EMD/F-Score/IoU（几何）、FID/CLIP Score（外观）、Stability Rate/Joint Accuracy/Penetration Volume（物理）、Grasp SR/Navigation SR/Sim-to-Real SR（任务）
- **Limitations**: 物理标注稀缺、可变形生成不成熟、评估碎片化、Sim-to-Real鸿沟、户外场景排除
- **Evidence Notes**: 全文162K字符逐块精读，覆盖全部8节、4个方法表(T2-T4)、3个数据集表(T5-T7)、1个评估指标表(T8)、1个仿真平台表(T1)，228篇参考文献
## 本地引用关系

-
## 证据元数据

- Fulltext Quality: fulltext (arXiv LaTeX-to-text, 162K chars, 8 main sections + tables)
- Evidence Coverage: high (全文已逐块精读，覆盖所有核心章节、4个方法汇总表、3个数据集表、评估指标表)
- Confidence: high
- Summary: 首篇面向具身AI的3D生成综述，以"数据生成器—仿真环境—Sim2Real桥梁"三维角色组织文献，系统梳理122+方法，揭示从视觉逼真到仿真就绪的范式转移


## Problem

具身AI和机器人系统对可扩展、多样化且物理上可靠的3D内容有强烈需求。传统3D生成关注视觉逼真度，但具身应用要求生成的资产具备运动学结构、材料属性、仿真器兼容性——即"仿真就绪"(simulation readiness)。现有文献分散在计算机视觉、图形学、机器人学和仿真系统等多个社区，缺乏统一的综述视角。


## Method

本文是综述论文，无单一方法。核心组织框架如下：

### 三大角色分类法
- **Data Generator (Sec 3)**：按物理复杂度递进组织
  - 铰接物体(Articulated Objects)：结构拓扑与参数化→语义推理与程序化合成→多状态与交互驱动
  - 物理接地物体(Physically-grounded Objects)：后验物理修正→仿真对齐训练→原生统一物理生成
  - 可变形物体(Deformable Objects)：布料/服装生成→弹塑性/软体生成
  - 端到端流水线(End-to-End Pipeline)：统一生成表示→专用Sim-Ready流水线→自动质量管控
- **Simulation Environments (Sec 4)**：按自主性递进
  - 结构驱动：程序化规则 vs 场景先验引导
  - 可控生成：指令/视觉/物理条件化
  - 智能体生成：模块化→自我反思→任务导向
- **Sim2Real Bridge (Sec 5)**：按数据流递进
  - 生成式数字孪生：自动场景重建→运动学重建→物理感知与视觉-动力学对齐
  - 生成式数据增强：视点/几何增强→动态/时序增强→物理感知一致性
  - 生成式任务与演示：演示缩放→世界模型→基础模型规模合成训练

### 仿真就绪定义
四个必要条件：(i)几何有效性 (ii)物理参数化 (iii)运动学可执行性 (iv)仿真器兼容性

### 仿真平台对比
覆盖MuJoCo、Isaac Sim、Habitat 3.0、AI2-THOR、OmniGibson、PyBullet、ManiSkill3、Genesis等8大平台


## Experiments

本文为综述，无单一实验。但汇总了丰富的方法对比和基准数据：

### 方法统计
- Table 2: 48个物体生成方法（26个铰接、12个物理、4个可变形、4个端到端流水线）
- Table 3: 35个场景生成方法（8个结构驱动、9个可控、18个智能体）
- Table 4: 39个Sim2Real方法（15个数字孪生、10个数据增强、14个任务/演示生成）

### 数据集汇总
- Table 5: 17个物体资产数据集（从ShapeNet到PhysX-Mobility的演进）
- Table 6: 11个场景数据集（从Matterport3D到MarketGen）
- Table 7: 12个机器人演示数据集（从Open X-Embodiment到MimicGen）

### 评估指标层级
- Level 1 几何与外观：CD、EMD、F-Score、IoU、FID、CLIP Score、WT Ratio
- Level 2 物理合理性与Sim-Readiness：稳定性率、关节精度、穿透体积、碰撞自由率、材料误差
- Level 3 具身任务性能：抓取SR、操控SR、导航SR、SPL、任务完成率、Sim-to-Real SR

### 代表性方法性能（来自各原始论文）
- PhysX-Anything：单图输入→URDF/MJCF输出，含质量/摩擦/惯性/材料
- SAGE：Agent生成10K场景/565K物体，语义+物理合理性评分
- RoboTwin 2.0：100K+轨迹/50任务，含域随机化
- GraspVLA：SynGrasp-1B十亿帧抓取数据集


## Limitations

1. **物理标注稀缺**：Objaverse等大规模数据集缺乏材料/质量/运动学参数；物理标注数据集(AKB-48, PhysXNet)规模远小
2. **可变形资产生成不成熟**：除服装外，通用软体/绳索/食品生成仍依赖逐实例优化，不可扩展
3. **场景生成效率-可控性矛盾**：学习方法高效但语义一致性差；Agent方法语义强但计算成本高
4. **评估碎片化**：几何指标忽略物理有效性；物理指标跨仿真器不一致；下游任务评估依赖策略和仿真器选择
5. **Sim-to-Real鸿沟持续**：外观、动力学、语义三个维度均有差距；生成式模型、物理引擎、策略学习三个社区各自优化，通过脆弱的转换流水线连接
6. **综述自身局限**：排除户外/自动驾驶场景生成；聚焦室内具身AI；部分方法因发表时间未纳入


## Key Takeaways

1. **对DLO操控的启示**：
   - 可变形物体生成(Sec 3.1.3)直接相关：PhysGaussian统一渲染与MPM仿真、DressCode的sewing pattern作为仿真原生中间表示的思路可扩展到DLO
   - 寻找DLO的"仿真原生中间表示"（类似服装的sewing pattern）是关键开放问题
   - PhysTwin的弹簧-质量模型用于可变形物数字孪生重建，可借鉴到绳索操控

2. **对Sim-to-Real的启示**：
   - 3DGS已成为Sim-to-Real桥梁的核心表示：SplatSim替代多边形网格、RoboSimGS混合表示、Real-is-Sim 60Hz同步数字孪生
   - R2S2R闭环（真实→仿真→真实）是主流趋势，EmbodiedGen等工具链正在自动化这一流程
   - 世界模型(GWM)用3DGS+DiT做动作条件状态预测，适合DLO操控的长时域规划

3. **对VLM-based控制的启示**：
   - VLA模型（RT-2, π₀, OpenVLA）的数据饥渴直接驱动了对可扩展3D生成的需求
   - LLM/VLM在铰接推理中发挥关键作用（Articulate-Anything, URDF-Anything+），语义先验是解决几何方法泛化不足的重要方向
   - GraspVLA的SynGrasp-1B表明仿真规模3D生成可作为训练开放词汇具身基础模型的先决基础设施

4. **方法论启示**：
   - 领域正从视觉逼真→仿真就绪转移，"simulation readiness"应成为DLO操控仿真环境的标准
   - 需要跨仿真器一致性测试（单一仿真器评估可能掩盖问题）
   - 可变形物体的"仿真原生中间表示"是一个值得探索的研究方向

## 相关概念

- [[imitation-learning]]
- [[reinforcement-learning]]
- [[sim-to-real]]
- [[robot-learning]]
- [[deformable-linear-object]]
- [[vision-language-model]]
- [[bimanual-manipulation]]
- [[grasping]]

## 相关研究者

- [[ye|Ye, Tianwei]]
