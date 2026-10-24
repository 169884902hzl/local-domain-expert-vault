---
title: "Unifying Representation and Calibration With 3D Foundation Models"
tags: [manipulation]
created: "2026-04-25"
updated: "2026-04-25"
type: "literature"
status: "done"
summary: "提出JCR方法利用3D基础模型(DUSt3R)从机械臂挂载RGB相机同时完成手眼标定和场景表征构建，无需标定标记（AprilTag/棋盘格），仅10张图像即可收敛，尺度误差<3.1%，并成功用于抓取和推动任务。"
authors: "Zhi, Weiming; Tang, Haozhan; Zhang, Tianyi; Johnson-Roberson, Matthew"
year: "2022"
venue: "IEEE Robotics and Automation Letters"
zotero_key: "7RZXHXMN"
---
## 摘要

Representing the environment is a central challenge in robotics, and is essential for effective decision-making. Traditionally, before capturing images with a manipulator-mounted camera, users need to calibrate the camera using a speciﬁc external marker, such as a checkerboard or AprilTag. However, recent advances in computer vision have led to the development of 3D foundation models. These are large, pre-trained neural networks that can establish fast and accurate multi-view correspondences with very few images, even in the absence of rich visual features. This paper advocates for the integration of 3D foundation models into scene representation approaches for robotic systems equipped with manipulator-mounted RGB cameras. Speciﬁcally, we propose the Joint Calibration and Representation (JCR) method. JCR uses RGB images, captured by a manipulator-mounted camera, to simultaneously construct an environmental representation and calibrate the camera relative to the robot’s end-effector, in the absence of speciﬁc calibration markers. The resulting 3D environment representation is aligned with the robot’s coordinate frame and maintains physically accurate scales. We demonstrate that JCR can build effective scene representations using a low-cost RGB camera attached to a manipulator, without prior calibration.


## 中文简述

提出基于学习方法的操控方法。

**研究方向**: 机器人操控

## 关键贡献

1. **JCR（Joint Calibration and Representation）方法**：首个从同一组RGB图像同时完成手眼标定和场景表征构建的方法，无需外部标记
2. **尺度恢复问题（SRP）**：将手眼标定扩展为同时求解手眼变换T_ce和尺度因子λ的优化问题
3. **多属性连续表征**：从少量RGB图像构建占据、颜色、语义分割的连续3D表征（神经网络隐式表示）
4. **低成本低图像验证**：~$10 USB摄像头+10张图像即可工作，部署门槛低
## 结构化提取

- Problem: 机械臂挂载RGB相机的无标记手眼标定和场景表征统一构建
- Method: JCR — DUSt3R 3D基础模型获取稠密对应 → 手眼标定（SO(3)对数映射闭式解+SRP尺度恢复）→ 连续神经表征（占据/颜色/分割）
- Tasks: 手眼标定、3D场景重建、抓取（Grasp）、推扫（Sweep）
- Sensors: 低成本USB RGB摄像头（~$10），挂载于机械臂末端
- Robot Setup: Unitree Z1 六自由度机械臂，RTX 4090 GPU推理
- Metrics: 标定残差（δt, δR）、尺度百分比误差、新视角渲染一致性、下游任务成功率
- Limitations: 仅静态环境、未融入标定不确定性、简单下游任务验证
- Evidence Notes: 全文7408词，3张表，10张图，Algorithm 1，开源代码github.com/tomtang502/arm_3d_reconstruction
## 本地引用关系

- [[boerdijk2025autonomous]]
- [[garcia2025generalizable]]
- [[qureshi2025splatsim]]
- [[wu2025rlgsbridge]]
- [[xie102multiview]]
## 证据元数据

