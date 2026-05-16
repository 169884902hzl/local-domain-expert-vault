---
title: "DiscreteRTC: Discrete diffusion policies are natural asynchronous executors"
tags: [manipulation, imitation, diffusion]
created: "2026-04-29"
updated: "2026-04-29"
type: "literature"
status: "done"
summary: "指出离散扩散策略的 native inpainting 特性使其天然适合异步执行，提出 DiscreteRTC 方法，无需额外 fine-tuning 即可在动态操控任务上超越 flow-matching RTC。"
authors: "Wang, Pengcheng; Hong, Kaiwen; Peng, Chensheng; Driggs-Campbell, Katherine; Tomizuka, Masayoshi et al."
year: "2026"
venue: "arXiv Preprint"
zotero_key: "GJWQ7M8E"
---
## 摘要

Unlike chatbots, physical AI must act while the world keeps evolving. Therefore, the inter-chunk pause of synchronous executors are fatal for dynamic tasks regardless of how fast the inference is. Asynchronous execution -- thinking while acting -- is therefore a structural requirement, and real-time chunking (RTC) makes it viable by recasting chunk transitions as inpainting: freezing committed actions and consistently generating the remainder. However, RTC with flow-matching policy is structurally suboptimal: its inpainting comes from inference-time corrections rather than the base policy, yielding little pre-training benefit, specific fine-tuning, heuristic guidance, and extra computation that inflates the latency. In this work, we observe that discrete diffusion（扩散） policies, which generate actions by iteratively unmasking, are natural asynchronous executors that resolve all limitations at once: they are fine-tuning free since inpainting is their native operation, while early stopping further provides adaptive guidance and reduces inference cost. We propose DiscreteRTC, which replaces external corrections with native unmasking, and show on dynamic simulated benchmarks and real-world dynamic manipulation（操控） tasks that it achieves higher success rates than continuous RTC and other baselines. In summary, DiscreteRTC is simpler to implement with 0 lines of code for async inpainting, faster at inference with only 0.7x computation compared with generating actions from scratch, and better at execution with 50% higher success rate in real-world dynamic pick task compared with flow-matching-based RTC. More visualizations are on https://outsider86.github.io/DiscreteRTCSite/.

## 中文简述

提出基于扩散模型的操控方法。

**研究方向**: 机器人操控、模仿学习、扩散模型

## 关键贡献

1. **系统分析 flow-matching RTC 的四大结构性缺陷**（Section 3），从预训练、fine-tuning、引导机制、推理成本四个维度论证其 suboptimality。
2. **发现离散扩散策略是天然异步执行器**：inpainting 是其原生操作（随机 mask 训练 = inpainting 训练），无需任何额外实现即可在推理时完成 chunk transition。
3. **提出 DiscreteRTC**：用离散扩散的 native unmasking 替代 flow-matching 的 ΠGDM correction，实现 0 行额外代码的异步 inpainting。
4. **Early stopping 自然引导机制**：推理可在满足最小条件时提前退出，保留部分 unmasked pattern 作为下一次推理的自适应引导。
5. **实验验证**：在 Kinetix 仿真 benchmark 和真实动态操控任务上超越 ContinuousRTC 及其他 baseline。
## 结构化提取

