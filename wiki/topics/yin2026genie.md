---
title: "Genie sim 3.0 : A high-fidelity comprehensive simulation platform for humanoid robot"
tags: [manipulation, imitation, VLM, RL, sim-to-real]
created: "2026-05-08"
updated: "2026-05-08"
type: "literature"
status: "done"
summary: "Genie Sim 3.0 是 Agibot 开源的高保真仿真平台，集成 LLM 驱动场景生成、3DGS 环境重建、双模式数据采集和 LLM-VLM 自动化评测，提供 10000+ 小时合成数据和 100000+ 评测场景，实验证明合成数据可实现 zero-shot Sim-to-Real 迁移（R²=0.924）。"
authors: "Yin, Chenghao; Huang, Da; Yang, Di; Wang, Jichao; Zhao, Nanshu et al."
year: "2026"
venue: "arXiv Preprint"
zotero_key: "BCZSH53D"
---
## 摘要

The development of robust and generalizable robot learning models is critically contingent upon the availability of large-scale, diverse training data and reliable evaluation benchmarks. Collecting data in the physical world poses prohibitive costs and scalability challenges, and prevailing simulation benchmarks frequently suffer from fragmentation, narrow scope, or insufficient fidelity to enable effective sim-to-real（仿真到真实迁移） transfer. To address these challenges, we introduce Genie Sim 3.0, a unified simulation platform for robotic manipulation（机器人操控）. We present Genie Sim Generator, a large language model（大语言模型） (LLM)-powered tool that constructs high-fidelity scenes from natural language instructions. Its principal strength resides in rapid and multi-dimensional generalization, facilitating the synthesis of diverse environments to support scalable data collection and robust policy evaluation. We introduce the first benchmark that pioneers the application of LLM for automated evaluation. It leverages LLM to mass-generate evaluation scenarios and employs Vision-Language Model（视觉-语言模型） (VLM) to establish an automated assessment pipeline. We also release an open-source dataset comprising more than 10,000 hours of synthetic data across over 200 tasks. Through systematic experimentation, we validate the robust zero-shot（零样本） sim-to-real（仿真到真实迁移） transfer capability of our open-source dataset, demonstrating that synthetic data can server as an effective substitute for real-world data under controlled conditions for scalable policy training. For code and dataset details, please refer to: https://github.com/AgibotTech/genie_sim.

## 中文简述

提出基于视觉-语言的操控方法，具有仿真到真实迁移特点。

**研究方向**: 机器人操控、模仿学习、视觉-语言模型、强化学习、仿真到真实迁移

## 关键贡献

1. **Genie Sim Generator**: LLM 驱动的场景生成管线，支持自然语言输入、多轮对话迭代精修、实时生成高保真仿真场景
2. **多维度场景泛化**: 从单个场景快速泛化出大量多样化变体，参数化光照、背景、布局、姿态、轨迹、传感器噪声和机器人形态
3. **LLM-VLM 自动化评测基准**: 首个利用 LLM 自动生成评测场景、VLM 自动评分的基准，涵盖 100,000+ 场景，覆盖语义理解、空间推理和操作执行三个维度
4. **Sim-to-Real 迁移验证**: 系统实验证明合成数据可替代真实数据实现 zero-shot 迁移，sim-real 性能相关系数 R²=0.924
5. **开源**: 5140 个资产、10,000+ 小时数据集、100,000+ 评测场景、完整代码库
## 结构化提取

- Problem: 机器人 VLA 模型训练数据获取成本高、仿真基准碎片化且保真度不足、评测不可扩展
- Method: LLM 驱动场景生成 + 3DGS 环境重建 + 双模式数据采集（遥操作/自动化） + LLM-VLM 自动化评测
- Tasks: 200 个操控任务（原子技能 pick/place/pull/push/open/close + 认知理解 + 复杂长时任务），实验验证用 4 个代表性任务
- Sensors: 鱼眼相机（3DGS 重建采集）、仿真 RGB 相机（数据采集和评测）、PICO VR 头显（遥操作）
- Robot Setup: Agibot G1（单臂验证）、Agibot G2（数据集生成），多种末端执行器（omnipicker, omnihands, INSPIRE skillhands, zhixing gripper）
- Metrics: 任务成功率、Sim-Real 相关系数 R²、zero-shot 真实世界成功率
- Limitations: 评测任务范围小、无 DLO/可变形物体、同量级仿真数据仍不如真实数据、依赖专用采集设备
- Evidence Notes: 基于 arXiv HTML 全文；Table I 精确数值和 4 个任务名称未完整捕获（可能以图片嵌入）
## 本地引用关系

- [[yin2026genie]]
## 证据元数据

- Fulltext Quality: fulltext (arXiv HTML)
- Evidence Coverage: high (完整论文内容，包括方法、实验、附录；Table I 的具体数值和 4 个任务名称未在 HTML 中完整捕获)
- Confidence: high
- Summary: Genie Sim 3.0 是 Agibot 开源的高保真仿真平台，集成 LLM 驱动场景生成、3DGS 环境重建、双模式数据采集和 LLM-VLM 自动化评测，提供 10000+ 小时合成数据和 100000+ 评测场景，实验证明合成数据可实现 zero-shot Sim-to-Real 迁移（R²=0.924）。


## Problem

机器人学习模型（特别是 VLA 模型）的发展严重依赖大规模、多样化的训练数据和可靠评测基准。真实世界数据采集成本高昂、可扩展性差；现有仿真基准存在碎片化、范围狭窄、保真度不足等问题，无法有效支撑 Sim-to-Real 迁移。三大瓶颈：(1) 高保真仿真环境构建需要大量人工；(2) 自动化生成缺乏精细控制和可复现性；(3) 现有评测指标单一、人工评测不可扩展。


