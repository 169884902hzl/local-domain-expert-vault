---
title: "BioProVLA-agent: An affordable, protocol-driven, vision-enhanced VLA-enabled embodied multi-agent system with closed-loop-capable reasoning for biological laboratory manipulation"
tags: [manipulation, VLM, robot-learning, bimanual]
created: "2026-05-16"
updated: "2026-05-16"
type: "literature"
status: "done"
summary: "提出基于 VLA 的低成本（$800-850）生物实验室多 Agent 闭环系统，通过 LLM 协议解析、VLM-RAG 状态验证和在线数据增强（AugSmolVLA）实现 15 个原子任务和 6 个组合任务的可验证执行，在透明器皿和过曝条件下表现稳健。"
authors: "Du, Zhaohui; Wang, Zhe; Fei, Hongmei; Cao, Xiwen; Xiao, Ting et al."
year: "2026"
venue: "arXiv Preprint"
zotero_key: "DPME6UIZ"
---
## 摘要

Biological laboratory automation can reduce repetitive manual work and improve reproducibility, but reliable embodied execution in wet-lab environments remains challenging. Protocols are often unstructured, labware is frequently transparent or reflective, and multi-step procedures require state-aware execution beyond one-shot（单样本） instruction following. Existing robotic systems often rely on costly hardware, fixed workflows, dedicated instruments, or robotics-oriented interfaces. Here, we introduce BioProVLA-Agent, an affordable, protocol-driven, vision-enhanced embodied multi-agent system enabled by Vision-Language-Action (VLA) models for biological manipulation（操控）. The system uses protocols as the task interface and integrates protocol parsing, visual state verification, and embodied execution in a closed-loop（闭环） workflow. A Tailored LLM Protocol Agent converts protocols into verifiable subtasks; a VLM-RAG Verification Agent assesses readiness and completion using observations, robot states, retrieved knowledge, and success/failure examples; and a VLA Embodied Agent executes verified subtasks through a lightweight policy. To improve robustness under wet-lab visual perturbations, we develop AugSmolVLA, an online augmentation strategy targeting transparent labware, reflections, illumination shifts, and overexposure. We evaluate the system on a hierarchical benchmark covering 15 atomic tasks, 6 composite workflows, and 3 bimanual（双臂） tasks, including tube loading, sorting, waste disposal, cap twisting, and liquid pouring. Across normal and high-exposure settings, AugSmolVLA improves execution stability over ACT, X-VLA, and the original SmolVLA, especially for precise placement, transparent-object manipulation（操控）, composite workflows, and visually degraded scenes. These results suggest a practical route toward accessible, protocol-centered, and verification-capable embodied AI for biological manipulation（操控）.

## 中文简述

提出基于视觉-语言的双臂方法，具有单样本学习特点。

**研究方向**: 机器人操控、视觉-语言模型、机器人学习、双臂操控

## 关键贡献

1. **低成本协议驱动多 Agent 框架**：硬件成本仅 $800-850 USD，以自然语言生物协议为任务接口，将协议理解、状态验证、具身执行、重试决策和人工干预统一为闭环流程
2. **协议到执行的中间表示**：将非结构化协议转换为结构化子任务单元（包含自然语言指令、前置条件、完成条件、知识库索引），桥接语义理解与机器人执行
3. **VLM-RAG 闭环验证机制**：整合实时视觉观测、机器人状态、检索知识和成功/失败示例，实现执行前的就绪性评估和执行后的完成性检查，提供可解释的失败反馈
4. **层级化生物操控基准 + AugSmolVLA**：15 个原子任务 + 6 个组合工作流 + 3 个双臂任务，并提出针对透明器皿、反光、光照变化和过曝的课程式在线数据增强策略
## 结构化提取

- Problem: 生物实验室机器人操控的三大挑战：非结构化协议解析、透明/反光器皿的视觉感知、多步骤任务的状态感知闭环执行
- Method: 四 Agent 闭环框架（Guiding Decision + LLM Protocol + VLM-RAG Verification + VLA Embodied），以自然语言协议为接口，AugSmolVLA 课程式在线视觉扰动增强
- Tasks: 15 个原子任务（盖子操作、插入、移除、精确放置、丢弃）、6 个组合工作流（加载、卸载、整理、清理）、3 个双臂任务（拧开/拧紧管盖、倾倒废液）
- Sensors: 相机视觉观测（受透明/反光/过曝干扰）、机器人关节状态
- Robot Setup: So-ARM101 双臂平台，低成本硬件约 $800-850 USD，标准生物实验耗材
- Metrics: 单任务 Success Rate (SR, 3 次重复, $\overline{SR} \pm SE$)，组合任务 Completion Rate (CR, 20 次试验步骤级完成率)
- Limitations: 任务复杂度和协议长度有限；双臂精细力控和时间同步仍困难（最高 55% SR）；无灵巧手；无自主实验设计能力；数据增强仅覆盖光照/反光
- Evidence Notes: 完整的全文精读覆盖了方法公式、所有实验表格（Table 2/4/5/6）、消融实验、相关工作、局限性讨论。论文提供了充分的定量实验证据支持各贡献点。
## 本地引用关系

