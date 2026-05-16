---
title: "Closed-Loop Open-Vocabulary Mobile Manipulation with GPT-4V"
tags: [manipulation, VLM]
created: "2026-04-25"
updated: "2026-04-25"
type: "literature"
status: "done"
summary: "提出COME-robot首个基于GPT-4V的闭环开放词汇移动操控系统，包含三级开放词汇感知（全局/局部/物体）和分层故障恢复机制（物体/局部/全局级），8个真机任务成功率比CaP*基线提升~35%（65% vs 30%移动，75% vs 47.5%桌面），故障恢复率31/38。"
authors: "Zhi, Peiyuan; Zhang, Zhiyuan; Zhao, Yu; Han, Muzhi; Zhang, Zeyu et al."
year: "2025"
venue: "2025 IEEE International Conference on Robotics and Automation (ICRA)"
zotero_key: "F4KCMSJ4"
---
## 摘要

Autonomous robot navigation and manipulation（操控） in open environments require reasoning and replanning with closed-loop（闭环） feedback. In this work, we present COME-robot, the first closed-loop（闭环） robotic system utilizing the GPT-4V vision-language foundation model for open-ended reasoning and adaptive planning in real-world scenarios. COME-robot incorporates two key innovative modules: (i) a multi-level open-vocabulary perception and situated reasoning module that enables effective exploration of the 3D environment and target object identification using commonsense knowledge and situated information, and (ii) an iterative closed-loop（闭环） feedback and restoration mechanism that verifies task feasibility, monitors execution success, and traces failure causes across different modules for robust failure recovery. Through comprehensive experiments involving 8 challenging real-world mobile and tabletop manipulation（操控） tasks, COME-robot demonstrates a significant improvement in task success rate (∼35%) compared to state-of-the-art（现有最优方法） methods. We further conduct comprehensive analyses to elucidate how COME-robot’s design facilitates failure recovery, free-form instruction following, and longhorizon task planning.


## 中文简述

提出基于视觉-语言的移动操控方法，具有闭环控制特点。

**研究方向**: 机器人操控、视觉-语言模型

## 关键贡献

1. **COME-robot系统**：首个GPT-4V驱动的闭环OVMM系统，整合开放推理、导航、操控和故障恢复
2. **多级开放词汇感知**：全局级（前沿探索建大物体地图）→局部级（导航到目标区域建小物体地图）→物体级（近距离观察+GPT-4V属性推理）
3. **分层闭环反馈恢复**：状态验证器（可行性+成功性验证）+计划恢复器（物体/局部/全局三级回溯）
4. **~35%成功率提升**：8个真实世界任务全面优于CaP*基线
## 结构化提取

- Problem: 开放词汇移动操控中的环境理解和闭环故障恢复
- Method: COME-robot — GPT-4V + 三级开放词汇感知 + 分层闭环反馈恢复（物体/局部/全局级）
- Tasks: 8个真机任务（4移动：移动玩具/转移所有玩具/移动杯子和玩具/收集杯子 + 4桌面：放水果/水果在杯中/准备杯子/整理桌面）
- Sensors: RGB-D相机×2（底盘+腕部）、LiDAR、IMU、腕部RGB-D
- Robot Setup: 4轮差速底盘 + Kinova Gen3 7-DOF臂 + Robotic平行夹爪，Unitree B2+Z1
- Metrics: 成功率(SR)、步骤成功率(SSR)、恢复率(RR)
- Limitations: GPT-4V误检、抓取位置不利、API延迟成本、单环境测试
- Evidence Notes: 全文6147词，3张表，5张图，ICRA 2025，项目页come-robot.github.io
## 本地引用关系

- [[ao2025llmasbtplanner]]
- [[garcia2025generalizable]]
- [[qiu2025wildlma]]
- [[singh2025intellirms]]
- [[styrud2025automatic]]
- [[tang2025uad]]
## 证据元数据

- Fulltext Quality: fulltext
- Evidence Coverage: 完整全文（~6147 词），含 Table I-III、Figure 1-5、8个任务（4移动+4桌面）、完整失败分析
- Confidence: high — 全文可读，ICRA 2025，北京通用人工智能研究院(BIGAI)，真机实验充分
- Summary: 提出COME-robot首个基于GPT-4V的闭环开放词汇移动操控系统，包含三级开放词汇感知（全局/局部/物体）和分层故障恢复机制（物体/局部/全局级），8个真机任务成功率比CaP*基线提升~35%（65% vs 30%移动，75% vs 47.5%桌面），故障恢复率31/38。


