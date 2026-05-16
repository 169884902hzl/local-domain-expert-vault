---
title: "E3VS-bench: A benchmark for viewpoint-dependent active perception in 3D gaussian splatting scenes"
tags: [imitation, VLM, robot-learning, planning]
created: "2026-04-30"
updated: "2026-04-30"
type: "literature"
status: "done"
summary: "基于 3D Gaussian Splatting 构建具身 3D 视觉搜索基准 E3VS-Bench，要求智能体在 5-DoF 视角空间中主动探索以获取视点依赖证据来回答问题，揭示当前 VLM 与人类在主动感知上的巨大差距"
authors: "Sakamoto, Koya; Miyanishi, Taiki; Azuma, Daichi; Kurita, Shuhei; Morikuni, Shu et al."
year: "2026"
venue: "arXiv Preprint"
zotero_key: "D3UBFHRS"
---
## 摘要

Visual search in 3D environments requires embodied agents to actively explore their surroundings and acquire task-relevant evidence. However, existing visual search and embodied AI benchmarks, including EQA, typically rely on static observations or constrained egocentric motion, and thus do not explicitly evaluate fine-grained viewpoint-dependent phenomena that arise under unrestricted 5-DoF viewpoint control in real-world 3D environments, such as visibility changes caused by vertical viewpoint shifts, revealing contents inside containers, and disambiguating object attributes that are only observable from specific angles. To address this limitation, we introduce {E3VS-Bench}, a benchmark for embodied 3D visual search where agents must control their viewpoints in 5-DoF to gather viewpoint-dependent evidence for question answering. E3VS-Bench consists of 99 high-fidelity 3D scenes reconstructed using 3D Gaussian Splatting and 2,014 question-driven episodes. 3D Gaussian Splatting enables photorealistic free-viewpoint rendering that preserves fine-grained visual details (e.g., small text and subtle attributes) often degraded in mesh-based simulators, thereby allowing the construction of questions that cannot be answered from a single view and instead require active inspection across viewpoints in 5-DoF. We evaluate multiple state-of-the-art（现有最优方法） VLMs and compare their performance with humans. Despite strong 2D reasoning ability, all models exhibit a substantial gap from humans, highlighting limitations in active perception and coherent viewpoint planning specifically under full 5-DoF viewpoint changes.

## 中文简述

提出基于模仿学习的操控方法。

**研究方向**: 模仿学习、视觉-语言模型、机器人学习、运动规划

## 关键贡献

1. **定义 E3VS 任务**：提出 Embodied 3D Visual Search 设定，智能体必须通过 5-DoF 视角控制获取任务相关的视觉证据
2. **构建 E3VS-Bench 基准**：99 个高保真 3DGS 场景 + 2,014 个人工标注的问题驱动 episode，覆盖 6 种推理类型
3. **全面评估 VLM**：测试多种 SOTA VLM（Gemini 2.5/3.0、GPT-5.1、Qwen3-VL、InternVL3.5、Step3-VL），发现所有模型与人类存在显著差距
## 结构化提取

- Problem: 现有具身 AI 基准不支持评估 5-DoF 自由视角控制下的视点依赖主动感知能力
- Method: 基于 3D Gaussian Splatting 场景构建 E3VS-Bench，5 阶段数据管线生成 2,014 个视点依赖 episode；VLM 智能体通过 5-DoF 离散动作空间主动探索
- Tasks: 具身 3D 视觉搜索（Embodied 3D Visual Search），6 种子任务：物体搜索、物体状态、物体属性、上下文搜索、空间推理、计数
- Sensors: 单目 RGB 相机（512×512, FOV 90°），可变帧数（1/3/5 帧）
- Robot Setup: 虚拟 5-DoF 相机智能体，非物理机器人；基于 SceneSplat++ 3DGS 渲染引擎
- Metrics: VLM Judge Score（1-5 分，GPT-5.1 评估）；Navigation Steps；Collision Rate
- Limitations: VLM-as-a-Judge 与人类评价相关性较弱（ρ=0.54）；仅零样本评估；仅室内场景
- Evidence Notes:

  - Gemini 3.0 Flash 最佳（2.79/5），但仍远低于人类（3.53/5）
  - GPT-5.1 仅略高于 Random Action
  - Start vs Goal 视角差距大，证明主动探索必要
  - Thinking 过程对 GPT-5.1 有效（+0.28），对 Gemini 3.0 Flash 无效
  - 多帧输入减少碰撞和步数但不提高正确率
  - Goal-initialized 实验解耦了识别和探索能力
