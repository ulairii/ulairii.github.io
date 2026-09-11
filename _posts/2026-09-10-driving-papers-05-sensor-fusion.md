---
title: '05: Sensor fusion: PointPainting and BEVFusion'
date: '2026-09-10'
permalink: /autonomous-driving-perception/05-sensor-fusion/
excerpt: Cameras provide dense appearance information; lidar provides direct surface geometry; radar can provide range and
  radial velocity. Combining them is useful only if the network receives evidence that is correctly aligned and still informative.
  The central question in sensor fusion is where the streams meet.
tags:
- autonomous driving
series: perception
series_number: 5
read_time: false
reading_minutes: 5
redirect_from:
- /autonomous-driving-perception/15-fusion/
---

{% include perception-series-nav.html %}

Cameras provide dense appearance information; lidar provides direct surface geometry; radar can provide range and radial velocity. Combining them is useful only if the network receives evidence that is correctly aligned and still informative. The central question in sensor fusion is **where the streams meet**.

A fusion architecture can combine measurements, learned features, or final detections. Those choices impose different information bottlenecks and different dependencies between sensor branches.

## PointPainting: attach image semantics to measured points

[PointPainting — Vora et al., CVPR 2020](https://arxiv.org/abs/1911.10150) first runs semantic segmentation on the camera images. It projects lidar points into those images and appends the corresponding class scores to each point. An existing lidar detector then processes this enriched point cloud.

This gives each measured point both geometry and semantic evidence. A point on a vehicle can carry image-based evidence that it belongs to a vehicle, rather than forcing the lidar encoder to infer everything from sparse shape alone.

The interface is also restrictive: image information is transferred at the locations where lidar points exist. Dense image evidence between those points is not preserved as an independent spatial representation. Because image segmentation precedes painting, its errors and latency affect the downstream detector.

## BEVFusion: preserve two feature streams before joining them

[BEVFusion — Liu et al., ICRA 2023](https://arxiv.org/abs/2205.13542) constructs camera and lidar features in a shared BEV coordinate system, then fuses them for downstream tasks. This is the paper subtitled *Multi-Task Multi-Sensor Fusion with Unified Bird's-Eye View Representation*; other papers use the same short name.

The camera branch can contribute a dense BEV feature field without restricting every contribution to a lidar return. The lidar branch supplies geometrically grounded features. The shared grid makes their combination suitable for tasks such as 3D detection and map segmentation.

The work also addresses the computational cost of BEV pooling. A view transformation is not merely a conceptual arrow in a diagram: moving and aggregating features can be a major runtime cost.

<figure>
  <a href="{{ '/images/driving-papers/05.svg' | relative_url }}" style="width:100%;" aria-label="Open architecture diagram at full size"><img src="{{ '/images/driving-papers/05.svg' | relative_url }}" alt="Sensor fusion: PointPainting and BEVFusion: a comparison of the information passed between the methods' main stages." width="760" height="460" style="height:auto;" loading="lazy"></a>
  <figcaption>Original schematic of the methods discussed here; simplified information flow, not a reproduction of a paper's complete architecture.</figcaption>
</figure>

## Why a shared coordinate system is necessary but insufficient

Imagine a camera feature and a lidar feature both assigned to a cell ten meters ahead. They are spatially compatible only if calibration, sensor timestamps, and vehicle motion have been handled consistently. Otherwise, the network may combine a vehicle's current geometry with its earlier appearance.

There is another subtlety: projection does not establish visibility. A 3D point can project to an image location where a nearer surface blocks it. Sensor placement and occlusion therefore affect which features should be trusted.

These are engineering consequences of the fusion interface, not problems attention automatically removes. A learned weighting mechanism can use patterns present in its training data; it cannot guarantee correct correspondence under arbitrary calibration error.

## More sensors and larger models are different interventions

[Simple-BEV — Harley et al., ICRA 2023](https://arxiv.org/abs/2206.07959) studies choices affecting BEV perception, including sensor inputs and practical training settings. It is valuable here because an architectural comparison can otherwise bundle several changes into a single headline result.

For example, adding a camera branch might also increase input resolution, backbone capacity, temporal context, and training time. A higher score then does not isolate the benefit of the fusion operator. Sensor fusion should be compared with strong single-sensor baselines under clearly stated conditions.

| Interface | Evidence passed onward | Main dependency |
|---|---|---|
| Painted points | Geometry plus image class scores | Lidar sampling and image segmentation |
| Shared BEV features | Spatial features from each branch | View transformation and alignment |
| Final detections | Boxes, classes, and confidence | Information retained by each detector |

## What the planner ultimately receives

A fused detector can still output only boxes. If the planner needs lane boundaries or uncertain free space, those tasks need their own outputs or access to a richer representation. Adding sensors does not decide the downstream interface.

Conversely, keeping two branches does not by itself guarantee resilience when one sensor fails. A model trained only with both streams may rely heavily on one of them. Missing-input behavior must be trained and evaluated deliberately.

The architectural advance is the ability to preserve complementary evidence before task-specific compression. The next question is how to turn those features into persistent actors and road structure that prediction and planning can use.

{% include perception-series-nav.html %}
