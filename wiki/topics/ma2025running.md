---
title: "Running VLAs at real-time speed"
tags: [manipulation, VLM, robot-learning, grasping]
created: "2026-04-27"
updated: "2026-04-27"
type: "literature"
status: "done"
summary: "通过 CUDA Graph + 计算图简化 + Triton 核优化，将 π₀ VLA 推理从 106.5ms 降至 27.3ms（双视角 RTX 4090），突破 30FPS 门槛。提出 Full Streaming 三频率闭环架构（力 480Hz/视觉 30Hz/文本 <1Hz）。落下笔抓取 100% 成功率验证系统延迟。"
authors: "Ma, Yunchao; Zhou, Yizhuang; Yang, Yunhuan; Wang, Tiancai; Fan, Haoqiang"
year: "2025"
venue: "arXiv Preprint"
zotero_key: "I5Y9MWDB"
---
## 摘要

In this paper, we show how to run pi0-level multi-view VLA at 30Hz frame rate and at most 480Hz trajectory frequency using a single consumer GPU. This enables dynamic and real-time tasks that were previously believed to be unattainable by large VLA models. To achieve it, we introduce a bag of strategies to eliminate the overheads in model inference. The real-world experiment shows that the pi0 policy with our strategy achieves a 100% success rate in grasping（抓取） a falling pen task. Based on the results, we further propose a full streaming inference framework for real-time robot control of VLA. Code is available at https://github.com/Dexmal/realtime-vla.

## 中文简述

通过 CUDA Graph 消除 CPU 开销、计算图简化（RMS Norm/QKV/Action-Time 融合）、Triton GEMM tile 调优与标量运算融合，将 π₀ VLA（3B 参数）推理从 106.5ms 降至 27.3ms（双视角 RTX 4090），首次突破 30FPS 实时门槛。进一步提出 Full Streaming Inference 三频率闭环架构（力控 480Hz / 视觉 30Hz / 文本 <1Hz），利用 VLM compute-bound 与 AE IO-bound 的互补性实现并行流式推理。落下笔抓取 100% 成功率验证端到端延迟 <200ms。

**研究方向**: VLA 推理优化、实时控制、CUDA 工程优化

## 关键贡献

1. **逐步推理优化管线**：从朴素 PyTorch 105ms → CUDA Graph → 计算图简化 → Triton 核优化 → 双视角 27.3ms，突破 30FPS 门槛
2. **Full Streaming Inference 框架**：提出三频率闭环架构（力控 480Hz / 视觉 30Hz / 文本 <1Hz），将 VLA 的 VLM 和 Action Expert 并行流式运行
3. **真实世界验证**：落下笔抓取任务 100% 成功率（10/10），端到端反应时间 <200ms，与人类相当
## 结构化提取

- **Problem**: VLA 模型（如 π₀ 3B）推理延迟通常 >100ms，无法满足 30FPS 实时控制需求，导致丢帧和反应延迟，使得动态任务（如抓取移动物体）无法执行。
- **Method**: 逐步推理优化管线（CUDA Graph 消除 CPU 开销 → 计算图简化（RMS norm/QKV/action-time 融合）→ Triton GEMM tile 调优 → gated linear 融合 → 标量运算融合）+ Full Streaming Inference 框架（VLM compute-bound 与 AE IO-bound 并行，三频率闭环：力控 480Hz / 视觉 30Hz / 文本 <1Hz）。
- **Tasks**: 落下笔抓取（上方 grabber 释放笔 → 下方 grabber 在正确时刻闭合抓住）。
- **Sensors**: 30FPS 720P USB 摄像头（单/双/三视角），延迟约 2 帧；提议使用力传感器（>2KHz）/ 电机电流 / 触觉信号作为 AE 高频输入。
- **Robot Setup**: 两个垂直对齐定制 grabber + USB 摄像头，推理硬件 RTX 4090 单卡。
- **Metrics**: 推理延迟（ms）、成功率（%）、帧率（FPS）、距 roofline 下界剩余优化空间。
- **Limitations**: 实验任务过于简单（落下笔抓取仅需判断闭合时刻，作者自承 LeNet/SVM 即可完成）；Full Streaming 480Hz 力控环仅为框架提案未实现；优化针对 RTX 4090 特定硬件；未探索量化；无多任务泛化验证；摄像头延迟（~66ms）仍是系统瓶颈。
- **Evidence Notes**: 推理优化有详细定量分解表（Tab. 1-3, Fig. 2），从 105ms → 27.3ms 的每一步加速量和下界分析可信。落下笔抓取 100% 成功率（10/10）验证了系统延迟而非策略能力。Full Streaming 框架仅有概念验证测量（并行 VLM+16AE 32.7ms），实际 480Hz 力控环未实现。整体证据强度：推理优化部分强，真实实验部分中等（简单任务），Full Streaming 部分弱（仅提案）。
## 本地引用关系