## 本地引用关系

- [[sakamoto2026e3vsbench]]
## 证据元数据

- Fulltext Quality: fulltext
- Evidence Coverage: complete（全文通过 arXiv HTML 获取，含正文、附录、所有表格和图表描述）
- Confidence: high
- Summary: 基于 3D Gaussian Splatting 构建具身 3D 视觉搜索基准 E3VS-Bench，要求智能体在 5-DoF 视角空间中主动探索以获取视点依赖证据来回答问题，揭示当前 VLM 与人类在主动感知上的巨大差距


## Problem

现有具身 AI 基准（如 EQA）依赖静态观测或受限的平面导航（2-DoF），无法评估真实 3D 环境中自由 5-DoF 视角控制下的精细视点依赖现象：
- 垂直视角变化导致的可见性变化
- 容器内部内容的揭示
- 仅从特定角度才能辨别的物体属性

这些场景要求智能体主动调整视角，而非被动接收观测。


## Method

### 场景构建
- 基于 SceneSplat++ 的 99 个 3DGS 重建场景（源自 ScanNet++）
- 3DGS 相比传统 mesh 保留了精细纹理（小文字、品牌标志），使视点依赖问题可被定义

### 数据集构建管线（5 阶段）
1. **3D 场景筛选**：从 SceneSplat++ 中人工筛选 105 个高质量重建场景（最终 99 个通过所有过滤）
2. **QA 生成**：Gemini 2.5 Flash 自动生成候选 QA，覆盖多视角可回答性
3. **无效 QA 过滤**：人工验证，移除模糊、多义或不可回答的问题（约 1,120 小时人工标注）
4. **视点标注**：标注者标记每个问题的可回答视点和不可回答视点
5. **可回答性过滤**：GPT-5.1 过滤掉无需视角转移即可回答的 episode（盲测和起始视角评分 ≥3 的排除）

### 6 种问题类型
- **OS**（Object Search）：定位指定物体
- **OST**（Object State）：识别物体状态（开/关等）
- **OA**（Object Attribute）：辨识精细属性（文字、材质、颜色）
- **CGS**（Context-guided Search）：基于功能上下文推理目标
- **SR**（Spatial Reasoning）：空间关系推理
- **CNT**（Counting）：计数

### 任务设定
- 状态空间：$v_t = (x, y, z, \theta, \phi) \in \mathbb{R}^5$
- 动作空间：11 个离散动作（6 平移 + 4 旋转 + stop），平移 0.25m，旋转 30°
- 碰撞处理：碰撞后状态不变
- 评估：VLM-as-a-Judge（GPT-5.1），1-5 分量表，Spearman ρ=0.54 与人类评价一致

### VLM 智能体框架
- System Prompt：定义世界坐标系（Z 轴向上）和动作约束
- User Prompt：提供问题、当前观测、步数、3D 坐标、上一步动作和碰撞反馈
- 单帧观测为默认设置，最多 25 步


## Experiments

### 数据集划分
- Train：1,406 episodes / 900 QA pairs / 68 scenes
- Val：231 episodes / 132 QA pairs / 10 scenes
- Test：377 episodes / 258 QA pairs / 21 scenes

### 主要结果（Table 2, test set, VLM Judge Score 1-5）

| 模型 | OS | OST | OA | CGS | SR | CNT | Avg |
|------|-----|------|------|------|------|------|------|
| Random Action | 2.38 | 2.18 | 2.60 | 2.20 | 2.50 | 2.00 | 2.28 |
| Gemini 2.5 Pro | 3.14 | 2.36 | 2.45 | 2.60 | 2.25 | 2.04 | 2.54 |
| **Gemini 3.0 Flash** | **3.21** | 2.82 | **3.18** | **3.53** | 2.75 | 1.88 | **2.79** |
| Gemini 3.0 Pro | 3.07 | 2.55 | 3.18 | 3.40 | **3.00** | 1.96 | 2.75 |
| GPT 5.1 | 2.90 | 2.18 | 2.53 | 2.73 | 2.25 | 1.88 | 2.42 |
| Qwen3-VL-8B | 2.86 | 2.36 | 2.60 | 3.13 | 1.88 | 1.96 | 2.46 |
| Qwen3-VL-30B | 2.67 | 2.09 | 2.60 | 2.47 | 2.25 | 1.84 | 2.32 |
| InternVL3.5-8B | 2.66 | 2.18 | 2.24 | 2.60 | 2.12 | 1.60 | 2.21 |
| Step3-VL-10B | 2.38 | 2.27 | 2.38 | 3.13 | 2.50 | 1.64 | 2.24 |
| **Human** | 3.12 | **3.59** | **4.06** | **4.06** | **3.35** | **3.59** | **3.53** |

