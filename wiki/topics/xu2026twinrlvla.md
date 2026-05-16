---
title: "TwinRL-VLA: Digital twin-driven reinforcement learning for real-world robotic manipulation"
tags: [manipulation, imitation, VLM, RL, sim-to-real]
created: "2026-05-02"
updated: "2026-05-02"
type: "literature"
status: "done"
summary: "提出TwinRL框架，通过手机扫描构建数字孪生，利用探索空间扩展策略和Sim-to-Real引导探索策略，解决VLA模型在真实世界在线RL中探索效率低和探索空间受限的问题，在4个操控任务上实现近100%成功率，比ConRFT等方法加速至少30%。"
authors: "Xu, Qinwen; Liu, Jiaming; Zhou, Rui; Shi, Shaojun; Han, Nuowei et al."
year: "2026"
venue: "arXiv Preprint"
zotero_key: "XWRG2HKI"
---
## 摘要

Despite strong generalization capabilities, Vision-Language-Action (VLA) models remain constrained by the high cost of expert demonstrations and insufficient real-world interaction. While online reinforcement learning（强化学习） (RL) has shown promise in improving general foundation models, applying RL to VLA manipulation（操控） in real-world settings is still hindered by low exploration efficiency and a restricted exploration space. Through systematic real-world experiments, we observe that the effective exploration space of online RL is closely tied to the data distribution of supervised fine-tuning (SFT). Motivated by this observation, we propose TwinRL, a digital twin-real-world collaborative RL framework designed to scale and guide exploration for VLA models. First, a high-fidelity digital twin is efficiently reconstructed from smartphone-captured scenes, enabling realistic bidirectional transfer between real and simulated environments. During the SFT warm-up stage, we introduce an exploration space expansion strategy using digital twins to broaden the support of the data trajectory distribution. Building on this enhanced initialization, we propose a sim-to-real（仿真到真实迁移） guided exploration strategy to further accelerate online RL. Specifically, TwinRL performs efficient and parallel online RL in the digital twin prior to deployment, effectively bridging the gap between offline and online training stages. Subsequently, we exploit efficient digital twin sampling to identify failure-prone yet informative configurations, which are used to guide targeted human-in-the-loop rollouts on the real robot. In our experiments, TwinRL approaches 100% success in both in-distribution regions covered by real-world demonstrations and out-of-distribution regions, delivering at least a 30% speedup over prior real-world RL methods and requiring only about 20 minutes on average across four tasks.

## 中文简述

提出基于强化学习的操控方法，具有仿真到真实迁移特点。

**研究方向**: 机器人操控、模仿学习、视觉-语言模型、强化学习、仿真到真实迁移

## 关键贡献

1. **关键观察**：通过系统真实世界实验，发现VLA RL的探索空间受SFT轨迹分布约束，与LLM领域类似（RL主要重加权已有路径而非扩展新路径）
2. **TwinRL框架**：数字孪生-真实世界协作RL框架，将数字孪生用作探索放大器和引导器
3. **探索空间扩展策略**：在SFT热身阶段用数字孪生生成多样轨迹，扩展探索覆盖
4. **Sim-to-Real引导探索策略**：并行数字孪生在线RL + 失败感知的真实世界HiL引导
## 结构化提取

- **Problem**: VLA模型真实世界在线RL中探索效率低、探索空间受SFT数据分布约束，导致OOD区域探索死锁和收敛缓慢
- **Method**: TwinRL三阶段框架——(1)数字孪生构建+探索空间扩展SFT，(2)数字孪生并行在线RL+缓冲区迁移，(3)失败感知HiL引导的真实世界在线RL
- **Tasks**: Pick-and-Place, Insert-Hexagon-Block, Insert-Triple-Column-Block, Erase-Whiteboard（桌面操控，精确插入，接触丰富任务）
- **Sensors**: Intel RealSense D455（第三人称RGB，256×256）+ D435（手腕RGB，128×128）
- **Robot Setup**: Franka FR3 7-DoF + UMI夹爪，RTX 4090推理+异步训练，A100离线SFT
- **Metrics**: 成功率（ID/OOD区域），训练时间（分钟），episode长度，收敛速度
- **Limitations**: 刚性物体假设，运动学模型无物理仿真，每任务需单独构建数字孪生，限于桌面操控
- **Evidence Notes**: 4个真实世界任务均验证了ID和OOD区域的近100%成功率；动机实验系统量化了SFT分布对探索的影响（A-only vs A+B在Region B: 0% vs 62.5%）；消融实验验证了各组件必要性；鲁棒性分析覆盖背景杂乱和光照变化
## 本地引用关系

