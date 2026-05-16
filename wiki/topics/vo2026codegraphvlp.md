---
title: "CodeGraphVLP: Code-as-planner meets semantic-graph state for non-markovian vision-language-action models"
tags: [manipulation, VLM, planning]
created: "2026-04-29"
updated: "2026-04-29"
type: "literature"
status: "done"
summary: "提出层次化框架 CodeGraphVLP，通过持久化语义图状态 + LLM 合成的可执行代码规划器 + 去噪视觉语言提示，解决 VLA 模型在非马尔可夫长时序操控任务中的局限性，在真实桌面任务上显著优于 π0、π0.5、Gr00T N1.5 等 baseline。"
authors: "Vo, Khoa; Tran, Sieu; Hanyu, Taisei; Ikebe, Yuki; Nguyen, Duy et al."
year: "2026"
venue: "arXiv Preprint"
zotero_key: "NKPFHC62"
---
## 摘要

Vision-Language-Action (VLA) models promise generalist robot manipulation（机器人操控）, but are typically trained and deployed as short-horizon policies that assume the latest observation is sufficient for action reasoning. This assumption breaks in non-Markovian long-horizon（长时序） tasks, where task-relevant evidence can be occluded or appear only earlier in the trajectory, and where clutter and distractors make fine-grained visual grounding brittle. We present CodeGraphVLP, a hierarchical framework that enables reliable long-horizon（长时序） manipulation（操控） by combining a persistent semantic-graph state with an executable code-based planner and progress-guided visual-language prompting. The semantic-graph maintains task-relevant entities and relations under partial observability. The synthesized planner executes over this semantic-graph to perform efficient progress checks and outputs a subtask instruction together with subtask-relevant objects. We use these outputs to construct clutter-suppressed observations that focus the VLA executor on critical evidence. On real-world non-Markovian tasks, CodeGraphVLP improves task completion over strong VLA baselines and history-enabled variants while substantially lowering planning latency compared to VLM-in-the-loop planning. We also conduct extensive ablation studies to confirm the contributions of each component.

## 中文简述

提出基于视觉-语言的操控方法，具有长时序任务特点。

**研究方向**: 机器人操控、视觉-语言模型、运动规划

## 关键贡献

1. **CodeGraphVLP 框架**：首次将持久化语义图状态 + 可执行代码规划器 + 去噪视觉语言提示三者结合，实现非马尔可夫长时序操控
2. **代码规划器设计**：展示如何通过 LLM 一次性合成可在语义图上查询进度的可执行程序，避免在线 VLM 调用，输出子任务指令和子任务相关物体
3. **实验验证**：设计 3 个真实世界非马尔可夫桌面任务，系统优于强 baseline 且规划延迟大幅降低，消融实验量化各组件贡献
## 结构化提取

- Problem: VLA 模型的马尔可夫假设在非马尔可夫长时序操控任务中失效，现有记忆增强和层次化方案各有局限
- Method: 层次化框架 CodeGraphVLP，结合持久化语义图状态 + LLM 合成的可执行代码规划器 + 去噪视觉语言提示
- Tasks: 真实世界桌面操控——Pick-and-Place Twice（立方体往返）、Place-and-Stack（放入+叠放）、Swap Cups（三步交换杯子）
- Sensors: 双路 RGB 相机（固定过肩视角 + 腕部相机），10Hz；本体感知（关节状态）
- Robot Setup: UR10e 机械臂 + Robotiq 2F-85 平行夹爪，单臂桌面操控
- Metrics: 任务完成成功率（%），含部分完成里程碑；规划延迟（ms）；消融对比
- Limitations: 依赖基础模型能力；属性/关系推断对视角敏感；代码规划器需要精心 prompt 设计；未验证开放世界场景
- Evidence Notes: 全文覆盖 Method/Experiments/Limitations；Table I/II 精确数值未完整抓取，Swap Cups 上 CodeGraphVLP=85%，去除去噪提示降至 40%；π0 FAST 全任务失败
## 本地引用关系

-
## 证据元数据

