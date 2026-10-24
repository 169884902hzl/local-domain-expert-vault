---
title: "KALIE: Fine-Tuning Vision-Language Models for Open-World Manipulation Without Robot Data"
tags: [manipulation, VLM]
created: "2026-04-25"
updated: "2026-04-25"
type: "literature"
status: "done"
summary: "提出 KALIE（Keypoint Affordance Learning from Imagined Environments），通过微调预训练 VLM 实现无机器人数据的开放世界操控。方法：(1) Affordance-aware 数据合成：ControlNet + soft edge context + 弹性变换生成多样合成图像，同时保持关键点标注一致性；(2) VLM 微调：CogVLM-17B + LoRA (rank 10, 6 layers)，自然语言输出关键点坐标。50 人工标注 → 500 合成图像。结果：table sweeping 14/15、drawer closing 15/15、towel hanging 13/15、trowel pouring 13/15、USB unplugging 9/15，全面超越 VoxPoser 和 MOKA"
authors: "Tang, Grace; Rajkumar, Swetha; Zhou, Yifei; Walke, Homer Rich; Levine, Sergey et al."
year: "2025"
venue: "2025 IEEE International Conference on Robotics and Automation (ICRA)"
zotero_key: "NQJMC837"
---
## 摘要

Building generalist robotic systems involves effectively endowing robots with the capabilities to handle novel objects in an open-world setting. Inspired by the advances of large pre-trained models, we propose Keypoint Affordance（可供性） Learning from Imagined Environments (KALIE), which adapts pre-trained Vision Language Models (VLMs) for robotic control in a scalable manner. Instead of directly producing motor commands, KALIE controls the robot by predicting pointbased affordance（可供性） representations based on natural language instructions and visual observations of the scene. The VLM is trained on 2D images with affordances labeled by humans, bypassing the need for training data collected on robotic systems. Through an affordance（可供性）-aware data synthesis pipeline, KALIE automatically creates massive high-quality training data based on limited example data manually collected by humans. We demonstrate that KALIE can learn to robustly solve new manipulation（操控） tasks with unseen objects given only 50 example data points. Compared to baselines using pre-trained VLMs, our approach consistently achieves superior performance.


## 中文简述

提出基于视觉-语言的操控方法。

**研究方向**: 机器人操控、视觉-语言模型

## 关键贡献

1. Affordance-aware 数据合成管线：ControlNet + soft edge context + 弹性变换，保持关键点标注一致性
2. 无机器人数据的 VLM 微调：仅需 50 张人工标注图像即可鲁棒解决新任务
3. 自然语言关键点输出格式：与 VLM 预训练任务一致，效果与回归头相当
## 结构化提取

- **Problem**: 无机器人数据微调 VLM 用于开放世界操控
- **Method**: KALIE — ControlNet affordance-aware 合成 + CogVLM-17B LoRA 微调 + 关键点 affordance
- **Tasks**: Table sweeping / Drawer closing / Towel hanging / Trowel pouring / USB unplugging
- **Sensors**: 俯视 RGB-D 相机
- **Robot Setup**: 7-DoF 机械臂 + Robotiq 2F-85 gripper
- **Metrics**: 任务成功率 (15 trials × 3 物体集) + MSE 关键点预测
- **Limitations**: 单臂桌面、开源 VLM 差距、仅 few-shot
- **Evidence Notes**: 全文读取，Table I + Figures 5-7 提供完整结果
## 本地引用关系

- [[garcia2025generalizable]]
- [[nasiriany2025rtaffordance]]
- [[patel2025realtosimtoreal]]
- [[smith2024steer]]
- [[tang2025uad]]
## 证据元数据

