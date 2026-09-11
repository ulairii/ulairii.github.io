---
title: 'How Self-Driving Cars See — 16: Remembering what happened a moment ago'
date: '2026-09-10'
permalink: /autonomous-driving-perception/16-tracking/
excerpt: The cyclist briefly disappears behind the truck. A detector processing only the latest image may return no cyclist at all. A useful temporal system should remember the recent observation, estimate where the cyclist might be now, and recognize the same person when they reappear.
tags:
- autonomous vehicles
- perception
- deep learning
- perception series
series_number: 16
read_time: false
---

{% include perception-series-nav.html %}

The cyclist briefly disappears behind the truck. A detector processing only the latest image may return no cyclist at all. A useful temporal system should remember the recent observation, estimate where the cyclist might be now, and recognize the same person when they reappear.

Two related ideas enter here: tracking objects and combining features over time. Tracking maintains identities and states. Temporal feature fusion gathers evidence across observations. A system can use either or both, but they do not provide the same output or solve exactly the same problem.

## A track is a maintained hypothesis about an object

A **track** stores an object's estimated state across time. It may include position, size, velocity, class, identity, and uncertainty. When a new detection arrives, the tracker decides whether to use it to update an existing track or start a new one.

Between observations, a motion model predicts how the state evolves. A constant-velocity model, for example, advances position according to the current velocity estimate. This is an approximation useful over some intervals, not a claim that road users always maintain speed and direction.

The prediction becomes less certain as time passes without a measurement. A sensible tracker represents or accounts for that growing uncertainty rather than treating a stale position as an exact current observation.