- [[xu2026twinrlvla]]
## 证据元数据

- Fulltext Quality: fulltext (arXiv HTML全文，87K字符，含所有章节和附录)
- Evidence Coverage: 高（方法、动机实验、主实验、消融、鲁棒性分析、附录细节均已覆盖）
- Confidence: high
- Summary: 提出TwinRL框架，通过手机扫描构建数字孪生，利用探索空间扩展策略和Sim-to-Real引导探索策略，解决VLA模型在真实世界在线RL中探索效率低和探索空间受限的问题，在4个操控任务上实现近100%成功率，比ConRFT等方法加速至少30%。


## Problem

VLA模型受限于昂贵的专家演示和不足的真实世界交互。在线RL虽可提升模型，但在真实世界VLA操控中仍面临两大瓶颈：
1. **探索空间受限**：在线RL的有效探索空间紧密依赖于SFT数据分布的空间覆盖范围。SFT未覆盖的OOD区域中，策略无法获得正奖励，导致探索死锁（exploration deadlock）。
2. **探索效率低下**：即使用HiL（人机交互）辅助，在OOD区域进行在线RL仍因奖励景观不利和回放缓冲区数据不平衡，导致收敛缓慢且不稳定。

核心观察来自动机实验：A-only SFT策略在Region B（OOD）成功率为0%，A+B策略达62.5%；仅用A-only初始化的在线RL在Region B训练40K步后仍无法突破探索死锁。


## Method

### 整体架构（三阶段）

**Stage I: 探索空间扩展（SFT阶段）**
- **数字孪生构建**：
  - 场景：手机拍摄视频 → 3DGS重建（~10分钟）
  - 物体：SAM3D重建（~5秒）
  - 机器人：URDF模型
  - 对齐：ICP粗对齐 + 可微3DGS渲染精对齐
  - 运动学交互模型（无物理仿真）
- **物体中心表示**：AnyGrasp估计6-DoF抓取姿态，定义物体-末端执行器关系
- **轨迹生成**：
  - 运动规划轨迹（OMPL工具包）
  - 演示仿射变换轨迹（单条演示→多样执行轨迹）
  - 30步任务约1分钟生成一组数字孪生演示
- **SFT训练**：合并真实演示+数字孪生演示，最小化模仿学习损失 L_IL

**Stage II: 数字孪生在线RL**
- 在数字孪生中并行运行N个环境的在线RL
- 联合目标：L_twin = β·L_IL + η·L_Q（IL正则化 + RL Q值优化，灵感来自ConRFT）
- 收集多样轨迹（成功、失败、恢复行为）存入数字孪生回放缓冲区
- **关键转移**：将数字孪生缓冲区数据初始化真实世界回放缓冲区，缓解离线→在线过渡的不稳定性

**Stage III: 真实世界在线RL**
- 用数字孪生高效评估当前策略在大量初始配置上的表现
- 构建目标初始配置集 S_target = {s0 | SR(s0) < threshold}（失败率高的配置）
- 用这些配置引导真实世界的HiL rollout
- 避免灾难性遗忘：回放缓冲区保留高精度行为

### VLA策略形式化
- 输入：语言指令ℓ + 多视角图像 I_t = {I_t^side, I_t^wrist}
- 输出：7-DoF末端执行器动作 a_t = (Δp_t, Δr_t, g_t)
- 基座模型：Octo


