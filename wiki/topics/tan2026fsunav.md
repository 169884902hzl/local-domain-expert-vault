---
title: "FSUNav: A cerebrum-cerebellum architecture for fast, safe, and universal zero-shot goal-oriented navigation"
tags: [imitation, VLM, RL, robot-learning, planning]
created: "2026-05-15"
updated: "2026-05-15"
type: "literature"
status: "done"
summary: "提出 Cerebrum-Cerebellum 双层架构实现零样本目标导航：Cerebellum 基于 DRL 的维度可配置局部规划器实现跨平台避障，Cerebrum 以 VLM 为核心构建语义-空间-规则三层推理实现开放词汇目标检测与验证，在 MP3D/HM3D 上达到 SOTA。"
authors: "Tan, Mingao; Li, Yiyang; Wang, Shanze; Zhang, Xinming; Zhang, Wei"
year: "2026"
venue: "arXiv Preprint"
zotero_key: "4U8DJUD9"
---
## 摘要

Current vision-language navigation methods face substantial bottlenecks regarding heterogeneous robot compatibility, real-time performance, and navigation safety. Furthermore, they struggle to support open-vocabulary semantic generalization and multimodal（多模态） task inputs. To address these challenges, this paper proposes FSUNav: a Cerebrum-Cerebellum architecture for fast, safe, and universal zero-shot（零样本） goal-oriented navigation, which innovatively integrates vision-language models (VLMs) with the proposed architecture. The cerebellum module, a high-frequency end-to-end（端到端） module, develops a universal local planner based on deep reinforcement learning（强化学习）, enabling unified navigation across heterogeneous platforms (e.g., humanoid, quadruped, wheeled robots) to improve navigation efficiency while significantly reducing collision risk. The cerebrum module constructs a three-layer reasoning model and leverages VLMs to build an end-to-end（端到端） detection and verification mechanism, enabling zero-shot（零样本） open-vocabulary goal navigation without predefined IDs and improving task success rates in both simulation and real-world environments. Additionally, the framework supports multimodal（多模态） inputs (e.g., text, target descriptions, and images), further enhancing generalization, real-time performance, safety, and robustness. Experimental results on MP3D, HM3D, and OVON benchmarks demonstrate that FSUNav achieves state-of-the-art（现有最优方法） performance on object, instance image, and task navigation, significantly outperforming existing methods. Real-world deployments on diverse robotic platforms further validate its robustness and practical applicability.

## 中文简述

提出基于强化学习的导航方法，具有零样本泛化特点。

**研究方向**: 模仿学习、视觉-语言模型、强化学习、机器人学习、运动规划

## 关键贡献

1. **Cerebellum 模块（低层执行与控制）**：基于 DRL 的平台解耦局部规划器，通过维度可配置输入表示和课程学习策略，实现异构机器人（人形、四足、轮式）的零样本跨平台部署，支持快速安全的局部导航控制
2. **Cerebrum 模块（高层理解与决策）**：以 VLM 为核心构建语义层（Semantic）、空间层（Spatial）、规则层（Rule）三层推理架构，统一支持目标导航（ON）、实例图像导航（IIN）、文本导航（TN）三种任务，无需任务特定训练
3. **多层次 VLM 利用范式**：VLM 不仅用于目标检测，还作为语义推理引擎参与目标解释、探索引导、验证和场景理解，实现开放词汇零样本目标定位
4. **系统性验证**：在 MP3D、HM3D 标准基准和真实机器人（Unitree Go2 EDU）上全面验证，在所有任务上达到 SOTA
## 结构化提取

- Problem: 视觉-语言导航中异构平台兼容性差、实时性不足、安全性机制缺失、开放词汇语义泛化和多模态交互受限
- Method: Cerebrum-Cerebellum 双层架构；Cerebellum = PointNet + SAC 的 DRL 局部规划器（维度可配置 + 课程学习）；Cerebrum = VLM（Qwen3-VL-32B-Instruct）驱动的语义-空间-规则三层推理；真机使用 VGGT 单目深度估计
- Tasks: Object-Goal Navigation (ON)、Instance-Image Navigation (IIN)、Text-Goal Navigation (TN)、Open-Vocabulary Navigation (OV)
- Sensors: RGB-D（仿真，640×480）、Intel RealSense D455 RGB + Livox MID-360 LiDAR（真机）、VGGT 单目深度估计
- Robot Setup: 仿真使用 Habitat Simulator 多种虚拟平台；真机使用 Unitree Go2 EDU 四足机器人（最大速度 0.6 m/s）；声称支持人形（Unitree G1）和轮式机器人（实验未展示）
- Metrics: SR（成功率，目标 1m 内停止）、SPL（路径长度加权成功率）
- Limitations: 无消融实验、真机实验仅一种平台一种任务、VLM 推理需要高端 GPU、单目深度估计精度有限、OVON 基准结果缺失、VLM 结构化输出可靠性未验证
- Evidence Notes:

  - 仿真实验仅评估 Cerebrum 模块，Cerebellum 使用模拟器内置规划器 → 无法直接验证完整系统在仿真中的端到端性能
  - 真机实验展示了完整架构但仅一个场景一个目标 → 跨平台声称未充分验证
  - Table I 的精确数值从正文文本重建，非直接读取表格 → 存在四舍五入误差可能
  - 论文为 arXiv 预印本（2026-04-03），可能仍有更新