## Method

### 1. 场景生成（Genie Sim Generator）
四阶段管线：
- **Intention Interpreter**: CoT-enabled LLM 将自然语言解析为结构化 JSON schema（语义类别、几何约束、空间关系）
- **Assets Index**: RAG 检索模块，5140 个物体通过 QWEN text-embedding-v4 编码为 2048 维向量存入 ChromaDB，余弦相似度检索，200ms 完成
- **DSL Code Generator**: 基于 Scene Language 语法，结合 LLM 上下文生成精确场景规格，支持迭代编辑
- **Results Assembler**: 实例化 DSL 程序，生成层级化 Scene Graph（节点=物体属性，边=空间关系），输出 OpenUSD/Isaac Sim 文件

### 2. 环境重建
基于 3D Gaussian Splatting (3DGS) 的照片级真实感渲染：
- 数据采集：MetaCam 手持 3D 激光扫描仪（鱼眼图像 + 位姿 + 点云）
- 相机位姿优化：SuperPoint + LightGLue 替换 COLMAP-PCD 的特征提取，提升弱纹理特征提取能力
- 利用 LiDAR SLAM 先验位姿进行三角化 + BA 优化
- 使用 gsplat 框架训练 3DGS
- Difix3D+ 扩散模型外推视角弥补覆盖不足
- PGSR 进行表面重建获取高精度 mesh

### 3. 数据采集（双模式）
- **遥操作**: PICO VR 头显控制仿真机器人，记录关节状态、视觉观测和物体位姿
- **自动化**: cuRobo GPU 加速运动规划器 + LLM 资产检索 + GraspNet 抓取标注
  - 多候选航点生成，逐个尝试 + 失败回滚
  - 保留完整环境（不移除无关物体），通过 mesh 简化平衡效率

### 4. 闭环评测
仿真器与推理服务通过 HTTP 解耦通信：
- 支持多种机器人（Genie G1, G2）和末端执行器
- 支持 本地/分布式 推理
- LLM + VLM 自动评分


## Experiments

### 实验设置
- 基座模型: π₀.₅
- 机器人: Agibot G1
- 32 组实验（4 任务 × 4 训练配置 × 2 评测环境）
- 训练配置:
  1. 200 episodes 真实数据
  2. 500 episodes 真实数据
  3. 500 episodes 仿真数据
  4. 1500 episodes 仿真数据
- 评测：真实环境 50 次试验，仿真环境 250 次试验

### 主要结果
- **合成数据有效性**: 1500 episodes 仿真数据在所有 4 个任务上取得最高 zero-shot 真实世界成功率
- **同等数量对比**: 500 episodes 时真实数据优于仿真数据（物理保真度差异：摩擦、接触动力学、碰撞）
- **Sim-Real 一致性**: R²=0.924，最佳拟合斜率 ≈1.045
- **数据规模律**: 成功率随训练数据量增加而显著提升，符合 scaling law
- **任务复杂度**: 复杂度越高，相同数据量下成功率越低

### 数据集统计
- 200 个代表性任务
- 10,000+ 小时仿真交互数据
- 多维度 domain randomization：任务布局、初始姿态、光照、场景配置、相机噪声、语义指令措辞
- 两个机器人平台: Agibot G1 和 G2

### 缺失证据
- Table I 中的具体任务名称和精确成功率数值未在 HTML 中完整捕获（可能以图片形式嵌入）
- 4 个任务的具体名称未明确列出（HTML 中编号列表为空）


## Limitations

1. **评测范围有限**: Sim-to-Real 验证仅用 4 个任务，覆盖面不足
2. **接触动力学差距**: 仿真中摩擦和接触动力学近似导致系统性差异
3. **同等量级劣势**: 同等数据量下仿真数据仍不如真实数据
4. **机器人类型局限**: 仅验证 Agibot G1 机型
5. **任务选择偏差**: 实验刻意避开过高/过低成功率的任务，不代表全部场景
6. **无 DLO/可变形物体**: 不涵盖可变形物体操控，仅刚性物体
7. **3DGS 重建依赖**: 环境重建需要专用激光扫描设备和密集视角采集


## Key Takeaways

1. **对 DLO 操控的启示**: Genie Sim 的场景生成管线和自动化评测框架可扩展到 DLO 操控场景，但目前资产库和任务集不包含可变形物体
2. **合成数据的实用价值**: 1500 episodes 仿真数据即可超越 500 episodes 真实数据，说明大规模 domain randomization 可弥合 sim-to-real gap，这对 DLO 操控的数据采集策略有指导意义
3. **LLM-VLM 评测范式**: 用 LLM 自动生成评测指令 + VLM 自动评分的闭环评测方案，可借鉴用于 DLO 操控策略评估
4. **RAG 资产检索**: 向量化资产库 + 语义检索的方式值得在 DLO 场景资产构建中借鉴
5. **Sim-Real 相关性**: R²=0.924 表明仿真评测可有效预测真实世界性能，支持先仿真后部署的开发流程

## 相关概念

- [[robotic-manipulation]]
- [[imitation-learning]]
- [[vision-language-model]]
- [[reinforcement-learning]]
- [[sim-to-real]]
- [[diffusion-model]]
- [[deformable-linear-object]]
- [[grasping]]

## 相关研究者

- [[yin-chenghao|Yin, Chenghao]]
