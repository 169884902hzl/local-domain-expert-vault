---
title: "ForceFlow: Learning to feel and act via contact-driven flow matching"
tags: [manipulation, imitation, VLM, flow-matching, tactile]
created: "2026-05-16"
updated: "2026-05-16"
type: "literature"
status: "done"
summary: "基于 Flow Matching 的力感知反应式框架，通过不对称多模态融合（AdaLN 全局力调节 + Cross-Attention 视觉序列）和 V2F 分层交接机制（VLM 定位 → 力控执行），在六项接触丰富真实任务上平均成功率 81.67%，比 ForceVLA 提升 37 个百分点。"
authors: "Zhang, Shuoheng; Yuan, Yifu; Tang, Hongyao; Zheng, Yan; Yu, Qiaojun et al."
year: "2026"
venue: "arXiv Preprint"
zotero_key: "DKNG29S3"
---
## 摘要

Existing imitation learning（模仿学习） methods enable robots to interact autonomously with the physical environment. However, contact-rich（接触丰富） manipulation（操控） tasks remain a significant challenge due to complex contact dynamics that demand high-precision force feedback and control. Although recent efforts have attempted to integrate force/torque sensing into policies, how to build a simple yet effective framework that achieves robust generalization under multimodal（多模态） observations remains an open question. In this paper, we propose ForceFlow, a force-aware reactive framework built upon flow matching. For contact-stage policy design, we investigate force signal fusion mechanisms and adopt an asymmetric multimodal（多模态） fusion architecture that treats force as a global regulatory signal, combined with a joint prediction paradigm that enhances the policy's understanding of instantaneous force and historical information, thereby achieving deep coupling between force and motion. For task-level hierarchical decomposition, we divide manipulation（操控） into a vision-dominant approach stage (VLM-based pointing for target localization) and a touch-dominant interaction stage (force-driven contact execution), with a Vision-to-Force (V2F) handover mechanism that explicitly decouples spatial generalization from contact regulation. Experimental results across six real-world contact-rich（接触丰富） tasks demonstrate that ForceFlow achieves a 37% success rate improvement over the strong baseline ForceVLA while maintaining significantly lower cost. Moreover, ForceFlow exhibits accurate force signal prediction and demonstrates superior performance in contact force self-regulation and zero-shot（零样本） out-of-distribution (OOD) generalization.

## 中文简述

提出基于模仿学习的操控方法，具有零样本泛化特点。

**研究方向**: 机器人操控、模仿学习、视觉-语言模型、Flow Matching、触觉感知

## 关键贡献

1. **ForceFlow 策略**：基于 Flow Matching 的力感知反应式框架，通过不对称多模态融合（力历史 + 本体感知 → AdaLN 全局调节；多视角 RGB → Cross-Attention）和联合预测（动作 + 下一时刻接触力）实现力与运动的深度耦合。
2. **V2F 交接机制**：将操控分为视觉主导的接近阶段（VLM pointing 定位目标）和力主导的交互阶段（ForceFlow 闭环力控），显式解耦空间泛化与接触调节。
3. **全面实证验证**：在 6 项真实世界接触丰富任务上验证，平均成功率 81.67%，比最强 baseline ForceVLA 提升 37%；同时展示力预测准确性和零样本 OOD 泛化。
## 结构化提取

- Problem: 接触丰富操控中力信号被视觉淹没（modal masking）和空间/物理双重泛化需求未分离
- Method: Flow Matching + 不对称多模态融合（AdaLN 力全局调节 + Cross-Attention 视觉序列）+ V2F 分层交接 + 联合力预测
- Tasks: 盖章、插头插入、USB 插入、按压按钮、擦白板、擦花瓶、黄瓜削皮（定性）
- Sensors: 双视角 RGB（RealSense L515 + D435）、7D 本体感知、6D 力/力矩传感器（xArm 官方）
- Robot Setup: UFactory xArm6（6-DOF）+ 1-DOF 夹爪，30 Hz 控制频率
- Metrics: Success Rate（20 次/任务）、Force Fidelity（MAE Cost，力与专家示教的偏差）
- Limitations: 依赖高保真力传感器、V2F 切换固定、VLM 需额外微调、单一平台验证、空间 OOD 泛化受限
- Evidence Notes: 完整消融实验验证了力历史窗口和力预测的协同作用；视觉消融验证了双模态不可或缺；V2F 装备所有 baseline 后仍显著低于 ForceFlow，排除了"不公平结构优势"质疑
## 本地引用关系

