---
title: '09: Trajectory planning: search, learned costs, and ChauffeurNet'
date: '2026-09-10'
permalink: /autonomous-driving-perception/09-trajectory-planning/
excerpt: A driving planner chooses a feasible motion through a changing environment. A path describes geometry; a trajectory
  also specifies when the vehicle reaches each position. Passing behind a pedestrian and passing in front can follow similar
  geometry but require different timing.
tags:
- autonomous driving
series: perception
series_number: 9
read_time: false
reading_minutes: 5
---

{% include perception-series-nav.html %}

A driving planner chooses a feasible motion through a changing environment. A **path** describes geometry; a **trajectory** also specifies when the vehicle reaches each position. Passing behind a pedestrian and passing in front can follow similar geometry but require different timing.

A route planner selects roads over a long distance. A local motion planner selects the next maneuver and trajectory. A controller turns that trajectory into steering, acceleration, and braking while responding to tracking error. This chapter concerns local motion planning, where learned methods increasingly interact with geometric search and optimization.

## The classical baseline: generate, constrain, score

The [survey by Paden et al., IEEE Transactions on Intelligent Vehicles 2016](https://arxiv.org/abs/1604.07446) describes planning and control approaches with different motion models, environmental assumptions, and computational demands. Search, sampling, and trajectory optimization remain useful reference points for learned planners.

A generic formulation is `τ* = argmin J(τ)` over feasible trajectories `τ`. The objective `J` may combine progress, comfort, route adherence, and obstacle-related cost. Constraints limit steering, acceleration, curvature, and collision exposure. Some systems first generate a finite candidate set; others optimize a continuous trajectory.

A Frenet coordinate frame, for example, describes progress along a reference road curve and lateral displacement from it. This can simplify lane-following trajectory generation, but the reference curve and its suitability become part of the design.

The benefit is explicit structure. The difficulty is specifying costs and predictions that produce reasonable behavior across diverse traffic interactions.

<figure>
  <a href="{{ '/images/driving-papers/09.svg' | relative_url }}" style="width:100%;" aria-label="Open architecture diagram at full size"><img src="{{ '/images/driving-papers/09.svg' | relative_url }}" alt="Trajectory planning: search, learned costs, and ChauffeurNet: a comparison of the information passed between the methods' main stages." width="760" height="460" style="height:auto;" loading="lazy"></a>
  <figcaption>Original schematic of the methods discussed here; simplified information flow, not a reproduction of a paper's complete architecture.</figcaption>
</figure>

## Neural Motion Planner: learn the cost, retain candidate selection

[End-to-end Interpretable Neural Motion Planner — Zeng et al., CVPR 2019](https://arxiv.org/abs/2101.06679) takes lidar and an HD map, predicts intermediate detections and future trajectories, and constructs a learned spatial cost volume over the planning horizon. Physically possible candidate trajectories are sampled and scored using that volume.

The learning problem is therefore richer than directly regressing the next steering command. The model learns which future positions are desirable, while the candidate generator provides motion structure. The selected trajectory minimizes the learned cost among the candidates considered.

A cost field can express several favorable corridors rather than forcing all behavior into one average path. But selection remains limited by candidate coverage: a useful maneuver cannot be chosen if it is absent from the candidate set. The cited paper appeared at CVPR in 2019; its arXiv upload is later.

## ChauffeurNet: imitation needs recovery examples

[ChauffeurNet — Bansal, Krizhevsky, and Ogale, 2018 preprint](https://arxiv.org/abs/1812.03079) learns driving behavior from a structured representation of the scene. It uses synthesized perturbations to expert driving and additional losses for undesirable outcomes and progress.

The key insight is about the training distribution. Expert logs mostly contain states reached by an expert. A learned policy's small errors can move the vehicle into states that those logs rarely show. Training only to imitate nominal behavior may provide little guidance about recovery.

Perturbed examples expose the learner to departures from the expert path. This work also makes clear that learning to drive does not imply learning directly from raw pixels: perception preprocessing and a downstream controller can remain outside the learned policy.

## What changes when part of the planner is learned

These approaches modify different parts of the decision process. A learned cost changes how candidates are ranked. An imitation policy changes how a trajectory is generated. A motion model or controller may still be conventional in both cases.

This decomposition is more useful than a binary division between “classical” and “AI” planning. It reveals where labels are needed, where constraints are applied, and what can be inspected after a failure.

A loss penalty is also different from a hard constraint. Penalizing a collision during training encourages avoidance in the examples seen; it does not guarantee that every future output satisfies a geometric condition. Explicit validation of a proposed trajectory can still serve a separate purpose.

The next architectural step is to let the planning objective influence the features used to perceive and predict the scene. That changes the training boundary of the system, while leaving many of these planning choices relevant.

{% include perception-series-nav.html %}