## Problem

开放词汇移动操控(OVMM)面临两大挑战：
1. **环境理解困难**：非结构化3D环境感知、开放词汇目标识别、自然语言指令到场景目标的映射
2. **闭环重规划困难**：长时序移动操控中感知/执行失败累积，模块间依赖导致连锁错误（如导航到桌子窄侧限制抓取空间）
3. **现有方法局限**：传统闭环依赖预定义符号逻辑（不适应开放场景），LLM/VLM方法多限于桌面场景，忽视部分可观测性和模块间依赖


## Method

### 开放词汇感知与情境推理
- **Environment Explorer**（三级）：
  - 全局：前沿探索+全局物体地图（类别/位置/点云/视觉特征/语言描述）
  - 局部：GPT-4V推理目标区域→导航→SAM-2跟踪物体状态→建局部物体放置图
  - 物体：近距离图像→GPT-4V提取细粒度属性（如杯子是否空/干净）
- **Goal Reasoner**：GPT-4V基于常识推理选择目标（如空杯适合倒水）

### 闭环反馈与恢复
- **Status Verifier**：可行性验证（任务能否继续）+成功验证（执行是否成功，用腕部相机前后对比）
- **Plan Restorer**（三级恢复）：
  - 物体级：重新尝试操控（如换抓取姿态）
  - 局部级：更新局部物体地图重新定位
  - 全局级：导航到新位置寻找替代物体/更好访问角度

### 实现细节
- GPT-4V生成Python代码执行，JSON格式输出reason+code
- API库：explore_global、explore_local、report_observation、navigate、grasp、place
- 机器人：4轮差速底盘+RGB-D+LiDAR+IMU + Kinova Gen3 7-DOF臂+腕部RGB-D


## Experiments

### 移动操控（4任务×5试验）
| 任务 | CaP* SR | COME SR | COME SSR | RR |
|------|---------|---------|----------|-----|
| MOVE TOY | 2/5 | 3/5 | 17/20 | 2/4 |
| TRANSFER ALL TOYS | 1/5 | 2/5 | 30/42 | 1/4 |
| MOVE CUP AND TOY | 1/5 | 4/5 | 27/30 | 4/5 |
| GATHER CUPS | 2/5 | 4/5 | 27/30 | 7/10 |
| **总计** | **6/20** | **13/20** | **101/122** | **14/23** |

### 桌面操控（4任务×10试验）
| 任务 | CaP* SR | COME SR | COME SSR | RR |
|------|---------|---------|----------|-----|
| PLACE FRUIT | 5/10 | 7/10 | 34/40 | 4/7 |
| FRUIT AMONG CUPS | 6/10 | 8/10 | 18/20 | 1/3 |
| PREPARE CUP | 4/10 | 8/10 | 17/20 | 7/10 |
| TIDY TABLE | 4/10 | 7/10 | 54/60 | 5/9 |
| **总计** | **19/40** | **30/40** | **123/140** | **17/29** |

### 故障分析（Table III）
- 总故障52次，14次直接导致任务失败，31/38次成功恢复（恢复率81.6%）
- 感知失败：误检(8次,5次恢复)、漏检(2次,1次恢复)、视觉反馈错误(3次,1次恢复)
- 执行失败：API错误(8次,5次恢复)、抓取失败(24次,17次恢复)、放置失败(6次,3次恢复)、导航失败(1次)


## Limitations

1. GPT-4V视觉验证仍有误检（6个误检物体通过验证，3个导致任务失败）
2. 抓取成功率受限（24次失败，多因导航到不利位置如桌角/墙边）
3. 依赖GPT-4V API，延迟和成本问题
4. 仅在单一卧室环境测试，泛化性未验证
5. 移动操控成功率65%仍有较大提升空间


## Key Takeaways

1. 三级感知层次（全局→局部→物体）有效解决大规模场景的部分可观测性问题
2. 分层故障恢复是关键创新——跨模块追踪故障根因（如导航位置导致抓取失败→全局级恢复）
3. GPT-4V的常识推理能力使开放指令理解成为可能（如"准备杯子"→选择空杯子）
4. 闭环重规划在长时序任务中价值最大——移动任务步骤更多，更多失败机会
5. 来自BIGAI（北京通用人工智能研究院），Siyuan Huang和Baoxiong Jia组

## 相关概念

- [[robotic-manipulation]]
- [[vision-language-model]]
- [[grasping]]

## 相关研究者

- [[zhi-peiyuan|Zhi, Peiyuan]]
