---
title: "RIO: Flexible real-time robot I/O for cross-embodiment robot learning"
tags: [imitation, VLM, robot-learning, bimanual, grasping]
created: "2026-05-16"
updated: "2026-05-16"
type: "literature"
status: "done"
summary: "提出 RIO 开源 Python 框架，通过 middleware-agnostic 的 Node 抽象实现跨构型（单臂/双臂/人形）机器人遥操作、数据采集和策略部署，端到端延迟 130ms（LeRobot 581ms），在 4 个硬件平台上验证 π0.5、GR00T、Diffusion Policy 和 RL-PPO 部署。"
authors: "Ortega-Kral, Pablo; Xing, Eliot; Bucker, Arthur; Luk, Vernon; Kim, Junseo et al."
year: "2026"
venue: "arXiv Preprint"
zotero_key: "ZG57S8UP"
---
## 摘要

Despite recent efforts to collect multi-task（多任务）, multi-embodiment（具身） datasets, to design recipes for training Vision-Language-Action models (VLAs), and to showcase these models on different robot platforms, generalist cross-embodiment（具身） robot capabilities remains a largely elusive ideal. Progress is limited by fragmented infrastructure: most robot code is highly specific to the exact setup the user decided on, which adds major overhead when attempting to reuse, recycle, or share artifacts between users. We present RIO (Robot I/O), an open source Python framework that provides flexible, lightweight components for robot control, teleoperation, data formatting, sensor configuration, and policy deployment across diverse hardware platforms and morphologies. RIO provides abstractions that enable users to make any choice and to switch between them, with minimal reconfiguration effort. We validate RIO on VLA deployment workflows across three morphologies (single-arm, bimanual（双臂）, humanoid) and four hardware platforms with varying grippers and cameras. Using teleoperated data collected with RIO, we fine-tune state-of-the-art（现有最优方法） VLAs including $π_{0.5}$ and GR00T on household tasks such as pick-and-place, folding, and bowl scrubbing. By open sourcing all our efforts, we hope the community can accelerate their pace of robot learning on real-world robot hardware. Additional details at: https://robot-i-o.github.io

## 中文简述

提出基于视觉-语言的双臂方法，具有多任务特点。

**研究方向**: 模仿学习、视觉-语言模型、机器人学习、双臂操控、抓取

## 关键贡献

1. **RIO 框架**：开源 Python 框架，提供 middleware-agnostic 的 Node 抽象（Server-Client 对），支持 Shared Memory / Thread / Zenoh / ZeroRpc / Portal 五种中间件，用户可在每一层（机器人、夹爪、相机、遥操作设备、数据格式、策略）自由选择并切换，仅需修改配置文件。
2. **跨构型验证**：在 3 种构型（单臂、双臂、人形）和 4 个硬件平台（xArm7、SO-100、Unitree G1、Booster T1）上完成从遥操作数据采集到策略微调再到部署的完整工作流。
3. **VLA 真实部署**：使用 RIO 采集的遥操作数据微调 π0.5 和 GR00T N1.5，在家庭任务（折叠衬衫、放罐头、折叠布料、擦碗、抓盒子）上达到 60%–95% 成功率；另部署 Diffusion Policy（翻饼、抛球）和 RL-PPO（人形导航）。
4. **性能优势**：端到端观测-动作延迟 130.3ms，对比 LeRobot 的 581.2ms，提升约 4.5 倍。
## 结构化提取

- **Problem**: 机器人学习基础设施碎片化，跨平台代码复用和数据共享成本高
- **Method**: Middleware-agnostic Node 抽象 + 可组合 Station 配置 + 异步策略推理 + 标准化 RLDS 数据格式
- **Tasks**: 折叠衬衫、放罐头、折叠布料、擦碗、抓盒子、翻饼、抛球、人形导航
- **Sensors**: RealSense D415/D405/D400、ZED、UVC 摄像头、iPhone (Record3D)
- **Robot Setup**: xArm7 (单臂) + Robotiq 2F-140、SO-100 (双臂) + ALOHA/GELLO、Unitree G1 (人形)、Booster T1 (人形)
- **Metrics**: 成功率 (20 trials)、任务完成时间 vs 演示时间、端到端延迟、GPU 利用率、Middleware 延迟
- **Limitations**: 仅单构型微调验证；动态任务 VLA 未验证；无移动操作和灵巧手支持；跨构型性能下降是开放问题
- **Evidence Notes**: 所有实验数据来自真实机器人部署，无仿真结果（除 RL-PPO 的仿真训练）。跨构型实验明确标注性能下降并归因为开放研究问题。新机器人 onboard 使用 coding agent 完成，9.2 分钟软件集成，有可复现的定量指标。
## 本地引用关系

