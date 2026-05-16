---
title: "PolyTouch: A robust multi-modal tactile sensor for contact-rich manipulation using tactile-diffusion policies"
tags: [manipulation, imitation, diffusion, robot-learning]
created: "2026-04-25"
updated: "2026-04-25"
type: "literature"
status: "done"
summary: "提出PolyTouch多模态触觉手指（相机触觉+声学+外围视觉），耐用性超GelSight Mini 20倍（35hr vs 1-3.3hr），单指成本$61，基于T3+CLIP+AST编码器和cross-attention的tactile-diffusion policy在4个双臂任务上成功率提升最多34%（鸡蛋装盘100% vs 66%）。"
authors: "Zhao, Jialiang; Kuppuswamy, Naveen; Feng, Siyuan; Burchfiel, Benjamin; Adelson, Edward"
year: "2025"
venue: "arXiv Preprint"
zotero_key: "QSPWYLCA"
---
## 摘要

Achieving robust dexterous manipulation（灵巧操控） in unstructured domestic environments remains a significant challenge in robotics. Even with state-of-the-art（现有最优方法） robot learning methods, haptic-oblivious control strategies (i.e. those relying only on external vision and/or proprioception) often fall short due to occlusions, visual complexities, and the need for precise contact interaction control. To address these limitations, we introduce PolyTouch, a novel robot finger that integrates camera-based tactile（触觉） sensing, acoustic sensing, and peripheral visual sensing into a single design that is compact and durable. PolyTouch provides high-resolution tactile（触觉） feedback across multiple temporal scales, which is essential for efficiently learning complex manipulation（操控） tasks. Experiments demonstrate an at least 20-fold increase in lifespan over commercial tactile（触觉） sensors, with a design that is both easy to manufacture and scalable. We then use this multi-modal（多模态） tactile（触觉） feedback along with visuoproprioceptive observations to synthesize a tactile（触觉）-diffusion policy（扩散策略） from human demonstrations; the resulting contactaware control policy significantly outperforms haptic-oblivious policies in multiple contact-aware manipulation（操控） policies. This paper highlights how effectively integrating multi-modal（多模态） contact sensing can hasten the development of effective contact-aware manipulation（操控） policies, paving the way for more reliable and versatile domestic robots. More information can be found at https://polytouch.alanz.info/.


## 中文简述

提出基于扩散策略的灵巧手方法，具有接触丰富特点。

**研究方向**: 机器人操控、模仿学习、扩散模型、机器人学习

## 关键贡献

1. **PolyTouch传感器设计**：单指集成三种模态——相机触觉（RGB相机+VHB/硅胶弹性体+荧光照明+曲面镜）、接触式麦克风声学（48kHz）、外围视觉（侧窗+镜面）
2. **VHB弹性体方案**：使用3M VHB双面胶替代硅胶，5分钟内可完成制作，无专业设备需求，消除脱层问题
3. **耐用性突破**：35小时连续工具使用无故障，比GelSight Mini标准凝胶寿命提升至少20倍
4. **Tactile-Diffusion Policy框架**：T3触觉编码器+CLIP视觉+AST声学+MLP本体感觉→Cross-Attention组合→Diffusion Policy U-Net
5. **ICRA 2025最佳论文提名**
## 结构化提取

- Problem: 非结构化家庭环境中接触丰富操控的触觉感知缺失和现有触觉传感器耐用性/制造性差
- Method: PolyTouch三模态传感器（VHB/硅胶弹性体+荧光照明+曲面镜）+ Tactile-Diffusion Policy（T3+CLIP+AST+Cross-Attention+Diffusion U-Net）
- Tasks: 双臂扳手插入、水果分类、鸡蛋敲开、鸡蛋装盘
- Sensors: 相机触觉（IMX708 RGB）、声学（压电接触麦克风48kHz）、外围视觉（侧窗+镜面）、腕部相机（FLIR Blackfly S）、场景相机（FRAMOS D415e）
- Robot Setup: 双臂Franka Panda，直立安装，每臂配PolyTouch-VHB指+Fin-Ray被动顺应指，SpaceMouse遥操作采集
- Metrics: 平均任务进度（3-7阶段）、平均任务成功率、弹性体耐久性（小时）
- Limitations: VHB磁滞、多模态需更多数据、仅4任务验证、整体成功率偏低
- Evidence Notes: 全文5680词，2张实验表，7张图，ICRA 2025 Best Paper提名，开源项目页polytouch.alanz.info
## 本地引用关系

- [[george2024vital]]
- [[han2025upvital]]
- [[liu2025forcemimic]]
- [[röfer2025pseudotouch]]
- [[wu2025tacdiffusion]]
- [[zheng120dottip]]
## 证据元数据

- Fulltext Quality: fulltext
- Evidence Coverage: 完整全文（~5680 词），含 Table I-II、Figure 1-7、详细传感器规格和实验结果
- Confidence: high — 全文可读，ICRA 2025 Best Paper提名，方法/实验/硬件规格描述完整
- Summary: 提出PolyTouch多模态触觉手指（相机触觉+声学+外围视觉），耐用性超GelSight Mini 20倍（35hr vs 1-3.3hr），单指成本$61，基于T3+CLIP+AST编码器和cross-attention的tactile-diffusion policy在4个双臂任务上成功率提升最多34%（鸡蛋装盘100% vs 66%）。


