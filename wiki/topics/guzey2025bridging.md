---
title: "Bridging the Human to Robot Dexterity Gap Through Object-Oriented Rewards"
tags: [manipulation]
created: "2026-04-25"
updated: "2026-04-25"
type: "literature"
status: "done"
summary: "提出 HUDOR 框架，通过物体导向的点追踪奖励实现从单个人类视频到多指灵巧手策略的在线微调。核心流程：(1) VR 头显采集人类手指尖轨迹并转换到机器人坐标系；(2) 利用 IK 重放人类轨迹作为初始策略；(3) 用 Co-Tracker 追踪物体表面点，计算人类和机器人轨迹的物体运动相似度作为 RL 奖励；(4) DrQv2 + OU 噪声探索学习残差策略。4 个任务平均 4x 改进，Bread Picking 8/10，Card Sliding 7/10，Music Box 6/10，Paper Sliding 17cm"
authors: "Guzey, Irmak; Dai, Yinlong; Savva, Georgy; Bhirangi, Raunaq; Pinto, Lerrel"
year: "2025"
venue: "2025 IEEE International Conference on Robotics and Automation (ICRA)"
zotero_key: "72PFZYDQ"
---
## 摘要

Training robots directly from human videos is an emerging area in robotics and computer vision. While there has been notable progress with two-ﬁngered grippers, learning autonomous tasks without teleoperation remains a difﬁcult problem for multi-ﬁngered robot hands. A key reason for this difﬁculty is that a policy trained on human hands may not directly transfer to a robot hand with a different morphology. In this work, we present HUDOR, a technique that enables online ﬁne-tuning of the policy by constructing a reward（奖励） function from the human video. Importantly, this reward（奖励） function is built using object-oriented rewards derived from off-the-shelf point trackers, which allows for meaningful learning signals even when the robot hand is in the visual observation, while the human hand is used to construct the reward（奖励）. Given a single video of human solving a task, such as gently opening a music box, HUDOR allows our fourﬁngered Allegro hand to learn this task with just an hour of online interaction. Our experiments across four tasks, show that HUDOR outperforms alternatives with an average of 4→ improvement. Code and videos are available on our website https://object-rewards.github.io/.

## 中文简述

提出基于学习方法的操控方法，具有人类视频学习特点。

**研究方向**: 机器人操控

## 证据元数据

- **Fulltext Quality**: fulltext
- **Evidence Coverage**: 读取了全文，包括 abstract、introduction、related work (Sec II)、method (Sec III)、experiments (Sec IV)、tables (I-II)、figures (1-6)
- **Confidence**: high — 全文完整，ICRA 2025 正式发表，4 个灵巧操控任务系统评估，Allegro 手 + Kinova 臂真实实验
- **Summary**: 提出 HUDOR 框架，通过物体导向的点追踪奖励实现从单个人类视频到多指灵巧手策略的在线微调。核心流程：(1) VR 头显采集人类手指尖轨迹并转换到机器人坐标系；(2) 利用 IK 重放人类轨迹作为初始策略；(3) 用 Co-Tracker 追踪物体表面点，计算人类和机器人轨迹的物体运动相似度作为 RL 奖励；(4) DrQv2 + OU 噪声探索学习残差策略。4 个任务平均 4x 改进，Bread Picking 8/10，Card Sliding 7/10，Music Box 6/10，Paper Sliding 17cm
## 关键贡献

1. 首个仅用单个人类视频 + 手部姿态轨迹学习多指灵巧手策略的框架
2. 物体导向奖励：通过 Co-Tracker 追踪物体表面点运动，计算人类-机器人轨迹匹配奖励，优于图像级和点级匹配
3. 残差策略学习：在 IK 重放基础上学习残差，减少搜索空间
4. 空间泛化：通过物体检测 + 深度估计实现训练策略的位置迁移
## 结构化提取

