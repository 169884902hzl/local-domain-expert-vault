---
title: "Grasping"
tags: [concept, grasping]
created: "2026-04-25"
updated: "2026-04-26"
type: "concept"
status: "done"
summary: "抓取是操控的前置技能，从分析式抓取规划到数据驱动抓取策略的演化中，泛化性和鲁棒性仍是核心挑战"
aliases: [grasping, "robot grasping", "prehensile manipulation"]
---

## Definition

抓取：机器人通过夹爪、手或接触策略稳定获取物体控制权的基础技能

## Key Ideas

- 抓取是多数操控任务的前置技能，决定后续操作稳定性。
- 常用输入包括 RGB-D、点云、触觉和物体姿态估计。
- 核心问题是可泛化抓取表示、遮挡、接触不确定性和真实部署鲁棒性。
- 数据驱动抓取已从分析式规划转向端到端学习：[[brohan2023rt2]] RT-2 将抓取动作编码为文本 token，[[fu2024mobile]] ALOHA 用 ACT/Diffusion Policy 直接学习抓取+后续操作。抓取作为子任务逐渐被整合进更长的操控流程中。
- 抓取稳定性评估正在从二值化（成功/失败）走向连续度量：[[wu2025tacdiffusion]] 输出 6D wrench，[[röfer2025pseudotouch]] 预测触觉信号间接评估抓取质量。
- 触觉反馈对抓取鲁棒性至关重要：[[zhao2025polytouch]] 的 Tactile-Diffusion Policy、[[funk2024evetac]] 的事件相机滑移检测都证明了这一点。

## Method Families

- 机器人操控路径：本地有 56 篇相关文献，代表论文包括 [[baumeister2025incremental]]、[[boerdijk2025autonomous]]、[[chen2025deformpam]]、[[chen2025effective]]。
- 模仿学习路径：本地有 25 篇相关文献，代表论文包括 [[chen2025deformpam]]、[[chen2025effective]]、[[chen2025vividex]]、[[chuang2025active]]。
- 强化学习路径：本地有 14 篇相关文献，代表论文包括 [[chen2025vividex]]、[[han2025upvital]]、[[jiang2024manipulation]]、[[karim2024davil]]。
- 视觉-语言模型路径：本地有 11 篇相关文献，代表论文包括 [[brohan2023rt2]]、[[dalal2025local]]、[[liu820enhancing]]、[[patel2025realtosimtoreal]]。
- 扩散模型路径：本地有 9 篇相关文献，代表论文包括 [[chen2025deformpam]]、[[chen2025vividex]]、[[keunknowndiffuser]]、[[li2025routing]]。

## Key Papers

- [[fu2024mobile]]：Mobile ALOHA 硬件系统（$32k）+ 静态 ALOHA 数据 co-training + ACT/Diffusion Policy/VINN；证据：任务成功率（20 次评估），子任务成功率。
- [[brohan2023rt2]]：Vision-Language-Action (VLA) 模型；动作表示为文本 token；co-fine-tune；证据：任务成功率。
- [[collaboration2025open]]：OXE 数据集（22 机器人/1M+ episodes）+ RT-X 模型家族；RLDS 统一格式；证据：任务成功率（零样本/微调）。
- [[zhi2025closedloop]]：COME-robot — GPT-4V + 三级开放词汇感知 + 分层闭环反馈恢复（物体/局部/全局级）；证据：成功率(SR)、步骤成功率(SSR)、恢复率(RR)。
- [[zhao2025polytouch]]：PolyTouch三模态传感器（VHB/硅胶弹性体+荧光照明+曲面镜）+ Tactile-Diffusion Policy（T3+CLIP+AST+Cross-At...；证据：平均任务进度（3-7阶段）、平均任务成功率、弹性体耐久性（小时）。
- [[yang2025simtoreal]]：SMMS运动模糊缓解（图像增强+数据增强+识别拒绝+数据平滑）+ 反馈线性化伺服控制（Type III PI Design Function）；证据：召回率、错误率、位姿精度(S_pos/S_att)、伺服最终误差、对准时间、抓取/堆叠成功率。
- [[wu2025tacdiffusion]]：TacDiffusion — DDPM 6D wrench 输出 + 动态系统滤波器 + 阻抗控制前馈力；证据：成功率（零样本迁移平均 95.7%）+ 执行时间。
- [[wu2025rlgsbridge]]：RL-GSBridge — Soft Mesh Binding GS + 物理动力学 GS 编辑 + SACwB RL；证据：成功率（抓取 Sim-to-Real avg ↓6.6%，Pick-and-Place ↑4%）。
- [[wu2025imperfect]]：SSDF — Transformer 自监督预训练 (MTP+TR+AA) + 特征相似度质量分数 + 加权 BC；证据：任务成功率（仿真 85.6%/88.0%/50.4%/29.6%/28.4%，真实平均 45%）。
- [[wang2025transdiff]]：TransDiff — DDPM + 多条件引导（语义/边缘/法线）+ RVCDB 损失；证据：RMSE/MAbs（深度）+ 抓取成功率（仿真 87.5%）。

