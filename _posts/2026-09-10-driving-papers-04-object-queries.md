---
title: '04: Object queries: DETR3D, PETR, and Sparse4D'
date: '2026-09-10'
permalink: /autonomous-driving-perception/04-object-queries/
excerpt: A dense BEV grid allocates features across an entire region, including empty road. If the required output is a set
  of objects, another design is to maintain a set of object hypotheses and gather only the evidence needed to refine them.
  DETR3D, PETR, and Sparse4D explore this direction through different uses of geometry and time.
tags:
- autonomous driving
series: perception
series_number: 4
read_time: false
reading_minutes: 5
redirect_from:
- /autonomous-driving-perception/18-sparse-perception/
---

{% include perception-series-nav.html %}

A dense BEV grid allocates features across an entire region, including empty road. If the required output is a set of objects, another design is to maintain a set of object hypotheses and gather only the evidence needed to refine them. DETR3D, PETR, and Sparse4D explore this direction through different uses of geometry and time.

“Sparse” here describes a compact set of learned object representations. It is distinct from sparse voxel convolution, which exploits empty locations in a spatial grid.

## DETR supplies the set-prediction idea

[DETR — Carion et al., ECCV 2020](https://arxiv.org/abs/2005.12872) predicts a set of objects using learned queries. During training, a one-to-one assignment matches predictions to annotated objects. Unmatched predictions learn a no-object outcome.

The key change is the training contract: the model learns to allocate predictions to distinct objects rather than generating many redundant boxes and relying on a separate suppression procedure to remove duplicates.

This does not make a query a permanent identity. Set prediction explains how objects are assigned within an example. Tracking the same vehicle over time requires an additional temporal mechanism.

## DETR3D: use 3D hypotheses to look into cameras

[DETR3D — Wang et al., CoRL 2021](https://arxiv.org/abs/2110.06922) connects object queries to 3D reference points. Camera calibration projects those points into different images, where the method samples features to update the queries and predict 3D boxes.

This is a 3D-to-2D retrieval direction: start with a spatial hypothesis, then ask which image evidence supports it. The architecture avoids requiring a dense depth map or a dense BEV feature map as the explicit intermediate output.

The advantage is focused computation. The difficulty is that feature retrieval depends on the current spatial hypothesis. If the reference point is inaccurate, the relevant image evidence may be difficult to gather. Iterative refinement is consequently an important part of this family of designs.

## PETR: put 3D position information into image features

[PETR — Liu et al., ECCV 2022](https://arxiv.org/abs/2203.05625) takes a different route. It constructs 3D coordinate information associated with image frustums and encodes that information into image features. Object queries then interact with these position-aware features to predict 3D objects.

An image frustum is the volume extending from a camera through its image plane. Associating coordinates with locations along that volume provides a way to tell the network where image evidence could lie in 3D.

The comparison is useful: DETR3D explicitly projects reference points to sample features; PETR transforms positional information so attention can operate over features carrying 3D context. Both use queries, but “uses a transformer” does not explain the difference between them.

<figure>
  <a href="{{ '/images/driving-papers/04.svg' | relative_url }}" style="width:100%;" aria-label="Open architecture diagram at full size"><img src="{{ '/images/driving-papers/04.svg' | relative_url }}" alt="Object queries: DETR3D, PETR, and Sparse4D: a comparison of the information passed between the methods' main stages." width="760" height="460" style="height:auto;" loading="lazy"></a>
  <figcaption>Original schematic of the methods discussed here; simplified information flow, not a reproduction of a paper's complete architecture.</figcaption>
</figure>

## Sparse4D: carry object hypotheses through time

[Sparse4D — Lin et al., 2022 preprint](https://arxiv.org/abs/2211.10581) associates sparse 3D anchors with instance features and aggregates evidence across views, feature scales, and timestamps. Keypoints associated with a hypothesis provide locations from which to collect supporting features.

[Sparse4D v3 — Lin et al., CVPR 2024](https://arxiv.org/abs/2311.11722) adds temporal instance denoising and quality-estimation tasks during training, and decoupled attention in the architecture. It also extends detection to tracking by assigning instance identities during inference. The useful architectural idea is to maintain instance-oriented state and repeatedly update it using fresh observations.

This offers a different temporal interface from retaining an entire BEV grid. An object representation can preserve motion and appearance evidence efficiently, but the system still needs to discover new objects and retire hypotheses that no longer have support.

## Dense and sparse representations serve different outputs

A dense map is convenient for road occupancy and spatial queries: features exist wherever the downstream task asks for them. A sparse object set is convenient for instance interaction: the representation explicitly separates the participants that a predictor may need to reason about.

Neither representation automatically solves the other's task. A list of detected cars does not describe all free space. A grid of occupied cells does not automatically say which cells belong to one moving actor.

The engineering question is therefore not simply whether sparse computation is faster. It is whether the retained representation supports the required output, and what additional computation is needed to recover information that it omits. That same question will reappear when planning methods choose between dense occupancy and vectors describing agents and lanes.

{% include perception-series-nav.html %}
