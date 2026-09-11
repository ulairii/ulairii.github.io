---
title: 'How Self-Driving Cars See — 10: Dividing space into voxels'
date: '2026-09-10'
permalink: /autonomous-driving-perception/10-voxels/
excerpt: The lidar cloud contains a broad truck side, a few bicycle returns, and scattered points from the road. Point-based networks can process that irregular collection directly. Another approach places the points into a regular grid so neighboring features have a clear spatial relationship.
tags:
  - autonomous driving
series_number: 10
read_time: false
series: perception
---

{% include perception-series-nav.html %}

The lidar cloud contains a broad truck side, a few bicycle returns, and scattered points from the road. Point-based networks can process that irregular collection directly. Another approach places the points into a regular grid so neighboring features have a clear spatial relationship.

A **voxel** is a small three-dimensional cell, analogous to a pixel in an image. Voxel methods combine the flexibility of learned point features with the regular neighborhoods of convolution. Their main challenge is that a fine three-dimensional grid can become very large, even when most cells contain no measured points.

## Assigning a point to a cell

First choose a region of interest and a cell size along each axis. For each point, subtract the grid origin, divide by the cell sizes, and take the integer cell indices. Points with the same indices belong to the same voxel.

For example, if cells are 0.2 meters wide and the horizontal origin is zero, a point at 1.13 meters falls into horizontal cell 5. The index identifies an interval, not the original precise coordinate. If we store only the index, we lose the point's offset within the cell.

A learned encoder can keep those offsets as input features. Points can carry their original coordinates, their displacement from the voxel center, or their displacement from the mean of points in that voxel. These quantities describe different aspects of local geometry.

The grid boundary matters too. Points outside the selected region are often discarded. That may be a sensible computational choice, but it defines where the model can use evidence. Extending the sensor range does not help a detector if its preprocessing removes the additional points.

## VoxelNet learns a description within each voxel

