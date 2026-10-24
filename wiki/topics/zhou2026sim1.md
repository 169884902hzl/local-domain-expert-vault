---
title: "SIM1: Physics-Aligned Simulator as Zero-Shot Data Scaler in Deformable Worlds"
tags: [manipulation, imitation, diffusion, sim-to-real, robot-learning]
created: "2026-05-07"
updated: "2026-05-07"
type: "literature"
status: "done"
summary: "提出 SIM1，首个面向可变形物体操控的物理对齐 R2S2R 数据引擎，通过高精度场景数字化、变形稳定化求解器（AVBD）和扩散轨迹生成实现零样本 Sim-to-Real 迁移，在 T 恤折叠任务上达到 90% 成功率和 15:1 合成/真实数据等效比。"
authors: "Zhou, Yunsong; Liu, Hangxu; Jiang, Xuekun; Shen, Xing; Zhou, Yuanzhen et al."
year: "2026"
venue: "arXiv Preprint"
zotero_key: "QVVJKU68"
---
## 摘要

Robotic manipulation（机器人操控） with deformable objects represents a data-intensive regime in embodied learning, where shape, contact, and topology co-evolve in ways that far exceed the variability of rigids. Although simulation promises relief from the cost of real-world data acquisition, prevailing sim-to-real（仿真到真实迁移） pipelines remain rooted in rigid-body abstractions, producing mismatched geometry, fragile soft dynamics, and motion primitives poorly suited for cloth interaction. We posit that simulation fails not for being synthetic, but for being ungrounded. To address this, we introduce SIM1, a physics-aligned real-to-sim-to-real（仿真到真实迁移） data engine that grounds simulation in the physical world. Given limited demonstrations, the system digitizes scenes into metric-consistent twins, calibrates deformable dynamics through elastic modeling, and expands behaviors via diffusion（扩散）-based trajectory generation with quality filtering. This pipeline transforms sparse observations into scaled synthetic supervision with near-demonstration（示范数据） fidelity. Experiments show that policies trained on purely synthetic data achieve parity with real-data baselines at a 1:15 equivalence ratio, while delivering 90% zero-shot（零样本） success and 50% generalization gains in real-world deployment. These results validate physics-aligned simulation as scalable supervision for deformable manipulation（操控） and a practical pathway for data-efficient（数据高效） policy learning.

## 中文简述

提出基于扩散模型的操控方法，具有仿真到真实迁移特点。

**研究方向**: 机器人操控、模仿学习、扩散模型、仿真到真实迁移、机器人学习

## 关键贡献

1. **SIM1 系统**：首个面向可变形物体操控的物理对齐 R2S2R（Real-to-Sim-to-Real）数据引擎，使合成数据可直接用于真实机器人部署
2. **三阶段对齐管线**：
   - 度量精确的场景数字化（SIM1-Scene）：亚毫米级精度 3D 扫描重建
   - 变形稳定化物理仿真（SIM1-Sim）：基于 AVBD 的稳定化求解器 + 参数标定
   - 扩散轨迹生成（SIM1-DataGen）：结构化轨迹分解 + 条件扩散强制 + 有效性过滤
3. **实验验证**：在 π0.5 和 π0 上分别实现 90% 和 76% 零样本成功率，泛化增益 +50% 和 +56%，15 个合成样本等效 1 个真实示教
## 结构化提取

- **Problem**: 可变形物体操控的数据密集性问题；现有 Sim-to-Real 管线基于刚体抽象，几何/动力学/运动三个层面均与真实世界不对齐
- **Method**: SIM1 — 物理对齐 R2S2R 三阶段管线（SIM1-Scene 场景数字化 + SIM1-Sim AVBD 稳定化仿真 + SIM1-DataGen 扩散轨迹生成）
- **Tasks**: T 恤折叠（主要 benchmark）；论文还展示了折叠、翻转、展平等多种衣物操控任务的仿真数据生成能力
- **Sensors**: RGB 头部相机（用于策略训练和视频判别器）
- **Robot Setup**: ARX ACONE 双臂平台（真实），ARX X5 双臂（仿真遥操作），平行爪夹持器
- **Metrics**: 成功率（30 次试验/配置，到达目标折叠状态）；通过率（生成数据有效性过滤）
- **Limitations**: 材质标定需专家参与、单任务验证、参数标定追求行为一致性而非物理真实性
- **Evidence Notes**:

  - 零样本 S2R 迁移：π0.5 90%, π0 76%（实验 4.2）
  - 泛化增益：空间 +50%, 纹理 +13%, 光照 +47%, 未见衣物 70% vs 20%（实验 4.2）
  - 数据等效比：15:1 域内, 5:1 域外（实验 4.2 scaling analysis）
  - 消融：MimicGen 0% → +轨迹分解 0% → +扩散 47% → +AVBD 67%/76%（Table 1）
  - 从头训练：真实 0% vs 合成 76%（实验 4.2 pretraining confound）
