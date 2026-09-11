---
title: 'How Self-Driving Cars See — 24: How do we know the system works?'
date: '2026-09-10'
permalink: /autonomous-driving-perception/24-evaluation/
excerpt: Return to the intersection from Chapter 1. The truck is parked near the crossing, the cyclist is moving along the road, and a pedestrian may be hidden from view. We now have many ways to describe the scene. How do we decide whether any of them actually work well?
tags:
  - autonomous driving
series_number: 24
read_time: false
series: perception
---

{% include perception-series-nav.html %}

Return to the intersection from Chapter 1. The truck is parked near the crossing, the cyclist is moving along the road, and a pedestrian may be hidden from view. We now have many ways to describe the scene. How do we decide whether any of them actually work well?

The answer begins with the claim being tested. Recognizing categories, estimating geometry, maintaining identity, forecasting motion, and driving through the intersection are related achievements with different evidence requirements. A strong evaluation connects each claim to the appropriate measurements and failure cases.

## Define the output before choosing the score

For image detection, the output is a set of labeled boxes. Evaluation needs rules for matching predictions to annotations and counting missed, duplicate, and incorrect detections. Average precision summarizes a precision–recall relationship under a particular protocol.

For three-dimensional detection, geometry is measured in a physical frame. Position, dimensions, heading, and sometimes velocity matter. The [nuScenes detection protocol](https://www.nuscenes.org/object-detection) is a primary example that reports several error components rather than treating every detection property as one indistinguishable success.

For segmentation or occupancy, the output is a spatial labeling. Intersection over union is useful, but the evaluated classes, visibility mask, range, and resolution determine what the score means. Occupancy on observed cells differs from completion of unobserved space.

For tracking, localization alone is insufficient. Identity continuity and lifecycle errors also matter. For maps, accurate curves and correct connections are distinct. The first task of an evaluator is to preserve these distinctions instead of searching for one universal number.

## Ask where the errors occur

An average can hide the conditions that matter most. Separate results by distance, object size, lighting, occlusion, road type, and motion where the data support those comparisons. A model may perform well overall while repeatedly missing distant cyclists.

Do not create so many small slices that each contains too little evidence. Report the number of examples and uncertainty in the measurements when appropriate. A dramatic percentage change on a tiny subset can be unstable.

For our scene, useful slices include partially occluded pedestrians, cyclists beside large vehicles, and objects near camera boundaries. These are concrete situations in which representation and alignment choices can affect behavior.

The slices should follow the intended deployment conditions, not only the places where a new method happens to look best. If a claim concerns a particular kind of robustness, the test should directly include that kind of variation.



<figure>
  <a href="{{ '/images/perception-series/24.svg' | relative_url }}" aria-label="Open diagram at full size" style="width:100%;"><img src="{{ '/images/perception-series/24.svg' | relative_url }}" alt="An evaluation sequence checks labels and splits, component outputs, timing and perturbations, then closed-loop behavior. Each level supports a different claim." width="720" height="530" style="height:auto;" loading="lazy"></a>
  <figcaption>Evidence should match the claim. Component accuracy, robustness tests, and closed-loop behavior answer complementary questions. Original diagram for this series.</figcaption>
</figure>

## Compare methods under the same information budget

A model using six cameras and history should not be compared as if it had the same inputs as a single-image model. A camera-only inference method may still use lidar supervision during training. External pretraining and automatic labels also change the available information.

Record the sensors, frames, resolution, spatial range, training data, model initialization, and inference requirements. Then make clear which differences are part of the proposed method and which are additional resources.

The same principle applies to baselines. A weakly tuned baseline can exaggerate an improvement. A useful comparison gives established methods reasonable settings and examines whether a simpler change accounts for the gain.

An ablation removes or changes one component to test its contribution under a defined setup. It helps answer whether temporal memory, depth supervision, or fusion actually matters. It does not automatically establish that the same contribution holds in every dataset or deployment.

## Prevent the test from leaking into training

Adjacent frames can be nearly identical. Splitting them randomly between training and testing can make the task easier than generalizing to a new drive. Scene-level or other appropriate separation helps preserve independence.

Maps, pseudo-labels, pretraining data, and cached features can also carry information across splits. A model need not receive a test image in a gradient update for leakage to occur. An offline preprocessing step may already have used it.

Future observations require special care in temporal tasks. They can be valid sources for label construction, but must not enter a causal model's inputs unless the experiment explicitly studies an offline setting.

The [nuScenes paper by Caesar and colleagues](https://arxiv.org/abs/1903.11027) and the [Waymo Open Dataset paper by Sun and colleagues](https://arxiv.org/abs/1912.04838) are useful starting points for understanding benchmark data and task definitions. The current official evaluation rules should be checked when reproducing a result.

## Timing is part of the prediction's meaning

Report latency with a clear boundary: what starts the clock, what ends it, and which preprocessing and transfers are included? State the hardware, precision, batch size, and input settings. A network-only measurement is useful if labeled as such.

Look at the distribution, not only the mean. Crowded scenes, variable numbers of points, and post-processing can change runtime. A system with occasional large delays may behave differently from one with a similar average and consistent timing.

Throughput and latency are different. Processing many frames per second in batches does not guarantee that the most recent sensor frame reaches the planner quickly. The age of the final scene estimate is often the more direct operational quantity.

Memory limits can change behavior too. If point caps, query caps, or spatial boundaries remove data, those settings belong in the method description. Resource constraints are not separate from perception when they determine which evidence is processed.

## Test degradation without changing the question silently

A robustness test can introduce blur, missing cameras, timing errors, calibration shifts, or fewer lidar returns. The perturbation should represent a clearly described condition. Its severity and physical interpretation matter.

Artificial corruptions are useful controlled probes, but may differ from real sensor failures. Darkening an image is not a full model of night. Dropping random points is not necessarily the same as rain, fog, or a particular lidar malfunction.

Compare clean and perturbed performance, and inspect whether the model recognizes reduced reliability. A confidence score that remains high during severe degradation can be important even if the average prediction error increases only moderately.

Recovery matters as well. After a camera becomes clear again, does temporal memory correct itself, or preserve the earlier mistake? Sequential tests can reveal behavior that independent corrupted images miss.

## Evaluate the downstream use of the representation

A perception improvement may not affect the planner if it concerns objects far from the route. A small error near the car's path may matter more. To support a driving claim, connect the representation to the actual decision process.

Open-loop trajectory agreement compares predictions with recorded behavior. Closed-loop testing lets actions change later states and observations. Both provide useful evidence, but they answer different questions, as Chapter 21 explained.

[CARLA, introduced by Dosovitskiy and colleagues at CoRL 2017](https://arxiv.org/abs/1711.03938), provides an open simulator for studying driving systems. Simulation enables repeatable interactive tests, while its rendering, dynamics, and road-user models limit what those tests establish about the physical world.

A closed-loop report should include the conditions tested and more than one outcome. Completion, rule-related events, collisions under a defined protocol, and comfort or efficiency can reveal different tradeoffs. A car that never moves is not a successful solution to reaching a destination.

## Use the intersection as an explanation test

Ask what the system knows about each element. For the truck, does it estimate the visible surface, full box, or detailed occupied volume? For the cyclist, does it preserve identity and distinguish current velocity from possible future turns?

For the pedestrian, does the output distinguish hidden space from observed empty space? For the road, does it describe only paint pixels, metric curves, or lane connectivity? For the signal, does it identify the relevant movement rather than only the color?

Then ask what happens after an error. If the cyclist is missed once, does memory help? If memory is wrong, can new evidence correct it? If the chosen action changes the viewpoint, can the system continue from the resulting state?

These questions connect technical mechanisms to observable behavior. They also expose where a claim extends beyond the evidence. A beautiful output rendering may answer only a small subset of them.

## Keep a method card for future papers

For each new paper, record six things: the measurements it receives, the representation it builds, the supervision it uses, how it handles space and time, the outputs it provides, and the evaluation that supports its claims.

Add the principal information loss. A box discards detailed shape. A pillar compresses height. A sparse object set may not describe arbitrary empty space. A latent state can hide what has been retained. Understanding that loss often explains the next research question.

Also record dates carefully. A preprint release and a conference publication can occur in different years. The sequence in this series follows learning dependencies and broad historical developments, not a claim that one method instantly replaced all earlier approaches.

## The question that connects the whole series

We began with recognizing objects in images, then added precise locations, three-dimensional geometry, shared sensor features, time, road structure, occupancy, and connections to action. Each change made some information easier to represent and use, while introducing new costs and assumptions.

The enduring question is: **what does the next decision need to know, and what evidence supports that knowledge?** Use it when reading a paper, inspecting a demo, or building a system. It turns a collection of model names into a coherent understanding of why the methods changed.

{% include perception-series-nav.html %}
