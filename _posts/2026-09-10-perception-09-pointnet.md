---
title: 'How Self-Driving Cars See — 09: How can a network read a cloud of points?'
date: '2026-09-10'
permalink: /autonomous-driving-perception/09-pointnet/
excerpt: Lidar gives us points in meters, which seems like an immediate advantage over image pixels. But the points arrive as an irregular collection. Some objects have many returns, others have few, and their order in memory need not have any spatial meaning.
tags:
- autonomous vehicles
- perception
- deep learning
- perception series
series_number: 9
read_time: false
---

{% include perception-series-nav.html %}

Lidar gives us points in meters, which seems like an immediate advantage over image pixels. But the points arrive as an irregular collection. Some objects have many returns, others have few, and their order in memory need not have any spatial meaning.

Early deep learning methods for point clouds had to decide how to handle that structure. PointNet made a simple choice: process points with a shared function, then combine them in a way that does not depend on their order. Understanding that decision will help us compare point, voxel, and pillar representations.

## Why reshaping points into an image is not enough

An image grid has a useful neighborhood structure. Adjacent entries usually describe adjacent directions in the camera view. A small convolutional filter can exploit that relationship. In an arbitrary list of lidar points, the next row may belong to a different object several meters away.

If we shuffle the list without moving any point, the physical scene is unchanged. A suitable model should not change its scene-level answer simply because the file stores those points in a different order. This property is called **permutation invariance**.

For a per-point output, we want a related behavior: shuffling input points should shuffle the corresponding outputs, while preserving each point's result. That is often called permutation equivariance. The distinction is about whether the output is one global description or a list tied to the input elements.

Some sensor-specific projections create useful grids from point clouds, such as organizing returns by beam direction. Those are legitimate alternatives. But they impose their own representation choices, including how to handle missing returns and points that share a projected location.

## PointNet applies a shared function to each point