- Fulltext Quality: partial（HTML 全文已获取，但 Table I/II/III 的精确数值单元格未完整抓取；部分数据从正文叙述中提取）
- Evidence Coverage: method 和实验设计覆盖充分；精确数值结果部分缺失
- Confidence: medium（方法细节明确，但部分表格数据需对照原文确认）
- Summary: 提出层次化框架 CodeGraphVLP，通过持久化语义图状态 + LLM 合成的可执行代码规划器 + 去噪视觉语言提示，解决 VLA 模型在非马尔可夫长时序操控任务中的局限性，在真实桌面任务上显著优于 π0、π0.5、Gr00T N1.5 等 baseline。


## Problem

现有 Vision-Language-Action (VLA) 模型默认假设当前观测足以决定下一步动作（马尔可夫假设），但在长时序操控任务中这一假设会失效：
- **部分可观测性**：任务关键信息可能被遮挡或已从视野消失
- **历史依赖性**：正确动作可能依赖于早期观测而非当前帧
- **杂乱干扰**：无关物体分散 VLA 的视觉 grounding 注意力

现有两类扩展方案的不足：
1. **Memory-augmented VLA**：历史容量 vs 效率权衡，有限记忆可能遗漏稀疏关键证据
2. **层次化 VLM-VLA**：VLM 在线规划延迟高，且仅通过语言接口与 VLA 通信，在杂乱场景中 grounding 脆弱


## Method

### 整体架构（Figure 1）

CodeGraphVLP 是一个层次化框架，包含三个核心模块：

#### 1. 持久化语义图状态 𝒢_t (Section III-B)

**图结构**：𝒢_t = (𝒱_t, ℰ_t)
- 节点 v_i ∈ 𝒱_t：任务相关实体，含语义名称、多视角 mask/bbox、任务属性
- 边 e_ij = (v_i, v_j, r) ∈ ℰ_t：类型化关系（in, on, near）

**初始化流程**（4 步）：
1. **物体分割**：YOLOE 实例分割（微调了 10 个视频的机器人臂 mask）→ 每视角 mask 集合
2. **任务相关物体识别**：Set-of-Mark prompting（物体轮廓+数字ID）→ VLM 查询筛选相关物体及属性
3. **多视角关联**：
   - 语义距离：CLIP 视觉特征余弦距离 < τ_vis 匹配
   - 几何距离：对未匹配物体，用归一化锚点距离签名做最近邻匹配 < τ_geo
4. **关系推导**：基于 mask 的轻量几何规则（near=距离阈值, in=包含关系, on=垂直顺序+边界接触）

**在线更新**：
- Cutie 追踪器更新已有节点的 mask
- 重新运行分割器 + 关联流程修正漂移和发现新物体
- 合并已有节点或添加新任务相关节点，刷新边

#### 2. Code-as-Planner (Section III-C)

**构建**：任务初始化时，LLM（GPT-5）一次性合成 Python 规划器 𝒫：
- 辅助函数：图查询原语（按类/属性过滤、定位容器、检查 holding、选择空缓冲区）
- 布尔谓词：编码任务约束和进度条件
- 主函数 policy(graph)：返回 (子任务指令 l^sub_t, 子任务相关物体 𝒪^rel_t)

**运行机制**：
- 每个 action chunk 执行后调用 𝒫(𝒢_t)
- 查询图状态判断当前子任务是否完成 → 更新 task_memory → 推进或重复
- 一次性合成分摊 LLM/VLM 推理成本，运行时无需大型模型在线参与

**示例（Swap Cups）**：
- 一次性角色绑定：识别 black_cup, other_cup, start_plates, buffer_plate
- 缓存三步 swap_plan（遵守容器互斥约束）
- 运行时扫描未完成步骤，基于 holding/in 谓词选择 pick up 或 put inside

#### 3. 去噪视觉语言提示 (Section III-D)

**子任务语言提示**：用规划器生成的短祈使句 l^sub_t 替代完整长时序指令 l

**去噪视觉提示**：
- 对每个视角 v，构建保留 mask：M^v_t = max_{i ∈ 𝒪^rel_t} m^v_{i,t}
- 生成去噪图像：Ĩ^v_t = I^v_t ⊙ M^v_t（仅保留子任务相关物体，其余像素置黑）

