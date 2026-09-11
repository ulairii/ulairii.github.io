---
title: '07: Occupancy and motion: SurroundOcc, Occ3D, and FIERY'
date: '2026-09-10'
permalink: /autonomous-driving-perception/07-occupancy-and-flow/
excerpt: Bounding boxes compress objects into a convenient form. They are less suitable for irregular obstacles, detailed
  free-space geometry, and surfaces that do not fit a known object category. Occupancy methods change the prediction target
  from “which objects exist?” to “what occupies each part of space?” Future occupancy extends that target through time.
tags:
- autonomous driving
series: perception
series_number: 7
read_time: false
reading_minutes: 5
redirect_from:
- /autonomous-driving-perception/19-occupancy/
- /autonomous-driving-perception/20-motion/
---

{% include perception-series-nav.html %}

Bounding boxes compress objects into a convenient form. They are less suitable for irregular obstacles, detailed free-space geometry, and surfaces that do not fit a known object category. Occupancy methods change the prediction target from “which objects exist?” to “what occupies each part of space?” Future occupancy extends that target through time.

There are two separate developments here: reconstructing the present scene in 3D and forecasting where agents will occupy the road. They overlap, but they are not interchangeable tasks.

## SurroundOcc: predict a spatial volume

[SurroundOcc — Wei et al., ICCV 2023](https://arxiv.org/abs/2303.09551) estimates 3D occupancy from multiple camera views. It brings image evidence into a volumetric representation and uses spatial processing to predict occupancy and semantics. The work also develops a way to produce dense supervision from available observations.

An occupancy cell represents a small region of space, so an object can have a more detailed shape than a box. But the representation is discretized: a thin pole may occupy only a few cells, and coarser resolution can erase small structures.

Occupancy also does not automatically mean open-world understanding. A semantic head can still be trained on a fixed vocabulary, and an unfamiliar obstacle remains difficult if the model has weak visual or geometric evidence for it.

## Occ3D: the labels define what the task actually means

[Occ3D — Tian et al., NeurIPS 2023](https://arxiv.org/abs/2304.14365) provides occupancy benchmarks and a pipeline for dense, visibility-aware labels. Its stages include densification, reasoning about occlusion, and image-guided refinement.

This is a substantive contribution because a lidar scan is not a complete occupancy label. A return indicates a sampled surface. Space behind it may be unobserved, and accumulating scans across time requires handling object motion.

The distinction among **occupied, free, and unobserved** is crucial. Treating every cell without a return as empty creates incorrect supervision. Visibility masks and evaluation conventions therefore belong in a comparison of occupancy methods, alongside network design.

<figure>
  <a href="{{ '/images/driving-papers/07.svg' | relative_url }}" style="width:100%;" aria-label="Open architecture diagram at full size"><img src="{{ '/images/driving-papers/07.svg' | relative_url }}" alt="Occupancy and motion: SurroundOcc, Occ3D, and FIERY: a comparison of the information passed between the methods' main stages." width="760" height="460" style="height:auto;" loading="lazy"></a>
  <figcaption>Original schematic of the methods discussed here; simplified information flow, not a reproduction of a paper's complete architecture.</figcaption>
</figure>

## FIERY: forecast a changing BEV scene

[FIERY — Hu et al., ICCV 2021](https://arxiv.org/abs/2104.10490) predicts future instance segmentation and motion in BEV from surround-camera history. Its probabilistic formulation represents uncertainty in future outcomes rather than assuming a single inevitable continuation.

The output is future dynamic-agent structure in BEV; it should not be described as the same task as full 3D semantic occupancy. The paper precedes SurroundOcc and Occ3D because future BEV prediction and present 3D reconstruction are parallel research lines, grouped here by their spatial representation.

A forecast is also different from temporal perception. Combining earlier frames helps estimate what exists now. Predicting future frames requires assumptions about behavior that has not yet happened.

## Occupancy Flow Fields: connect occupancy across time

[Occupancy Flow Fields — Mahjourian et al., RA-L 2022](https://arxiv.org/abs/2203.03875) represents agent occupancy probabilities together with two-dimensional flow vectors in a spatiotemporal grid. A consistency objective connects predicted occupancy and flow.

The motivation is the weakness of an occupancy-only sequence. Two successive probability maps can show where agents might be without explaining which occupied regions move into which later regions. Flow supplies motion correspondence that can help recover that structure.

These probabilities describe cell occupancy, not a universal probability that any planned path is safe. The planner must still account for time, its own footprint, and how different cells and futures are related.

## What occupancy changes for planning

A planner can evaluate whether the car's footprint intersects occupied space at each future time. This is more directly spatial than checking a category label, and can represent obstacles that are awkward to approximate by standard boxes.

However, multiplying independent cell probabilities would generally ignore correlations. A single uncertain vehicle may cover many cells; those cells are not independent obstacles. Likewise, two plausible future maneuvers should not be confused with two vehicles that both exist.

Object trajectories and occupancy thus offer complementary interfaces. Trajectories make actor identity and alternative intentions explicit. Occupancy offers a spatial field that is convenient for collision reasoning. The appropriate choice depends on what uncertainty the planner needs and how the representation preserves it.

{% include perception-series-nav.html %}
