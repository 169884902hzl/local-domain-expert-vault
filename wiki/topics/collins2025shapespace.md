---
title: "Shape-Space Deformer: Unified Visuo-Tactile Representations for Robotic Manipulation of Deformable Objects"
tags: [manipulation]
created: "2026-04-25"
updated: "2026-04-25"
type: "literature"
status: "done"
summary: "提出 Shape-Space Deformer，用统一潜在表示编码多种物体的变形，通过超网络条件化模板增强实现精细重建，在力泛化（Random CD 0.872 vs VIRDO 300.5）和新物体适应（k=2 样本 CD 0.521）上大幅超越 VIRDO，支持实时渲染（0.2s/重建）"
authors: "Collins, Sean M. V.; Tidd, Brendan; Baktashmotlagh, Mahsa; Moghadam, Peyman"
year: "2025"
venue: "2025 IEEE International Conference on Robotics and Automation (ICRA)"
zotero_key: "XT4NE2JY"
---
## 摘要

Accurate modelling of object deformations is crucial for a wide range of robotic manipulation（机器人操控） tasks, where interacting with soft or deformable objects is essential. Current methods struggle to generalise to unseen forces or adapt to new objects, limiting their utility in real-world applications. We propose Shape-Space Deformer, a unified representation for encoding a diverse range of object deformations using template augmentation to achieve robust, fine-grained reconstructions that are resilient to outliers and unwanted artefacts. Our method improves generalization to unseen forces and can ra~i~ly adapt to novel objects, significantly outperforming ex1stmg approaches. We perform extensive experiments to test a range of force generalisation settings and evaluate our method's ability to reconstruct unseen deformations. Our results demonstrate significant improvements in reconstruction accuracy and robustness. Our approach is suitable for real-time performance, making it ready for downstream manipulation（操控） applications.

## 中文简述

提出基于触觉感知的操控方法，具有泛化能力特点。

**研究方向**: 机器人操控

## 证据元数据

- **Fulltext Quality**: fulltext
- **Evidence Coverage**: 读取了全文，包括 abstract、introduction、related work、method (Sec III)、experiments (Sec IV)、tables (I-IV)、figures (1-7)
- **Confidence**: high — 全文完整，6 种厨房用具上进行了形状重建、力泛化、物体泛化三类实验
- **Summary**: 提出 Shape-Space Deformer，用统一潜在表示编码多种物体的变形，通过超网络条件化模板增强实现精细重建，在力泛化（Random CD 0.872 vs VIRDO 300.5）和新物体适应（k=2 样本 CD 0.521）上大幅超越 VIRDO，支持实时渲染（0.2s/重建）
## 关键贡献

1. 统一潜在表示：将多种物体及其变形状态编码在共享潜在空间中
2. 模板增强 + 超网络：用圆柱模板 + 超网络条件化生成变形场，而非固定名义形状
3. 显式表面渲染：变形场直接映射查询点到最近表面点，无需 Marching Cubes 等提取算法
4. 强泛化能力：在力泛化和新物体适应上大幅超越 VIRDO
## 结构化提取

- **Problem**: 可变形物体表示方法的力/物体泛化能力差
- **Method**: Shape-Space Deformer — 统一潜在表示 + 超网络条件化 + 变形场表面渲染
- **Tasks**: 可变形物体形状重建（铲子、勺子等厨房用具）
- **Sensors**: 视觉+触觉（反应力 + 接触位置）
- **Robot Setup**: 无实际机器人实验（纯仿真/数据集）
- **Metrics**: Chamfer Distance（CD↓）
- **Limitations**: 物体多样性有限、无闭环操控、方向泛化仍差
- **Evidence Notes**: 全文读取，Tables I-IV 提供完整定量结果
## 本地引用关系

- [[chen2025deformpam]]
- [[li2025routing]]
- [[scheikl620movement]]
## Problem

可变形物体的神经场表示方法（如 VIRDO）在未见过的力作用下泛化能力差，对新物体需要重新训练。SDF 标量输出无法直接定位表面点，限制了变形细节的重建质量。


## Method

- **统一表示**：n 个物体用 object code α∈R^6 编码，m 个变形用 force code z∈R^12 编码
- **超网络 ω**：MLP 以 [α, z] 为输入，输出主网络 Ω_D 的参数
- **Shape-Space Deformer Ω_D**：变形场，输入查询点 x∈R^3 → 输出位移向量 d∈R^3，x'=x+d 即最近表面点
- **力编码器 F**：从反应力 u 和接触位置 C 生成 force code z
- **训练**：联合优化 α、F、Ω_D（1M 参数），500 epochs，Adam optimizer
- **渲染**：将圆柱模板网格的顶点通过 Ω_D 变形到目标形状，0.2s 即可完成一次重建

关键创新 vs VIRDO：
- VIRDO：预训练名义形状网络 → 固定 → 在名义形状上训练变形网络（两阶段）
- Ours：统一学习名义+变形形状，通过超网络动态条件化（端到端）
- VIRDO 用 SDF（标量距离），Ours 用变形场（向量位移），直接定位表面


## Experiments

- **数据集**：VIRDO 数据集，6 种厨房用具（铲子、勺子等），每物体 24 个变形样本
- **形状重建（已知变形）**：CD 0.2035（名义）/ 0.4940（变形），vs VIRDO 0.7505/0.7640（提升 1.5-3.7×）
- **力泛化（未见力）**：
  - Random：0.872 vs VIRDO 300.5（提升 345×）
  - Lowest：0.579 vs 0.972
  - Highest：1.993 vs 375.8
  - Direction：5.895 vs 362.1
- **物体泛化**：k=2 样本即达 CD 0.521，k=4 达 0.383
- **效率**：1M 参数（vs VIRDO 52.6M），训练 0.45h（vs 8.78h），渲染 0.2s（vs 5.0s）


## Limitations

1. 仅在 6 种厨房用具上验证，物体多样性有限
2. 未在实际机器人操控任务中闭环测试
3. 物体泛化实验中 k=1 时 CD 高达 4.75（仍较差）
4. 方向泛化实验 CD=5.895 仍不理想
5. 依赖已知物体类别和接触位置信息


## Key Takeaways

- 统一潜在空间 + 超网络是比两阶段训练更有效的多物体变形表示方法
- 变形场（向量位移）比 SDF（标量距离）更适合可变形物体的精细重建
- 模板增强策略使模型能从其他物体迁移变形知识到新物体
- 极高参数效率（1M vs 52.6M）和实时渲染能力使下游应用可行
- 力泛化的关键在于共享变形空间中的知识迁移

## 相关概念

- [[robotic-manipulation]]
- [[deformable-linear-object]]
- [[tactile-sensing]]

## 相关研究者

- [[collins|Collins, Sean M. V.]]