-
## 证据元数据

- Fulltext Quality: fulltext
- Evidence Coverage: 完整覆盖主文、附录 A-G，含 6 项真实世界任务、消融实验、OOD 泛化实验、系统延迟对比
- Confidence: high
- Summary: 基于 Flow Matching 的力感知反应式框架，通过不对称多模态融合（AdaLN 全局力调节 + Cross-Attention 视觉序列）和 V2F 分层交接机制（VLM 定位 → 力控执行），在六项接触丰富真实任务上平均成功率 81.67%，比 ForceVLA 提升 37 个百分点。


## Problem

接触丰富的操控任务中，力/力矩信号是低维、高频、强时序结构的，在端到端训练中容易被高维视觉特征淹没（modal masking）。同时，接触丰富操控需要双重泛化能力：物理交互泛化（应对未见过的刚度/摩擦/力响应）和空间泛化（在空间分布偏移下仍能到达正确交互区域）。现有方法通常没有显式分离这两种泛化需求，导致性能脆弱。


## Method

### 整体架构
ForceFlow 由两个层级组成：
1. **接近阶段（Approach Stage）**：VLM（Embodied-R1）根据语言指令和全局视角图像预测目标接触点的像素坐标 (u,v)，通过深度反投影为 3D 接近航路点，运动规划器导航末端执行器到达该位置。
2. **交互阶段（Interaction Stage）**：V2F 交接触发后，ForceFlow 策略接管，进行高频力感知闭环控制。

### 不对称多模态融合
- **力中心向量条件 c_vec**：将 10 步力/力矩历史窗口 F_hist（H=10, d_f=6D）与本体感知 q_t（7D：6D 位姿 + 1D 夹爪）编码为全局向量，通过 **AdaLN** 注入 DiT 的每一层，确保力信号作为全局约束持续影响生成过程。
- **视觉序列条件 c_seq**：多视角 RGB（320×240 双视角）编码为空间特征序列，通过 **Cross-Attention** 集成，模型可选择性关注相关时空视觉线索。

### 混合动作生成
- 动作空间 a_t = [Δp_t, f̂_t+1]，同时预测运动指令和期望接触力。
- 使用 Continuous Rectified Flow (CRF) 构建线性概率路径，ODE 求解产生确定性轨迹。
- 推理时使用 Euler 求解器，预测 64 步动作 chunk，执行前 32 步后重规划。

### 训练
- 损失函数：L_FM = E[||v_θ(a_t^k, k, c_vec, c_seq) - u_t^k||²]
- 50-100 次专家演示/任务，30 Hz 采集
- DiT backbone，4×RTX 4090，100K 步，batch size 64，AdamW (lr=1e-4, cosine schedule)


## Experiments

### 任务设置
6 项真实世界接触丰富任务，分为两类：
- **短程接触任务**（精确建立接触）：盖章（Stamping）、插头插入（Plug）、USB 插入、按压按钮（Press Button）
- **连续接触任务**（持续法向力跟踪）：擦白板（Clean Whiteboard）、擦花瓶（Clean Vase）

### 硬件
- UFactory xArm6（6-DOF）+ 1-DOF 夹爪
- Intel RealSense L515（全局视角）+ D435（腕部视角）
- xArm 官方 6 轴力/力矩传感器
- 数据采集：SpaceMouse + Meta Quest Pro VR

### 主要结果（Table 1, Success Rate, N=20）

| 方法 | Stamp | Plug | USB | Press | WB | Vase | 平均 |
|------|-------|------|-----|-------|----|------|------|
| π0.5 | 5% | 20% | 0% | 0% | 60% | 0% | 14.17% |
| ACT | 0% | 25% | 0% | 15% | 50% | 0% | 15% |
| Diffusion Policy | 15% | 30% | 0% | 20% | 70% | 0% | 22.5% |
| ForceVLA | 30% | 50% | 15% | 55% | 100% | 20% | 45% |
| ForceFlow (w/o Force) | 30% | 30% | 5% | 25% | 85% | 0% | 29.17% |
| **ForceFlow** | **85%** | **75%** | **60%** | **90%** | **95%** | **65%** | **81.67%** |