## 本地引用关系

-
## 证据元数据

- Fulltext Quality: fulltext（arXiv HTML 全文，表格数据从正文文本重建）
- Evidence Coverage: high（方法、实验、真机部署均有详细描述；缺少消融实验数据）
- Confidence: high
- Summary: 提出 Cerebrum-Cerebellum 双层架构实现零样本目标导航：Cerebellum 基于 DRL 的维度可配置局部规划器实现跨平台避障，Cerebrum 以 VLM 为核心构建语义-空间-规则三层推理实现开放词汇目标检测与验证，在 MP3D/HM3D 上达到 SOTA。


## Problem

现有视觉-语言导航（VLN）方法面临四个核心瓶颈：

1. **异构平台兼容性差**：大多数方法针对特定平台设计（如轮式机器人），难以泛化到人形、四足等异构平台，跨平台使用需要大量重训练和适配
2. **实时性不足**：依赖计算密集型大模型，推理延迟高，难以满足动态环境中的低延迟导航需求
3. **安全性机制缺失**：现有研究主要关注路径规划和成功率优化，对碰撞避免和动态障碍物避让关注不足
4. **语义泛化和多模态交互受限**：依赖预定义目标类别或固定词汇表，无法理解开放词汇指令；任务输入通常限于单一模态（如文本）


## Method

### 整体架构：Cerebrum-Cerebellum 双层架构

- **Cerebellum（小脑）**：高频端到端模块，负责实时无图局部导航和避障，输出速度命令 $\mathbf{u}_t = (v_t, \omega_t)$
- **Cerebrum（大脑）**：基于 VLM 的三层推理模块，负责高层语义理解和目标验证，输出二维目标坐标 $\mathbf{g} \in \mathbb{R}^2$
- 闭环运行：Cerebrum 生成高层意图 → Cerebellum 执行精确运动和避障

### Cerebellum 模块细节

1. **输入表示**（维度可配置）：
   - $\mathbf{o}_t = \{\mathbf{xr}_t, \mathbf{g}_t, \mathbf{v}_t, \mathbf{L}_{dyn}\}$
   - $\mathbf{xr}_t$：统一几何表示（点集），整合异构传感器（深度相机、LiDAR）
   - $\mathbf{g}_t \in \mathbb{R}^2$：相对目标位置（机器人本地坐标系）
   - $\mathbf{v}_t = (v_t, \omega_t)$：当前速度
   - $\mathbf{L}_{dyn}$：速度限制 $(v_{max}, \omega_{max})$ 和加速度限制

2. **维度感知编码**：
   - 机器人建模为长方体 $\mathbf{body} = [L_{front}, L_{rear}, W]$
   - 每个障碍物点编码维度感知特征：$\mathbf{p}_{t,i} = (\sin\phi, \cos\phi, 1/(d-\beta), L_{front}, L_{rear}, W/2)$
   - 直接将物理尺寸嵌入每个点，使策略网络能基于自身几何约束评估障碍物紧迫性

3. **网络结构**：
   - PointNet 编码器：共享 MLP + max-pooling 提取全局几何特征
   - 拼接目标和状态信息后通过 SAC（Soft Actor-Critic）网络生成动作

4. **课程学习训练**：
   - 按周长分组机器人
   - 从开放地图到逐渐缩小可导航区域的渐进式难度
   - 每阶段成功率超 90% 后晋级下一阶段

### Cerebrum 模块细节

**语义层（Semantic Layer）**：
- VLM 解析多模态目标（物体类别、参考图像、自然语言指令）为结构化目标配置
- $\mathcal{P}_{target} = \langle c_{core}, \mathcal{A}_{attr}, \mathcal{R}_{ctx} \rangle$（核心类别 + 视觉属性 + 空间/语义关系）
- 开放词汇视觉定位：VLM 输出归一化 bbox（JSON 格式）→ 像素坐标 → 深度投影到 3D 空间

**空间层（Spatial Layer）**：
- BEV 鸟瞰图（自由/占据/未知三态）
- VLM 驱动的语义探索：目标不可见时，VLM 选择安全可达且语义上可能接近目标的点作为中间子目标
- Frontier 探索：测地距离场 + 信息增益评估前沿区域
- 混合探索策略：语义路标 + 几何前沿平衡效率与语义导向

