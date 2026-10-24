---
title: "Long-horizon manipulation via trace-conditioned VLA planning"
tags: [manipulation, imitation, VLM, robot-learning, planning]
created: "2026-04-29"
updated: "2026-04-29"
type: "literature"
status: "done"
summary: "提出层次化框架 LoHo-Manip，通过独立的 VLM 任务管理器预测 progress-aware 剩余子任务序列和 2D visual trace，将长时序操控分解为反复的短时序 VLA 局部控制，实现隐式进度跟踪、重规划和失败恢复。"
authors: "Liu, Isabella; Cheng, An-Chieh; Yan, Rui; Chen, Geng; Qiu, Ri-Zhao et al."
year: "2026"
venue: "arXiv Preprint"
zotero_key: "QEEQS6J5"
---
## 摘要

Long-horizon（长时序） manipulation（操控） remains challenging for vision-language-action (VLA) policies: real tasks are multi-step, progress-dependent, and brittle to compounding execution errors. We present LoHo-Manip, a modular framework that scales short-horizon VLA execution to long-horizon（长时序） instruction following via a dedicated task-management VLM. The manager is decoupled from the executor and is invoked in a receding-horizon manner: given the current observation, it predicts a progress-aware remaining plan that combines (i) a subtask sequence with an explicit done + remaining split as lightweight language memory, and (ii) a visual trace -- a compact 2D keypoint trajectory prompt specifying where to go and what to approach next. The executor VLA is adapted to condition on the rendered trace, thereby turning long-horizon（长时序） decision-making into repeated local control by following the trace. Crucially, predicting the remaining plan at each step yields an implicit closed loop: failed steps persist in subsequent outputs, and traces update accordingly, enabling automatic continuation and replanning without hand-crafted recovery logic or brittle visual-history buffers. Extensive experiments spanning embodied planning, long-horizon（长时序） reasoning, trajectory prediction, and end-to-end（端到端） manipulation（操控） in simulation and on a real Franka robot demonstrate strong gains in long-horizon（长时序） success, robustness, and out-of-distribution generalization. Project page: https://www.liuisabella.com/LoHoManip

## 中文简述

提出基于视觉-语言的操控方法，具有泛化能力特点。

**研究方向**: 机器人操控、模仿学习、视觉-语言模型、机器人学习、运动规划

## 关键贡献

1. **LoHo-Manip 模块化框架**：将任务管理 VLM（Manager）与短时序 VLA 执行器（Executor）分离，Manager 可跨不同 VLA 复用。
2. **Receding-horizon 剩余规划预测**：Manager 在每步都从当前观测预测"已完成 + 剩余"子任务序列，实现隐式进度跟踪、隐式重规划和隐式失败恢复，无需手工设计的恢复逻辑。
3. **Visual trace 作为可执行 prompt**：将 2D 关键点轨迹渲染到观测上作为 Executor 的空间条件信号，将长时序决策转化为局部 trace-following 控制，提升 OOD 泛化能力。
## 结构化提取

- **Problem**: VLA 在长时序操控中面临累积误差脆弱性和模块性差两个核心问题；单次规划无法应对部分失败，紧耦合架构难以更换执行器
- **Method**: 层次化 Manager-VLM（Qwen3-VL）+ Executor-VLA（π0.5）框架；Manager 预测 progress-aware 剩余子任务序列 + 2D visual trace；receding-horizon 闭环执行；trace 渲染到观测上作为 Executor 空间条件信号
- **Tasks**: 长时序桌面操控（抓取-放置链、物体交互序列、隐式语言指令）
- **Sensors**: RGB 相机（top-view static + wrist-view on gripper），2× Intel RealSense
- **Robot Setup**: Franka 单臂机械臂，桌面环境，100 条遥操作演示训练
- **Metrics**: 任务成功率（LIBERO/VLABench/real-world）, BLEU（RoboVQA）, DFD/HD/RMSE（轨迹预测）, Intention Score / Progress Score（VLABench）
- **Limitations**: 2D trace 无法表达复杂 3D 交互；依赖精确 sub-task grounding；仅桌面单臂；真机演示数据量小（100 条）
- **Evidence Notes**:

  - LIBERO avg 97.5%（Long 子集 95.2%，显著高于 baseline 60-77%）
  - VLABench avg 0.39（vs π0.5 0.24，+62.5% 相对提升）
  - Real-world OOD 场景优于 π0.5 baseline
  - 跨 VLA 兼容性验证（StarVLA + Manager: 0.18→0.24）
  - Manager 推理开销约 19%（86s vs 72s 每集）
