---
title: "Diffusion Model"
tags: [concept, diffusion]
created: "2026-04-25"
updated: "2026-04-26"
type: "concept"
status: "done"
summary: "扩散策略将动作序列生成建模为条件去噪过程，是多模态动作分布建模的主流方案，但推理速度和闭环纠错仍是部署瓶颈"
aliases: ["diffusion model", "diffusion policy", diffusion]
---

## Definition

扩散模型：通过逐步去噪生成数据的生成模型

## Key Ideas

- 扩散策略的核心优势是自然处理**多模态动作分布**：同一观测可能对应多种合理动作，CVAE（ACT）容易模式坍缩，而扩散模型通过迭代去噪可以覆盖全部模式。[[chi2024diffusion]] 在 Push-T/Sauce 等多目标配置任务上证明了这一点。
- **条件化方式**决定性能：[[zhu2024scaling]] ScaleDP 用 AdaLN 替代 cross-attention 融合条件信息，配合非因果自注意力，实现了从 10M 到 1B 的规模扩展。[[chen2025coordinated]] 用物体状态而非动作作为预测目标，更好地捕获协调失败。
- 推理速度是最大瓶颈：DDPM 需要多步去噪，[[chi2024diffusion]] 的推理延迟高于 LSTM-GMM。[[li2025routing]] 用 DDIM 将去噪迭代降至 2 步，[[wu2025discrete]] 用 VQ-VAE+离散潜空间扩散加速。
- 扩散策略在 DLO/可变形物体操控中特别有价值：因为可变形物体的动作分布天然多模态。[[li2025routing]]、[[chen2025deformpam]]、[[scheikl620movement]] 都在 DLO 场景中使用了扩散策略。
- 触觉条件扩散为接触丰富任务提供了新方案：[[zhao2025polytouch]] 的 Tactile-Diffusion Policy 和 [[wu2025tacdiffusion]] 的 6D wrench 输出都展示了触觉信号作为扩散条件输入的独特价值。

## Method Families

- **DDPM/DDIM 条件扩散策略**：标准的去噪扩散概率模型用于动作序列生成。[[chi2024diffusion]] DDPM+视觉条件化+时序 Transformer；[[li2025routing]] DDIM（2 步去噪）用于 DLO routing；[[wang2025transdiff]] 多条件引导（语义/边缘/法线）。主流方案。
- **大规模扩散策略**：扩展模型规模和训练数据。[[zhu2024scaling]] ScaleDP 10M→1B（AdaLN 条件融合）；[[team2024octo]] Octo（OXE 预训练+Diffusion Action Head）；[[collaboration2025open]] RT-X。展示规模效应但推理更慢。
- **离散潜空间扩散**：量化动作后扩散。[[wu2025discrete]] VQ-VAE+DDIM 离散扩散（MT-5 84%/MT-12 66.3%）。推理更快但动作精度损失。
- **多模态/触觉条件扩散**：结合触觉等多模态输入。[[zhao2025polytouch]] Tactile-Diffusion Policy；[[wu2025tacdiffusion]] DDPM 6D wrench 输出（零样本 95.7%）；[[george2024vital]] VITaL 多模态预训练+扩散策略。触觉为接触任务提供关键信号。
- **偏好/质量引导扩散**：在推理时用额外模型选择最优动作。[[chen2025deformpam]] DPO 偏好学习+reward-guided action selection；[[lee2025diffdagger]] 扩散 loss 做不确定性估计+DAgger 主动学习。

## Key Papers

- [[chi2024diffusion]]：Diffusion Policy 是操控扩散策略的奠基工作。DDPM+闭环动作序列预测+视觉条件化，在 Push-T/Sauce 等任务上建立基线。后续几乎所有扩散策略论文都以此为比较对象。
- [[zhu2024scaling]]：ScaleDP 将扩散策略从 10M 扩展到 1B。AdaLN 替代 cross-attention、非因果自注意力、ViT 式配置。展示了规模效应在操控策略中的潜力。
- [[chen2025coordinated]]：分解为状态预测扩散+逆动力学模型。核心洞察：物体状态 > 动作作为预测目标。在 Push-L 双臂任务上 79.3% SR。
- [[wu2025discrete]]：Discrete Policy 用 VQ-VAE 量化动作+DDIM 离散潜空间扩散。为高频控制提供了更快的推理方案（MT-5 84%）。
- [[li2025routing]]：两阶段 RL→Diffusion 用于 DLO routing。DDIM 仅 2 步去噪实现闭环，在干扰下比 open-loop RL 更鲁棒（58.24% vs 48.35%）。
- [[zhao2025polytouch]]：Tactile-Diffusion Policy 结合触觉三模态传感器。展示了触觉信号对扩散策略的增益。
- [[wu2025tacdiffusion]]：TacDiffusion 输出 6D wrench 而非位姿，零样本迁移平均 95.7%。为力控任务提供了扩散策略方案。
- [[team2024octo]]：Octo 在 OXE 上预训练含 Diffusion Action Head。跨机器人泛化但控制频率 ~6Hz。
- [[chen2025deformpam]]：DeformPAM 用偏好学习引导扩散策略的 action selection。解决可变形物体长时序任务的分布偏移。
- [[lee2025diffdagger]]：Diff-DAgger 用扩散 loss 做不确定性估计+DAgger 主动学习。F1 失败预测+成功率提升。

## Evidence Map