## Problem

在非结构化家庭环境中实现鲁棒灵巧操控面临挑战：
1. **触觉盲策略局限**：仅依赖外部视觉/本体感觉的策略在遮挡、视觉复杂场景、精确接触控制中表现不足
2. **现有触觉传感器耐用性差**：GelSight Mini标准凝胶在1-3.3小时内即失效（撕裂/脱层/掉漆）
3. **制造门槛高**：现有传感器需专业设备和技能，阻碍大规模采用
4. **单一模态不够**：相机触觉（高空间分辨率但低频率）、声学（高频率但低空间分辨率）各有局限


## Method

### 硬件设计
- **触觉感知**：IMX708相机，蓝光LED(450nm)照明，荧光粉/绿漆发光，黄色滤光膜平衡光谱，曲面镜扩大FoV至100mm×25mm
- **声学感知**：压电式接触麦克风，48kHz采样，与视频同步（Raspberry Pi编码）
- **外围视觉**：两个亚克力侧窗+镜面，可见触觉面周围和下方区域
- **弹性体方案**：VHB（3层透明胶带+45μm铝粉，粘性自粘无脱层）或硅胶（XP-565+灰色硅胶墨）
- **保护层**：3M Nextcare Soft & Stretch胶带（类人类皮肤质感，不易起皱）
- **成本**：~$61/指（相机$35+麦克风$8+HDMI板$7+LED板$5+亚克力$3+胶带$3）
- **尺寸**：51mm(L)×59mm(W)×122mm(H)

### 策略学习
- **编码器**：T3（触觉+外围视觉，预训练ViT）、CLIP（腕部+场景视觉，预训练ViT）、AST（声学，log-mel频谱图→预训练ViT）、MLP（本体感觉，scratch）
- **模态组合器**：6块12头Cross-Attention融合触觉/外围视觉与场景视觉，其余模态池化后拼接投影
- **Diffusion Policy**：U-Net变体，观测历史2步，动作预测16步，执行8步
- **训练**：500 epochs，batch 10，AWS G5.48xLarge（8×A10G）


## Experiments

### 耐久性测试
- **对比**：PolyTouch-VHB vs GelSight Mini（两种标准凝胶+XP-565定制凝胶）
- **条件**：Franka Panda持续在刮刀手柄上摩擦，力10-30N随机，6D运动随机
- **结果**：PolyTouch-VHB 35hr无故障 | GelSight标准凝胶1.0hr撕裂/3.3hr掉漆 | XP-565凝胶25.0hr掉漆

### 双臂操控任务（3种网络变体 × 4任务）
- **visuo-proprio**：4个相机（2腕+2场景）+ 本体感觉，无触觉/声学
- **multi-concate**：全模态，直接拼接无cross-attention
- **multi-crossatn**：全模态 + cross-attention（提出方法）

| 任务 | 数据量 | visuo-proprio成功率 | multi-crossatn成功率 | 绝对提升 |
|------|--------|--------------------|--------------------|---------|
| 扳手插入 | ~200 | 0% | 18% | +18% |
| 水果分类 | ~150 | 33% | 46% | +13% |
| 鸡蛋敲开 | ~70 | 50% | 54% | +3% |
| 鸡蛋装盘(全) | ~150 | 66% | 100% | +34% |
| 鸡蛋装盘(1/3) | ~50 | 0% | 0% | 0% |

### 关键发现
1. 触觉策略消除力度控制失败模式（插入扳手过度用力/舀蛋力度不足）
2. 外围视觉减少抓取精度问题（visuo-proprio 11次 vs 触觉策略平均3次）
3. 触觉在视觉相似物体区分上关键（黑莓vs蓝莓：80% vs 20%）
4. 更多模态需要更多数据才能发挥全部潜力


## Limitations

1. VHB弹性体存在磁滞（丙烯酸泡沫粘度导致响应较慢），可用时序差分图像和外周视觉信号缓解
2. 多模态策略在大数据量时优势明显（全数据34%提升），小数据时优势减弱（1/3数据0%提升）
3. 仅在4个特定双臂任务上验证，未测试泛化性
4. 任务成功率整体偏低（扳手插入最高仅18%，说明任务本身难度大）


## Key Takeaways

1. VHB胶带作为触觉弹性体是突破性创新：5分钟制作、无脱层、20倍寿命提升
2. 三模态融合（触觉+声学+外围视觉）覆盖不同时间尺度需求，cross-attention是有效融合方式
3. 触觉反馈对力控制和纹理区分不可替代，仅视觉的策略存在结构性缺陷
4. 低成本（$61/指）和易制造性使大规模数据采集和策略训练成为可能
5. 来自MIT CSAIL + Toyota Research Institute，Edward Adelson（GelSight发明人）组

## 相关概念

- [[robotic-manipulation]]
- [[imitation-learning]]
- [[diffusion-model]]
- [[robot-learning]]
- [[vision-language-model]]
- [[tactile-sensing]]
- [[bimanual-manipulation]]
- [[grasping]]

## 相关研究者

- [[zhao|Zhao, Jialiang]]
- [[kuppuswamy|Kuppuswamy, Naveen]]
- [[feng|Feng, Siyuan]]
