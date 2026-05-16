---
title: "Grounding sim-to-real generalization in dexterous manipulation: An empirical study with vision-language-action models"
tags: [manipulation, VLM, RL, sim-to-real]
created: "2026-05-02"
updated: "2026-05-02"
type: "literature"
status: "done"
summary: "系统性实证研究VLA模型零样本Sim-to-Real迁移的四维因子（域随机化、渲染保真度、物理真实度、RL微调），基于10k+真实世界试验得出五个关键结论：空间随机化主导迁移性能、帧级随机化优于回合级、渲染保真度有边际递减效应、RL微调显著提升鲁棒性。"
authors: "Jin, Ruixing; Zhu, Zicheng; Ouyang, Ruixiang; Xu, Sheng; Yue, Bo et al."
year: "2026"
venue: "arXiv Preprint"
zotero_key: "V453E9FX"
---
## 摘要

Learning a generalist control policy for dexterous manipulation（灵巧操控） typically relies on large-scale datasets. Given the high cost of real-world data collection, a practical alternative is to generate synthetic data through simulation. However, the resulting synthetic data often exhibits a significant gap from real-world distributions. While many prior studies have proposed algorithms to bridge the Sim-to-Real（仿真到真实迁移） discrepancy, there remains a lack of principled research that grounds these methods in real-world manipulation（操控） tasks, particularly their performance on generalist policies such as Vision-Language-Action (VLA) models. In this study, we empirically examine the primary determinants of Sim-to-Real（仿真到真实迁移） generalization across four dimensions: multi-level domain randomization, photorealistic rendering, physics-realistic modeling, and reinforcement learning（强化学习） updates. To support this study, we design a comprehensive evaluation protocol to quantify the real-world performance of manipulation（操控） tasks. The protocol accounts for key variations in background, lighting, distractors, object types, and spatial features. Through experiments involving over 10k real-world trials, we derive critical insights into Sim-to-Real（仿真到真实迁移） transfer. To inform and advance future studies, we release both the robotic platforms and the evaluation protocol for public access to facilitate independent verification, thereby establishing a realistic and standardized benchmark for dexterous manipulation（灵巧操控） policies.

## 中文简述

提出基于强化学习的灵巧手方法，具有仿真到真实迁移特点。

**研究方向**: 机器人操控、视觉-语言模型、强化学习、仿真到真实迁移

## 关键贡献

1. **因子化实证框架**：将Sim2Real迁移分解为四个维度——多层域随机化、逼真渲染、物理真实建模、RL微调，在统一框架下进行受控对比实验
2. **结构化域随机化分析**：将域随机化分解为五个结构化因子（背景BG、光照LT、桌面干扰物TD、相机位姿CP、桌面高度TH），独立评估每个因子的贡献
3. **10k+真实世界试验**：设计全面评估协议，控制背景、光照、干扰物、物体类型、空间位置等变量，进行超万次真实世界试验
4. **五个关键发现（Lessons）**：空间随机化主导迁移、帧级优于回合级、渲染保真度边际递减、RL显著增强鲁棒性
5. **开放基准平台**：发布标准化评估协议和双臂机器人在线评估平台，支持可复现的Sim2Real基准测试
## 结构化提取

- **Problem**: VLA模型Sim-to-Real迁移缺乏系统性因子化实证研究；哪些仿真设计因素影响VLA在灵巧操控中的零样本迁移性能
- **Method**: OpenVLA-OFT + SFT/GRPO-RL，在RoboTwin 2.0中训练，5个双臂任务，结构化域随机化（5因子×2粒度），3级渲染保真度，10k+真实世界试验
- **Tasks**: 5个双臂桌面操控任务（Click Bell, Place Empty Cup, Beat Block Hammer, Stack Bowls Two, Pick Dual Bottles）
- **Sensors**: 单个前向Intel RealSense D435 RGB相机（640×480）
- **Robot Setup**: 仿真端Cobot Magic双臂平台，真实端Piper双臂平台，可调高度桌面
- **Metrics**: 任务成功率（success rate），在Sim-OOD和真实世界两个环境分别评估
- **Limitations**: 仅OpenVLA-OFT架构；仅双臂桌面任务（无DLO）；仅零样本迁移；Beat Block Hammer持续低分；物理真实度仅测极端值
- **Evidence Notes**: (1) 空间随机化（TH, CP）贡献最大，是外观随机化的2-3倍 (2) 帧级DR一致优于回合级，尤其对CP和BG (3) 渲染保真度Low→Medium提升显著，Medium→High边际递减 (4) SFT→RL提升约28个百分点(real)，RL+DR再提升约10个百分点 (5) 干扰物造成最大性能退化，光照影响最小 (6) 真实世界成功率在最佳设置下：Stack Bowls 63.1%、Click Bell 49.7%、Place Cup 41.0%
## 本地引用关系