## 本地引用关系

-
## 证据元数据

- Fulltext Quality: fulltext (arXiv HTML version, 包含正文全部内容、参考文献、实验表格和图表描述；附录 B/C 仅引用未展开)
- Evidence Coverage: high (Introduction, Related Work, Method, Experiments, Ablation, Conclusion, References 均已覆盖)
- Confidence: high
- Summary: 提出 SIM1，首个面向可变形物体操控的物理对齐 R2S2R 数据引擎，通过高精度场景数字化、变形稳定化求解器（AVBD）和扩散轨迹生成实现零样本 Sim-to-Real 迁移，在 T 恤折叠任务上达到 90% 成功率和 15:1 合成/真实数据等效比。


## Problem

可变形物体（尤其是衣物）的机器人操控是具身学习中数据需求最大的场景之一。现有 Sim-to-Real 管线基于刚体抽象，存在三个核心缺陷：
1. **几何不对齐**：仿真场景与真实环境缺乏度量一致性，形状偏差在软体变形中被放大
2. **动力学不稳定**：物理引擎针对刚体优化，布料等软体交互产生过度拉伸、接触不稳定
3. **运动基元不适用**：基于抓取点和简单 pick-and-place 的轨迹策略无法处理衣物交互

核心假设：仿真失败不是因为"仿真是假的"，而是因为"仿真没有与真实世界对齐"（ungrounded）。


## Method

### 整体框架（R2S2R 范式）

SIM1 采用三阶段对齐，解决几何、动力学和运动的不对称性：

#### 3.1 SIM1-Scene: 场景数字化
- **可变形资产**：使用 EinScan Rigil Pro 专业 3D 扫描仪获取衣物高保真 mesh + 纹理；衣物穿在人偶上扫描，手动分割去除人偶点云；Poisson 重建 + 网格后处理（补洞、平滑、重网格化）→ 带纹理 OBJ 资产，亚毫米精度
- **机器人资产**：ARX ACONE 双臂平台，URDF 从 CAD 模型生成直接导入，验证尺寸精度和根变换对齐
- **环境资产**：公开 3D 模型库或手工创建，按真实测量缩放

#### 3.2 SIM1-Sim: 变形稳定化物理仿真
- **Augmented VBD (AVBD) 求解器**：扩展 Newton-VBD，引入显式应变约束
  - 应变约束：边长不超过 $(1+\xi)l_0$，激活时注入惩罚能量 $E_{strain}$
  - 参数更新：惩罚刚度 $k^{(n+1)} = \min(k_{max}, k^{(n)} + \beta|C(\mathbf{e})|)$
  - 直觉：虚拟弹簧仅在过度拉伸时激活，加速收敛到物理一致状态
- **参数标定基础设施**：
  - 参数集 $\Theta = \{\rho, E, \nu, \mu, \eta, \zeta\}$（密度、杨氏模量、泊松比、摩擦、恢复系数、松弛）
  - 双向同步仿真：专家操控真实机器人 → 关节状态流式传输到仿真器 → 视觉比较 → 迭代调整参数
  - 不恢复真实物理参数，而是建立行为一致性

#### 3.3 SIM1-DataGen: 结构化可变形操控合成
- **轨迹分解**：将示教轨迹分割为交互段（保持抓取配置）和运动段（用于生成）；交互段从池中随机选取并保留顺序多样性
- **扩散运动生成**：条件扩散强制（Conditional Diffusion Forcing）
  - 给定边界姿态 $(\mathbf{p}_s, \mathbf{p}_e)$ 和历史 $\mathbf{h}$，预测中间运动
  - Transformer 序列模型从部分损坏 token 重建轨迹
  - 损失：$\min_\theta \mathbb{E}\|\epsilon - \epsilon_\theta(g(\mathbf{x}^0, \mathbf{k}); \mathbf{h}, \mathbf{p}_s, \mathbf{p}_e, \mathbf{k})\|_2^2$
- **有效性检查**：
  1. 轻量状态过滤：基于衣物粒子统计的阈值规则（vibe coding 合成）
  2. 视频判别器：ResNet-18 + Transformer 编码器，输出有效性分数 $s = D(\mathbf{V})$，阈值 $\tau_{disc}$ 过滤
