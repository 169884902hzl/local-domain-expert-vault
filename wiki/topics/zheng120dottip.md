---
title: "DotTip: Enhancing Dexterous Robotic Manipulation With a Tactile Fingertip Featuring Curved Perceptual Morphology"
tags: [manipulation]
created: "2026-04-25"
updated: "2026-04-25"
type: "literature"
status: "done"
summary: "提出DotTip三维曲面触觉指尖传感器，基于电容阵列（指纹传感器）+ 仿生微结构硅胶皮肤+半球形软覆盖层，有效接触面积528mm²（2.3倍于平面DotView），接触角度范围±45°，CNN（ResNet-18）估计接触角度和力，精度1.56°/0.28N，在摇杆操控任务中显著优于平面传感器DotView。"
authors: "Zheng, Haoran; Shi, Xiaohang; Bao, Ange; Jin, Yongbin; Zhao, Pei"
year: "2020"
venue: "IEEE Robotics and Automation Letters"
zotero_key: "94EGL9S8"
---
## 摘要

Tactile（触觉） sensing technologies enable robots to interact with the environment in increasingly nuanced and dexterous（灵巧） ways. A signiﬁcant gap in this domain is the absence of curved tactile（触觉） sensors, which are essential for performing sophisticated manipulation（操控） tasks. In this study, we present DotTip, a tactile（触觉） ﬁngertip featuring a three-dimensional curved perceptual surface that closely mimics human ﬁngertip morphology. A convolutional neural network-based deep learning framework precisely calculates the contact angles and forces from the sensor tactile（触觉） images, achieving mean errors of 1.56◦ and 0.28 N, respectively. DotTip’s performance is evaluated in real-world tasks, demonstrating its efﬁcacy in tactile（触觉） servoing, slip prevention, and grasping（抓取）, along with the more challenging benchmark task of controlling a joystick. These ﬁndings demonstrate that DotTip possesses superior 3D tactile（触觉） sensing capabilities necessary for ﬁne-grained dexterous（灵巧） manipulations compared to its ﬂat counterparts.


## 中文简述

提出基于触觉感知的抓取方法，具有接触丰富特点。

**研究方向**: 机器人操控

## 关键贡献

1. **DotTip传感器**：半球形曲面触觉指尖，有效接触面积528mm²（vs DotView 225mm²，提升2.3倍），接触角度范围±45°
2. **优化仿生突起设计**：圆柱基底+半球顶部（7×7阵列，1.1mm间距），FEM验证增强3D接触位置灵敏度
3. **CNN接触估计**：ResNet-18从触觉图像预测接触角度(θ,φ)和力(Fn,Fs1,Fs2)，精度1.56°/0.28N，接触定位精度0.53mm（优于人类指尖0.94mm）
4. **摇杆操控基准**：首次用摇杆操控作为触觉传感器灵巧操控对比基准，证明3D曲面触觉的优势
## 结构化提取

- Problem: 灵巧操控缺乏3D曲面触觉传感器，平面传感器在非平行接触时失效
- Method: DotTip曲面触觉指尖（半球形硅胶+仿生7×7微结构+电容阵列指纹传感器），ResNet-18 CNN估计接触角度和力
- Tasks: 触觉伺服、防滑抓取、三棱柱抓取、摇杆操控（含Snake游戏）
- Sensors: FPC1020AM电容阵列（192×192, 508dpi）、六轴力/力矩传感器(KMS40)、VIVE Tracker 3.0位姿追踪
- Robot Setup: Allegro Hand（四指全驱动灵巧手），Raspberry Pi 4B，RTX 4070推理
- Metrics: 角度RMSE/误差std/R²、力RMSE/误差std/R²、接触定位精度(0.53mm)、摇杆角度跟踪RMSE
- Limitations: 采样率低(33Hz)、软材料长期精度下降(~3月)、装配误差需迁移学习、系统延迟150ms、最大力9.4N
- Evidence Notes: 全文6626词，1张性能表，10张图，4个应用实验+视频补充材料，IEEE RA-L 2025
## 本地引用关系

- [[george2024vital]]
- [[han2025upvital]]
- [[röfer2025pseudotouch]]
- [[wu2025tacdiffusion]]
- [[zhao2025polytouch]]
## 证据元数据

