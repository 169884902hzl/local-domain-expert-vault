---
title: "Variational neural belief parameterizations for robust dexterous grasping under multimodal uncertainty"
tags: [VLM, tactile, planning, grasping]
created: "2026-05-01"
updated: "2026-05-01"
type: "literature"
status: "stub"
summary: "提出基于触觉感知的抓取方法，具有接触丰富特点。"
authors: "Enwerem, Clinton; Kalyanaraman, Shreya; Baras, John S.; Belta, Calin"
year: "2026"
venue: "arXiv Preprint"
zotero_key: "A8CXSRV7"
---
## 摘要

Contact variability, sensing uncertainty, and external disturbances make grasp execution stochastic. Expected-quality objectives ignore tail outcomes and often select grasps that fail under adverse contact realizations. Risk-sensitive POMDPs address this failure mode, but many use particle-filter beliefs that scale poorly, obstruct gradient-based optimization, and estimate Conditional Value-at-Risk (CVaR) with high-variance approximations. We instead formulate grasp acquisition as variational inference over latent contact parameters and object pose, representing the belief with a differentiable Gaussian mixture. We use Gumbel-Softmax component selection and location-scale reparameterization to express samples as smooth functions of the belief parameters, enabling pathwise gradients through a differentiable CVaR surrogate for direct optimization of tail robustness. In simulation, our variational neural belief improves robust grasp success under contact-parameter uncertainty and exogenous force perturbations while reducing planning time by roughly an order of magnitude relative to particle-filter model-predictive control. On a serial-chain robot arm with a multifingered hand, we validate grasp-and-lift success under object-pose uncertainty against a Gaussian baseline. Both methods succeed on the tested perturbations, but our controller terminates in fewer steps and less wall-clock time while achieving a higher tactile（触觉） grasp-quality proxy. Our learned belief also calibrates risk more accurately, keeping mean absolute calibration error below 0.14 across tested simulation regimes, compared with 0.58 for a Cross-Entropy Method planner.

## 中文简述

提出基于触觉感知的抓取方法，具有接触丰富特点。

**研究方向**: 视觉-语言模型、触觉感知、运动规划、抓取

## 关键贡献

（待精读 - 在 Claudian 中说 "精读 A8CXSRV7" 即可生成完整分析）

## 结构化提取

- Problem: 待精读补充
- Method: 待精读补充
- Tasks: 待精读补充
- Sensors: 待精读补充
- Robot Setup: 待精读补充
- Metrics: 待精读补充
- Limitations: 待精读补充
- Evidence Notes: 待精读补充

## 本地引用关系

-
## 相关概念

- [[vision-language-model]]
- [[tactile-sensing]]
- [[planning]]
- [[grasping]]

## 相关研究者

- [[enwerem|Enwerem, Clinton]]