-
## 证据元数据

- Fulltext Quality: fulltext
- Evidence Coverage: complete
- Confidence: high
- Summary: 提出基于 VLA 的低成本（$800-850）生物实验室多 Agent 闭环系统，通过 LLM 协议解析、VLM-RAG 状态验证和在线数据增强（AugSmolVLA）实现 15 个原子任务和 6 个组合任务的可验证执行，在透明器皿和过曝条件下表现稳健。


## Problem

生物实验室中的机器人操控面临三重挑战：
1. **协议非结构化**：生物实验协议以自然语言书写，包含专业术语、隐含条件和严格步骤依赖，传统系统需要用户将其转化为 ROS 脚本或机器人专用程序
2. **视觉感知困难**：常见生物实验耗材（离心管、冻存管、血清瓶）多为透明或反光材质，导致视觉定位和操控不稳定
3. **多步骤需要状态感知**：长流程实验需要持续判断任务就绪、完成和异常状态，而非一次性指令跟随

现有自动化平台依赖昂贵硬件、固定工作流或专用仪器，限制了资源受限实验室的可及性。


## Method

### 整体架构（四 Agent 协作）

1. **Guiding Decision Agent**：中枢调度器，管理系统初始化、子任务序列检查、闭环控制流程（前置验证→执行→后置验证）、重试/重排序/人工干预决策
2. **Tailored LLM Protocol Agent**：将非结构化协议解析为结构化子任务序列 $\mathcal{T} = \{\tau_i\}_{i=1}^N$，每个子任务 $\tau_i = (I_i, Pre_i, Post_i, K_i)$ 包含指令、前置条件、完成条件和知识库索引。通过 prompt 约束 LLM 执行意图解析、实体识别、动作空间映射
3. **VLM-RAG Verification Agent**：基于检索增强的视觉语义验证。从知识库 $\mathcal{K}$ 中检索相关项 $\mathcal{B}_i = \text{TopK}_{b \in \mathcal{K}} \text{sim}(\phi(Q_i^j), \phi(b))$，融合视觉观测、机器人状态、验证条件和参考示例进行二元判断（pass/fail）并输出自然语言解释
4. **VLA Embodied Agent**：基于 SmolVLA 的轻量级 VLA 策略，接收验证后的子任务指令生成动作序列 $A_t = \pi_\theta(O_t, R_t, I_i)$

### AugSmolVLA 课程式在线数据增强

在 SmolVLA 微调过程中引入动态视觉扰动：
- 扰动类型：亮度调整、对比度变化、低光照、过曝
- 课程式三阶段训练：
  - Stage 1 ($\mathcal{E}_1$)：仅原始数据，学习基础动作映射
  - Stage 2 ($\mathcal{E}_2$)：引入增强数据，扰动强度递增
  - Stage 3 ($\mathcal{E}_3$)：原始 + 增强混合训练，平衡稳定性与泛化性
- 不需要离线生成额外数据集，训练时动态扰动

### 闭环控制流程

对于每个子任务 $\tau_i$：
1. VLM-RAG 验证前置条件 $v_i^{pre} = V(O_t, R_t, Pre_i, K_i)$
2. 若 $v_i^{pre} = 1$：执行动作 $A_i = \pi_{VLA}(O_t, R_t, I_i)$
3. 若 $v_i^{pre} = 0$：尝试重排序未执行子任务、二次验证、或请求人工干预
4. 执行后验证完成条件 $v_i^{post} = V(O_{t+1}, R_{t+1}, Post_i, K_i)$
5. 若 $v_i^{post} = 1$：标记完成，进入下一子任务
6. 若 $v_i^{post} = 0$：触发重试、序列调整或人工干预

### 硬件平台

