---
title: "FlexiTac: A low-cost, open-source, scalable tactile sensing solution for robotic systems"
tags: [RL, sim-to-real, tactile, grasping, tactile-sensing]
created: "2026-05-01"
updated: "2026-05-01"
type: "literature"
status: "done"
summary: "提出基于 FPC-Velostat-FPC 三层叠层结构的低成本开源压阻式触觉传感器 FlexiTac（约$30/单元），支持 3D 视触觉融合、跨具身技能迁移和 real-to-sim-to-real 训练管线。"
authors: "Huang, Binghao; Li, Yunzhu"
year: "2026"
venue: "arXiv Preprint"
zotero_key: "ECR8AF7M"
---
## 摘要

We present FlexiTac, a low-cost, open-source, and scalable piezoresistive tactile（触觉） sensing solution designed for robotic end-effectors. FlexiTac is a practical "plug-in" module consisting of (i) thin, flexible tactile（触觉） sensor pads that provide dense tactile（触觉） signals and (ii) a compact multi-channel readout board that streams synchronized measurements for real-time control and large-scale data collection. FlexiTac pads adopt a sealed three-layer laminate stack (FPC-Velostat-FPC) with electrode patterns directly integrated into flexible printed circuits, substantially improving fabrication throughput and repeatability while maintaining mechanical compliance for deployment on both rigid and soft grippers. The readout electronics use widely available, low-cost components and stream tactile（触觉） signals to a host computer at 100 Hz via serial communication. Across multiple configurations, including fingertip pads and larger tactile（触觉） mats, FlexiTac can be mounted on diverse platforms without major mechanical redesign. We further show that FlexiTac supports modern tactile（触觉） learning pipelines, including 3D visuo-tactile（触觉） fusion for contact-aware decision making, cross-embodiment（具身） skill transfer, and real-to-sim-to-real（仿真到真实迁移） fine-tuning with GPU-parallel tactile（触觉） simulation. Our project page is available at https://flexitac.github.io/.

## 中文简述

提出基于触觉感知的操控方法，具有仿真到真实迁移特点。

**研究方向**: 强化学习、仿真到真实迁移、触觉感知、抓取、触觉感知

## 关键贡献

1. **FlexiTac 平台**：开源、低成本的触觉传感平台（约 $30/单元），集成柔性触觉传感器垫、紧凑型多通道读出板和统一软件接口，支持 100Hz 实时同步采集
2. **FPC 制造友好设计**：用 FPC（柔性印刷电路）上的图案化铜开孔直接作为电极，取代 V1 版本中手工对齐的导电丝，大幅提高制造重复性和吞吐量（约 5 分钟/垫）
3. **现代触觉学习管线支持**：演示了 FlexiTac 在三大学习管线中的适用性——3D 视触觉融合（3D-ViTac）、跨具身技能迁移（Touch in the Wild）、real-to-sim-to-real 训练（VT-refine）
## 结构化提取

- **Problem**: 现有机器人触觉传感器成本高、制造复杂、平台适配难、仿真支持不足
- **Method**: FPC-Velostat-FPC 三层叠层压阻式触觉传感器 + Arduino Nano 读出板 + 3D 视触觉融合 / 跨具身迁移 / Real-to-Sim-to-Real 三条学习管线
- **Tasks**: 多平台触觉传感部署展示（抓取、双臂操控、人形机器人操控、便携数据采集、手套采集），无单一任务定量评估
- **Sensors**: FlexiTac 压阻式触觉传感器阵列（12×32 / 8×16 / 16×16 / 32×32），多视角 RGB-D 相机，鱼眼相机
- **Robot Setup**: xArm 850, ALOHA, Franka, LeRobot 夹爪, Robotiq 2F-140, Dexmate 机器人, 半人形机器人, 便携式人工采集设备
- **Metrics**: 读出频率（100Hz）, 成本（~$30）, 制造时间（~5min/垫）, 厚度（<1mm）, 电极间距（2mm）— 无任务成功率等性能指标
- **Limitations**: 仅压力感知、仿真省略剪切力、无定量性能对比、传感器线性范围有限、缺乏长期耐久性验证
- **Evidence Notes**: 全文通过 arXiv HTML 获取，内容完整。作为系统/硬件论文，侧重平台设计和部署展示，定量实验数据缺失属于论文定位决定而非遗漏。三条学习管线（3D-ViTac、Touch in the Wild、VT-refine）的定量结果分别引用了已发表的对应论文。
## 本地引用关系