## Experiments

### 实验设置
- **机器人**：Franka FR3 + 3D打印UMI夹爪
- **传感器**：Intel RealSense D455（第三人称，256×256）+ D435（手腕视角，128×128）
- **操控方式**：3D SpaceMouse遥操作
- **计算**：RTX 4090（推理+异步训练），A100 80GB（SFT离线训练）
- **4个任务**：
  1. Pick-and-Place（拾取放置）
  2. Insert-Hexagon-Block（六角块插入，精确定位）
  3. Insert-Triple-Column-Block（三列块插入，多步精确）
  4. Erase-Whiteboard（擦白板，接触丰富）
- **评估区域**：ID区域（红色，有真实演示覆盖）+ OOD区域（蓝色，未见配置）
- **Baseline**：ConRFT、HiL-based RL（Luo et al., Science Robotics）

### 主要结果
- **SFT阶段**：探索空间扩展策略使平均成功率提升42%（相比仅用真实演示训练）
- **在线RL阶段**：
  - TwinRL在ID和OOD区域均接近100%成功率
  - 比ConRFT和HiL-RL方法加速至少30%
  - 每个任务平均仅需约20分钟真实世界训练
- **Episode长度分析**（附录D）：TwinRL在Insert-Triple-Column-Block任务上episode长度下降更快更稳定

### 消融实验（附录）
- OOD-only增强 vs 联合增强（ID+OOD）
- 验证各组件贡献：数字孪生数据扩展、双缓冲区初始化、失败感知引导
- 结果表明：仅OOD增强导致ID性能下降，联合增强效果最佳

### 鲁棒性分析
- 在未见场景下评估：背景杂乱、光照变化
- SFT baseline在分布偏移下显著性能退化
- TwinRL训练的策略在鲁棒性场景中保持强性能


## Limitations

- **数字孪生质量依赖**：重建质量受手机拍摄条件和3DGS精度影响，复杂场景可能引入误差
- **运动学模型限制**：使用运动学交互模型而非物理仿真，无法处理需要精确接触力建模的任务（如柔性物体操控）
- **刚性物体假设**：物体中心表示假设刚性物体，不直接适用于可变形物体
- **单一抓取策略**：使用AnyGrasp固定抓取姿态，对非典型抓取策略支持有限
- **每任务需单独构建数字孪生**：虽然构建速度快（~15分钟），但泛化到新任务仍需人工流程
- **任务复杂度**：当前实验限于桌面操控，未验证在更复杂场景（如双臂协作、移动操控）的效果


## Key Takeaways

1. **SFT数据分布约束RL探索**：这一发现对DLO操控研究有启发——如果SFT仅覆盖有限的DLO配置，RL在未见DLO形态（如不同弯曲程度、缠绕方式）下可能同样遭遇探索死锁
2. **数字孪生作为探索放大器**：不仅是数据增强工具，更是在线RL的探索策略。这种"先仿真后真实"的渐进式RL训练对Sim-to-Real有参考价值
3. **手机扫描→数字孪生的高效流程**：15分钟构建（3DGS + SAM3D + ICP对齐），无需专业设备或完整物理仿真器
4. **失败感知引导**：用数字孪生高效识别易失败配置，有针对性地引导HiL，减少人工干预量——对于需要安全约束的DLO操控场景有潜在应用价值
5. **与现有VLA RL的对比**：相比ConRFT等纯真实世界方法，TwinRL通过仿真预训练+缓冲区迁移解决冷启动问题；相比SimLauncher，TwinRL更强调探索空间扩展而非critic学习引导

## 相关概念

- [[robotic-manipulation]]
- [[imitation-learning]]
- [[vision-language-model]]
- [[reinforcement-learning]]
- [[sim-to-real]]
- [[deformable-linear-object]]
- [[bimanual-manipulation]]
- [[grasping]]

## 相关研究者

- [[xu-qinwen|Xu, Qinwen]]
- [[liu-jiaming|Liu, Jiaming]]