- **视觉随机化**：Blender 渲染，随机化材质、光照、相机参数；输出 LeRobot 格式


## Experiments

### 设置
- **机器人**：ARX ACONE 双臂 + 平行爪夹持器
- **任务**：T 恤折叠（代表性 benchmark，20+ 秒长时序操控）
- **数据**：1000 条真实轨迹（示教教学），200 条仿真源示教，10k 合成生成数据
- **模型**：π0.5（后训练 + 从头训练）、π0（后训练）
- **评估**：每配置 30 次试验；成功 = 衣物到达目标折叠状态且无掉落/展开
- **域内/域外**：域内用相同布局/衣物/桌面/光照/相机；域外引入空间偏移（≤8cm, ±15°）、纹理替换、光照随机化、相机仰角扰动（±5°）

### 主要结果

#### Q1: 仿真训练 vs 真实数据训练
| 设置 | 模型 | 真实数据 | 仿真遥操作 | 仿真生成 |
|------|------|---------|----------|---------|
| 域内 | π0.5 后训练 | **97%** | 87% | 达到同等水平 |
| 域内（从头） | π0.5 | 0% | - | **76%** |
| 零样本 | π0.5 | - | - | **90%** |
| 零样本 | π0 | - | - | **76%** |

关键发现：真实数据从头训练完全失败（0%），合成数据从头训练达 76%，证明性能来源于生成数据而非预训练先验。

#### Q2: 域外泛化
仿真多样性带来显著泛化提升：
- 空间偏移：+50% (π0.5)
- 纹理变化：+13%
- 光照扰动：+47%
- 未见 polo 衫：真实数据 20%，合成数据 70%

#### Q3: 数据缩放效率
- 域内：1 个真实示教 ≈ 15 个合成样本（饱和点）
- 域外（纹理泛化）：1 个真实 ≈ 5 个合成样本
- π0.5 在固定预算下优于 π0（更丰富的预训练或更强的状态表征）

### 消融实验
| 模块 | 通过率 | 域内成功率 | 域外平均 |
|------|--------|----------|---------|
| MimicGen（刚体基线） | **0%** | 0% | 0% |
| + 轨迹分解 | >0% | 0% | 0% |
| + 扩散生成 | - | **47%** | 弱 |
| + AVBD 求解器 | - | **67%** | **76%** |

- 场景重建：AR Code 方法产生厘米级 mesh 和伪影；SIM1 达亚毫米级精度
- 通用求解器（FEM, VBD）：在刚-软交互中产生过度拉伸、粒子间隙、局部延迟


## Limitations

1. **材质标定需专家参与**：每个资产需要专家引导的参数调优，限制了在任意布料类型上的完全自动化
2. **单任务 benchmark 验证**：真实世界实验主要在 T 恤折叠任务上验证（虽然论文展示了框架在更多任务上的能力）
3. **仿真-真实参数不等价**：标定追求行为一致性而非恢复真实物理参数，可能在新场景泛化时受限


## Key Takeaways

1. **物理对齐是仿真数据有效的先决条件**：仿真失败不是因为"假"，而是因为"没有对齐"。几何精度、动力学稳定、运动质量三者缺一不可
2. **AVBD 应变约束机制**：在 VBD 基础上引入显式应变约束，通过惩罚能量项抑制过度拉伸，是刚-软交互稳定化的关键技术
3. **扩散轨迹生成优于刚体切片**：MimicGen 风格的轨迹切片在可变形任务上完全失败（0%通过率），扩散模型能学习类人运动过渡
4. **合成数据缩放效率**：15:1 的等效比表明高质量仿真数据可替代真实数据采集，且在域外泛化上优势更大
5. **对 DLO 操控的启示**：虽然本文聚焦衣物（布料），但 R2S2R 范式、变形稳定化求解器和结构化轨迹合成的思路可直接迁移到 DLO 操控场景
6. **双臂协同验证**：ARX ACONE 双臂平台的成功部署验证了该方法在双手协调操控中的可行性

## 相关概念

- [[robotic-manipulation]]
- [[imitation-learning]]
- [[diffusion-model]]
- [[sim-to-real]]
- [[robot-learning]]
- [[deformable-linear-object]]
- [[bimanual-manipulation]]
- [[grasping]]

## 相关研究者

- [[zhou-yunsong|Zhou, Yunsong]]
- [[shen|Shen, Xing]]