- **Problem**: Flow-matching 策略在 RTC 异步执行中存在结构性缺陷——预训练不覆盖 inpainting、需额外 fine-tuning、依赖启发式引导、推理成本翻倍。
- **Method**: 提出将异步 chunk transition 直接用离散扩散的 native unmasking 完成，无需额外 correction、fine-tuning 或 heuristic schedule；early stopping 提供自适应引导并降低推理成本。
- **Tasks**: 动态物体操控（Dynamic Pick / Dynamic Place），仿真 benchmark（Kinetix 12 个环境）。
- **Sensors**: Wrist-mounted RGB camera（真实），4-frame history + previous action（仿真）。
- **Robot Setup**: UR5e + Robotiq gripper，20Hz 控制频率，5x 线性插值产生 100Hz servo stream，RTX 4090 部署。
- **Metrics**: Success rate（20 trials/task），inference time (ms)，solve rate（仿真 2048 trials），throughput（每 256 steps 完成任务数）。
- **Limitations**: 朴素 bin 量化产生长 token 序列；模块化架构阻止 backbone 参与 unmasking；max-confidence 解码不产生隐式 AR 顺序。
- **Evidence Notes**:

  - Figure 4: 不同 inference delay 下 DiscreteRTC 一致优于 ContinuousRTC（Kinetix solve rate + throughput）。
  - Table 1: 真实 Dynamic Pick DiscreteRTC 75% vs ContinuousRTC 25%，推理 206ms vs 256ms。
  - Figure 8: Inpainting fine-tuning 反而一致降低 DiscreteRTC 性能，验证 fine-tuning-free。
  - Figure 5: DiscreteRTC 超越 Training-time Continuous RTC。
  - Appendix B.1: Max-confidence unmasking 不具备隐式 AR 顺序，限制 natural schedule 效果。
## 本地引用关系

-
## 证据元数据

- Fulltext Quality: fulltext
- Evidence Coverage: complete（含主文、附录、实验细节）
- Confidence: high
- Summary: 指出离散扩散策略的 native inpainting 特性使其天然适合异步执行，提出 DiscreteRTC 方法，无需额外 fine-tuning 即可在动态操控任务上超越 flow-matching RTC。


## Problem

Flow-matching 策略在 Real-Time Chunking (RTC) 异步执行框架中存在四个结构性缺陷：
1. **预训练不包含 inpainting**：flow-matching 训练时所有 action 以同一噪声水平被 corrupted，但 RTC 推理时 action chunk 具有不一致的噪声水平（committed prefix 为 0，新 action 为 1），scaling pre-training 不直接提升异步性能。
2. **需要额外 fine-tuning**：必须用 action-suffix conditioning 等技术显式引入 inpainting 训练模式。
3. **启发式引导**：ΠGDM 依赖手工设计的指数衰减 soft-masking 权重 schedule，跨场景固定不变。
4. **额外推理开销**：每步去噪需计算 vector-Jacobian product (VJP)，推理成本近乎翻倍。


## Method

### 核心思路
将异步执行中的 chunk transition 问题重新表述为离散扩散的 inpainting 问题。离散扩散策略的训练过程本身就是"给定部分 masked 序列，预测完整 action chunk"，因此 RTC 的 inpainting 需求与训练完全一致。

### 技术细节
- **Discrete Diffusion Policy**：将连续 action 通过 512-bin（仿真）或 256-bin（真实）量化为离散 token，用 iterative unmasking 生成 action chunk。
- **Inpainting = Forward Pass**：将上次 chunk 的 committed prefix tokens 直接放置，剩余部分用标准 forward pass unmasking，即 $\mathbf{A}_t^{k+1} = \pi(\mathbf{A}_t^k, \mathbf{o}_t)$，无任何额外 correction term。
- **Early Stopping**：只需确保 committed actions 之后的 $s$ 个 action 被完全 unmasked，其余可保持部分 masked 状态，自然传递给下一次推理作为引导信号。
- **推理效率**：unmasking 从中间状态开始、在中间阶段结束，每步需 unmask 的 token 数减少。总计算量约为从零生成的 ~0.7x（对比 ContinuousRTC 的 ~1.7x）。

### 网络架构
- **仿真（Kinetix）**：MLPMixer backbone + AdaLN，4 blocks，8 tokens（chunk 长度 H=8），channel dim 256。
- **真实机器人**：Qwen2.5-VL-3B-Instruct VLM + layerwise cross-attention DiT action head（36 blocks），256-bin 量化，16×10=160 tokens/chunk。


## Experiments

### 仿真：Kinetix Benchmark
- **Setup**：Kinetix-Symbolic-Continuous-v1，60Hz 物理 / 30Hz 控制，action 加 Gaussian noise (std=0.1)，4-frame history，H=8 chunk，5 denoising/unmasking steps。
- **Baselines**：Naive Async、Bidirectional Decoding (BID, N=16)、ContinuousRTC (ΠGDM)。
- **主要结果（Figure 4）**：
  - DiscreteRTC 在不同 inference delay 下一致优于 ContinuousRTC（solve rate 和 throughput）。
  - DiscreteRTC 所需 iterative steps 少于 ContinuousRTC，尤其在大 delay 时。