[PointNet, by Qi and colleagues, CVPR 2017](https://arxiv.org/abs/1612.00593), learns per-point features and uses a symmetric aggregation operation to produce a global feature. Because the same transformation is applied to each point and the aggregation ignores order, the representation can satisfy the desired invariance.

A shared multilayer perceptron is a small neural network applied independently to each point's input values. Those values may include coordinates and other available attributes. After transformation, each point has a learned feature vector rather than only an XYZ position.

A common aggregation is maximum pooling across points for each feature channel. It keeps the largest response in each channel. A different point may supply the maximum for each channel, so the final vector summarizes several kinds of evidence across the set.

This is not the same as choosing the physically highest point. Pooling operates on learned feature values, not necessarily on raw height. The operation is best understood as retaining the strongest response to each learned measurement.



<figure>
  <a href="{{ '/images/perception-series/09.svg' | relative_url }}" aria-label="Open diagram at full size" style="width:100%;"><img src="{{ '/images/perception-series/09.svg' | relative_url }}" alt="Three unordered points pass through the same feature function and then a maximum operation. Reordering the points produces the same pooled vector." width="720" height="460" style="height:auto;" loading="lazy"></a>
  <figcaption>A symmetric aggregation makes the global result independent of point order. Coordinates and feature values are illustrative. Original diagram for this series.</figcaption>
</figure>

## A small numerical example makes pooling concrete

Suppose three points produce two-channel features: (2, 1), (0, 4), and (3, 2). Channel-wise maximum pooling gives (3, 4). Reordering the three input vectors gives the same result.

That stability solves the storage-order problem. It also reveals information loss. The pooled vector does not preserve every feature value or tell us directly which points were neighbors. Many different sets can share the same pooled result.

A learned representation can retain information needed for a particular task without retaining the entire input. For classification, that may be sufficient. For detailed geometry, we need to examine what local relationships are available before and after aggregation.

This is a recurring theme: a compact representation is useful precisely because it discards information. The question is whether it discards information the downstream task still needs. There is no universally best compression independent of the task.

## Global and local features answer different questions

A global feature can help classify an object or provide context for segmentation. A per-point segmentation model can combine a point's own features with the global summary, then predict a label for that point. The global information helps interpret local ambiguity.

However, a function applied independently to each point does not directly compare that point with its immediate neighbors before global pooling. Local surface shape may require relationships among nearby points: a flat patch, a curved edge, or a narrow vertical structure.

[PointNet++, by Qi and colleagues, NeurIPS 2017](https://arxiv.org/abs/1706.02413), addresses local structure through hierarchical processing of neighborhoods. At a high level, it chooses representative locations, groups nearby points, summarizes each neighborhood, and repeats at larger spatial scales.

The neighborhood definition introduces new choices. A fixed radius corresponds to a physical distance, while a fixed number of neighbors can span different physical extents in dense and sparse regions. Neither choice automatically handles every variation in lidar density.

## A road scene is larger than a single object crop

PointNet is foundational, but its original tasks should not be confused with a complete road detector. A full driving scene contains multiple objects, ground, buildings, and large empty regions. Detecting objects requires locating and separating them, then estimating their geometry.

One bridge between image detection and point processing is [Frustum PointNets, by Qi and colleagues, CVPR 2018](https://arxiv.org/abs/1711.08488). It uses image detections to select three-dimensional frustums, then processes the points within those candidate regions for object understanding.

A **frustum** is the expanding region of space defined by an image region over a depth range. The image box narrows the search direction, while the points inside provide metric geometry. The method illustrates how two representations can divide the work.

It also creates a dependency: an image proposal that misses an object can prevent later point processing from considering it. Restricting computation to candidates is efficient, but the candidate stage influences what evidence reaches the rest of the system.

## Density and visibility shape the input

The truck side may contain a broad patch of returns. The cyclist may have only a few points, and some may come from different bicycle components. A point model must handle that uneven evidence without assuming each object is sampled equally well.

Sampling points down to a fixed budget can reduce computation. It can also remove small or thin structures. The effect depends on the sampling strategy and the distribution of returns. A uniform point budget does not imply uniform information retention across objects.

Accumulating several lidar sweeps can provide more points, but only if coordinates and time are handled correctly. A moving cyclist can become a trail when old points are transformed using only the car's motion. More points can mean more inconsistent geometry rather than more useful evidence.

These issues belong to the measurement and representation, not just to optimization. A larger point network cannot reliably recover a detailed surface that was never observed unless it relies on learned shape assumptions. That may help, but the source of information should be clear.

## Coordinates carry assumptions too

A point network can receive absolute coordinates, coordinates relative to a neighborhood center, or both. Absolute position tells the model where a point lies in the sensor frame. Relative coordinates emphasize local shape and can reduce sensitivity to translation.

For driving, vertical position relative to the road can be useful. But the sensor's mounting and the road slope affect raw height coordinates. A model trained with one convention may not transfer cleanly to another unless the inputs are normalized or transformed appropriately.

Features such as lidar return intensity can provide additional evidence, but their meaning depends on the sensor and processing. Treating an attribute as universally comparable across devices can introduce a hidden domain shift.

The model's input specification is therefore part of the method. When reproducing a point-cloud result, check coordinate conventions, selected attributes, range limits, sampling, and temporal accumulation before attributing differences solely to network architecture.

## Try changing one point

Return to the three feature vectors (2, 1), (0, 4), and (3, 2). If the first becomes (1, 0), the maximum remains (3, 4). That point changed without affecting the pooled result. If the second becomes (0, 1), the second pooled channel falls to 2.

The example shows both robustness and selectivity. Some changes are ignored because other points supply stronger responses; others alter the summary. A learned encoder determines what those responses mean. It does not make maximum pooling an exact record of all points. For a small road object, the practical issue is whether its evidence creates a useful response before the aggregation discards the rest.

## Check your understanding

Why does max pooling solve the ordering problem? The maximum of a set of values is unchanged by rearranging them. Shared per-point processing followed by that aggregation can therefore produce the same global vector after a shuffle.

Does order invariance mean the model preserves all geometry? No. Aggregation compresses the set, and local relationships may need explicit neighborhood processing.

Point methods respect irregular inputs directly. Next we will explore the alternative: organize points into a regular three-dimensional grid so that learned local operations can use a more structured neighborhood.

{% include perception-series-nav.html %}