**VLA 执行**：以 (去噪多视角观测, 本体感知, 子任务指令) 为输入预测动作 chunk

**训练**：将长时序 demo 转化为 (去噪观测, 本体感知, 动作轨迹, 子任务指令) 元组，通过 MLE 优化 VLA 参数


## Experiments

### 硬件设置
- 机械臂：UR10e + Robotiq 2F-85 平行夹爪
- 相机：固定过肩视角 + 腕部相机（2 路 RGB，10Hz）
- GPU：4× NVIDIA A6000（训练），1× GPU（推理）

### 任务设计（3 个真实世界非马尔可夫任务）

1. **Pick-and-Place Twice**：立方体在两盘子间往返一次（初始和终止状态视觉相似，需要记忆已完成步骤）
2. **Place-and-Stack**：将立方体放入杯子，再叠上另一个杯子（立方体放入后完全遮挡，需依赖历史观测选择空杯）
3. **Swap Cups**：利用空缓冲盘交换两个杯子位置（需记忆初始分配，且有两个变体：黑杯先或蓝杯先）

### 演示数据
- Pick-and-Place Twice: 100 段
- Place-and-Stack: 100 段
- Swap Cups: 200 段（黑杯先/蓝杯先各 100）

### Baselines
- π0, π0 FAST, π0.5, Gr00T N1.5（原始，不含历史）
- History-augmented Gr00T N1.5（4 帧历史，1s 间隔）

### 训练配置
- VLA backbone: π0（flow-based）
- LoRA fine-tune: 50K iterations, lr=1e-5, batch_size=128
- 推理：action chunk horizon H=10 后重规划

### 主要结果（Table I）
- CodeGraphVLP 在所有任务上成功率最高
- π0 FAST 在所有任务上完全失败（自回归解码在长时序闭环控制中崩溃）
- Flow/diffusion 解码器的 VLA 更稳定
- 即使最强的 history-augmented baseline 也显著低于 CodeGraphVLP
- 说明非结构化时序上下文不足以解决非马尔可夫依赖和杂乱 grounding 错误

### 消融实验

**Table II: 规划效率（Swap Cups）**
- Code-as-Planner vs 两种 VLM 在线规划器
- VLM 规划器即使加入语义图状态仍有改善空间
- Code-as-Planner 成功率更高且延迟大幅降低（一次性合成 vs 反复调用 VLM）

**Table III: 去噪视觉提示（Swap Cups）**
- 去除去噪视觉提示：成功率从 **85%** 降至 **40%**
- 说明进度引导的感知输入对杂乱场景下的动作推理至关重要


## Limitations

1. **依赖基础模型能力**：语义图构建和程序合成均依赖 VLM/LLM，受其能力和失败模式限制
2. **视角和视觉质量敏感**：VLM 推断的属性和关系对相机视角和视觉质量敏感
3. **代码规划器需精心设计 prompt**：合成代码的可靠性取决于 prompt 工程
4. **未涉及开放世界场景**：当前语义图构建流程假设了固定的物体类别和关系类型
5. **未来方向**：开放世界语义图生成模块；合成代码的自动验证和自检机制


## Key Takeaways

1. **结构化状态优于隐式记忆**：将任务上下文外化为显式语义图 + 可执行代码规划器，比 memory-augmented VLA 的隐式历史表示更有效追踪非马尔可夫进度
2. **程序化推理替代在线 VLM 调用**：一次性合成可执行代码规划器，避免在线 VLM 推理的高延迟，同时保持可解释性
3. **去噪视觉提示是关键**：85%→40% 的消融证明，通过 mask 过滤非相关物体对 VLA 在杂乱场景中的 grounding 至关重要
4. **与我们研究的相关性**：
   - 语义图的结构化表示思路可迁移到 DLO 操控（如追踪绳索状态和与环境的交互关系）
   - Code-as-Planner 的程序化推理范式适合需要精确时序控制的 DLO 任务
   - 去噪视觉提示策略对 DLO 操控中减少背景干扰有参考价值

## 相关概念

- [[robotic-manipulation]]
- [[vision-language-model]]
- [[planning]]
- [[deformable-linear-object]]
- [[grasping]]

## 相关研究者

- [[vo|Vo, Khoa]]
