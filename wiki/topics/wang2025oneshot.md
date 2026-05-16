---
title: "One-Shot Dual-Arm Imitation Learning"
tags: [imitation]
created: "2026-04-25"
updated: "2026-04-25"
type: "literature"
status: "done"
summary: "提出 ODIL（One-Shot Dual-Arm Imitation Learning），从单次演示学习双臂协调操控。核心是 3 阶段视觉伺服：(1) 3D 视觉伺服用粗定位；(2) 3D+2.5D 视觉伺服结合深度匹配器（SIFT+LightGlue, SuperPoint+LightGlue）进行精确对齐。提出 4 种双臂协调范式：Act-Act（双臂同时动作）、Stabilize-Act（一臂固定一臂动作）、Rearrange-Act（一臂重排一臂动作）、Rearrange-Rearrange（双臂重排）。ABB YuMi 双臂机器人验证，6 个日常任务，平均 4-DoF 精度 77.2%"
authors: "Wang, Yilong; Johns, Edward"
year: "2025"
venue: "2025 IEEE International Conference on Robotics and Automation (ICRA)"
zotero_key: "28GQCRAU"
---
## 摘要

We introduce One-Shot（单样本） Dual-Arm（双臂） Imitation Learning（模仿学习） (ODIL), which enables dual-arm（双臂） robots to learn precise and coordinated everyday tasks from just a single demonstration（示范数据） of the task. ODIL uses a new three-stage visual servoing (3VS) method for precise alignment between the end-effector and target object, after which replay of the demonstration（示范数据） trajectory is sufficient to perform the task. This is achieved without requiring prior task or object knowledge, or additional data collection and training following the single demonstration（示范数据）. Furthermore, we propose a new dual-arm（双臂） coordination paradigm for learning dual-arm（双臂） tasks from a single demonstration（示范数据）. ODIL was tested on a real-world dual-arm（双臂） robot, demonstrating stateof-the-art performance across six precise and coordinated tasks in both 4-DoF and 6-DoF settings, and showing robustness in the presence of distractor objects and partial occlusions. Videos are available at: https://www.robot-learning. uk/one-shot（单样本）-dual-arm（双臂）.


## 中文简述

提出基于模仿学习的双臂方法，具有单样本学习特点。

**研究方向**: 模仿学习

## 关键贡献

1. 单样本双臂模仿学习：仅需一次演示即可学习新任务
2. 3 阶段视觉伺服：3D 粗定位 → 3D+2.5D 精确对齐，渐进提高精度
3. 深度匹配器集成：SIFT+LightGlue 和 SuperPoint+LightGlue 实现鲁棒特征匹配
4. 4 种双臂协调范式：系统化分类双臂协作模式
5. 零样本泛化：通过视觉伺服自然泛化到新物体实例
## 结构化提取

- **Problem**: 从单次演示学习双臂协调操控并泛化到新物体
- **Method**: ODIL — 3 阶段视觉伺服（3D→3D+2.5D）+ 深度匹配器（SIFT+LG/SP+LG）+ 双臂协调范式
- **Tasks**: 6 个双臂日常任务（拧盖/拾取/开合/转移/插入/折叠）
- **Sensors**: RGB-D 相机（固定+腕部）
- **Robot Setup**: ABB YuMi 双臂机器人
- **Metrics**: 4-DoF 位姿精度（平均 77.2%）+ 任务成功率
- **Limitations**: 遮挡敏感、精度有限、单样本鲁棒性、未扩展长时序
- **Evidence Notes**: 全文读取，Figures 提供完整任务演示和性能对比
## 本地引用关系

- [[chen2025coordinated]]
- [[gao2024prime]]
- [[grotz2025twin]]
- [[hartz2024art]]
- [[karim2024davil]]
- [[liu2025forcemimic]]
## 证据元数据