- So-ARM101 双臂机械臂平台
- 硬件成本约 $800-850 USD
- 标准生物实验室耗材：BY-80C 离心机、15mL 离心管、1.8mL 冻存管、水浴锅、血清瓶、垃圾桶


## Experiments

### 数据集
- 15 个原子任务（12 单臂 + 3 双臂），每个任务 100 条遥操作示教轨迹
- 数据格式：LeRobot
- 任务类型：盖子操作、插入、移除、精确放置、丢弃、拧转、倾倒

### 评估指标
- 单任务：Success Rate (SR)，3 次独立重复实验，报告 $\overline{SR} \pm SE_{SR}$
- 组合任务：Completion Rate (CR)，20 次试验，按步骤级别计算完成比例

### 单臂任务结果（Table 2）

AugSmolVLA 在全部 12 个单臂任务上取得最佳：
- Place Cryotube to Red Rack：40.00% → 65.00%（+25%）
- Place Centrifuge Tube to Orange Rack：43.33% → 53.33%（+10%）
- Discard Cryotube：48.33% → 55.00%
- Close Centrifuge Lid：100.00%（SmolVLA/AugSmolVLA 均达上限）
- 精确放置和透明物体操控任务提升最为显著

### 组合任务结果（Table 4）

AugSmolVLA 在全部 6 个组合任务上取得最佳：
- Clean up waste materials：75.00%（SmolVLA 62.50%，+12.5%）
- Tidy up the desktop：72.50%（SmolVLA 62.50%，+10%）
- Loading centrifuge tube：56.67%（ACT 28.33%，X-VLA 35.00%）

### 双臂任务结果（Table 5）

双臂任务成功率普遍较低，AugSmolVLA 仍为最优：
- Unscrew Tube Cap：55.00%（ACT 11.67%，X-VLA 5.00%）
- Tighten Tube Cap：33.33%（ACT 8.33%，X-VLA 11.67%）
- Pour Waste Liquid：36.67%（ACT 3.33%，X-VLA 10.00%）
- 组合 CR：39.45%（SmolVLA 37.00%）

### 过曝消融实验（Table 6）

在过曝条件下，原始 SmolVLA 显著下降：
- Place Cryotube to Red Rack：40.00% → 31.67%
- Discard Cryotube：48.33% → 31.67%
- Loading centrifuge tube CR：55.00% → 39.60%

AugSmolVLA 在过曝下恢复/提升：
- Place Cryotube to Red Rack：31.67% → 71.67%（+40%）
- Discard Cryotube：31.67% → 43.33%
- Place Centrifuge Tube：恢复至 43.33%（与正常条件持平）


## Limitations

1. 任务复杂度有限：仅覆盖基础生物实验操作，协议长度和物体多样性有待扩展
2. 双臂协调仍是挑战：精细接触控制和时间同步的准确率仍然较低（拧转任务最高仅 55%，倾倒 37%）
3. 未使用灵巧手：目前仅限夹爪操控
4. 缺少自主实验设计和决策能力：当前仅"执行实验步骤"，未达到自主设计和辅助科学发现的水平
5. 数据增强仅覆盖光照/反光扰动，未涉及其他视觉挑战（如遮挡、液面变化）
6. 基准规模有限（15 原子任务），泛化性验证不充分


## Key Takeaways

1. **多 Agent 闭环验证是长流程任务的关键设计模式**：将 VLM-RAG 验证插入执行前后，显著降低误差传播风险，对 DLO 多步骤操控（如绕线、打结序列）有直接借鉴价值
2. **课程式在线数据增强对透明/反光场景有效**：AugSmolVLA 的在线增强策略可直接迁移到 DLO 操控中的视觉挑战（DLO 与透明器皿共享边界模糊、反光干扰等视觉困难）
3. **低成本硬件可行**：$800-850 的平台实现复杂双臂操控，说明研究重心应从硬件转向算法和系统设计
4. **VLM-RAG 验证概念可迁移至 DLO 状态验证**：利用检索增强判断 DLO 状态（缠绕、松弛、结的类型），为 DLO 操控闭环提供语义层反馈
5. **协议驱动接口降低使用门槛**：以自然语言协议为接口的思想可推广为"任务描述驱动的 DLO 操控"，使非机器人专家也能使用

## 相关概念

- [[robotic-manipulation]]
- [[vision-language-model]]
- [[robot-learning]]
- [[bimanual-manipulation]]
- [[deformable-linear-object]]
- [[grasping]]

## 相关研究者

- [[du-zhaohui|Du, Zhaohui]]
- [[wang-zhe|Wang, Zhe]]
