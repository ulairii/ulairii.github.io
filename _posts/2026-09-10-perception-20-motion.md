---
title: 'How Self-Driving Cars See — 20: Representing a world that moves'
date: '2026-09-10'
permalink: /autonomous-driving-perception/20-motion/
excerpt: The cyclist moves through the intersection while the truck remains parked. A current occupancy grid describes where matter is estimated to be now. To choose a motion, the car also needs to reason about where road users may be when it reaches the crossing.
tags:
  - autonomous driving
series_number: 20
read_time: false
series: perception
---

{% include perception-series-nav.html %}

The cyclist moves through the intersection while the truck remains parked. A current occupancy grid describes where matter is estimated to be now. To choose a motion, the car also needs to reason about where road users may be when it reaches the crossing.

Adding time creates several different tasks that are often grouped under the word “4D.” We will separate observing change, reconstructing a sequence, and forecasting future states. The distinction determines what evidence is available and what uncertainty the output must represent.

## Time can be an input without being a future target

A model can use several past frames to estimate the current scene. This is temporal perception. Its target is still the present, even though its input includes history. A denser or more stable current reconstruction does not automatically predict the future.

A model can also reconstruct a sequence of past states, perhaps using all observations offline. That may be useful for annotation or mapping, but it has a different information setting from an online system that cannot access future frames.

**Forecasting** predicts states at future timestamps from currently available information. The targets have not yet been observed at inference time. Uncertainty comes not only from measurement errors, but also from the fact that several future behaviors may be possible.

Thus “4D perception” is an umbrella phrase, not a precise task definition. Ask which timestamps are inputs, which timestamps are outputs, whether future observations are used, and whether the representation tracks individual objects or spatial cells.

## Scene flow estimates motion of spatial points

**Optical flow** describes apparent motion in the image plane. **Scene flow** describes three-dimensional motion associated with scene points or surfaces. Both require conventions about time and coordinate frames.

A stationary pole can have large image motion because the camera moves. In world coordinates, its physical motion remains zero. A scene-flow representation must specify whether self-motion has been removed or whether the vectors describe change in a moving sensor frame.

For the cyclist, different body and bicycle parts can move differently. A single object velocity is a compact approximation, while a dense flow field can represent more local variation. That richer output is also harder to supervise and estimate under sparse observations.

Occlusion creates missing correspondence. A point visible now may not be visible in the next frame. A model may infer its motion, but cannot obtain a direct correspondence from absent evidence. Evaluation should distinguish visible and occluded cases where possible.



<figure>
  <a href="{{ '/images/perception-series/20.svg' | relative_url }}" aria-label="Open diagram at full size" style="width:100%;"><img src="{{ '/images/perception-series/20.svg' | relative_url }}" alt="Current occupancy is shown beside two possible future occupancy maps, one with a cyclist continuing straight and one with the cyclist turning. Motion arrows connect cells over time." width="720" height="480" style="height:auto;" loading="lazy"></a>
  <figcaption>A current estimate, a motion field, and a future forecast answer different questions. The two futures are alternatives, not simultaneous measured outcomes. Original diagram for this series.</figcaption>
</figure>

## Occupancy flow connects spatial extent and movement

An occupancy forecast can assign a probability that each grid cell will contain a road user at a future time. This represents possible occupied regions, but a sequence of such grids can lose information about which parts correspond over time.