-
## 证据元数据

- Fulltext Quality: fulltext
- Evidence Coverage: complete（全文可获取，实验数据、架构细节、附录代码均已覆盖）
- Confidence: high
- Summary: 提出 RIO 开源 Python 框架，通过 middleware-agnostic 的 Node 抽象实现跨构型（单臂/双臂/人形）机器人遥操作、数据采集和策略部署，端到端延迟 130ms（LeRobot 581ms），在 4 个硬件平台上验证 π0.5、GR00T、Diffusion Policy 和 RL-PPO 部署。


## Problem

机器人学习领域面临严重的**基础设施碎片化**问题：大多数机器人代码高度绑定特定硬件配置，导致跨平台复用、数据共享和策略迁移成本极高。具体表现为：
1. 现有 VLA checkpoint 通常绑定特定机器人平台（如 DROID 的 Franka、BridgeData V2 的 WidowX），用户要么一比一复现硬件，要么从零重写整个控制栈。
2. 跨构型数据集（如 Open X-Embodiment）在实践中是多个独立采集的聚合，数据格式和传感器配置各异，需要大量清洗工作。
3. 现有框架（如 ROS）虽然支持分布式通信，但构建系统复杂、学习曲线陡峭；LeRobot 虽然降低了门槛，但在多构型灵活性方面仍有不足。


## Method

### 核心架构
- **Node 抽象**：所有硬件组件（机器人、相机、遥操作设备、策略）均实现为 Node，动态继承自指定 Middleware。Node 支持 pub-only / req-only / combined 三种执行模式，通过 ring_buffer 发布状态、request_queue 接收命令。Factory 函数自动生成匹配的 Server-Client 对。
- **Middleware 层**：隐藏传输层细节。Zenoh 和 Shared Memory 达到亚毫秒级延迟（0.43ms / 0.54ms），Thread 和 ZeroRpc 约 1ms，Portal 约 2ms 但支持分布式多机。
- **Robot Station**：可组合的 dataclass 配置，描述硬件拓扑（如 `{arm, gripper, arm2, gripper2, wrist_camera, wrist_camera2}`），上下文管理器自动初始化所有 Server Node。

### 数据采集
- 强制标准化单位（米、弧度），RLDS 格式，Morphology 抽象定义各构型的观测键。
- 使用 RoboDM 压缩存储（150 个三相机 episode 仅占 1.31 GB）。
- 遥操作支持三种脚本：相对末端执行器位姿（Keyboard/Spacemouse/Gamepad/Phone）、绝对关节映射（GELLO leader-follower）、VR 腕部位姿重定向（人形上半身）。

### 策略推理
- 异步推理 Node 直接通过 middleware 处理推理请求，无需额外策略服务器。
- 支持动作分块（action chunking），主循环非阻塞，精确计时。
- 策略 API 仅需实现：实例化 → 标准化观测到策略格式转换 → 推理。

### 形态学抽象
- Embodiment 基类提供 `reset()` / `step()` / `get_state()` Gym 风格接口。
- SingleArm / Bimanual / Humanoid 子类定义各自观测 schema。


## Experiments

### 硬件配置
- GPU: NVIDIA RTX 4090, CPU: AMD Ryzen 7 5700X, RAM: 64 GB
- 单臂: UFactory xArm7 + Robotiq 2F-140 + 3x RealSense D400
- 双臂: SO-100 + ALOHA/GELLO 遥操作
- 人形: Unitree G1, Booster T1

### 主要结果（Table III）