-
## 证据元数据

- Fulltext Quality: fulltext (via arXiv HTML)
- Evidence Coverage: full (all sections read: Abstract, Introduction, Hardware, System Integration, Conclusion, References)
- Confidence: high
- Summary: 提出基于 FPC-Velostat-FPC 三层叠层结构的低成本开源压阻式触觉传感器 FlexiTac（约$30/单元），支持 3D 视触觉融合、跨具身技能迁移和 real-to-sim-to-real 训练管线。


## Problem

现有机器人触觉传感器存在以下问题：
1. **成本高**：多数触觉传感器（如 GelSight、DIGIT 等视觉触觉传感器，ReSkin 等磁触觉传感器）价格昂贵或难以批量制造
2. **制造复杂度**：传统设计依赖手工对齐导电丝，重复性差、吞吐量低
3. **平台适配困难**：不同机器人末端执行器需要不同的机械设计
4. **仿真支持不足**：高维光学触觉图像难以在仿真中精确建模，限制了 Sim-to-Real 训练

FlexiTac 旨在提供一个低成本、开源、可扩展的压阻式触觉传感方案，降低触觉感知在机器人学习研究中的门槛。


## Method

### 硬件设计

**传感器原理**：压阻式传感矩阵，机械压力转化为电阻变化，读出电子电路将电阻变化转化为电压信号。

**传感器垫结构**（三层密封叠层）：
- 顶层 FPC：垂直方向电极引线
- 中间层：压阻薄膜（Velostat）
- 底层 FPC：水平方向电极引线
- 外层封装：层压片

**关键设计特点**：
- 总厚度 < 1mm，轻量柔性
- 电极间距 2mm，标准配置 12×32 感知矩阵
- V2 创新：FPC 集成电极取代手工导电丝
- 电极间开窄槽增加柔性和灵敏度
- 底层 FPC 加支撑梁和 0.2mm 聚酰亚胺加强筋
- 使用桌面切割机（Silhouette Cameo 5）批量制造

**读出板设计**：
- Arduino Nano 作为 MCU
- 多路复用器（CD74HC4067M96）+ 移位寄存器（SN74HC595NSR）
- 0.5mm FFC 连接器
- 通过串口以 100Hz 输出同步触觉数据
- 向下兼容低分辨率传感器垫

**成本**（30 单位批次）：
| 组件 | 成本 |
|------|------|
| FPC 对（传感器垫） | $3.55 |
| 读出板 PCB | $3.10 |
| Arduino Nano | ~$25 |
| **总计** | **~$30** |

1000 单位批次：FPC 对降至 $1.36，PCB 降至 $2.61。

### 系统级集成

**3D 视触觉融合**（3D-ViTac 管线）：
- 多视角 RGB-D 重建 3D 视觉点云
- 触觉信号通过正运动学转换为 3D 触觉点（每个 taxel 的 3D 位置 + 触觉强度作为特征通道）
- 合并视觉和触觉点云为统一 3D 表示，加入模态指示器
- 使用 Diffusion Policy 进行动作生成

**跨具身技能迁移**（Touch in the Wild 管线）：
- 便携式人类数据采集设备：鱼眼相机 + FlexiTac 垫 + 紧凑读出板
- xArm 机器人平台：FlexiTac 装配的夹爪
- 共享触觉接口，保持跨具身的信号一致性

