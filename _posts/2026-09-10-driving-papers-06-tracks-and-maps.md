---
title: '06: Scene structure: tracking, MapTR, and road topology'
date: '2026-09-10'
permalink: /autonomous-driving-perception/06-tracks-and-maps/
excerpt: 'A detector produces a snapshot. Driving also needs persistent actors and road structure: which vehicle was seen
  before, how it is moving, where the lanes are, and which road elements connect. Tracking and mapping address these questions
  with different forms of structured output.'
tags:
- autonomous driving
series: perception
series_number: 6
read_time: false
reading_minutes: 5
redirect_from:
- /autonomous-driving-perception/16-tracking/
- /autonomous-driving-perception/17-maps/
---

{% include perception-series-nav.html %}

A detector produces a snapshot. Driving also needs persistent actors and road structure: which vehicle was seen before, how it is moving, where the lanes are, and which road elements connect. Tracking and mapping address these questions with different forms of structured output.

Their common methodological theme is that **a useful scene representation needs relationships**, not just independently accurate coordinates.

## SORT and AB3DMOT: establish a strong association baseline

[SORT — Bewley et al., ICIP 2016](https://arxiv.org/abs/1602.00763) combines detector outputs with a Kalman filter and assignment between predicted tracks and new detections. A motion model predicts where an object should appear; a matching procedure decides which new observation belongs to which track.

[AB3DMOT — Weng et al., IROS 2020](https://arxiv.org/abs/1907.03961) shows the effectiveness of a similarly simple approach for 3D multi-object tracking. Both papers are useful reminders that a learned detector does not require every downstream operation to be a neural network.

Association creates a specific failure mode. Two nearby vehicles may be localized correctly yet assigned each other's identities. A predictor then receives a discontinuous history, even though a frame-level detection metric remains good. Missed detections introduce another decision: keep a track alive temporarily or terminate it and risk rediscovering the same actor later.

## From tracked boxes to learned track features

A classical interface passes estimated position, velocity, and uncertainty. An instance-query approach can additionally retain learned features that help explain the observations. The tracking component in [UniAD — Hu et al., CVPR 2023](https://arxiv.org/abs/2212.10156) uses track queries as part of a system whose later tasks consume those representations.

The important difference is the information crossing the interface. A learned feature can preserve useful evidence beyond a final box, while an explicit state estimate is easier to inspect and connect to a conventional motion model. These choices can coexist.

## MapTR: predict road elements as vectors

[MapTR — Liao et al., ICLR 2023](https://arxiv.org/abs/2208.14437) constructs a local vector map from observations. A map element is represented by points describing its geometry, rather than only by a raster image whose pixels must later be converted into lines.

It uses structured queries and matching to learn these elements. A key detail is that equivalent point orderings can describe the same geometry. A line read from one end or the other should not become a completely different learning target merely because its sequence is reversed. MapTR accounts for such equivalences in its representation and learning.

This illustrates why the output format matters to optimization. A loss should penalize a genuinely wrong road shape, not an arbitrary labeling convention.

<figure>
  <a href="{{ '/images/driving-papers/06.svg' | relative_url }}" style="width:100%;" aria-label="Open architecture diagram at full size"><img src="{{ '/images/driving-papers/06.svg' | relative_url }}" alt="Scene structure: tracking, MapTR, and road topology: a comparison of the information passed between the methods' main stages." width="760" height="460" style="height:auto;" loading="lazy"></a>
  <figcaption>Original schematic of the methods discussed here; simplified information flow, not a reproduction of a paper's complete architecture.</figcaption>
</figure>

## A geometric map is not automatically a road graph

Two lane curves may lie very close together while belonging to different routes. At a junction, a planner needs connections and traffic relationships, not only accurate polylines.

[OpenLane-V2 — Wang et al., NeurIPS 2023](https://arxiv.org/abs/2304.10440) emphasizes lane topology and relationships involving traffic elements. It makes the distinction between detecting road geometry and understanding road structure explicit.

A vector representation is therefore useful but not sufficient by itself. Point sequences describe shape; graph edges or other explicit relations describe connectivity. A lane's visual boundary also does not, by itself, tell the car whether a traffic light permits proceeding.

| Output | What it preserves | What still needs attention |
|---|---|---|
| Tracked boxes | Actor identity and estimated state | Association errors and uncertainty |
| Learned track queries | Actor-specific feature history | Meaning and stability of retained features |
| Map polylines | Compact road geometry | Connectivity and traffic relationships |

## The handoff to prediction

A motion predictor often assumes clean agent histories and a correct map. Those assumptions make the prediction problem easier to study, but they hide upstream errors. When deployed perception supplies the inputs, track switches, missing actors, and lane mistakes become forecasting errors too.

That is why a strong result using annotated trajectories should not be read as a result for the complete sensor-to-prediction system. The interface defines the experiment. Tracking and mapping make the scene easier to reason about, but they also determine which uncertainties reach the next stage and which disappear during conversion.

{% include perception-series-nav.html %}