### 静态基线对比（Table 3）
- **Blind VLM**（无图像）：Gemini 2.5 Flash 1.82，Qwen3-VL-8B 1.67
- **VQA at Start**：Gemini 2.5 Flash 2.14（起始视角不够）
- **VQA at Birdview**：仅 1.48-1.59（鸟瞰视角不够）
- **VQA at Goal**：Gemini 2.5 Flash 3.58，GPT-5.1 3.60，Human 4.12
- **2D Visual Search**（SEAL/DyFO）：1.68/1.86（远低于 3D 探索）
- Start vs Goal 差距巨大，证明需要主动探索

### 消融实验
1. **Thinking 过程**（Table 4）：GPT-5.1 + thinking 从 2.42 → 2.70；Gemini 3.0 Flash + thinking 无显著变化
2. **多帧记忆**（Fig. 6）：1/3/5 帧对比，多帧减少步数和碰撞率，但对正确率无显著影响
3. **Goal-initialized 视点**（Table 5）：从目标视角出发，Gemini 3.0 Flash 3.41，Qwen3-VL-8B 3.38，接近 VQA at Goal 上界

### 关键发现
- Gemini 3.0 Flash 整体最强（2.79），但仍远低于人类（3.53）
- GPT-5.1 仅略高于 Random Action（2.42 vs 2.28）
- CNT（计数）是最难的类别，所有模型表现最差
- SR（空间推理）中 Gemini 3.0 Pro 达到接近 VQA at Goal 的性能，说明该模型具备空间视角规划能力
- CGS（上下文搜索）比 OS（物体搜索）更容易，因为可用功能区域推理
- OA（属性识别）对视角高度敏感，需要探索性视角发现


## Limitations

1. **VLM-as-a-Judge 弱相关性**：Spearman ρ=0.54，自动评估可能不够准确捕捉视角充分性
2. **评分偏差**：最终观测与目标视角差异大时仍可能获得相似评分
3. **零样本评估**：当前工作仅做 zero-shot，未利用 train/val split 优化
4. **3DGS 渲染限制**：部分视点可能存在穿透或渲染伪影，尽管有人工过滤
5. **场景覆盖**：仅室内场景（ScanNet++），未覆盖户外或大规模环境
6. **动作空间离散**：固定 0.25m 平移和 30° 旋转可能无法捕捉精细视角调整


## Key Takeaways

1. **3DGS 作为具身 AI 仿真环境的优势**：相比 mesh 保留了精细纹理，使视点依赖任务可定义。这对 DLO 操控有启发——DLO 的形变状态同样高度视点依赖
2. **VLM 的 5-DoF 视角规划缺陷**：当前 VLM 在 2D 推理强，但 3D 主动感知弱，说明需要专门的视角规划训练
3. **视点依赖证据的重要性**：验证了"单视角不够"的假设，对机器人操控中多视角观测策略有参考价值
4. **Benchmark 设计模式**：5 阶段过滤管线（生成 → 人工验证 → 标注 → 可回答性过滤）可作为构建其他具身 AI 基准的模板
5. **VLM-as-a-Judge 的局限**：ρ=0.54 提醒我们在评估开放式回答时需要谨慎，可能需要更精细的评估协议

## 相关概念

- [[imitation-learning]]
- [[vision-language-model]]
- [[robot-learning]]
- [[planning]]
- [[sim-to-real]]
- [[deformable-linear-object]]

## 相关研究者

- [[sakamoto|Sakamoto, Koya]]
- [[miyanishi-taiki|Miyanishi, Taiki]]
- [[kurita|Kurita, Shuhei]]