- [[brohan2023rt2]]
- [[do2025watch]]
- [[kim2024openvla]]
- [[röfer2025pseudotouch]]
- [[zhao2025polytouch]]
## 证据元数据

- **Zotero Key**: I5Y9MWDB
- **Citekey**: ma2025running
- **Authors**: Ma Yunchao, Zhou Yizhuang, Yang Yunhuan, Wang Tiancai, Fan Haoqiang
- **Affiliation**: Dexmal + StepFun
- **Venue**: arXiv preprint, 2025-10
- **Paper Type**: System/Engineering paper (inference optimization)
- **Fulltext Quality**: Complete, 11 pages with detailed performance tables and computation flow diagrams
- **Evidence Coverage**: High for inference optimization (quantitative breakdown per kernel); Medium for real-world validation (simple task only); Low for Full Streaming framework (proposal only)
- **Confidence**: High on optimization results (reproducible numbers); Medium on real-world applicability (limited task complexity)
- **Summary**: 通过 CUDA Graph + 计算图简化 + Triton 核优化，将 π₀ VLA 推理从 106.5ms 降至 27.3ms（双视角 RTX 4090），突破 30FPS 门槛。提出 Full Streaming 三频率闭环架构（力 480Hz/视觉 30Hz/文本 <1Hz）。落下笔抓取 100% 成功率验证系统延迟。


## Problem

VLA 模型（如 π₀，3B 参数）推理延迟通常为数百毫秒，无法满足实时控制需求（需 <33ms 即 30FPS）。具体问题：
- 朴素 PyTorch 实现：单视角 105ms，双视角 106.5ms
- OpenPI 官方 JAX 实现：单视角 43.8ms，双视角 53.7ms
- 均远超 30FPS 所需的 33ms 门槛，导致丢帧和反应延迟


## Method

### 3.1 CUDA Graph 消除 CPU 开销
- 将所有 CUDA 核记录为图，重放时纯 GPU 驱动，消除 Python 开销
- Transformer 模块无动态分支，天然适合 CUDA Graph
- **效果**：推理时间从 ~105ms 降至 ~43ms（约 2x 加速），消除主要 CPU 瓶颈

### 3.2 计算图简化（3 种变换）
1. **RMS Norm 融合**：将 RMS 归一化仿射参数吸收到后续线性层（线性运算可结合律）
2. **Action-Time Embedding 折叠**：将 action value 的两次线性投影合并为一次（无非线性中间层）；time step 编码仅有 10 个离散值，预计算后融合为 bias
3. **QKV 融合**：将 Q/K/V 三个独立矩阵合并为一个大矩阵，通过切片取回；RoPE 操作预计算权重并融合进矩阵乘法
- **效果**：减少 ~7-8ms

### 4.1 GEMM Tile 参数调优
- 使用 Triton 实现，手动调优 matmul 的 tile 策略（替代 cuBLAS 默认调度）
- LLM 最后一层仅传递 KV cache 给 AE，无需计算 features，额外节省 ~0.7ms
- **效果**：~1.5ms 节省

### 4.2 Gated Linear Layer 融合
- FFN 中的 gated up-projection：两个 matmul 可并行，且共享输入加载、合并写入
- **效果**：~1.7ms 节省

### 4.3 Partial Split-k
- 针对特殊 GEMM 尺寸 512×1152×1152（144 blocks 不整除 128 SMs）
- 拆为 512×1152×1024 + 512×1152×128，分别用不同 tile 配置均匀分配到 SMs
- **效果**：<0.1ms（理论意义大于实际）

### 4.4 标量运算融合
- bias、residual shortcut、activation 合并进 GEMM
- RMS norm：先计算 token 级统计量到独立 buffer，在下一次 GEMM 的累加后除以对应因子
- **效果**：~4ms 节省

### 5. 下界分析（Roofline Model）
- RTX 4090：HBM 带宽 1.01 TB/s，BF16 MAC 91.4 TMAC/s
- 各模块 roofline：Vision Encoder 2.485ms / LLM 10.727ms / AE 6.486ms
- 总下界（双视角）：19.7ms + 同步开销 0.86ms = 20.6ms
- 实际 27.3ms vs 下界 20.6ms → 距最优仅剩 ~30% 优化空间

