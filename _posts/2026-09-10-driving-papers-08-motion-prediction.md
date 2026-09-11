---
title: '08: Motion prediction: VectorNet, LaneGCN, and MTR'
date: '2026-09-10'
permalink: /autonomous-driving-perception/08-motion-prediction/
excerpt: Motion prediction estimates what other road users may do. Planning chooses what our own vehicle should do. The tasks
  interact, but a network that predicts a pedestrian's future is not yet a planner.
tags:
- autonomous driving
series: perception
series_number: 8
read_time: false
reading_minutes: 5
---

{% include perception-series-nav.html %}

Motion prediction estimates what other road users may do. Planning chooses what our own vehicle should do. The tasks interact, but a network that predicts a pedestrian's future is not yet a planner.

VectorNet, LaneGCN, and Motion Transformer show how forecasting evolved from generic scene encoding toward structured road relationships and multiple possible futures. Their inputs are typically agent histories and map information, so the sensor-perception problem has already been partly solved before these models begin.

## VectorNet: keep the geometry as vectors

[VectorNet — Gao et al., CVPR 2020](https://arxiv.org/abs/2005.04259) encodes road elements and agent trajectories as vectors. A local network aggregates features within each polyline, and a global interaction network models relationships among the resulting scene elements.

A *polyline* is simply a sequence of connected line segments. It can describe a lane boundary or an actor's observed path. Keeping that structure avoids first drawing the information into an image and asking a convolutional network to recover the relationships from pixels.

The methodological change is to preserve the form of the available data. An HD map already contains geometric elements, so rasterization is a design choice rather than an unavoidable preprocessing step. VectorNet is a forecasting encoder; it does not itself infer the HD map from camera images.

## LaneGCN: road connectivity is a strong prior

[LaneGCN — Liang et al., ECCV 2020](https://arxiv.org/abs/2007.13732) builds a lane graph that explicitly retains road structure. Its graph processing distinguishes lane relationships and supports information propagation along lanes. A fusion network models actor-to-lane, lane-to-lane, lane-to-actor, and actor-to-actor interactions.

This supplies a useful inductive bias: the model is designed to process the relationships that constrain traffic. A nearby lane on the opposite side of a divider is not equivalent to the next lane segment on the actor's route.

The limitation follows from the same choice. An incorrect or outdated lane graph can strongly influence the forecast. Structured inputs reduce the work the network must learn from scratch, but they also make input quality part of the model's operating assumptions.

<figure>
  <a href="{{ '/images/driving-papers/08.svg' | relative_url }}" style="width:100%;" aria-label="Open architecture diagram at full size"><img src="{{ '/images/driving-papers/08.svg' | relative_url }}" alt="Motion prediction: VectorNet, LaneGCN, and MTR: a comparison of the information passed between the methods' main stages." width="760" height="460" style="height:auto;" loading="lazy"></a>
  <figcaption>Original schematic of the methods discussed here; simplified information flow, not a reproduction of a paper's complete architecture.</figcaption>
</figure>

## MTR: separate broad intentions from local refinement

[Motion Transformer, or MTR — Shi et al., NeurIPS 2022](https://arxiv.org/abs/2209.13508) combines global intention localization with local movement refinement. Motion query pairs specialize in different possible motion modes, and the decoder refines their trajectories using relevant scene information.

This addresses a recurring problem: one observed history can lead to several valid futures. A vehicle may continue, turn, or slow down. Assigning different queries to different modes helps the model organize that uncertainty instead of forcing every possibility through one undifferentiated feature.

A *mode* is a distinct plausible outcome, not a time step. Each predicted mode contains a trajectory across the forecast horizon, together with a score indicating how the model ranks that alternative.

## Why averaging futures gives the wrong answer

Consider equally plausible left and right turns. A model trained to output one trajectory with squared error can prefer their average, which may point straight into an invalid area. A collection of trajectories preserves the alternatives, but introduces new questions: how many candidates, how to keep them distinct, and how to assign probabilities or confidence?

This also explains a limitation of minimum-displacement metrics. A metric that picks the closest predicted trajectory after seeing the future measures whether the candidate set covers the realized outcome. It does not establish that the model assigned sensible confidence to that candidate. Comparisons must match candidate count and horizon.

| Method | Structural choice | Main question it helps answer |
|---|---|---|
| VectorNet | Local polylines, then global interaction | How should maps and histories be encoded? |
| LaneGCN | Explicit lane graph and actor–map interaction | Which road relationships constrain motion? |
| MTR | Intention queries and trajectory refinement | How can several futures be organized? |

## The remaining gap to planning

A predictor can describe what another driver is likely to do under the observed scene. A planner must consider what may happen after our car accelerates, yields, or changes lanes. Those actions can change the other driver's response.

An unconditional forecast is not automatically an action-conditioned model of that interaction. Nor should the planner select the most likely future and ignore the rest. Prediction makes uncertainty explicit; planning must decide how to act given that uncertainty, route objectives, vehicle limits, and the cost of a mistake.

{% include perception-series-nav.html %}