-
## 证据元数据

- Fulltext Quality: fulltext (arXiv HTML)
- Evidence Coverage: high (全文含方法、实验表格、消融、附录细节)
- Confidence: high
- Summary: 系统性实证研究VLA模型零样本Sim-to-Real迁移的四维因子（域随机化、渲染保真度、物理真实度、RL微调），基于10k+真实世界试验得出五个关键结论：空间随机化主导迁移性能、帧级随机化优于回合级、渲染保真度有边际递减效应、RL微调显著提升鲁棒性。


## Problem

VLA模型通常依赖大规模数据集训练，而真实世界数据采集成本极高，仿真数据成为替代方案。但仿真与现实之间存在显著分布差距（Sim2Real gap）。虽然已有多种Sim2Real技术（域随机化、域适应、逼真渲染、RL微调），但缺乏系统性实证研究将这些方法在VLA模型的真实操控任务上进行因子化比较。核心问题是：**哪些具体因素、在多大程度上影响VLA模型在灵巧操控任务中的Sim-to-Real迁移能力？**


## Method

### 基础架构
- **策略模型**：OpenVLA-OFT，基于 Llama-2 7B 语言骨干 + SigLIP/DINOv2 融合视觉编码器
- **关键设计**：并行解码 + action chunking，连续动作表示（L1回归），FiLM模块调制视觉特征
- **RL变体**：保留LLaMA2输出头生成离散动作token，使用交叉熵损失

### 训练流程
1. **SFT阶段**：在RoboTwin 2.0仿真器中采集100条示范轨迹/任务，使用LoRA(rank=32)微调，L1回归损失
2. **RL微调阶段**：使用GRPO（Group Relative Policy Optimization），从SFT检查点初始化，无KL正则化，50 epochs
3. **训练硬件**：8× NVIDIA H100 80GB

### 域随机化（5个因子）
- **ξ_BG（背景）**：从11000张纹理库随机采样墙壁和桌面纹理
- **ξ_TD（桌面干扰物）**：从RoboTwin-OD（731物体，147类别）随机添加任务无关物体
- **ξ_CP（相机位姿）**：对头部相机施加±0.01m位移偏移
- **ξ_LT（光照）**：随机化光源颜色、类型、强度和位置
- **ξ_TH（桌面高度）**：±3cm范围内均匀变化

### 随机化粒度
- **回合级（episode-wise）**：每个回合开始时采样一次，固定不变
- **帧级（frame-wise）**：每个仿真步骤重新采样（仅限BG、LT、CP；TH和TD保持回合级）

### 渲染保真度（3级）
- **Low**：非光线追踪，4 spp，路径深度4
- **Medium**：光线追踪，4 spp，路径深度4
- **High**：光线追踪，32 spp，路径深度8，OIDN去噪

### 物理真实度
- 对照组：故意设置极端物理参数（摩擦系数0.001、恢复系数0.2、重力0.05 m/s²）


## Experiments

### 任务（5个双臂操控任务）
| 任务 | 描述 | 平均步数 |
|------|------|---------|
| Stack Bowls Two | 堆叠两个碗 | 313 |
| Beat Block Hammer | 用锤子敲击方块 | 113 |
| Pick Dual Bottles | 双臂各拾取一个瓶子 | 127 |
| Click Bell | 按铃铛顶部 | 85 |
| Place Empty Cup | 将空杯放到杯垫上 | 174 |