- **Problem**: 多指灵巧手策略学习的人类-机器人形态鸿沟
- **Method**: HUDOR — 物体导向点追踪奖励 + 残差 DrQv2 策略学习 + IK 重放初始化
- **Tasks**: Bread Picking、Card Sliding、Music Box Opening、Paper Sliding
- **Sensors**: Meta Quest 3 VR 手部追踪 + 2×RealSense RGB-D 相机
- **Robot Setup**: Kinova JACO 6-DOF + Allegro 16-DOF 四指手
- **Metrics**: 成功率（10 次试验）、位移距离（cm）
- **Limitations**: in-scene 限制、探索轴先验、无重试机制、精度敏感任务泛化差
- **Evidence Notes**: 全文读取，Tables I-II 提供完整定量和奖励消融结果
## 本地引用关系

- [[chen2025vegetable]]
- [[chen2025vividex]]
- [[do2025watch]]
## Problem

多指灵巧手的策略学习面临两大挑战：(1) 人类手和机器人手的形态差异导致策略无法直接迁移；(2) 灵巧手遥操作困难且数据量大。现有方法需要额外的遥操作数据或在线人类干预。


## Method

- **数据采集**：Meta Quest 3 VR 头显获取手指尖位置 + RGB-D 相机获取视频
- **坐标系转换**：ArUco 标记建立 VR→world→robot 坐标变换
- **IK 重放**：全臂手 IK（梯度下降，手学习率 50x 臂学习率）生成初始轨迹
- **物体导向奖励**：
  - langSAM（GroundingDINO + SAM）生成初始物体分割 mask
  - Co-Tracker 在人类和机器人视频中追踪物体表面 N 个点
  - 计算物体运动向量（点集质心位移），RMSE 匹配作为奖励
  - Music Box 任务加入旋转向量并使用稀疏奖励（最后 5 帧）
- **残差策略**：DrQv2 学习残差 εr(atr, Δst, P̂Rt, TRt)，输入为人类重定位指尖位置+指尖速度变化+点集质心+物体运动
- **探索策略**：选定动作子集 + OU 噪声探索


## Experiments

- **Bread Picking**：HUDOR 8/10 vs BC 3/10 vs Point Cloud BC 3/10（15×10cm 区域）
- **Card Sliding**：HUDOR 7/10 vs BC 0/10（10×10cm 区域）
- **Music Box Opening**：HUDOR 6/10 vs BC 0/10（10×10cm 区域）
- **Paper Sliding**：HUDOR 17.3±1.5cm vs BC 4.1±1.3cm（15×15cm 区域）
- **奖励消融**：HUDOR vs Image OT（Bread 8 vs 6，Music Box 6 vs 1）vs Point OT（6 vs 2）
- **物体泛化**：Card Sliding 在新物体上 2-5/10，Bread Picking 在新物体上 2-5/10
- **空间泛化**：Bread Picking 在 15×10cm 范围内大部分位置成功，Music Box 因灵敏度要求泛化差
- **训练时间**：约 1 小时在线交互


## Limitations

1. 仅支持 in-scene 人类视频，不支持 in-the-wild 数据
2. 探索轴需要先验知识（手动选择哪些动作维度参与探索）
3. 无重试机制，犯错只能等下个 episode
4. 高精度任务（Music Box）空间泛化差
5. 物体形状/重量/摩擦差异影响泛化


## Key Takeaways

- 物体导向奖励（追踪物体运动而非图像匹配）是跨形态策略迁移的关键
- 轨迹级匹配优于点级和图像级匹配，因为避免了点对应不一致和视觉差异问题
- 残差策略大幅缩小搜索空间，使在线 RL 在 1 小时内收敛
- 离线 BC 方法在灵巧任务上严重过拟合，在线修正是必要的
- 点追踪（Co-Tracker）是连接人类和机器人行为空间的通用工具

## 相关概念

- [[robotic-manipulation]]
- [[grasping]]

## 相关研究者

- [[guzey|Guzey, Irmak]]
- [[pinto-lerrel|Pinto, Lerrel]]