[Occupancy Flow Fields, by Mahjourian and colleagues, IEEE Robotics and Automation Letters 2022](https://arxiv.org/abs/2203.03875), combines occupancy probabilities with two-dimensional flow vectors for motion forecasting. The work connects spatial occupancy and movement, including consistency between those outputs.

Its representation is a spatiotemporal grid for agents; it should not be confused with a full three-dimensional semantic reconstruction of all surfaces. Different papers use occupancy for different spatial dimensions and different target entities.

Flow conventions also differ. A vector may point forward to a later location or backward to a source location. The direction matters when warping one grid into another. Always check the definition before interpreting arrows in a figure or implementing a loss.

## Camera features can support future instance prediction

[FIERY, by Hu and colleagues, ICCV 2021](https://arxiv.org/abs/2104.10490), predicts future instance segmentation and motion in BEV from surround camera observations. It connects perception and forecasting through a shared representation and models multiple possible futures.

The input images provide evidence about the current scene and recent motion. The future output additionally relies on learned regularities of road behavior. A cyclist's current heading helps, but a turn can remain plausible depending on the road and interaction context.

This illustrates why uncertainty in the future is not simply uncertainty in depth. Even with a perfectly known current position, the cyclist may choose different actions. Improving the current detector cannot eliminate all forecasting uncertainty.

Conversely, a poor current estimate can contaminate the future prediction. A model may forecast a smooth trajectory from a wrong starting point. Evaluating both present-state quality and future behavior helps identify where the error originates.

## Averaging plausible futures can produce an implausible one

Suppose the cyclist may continue straight or turn right. A model trained to return one path by minimizing squared position error can favor an average between the alternatives. That average may cut across an area the cyclist would not actually traverse.

Multiple trajectories, probability distributions, or sampled future states can retain distinct possibilities. The prediction then needs both useful coverage and meaningful confidence. Returning many arbitrary guesses is not a sufficient solution.

For a grid forecast, probabilities at separate cells do not automatically specify a coherent joint future. Two high-probability cells may correspond to alternative positions of one cyclist, not two cyclists appearing simultaneously. The representation's dependence structure affects how a planner should interpret it.

This is an important limitation of visually intuitive heatmaps. They summarize uncertainty spatially, but the full relationship among objects, cells, and times may be richer than the displayed colors indicate.

## The car's action can change what others do

A forecast based only on observed history may estimate likely behavior under the kinds of interactions seen in the data. But the cyclist's response could depend on whether our car slows, proceeds, or changes position.

A model conditioned on a candidate action can attempt to represent those alternatives. That is a stronger requirement than forecasting one likely continuation from history alone. The training data must contain enough evidence to learn how different actions relate to subsequent events.

Recorded data show the action that actually occurred, not every action that could have occurred. Counterfactual behavior is therefore difficult to validate from logs alone. Simulation and other forms of evaluation can help, but introduce their own assumptions.

We will return to action-conditioned world models in Chapter 23. For now, the distinction is enough: forecasting a continuation and predicting responses to alternative actions are related but different tasks.

## Temporal targets need careful construction

If several scans are combined to label a moving object, its points must be related to the appropriate object pose at each time. Otherwise the target can encode a trail rather than a coherent body. Rotation and articulated motion make this more complicated than a single translation.

A future occupancy label also needs a defined coordinate frame. Is it expressed in the current car frame, a future car frame, or a world frame? Each choice is possible, but the transformation must be consistent with the target and the planner's use.

Visibility changes across time. A future target may include an agent currently hidden behind the truck. Predicting such an appearance is a different challenge from advancing a clearly visible object. The benchmark should identify what information the model could have used.

These details influence the meaning of success. A model evaluated only on already visible agents does not establish equal performance on newly appearing ones, even if both results are summarized as future occupancy prediction.

## Evaluate horizons, calibration, and motion consistency

Errors generally depend on the forecast horizon. A short-term estimate based on recent velocity is a different problem from predicting several seconds of interaction. Reporting results by horizon makes that distinction visible.

For probabilistic outputs, confidence should be checked against observed frequencies under an appropriate protocol. A visually concentrated heatmap can be confidently wrong. A broad forecast can cover the truth while providing little useful discrimination.

Motion consistency matters too. Occupancy should not jump between locations in ways incompatible with the predicted flow. Object identities, when represented, should remain coherent. Metrics and visual inspections should test these relationships rather than only one timestamp at a time.

No forecast removes the need to update when new evidence arrives. The car should re-estimate the scene as it moves. A useful future model supports that repeated decision process instead of pretending the next several seconds are already known.

## Check your understanding

Does a model using ten past frames necessarily forecast the future? No. It may only improve the current estimate. The target timestamp defines the distinction.

Why can the mean of two valid paths be invalid? The alternatives may follow separate road branches, while their average passes through neither. A representation of multiple futures can retain that difference.

Next we will examine how these perception and prediction outputs are connected to planning, and why a better isolated metric does not always produce better driving.

{% include perception-series-nav.html %}
