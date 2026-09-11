---
layout: single
title: "From Perception to Planning: Key Papers in Autonomous Driving"
permalink: /autonomous-driving-perception/
author_profile: true
read_time: false
redirect_from:
  - /autonomous-driving-perception/22-pretraining/
---

A concise history of autonomous-driving perception and motion planning through the papers that changed their representations, architectures, and training objectives. **12 articles**, usually **5–6 minutes each**, cover selected developments from **2012 to 2025**.

The series follows a technical dependency order rather than a strict publication timeline: image and 3D representations → scene structure and prediction → trajectory planning and evaluation. The date ranges below place each group of papers in context. These approaches often coexist; newer does not automatically mean better.

**[Start with image perception]({{ '/autonomous-driving-perception/01-image-detection/' | relative_url }})** · **[Go directly to trajectory planning]({{ '/autonomous-driving-perception/09-trajectory-planning/' | relative_url }})** · **[Back to Blog]({{ '/year-archive/' | relative_url }})**

Each article explains the main computation, the reason for the design, and its tradeoffs, with a simple architecture diagram and links to the original papers. Basic concepts are introduced where they are needed.

## Image and 3D representations

### 01. [Image perception: R-CNN, YOLO, and FCN]({{ '/autonomous-driving-perception/01-image-detection/' | relative_url }})

**2012–2017** · R-CNN · Faster R-CNN · YOLO · RetinaNet · FCN

### 02. [Lidar perception: PointNet, VoxelNet, and CenterPoint]({{ '/autonomous-driving-perception/02-lidar-representations/' | relative_url }})

**2017–2021** · PointNet · VoxelNet · SECOND · PointPillars · CenterPoint

### 03. [Camera BEV: Lift-Splat-Shoot, BEVDepth, and BEVFormer]({{ '/autonomous-driving-perception/03-camera-bev/' | relative_url }})

**2020–2023** · Lift-Splat-Shoot · BEVDepth · BEVFormer

### 04. [Object queries: DETR3D, PETR, and Sparse4D]({{ '/autonomous-driving-perception/04-object-queries/' | relative_url }})

**2020–2024** · DETR · DETR3D · PETR · Sparse4D

### 05. [Sensor fusion: PointPainting and BEVFusion]({{ '/autonomous-driving-perception/05-sensor-fusion/' | relative_url }})

**2020–2023** · PointPainting · BEVFusion · Simple-BEV

## Scene structure and prediction

### 06. [Scene structure: tracking, MapTR, and road topology]({{ '/autonomous-driving-perception/06-tracks-and-maps/' | relative_url }})

**2016–2023** · SORT · AB3DMOT · MapTR · OpenLane-V2

### 07. [Occupancy and motion: SurroundOcc, Occ3D, and FIERY]({{ '/autonomous-driving-perception/07-occupancy-and-flow/' | relative_url }})

**2021–2023** · SurroundOcc · Occ3D · FIERY · Occupancy Flow Fields

### 08. [Motion prediction: VectorNet, LaneGCN, and MTR]({{ '/autonomous-driving-perception/08-motion-prediction/' | relative_url }})

**2020–2022** · VectorNet · LaneGCN · Motion Transformer

## Planning and evaluation

### 09. [Trajectory planning: search, learned costs, and ChauffeurNet]({{ '/autonomous-driving-perception/09-trajectory-planning/' | relative_url }})

**2016–2019** · Paden survey · Neural Motion Planner · ChauffeurNet

### 10. [Joint perception and planning: TransFuser and UniAD]({{ '/autonomous-driving-perception/10-joint-driving/' | relative_url }})

**2021–2023** · TransFuser · UniAD

### 11. [Efficient and generative planning: VAD and DiffusionDrive]({{ '/autonomous-driving-perception/11-vector-and-diffusion-planning/' | relative_url }})

**2023–2025** · VAD · DiffusionDrive

### 12. [Evaluating driving: nuPlan, PDM, NAVSIM, and world models]({{ '/autonomous-driving-perception/12-planning-evaluation/' | relative_url }})

**2021–2024** · nuPlan · PDM · NAVSIM · GAIA-1

## Scope

“Planning” here means local motion or trajectory planning: selecting the vehicle's future movement under road, interaction, and vehicle constraints. It is distinct from choosing a route through a city or tracking a trajectory with a low-level controller.

This is a selective paper history, not an exhaustive survey or a current leaderboard. General pretraining and vision-language models are outside the main thread. World models appear in the final article in relation to simulation and evaluation. The original 24-part introduction has been consolidated into this edition; old chapter links redirect to the relevant article or this guide.