## 本地引用关系

- [[kim2024openvla]]
## 证据元数据

- Fulltext Quality: fulltext (arXiv HTML)
- Evidence Coverage: 完整覆盖摘要、方法、实验（4个benchmark + real-world + ablation）、相关工作、结论、附录
- Confidence: high
- Summary: 提出层次化框架 LoHo-Manip，通过独立的 VLM 任务管理器预测 progress-aware 剩余子任务序列和 2D visual trace，将长时序操控分解为反复的短时序 VLA 局部控制，实现隐式进度跟踪、重规划和失败恢复。


## Problem

VLA 模型在短时序操控（抓取、放置、推）上已取得显著进展，但长时序操控仍面临两个核心挑战：

1. **累积误差下的脆弱性**：长序列放大小误差，单次规划无法可靠应对部分失败、遮挡或物体移动（drift 问题）。
2. **模块性差**：将规划与执行紧耦合在单一模型中（monolithic VLA），更换执行器（如不同机器人、动作空间）需要重新设计整个系统。

根本问题：长时序操控需要**任务管理**（分解、进度跟踪、持续重评估），而不仅仅是低层控制。


## Method

### 系统架构（两层分离）

**Manager（任务管理 VLM）**
- 初始化：Qwen3-VL（冻结视觉编码器，微调语言模型）
- 输入：自然语言指令 x + 当前观测 o_t + 文本进度摘要 C_{t-1}
- 输出：
  - (a) Progress-aware plan text：C_t（已完成子任务）+ R_t（剩余子任务）
  - (b) Visual trace τ_t：剩余执行路径的 2D 关键点序列
- 设计为通用模块，不依赖具体 Executor，可换接不同 VLA

**Executor（VLA 执行器）**
- 架构：π0.5（Physical Intelligence）
- 训练：在渲染了 trace prompt 的观测上微调，学会跟随轨迹执行短时序子任务
- 也验证了与 StarVLA 的兼容性

### Visual Trace 表示
- 从末端执行器 2D 像素坐标提取：τ_t* = {p_t, p_{t+1}, ..., p_{t_K^e}}
- 存储为紧凑的 waypoints 序列，归一化到 [0, 1000] 范围
- 渲染到观测图像上作为视觉 prompt

### Progress-Aware Plan
- 原子交互原语序列 S̄ = [s̄^(1), ..., s̄^(K)]
- 每步维护：C_t*（已完成前缀）+ R_t*（剩余后缀）
- C_t 作为轻量级文本记忆，替代长视觉历史

### Receding-Horizon 闭环执行
- Manager 每约 100 步 Executor 步骤调用一次
- 始终从当前观测预测剩余规划
- 失败步骤自动保留在后续输出中，trace 随之更新
- 无需手工失败检测器或特殊恢复逻辑

### 训练数据
- Bridge subset（Open X-Embodiment 格式）：真实机器人演示视频 → 提取原子交互原语 + 末端执行器 trace
- RoboVQA + EgoPlan-BenchIT：辅助长时序推理/规划数据
- 合成失败恢复样本：从 Bridge 数据集中筛选抓取-放置片段，用场景中其他可抓取物体替换原始抓取对象生成"假"失败数据

### 数据管线
- 时序分割：利用 VLM 视频理解能力识别物理交互事件及其时间跨度
- Trace 提取：逐帧定位末端执行器 → 像素坐标 → 归一化 → 重采样


## Experiments

### 3.1 Embodied Reasoning & Trajectory Prediction

**RoboVQA（长时序推理）**：LoHo-Manip-4B avg BLEU **63.1**，超越所有开源模型和商业 API（Gemini-3.0-Flash 37.3, GPT-4V 26.8）

**EgoPlan-Bench2（人类级别规划）**：avg **56.7**，超越 Gemini-3.0-Flash（48.8）和 ThinkAct-7B（48.2）

