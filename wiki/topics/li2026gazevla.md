---
title: "GazeVLA: Learning human intention for robotic manipulation"
tags: [manipulation, imitation, robot-learning]
created: "2026-04-30"
updated: "2026-04-30"
type: "literature"
status: "done"
summary: "通过大规模第一人称视频学习人类注视意图作为中间表示，采用意图-动作推理链（CoT）范式将人类意图迁移至机器人操控，在仿真与真实场景的长时序和精细操控任务上显著优于基线方法"
authors: "Li, Chengyang; Xiong, Kaiyi; Xu, Yuan; Qian, Lei; Wang, Yizhou et al."
year: "2026"
venue: "arXiv Preprint"
zotero_key: "Q3B5P3X8"
---
## 摘要

Embodied foundation models have achieved significant breakthroughs in robotic manipulation（机器人操控）, yet they still depend heavily on large-scale robot demonstrations. Although recent works have explored leveraging human data to alleviate this dependency, effectively extracting transferable knowledge remains a significant challenge due to the inherent embodiment（具身） gap between human and robot. We argue that the intention underlying human actions can serve as a powerful intermediate representation for bridging this gap. In this paper, we introduce a novel framework that explicitly learns and transfers human intention to facilitate robotic manipulation（机器人操控）. Specifically, we model intention through gaze, as it naturally precedes physical actions and serves as an observable proxy for human intent. Our model is first pretrained on a large-scale egocentric human dataset to capture human intention and its synergy with action, followed by finetuning on a small set of robot and human data. During inference, the model adopts a Chain-of-Thought reasoning paradigm, sequentially predicting intention before executing the action. Extensive evaluations in simulation and real-world settings, across long-horizon（长时序） and fine-grained tasks, and under few-shot（少样本） and robustness benchmarks, show that our method consistently outperforms strong baselines, generalizes better, and achieves state-of-the-art（现有最优方法） performance.

## 中文简述

提出基于预训练的操控方法，具有泛化能力特点。

**研究方向**: 机器人操控、模仿学习、机器人学习

## 关键贡献

1. 提出显式建模意图的学习框架，将意图（gaze）作为感知与动作之间的中间表示，使模型遵循意图-动作推理链
2. 验证了从人类数据学到的意图可以迁移到机器人端（无需机器人侧意图标注），显著提升操控性能和泛化能力
3. 在仿真（AV-ALOHA）和真实场景（ALOHA 夹爪 + Unitree G1 灵巧手）上进行全面评估，在长时序任务和精细操控上一致优于基线
## 结构化提取

- Problem: VLA 模型依赖大量机器人示教数据，现有利用人类数据的方法未充分利用人类行为的意图结构
- Method: VLIA (Vision-Language-Intention-Action)，基于 PaliGemma VLM + flow matching 动作专家，将注视作为意图中间表示，采用意图-动作 CoT 推理链
- Tasks: pick-and-place、螺丝拧紧、瓶子放置、键盘打字、钩包装、穿针（仿真）、精细操控
- Sensors: 第一人称 RGB 相机、Pupil Neon 眼镜（注视 + 相机位姿）、HaWoR 手部追踪
- Robot Setup: 双臂 ALOHA（2×7-DoF 夹爪）、Unitree G1（26-DoF 含灵巧手）、AV-ALOHA 仿真（21-DoF 含主动视觉臂）
- Metrics: 任务成功率（ID/OOD 条件下各 20-100 次试验）、意图预测误差（平均 4.8% 图像对角线）
- Limitations: 预训练不含机器人数据、未显式对齐人机动作空间、注视仅 2D、评估样本量有限
- Evidence Notes:

  - 仿真 OOD 场景相对 π0.5 提升 22%（Table 1，具体数值在图片中未完全提取）
  - 真实 pick-and-place 85% 成功率；精细操控为 π0.5 的 2 倍（Fig. 6）
  - 消融验证意图迁移、CoT 推理、泛化能力、人类数据贡献四个维度（Table 2）
  - 注视预测在相同视觉输入不同语言指令下能正确区分任务目标（Fig. 4 反事实实验）
## 本地引用关系

-
## 证据元数据

- Fulltext Quality: fulltext (arXiv HTML 完整抓取)
- Evidence Coverage: 完整覆盖所有章节，包括 Introduction、Method、Experiments (仿真+真实+消融)、Conclusion；补充材料未获取
- Confidence: high
- Summary: 通过大规模第一人称视频学习人类注视意图作为中间表示，采用意图-动作推理链（CoT）范式将人类意图迁移至机器人操控，在仿真与真实场景的长时序和精细操控任务上显著优于基线方法


## Problem

现有 VLA（Vision-Language-Action）模型严重依赖大规模机器人示教数据，采集成本高且难以扩展。虽然已有方法尝试利用人类数据缓解此问题，但存在三类不足：

1. **2D 视觉原语方法**（关键点/边界框/轨迹）：这些信号是后处理得到的，不能反映人类动作选择的内在决策过程
2. **跨具身对齐方法**（联合训练/共享隐空间）：仍面临较大的人-机器人具身差距
3. **通用预训练方法**（视觉表示/世界模型）：只关注"做什么"而忽略了"为什么这样做"

核心洞察：人类行为遵循"意图先于动作"的认知原则，注视（gaze）天然先于物理动作且直接反映任务目标，可作为意图的可观测代理信号。


## Method

