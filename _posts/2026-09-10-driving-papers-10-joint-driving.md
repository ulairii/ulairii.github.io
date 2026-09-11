---
title: '10: Joint perception and planning: TransFuser and UniAD'
date: '2026-09-10'
permalink: /autonomous-driving-perception/10-joint-driving/
excerpt: Optimizing detection, prediction, and planning separately can discard useful information at each interface. A box
  contains less evidence than the feature that produced it, and the perception error most important to a planner may not be
  the one that dominates average detection accuracy.
tags:
- autonomous driving
series: perception
series_number: 10
read_time: false
reading_minutes: 5
redirect_from:
- /autonomous-driving-perception/21-planning/
---

{% include perception-series-nav.html %}

Optimizing detection, prediction, and planning separately can discard useful information at each interface. A box contains less evidence than the feature that produced it, and the perception error most important to a planner may not be the one that dominates average detection accuracy.

End-to-end driving research asks how observations and driving objectives should be connected. It does not prescribe one universal architecture. TransFuser and UniAD illustrate two influential answers: fuse sensor features for a driving policy, or coordinate explicit intermediate tasks around planning.

## TransFuser: fuse for the driving decision

[TransFuser — Prakash, Chitta, and Geiger, CVPR 2021](https://arxiv.org/abs/2104.09224) uses attention to combine camera and lidar representations in an imitation-learning driving system. Information is exchanged across the sensor branches so the policy can use broader scene context.

Its motivation goes beyond matching measurements of the same physical surface. A traffic signal can affect a vehicle at a different location. Driving decisions require semantic relationships as well as geometric correspondence.

The system predicts waypoints, which a controller follows. Its CARLA experiments evaluate behavior in simulation, where the chosen motion changes subsequent observations. That evaluation setting differs from predicting a trajectory against a fixed driving log.

TransFuser therefore connects fusion to the policy objective. It is not simply a BEV detector followed by a box-to-action conversion, and its “end-to-end” label does not mean the vehicle controller has disappeared.

## UniAD: keep the tasks, change their interfaces

[UniAD — Hu et al., CVPR 2023](https://arxiv.org/abs/2212.10156) organizes tracking, mapping, motion forecasting, occupancy prediction, and planning in a shared framework. Camera features are converted into BEV features, while queries provide interfaces between the task modules.

Track queries represent agents; map queries represent road elements. Motion prediction uses the structured scene, and occupancy-related information contributes to planning. Rather than communicating only through final boxes or maps, modules can exchange learned features.

The distinctive claim is **task coordination toward planning**, not merely adding several independent output heads to one backbone. Its training schedule also uses stages, illustrating that an end-to-end framework need not be trained from scratch with every objective active at once.

The original paper's planning results use nuScenes-based evaluation. They should be interpreted within that protocol, rather than treated as directly comparable to a CARLA driving score.

<figure>
  <a href="{{ '/images/driving-papers/10.svg' | relative_url }}" style="width:100%;" aria-label="Open architecture diagram at full size"><img src="{{ '/images/driving-papers/10.svg' | relative_url }}" alt="Joint perception and planning: TransFuser and UniAD: a comparison of the information passed between the methods' main stages." width="760" height="460" style="height:auto;" loading="lazy"></a>
  <figcaption>Original schematic of the methods discussed here; simplified information flow, not a reproduction of a paper's complete architecture.</figcaption>
</figure>

## What joint training can improve

Consider a partially occluded cyclist. A detector might produce an uncertain box while retaining evidence of motion in its features. If prediction receives only the box, that evidence may be lost. A feature-level interface offers a route for retaining it.

This is an architectural motivation, not a guarantee that the model learns the desired behavior. Different tasks can compete for capacity, and their losses may have very different scales. A large mapping loss can dominate optimization without producing a corresponding improvement in the selected trajectory.

Intermediate supervision can make training easier and provide useful diagnostic outputs. However, the presence of an interpretable output does not prove that the policy depends on it. Ablations and interventions are needed to establish which inputs and modules affect the decision.

## Why the training boundary matters

| Question | What it reveals |
|---|---|
| Are inputs raw sensors or annotated agent states? | How much perception the system actually solves |
| Is the output steering, waypoints, or a timed trajectory? | What remains for downstream execution |
| Which intermediate tasks receive labels? | The supervision and annotation burden |
| Is evaluation based on log replay or interactive rollout? | Whether errors can change later observations |

These are different dimensions of a system. A sensor-to-trajectory model can retain explicit geometry, use multiple losses, and rely on a conventional controller. A modular system can share learned features. The important issue is where information and training signals flow.

My reading of these papers is that tighter integration expands the design space rather than settling it. Once planning becomes the organizing objective, it is natural to ask whether every dense intermediate representation is worth computing. That question leads to vectorized planning and, separately, to models that generate several candidate trajectories directly.

{% include perception-series-nav.html %}
