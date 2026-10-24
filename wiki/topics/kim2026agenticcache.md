---
title: "AgenticCache: Cache-driven asynchronous planning for embodied AI agents"
tags: [VLM, robot-learning, planning]
created: "2026-05-01"
updated: "2026-05-01"
type: "literature"
status: "stub"
summary: "提出基于大语言模型的操控方法。"
authors: "Kim, Hojoon; Wu, Yuheng; Tambe, Thierry"
year: "2026"
venue: "arXiv Preprint"
zotero_key: "HIBN9UZ9"
---
## 摘要

Embodied AI agents increasingly rely on large language models (LLMs) for planning, yet per-step LLM calls impose severe latency and cost. In this paper, we show that embodied tasks exhibit strong plan locality, where the next plan is largely predictable from the current one. Building on this, we introduce AgenticCache, a planning framework that reuses cached plans to avoid per-step LLM calls. In AgenticCache, each agent queries a runtime cache of frequent plan transitions, while a background Cache Updater asynchronously calls the LLM to validate and refine cached entries. Across four multi-agent embodied benchmarks, AgenticCache improves task success rate by 22% on average across 12 configurations (4 benchmarks x 3 models), reduces simulation latency by 65%, and lowers token usage by 50%. Cache-based plan reuse thus offers a practical path to low-latency, low-cost embodied agents. Code is available at https://github.com/hojoonleokim/MLSys26_AgenticCache.

## 中文简述

提出基于大语言模型的操控方法。

**研究方向**: 视觉-语言模型、机器人学习、运动规划

## 关键贡献

（待精读 - 在 Claudian 中说 "精读 HIBN9UZ9" 即可生成完整分析）

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
- [[robot-learning]]
- [[planning]]

## 相关研究者

- [[kim-hojoon|Kim, Hojoon]]