## Evidence Map

- 本地证据规模：当前概念页连接 62 篇 literature notes，其中 62 篇为 `status: done`。
- 代表性证据链：[[fu2024mobile]]、[[brohan2023rt2]]、[[collaboration2025open]]、[[zhi2025closedloop]]、[[zhao2025polytouch]]。
- 主要交叉主题：机器人操控(56)、模仿学习(25)、强化学习(14)、视觉-语言模型(11)、扩散模型(9)。
- 可核查实验结果主要来自：[[fu2024mobile]]、[[brohan2023rt2]]、[[collaboration2025open]]、[[zhi2025closedloop]]、[[zhao2025polytouch]]；回答具体性能问题时应回到这些论文笔记核对指标。

## Open Problems

- [[fu2024mobile]] 暴露的限制：占地面积大（90x135cm）；固定手臂高度限制低处操作；仅单任务学习；Cook Shrimp（长时域）成功率低。
- [[brohan2023rt2]] 暴露的限制：控制频率低（1-3Hz）；无法执行精细操控；仅限单臂数据；模型巨大（55-305B 参数）。
- [[collaboration2025open]] 暴露的限制：数据质量不均匀；某些数据集任务单一；缺乏精细操控数据；动作空间统一化有精度损失。
- [[zhi2025closedloop]] 暴露的限制：GPT-4V误检、抓取位置不利、API延迟成本、单环境测试。
- [[zhao2025polytouch]] 暴露的限制：VHB磁滞、多模态需更多数据、仅4任务验证、整体成功率偏低。
- [[yang2025simtoreal]] 暴露的限制：依赖ArUco标记、竞赛特定环境、未在工业场景验证、仿真碰撞处理缺陷。

## Related Concepts

- [[robotic-manipulation]]
- [[deformable-linear-object]]
- [[vision-language-model]]
- [[imitation-learning]]
- [[bimanual-manipulation]]
- [[diffusion-model]]
- [[reinforcement-learning]]
- [[robot-learning]]
- [[sim-to-real]]
- [[planning]]
- [[tactile-sensing]]
- [[flow-matching]]
- [[dynamical-systems]]
- [[novel-view-synthesis]]
- [[collision-avoidance]]
- [[physical-reasoning]]
## Related Papers