- **扩展结果（Figure 5）**：
  - DiscreteRTC 超越 Training-time Continuous RTC（需要专门 fine-tuning 的方法）。
  - DiscreteRTC + Fixed Steps 可用相同计算预算生成更细粒度 action。
  - 集成 VLASH 可在 varying delays 下更稳定，但小 delay 时有性能下降。
- **Inpainting Fine-tuning Ablation（Figure 8）**：对离散扩散策略做 inpainting-specific fine-tuning 反而一致降低性能，验证了 fine-tuning-free 的正确性。

### 真实机器人
- **Setup**：UR5e + Robotiq gripper + wrist RGB camera，20Hz 控制，RTX 4090，每任务 20 trials。
- **任务**：Dynamic Pick（拾取旋转平台上的运动物体）、Dynamic Place（放置物体到运动平台），转台 15-20 rpm。
- **Results（Table 1）**：

| Method | Dynamic Pick SR | Dynamic Place SR | Inference (ms) |
|--------|-----------------|------------------|----------------|
| Continuous Sync | 0% | 0% | 151 |
| Continuous RTC | 25% | 40% | 256 |
| Discrete Sync | 0% | 0% | 303 |
| DiscreteRTC | **75%** | **60%** | 206 |

- Sync baseline 全部失败（0%），验证异步执行的必要性。
- DiscreteRTC 在 Dynamic Pick 上比 ContinuousRTC 高 50% 成功率。
- ContinuousRTC 推理时间从 151→256ms（1.7x 开销），DiscreteRTC 从 303→206ms（减少）。

### Natural Schedule 消融（Appendix B.1）
- Max-confidence unmasking 不具备隐式 AR 顺序，倾向于在全 chunk 范围均匀分配 unmasking budget，导致 early stopping 的推理节省和 natural guidance 优势被抵消。
- 这激发了未来方向：设计 principled unmasking strategy（如 AR-block decoding）。


## Limitations

1. **朴素 k-bin 量化忽略时序结构**：产生过长的 token 序列，需要更紧凑、时序感知的 tokenizer（如 FAST、OAT）。
2. **模块化架构限制**：AR-VLM + discrete diffusion head 的分离设计阻止了 backbone 参与迭代 unmasking，需要 unified discrete diffusion VLA。
3. **Max-confidence unmasking 未充分发挥 natural schedule 潜力**：当前解码策略不产生隐式 AR 顺序，需要更合适的 unmasking 策略。


## Key Takeaways

1. **核心洞察**：离散扩散的训练过程（随机 mask + 预测完整序列）本身就是 inpainting 训练，因此无需任何额外设计即可支持异步执行。这一观察将 RTC 的 inpainting 问题从"推理时修正"转化为"训练时原生能力"。
2. **对 DLO 操控的启示**：DLO 操控是高度动态的任务，需要连续闭环控制。DiscreteRTC 的低延迟异步执行和 chunk 间连续性保障对 DLO 跟踪、绕障碍等动态场景有直接价值。
3. **对 VLM-based 控制的启示**：当前 SOTA VLA（π0, π0.5, Gr00t）均采用 flow-matching action head。DiscreteRTC 指出离散扩散 head 在异步执行场景下有结构性优势，这为 VLA 架构选型提供了新的视角。
4. **Scalability 优势**：由于 inpainting 是原生操作，scaling pre-training 直接提升异步性能，不需要额外的 fine-tuning pipeline，对大规模 VLA 训练有实际意义。

## 相关概念

- [[robotic-manipulation]]
- [[imitation-learning]]
- [[diffusion-model]]
- [[vision-language-model]]
- [[deformable-linear-object]]
- [[grasping]]

## 相关研究者

- [[wang-pengcheng|Wang, Pengcheng]]
- [[hong|Hong, Kaiwen]]
