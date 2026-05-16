---
title: "UAD: Unsupervised Affordance Distillation for Generalization in Robotic Manipulation"
tags: [manipulation, VLM, imitation]
created: "2026-04-25"
updated: "2026-04-25"
type: "literature"
status: "done"
summary: "提出 UAD（Unsupervised Affordance Distillation），从基础模型无监督蒸馏 affordance 知识到任务条件 affordance 模型。两阶段：(1) 提取：DINOv2 多视角融合 → PCA → 聚类语义区域 + GPT-4o 提议任务指令并关联区域 → 余弦相似度生成连续 affordance 图；(2) 蒸馏：冻结 DINOv2 + FiLM 解码器训练任务条件 affordance 模型。仅用渲染单物体训练，零样本泛化到真实多物体场景。AGD20K benchmark 竞争性能（KLD 0.526 vs 1.405 LOCATE）。IL 策略：10 演示即可泛化到未见实例/类别/指令，真实 3 任务平均 73% 成功率"
authors: "Tang, Yihe; Huang, Wenlong; Wang, Yingke; Li, Chengshu; Yuan, Roy et al."
year: "2025"
venue: "2025 IEEE International Conference on Robotics and Automation (ICRA)"
zotero_key: "UNXN9T5I"
---
## 摘要

Understanding ﬁne-grained object affordances is imperative for robots to manipulate objects in unstructured environments given open-ended task instructions. However, existing methods of visual affordance（可供性） predictions often rely on manually annotated data or conditions only on a predeﬁned set of tasks. We introduce Unsupervised Affordance（可供性） Distillation (UAD), a method for distilling affordance（可供性） knowledge from foundation models into a task-conditioned affordance（可供性） model without any manual annotations. By leveraging the complementary strengths of large vision models and vision-language models, UAD automatically annotates a large-scale dataset with detailed <instruction, visual affordance（可供性）> pairs. Training only a lightweight task-conditioned decoder atop frozen features, UAD exhibits notable generalization to in-the-wild robotic scenes and to various human activities, despite only being trained on rendered objects in simulation. Using affordance（可供性） provided by UAD as the observation space, we show an imitation learning（模仿学习） policy that demonstrates promising generalization to unseen object instances, object categories, and even variations in task instructions after training on as few as 10 demonstrations. Project website with Appendix: unsup-affordance（可供性）.github.io/.


## 中文简述

提出基于模仿学习的操控方法，具有泛化能力特点。

**研究方向**: 机器人操控、视觉-语言模型、模仿学习

## 关键贡献

1. 无监督 affordance 标注管线：LVM（DINOv2）提供像素级特征 + VLM（GPT-4o）提议任务和关联区域
2. 任务条件 affordance 模型：冻结 DINOv2 + FiLM 解码器，仅用渲染单物体训练
3. Affordance 作为观察空间的 IL 策略：10 演示即可泛化到未见物体/类别/指令
## 结构化提取

- **Problem**: 从基础模型无监督蒸馏任务条件 affordance 知识
- **Method**: UAD — DINOv2 聚类 + GPT-4o 任务关联 + FiLM 解码器蒸馏 + affordance-as-observation IL
- **Tasks**: Pouring/Opening/Insertion（仿真）+ Drawer/Pen/Plant（真实）
- **Sensors**: RGB-D 相机（俯视/侧视）
- **Robot Setup**: Franka Emika Panda + 2 RGB-D 相机
- **Metrics**: AUC affordance + KLD/SIM/NSS (AGD20K) + 任务成功率
- **Limitations**: 单帧、单物体训练、运动泛化、小样本评估
- **Evidence Notes**: 全文读取，Table I + Figures 4-6 提供完整对比
## 本地引用关系

- [[chen2025effective]]
- [[hartz2024art]]
- [[lee2025diffdagger]]
- [[shi2025zeromimic]]
- [[tang2025kalie]]
## 证据元数据