**Real-to-Sim-to-Real 训练**（VT-refine 管线）：
- GPU 并行触觉仿真：每个触觉垫建模为密集的 taxel 接触点集
- 查询 SDF 计算每个 taxel 的穿透深度和法向速度
- Kelvin-Voigt 惩罚模型（线性弹簧 + 粘性阻尼器）
- **省略剪切力**以降低建模复杂度
- 触觉标定：仅调节法向刚度 k_n 和阻尼 k_d
- 统一归一化规则（含噪声底阈值）


## Experiments

**说明**：本文是系统/硬件论文，未提供传统定量实验表格。实验验证以多平台部署展示为主。

**部署平台展示**（Fig. 1）：
1. xArm + 透明管操控
2. ALOHA + 烧杯和滴管操控
3. LeRobot FlexiTac 平台
4. 半人形机器人
5. 便携式触觉夹爪
6. Franka + 触觉皮肤
7. 触觉手套
8. Dexmate 机器人 + 笔操控

**传感器配置变体**：
- 12×32（标准指尖垫）
- 8×16、16×16（紧凑型）
- 32×32（大型触觉垫）

**关键定量数据**：
- 读出频率：100 Hz
- 传感器垫制造时间：~5 分钟/垫
- 电极间距：2mm
- 总厚度：<1mm
- 单元成本：~$30

**缺失证据**（明确标注）：
- 未报告传感器精度、灵敏度、迟滞等定量性能指标
- 未报告与现有触觉传感器（如 GelSight、ReSkin）的对比实验
- 未报告学习管线的定量成功率或性能数据（引用了 3D-ViTac、Touch in the Wild、VT-refine 等已发表工作）
- 未报告传感器长期耐用性数据


## Limitations

1. **感知模态有限**：压阻式传感器仅捕获压力信号，无法感知振动、温度或纹理
2. **仿真简化**：省略剪切力建模，仅模拟法向力和穿透深度
3. **无定量性能对比**：作为系统论文，未提供与竞品的性能基准对比
4. **传感器线性范围有限**：仅在典型操控负载下近似线性
5. **Arduino 成本占比高**：MCU 模块占 ~$25/总 $30，可通过集成 PCB 进一步降低
6. **缺乏长期耐久性验证**：未报告传感器在长期使用中的信号衰减或故障率


## Key Takeaways

1. **对 DLO 操控的潜在价值**：FlexiTac 的薄型柔性设计（<1mm）可贴合在 DLO 操控夹爪表面，提供接触压力分布反馈，有助于检测 DLO（如线缆、绳索）的滑动和接触位置
2. **Real-to-Sim-to-Real 管线的启示**：压阻式传感器的一维压力信号比光学触觉传感器的高维图像更容易仿真，使 Sim-to-Real 对齐更可行；Kelvin-Voigt 惩罚模型 + 触觉标定的思路可直接应用于 DLO 操控的仿真训练
3. **跨具身迁移对 DLO 采集的意义**：便携式触觉采集设备可用于收集人类操作 DLO 时的触觉数据，再迁移到机器人执行
4. **3D 视触觉融合的通用性**：将触觉信号提升到 3D 空间并与视觉点云融合的方法，是一种模态无关的多模态融合范式，可扩展到 DLO 场景
5. **开源生态价值**：低成本（~$30）+ 完整开源设计文件降低了触觉感知的实验门槛，适合在双臂机器人 DLO 操控研究中快速集成和迭代

## 相关概念

- [[reinforcement-learning]]
- [[sim-to-real]]
- [[tactile-sensing]]
- [[grasping]]
- [[vision-language-model]]
- [[diffusion-model]]
- [[deformable-linear-object]]
- [[bimanual-manipulation]]

## 相关研究者

- [[huang-binghao|Huang, Binghao]]
- [[li-yunzhu|Li, Yunzhu]]
