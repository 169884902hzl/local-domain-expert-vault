---
title: "Force policy: Learning hybrid force-position control policy under interaction frame for contact-rich manipulation"
tags: [manipulation, imitation, DLO]
created: "2026-05-12"
updated: "2026-05-12"
type: "literature"
status: "done"
summary: "提出 Interaction Frame 将接触操控的力-位分解为物理可观测量，构建全局视觉策略+高频局部力控策略的分层架构，在抛光和插入类任务上显著优于所有基线，泛化到未见物体时成功率达 80-100%。"
authors: "Fang, Hongjie; Tang, Shirun; Mei, Mingyu; Qin, Haoxiang; He, Zihao et al."
year: "2026"
venue: "arXiv Preprint"
zotero_key: "4SHTQPFJ"
---
## 摘要

Contact-rich（接触丰富） manipulation（操控） demands human-like integration of perception and force feedback: vision should guide task progress, while high-frequency interaction control must stabilize contact under uncertainty. Existing learning-based policies often entangle these roles in a monolithic network, trading off global generalization against stable local refinement, while control-centric approaches typically assume a known task structure or learn only controller parameters rather than the structure itself. In this paper, we formalize a physically grounded interaction frame, an instantaneous local basis that decouples force regulation from motion execution, and propose a method to recover it from demonstrations. Based on this, we address both issues by proposing Force Policy, a global-local vision-force policy in which a global policy guides free-space actions using vision, and upon contact, a high-frequency local policy with force feedback estimates the interaction frame and executes hybrid force-position control for stable interaction. Real-world experiments across diverse contact-rich（接触丰富） tasks show consistent gains over strong baselines, with more robust contact establishment, more accurate force regulation, and reliable generalization to novel objects with varied geometries and physical properties, ultimately improving both contact stability and execution quality. Project page: https://force-policy.github.io/

## 中文简述

提出基于力控制的绳索操控方法，具有泛化能力特点。

**研究方向**: 机器人操控、模仿学习、可变形物体操控

## 关键贡献

1. **Interaction Frame（IF）理论形式化**：基于物理的环境刚度谱分解，定义瞬时局部坐标基，将力调节与运动执行解耦；与经典 TFF 不同，无需已知几何先验，仅从物理响应恢复
2. **自适应 IF 恢复方法**：针对耗散残差主导（摩擦类任务）和结构残差主导（刚度类任务）两种情况分别提出重建公式，使用 Gemini 3 Pro 进行语义分类选择策略
3. **Force Policy 分层架构**：全局视觉策略（RISE-2）负责自由空间运动和任务推进，高频局部力策略负责接触交互的混合力-位控制；通过选择掩码 S 作为隐式路由器
4. **双策略异步调度器**：多线程异步推理 + DTW waypoint 对齐 + 加速度连续轨迹规划，实现延迟感知的平滑执行
5. **四种规范任务模式分类**：Free / Surface / Insertion / Rotation，每种对应不同的选择掩码和参考力配置
## 结构化提取

- **Problem**: 接触丰富操控中视觉全局引导与力局部控制的角色纠缠，以及任务交互结构缺乏显式表示
- **Method**: Interaction Frame 理论 + 自适应恢复 + 全局视觉策略/局部力策略分层架构 + 双策略异步调度器
- **Tasks**: Push and Flip（抛光类）、Plug in EV Charger（插入类）、Scrape off Sticker Easy/Hard（表面交互类）
- **Sensors**: 6-DoF 力/力矩传感器（Flexiv 法兰端）、全局 RGB-D 相机（RealSense D415）、腕部 RGB-D 相机（RealSense D415）、末端执行器本体感受（关节位置/速度）
- **Robot Setup**: 单臂 Flexiv Rizon 4 + GN-02 夹爪，6-DoF F/T 传感器安装在法兰端
- **Metrics**: 任务成功率（主要）、力距离 dd（力控制精度）、IF 角度误差（恢复准确性）、SPARC（轨迹平滑度）
- **Limitations**: 仅适用稳定接触；不支持多点/面接触和力矩控制；力驱动高层决策未探索；评估仅两类任务
- **Evidence Notes**: 论文提供了完整的理论推导（含定理证明）、三个真实任务实验（每任务 10-20 次试验 × 7 种方法）、6 个未见物体泛化测试、IF 恢复方法对比消融、异步调度器消融。力控制结果有数值表格和可视化曲线支撑。
## 本地引用关系