- Fulltext Quality: fulltext
- Evidence Coverage: 完整全文（~6626 词），含 Table I、Figure 1-10、公式推导、CNN架构描述、4个应用实验
- Confidence: high — 全文可读，IEEE RA-L 2025，定量评估完整，对比基线清晰
- Summary: 提出DotTip三维曲面触觉指尖传感器，基于电容阵列（指纹传感器）+ 仿生微结构硅胶皮肤+半球形软覆盖层，有效接触面积528mm²（2.3倍于平面DotView），接触角度范围±45°，CNN（ResNet-18）估计接触角度和力，精度1.56°/0.28N，在摇杆操控任务中显著优于平面传感器DotView。


## Problem

现有触觉传感器大多采用平面感知面，在灵巧操控场景中存在不足：
1. **平面设计的局限**：平面传感器仅在接触面平行时提供有效触觉反馈，灵巧手手指难以维持可感知接触
2. **缺乏3D曲面感知**：人类指尖具有3D曲面形态，机器人灵巧操控需要类似的多方向接触感知
3. **现有曲面传感器问题**：分布式阵列易损坏（BioTac昂贵脆弱、uSkin分辨率低、InSight力范围小<2N、气动精度低）


## Method

### 传感器设计
- **感知核心**：FPC1020AM电容式指纹传感器（192×192像素，508dpi，8位灰度）
- **仿生微结构**：导电硅胶皮肤内表面7×7突起阵列（半球r=0.5mm + 圆柱基底，1.1mm间距），接触变形产生"点"图案
- **曲面覆盖**：EcoFlex 00-30硅胶半球形覆盖层（最厚5.6mm），传递接触变形
- **尺寸/成本**：21mm(W)×32mm(H)×34mm(T)，16g，~$30 USD
- **通信**：SPI→Raspberry Pi 4B→TCP，30ms/帧，单Pi连4个传感器25Hz

### CNN接触估计
- **网络**：ResNet-18(单通道输入)→512维→FC(64)→FC(16)→6维输出(θ,φ,Fn,Fs1,Fs2)
- **训练**：24558对数据（15分钟采集），batch 128，Adam lr=1e-4，200 epochs
- **采集**：六轴力/力矩传感器(KMS40) + VIVE Tracker 3.0位姿追踪，不同角度/力接触
- **推理**：ONNX部署在RTX 4070，~3ms/帧


## Experiments

### 定量评估（Table I）
- 接触角度：RMSE θ=1.64°, φ=1.70°，R²>96%
- 接触力：RMSE Fn=0.24N, Fs1=0.13N, Fs2=0.15N，R²>95%
- 总力中位误差：0.21N(<3.5N), 0.26N(3.5-6N), 0.37N(>6N)
- 角度中位误差：1.21°, 1.10°, 1.13°（三个力等级）

### 应用实验
1. **触觉伺服**：Allegro Hand跟踪人手运动维持2N法向力，30Hz控制，快速运动时偏差
2. **防滑抓取**：抓持灌沙塑料瓶，剪切/法向力比超阈值μ̂=0.5时自动增大法向力
3. **抓取三棱柱**：曲面触觉面允许非平行接触，比平面传感器运动空间更大
4. **摇杆操控（核心对比实验）**：
   - 无触觉反馈→快速脱离
   - DotView（平面）→初始好，大角度时脱离
   - DotTip（曲面）→全程稳定接触，RMSE最低，持续时间最长
   - 成功玩Snake游戏（摇杆信号映射）


## Limitations

1. 采样率受限于指纹传感器SPI频率（~33Hz），需更高速硬件
2. 软材料应力松弛影响长期精度（建议~3个月重新校准）
3. 装配误差导致传感器间差异，需迁移学习适应
4. 系统延迟~150ms影响快速响应
5. 最大力9.40N（相对其他传感器如SaLoutos的25N较小）
6. 仅单指实验，未展示多指协调操控


## Key Takeaways

1. 3D曲面触觉面对灵巧操控至关重要——平面传感器在大角度接触时丧失感知
2. 低成本指纹传感器作为电容阵列是巧妙选择：$30、高分辨率(508dpi)、商业可用
3. 15分钟数据采集+CNN即可获得高精度接触估计，数据效率高
4. 摇杆操控是评估触觉传感器灵巧操控能力的优秀基准任务
5. 来自浙大流体动力与机电系统国重实验室，Zhao Pei组

## 相关概念

- [[robotic-manipulation]]
- [[tactile-sensing]]
- [[bimanual-manipulation]]
- [[grasping]]

## 相关研究者

- [[zheng|Zheng, Haoran]]