- **本地证据规模**：27 篇 status:done 文献，覆盖核心 DDPM/DDIM（8 篇）、大规模扩展（3 篇）、离散扩散（2 篇）、多模态/触觉（5 篇）、偏好引导（3 篇）、DLO 应用（6 篇）。
- **强证据问题**（本地证据充分支持）：
  - 扩散 vs CVAE/GMM 在多模态动作分布中的优势：[[chi2024diffusion]] 有系统性对比。
  - 规模扩展的效果：[[zhu2024scaling]] 从 10M 到 1B 的定量数据。
  - DLO 场景中扩散策略的有效性：[[li2025routing]]、[[chen2025deformpam]] 有完整验证。
- **弱证据问题**（本地证据不足或缺失）：
  - 扩散策略在双臂 DLO 协同操控中的应用（仅有 [[chen2025coordinated]] 间接涉及）。
  - 推理速度优化方案（量化、蒸馏、一致性模型）在操控中的效果。
  - 扩散策略的理论收敛保证。

## Open Problems

- **推理速度 vs 动作质量的权衡**：[[chi2024diffusion]] 的推理延迟高于 LSTM-GMM，不适合 50Hz+任务。DDIM 减步和离散扩散是方向，但精度损失需要量化。
- **长时序扩散策略的累积误差**：扩散策略输出短时域动作块，长时序任务需要多次调用。[[chen2025deformpam]] 的分布偏移问题说明累积误差仍然严重。
- **扩散策略 + DLO 双臂操控**：当前 DLO 扩散策略（[[li2025routing]]、[[chen2025deformpam]]）都是单臂或简单双臂。双臂 DLO 协调的多模态动作分布如何用扩散策略建模是核心挑战。
- **闭环纠错的扩散策略**：扩散策略的闭环能力依赖于每步重新去噪，但去噪步数减少时纠错能力下降。如何实现既快又准的闭环扩散策略？

## Related Concepts

- [[deformable-linear-object]]
- [[robotic-manipulation]]
- [[imitation-learning]]
- [[vision-language-model]]
- [[grasping]]
- [[bimanual-manipulation]]
- [[reinforcement-learning]]
- [[robot-learning]]
- [[sim-to-real]]
- [[planning]]
- [[tactile-sensing]]
- [[flow-matching]]
- [[test-time-scaling]]
- [[dynamical-systems]]
- [[novel-view-synthesis]]
## Related Papers

- [[chen2025benchmarking]]
- [[chen2025coordinated]]
- [[chen2025deformpam]]
- [[chen2025effective]]
- [[chen2025vividex]]
- [[chen2026abotphysworld]]
- [[chen2026craft]]
- [[chen2026elasticflow]]
- [[chen2026posterior]]
- [[chen2026ropa]]
- [[chen2026rotridiff]]
- [[chi2024diffusion]]
- [[dai2024racer]]
- [[dong2026faster]]
- [[feng2026demystifying]]
- [[fu2024mobile]]
- [[gao2026driftbased]]
- [[george2024vital]]
- [[gu2026refinedp]]
- [[gu2026vistabot]]
- [[guan2026dssp]]
- [[han2026stereopolicy]]
- [[hartz2024art]]
- [[he2026exploratory]]
- [[he2026generative]]
- [[hu2026arvla]]
- [[huang2026flexitac]]
- [[huang2026kinder]]
- [[jauhri2026wholebody]]
- [[ji2026recovering]]
- [[jiang2026blockr1]]
- [[jiang2026break]]
- [[jiang2026world4rl]]
- [[keunknowndiffuser]]
- [[khan2026discrete]]
- [[kim2024openvla]]
- [[lee2025diffdagger]]
- [[lee2026implicit]]
- [[levy2026simulation]]
- [[li2025routing]]
- [[li2026affordsim]]
- [[li2026ets]]
- [[li2026gazevla]]
- [[li2026h2r]]
- [[li2026hpedit]]
- [[li2026realvlgr1]]
- [[liu2025forcemimic]]
- [[longhini2026behavioral]]
- [[lu2026unified]]
- [[luo2026selfimproving]]
- [[ma2026human]]
- [[ma2026semanticcontact]]
- [[moletta2026preference]]
- [[ortegakral2026rio]]
- [[park2026acg]]
- [[park2026demodiffusion]]
- [[patil2026youve]]
- [[peters2026coordinated]]
- [[puthumanaillam2026muninn]]
- [[qi2026compose]]
- [[qureshi2025splatsim]]
- [[sagar2026robomd]]
- [[scheikl620movement]]
- [[sha2026efficient]]
- [[shi2025zeromimic]]
- [[shi2026agile]]
- [[stambaugh2026mixeddensity]]
- [[team2024octo]]
- [[tu2026embody4d]]
- [[wang2025transdiff]]
- [[wang2026any2any]]
- [[wang2026beyond]]
- [[wang2026discretertc]]
- [[wang2026ocra]]
- [[wang2026offline]]
- [[wang2026phys2real]]
- [[wang2026visionlanguageaction]]
- [[wei2026navol]]
- [[wu2025discrete]]
- [[wu2025imperfect]]
- [[wu2025tacdiffusion]]
- [[wu2026affordgrasp]]
- [[wu2026contrastive]]
- [[xia2024cage]]
- [[xiao2026worldenv]]
- [[xu2026expertgen]]
- [[xu2026fingereye]]
- [[xu2026r2rgen]]
- [[xue2026tube]]
- [[yang2026hivla]]
- [[yang2026physforge]]
- [[yang2026ultradexgrasp]]
- [[ye2026reinforcement]]
- [[yin2026genie]]
- [[zhang2026forceflow]]
- [[zhang2026generative]]
- [[zhang2026handx]]
- [[zhang2026touchguide]]
- [[zhao2023finegrained]]
- [[zhao2025polytouch]]
- [[zhou2025oneshot]]
- [[zhou2026characterizing]]
- [[zhou2026sim1]]
- [[zhu2024scaling]]
- [[ziakas2026aligning]]