- [[fang2026force]]
## 证据元数据

- Fulltext Quality: fulltext（通过 arXiv HTML 获取完整论文文本）
- Evidence Coverage: 完整覆盖理论推导、方法设计、实验结果、消融分析、局限性和补充材料
- Confidence: high
- Summary: 提出 Interaction Frame 将接触操控的力-位分解为物理可观测量，构建全局视觉策略+高频局部力控策略的分层架构，在抛光和插入类任务上显著优于所有基线，泛化到未见物体时成功率达 80-100%。


## Problem

接触丰富的机器人操控（contact-rich manipulation）需要同时处理两种不同尺度的控制需求：
1. **全局层面**：视觉引导任务进展、长期规划和空间定位
2. **局部层面**：高频力反馈实现稳定的接触交互

现有方法的两大瓶颈：
- **学习策略的单体设计问题**：将视觉和力信号纠缠在单一端到端网络中，全局泛化与局部精修相互制约
- **控制结构缺失**：控制中心化方法假设已知任务结构或仅学习控制器参数，而非学习结构本身

核心挑战：如何在保持全局泛化能力的同时实现稳定的局部力控制？如何显式表示任务交互结构使其跨任务迁移？


## Method

### 理论基础（III-A）
- 将环境局部响应建模为对称刚度矩阵 K_env
- 谱分解得到主刚度 λ_i 和主轴 q_i，将交互空间分为约束子空间 U（高刚度）和可运动子空间 T（低刚度）
- 引入任务意图 {ξ*, W*}：运动意图驱动 T 子空间，力意图驱动 U 子空间
- IF z 轴 = 主力意图方向，x 轴 = 运动意图在 z 正交平面上的投影

### IF 恢复（III-B, IV-A）
- 非理想接触下功率 P = W_c^T ξ* + W*^T ξ_c
  - 结构残差主导时：W* ≈ W，运动正交化 ξ* = ξ - Proj_W(ξ)
  - 耗散残差主导时：ξ* ≈ ξ，力正交化 W* = W - Proj_ξ(W)
- 使用 Gemini 3 Pro 根据视觉上下文和任务描述分类主导残差类型
- 任务模式分类基于 IF 对齐的信号特征（twist/wrench 在各轴的相对大小）

### 力策略架构（IV-B）
- **局部策略 Π_local**：输入 = 末端执行器运动历史 Δs + 力历史 W + 全局视觉特征 ϕ(I)；编码器 = ResNet（腕部图像）+ GRU（本体感受）；FiLM 条件化 ϕ(I)；输出 = (Σ, S, W^ref, Δs chunk)
- **全局策略 Π_global**：RISE-2 实现，仅依赖全局 3D 视觉感知；接触时仅提供视觉特征 ϕ(I)
- **路由器**：选择掩码 S 的非零项隐式激活力控轴，切换控制权
- **实现细节**：全局视觉特征 = RISE-2 扩散头的 action feature；局部去噪使用 MIP head；IF/力参考/掩码用 MLP head 预测

### 异步调度器（IV-C）
- 多线程异步设计：推理与执行重叠
- 双策略输出统一重采样至 50Hz
- DTW waypoint 对齐：消除延迟导致的不连续跳变
- 加速度连续轨迹规划：抑制急动，减少惯性干扰，提高力感知保真度


## Experiments

