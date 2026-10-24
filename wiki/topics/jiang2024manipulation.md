---
title: "Robot manipulation in salient vision through referring image segmentation and geometric constraints"
tags: [manipulation, RL]
created: "2026-04-25"
updated: "2026-04-25"
type: "literature"
status: "done"
summary: "提出 CLIPU2Net 轻量级参考图像分割模型（6.6MB 解码器），集成到手眼视觉伺服系统，通过几何约束（点-点、点-线、线-线、平行线）将语言指令转化为机器人动作。GPT-4o 自动推断几何约束类型。46 个真实世界操控任务验证，在 4 种操控场景（reach-grasp、pick-place、pull-open、pour）中优于传统 Vita 方法"
authors: "Jiang, Chen; Luo, Allie; Jagersand, Martin"
year: "2024"
venue: "arXiv Preprint"
zotero_key: "TWQMPW7H"
---
## 摘要

In this paper, we perform robot manipulation（机器人操控） activities in real-world environments with language contexts by integrating a compact referring image segmentation model into the robot’s perception module. First, we propose CLIPU2Net, a lightweight referring image segmentation model designed for fine-grain boundary and structure segmentation from language expressions. Then, we deploy the model in an eye-in-hand visual servoing system to enact robot control in the real world. The key to our system is the representation of salient visual information as geometric constraints, linking the robot’s visual perception to actionable commands. Experimental results on 46 real-world robot manipulation（机器人操控） tasks demonstrate that our method outperforms traditional visual servoing methods relying on labor-intensive feature annotations, excels in finegrain referring image segmentation with a compact decoder size of 6.6 MB, and supports robot control across diverse contexts.

## 中文简述

提出基于学习方法的操控方法。

**研究方向**: 机器人操控、强化学习

## 证据元数据

- **Fulltext Quality**: fulltext
- **Evidence Coverage**: 读取了全文，包括 abstract、introduction、related work (Sec II)、method (Sec III)、experiments (Sec IV)、tables (I-IV)、figures (1-7)
- **Confidence**: high — 全文完整，arXiv 2024 预印本，46 个真实机器人任务系统评估，消融实验完备
- **Summary**: 提出 CLIPU2Net 轻量级参考图像分割模型（6.6MB 解码器），集成到手眼视觉伺服系统，通过几何约束（点-点、点-线、线-线、平行线）将语言指令转化为机器人动作。GPT-4o 自动推断几何约束类型。46 个真实世界操控任务验证，在 4 种操控场景（reach-grasp、pick-place、pull-open、pour）中优于传统 Vita 方法
## 关键贡献

1. CLIPU2Net：6.6MB 解码器的参考图像分割模型，使用 masked attention fusion 和 U2Net 解码器实现精细边界分割
2. 几何约束框架：将分割结果转化为 p2p/p2l/l2l/par 四种几何约束用于 UIBVS 控制
3. GPT-4o 自动推断：从初始视觉观察和任务描述自动确定几何约束类型
4. 46 个真实世界任务验证，覆盖 4 种操控场景
## 结构化提取

- **Problem**: 传统视觉伺服依赖人工标注，LLM 方法计算昂贵且只有点级 affordance
- **Method**: CLIPU2Net + 几何约束 + UIBVS 控制，GPT-4o 自动推断约束
- **Tasks**: 46 个真实世界操控任务（4 种场景：reach-grasp、pick-place、pull-open、pour）
- **Sensors**: Eye-in-hand RGB 相机
- **Robot Setup**: 桌面 Franka 机器人（真实）
- **Metrics**: 成功率（3 次尝试计分：100%/50%/0%），约束推断准确率
- **Limitations**: 零件分割有限、约束推断不稳定、需启发式配对
- **Evidence Notes**: 全文读取，Tables I-IV 提供完整分割/控制/消融结果
## 本地引用关系

- [[garcia2025generalizable]]
- [[liu2025kuda]]
- [[tang2025kalie]]
## Problem

传统 eye-in-hand 视觉伺服系统依赖人工标注的视觉特征，无法处理遮挡和透明物体。LLM/VLM 方法计算成本高且仅输出点级 affordance，无法提供精细边界信息。如何在轻量模型中实现语言驱动的参考图像分割并桥接到视觉伺服控制？


## Method

- **CLIPU2Net 架构**：
  - CLIP 视觉/文本编码器提取联合视觉-文本表示
  - Masked Multimodal Fusion：替换 FiLM，使用 masked attention 仅计算文本-图像 token 间注意力
  - U²Net 解码器：6 个 RSU 块，恢复多尺度信息
  - 融合 CLIPSeg 的 U 形 transformer encoder 信息（第 9/6/3 层视觉特征）
  - Focal + DICE 联合损失
- **几何约束**：
  - p2p (点-点)、p2l (点-线)、l2l (线-线)、par (平行线) 四种基础约束
  - Object-gripper interaction：PCA 提取显著性图的点/线
  - Object-object interaction：双注意力（携带物+目标），双 prompt
  - UIBVS 控制律：ė = Ju(q)q̇，Jacobian 用 Broyden's method 在线更新
- **约束推断**：GPT-4o 从初始观察 + 任务描述推断约束类型 E 和目标 prompt l


## Experiments

- **参考图像分割**：
  - PhraseCut: mIoU 0.542, cIoU 0.589（优于 MDETR 0.531/0.546，仅 1/4 大小）
  - DIS5K: Fβ^m 0.846（优于 FP-DIS 0.831）
  - UMD+GT: Sα 0.932（优于 CLIPUNetr 0.897）
- **机器人控制（46 任务）**：
  - Reach-and-Grasp: 水果/饮料/工具类 91-100% 成功率
  - Pick-and-Place: 83-100% 成功率（GPT-4o 约束推断 87.5-100% 准确）
  - Pull-open: 100% 成功率
  - Pour: 100% 成功率
  - vs Classical Vita: glass cup 从 38%→75%，close drawer 从 0%→100%
- **消融**：masked attention 和 U2Net 解码器均显著贡献（+0.04 mIoU）


## Limitations

1. 零件分割能力有限（无法区分 pen cap vs pen body，knife blade vs handle）
2. GPT-4o 约束推断准确率因任务而异（50-100%）
3. 需要预定义的启发式点/线配对（静态点在图像固定位置）
4. 透明/反光物体（glass cup）仍是挑战


## Key Takeaways

- 几何约束（点+线）是视觉伺服中通用且有效的运动表示，可适配多种操控场景
- 轻量模型（6.6MB）足以实现实时参考图像分割，优于大型 LLM 方法
- Masked attention fusion 通过限制注意力计算减少收敛问题
- GPT-4o 可推断线级 affordance（如手柄），验证操控上下文可从图像几何中提取
- 双注意力机制（object-gripper + object-object）覆盖 pick-place 全流程

## 相关概念

- [[robotic-manipulation]]
- [[reinforcement-learning]]
- [[vision-language-model]]
- [[grasping]]

## 相关研究者

- [[jiang|Jiang, Chen]]
