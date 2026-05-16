---
title: "Robotic Tissue Manipulation in Endoscopic Submucosal Dissection Via Visual Feedback"
tags: [manipulation]
created: "2026-04-25"
updated: "2026-04-25"
type: "literature"
status: "done"
summary: "磁力组织操控用于内镜黏膜下剥离术(ESD)：外部UR16e机械臂搭载永磁体操控体内磁夹，YOLO V5检测+PCA角度计算+改进最速下降导航算法，ROS Gazebo仿真中8.4秒平均完成±30°倾斜调整，仅仿真验证无真机实验。"
authors: "Zhang, Tao; Jue, Terry L.; Marvi, Hamid"
year: "2025"
venue: "2025 IEEE International Conference on Robotics and Automation (ICRA)"
zotero_key: "Q2554XSF"
---
## 摘要

Colorectal cancer is the third most commonly diagnosed cancer and the second leading cause of cancer-related deaths in the United States. Despite advancements in screening and treatment, there remains a critical need for more effective and minimally invasive methods to manage complex polyps and early-stage colorectal cancers. This study introduces a novel approach to magnetic tissue manipulation（操控） for Endoscopic Submucosal Dissection (ESD), leveraging visual feedback to enhance precision and control. We develop and evaluate the proposed system within a ROS Gazebo simulation environment, integrating a small magnetic endoscopic clip affixed to tissue, which is manipulated by an external large magnet mounted on a robotic arm.


## 中文简述

提出基于学习方法的操控方法。

**研究方向**: 机器人操控

## 关键贡献

1. **ROS Gazebo仿真环境**：建立了包含UR16e机械臂、磁力交互（偶极近似模型）、组织平台的完整仿真框架
2. **视觉反馈闭环磁力操控**：YOLO V5检测磁夹 + PCA计算倾斜角 + 改进最速下降导航算法（try-and-execute变体）
3. **多视角验证**：8个虚拟相机模拟不同内镜视角，目标角度±30°，平均8.4秒收敛
4. **从手工操控到机器人操控的演进**：系统对比了Table I中8种组织操控方法（手动/机器人 × 磁力/非磁力）
## 结构化提取

- Problem: ESD中组织牵引操控，需在受限空间精确控制磁夹倾斜角度以暴露黏膜下层
- Method: 外部永磁体(UR16e)操控体内磁夹，YOLO V5+PCA角度检测，改进最速下降导航算法
- Tasks: 磁夹倾斜角操控（目标±30°），ESD组织牵引
- Sensors: 虚拟RGB相机（8个视角模拟内镜），YOLO V5检测
- Robot Setup: UR16e机械臂 + 外部N52 NdFeB磁铁（210mm×50mm）+ 内部N55 NdFeB磁夹（3.1mm×10mm）
- Metrics: 操控时间（最大/最小/平均）、角度误差、末端执行器轨迹
- Limitations: 仅仿真（无噪声/软组织）、仅pitch角、PCA偶有误算、未做临床验证
- Evidence Notes: 全文5432词，2张实验表，2个算法，5张图，ROS Gazebo仿真环境
## 本地引用关系

- [[collins2025shapespace]]
- [[liu2025autonomous]]
- [[pallar2025optimal]]
- [[scheikl620movement]]
## 证据元数据

- Fulltext Quality: fulltext
- Evidence Coverage: 完整全文（~5432 词），含 Table I-II、Algorithm 1-2、Figure 1-5、完整参考文献
- Confidence: high — 全文可读，仿真实验数据完整，算法描述清晰
- Summary: 提出基于视觉反馈的磁力组织操控方法用于内镜黏膜下剥离术(ESD)，通过外部机械臂(UR16e)搭载永磁体操控体内磁夹，使用YOLO V5检测+PCA角度计算+改进最速下降导航算法，在ROS Gazebo仿真中8.4秒平均完成±30°倾斜调整。


## Problem

内镜黏膜下剥离术(ESD)中需要组织牵引以暴露黏膜下层进行精确切割，当前面临：
1. **操作空间受限**：结肠内空间狭小，传统器械难以操作
2. **手动磁控效率低**：现有磁力辅助ESD需额外医护人员手动操控外部磁铁，耗时长（传统ESD剥离阶段平均1394.7秒）
3. **精确控制困难**：手动控制无法实现亚毫米级精确操控
4. **人员依赖**：需要专门技术人员辅助，增加手术复杂度


## Method

### 磁力交互建模
- 外部磁铁：N52 NdFeB圆柱，直径210mm，厚50mm
- 内部磁夹：N55 NdFeB，外径3.1mm，内径2.1mm，厚10mm
- 基于磁偶极近似计算力和力矩（公式1-3）

### 视觉感知
- **YOLO V5**检测磁夹：2000+仿真图像训练，离线训练→在线推理
- **PCA角度计算**（Algorithm 1）：灰度化→二值阈值→非零像素提取→PCA→arctan计算倾斜角

### 导航算法（Algorithm 2）
- **改进最速下降法**：12方向等间隔圆形采样（30°间隔），当某方向产生25%以上角度变化时跳过剩余尝试
- 85%/95%误差减少时减速
- 误差<阈值（1-2°）时停止
- 外部磁铁仅沿xy平面移动（固定z和朝向）


## Experiments

### 仿真设置
- 8个相机模拟不同内镜视野
- 目标倾斜角：-30°和+30°（覆盖ESD所需11点-1点方向范围）

### 结果（Table II）
- **全数据集**：最大15.2s，最小5.3s，平均8.4s
- 按相机分：Camera 5最快（5.94s平均-30°），Camera 6最慢（9.43s平均+30°）
- 对比团队此前ex-vivo/in-vivo试验：操控时间从分钟级降至秒级
- 重复试验显示轨迹不同但均可收敛

### 对比分析（Table I）
- 与手动磁控[4][6][8][9]对比：机器人控制可减少人力需求
- 与非磁力机器人方法[10][11]对比：DRL方法平均规划时间377秒，本文方法8.4秒
- 与MARS机器人平台[13]对比：该方法无视觉反馈，本文引入视觉闭环


## Limitations

1. **仅仿真验证**：无随机噪声、无呼吸运动、无软组织变形（刚性假设）
2. **角度限制**：仅计算pitch角，未用yaw角（计划加入）
3. **PCA角度计算偶有错误**：作者承认有时推导出不正确的角度值
4. **临床现实挑战**：内镜镜头雾化/污渍、光线反射、手持相机抖动、患者体型差异
5. **磁力安全**：外部磁铁可能吸引内镜等金属器械
6. **±30°范围有限**：估计±45°仅略增时间，但未验证


## Key Takeaways

1. 磁力操控在受限空间（如结肠ESD）具有独特优势：无物理连接、运动范围大
2. 改进最速下降法（try-and-execute）比标准最速下降法更适合磁力操控场景（不需严格沿梯度方向）
3. YOLO+PCA的轻量视觉管线足以实现实时角度反馈
4. 从分钟级到秒级的时间缩减证明了机器人辅助磁力操控的可行性
5. 下一步为ex-vivo和in-vivo试验，需处理软组织变形和临床噪声

## 相关概念

- [[robotic-manipulation]]

## 相关研究者

- [[zhang|Zhang, Tao]]