### 实验设置
- **机器人**：Flexiv Rizon 4 机械臂 + GN-02 夹爪 + 6-DoF F/T 传感器
- **传感器**：2x Intel RealSense D415（全局相机 + 腕部相机）
- **数据采集**：arm-to-arm 遥操作 + 力反馈，每任务 50 次示范
- **计算**：π 系列模型在 A800 GPU 上运行，其余在 RTX 3090 上
- **评估**：Push and Flip 20 次试验，其余各 10 次

### 主实验结果（Table II）

| 任务 | Force Policy | 次优基线 |
|------|-------------|---------|
| Push and Flip (push) | 100% | 100% (RISE-2/RDP/FoAR) |
| Push and Flip (flip) | **95%** | 62.5% (TA-VLA) |
| Plug in EV Charger (contact) | 100% | 100% (多个) |
| Plug in EV Charger (match) | **90%** | 90% (RISE-2) |
| Plug in EV Charger (plug in) | **65%** | 10% (FoAR) |
| Scrape off Sticker Easy (full off) | **100%** | 80% (RISE-2) |
| Scrape off Sticker Hard (full off) | **90%** | 20% (FoAR) |

### 力控制评估（Table III）
- Force Policy 平均力距离 dd = 0.00 cm（最接近人类示范力曲线）
- 次优 FoAR = 0.25 cm，最差 TA-VLA = 1.25 cm

### 泛化实验（Table IV）
- Push and Flip 任务，6 个未见物体（不同颜色、几何形状、刚度）
- Force Policy：4/5 ~ 5/5 成功率
- 所有基线：0/5 ~ 3/5 成功率
- RISE-2 在未见物体上接近接触区域成功率很高，但视觉无法可靠完成接触建立

### 消融实验
1. **IF 恢复对比**（Scrape off Sticker）：自适应方法 > twist-only > wrench-only（50% → 90%）> analytic > power-based
2. **语义分类准确性**：三个任务分别为 100%、92%、98%
3. **异步调度器**：力/运动 SPARC 指标显著提升，轨迹更平滑


## Limitations

1. **IF 理论范围**：仅适用于稳定接触操控（排除断裂、塑性变形等不可逆变化）
2. **多点/面接触**：理论讨论但未实现
3. **力矩控制**：未显式估计真实接触点，力矩控制不直接支持
4. **力用于高层决策**：如"拉一下检查连接器是否插好"等力驱动判断未探索
5. **评估范围**：仅覆盖 peg-in-hole 和 surface interaction 两类任务
6. **全局策略绑定 RISE-2**：模块化设计但未验证与其他全局策略的兼容性


## Key Takeaways

1. **力信号的本质是间歇性的**：仅在接触阶段有意义，自由空间中是噪声。将力信号全局注入会降低性能（ForceVLA 的失败案例证明了这一点）
2. **交互结构的显式建模 > 隐式学习**：IF 提供了可解释的控制分解，使策略学习有更好的 credit assignment
3. **全局-局部分层是力操控的正确抽象**：视觉管"去哪里"，力控管"怎么动"，各自在最擅长的尺度工作
4. **混合力-位控制比阻抗/导纳更适合多轴约束**：明确分离"应施加力"和"应实现位置"的方向
5. **LLM 的语义先验可辅助物理建模**：用 Gemini 分类残差类型是一种轻量的任务先验注入

### 与 DLO 操控的关联
- DLO 操控中的弯折、缠绕、插入等操作本质上是 contact-rich 任务
- IF 的自适应恢复策略可能适用于 DLO 接触中刚度/摩擦混合的场景
- 全局-局部分层架构可迁移到 DLO：视觉定位 DLO + 局部力控处理接触
- 当前局限：DLO 拉伸/弯曲属于大变形，IF 的局部保守假设可能不完全适用

## 相关概念

- [[robotic-manipulation]]
- [[imitation-learning]]
- [[deformable-linear-object]]
- [[vision-language-model]]
- [[grasping]]

## 相关研究者

- [[fang|Fang, Hongjie]]