- **Fulltext Quality**: fulltext
- **Evidence Coverage**: 读取了全文，包括 abstract、introduction (Sec I)、related work (Sec II)、method (Sec III)、experiments (Sec IV)、figures (1-10)
- **Confidence**: high — 全文完整，ICRA 2025，Imperial College London，3 阶段视觉伺服（3D→3D+2.5D），深度匹配器（SIFT+LG, SP+LG），双臂协调范式（Act-Act/Stabilize-Act/Rearrange-Act/Rearrange-Rearrange），ABB YuMi，6 任务，77.2% 平均 4-DoF 精度
- **Summary**: 提出 ODIL（One-Shot Dual-Arm Imitation Learning），从单次演示学习双臂协调操控。核心是 3 阶段视觉伺服：(1) 3D 视觉伺服用粗定位；(2) 3D+2.5D 视觉伺服结合深度匹配器（SIFT+LightGlue, SuperPoint+LightGlue）进行精确对齐。提出 4 种双臂协调范式：Act-Act（双臂同时动作）、Stabilize-Act（一臂固定一臂动作）、Rearrange-Act（一臂重排一臂动作）、Rearrange-Rearrange（双臂重排）。ABB YuMi 双臂机器人验证，6 个日常任务，平均 4-DoF 精度 77.2%


## Problem

双臂协调操控需要精确的时空协调，现有方法依赖大量演示或复杂策略网络。如何从单次演示高效学习双臂协调策略，并在不同物体实例上泛化？


## Method

- **任务设定**：
  - 输入：单次演示视频（双臂动作），当前 RGB-D 观察
  - 输出：双臂 6D 位姿指令
  - 无需训练策略网络，纯视觉伺服
- **3 阶段视觉伺服**：
  - Stage 1（3D 视觉伺服）：粗定位双臂到目标附近
  - Stage 2（3D+2.5D 视觉伺服）：结合 3D 点匹配和 2.5D 像素对齐
  - Stage 3（精确执行）：基于匹配器的精细调整
- **深度匹配器**：
  - SIFT + LightGlue（LG）：传统特征+现代匹配器
  - SuperPoint (SP) + LightGlue：学习特征+匹配器
  - SP+LG 在纹理丰富场景更优，SIFT+LG 更鲁棒
- **双臂协调范式**：
  - Act-Act：双臂同时执行动作（如双侧挤压）
  - Stabilize-Act：一臂固定物体，一臂执行操作（如扶瓶拧盖）
  - Rearrange-Act：一臂重排环境，一臂执行操作
  - Rearrange-Rearrange：双臂同时重排（如折叠衣物）
- **演示处理**：
  - 从演示中提取关键帧和对应的双臂位姿
  - 基于任务阶段自动识别协调范式
  - 视觉伺服目标从演示关键帧中提取


## Experiments

- **6 任务评估**（ABB YuMi 双臂）：
  - 瓶盖拧开（Stabilize-Act）
  - 双侧物体拾取（Act-Act）
  - 盒子开合（Rearrange-Act）
  - 物体转移（Rearrange-Act）
  - 双侧对齐插入（Act-Act）
  - 折叠调整（Rearrange-Rearrange）
- **性能指标**：
  - 平均 4-DoF 精度：77.2%（位置+方向）
  - 位置精度优于方向精度
  - SP+LG 和 SIFT+LG 在不同任务上各有优势
- **消融**：
  - 3 阶段伺服优于 1 阶段或 2 阶段
  - 深度匹配器优于传统匹配方法
  - 协调范式选择对性能有显著影响


## Limitations

1. 仅适用于演示中可见的协调模式，无法自动发现新模式
2. 视觉伺服对遮挡和光照变化敏感
3. 单样本学习的鲁棒性有限，某些任务可能需要多次尝试
4. 4-DoF 精度（77.2%）在精密装配场景可能不够
5. 未扩展到移动双臂或长时序多步任务


## Key Takeaways

- 视觉伺服是单样本双臂操控的有效范式：无需策略训练，利用演示+实时匹配
- 3 阶段渐进式伺服解决精度问题：粗→细的分层策略
- 双臂协调范式的系统化分类有助于任务分解：4 种模式覆盖常见双臂任务
- 深度匹配器（LightGlue）显著提升视觉伺服鲁棒性：优于传统 ICP/特征匹配
- 单样本学习通过视觉伺服自然实现泛化：匹配器对物体实例变化鲁棒

## 相关概念

- [[imitation-learning]]
- [[bimanual-manipulation]]

## 相关研究者

- [[wang-yilong|Wang, Yilong]]