**ShareRobot-T（2D 轨迹预测）**：DFD **0.2309**, HD **0.2058**, RMSE **0.1559**，均为最佳

**VABench-V（2D 轨迹预测）**：DFD **0.2123**, HD **0.1821**, RMSE **0.1469**，均为最佳

### 3.2 Embodied Agent（EmbodiedBench）

**EB-Alfred**：avg **0.38**（vs GPT-4o mini 0.24, Qwen3-VL-4B 0.19）
**EB-Habitat**：avg **0.38**（vs GPT-4o mini 0.33, Qwen3-VL-4B 0.30）

### 3.3 VLA in Simulation

**LIBERO（短时序基础能力）**：
- LoHo-Manip: avg **97.5%**（Spatial 98.0, Object 98.6, Goal 98.0, Long **95.2**）
- 对比：StarVLA 96.6, ThinkAct 84.4, π0-fast 85.5
- 特别在 Long 子集上从 60-77% 大幅提升到 95.2%

**VLABench（长时序推理泛化）**：
- LoHo-Manip: avg **0.39**（In-Dist 0.54, Cross-Cat 0.23, CommonSense 0.36, Semantic 0.42, UnseenTexture 0.39）
- 对比：π0.5 0.24, π0-fast 0.22

### 3.4 Real-World（Franka 真机）

- 硬件：Franka 单臂 + 2× Intel RealSense（top-view static + wrist-view）
- 训练数据：100 条遥操作演示
- 评估：单步 OOD（未见物体类别）+ 多步 OOD（新空间布局 + 未见语言组合）
- 结果：显著优于同数据量微调的 π0.5 baseline，OOD 场景下 Manager 提供的语义规划和 trace grounding 对泛化至关重要

### Ablation

**Sub-task & Trace 数据管线**（Tab. 6）：去除后 ShareRobot-T DFD 从 0.2309→0.2437，VABench-V DFD 从 0.2123→0.2500

**不同 VLA Executor 兼容性**（Tab. 7）：StarVLA + LoHo-Manip Manager 从 avg 0.18→0.24，验证模块化设计

**推理效率**（Tab. 8）：Manager ~2Hz, Executor ~10Hz（A6000 GPU），带 Manager 每集 ~86s vs 不带 ~72s，开销约 19%


## Limitations

1. **依赖精确的 sub-task grounding 和 trace prediction**：虽然 receding-horizon 设计允许适应执行偏差，但感知和空间 grounding 的改进可进一步提升管线稳定性。
2. **Visual trace 仅 2D**：当前 2D 轨迹表示无法充分表达高精度操控或接触丰富行为中的复杂交互模式。
3. **仅限桌面单臂场景**：实验集中在单臂桌面操控，未验证多臂、移动操作或动态环境。
4. **真机数据量小**：仅 100 条演示，泛化能力受限于演示覆盖的场景多样性。


## Key Takeaways

1. **层次化分解是长时序操控的有效范式**：Manager-Executor 分离将复杂的长期规划问题简化为反复的短时序控制，与 DLO 操控中分解长时序任务（定位 → 抓取 → 变形 → 放置）的思路一致。
2. **Visual trace 作为中间表示**：2D 轨迹 prompt 是一种简洁有效的 Manager→Executor 接口，但 2D 表示对 DLO 这类需要 3D 理解的操控可能不足，值得探索 3D trace 扩展。
3. **Receding-horizon 剩余规划**：隐式恢复机制避免了手工失败检测器，对 DLO 操控中常见的抓取失败、线缆滑落等场景有参考价值。
4. **模块化设计的泛化优势**：Manager 不依赖特定 Executor，意味着可以在保留高层规划能力的同时更换底层策略——对双臂 DLO 场景，可复用 Manager 的任务分解能力而只需训练专门的 DLO 执行器。
5. **失败恢复数据增强**：通过替换场景物体合成"假"失败数据的方法简单有效，值得借鉴用于 DLO 操控训练数据的多样性增强。

## 相关概念

- [[robotic-manipulation]]
- [[imitation-learning]]
- [[vision-language-model]]
- [[robot-learning]]
- [[planning]]
- [[deformable-linear-object]]
- [[bimanual-manipulation]]
- [[grasping]]

## 相关研究者

- [[liu-isabella|Liu, Isabella]]