[VoxelNet, by Zhou and Tuzel, CVPR 2018](https://arxiv.org/abs/1711.06396), introduced learned voxel feature encoding for three-dimensional detection. It groups points, learns pointwise features with local aggregation, and uses the resulting voxel representation in a detection network.

The important change is that a voxel need not contain only a binary occupied flag or a hand-designed statistic. A learned vector can summarize the points' arrangement and attributes in ways useful for the training task.

Imagine two cells with the same number of returns. In one, the points form a nearly vertical surface; in the other, they lie near the road. A count alone cannot distinguish those structures. Coordinate relationships give a learned encoder more evidence.

Pooling still compresses information. The vector does not preserve an unlimited list of points. Its capacity, sampling limits, and training objective determine which distinctions remain accessible to later layers. Voxelization organizes the input; it does not remove the representation tradeoff.



<figure>
  <a href="{{ '/images/perception-series/10.svg' | relative_url }}" aria-label="Open diagram at full size" style="width:100%;"><img src="{{ '/images/perception-series/10.svg' | relative_url }}" alt="A sparse point cloud is grouped into grid cells. Only a few cells have features; a comparison shows the larger number of cells created by finer resolution." width="720" height="460" style="height:auto;" loading="lazy"></a>
  <figcaption>Grid size grows along all three axes. Sparse storage avoids allocating full feature vectors to every empty input cell. Original diagram for this series.</figcaption>
</figure>

## Why the third dimension is expensive

Consider an illustrative region 80 meters long, 80 meters wide, and 6 meters tall. With 0.2-meter cells along each axis, it contains 400 × 400 × 30 cells, or 4.8 million cells. At 32 float32 feature values per cell, one dense feature array alone is about 614 million bytes.

That estimate excludes gradients, intermediate activations, indexing structures, and other layers. It is not a memory measurement for a named model. It simply shows how quickly a dense representation can grow.

Halving the cell size along all three axes multiplies the number of cells by eight. A change that sounds like “twice the resolution” can therefore require far more than twice the storage. This is why resolution choices deserve physical interpretation.

Coarser cells reduce cost, but can merge nearby surfaces. The thin bicycle frame and a patch of background may enter the same cell. The network can retain some distinction through internal point offsets, yet its later spatial lattice is still coarser.

## Sparse convolution avoids computing everywhere

A lidar scan samples surfaces, leaving many grid cells without returns. **Sparse convolution** represents active locations and computes using their features, rather than storing and processing every location in the bounding volume as a dense array.

[SECOND, by Yan, Mao, and Li, Sensors 2018](https://pmc.ncbi.nlm.nih.gov/articles/PMC6210968/), applies sparse convolution in a voxel-based three-dimensional detector. It illustrates how computational organization can make a geometric representation more practical without changing the sensor itself.

Sparse computation needs bookkeeping. The implementation must find which active input coordinates contribute to each output coordinate. Index generation and memory access have costs. A lower arithmetic count therefore does not translate automatically into the same proportional wall-clock speedup.

Different sparse operations also treat output locations differently. Some can activate neighboring locations as information propagates. Others preserve the active pattern under specified conditions. The exact operation affects both efficiency and how features spread through space.

## Preserving sparsity changes neighborhood communication

Repeated ordinary sparse convolutions can expand the set of active locations. That growth may be useful for communication, but it can reduce the advantage of sparsity. **Submanifold sparse convolution** restricts outputs to an existing active pattern for appropriate layer configurations.

[Graham, Engelcke, and van der Maaten, CVPR 2018](https://arxiv.org/abs/1711.10275), explain this idea in the context of three-dimensional semantic segmentation. Its role here is to show that “sparse convolution” names a family of choices, not one universal operation.

Preserving an active pattern does not mean the model knows that all other cells are physically empty. In a raw lidar grid, inactive can mean no point was stored there. It may reflect occlusion, limited range, or sampling, rather than observed free space.

That semantic distinction is essential. The computational mask saying where features exist is not automatically an occupancy label. Chapter 19 will separate measured surfaces, free-space evidence, and unknown regions more carefully.

## What happens after voxel features are computed?

A detector can process the three-dimensional feature volume and then transform or compress it into a bird's-eye-view representation for prediction. The top view provides convenient horizontal geometry for road objects while retaining some height information in its channels.

The prediction head may use reference boxes, centers, or other encodings. Voxelization describes how measurements are represented and encoded; it does not uniquely determine the detector's output parameterization. Those are separate design decisions.

This separation helps read comparisons. Two detectors can share a voxel backbone and use different heads. Two others can share a center-based head while using different point encoders. An improvement in one part should not be attributed automatically to another.

For the truck, the voxel representation preserves a structured neighborhood of measured surfaces. The detection head turns those features into a compact box estimate. Each step changes what information is explicit and what must be carried indirectly in learned channels.

## Sampling caps can introduce less visible losses

Implementations often limit the number of points per voxel and the total number of voxels. Such caps bound computation, but discarded points and cells are no longer available to the model. The effect can vary with scene density and sensor configuration.

A cap chosen for one lidar may behave differently with a denser sensor. A crowded intersection can reach limits that an empty road never approaches. The sampling order can also matter unless the selection policy is controlled.

These details are easy to overlook because they occur before the main network. Yet they can affect small objects, distant objects, and reproducibility. A method description should record cell sizes, coordinate range, sampling strategy, and feature inputs.

The same principle applies to runtime results. Preprocessing and sparse index construction belong in a complete latency measurement when the deployed system must perform them for every observation.

## A cell boundary example

Two points at horizontal positions 0.199 and 0.201 meters are only two millimeters apart, but lie in different 0.2-meter cells when the grid starts at zero. Two other points farther apart can still share one cell. Grid membership is a computational partition, not a complete measure of geometric similarity.

Keeping relative coordinates helps the encoder retain within-cell structure. Neighboring convolution then allows information to cross cell boundaries. Neither step makes resolution irrelevant: the lattice still influences which features are grouped and how much detail later layers preserve. This small example explains why changing cell size or origin can change the representation even when the physical cloud is almost unchanged.

## Check your understanding

What happens to the cell count if every cell edge is halved? For a fixed three-dimensional volume, the count grows by eight. Feature channels and numerical precision then determine storage per cell.

Does an inactive voxel mean free space? Not necessarily. It may only mean no point was stored there. Absence of a return and evidence of empty space are different.

Voxel methods provide structured three-dimensional computation, but height resolution is costly. Next we will study a deliberate simplification: group points into vertical columns and use a two-dimensional network, then detect objects through their centers.

{% include perception-series-nav.html %}
