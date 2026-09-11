---
layout: single
title: "How Self-Driving Cars See: A History of Deep Learning for Perception"
permalink: /autonomous-driving-perception/
author_profile: true
read_time: false
---

How does a collection of images and distance measurements become a useful description of a busy road? This series follows that question from image recognition to three-dimensional detection, sensor fusion, temporal perception, and occupancy, then considers how perception connects to driving.

Each chapter is written in plain English for readers without a background in the field. Allow about **10 minutes per chapter**, including the diagrams. Technical terms are introduced when needed, and original papers are linked for optional further reading.

The chapters follow a learning order. The dates indicate broad periods of development, not a sequence in which each new method replaced everything before it. Camera, lidar, and radar methods have developed alongside one another.

**Start here:** [Chapter 1: What does a car need to know at an intersection?]({{ '/autonomous-driving-perception/01-intersection/' | relative_url }})

All **24 chapters are available**. Read them in order, or use the groups below to revisit a topic. The series covers foundations from 2012 onward and selected research developments through 2025; it is a history of methods, not a continuously updated leaderboard.

## First, understand the problem

**01. [What does a car need to know at an intersection?]({{ "/autonomous-driving-perception/01-intersection/" | relative_url }})**

Start with one road scene and separate perception, tracking, prediction, planning, and control.

**02. [What do cameras, lidar, and radar actually measure?]({{ "/autonomous-driving-perception/02-sensors/" | relative_url }})**

Understand the evidence each sensor provides and the conditions that make it unreliable.

**03. [How does a neural network learn to recognize a car?]({{ "/autonomous-driving-perception/03-learning/" | relative_url }})**

Learn the essentials of features, training examples, losses, and generalization.

**04. [How does a pixel become a position on the road?]({{ "/autonomous-driving-perception/04-geometry/" | relative_url }})**

Connect image coordinates, camera geometry, depth, and the car’s coordinate system.

## Finding the world in images · roughly 2013–2017

**05. [From recognizing a car to finding it in a picture]({{ "/autonomous-driving-perception/05-region-detection/" | relative_url }})**

Follow region proposals, shared image features, and bounding boxes through the R-CNN family.

**06. [Detecting objects fast enough to drive]({{ "/autonomous-driving-perception/06-fast-detection/" | relative_url }})**

Understand one-stage detection, small objects, duplicate boxes, and the speed–accuracy tradeoff.

**07. [Giving every pixel a meaning]({{ "/autonomous-driving-perception/07-segmentation/" | relative_url }})**

Explore segmentation, road boundaries, lane markings, and traffic signals.

**08. [Why a correct image box is not enough]({{ "/autonomous-driving-perception/08-why-3d/" | relative_url }})**

See why distance, size, and orientation are essential for reasoning about physical space.

## Moving into three dimensions · roughly 2017–2021

**09. [How can a network read a cloud of points?]({{ "/autonomous-driving-perception/09-pointnet/" | relative_url }})**

Understand unordered points, point features, and local structure.

**10. [Dividing space into voxels]({{ "/autonomous-driving-perception/10-voxels/" | relative_url }})**

Follow voxel encoding and sparse convolution, including their memory costs.

**11. [Turning a point cloud into a bird’s-eye view]({{ "/autonomous-driving-perception/11-pillars-centers/" | relative_url }})**

Connect PointPillars to CenterPoint and examine what these representations preserve.

**12. [Estimating three-dimensional objects with cameras]({{ "/autonomous-driving-perception/12-camera-3d/" | relative_url }})**

Explore depth ambiguity, geometric assumptions, pseudo point clouds, and direct box prediction.

## Bringing observations together · roughly 2020–2023

**13. [Building one bird’s-eye view from several cameras]({{ "/autonomous-driving-perception/13-lift-splat-shoot/" | relative_url }})**

Explain Lift-Splat-Shoot through depth distributions, projection, and feature aggregation.

**14. [Letting a map query the images]({{ "/autonomous-driving-perception/14-bevformer/" | relative_url }})**

Introduce attention through BEVFormer’s spatial and temporal operations.

**15. [Combining cameras, lidar, and radar]({{ "/autonomous-driving-perception/15-fusion/" | relative_url }})**

Compare fusion stages and explain alignment, synchronization, and BEVFusion.

**16. [Remembering what happened a moment ago]({{ "/autonomous-driving-perception/16-tracking/" | relative_url }})**

Connect tracking, motion compensation, temporal features, and errors from stale observations.

## Choosing how to represent the world · from around 2022

**17. [Drawing lanes and intersections as a local map]({{ "/autonomous-driving-perception/17-maps/" | relative_url }})**

Move from pixels to lines, lane connections, and road topology.

**18. [Computing only where it helps: sparse perception]({{ "/autonomous-driving-perception/18-sparse-perception/" | relative_url }})**

Explain object queries, spatial sampling, and temporal state with Sparse4D.

**19. [What if the obstacle has no familiar name?]({{ "/autonomous-driving-perception/19-occupancy/" | relative_url }})**

Introduce occupancy, semantic occupancy, free space, unknown space, and supervision.

**20. [Representing a world that moves]({{ "/autonomous-driving-perception/20-motion/" | relative_url }})**

Separate temporal reconstruction, scene flow, occupancy flow, and future prediction.

## Connecting perception to driving

**21. [Does better perception produce better driving?]({{ "/autonomous-driving-perception/21-planning/" | relative_url }})**

Use UniAD to explain task interaction, joint training, and different meanings of end-to-end.

**22. [Learning beyond the labeled examples]({{ "/autonomous-driving-perception/22-pretraining/" | relative_url }})**

Examine pretraining, automatic labels, open vocabulary, and vision-language models.

**23. [Can a car predict how the world will change?]({{ "/autonomous-driving-perception/23-world-models/" | relative_url }})**

Explain world models, action conditioning, simulation, and their limits.

**24. [How do we know the system works?]({{ "/autonomous-driving-perception/24-evaluation/" | relative_url }})**

Return to the intersection with evaluation, latency, rare events, and closed-loop behavior.

## How to read the series

Start at Chapter 1 if the subject is new to you. Each chapter introduces a practical problem, explains a method, and examines what information it can lose. Diagrams are created for this series unless a caption says otherwise. Sources are linked beside the claims they support.

As you read, keep asking: **What goes in? What comes out? What can this representation miss?**