- **Fulltext Quality**: fulltext
- **Evidence Coverage**: 读取了全文，包括 abstract、introduction (Sec I)、related work (Sec II)、method (Sec III)、experiments (Sec IV)、figures (1-7)
- **Confidence**: high — 全文完整，ICRA 2025，UC Berkeley + Cornell，7-DoF 机械臂 + Robotiq 2F-85，CogVLM-17B + LoRA，50 示例 → 500 合成，5 任务 × 3 未见物体集
- **Summary**: 提出 KALIE（Keypoint Affordance Learning from Imagined Environments），通过微调预训练 VLM 实现无机器人数据的开放世界操控。方法：(1) Affordance-aware 数据合成：ControlNet + soft edge context + 弹性变换生成多样合成图像，同时保持关键点标注一致性；(2) VLM 微调：CogVLM-17B + LoRA (rank 10, 6 layers)，自然语言输出关键点坐标。50 人工标注 → 500 合成图像。结果：table sweeping 14/15、drawer closing 15/15、towel hanging 13/15、trowel pouring 13/15、USB unplugging 9/15，全面超越 VoxPoser 和 MOKA


## Problem

预训练 VLM 在机器人操控中零样本应用不稳定，需要大量硬编码领域知识补偿。直接在机器人数据上微调受限于数据规模。如何在不收集机器人数据的情况下，高效适应 VLM 用于开放世界操控任务？


## Method

- **问题设定**：
  - 输入：RGB-D 图像 + 自然语言指令
  - 输出：5 个关键点（grasp/function/target/pre-contact waypoint/post-contact waypoint）
  - 关键点驱动运动规划器生成 6-DoF 轨迹
- **Affordance-aware 数据合成**：
  - 开放词汇分割（SAM）→ 物体掩码
  - Soft edge map 作为 ControlNet 的上下文：保留轮廓但去除纹理细节
  - 对上下文应用变换 h()（缩放/平移/旋转/弹性扭曲）→ 新物体形状
  - 掩码扩展为 h(m) + m → ControlNet inpainting
  - 关键点同步变换：y' = h(y)
  - GPT-4V 采样替代物体描述
- **VLM 微调**：
  - CogVLM-17B + LoRA (rank 10, 6 layers)
  - 自然语言格式输出：'grasp keypoint': [x, y], ...
  - 交叉熵损失
  - Adam 优化器，lr=1e-5，cosine scheduler，6000 iterations
- **数据规模**：50 人工 + 500 合成 = 550 总计


## Experiments

- **5 任务 × 3 未见物体集 × 5 trials = 75 总评估**：
  - VoxPoser: 3/15, 8/15, 1/15, 0/15, 0/15
  - MOKA: 9/15, 9/15, 5/15, 7/15, 2/15
  - KALIE: **14/15, 15/15, 13/15, 13/15, 9/15**
- **消融**（sweeping 任务 MSE）：
  - 无增强 > 仅标准增强 > KALIE 完整方法
  - Soft edge context 优于 depth/segmentation mask
  - 10 示例 + 合成 ≈ 50 示例 + 合成：合成数据显著提升可扩展性
  - 自然语言输出 ≈ 回归头：与 VLM 预训练更一致


## Limitations

1. 关键点 affordance 表示限于单臂桌面操控
2. 开源 VLM (CogVLM-17B) 与最先进闭源 VLM 有差距
3. 仅验证 few-shot 泛化，未展示 zero-shot 到新任务
4. 合成数据质量依赖 soft edge 提取的准确性
5. 单阶段任务，未扩展到多步骤操控


## Key Takeaways

- Soft edge context 是数据合成的关键：保留形状信息同时允许纹理多样性
- 无需机器人数据即可微调 VLM：人工标注图像 + 合成扩展足够
- 关键点 affordance 表示将运动生成与感知解耦：VLM 仅需预测关键点
- 合成数据使 10 示例达到 50 示例水平：数据合成是可扩展性的关键
- 自然语言输出格式与 VLM 预训练一致：无需额外输出头

## 相关概念

- [[robotic-manipulation]]
- [[vision-language-model]]
- [[grasping]]

## 相关研究者

- [[tang|Tang, Grace]]
