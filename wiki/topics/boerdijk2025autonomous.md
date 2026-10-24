---
title: "Towards Autonomous Data Annotation and System-Agnostic Robotic Grasping Benchmarking with 3D-Printed Fixtures"
tags: [manipulation]
created: "2026-04-25"
updated: "2026-04-25"
type: "literature"
status: "done"
summary: "提出 3D 打印夹具（fixture）方法，通过在刚性物体上安装可拆卸的带 fiducial marker 的夹具，实现纯 RGB 图像的自主 6D 位姿标注（平均精度约 6mm），并支持可重复的机器人抓取基准测试"
authors: "Boerdijk, Wout; Durner, Maximilian; Sakagami, Ryo; Lehner, Peter; Triebel, Rudolph"
year: "2025"
venue: "2025 IEEE International Conference on Robotics and Automation (ICRA)"
zotero_key: "JCUAZUH7"
---
## 摘要

The interaction of robots with their environment requires robust object-centric perception capabilities, typically achieved using learning-based methods trained on synthetic data. However, real-world deployment demands evaluating these capabilities in relevant environments, often involving extensive manual annotation for a quantitative analysis. Additionally, standardized evaluations for robotic tasks, such as grasping（抓取）, need reproducible object scene configurations and performance benchmarks. We propose a solution to both problems by temporarily employing 3D-printed components, socalled fixtures, which can be designed for any rigid object. Once the scene is set up and object poses are extracted, the fixtures are removed, leaving the natural scene without any artificial distractions. The presented approach is seemingly applicable for pre-determined configurations of multiple objects, which enables precise re-building of scenes with consistent object-toobject relations. Our suggested annotation procedure achieves strong pose accuracy solely on RGB images without any manual involvement. We evaluate and show the usability of the proposed fixtures for automated real-world data annotation to fine-tune a detector and for benchmarking object pose estimation algorithms for robotic grasping（抓取）. Code and fixture meshes for 3D printing are available at https://github.com/DLRRM/fixture generation.

## 中文简述

提出基于学习方法的线缆操控方法。

**研究方向**: 机器人操控

## 证据元数据

- **Fulltext Quality**: fulltext
- **Evidence Coverage**: 读取了全文，包括 abstract、introduction、related work、method (Sec III)、experiments (Sec IV-VI)、tables (I-IV)、figures (1-7)、conclusion
- **Confidence**: high — 全文完整，实验设计严谨，定量数据充分
- **Summary**: 提出 3D 打印夹具（fixture）方法，通过在刚性物体上安装可拆卸的带 fiducial marker 的夹具，实现纯 RGB 图像的自主 6D 位姿标注（平均精度约 6mm），并支持可重复的机器人抓取基准测试
## 关键贡献

1. 提出 3D 打印夹具框架，可自动设计并安装在任意刚性物体上，通过 fiducial marker（AprilTag）从 RGB 图像自主获取 6D 物体位姿
2. 支持场景夹具（scene fixtures）捕获多物体间关系，实现精确场景重建
3. 验证了标注精度（平均深度偏移约 6mm）和夹具移除后物体位姿稳定性（<1mm 平移，<1° 旋转）
4. 展示两个应用：自动数据标注微调检测器 + 可重复的抓取基准测试
## 结构化提取

- **Problem**: 真实世界 6D 物体位姿标注耗时，跨系统抓取基准难以复现场景
- **Method**: 3D 打印可拆卸夹具 + AprilTag 标记 + BlenderProc 自动设计，纯 RGB 标注
- **Tasks**: 物体位姿标注、目标检测微调、机器人抓取基准测试
- **Sensors**: RGB 相机（Ximea 立体相机 + Manta GigE）
- **Robot Setup**: DLR SARA 7 轴机械臂 + 立体相机（第 6 关节）
- **Metrics**: 平均深度偏移、移除误差（平移/旋转）、mAP、抓取成功率
- **Limitations**: 仅刚性物体、手动移除夹具、扫描模型伪影
- **Evidence Notes**: 全文读取，Table I-IV 提供定量结果，18 个 YCB 物体 + 10 个场景夹具
## 本地引用关系

- [[grotz2025twin]]
- [[huang2025match]]
- [[lips2024keypoints]]
## Problem

1. 真实世界机器人数据标注耗时费力，特别是 6D 物体位姿标注
2. 跨系统、跨实验室的机器人抓取基准测试难以精确复现场景和物体配置


## Method

- **夹具设计**：三种类型 — top-down（通用）、slider（盒状物）、cylindric topper（圆柱物），通过 BlenderProc 自动生成
- **标注流程**：安装夹具 → 拍照检测 AprilTag → 推导物体位姿 → 移除夹具 → 干净图像
- **场景夹具**：多物体配置，捕获物体间关系，支持精确场景重建
- **位姿精度评估**：对比实际深度图与渲染深度图的差异


## Experiments

- **物体**：18 个 YCB 物体（4 圆柱、7 滑轨、6 顶装夹具）
- **场景**：10 个场景夹具（5 easy + 5 difficult），每个 3-5 个物体
- **标注精度**：平均深度偏移 6.23mm，优于 TLESS 的 9mm
- **移除误差**：平移 <1mm，旋转 <1°
- **检测器微调**：Yolov7 在 STIOS 数据集上 fine-tune 后 recall 从 0.742 提升至 0.938
- **抓取基准**：CosyPose+Yolov7 在 easy/difficult 场景分别成功抓取 10/9 个物体，ground truth 位姿可达 18/18


## Limitations

1. 仅适用于刚性物体
2. 扫描模型伪影影响夹具生成
3. 夹具需要手动移除
4. 圆柱物体 z-rotation 不确定


## Key Takeaways

- 简单但实用的工程方法解决了真实世界数据标注和场景复现两大难题
- 标注精度已达到可实用水平（6mm）
- 场景夹具概念对可重复基准测试有重要价值
- 代码和夹具模型开源

## 相关概念

- [[robotic-manipulation]]
- [[deformable-linear-object]]
- [[grasping]]

## 相关研究者

- [[boerdijk|Boerdijk, Wout]]