| 机器人 | 策略 | 任务 | 成功率 | 完成时间(s) | 演示时间(s) |
|--------|------|------|--------|-------------|-------------|
| xArm7 | π0.5 | 折叠衬衫 | 92.5% | 41.96±14.58 | 41.57±9.25 |
| xArm7 | π0.5 | 放罐头 | 95.0% | 16.08±3.41 | 14.46±2.00 |
| SO-100 | π0.5 | 折叠布料 | 60.0% | 27.50±5.51 | 22.43±3.30 |
| SO-100 | π0.5 | 擦碗 | 64.0% | 40.33±13.68 | 27.66±5.22 |
| Unitree G1 | GR00T N1.5 | 抓盒子 | 95.0% | 9.07±6.10 | 10.38±4.04 |
| xArm7 | Diffusion Policy | 翻饼 | 66.7% | 12.36±2.57 | 7.59±0.79 |
| xArm7 | Diffusion Policy | 抛球 | 100.0% | 14.73±1.28 | 13.26±2.23 |
| Unitree G1 | RL-PPO | 导航 | 100.0% | 31.27±6.56 | N/A |
| Booster T1 | RL-PPO | 导航 | 100.0% | 29.73±4.49 | N/A |

每个任务 20 次试验，VLA 使用 50 演示微调。

### 跨构型微调（Table V）
- 混合 xArm7 + SO-100 数据训练单 checkpoint
- 双臂 (SO-100) 折叠: 60.0%，单臂 (xArm7) 折叠: 70.0%
- 性能下降，作者指出这是开放研究问题而非框架局限

### 延迟对比（Figure 6）
- RIO 端到端: 130.3ms
- LeRobot 端到端: 581.2ms
- 原因：RIO 直接利用 middleware 做异步推理，而 LeRobot 通过网络向独立策略服务器传输

### Middleware 延迟（Table IV, 2048B payload, 1000 pass）
| Middleware | 延迟 (ms) |
|------------|-----------|
| Zenoh | 0.43±0.13 |
| Shared Memory | 0.54±0.62 |
| Thread | 0.99±0.30 |
| ZeroRpc | 1.05±0.17 |

### 新机器人 onboard 实验
- 使用 Claude Code (Opus 4.6) 将 AgileX PiPER 臂集成到 RIO
- 软件部分: 9.2 分钟，420 行代码，3 个文件，零人工干预
- 物理硬件设置（CAN 总线接线、安装）约 40 分钟


## Limitations

1. **仅验证单构型微调**：跨构型微调的性能下降显著（Table V），作者承认跨构型泛化仍是开放研究问题。
2. **动态任务的 VLA 可靠性未充分验证**：动态任务（翻饼、抛球）仅使用 Diffusion Policy，VLA 在动态任务上的表现未报告。
3. **缺乏系统性的分布偏移基准测试**：未量化不同构型间的 sim-to-real 或 cross-embodiment 分布偏移。
4. **硬件覆盖有限**：不支持移动操作平台和多指灵巧手。
5. **训练栈由用户自带**：RIO 只负责数据采集和部署，不提供训练管线，用户仍需自行处理训练格式转换。
6. **双臂任务策略完成时间显著长于演示时间**（平均多 8.87s），作者归因于策略重试行为而非系统开销。


## Key Takeaways

1. **工程基础设施是机器人学习的关键瓶颈**：与 CV/NLP 领域的标准化框架（PyTorch、HuggingFace）不同，机器人领域缺少可复用的硬件抽象层。RIO 试图填补这一空白。
2. **Middleware-agnostic 设计是核心创新**：通过动态继承实现的 middleware 切换，使得同一套 Node 代码可在调试（Thread）、高性能（Shared Memory）、分布式（Zenoh）之间无缝切换。
3. **对 DLO 操控的启示**：RIO 的 Morphology 抽象和标准化观测 schema 可以直接扩展到 DLO 场景——只需定义新的 DLOManipulation morphology 和对应观测键。双臂 SO-100 的折布实验（60% 成功率）暗示 DLO 操控在通用 VLA 框架下仍有很大提升空间。
4. **异步推理的重要性**：130ms vs 581ms 的差异主要来自避免独立策略服务器的网络开销，直接在 middleware 层做异步推理。这对于需要高频控制的 DLO 操控尤为关键。
5. **跨构型学习仍是开放问题**：即使数据格式统一，跨构型策略的性能仍然下降，说明需要更好的构型不变表征。

## 相关概念

- [[imitation-learning]]
- [[vision-language-model]]
- [[robot-learning]]
- [[bimanual-manipulation]]
- [[grasping]]
- [[diffusion-model]]
- [[deformable-linear-object]]

## 相关研究者

- [[ortega-kral|Ortega-Kral, Pablo]]