### 数据构建
- **预训练数据**：聚合 13 个第一人称数据集（ADT, Nymeria, EGTEAGaze+, Ego4D, EgoMe, HOT3D, Ego-Exo4D, HoloAssist, H2O, TACO, OAKINK2, HOI4D, EgoDex），共 150M+ 帧，包含手部标注和注视标注
- **后训练数据**：使用 Pupil Neon 眼镜采集人类示教 + 少量机器人数据，1:1 采样比例
- 数据处理：长视频由 Qwen 切分为原子动作片段，统一坐标系（以片段首帧相机坐标系为参考），MANO 模型重建手部运动
- 动作空间：a ∈ ℝ^(2×24)（双手机器人），包含 5 指尖位置 + 手腕位置 + 6DoF 手腕旋转 + 手部掩码
- 意图表示：i ∈ ℝ²，即图像平面上的 2D 注视坐标

### 模型架构 (VLIA)
- **VLM 主干**：PaliGemma（SigLIP 视觉编码器 + Gemma-2B 语言模型）
- **动作专家**：条件 flow matching 生成连续动作序列
- **意图-动作推理链**：先自回归预测意图 token（gaze 坐标离散化为 token），再基于 KV cache 通过 flow matching 生成连续动作

### 损失函数
- 意图损失：标准自回归 next-token prediction，L_intent
- 动作损失：条件 flow matching，L_action
- 总损失：L = λ_action × L_action + λ_intent × L_intent，其中 λ_action=1, λ_intent=0.1

### 训练策略
- **预训练（人类数据）**：分阶段训练——先冻结 VLM 只训练动作专家（warm-up），再全参数联合优化；20k steps，8×A800，batch size 2048，lr=5e-5
- **后训练（人类+机器人数据）**：联合训练，机器人数据无意图标注，但意图知识通过人类数据迁移
- 训练时对图像和注视信号进行同步数据增强，缓解人类注视中心偏差


## Experiments

### 仿真实验（AV-ALOHA）
- **平台**：双臂 7-DoF + 7-DoF 相机臂 = 21-DoF 主动视觉操控
- **数据**：每任务 100 条轨迹训练，100 次推理评估
- **基线**：LFA (ACT-based)、DP (Diffusion Policy)、H-RDT (人类预训练)、π0.5
- **ID 结果**：全面优于所有基线
- **OOD 结果**（干扰物+光照变化）：相对 π0.5 提升 22%；LFA 和 DP 在光照变化下成功率为 0%
- 注释：Table 1 的具体数值未在 HTML 中完整呈现（为图片格式），论文声称全面领先

### 真实世界实验
- **平台 1**：双臂 ALOHA（夹爪，2×7-DoF）
- **平台 2**：Unitree G1（灵巧手 Inspire Hands，2×7-DoF 手臂 + 2×6-DoF 灵巧手 = 26-DoF）
- **数据**：每任务 10 条机器人轨迹 + 50 条人类示教（各约 10 分钟采集）
- **评估**：每方法每任务 20 次试验
- **结果**：
  - 简单 pick-and-place：85% 成功率
  - 精细操控（螺丝拧紧）：成功率为 π0.5 的 2 倍
  - 灵巧操控（瓶子放置、键盘打字）：意图引导使长时序任务中按键更精准，基线方法常出现累积错误

### 消融实验
1. **意图迁移**：机器人训练数据无意图标注，但预测的注视仍准确定位到操控对象上 → 人类意图成功迁移到机器人
2. **CoT 推理**：去除意图推理链（直接从视觉+语言预测动作）后性能下降 → 意图-动作因果结构有实质贡献
3. **泛化能力**：在 OOD 物体位置、新物体类别、未见背景下均优于 ACT/DP/π0.5；背景变化时 ACT/DP 成功率降至 0%
4. **人类数据贡献**：
   - 仅机器人数据（无预训练）→ 易过拟合
   - 加人类数据 finetune 但无预训练 → 小数据下可能崩溃
   - 预训练 + 联合后训练（完整方法）→ 最佳泛化


## Limitations

1. **预训练不含机器人数据**：当前框架预训练阶段仅使用人类数据，未引入机器人数据联合预训练
2. **未显式对齐人-机器人动作空间**：没有在统一的隐空间中显式对齐人类和机器人的动作表示
3. **注视表示局限性**：仅用 2D 像素坐标表示意图，可能丢失 3D 空间信息
4. **评估规模有限**：每个真实世界任务仅 20 次试验，统计显著性可能不够强
5. **补充材料未获取**：更多实现细节和额外实验结果未在本次精读中覆盖


## Key Takeaways

1. **意图作为中间表示是有效桥接**：将人类注视意图作为"为什么这样做"的显式中间表示，比直接模仿"做什么"更能实现跨具身迁移——这对 DLO 操控中"先看后动"的策略选择有启发
2. **CoT 推理范式在 VLA 中的价值**：意图-动作的顺序推理链（先预测注视点，再生成动作）显著提升精细操控精度，尤其适合需要准确定位的任务
3. **大规模人类数据 + 小规模机器人数据的范式**：150M 帧人类数据预训练 + 少量机器人数据微调的模式值得借鉴，降低了机器人数据采集成本
4. **注视信号的可获取性**：AR/VR 设备（Pupil Neon 等）使注视数据的大规模采集成为可能，且采集成本远低于机器人示教
5. **与 DLO 操控的关联**：DLO 操控中操作者通常会先注视目标接触点再执行动作，注视意图建模可直接应用于 DLO 任务的任务分解和关键点定位

## 相关概念

- [[robotic-manipulation]]
- [[imitation-learning]]
- [[robot-learning]]
- [[vision-language-model]]
- [[diffusion-model]]
- [[deformable-linear-object]]
- [[bimanual-manipulation]]
- [[grasping]]

## 相关研究者

- [[li-chengyang|Li, Chengyang]]