- **Fulltext Quality**: fulltext
- **Evidence Coverage**: 读取了全文，包括 abstract、introduction (Sec I)、related work (Sec II)、method (Sec III)、experiments (Sec IV)、figures (1-6)、tables (I)
- **Confidence**: high — 全文完整，ICRA 2025，Stanford University（Fei-Fei Li 组），DINOv2 冻结 + FiLM 轻量解码器，BEHAVIOR1K 206 物体/76 类别/667 指令，OmniGibson 仿真 + Franka 真实，10 演示即可训练 IL 策略
- **Summary**: 提出 UAD（Unsupervised Affordance Distillation），从基础模型无监督蒸馏 affordance 知识到任务条件 affordance 模型。两阶段：(1) 提取：DINOv2 多视角融合 → PCA → 聚类语义区域 + GPT-4o 提议任务指令并关联区域 → 余弦相似度生成连续 affordance 图；(2) 蒸馏：冻结 DINOv2 + FiLM 解码器训练任务条件 affordance 模型。仅用渲染单物体训练，零样本泛化到真实多物体场景。AGD20K benchmark 竞争性能（KLD 0.526 vs 1.405 LOCATE）。IL 策略：10 演示即可泛化到未见实例/类别/指令，真实 3 任务平均 73% 成功率


## Problem

细粒度物体 affordance 理解对机器人开放世界操控至关重要。现有方法依赖手动标注或仅支持预定义任务集。如何从基础模型中无监督提取 affordance 知识并蒸馏为支持任意任务指令的轻量模型？


## Method

- **Affordance 提取**：
  - 3D 物体 → 14 视角渲染 → DINOv2 像素特征 → 多视角融合 → 3D 特征场
  - PCA 降维 → 聚类 → M 个语义区域
  - GPT-4o 提议任务指令 + 关联区域（visual prompting）
  - 区域参考特征 → 余弦相似度 → 连续 affordance 图 [0,1]^{H×W}
  - 数据集：BEHAVIOR1K，206 物体，76 类别，667 指令
- **Affordance 蒸馏**：
  - 冻结 DINOv2 + 3 层 FiLM (256→64→1) + BCE 损失
  - 语言嵌入来自 OpenAI API
  - FiLM 对空间位置无差别，适合建立特征-任务关联
- **IL 策略**：
  - Multi-view Transformer Policy（基于 RVT）
  - 输入：affordance 图 + 深度 + (x,y,z) 坐标 + 本体感觉
  - 输出：7D 动作（6-DoF 位姿 + gripper）
  - 仅 10 演示训练


## Experiments

- **Affordance 预测**：
  - 渲染物体：4 评估集（训练/新实例/新类别/新指令），AUC ≥ 0.92
  - DROID 真实机器人数据集：UAD 0.840 vs CLIP 0.500 vs OpenSeeD 0.836
  - AGD20K 人类活动：UAD KLD 0.526 vs LOCATE 1.405 vs AffordanceLLM 1.463
- **仿真 IL**（3 任务 × 4 泛化设置 × 15 trials）：
  - UAD 在所有设置下优于 DINOv2/CLIP/Voltron
  - 细粒度任务（Opening 检测薄手柄）优势最明显
- **真实 IL**（Franka + 2 RGB-D 相机）：
  - Open Drawer: 成功
  - Insert Pen: 成功
  - Water Plant: 成功
  - 平均成功率 73%（10 trials/task）


## Limitations

1. 仅提供视觉级 affordance，不直接提供运动级泛化
2. 仅考虑单帧静态 affordance，不支持多步视觉理解
3. 训练数据仅含单物体渲染，扩展到真实多物体可能改善
4. 未与更大规模 VLM（如 GPT-4V 微调）比较
5. IL 策略评估样本量较小（10 trials/task）


## Key Takeaways

- LVM+VLM 互补是关键：DINOv2 提供像素特征，GPT-4o 提供任务语义
- 仅用渲染单物体训练即可泛化到真实多物体：DINOv2 预训练特征的零样本迁移能力
- Affordance 作为观察空间优于原始 RGB：为 IL 策略提供任务相关注意力
- FiLM 是高效的语言条件化方法：仅训练轻量解码器
- 连续 affordance 图优于二值分割：保留细粒度功能区域信息

## 相关概念

- [[robotic-manipulation]]
- [[vision-language-model]]
- [[imitation-learning]]
- [[grasping]]

## 相关研究者

- [[tang-yihe|Tang, Yihe]]
- [[huang|Huang, Wenlong]]
- [[wang-yingke|Wang, Yingke]]