### 真实世界评估设置
- **机器人**：Piper双臂平台
- **相机**：Intel RealSense D435，640×480
- **变量控制**：背景（3种纹理）、光照（3种位置）、物体（见过/未见）、干扰物（2/4/8个）、空间（3×3网格）

### 主要结果

**域随机化因子对比（Tab.1，平均真实世界成功率）**：
| 设置 | Click Bell | Place Cup | Beat Hammer | Stack Bowls | Pick Bottles |
|------|-----------|-----------|-------------|-------------|-------------|
| Clean | 2.7% | 5.4% | 0.0% | 26.2% | 1.5% |
| CP | 23.5% | 17.5% | 4.6% | 42.3% | 16.2% |
| TH | 36.9% | 24.8% | 6.5% | 49.6% | 15.4% |
| All Factors | 49.7% | 41.0% | 11.5% | 63.1% | 23.8% |

**帧级 vs 回合级（Tab.2）**：帧级CP比回合级CP在真实世界平均提升3-8%；帧级BG提升更显著（高达13%）；帧级LT提升最小（0-2%）。

**RL微调效果（Tab.3）**：
| 训练变体 | 平均Sim-OOD | 平均Real |
|---------|-----------|---------|
| SFT (clean) | 18.4% | 5.6% |
| SFT + RL (clean) | 53.4% | 33.4% |
| SFT + RL + DR | 70.8% | 42.8% |

### 消融/额外实验
- 渲染保真度：Low→Medium提升显著，Medium→High边际递减；物理真实度影响小于视觉保真度
- 干扰物引入最大的性能退化，光照变化影响最小


## Limitations

1. **架构单一**：仅测试OpenVLA-OFT，未覆盖其他VLA架构（如π₀、GR00T）
2. **任务类型有限**：仅双臂桌面操控，无DLO/可变形物体、无移动操作
3. **Beat Block Hammer任务持续低分**：即使是最佳设置（SFT+RL+DR）仅16.2%，表明该方法对某些精细交互任务能力有限
4. **仅零样本评估**：不考虑使用少量真实数据微调的场景
5. **物理真实度实验设计**：仅设极端值 vs 默认值，缺少中间物理保真度的梯度实验
6. **单相机设置**：仅用正前方向RGB相机，未探索多相机或深度信息的影响
7. **仿真平台依赖**：基于RoboTwin 2.0，结论是否可推广到Isaac Gym/MuJoCo等平台未验证


## Key Takeaways

### 对DLO操控的启示
1. **空间随机化优先**：在DLO Sim-to-Real中，应优先随机化相机位姿和桌面/工作空间几何参数，而非过度关注纹理和光照
2. **帧级随机化策略**：对DLO场景中的背景和相机采用帧级随机化可提升迁移鲁棒性
3. **RL微调是关键杠杆**：仅靠SFT在clean仿真中训练的VLA几乎无法迁移到真实世界（平均5.6%成功率），RL微调将之提升至33.4%，再结合DR达到42.8%。对于DLO这种高维连续操控任务，RL微调应作为标准流程
4. **评估协议可借鉴**：受控因子评估（背景/光照/干扰物/物体/空间）+ 3×3网格空间泛化测试的方法论可直接应用于DLO操控基准设计
5. **渲染保真度够用即可**：Medium级别已捕获大部分可迁移视觉特征，对DLO仿真不必追求极致渲染

### 对VLM-based控制的意义
- VLA模型（VLM+动作头）的Sim-to-Real迁移性能高度依赖训练时的环境多样性，而非单纯增加模型参数
- RL微调为VLA引入了超越行为克隆的泛化能力，这对需要适应DLO变形不确定性的策略尤为重要

## 相关概念

- [[robotic-manipulation]]
- [[vision-language-model]]
- [[reinforcement-learning]]
- [[sim-to-real]]
- [[deformable-linear-object]]
- [[bimanual-manipulation]]
- [[grasping]]

## 相关研究者

- [[jin|Jin, Ruixing]]