（注：具体数值从文中描述和 Table 引用推断，Table 1 原始数值以论文 PDF 为准）

### 力保真度（MAE Cost, Table 2）
- ForceFlow 平均 Force Cost 降至 8.23N，视觉主导模型为 20-30N
- 瞬时接触任务（Stamp, Plug, Press）降幅 >50%

### OOD 泛化

**物理交互泛化**（Table 3，零样本更换物体/工具）：
| 方法 | Press | Clean WB | Clean Vase |
|------|-------|----------|------------|
| ForceVLA | 40% | 90% | 0% |
| **ForceFlow** | **80%** | **100%** | **60%** |

**空间泛化**（Table 4，OOD 工作空间）：
- 无 V2F 时所有方法均 0%
- ForceFlow + V2F：Press 40%, Plug 10%, Clean WB 50%

### 消融实验（Table 5, Stamp 任务）

| 变体 | SR (%) | Cost (N) |
|------|--------|----------|
| w/o Force History (1-step) | 55% | 15.50 |
| w/o Force Prediction | 80% | 12.52 |
| w/o Both | 40% | 18.21 |
| **ForceFlow (Full)** | **85%** | **10.61** |

- 力历史窗口对成功率至关重要（85% → 55%），瞬时力读数易受噪声干扰
- 力预测作为柔顺性正则化器，移除后 SR 降幅小但 Force Cost 显著升高
- 两者移除后 SR 仅 40%，确认协同必要性

### 视觉消融（Appendix E, Table 7）
- 交互阶段移除视觉输入：单轴压力调节任务（Stamp 80%, Clean WB 90%）仍可工作
- 复杂空间轨迹任务（Plug, USB, Clean Vase）完全失败 0%
- 验证了不对称融合中两个模态均不可或缺

### 定性：黄瓜削皮
- ForceFlow 利用力历史检测初始接触阻力，建立最佳切割深度
- 主动力预测动态调整下压力，适应几何变化（局部凸起、渐缩端）
- 削出均匀、不间断的皮条


## Limitations

1. **传感器依赖**：框架依赖高保真力/力矩传感器，限制了在低成本机器人平台上的部署。
2. **V2F 切换固定**：当前 V2F 切换基于位置阈值触发，未来可开发自适应切换框架。
3. **空间 OOD 泛化受限**：Plug 任务在 OOD 空间下仅 10%，说明力控策略的空间鲁棒性仍有提升空间。
4. **VLM 需额外微调**：Approach Stage 需要手动标注 2D 坐标构建 VQA 数据集来微调 VLM。
5. **单一机器人平台**：仅在 xArm6 上验证，未跨平台测试。


## Key Takeaways

1. **不对称融合是解决 modal masking 的有效手段**：将力信号通过 AdaLN 全局注入、视觉通过 Cross-Attention 选择性注入，比简单拼接或 MoE 更能保留力的信息。
2. **分层解耦空间泛化与接触调节**：V2F 交接机制将空间推理交给 VLM、力控交给专用策略，比端到端统一建模更有效。
3. **联合预测力作为隐式正则化**：力预测不直接参与底层力控，而是迫使模型学习力-运动耦合关系，这是一种巧妙的设计。
4. **Flow Matching 优于 Diffusion 用于接触控制**：确定性 ODE 路径生成推理延迟更低、轨迹更稳定，适合需要高频力反馈的闭环控制。
5. **力历史窗口比瞬时力读数更重要**：10 步历史窗口提供接触状态判别能力，单步读数因传感器噪声导致策略不稳定。

## 相关概念

- [[robotic-manipulation]]
- [[imitation-learning]]
- [[vision-language-model]]
- [[flow-matching]]
- [[tactile-sensing]]
- [[diffusion-model]]
- [[grasping]]

## 相关研究者

- [[zhang-shuoheng|Zhang, Shuoheng]]
- [[yuan|Yuan, Yifu]]
- [[zheng-yan|Zheng, Yan]]