- Fulltext Quality: fulltext
- Evidence Coverage: 完整全文（~7408 词），含 Table I-III、Figure 1-10、Algorithm 1、公式(1)-(16)，4个子实验+2个下游任务
- Confidence: high — 全文可读，IEEE RA-L 2024，CMU Robotics Institute，对比实验充分
- Summary: 提出JCR方法利用3D基础模型(DUSt3R)从机械臂挂载RGB相机同时完成手眼标定和场景表征构建，无需标定标记（AprilTag/棋盘格），仅10张图像即可收敛，尺度误差<3.1%，并成功用于抓取和推动任务。


## Problem

机械臂挂载相机在使用前需要手眼标定，传统方法存在以下问题：
1. **标定过程繁琐**：需要特定外部标记（棋盘格/AprilTag），需采集大量标定图像
2. **SfM方法在少图像时失败**：COLMAP等传统SfM方法依赖手工特征匹配，在少图像（10-15张）或弱纹理场景（如光滑桌面）时无法收敛
3. **标定和建图分离**：标定与场景表征构建是独立步骤，需分步完成
4. **尺度缺失**：3D基础模型输出无物理尺度，需额外恢复


## Method

### 3D基础模型（DUSt3R）
- 输入RGB图像对，输出逐像素3D点图和置信度图
- 通过全局对齐优化恢复相对相机位姿（公式1）
- 无需手工特征，可处理弱纹理场景

### 手眼标定（无标记）
- **旋转求解**：利用SO(3)→so(3)对数映射，通过外积矩阵M的闭式解求解R_ce（公式7）
- **平移+尺度求解**：SRP优化问题（公式8-10），Q^TQ的闭式解+数值优化λ
- 核心：T_E^{i+1}_i * T^e_c = T^e_c * T_P^{i+1}_i(λ)（公式4）

### 场景表征构建
- **点云变换**：x̄_i = E^{-1}T_ce*(λ*xi)（公式12），转换到机器人坐标系
- **占据表征**：小MLP+正弦位置编码+NCE训练（公式13）
- **语义分割**：SAM分割2D标签→3D点多类分类（公式14）
- **颜色表征**：MSE回归RGB值（公式15）
- 所有表征15秒内训练收敛（RTX 4090）


## Experiments

### 手眼标定评估（Table I）
- **对比方法**：COLMAP、Ray Diffusion、JCR(DUSt3R)
- **结果**：COLMAP在10-12张图像时多个场景发散，Ray Diffusion误差大；JCR在所有场景和图像数量下残差最小（δt < 0.02, δR < 0.01）
- **效率**：DUSt3R推理+优化<1分钟（RTX 4090）

### 尺度恢复（Figure 4）
- 8张和10张图像，测量4个物体高度
- 10张图像时所有物体高度百分比误差≤3.1%

### 标记对比和新视角评估（Table III）
- JCR vs AprilTag标定：旋转差<0.02rad，平移差<8mm
- 新视角渲染与隐藏测试图像高度一致，无明显漂移

### 下游任务
- **Grasp任务**：从分割表征采样锤子3D点→GPD抓取姿态检测→成功抓取
- **Sweep任务**：从分割表征定位茶叶盒和终点线→推扫到目标位置→成功


## Limitations

1. 仅适用于静态环境，未处理动态场景
2. 未将标定不确定性融入表征构建
3. 依赖DUSt3R基础模型质量，模型偏差会影响结果
4. 下游任务仅展示2个简单场景（抓取+推扫）
5. 神经网络表征（单隐藏层256节点）可能在大场景中不够表达


## Key Takeaways

1. 3D基础模型（DUSt3R）可作为机器人视觉的"即插即用"模块，替代传统SfM
2. 手眼标定和场景建图可以统一在同一框架内，同一组图像完成两个任务
3. 少图像（10张）即可实现高质量标定和建图，大幅降低部署门槛
4. 低成本RGB相机（$10）即可替代深度相机用于场景建模
5. 来自CMU Robotics Institute，Matthew Johnson-Roberson组

## 相关概念

- [[robotic-manipulation]]
- [[grasping]]

## 相关研究者

- [[zhi|Zhi, Weiming]]
