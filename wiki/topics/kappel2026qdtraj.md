---
title: "QDTraj: Exploration of diverse trajectory primitives for articulated objects robotic manipulation"
tags: [manipulation, RL]
created: "2026-05-01"
updated: "2026-05-01"
type: "literature"
status: "stub"
summary: "提出基于学习方法的操控方法，具有泛化能力特点。"
authors: "Kappel, Mathilde; Khoramshahi, Mahdi; Annabi, Louis; Amar, Faiz Ben; Doncieux, Stéphane"
year: "2026"
venue: "arXiv Preprint"
zotero_key: "Z33VKETT"
---
## 摘要

Thanks to the latest advances in learning and robotics, domestic robots are beginning to enter homes, aiming to execute household chores autonomously. However, robots still struggle to perform autonomous manipulation（操控） tasks in open-ended environments. In this context, this paper presents a method that enables a robot to manipulate a wide spectrum of articulated objects. In this paper, we automatically generate different robot low-level trajectory primitives to manipulate given object articulations. A very important point when it comes to generating expert trajectories is to consider the diversity of solutions to achieve the same goal. Indeed, knowing diverse low-level primitives to accomplish the same task enables the robot to choose the optimal solution in its real-world environment, with live constraints and unexpected changes. To do so, we propose a method based on Quality-Diversity algorithms that leverages sparse reward（奖励） exploration in order to generate a set of diverse and high-performing trajectory primitives for a given manipulation（操控） task. We validated our method, QDTraj, by generating diverse trajectories in simulation and deploying them in the real world. QDTraj generates at least 5 times more diverse trajectories for both hinge and slider activation tasks, outperforming the other methods we compared against. We assessed the generalization of our method over 30 articulations of the PartNetMobility articulated object dataset, with an average of 704 different trajectories by task. Code is publicly available at: https://kappel.web.isir.upmc.fr/trajectory_primitive_website

## 中文简述

提出基于学习方法的操控方法，具有泛化能力特点。

**研究方向**: 机器人操控、强化学习

## 关键贡献

（待精读 - 在 Claudian 中说 "精读 Z33VKETT" 即可生成完整分析）

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

- [[robotic-manipulation]]
- [[reinforcement-learning]]

## 相关研究者

- [[kappel|Kappel, Mathilde]]