[SORT, by Bewley and colleagues, ICIP 2016](https://arxiv.org/abs/1602.00763), provides a simple example using a Kalman filter and assignment between detections and tracks. Its importance here is conceptual: learned detection can be combined with explicit state estimation and association.

## Association decides which observation belongs to which track

Suppose two cyclists pass close together. The new detections must be matched to the old tracks. Spatial proximity helps, but the closest current box is not always the same person, especially when motion is fast or detections are noisy.

An assignment algorithm can evaluate a matrix of costs between tracks and detections, then choose compatible matches. Costs may include box overlap, predicted position, category, and appearance similarity. Gating can exclude implausible matches before assignment.

[Deep SORT, by Wojke, Bewley, and Paulus, ICIP 2017](https://arxiv.org/abs/1703.07402), adds a learned appearance association metric to help maintain identities. That is a specific use of deep learning inside tracking, rather than replacing the entire tracking problem with a classifier.

Appearance is imperfect evidence. Similar clothing can confuse identity, and lighting or viewpoint can change the same person's features. Geometry and appearance therefore need to be interpreted together, with an explicit policy for uncertainty and missing observations.



<figure>
  <a href="{{ '/images/perception-series/16.svg' | relative_url }}" aria-label="Open diagram at full size" style="width:100%;"><img src="{{ '/images/perception-series/16.svg' | relative_url }}" alt="A cyclist is visible, then hidden, then visible again. Solid boxes mark measurements and a dashed box marks the predicted state during occlusion." width="720" height="470" style="height:auto;" loading="lazy"></a>
  <figcaption>A maintained track can persist without a current detection, but its predicted position is not a fresh measurement. Original diagram for this series.</figcaption>
</figure>

## Prediction and correction serve different roles

A Kalman-style estimator alternates between predicting the state and correcting it using a measurement under model assumptions. The correction balances uncertainty in the prior estimate and in the measurement. It does not simply replace all history with the newest number.

For a small illustrative example, a motion model predicts the cyclist near 12 meters ahead, while a noisy new measurement suggests 13 meters. A weighted update may lie between them. The appropriate weight depends on uncertainty, not on a universal rule that the latest observation is always best.

If the cyclist suddenly turns, the motion model can be wrong. If a detector jumps to the truck edge, the measurement can be wrong. Robust behavior depends on recognizing which assumptions are no longer appropriate and allowing the track to recover.

A smooth track is therefore not necessarily an accurate one. Excessive smoothing can make a turning object lag behind its true position. Evaluation needs to examine responsiveness alongside visual stability.

## The vehicle's motion must be separated from object motion

As our car moves, every stationary object changes coordinates in the vehicle frame. If we compare positions across time without compensating for that movement, we can incorrectly infer that the parked truck is moving.

Three-dimensional tracking often brings detections into a shared frame or explicitly includes relative pose transformations. [AB3DMOT, by Weng and colleagues, IROS 2020](https://arxiv.org/abs/2008.08063), is a useful baseline for studying three-dimensional state estimation and data association.

Pose estimates are themselves imperfect. A small heading error can create a larger positional discrepancy for distant objects. Temporal alignment therefore depends on localization quality as well as detection quality.

The reference frame must be recorded with each state. A velocity in world coordinates differs from relative velocity measured in the moving vehicle frame. Mixing them can produce a plausible-looking but physically incorrect extrapolation.

## Feature fusion can help before an object is detected

A tracker usually receives detections or object features. Temporal perception can instead combine image, point, voxel, or BEV features before the final detection head. Weak evidence across several frames may then support an object that no single frame detects confidently.

Historical feature maps need alignment. Stationary road structure can be warped using the car's motion. Moving objects require additional handling, such as learned sampling, motion estimation, or object-specific memory.

BEVFormer's temporal operation, introduced in Chapter 14, is one example of using past representations. Other methods retain object queries or accumulated points. The choice determines whether memory is organized around space, measurements, or individual entities.

Feature memory alone does not guarantee persistent identities. A detector using several frames may output better boxes while assigning no track ID. Conversely, a tracker can maintain identities using single-frame detections without sharing dense features across frames.

## Missing observations require lifecycle decisions

When the cyclist disappears, how long should the track remain? Keeping it briefly can handle occlusion. Keeping it indefinitely can create a phantom object after the cyclist has left the scene or after a false detection.

Track initiation has a similar tradeoff. Starting a new track immediately responds quickly, but may preserve false positives. Requiring repeated detections can improve confidence while delaying recognition of newly appearing objects.

The system needs policies for creation, confirmation, update, and deletion. Learned models can influence those decisions, but the behavior should remain inspectable. A benchmark may reward one tradeoff while a downstream planner needs a different treatment of uncertainty.

During an occlusion, a predicted track should be distinguishable from a currently observed object. The planner can then use the hypothesis with appropriate caution rather than assuming every state has equally recent evidence.

## Temporal evaluation must respect causality

An online system can use past and current observations, not future measurements that have not yet arrived. An offline annotation or smoothing algorithm may use the entire sequence. Those are different information settings.

A model evaluated with future frames can produce better estimates, but that result should not be presented as causal online performance. Similarly, labels generated from future observations may be valid training targets while remaining unavailable as inference inputs.

Metrics should consider both detection and identity quality. A tracker might localize every object but repeatedly swap identities. Another might preserve identities while missing many objects. Aggregate scores need to be interpreted with the underlying errors.

Latency also belongs in temporal evaluation. A stable estimate delivered late can still be stale. The complete age of the state depends on sensor timing, history length, and computation, not just the frequency at which results are returned.

## Walk through one missed detection

At time one, the cyclist is detected and a track is confirmed. At time two, the truck blocks the view, so the motion model advances the state without a matching detection. At time three, the cyclist reappears near the predicted region. The association step checks whether that observation is compatible with the maintained state and appearance.

A successful match restores direct evidence and updates the estimate. A large discrepancy should not be silently accepted just to preserve the identity. It may mean the cyclist turned, the original state was inaccurate, or the new detection belongs to someone else.

This example also explains why a tracker needs a policy for unmatched detections. A second cyclist entering the scene deserves a new track rather than being forced into the old one. Identity continuity is useful only when it corresponds to the physical entity. The exact confirmation and deletion delays are design choices, and should be reported when they materially affect the evaluation.

## Check your understanding

If an object is absent from the current detector output, must its track disappear? No. A tracker can maintain a predicted hypothesis during a short gap, while increasing uncertainty and applying a deletion policy.

Does using several frames automatically provide tracking? No. Temporal features can improve detection without persistent object identities. Tracking adds association and state maintenance.

Our perception system now has memory. Next we will describe another kind of structure it needs to maintain: the lanes, boundaries, and connections that organize an intersection.

{% include perception-series-nav.html %}