**规则层（Rule Layer）**：
- 探索/确认双模式切换
- 两阶段 VLM 验证：全局场景确认 → 局部实例匹配
- 自适应冷却机制防止频繁 VLM 查询
- VLM 构建语义场景图（推断物体间空间关系）

### 关键技术选择

- **VLM**：Qwen3-VL-32B-Instruct（通过 Ollama 部署）
- **深度估计**（真机）：VGGT 模型从 RGB 估计深度图（不依赖专用深度传感器）
- **硬件**：2× NVIDIA RTX 4090


## Experiments

### 仿真实验（Habitat Simulator）

**数据集**：MP3D、HM3D
**任务**：ON（目标导航）、IIN（实例图像导航）、TN（文本导航）、OV（开放词汇导航）
**指标**：SR（成功率）、SPL（路径长度加权成功率）
**输入**：RGB-D 640×480，79° HFOV

**主要结果（从正文文本重建）**：

| 任务 | 数据集 | FSUNav SR | FSUNav SPL | 最强竞争者 SR | 最强竞争者 SPL |
|------|--------|-----------|------------|---------------|----------------|
| ON | MP3D | 48.75% | 26.93% | CogNav 46.6% / 16.1% | - |
| ON | HM3D | 76.2% | 40.49% | PEANUT+LOG 64.3% / 34.2%（监督式） | - |
| IIN | HM3D | 72.6% | 34.88% | IEVE 70.2% / 25.2%（监督式） | - |
| TN | HM3D | 39.8% | 21.58% | UniGoal 20.2% / 11.4% | - |
| OV | HM3D | 56.87% | 32.59% | MTU3D 40.8% / 12.1% | - |

关键发现：
- FSUNav 是唯一同时实现 training-free 和 universal 的方法
- TN 任务上几乎翻倍了之前最优方法 UniGoal 的性能
- OV 任务上大幅超越监督式方法 MTU3D 和 VISOR
- 注意：仿真实验仅评估 Cerebrum 模块，局部规划器使用模拟器内置模块

### 真机实验

- **平台**：Unitree Go2 EDU 四足机器人
- **最大运动速度**：0.6 m/s
- **感知**：Intel RealSense D455 RGB（640×480）+ Livox MID-360 LiDAR
- **深度**：VGGT 模型从 RGB 估计（不使用深度传感器的深度数据）
- **通信**：WLAN 无线网络连接远程工作站
- **任务**：开放词汇目标导航（如"找到伞"）
- **结果**：成功完成导航任务，展示实时动态避障能力
- **局限**：仅展示了一个任务类型（物体目标导航），人形机器人和轮式机器人的实验"将在后续版本中更新"

### 消融实验

论文未报告消融实验。这是一个重要缺失。


## Limitations

1. **消融实验缺失**：论文未提供消融研究，无法量化各组件（语义路标、两阶段验证、课程学习等）的独立贡献
2. **真机实验有限**：仅在四足机器人上展示了一种任务类型；人形和轮式平台实验尚未完成，无法验证跨平台声称
3. **VLM 推理延迟**：使用 Qwen3-VL-32B-Instruct（32B 参数），需要 2×RTX 4090，实时性受 VLM 推理速度限制
4. **深度估计可靠性**：真机使用 VGGT 从 RGB 估计深度，精度受限于单目估计，可能影响 3D 投影和目标定位
5. **OVON 基准缺失**：摘要提到 OVON 基准但正文中未给出详细结果
6. **场景复杂度**：真机实验场景较简单（"找到伞"），未展示复杂动态环境（如人群、狭窄通道）中的表现
7. **VLM 输出格式依赖**：依赖 VLM 输出结构化 JSON 格式的 bbox，实际部署中可能出现格式错误或幻觉


## Key Takeaways

1. **Cerebrum-Cerebellum 分层架构**是将 VLM 高层语义推理与 DRL 低层运动控制解耦的有效范式，这种分层思想可迁移到 DLO 操控：VLM 理解 DLO 状态和目标，DRL 执行精细操控
2. **维度可配置表示**是一种优雅的跨平台泛化方案：将机器人物理尺寸直接编码到观测点特征中，使同一策略无需重训练即可适配不同形态
3. **VLM 作为通用语义引擎**的多层次利用（检测+探索引导+验证+场景图）值得借鉴，不局限于单一感知角色
4. **Training-free 方法在导航任务上已可超越监督式方法**，说明 VLM 的泛化能力在具身智能任务中具有巨大潜力
5. **语义路标探索**（VLM 选择语义上合理的中间子目标）是比纯几何前沿探索更高效的策略

## 相关概念

- [[imitation-learning]]
- [[vision-language-model]]
- [[reinforcement-learning]]
- [[robot-learning]]
- [[planning]]
- [[sim-to-real]]
- [[deformable-linear-object]]

## 相关研究者

- [[tan|Tan, Mingao]]