### 6. Full Streaming Inference 框架
- **核心洞察**：VLM 是 compute-bound，AE 是 IO-bound → 并行运行可同时充分利用 IO 和计算资源
- **三频率闭环**：
  - **力控环 480Hz**：高频传感器（力/触觉/电机电流）→ AE → 轨迹缓冲区，单次 AE ~2ms
  - **视觉环 30Hz**：图像帧 → VLM → KV Cache → AE，最低 1/30s 反应
  - **文本环 <1Hz**：文本推理与视觉编码"搭便车"，30 token/s 用于交互或 CoT
- AE 的 flow matching 改写为"渐进式"生成（类似 auto-regressive），每步生成部分动作列表
- 提出 Persistent Megakernel 实现方案（细节留后续工作）


## Experiments

### 真实世界实验：落下笔抓取
- **硬件**：两个垂直对齐的定制 grabber + 30FPS 720P USB 摄像头 + RTX 4090
- **任务**：上方 grabber 释放笔 → 下方 grabber 在正确时刻闭合抓住笔
- **时序约束**：grabber 开/闭需 60ms（~2 帧）；笔下落约 30cm；人类类似任务下落 30cm 是反应下限
- **数据**：600 episodes 自动采集（闭合约在释放后 200ms）
- **训练**：使用 OpenPI 官方仓库训练，空 prompt，few epochs
- **推理**：多线程（camera thread / inference thread / grabber thread），ring buffer 管理帧和输出
- **结果**：10 连续实验 **100% 成功率**
- **端到端延迟**：摄像头延迟 ~2 帧 + 推理 27.3ms + grabber 60ms ≈ <200ms

### 性能分解表（双视角，RTX 4090）
| 阶段 | naive PyTorch | +CUDA Graph | +简化图 | +优化核 | Roofline 下界 |
|------|--------------|-------------|---------|---------|--------------|
| 总计 | 106.5ms | ~53ms | ~45ms | 27.3ms | 20.6ms |

### 并行流式推理
| 条件 | 时间 |
|------|------|
| 串行 VLM + 10 AE | 27.3ms |
| 并行 VLM + 10 AE | 26.3ms |
| 并行 VLM + 16 AE | 32.7ms（恰好在 1/30s 边界内） |


## Limitations

1. **实验过于简单**：落下笔抓取仅需判断"何时闭合"，任务复杂度极低。作者自承"从学习角度看这是 trivial 的，用 LeNet 或 SVM 都能做到"。核心价值是系统延迟验证而非策略学习能力。
2. **Full Streaming Inference 仅是框架提案**：480Hz 力控环、文本推理融合、Persistent Megakernel 等均未实现，留作 future work。
3. **单消费级 GPU 依赖**：所有优化针对 RTX 4090（128 SMs、1.01 TB/s），迁移到其他硬件需重新调优 tile 参数。
4. **量化未探索**：BF16 精度，未尝试 INT8/FP8 量化，作者指出这可能是进一步提升的方向。
5. **无多任务泛化验证**：仅验证单一任务，未测试优化后模型在多任务/长时序场景的表现。
6. **摄像头延迟是瓶颈**：USB 摄像头 ~2 帧延迟（~66ms），RealSense >100ms。即使推理达到 30FPS，传感器延迟仍是系统瓶颈。


## Key Takeaways

1. **VLA 推理速度的根本瓶颈是工程而非算法**：通过 CUDA Graph + 计算图简化 + Triton 核优化，3B 参数的 π₀ 可在单 GPU 上达 30FPS，无需模型压缩或蒸馏。这对 [[brohan2023rt2]]（1-3Hz）和 [[kim2024openvla]]（~6Hz）的控制频率瓶颈问题给出了工程解决方案。
2. **VLM 和 AE 的 compute/IO 互补性**是 Full Streaming 的理论基础：VLM compute-bound + AE IO-bound → 并行运行可同时利用硬件资源。这个洞察对未来 VLA 系统设计有重要价值。
3. **三频率闭环架构**（力 480Hz / 视觉 30Hz / 文本 <1Hz）是 VLA 部署的新范式，将 VLA 从"中频控制层"升级为"全频控制方案"。特别是 480Hz 力控环若实现，可触达实时力控门槛。
4. **对本研究方向的启示**：双臂 DLO 操控需要高频力反馈控制来维持张力，Full Streaming 的 480Hz 力控环若与触觉传感器结合，可能是解决 DLO 张力控制的新路径。

## 相关概念

- [[robotic-manipulation]]
- [[vision-language-model]]
- [[robot-learning]]
- [[grasping]]
- [[deformable-linear-object]]
- [[bimanual-manipulation]]

## 相关研究者

- [[ma|Ma, Yunchao]]