- [[Reactive Motion Generation via Phase-varying Neural Potential Functions]]
- [[antonova2021bayesian]]
- [[bang2026environmental]]
- [[baumeister2025incremental]]
- [[blancomulero2024benchmarking]]
- [[boerdijk2025autonomous]]
- [[brohan2023rt2]]
- [[chen2025benchmarking]]
- [[chen2025deformpam]]
- [[chen2025effective]]
- [[chen2025vegetable]]
- [[chen2025vividex]]
- [[chen2026abotphysworld]]
- [[chen2026adacleargrasp]]
- [[chen2026craft]]
- [[chen2026posterior]]
- [[chen2026ropa]]
- [[chen2026rotridiff]]
- [[choi2026rankq]]
- [[chuang2025active]]
- [[collaboration2025open]]
- [[cui2026aharobot]]
- [[dai2024racer]]
- [[dalal2025local]]
- [[das2026dart]]
- [[deshpande2026molmob0t]]
- [[dong2025vitavla]]
- [[du2024embedded]]
- [[du2026bioprovlaagent]]
- [[enwerem2026variational]]
- [[fan2026xr1]]
- [[fang2026dexdrummer]]
- [[fang2026force]]
- [[feng2026demystifying]]
- [[feng2026see]]
- [[fu2024mobile]]
- [[funk2024evetac]]
- [[gao2024prime]]
- [[gao2025must]]
- [[gao2026driftbased]]
- [[george2024vital]]
- [[grotz2025twin]]
- [[gu2026refinedp]]
- [[gu2026vistabot]]
- [[guan2026dssp]]
- [[guzey2025bridging]]
- [[haldar2026point]]
- [[han2025upvital]]
- [[hartz2024art]]
- [[he2026exploratory]]
- [[huang2026flexitac]]
- [[huang2026kinder]]
- [[huang2026mimic]]
- [[iek2026coral]]
- [[jauhri2026wholebody]]
- [[jeong2026your]]
- [[jia2026dreamplan]]
- [[jia2026gsplayground]]
- [[jiang2024manipulation]]
- [[jie2026omnivlarl]]
- [[jin2026grounding]]
- [[kang2026coenv]]
- [[karim2024davil]]
- [[keunknowndiffuser]]
- [[khan2026discrete]]
- [[li2025routing]]
- [[li2026affordsim]]
- [[li2026forcevla2]]
- [[li2026gazevla]]
- [[li2026h2r]]
- [[li2026hierarchical]]
- [[li2026realvlgr1]]
- [[liang2026vanim]]
- [[lin2026hifvla]]
- [[lips2024keypoints]]
- [[liu2025autonomous]]
- [[liu2025forcemimic]]
- [[liu2026longhorizon]]
- [[liu820enhancing]]
- [[liufu2026repovla]]
- [[longhini2026behavioral]]
- [[lu2026unified]]
- [[luijkx2026llmguided]]
- [[luo2024humanagent]]
- [[luo2026flash]]
- [[luo2026selfimproving]]
- [[ma2025running]]
- [[ma2026human]]
- [[ma2026semanticcontact]]
- [[mahboob2026betting]]
- [[marougkas2025integrating]]
- [[missal2026ropedreamer]]
- [[mitrano2024grasp]]
- [[mosbach2025promptresponsive]]
- [[narendra2026knowledgeguided]]
- [[nasiriany2025rtaffordance]]
- [[nazarczuk2025closed]]
- [[nie820smaller]]
- [[niu2026versatile]]
- [[ortegakral2026rio]]
- [[ozdamar820pushing]]
- [[park2026acg]]
- [[park2026demodiffusion]]
- [[patankar2025synthesizing]]
- [[patel2024getzero]]
- [[patel2025realtosimtoreal]]
- [[patil2026youve]]
- [[peters2026coordinated]]
- [[qi2026compose]]
- [[qiu2025wildlma]]
- [[röfer2025pseudotouch]]
- [[saad2026hybrid]]
- [[sagar2026robomd]]
- [[scheikl620movement]]
- [[schperberg2026mobius]]
- [[sha2026efficient]]
- [[shi2025zeromimic]]
- [[shi2026agile]]
- [[singh2025handobject]]
- [[singh2025intellirms]]
- [[smith2024steer]]
- [[steen2024quadratic]]
- [[styrud2025automatic]]
- [[sun2026maniparena]]
- [[tang2025kalie]]
- [[tang2025uad]]
- [[tong2024ovalprompt]]
- [[tu2026embody4d]]
- [[vo2026codegraphvlp]]
- [[wang2023hierarchical]]
- [[wang2023multistage]]
- [[wang2025transdiff]]
- [[wang2025vlaadapter]]
- [[wang2026beyond]]
- [[wang2026discretertc]]
- [[wang2026ocra]]
- [[wang2026offline]]
- [[wang2026radar]]
- [[wang2026visionlanguageaction]]
- [[wang2026vlathinker]]
- [[wang2026while]]
- [[wu2025imperfect]]
- [[wu2025rlgsbridge]]
- [[wu2025tacdiffusion]]
- [[wu2026affordgrasp]]
- [[wu2026continually]]
- [[wu2026contrastive]]
- [[xia2024cage]]
- [[xiao2026avavla]]
- [[xiao2026worldenv]]
- [[xie102multiview]]
- [[xie2026humanintention]]
- [[xu2026expertgen]]
- [[xu2026fingereye]]
- [[xu2026r2rgen]]
- [[xu2026roboagent]]
- [[xu2026token]]
- [[xu2026twinrlvla]]
- [[xue2026tube]]
- [[yan2026tac2real]]
- [[yang2025simtoreal]]
- [[yang2026hivla]]
- [[yang2026physforge]]
- [[yang2026rise]]
- [[yang2026twintrack]]
- [[yang2026ultradexgrasp]]
- [[ye2026generation]]
- [[ye2026reinforcement]]
- [[yin2026genie]]
- [[yokomizo2026physquantagent]]
- [[yuan2026embodiedr1]]
- [[zeng2026recapa]]
- [[zhang2021dair]]
- [[zhang2026forceflow]]
- [[zhang2026handx]]
- [[zhang2026joyaira]]
- [[zhang2026touchguide]]
- [[zhao2025polytouch]]
- [[zhao2026rosclaw]]
- [[zhao2026vitactracing]]
- [[zheng120dottip]]
- [[zheng2026pokevla]]
- [[zhi102unifying]]
- [[zhi2025closedloop]]
- [[zhou2025oneshot]]
- [[zhou2026ego]]
- [[zhou2026rcnf]]
- [[zhou2026sim1]]
- [[zhou2026vlbiman]]
- [[zhu2026nsvla]]
- [[ziakas2026aligning]]