---
title: '03: Camera BEV: Lift-Splat-Shoot, BEVDepth, and BEVFormer'
date: '2026-09-10'
permalink: /autonomous-driving-perception/03-camera-bev/
excerpt: 'Camera-only 3D perception must solve two problems together: recognize visual content and place it in physical space.
  Multiple cameras increase coverage, but their feature maps still live in different perspective views. Lift-Splat-Shoot,
  BEVDepth, and BEVFormer offer influential ways to construct a shared bird''s-eye-view representation.'
tags:
- autonomous driving
series: perception
series_number: 3
read_time: false
reading_minutes: 5
redirect_from:
- /autonomous-driving-perception/04-geometry/
- /autonomous-driving-perception/08-why-3d/
- /autonomous-driving-perception/12-camera-3d/
- /autonomous-driving-perception/13-lift-splat-shoot/
- /autonomous-driving-perception/14-bevformer/
---

{% include perception-series-nav.html %}

Camera-only 3D perception must solve two problems together: recognize visual content and place it in physical space. Multiple cameras increase coverage, but their feature maps still live in different perspective views. Lift-Splat-Shoot, BEVDepth, and BEVFormer offer influential ways to construct a shared bird's-eye-view representation.

The distinction is **which side initiates the transformation**. Image features can be distributed into space, or locations in space can retrieve evidence from the images.

## Lift-Splat-Shoot: distribute each pixel along its depth ray

[Lift-Splat-Shoot — Philion and Fidler, ECCV 2020](https://arxiv.org/abs/2008.05711) predicts a visual feature and a distribution over discrete depths at each image location. For a feature `f` and depth probability `p(d)`, the contribution at depth `d` is conceptually `p(d) × f`.

Using camera calibration, those contributions are placed in 3D and pooled into BEV cells. Evidence from different cameras can then meet in the same grid. The original work also demonstrates using the BEV representation for downstream tasks including planning through trajectory scoring.

A distribution is important because the image may not determine a single reliable depth. However, distributed evidence can also become spatially blurred. If depth is wrong, the appearance feature is assigned to the wrong part of the road.

The method learns the view transformation through task supervision; it does not require ground-truth depth as the central supervision mechanism of its original design.

<figure>
  <a href="{{ '/images/driving-papers/03.svg' | relative_url }}" style="width:100%;" aria-label="Open architecture diagram at full size"><img src="{{ '/images/driving-papers/03.svg' | relative_url }}" alt="Camera BEV: Lift-Splat-Shoot, BEVDepth, and BEVFormer: a comparison of the information passed between the methods' main stages." width="760" height="460" style="height:auto;" loading="lazy"></a>
  <figcaption>Original schematic of the methods discussed here; simplified information flow, not a reproduction of a paper's complete architecture.</figcaption>
</figure>

## BEVDepth: make depth a directly supervised component

[BEVDepth — Li et al., AAAI 2023](https://arxiv.org/abs/2206.10092) focuses on this placement problem. It incorporates camera information in depth estimation and uses lidar-derived depth supervision during training, along with refinements to depth-related feature processing.

The distinction between training and inference matters. A camera-only inference model may still use lidar measurements to create training targets. That is different from consuming a lidar point cloud each time the deployed model predicts a scene.

The methodological lesson is that a representation's hidden bottleneck can deserve its own supervision. If image features are strong but placed at the wrong distances, improving the detector head alone addresses the wrong part of the pipeline.

Depth labels are also incomplete observations. A projected lidar return supervises a visible surface sample; it does not provide dense, perfect depth for every image pixel.

## BEVFormer: let BEV locations retrieve image evidence

[BEVFormer — Li et al., ECCV 2022](https://arxiv.org/abs/2203.17270) starts from learned queries associated with BEV locations. Geometric reference points connect those queries to relevant camera views, and spatial cross-attention gathers image features. Temporal self-attention also incorporates information from earlier BEV features.

Here a *query* is a learned feature used to request relevant evidence. It is not a text question. Geometry narrows where the network looks; attention learns how to combine the selected information.

BEVFormer therefore differs from explicitly distributing every image feature across predicted depth bins. It also makes temporal information part of the BEV construction, rather than treating each frame as an isolated scene.

| Method | Main transformation | Where depth or geometry enters |
|---|---|---|
| Lift-Splat-Shoot | Image features are lifted and pooled | Predicted depth distribution and calibration |
| BEVDepth | Depth-guided lifting with stronger depth learning | Camera-aware estimation and training depth targets |
| BEVFormer | BEV queries gather image features | Projected 3D references and temporal alignment |

## Shared failure modes explain the next design choices

All three approaches depend on consistent coordinates. Camera calibration specifies how a point in vehicle coordinates projects into an image. When history is used, vehicle motion must also be accounted for. A stationary building appears to move in the camera as the car advances; a moving vehicle has additional motion of its own.

Temporal aggregation can fill gaps and stabilize estimates, but it can also preserve stale evidence. Aligning the ego vehicle does not align every independently moving object. Likewise, a finer BEV grid provides more spatial locations without creating missing depth evidence.

These distinctions guide useful comparisons. Match camera resolution, temporal context, training supervision, and spatial range before attributing an improvement to the view transformation alone.

BEV gives detection, mapping, and planning a common spatial language. It is not the only possible language. The next chapter examines methods that preserve a smaller set of object features and retrieve image evidence for those objects, avoiding a dense scene grid as the mandatory intermediate representation.

{% include perception-series-nav.html %}
