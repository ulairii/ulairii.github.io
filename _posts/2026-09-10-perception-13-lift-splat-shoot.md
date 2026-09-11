---
title: 'How Self-Driving Cars See — 13: Building one bird’s-eye view from several cameras'
date: '2026-09-10'
permalink: /autonomous-driving-perception/13-lift-splat-shoot/
excerpt: Our car has several cameras facing different directions. Each produces useful features, but those features live in separate image coordinate systems. A cyclist seen near one camera's edge may appear again in another. The planner would rather receive one spatial description around the car.
tags:
- autonomous vehicles
- perception
- deep learning
- perception series
series_number: 13
read_time: false
---

{% include perception-series-nav.html %}

Our car has several cameras facing different directions. Each produces useful features, but those features live in separate image coordinate systems. A cyclist seen near one camera's edge may appear again in another. The planner would rather receive one spatial description around the car.

Lift-Splat-Shoot offers a clear way to construct such a description. It estimates where image evidence might lie in three-dimensional space, places weighted features there, and combines them into a bird's-eye-view grid. The method is especially useful to study because every stage connects directly to geometry from earlier chapters.

## Begin with one image location

A camera backbone produces a feature vector at each location of a reduced-resolution image feature map. The vector encodes learned visual evidence from a surrounding region. Its spatial location can be related to an original image direction using the image processing and calibration conventions.

That direction defines a ray. It does not identify a unique point, because depth remains unknown. The model therefore also predicts a distribution over selected depth bins for that feature location.

The feature vector answers something like “what useful visual evidence is here?” The depth weights answer “where along this ray might that evidence belong?” Separating these roles gives the method a structured way to move appearance into space.

This explanation is based on [Lift-Splat-Shoot, by Philion and Fidler, ECCV 2020](https://arxiv.org/abs/2008.05711). Its original experiments include BEV segmentation and a planning component. It should not be described as originally identical to every later camera 3D detector that uses a related lifting operation.

## Lift: keep a weighted feature at each candidate depth

For each depth bin, multiply the visual feature vector by that bin's weight. The result is a collection of weighted features along the viewing ray. Repeating this across image locations creates a frustum-shaped set of candidate spatial features.

Here is an illustrative calculation. Let one feature channel have value 4, and let three depth bins receive weights 0.1, 0.7, and 0.2. The corresponding lifted values are 0.4, 2.8, and 0.8. The evidence is strongest at the middle candidate, but the alternatives are retained.

This is a feature representation rather than a set of confirmed surface points. A nonzero value at a candidate depth does not mean a physical object has been measured there. The weight expresses a learned allocation of evidence for the task.

The distinction matters when visualizing the result. A spread of lifted features can reflect depth ambiguity. It should not be interpreted as a thick physical object unless the decoded output and its semantics support that interpretation.



<figure>
  <a href="{{ '/images/perception-series/13.svg' | relative_url }}" aria-label="Open diagram at full size" style="width:100%;"><img src="{{ '/images/perception-series/13.svg' | relative_url }}" alt="An image feature with depth weights is lifted along a ray, transformed into vehicle coordinates, and summed into top-view cells across cameras." width="720" height="510" style="height:auto;" loading="lazy"></a>
  <figcaption>Lift retains candidate depths. Splat places their weighted features into a common grid, where different cameras can contribute to the same cell. Original diagram for this series.</figcaption>
</figure>

## Geometry places the candidates in a shared frame

Each pixel direction and candidate depth gives a point in camera coordinates. The camera's extrinsic transform then maps that point into the vehicle frame. Now features from different cameras can be compared by their spatial coordinates rather than by unrelated image positions.

This uses known calibration. It is not an arbitrary learned rearrangement of pixels into a map. Learning estimates features and their depth allocation, while geometry supplies the relation between camera rays and the shared coordinate system.

Resizing and cropping must be reflected in that geometry. A correct depth weight associated with an incorrect ray still places evidence in the wrong region. Calibration errors can also shift contributions from different cameras so they fail to align.

The selected depth range and BEV boundaries limit coverage. Features outside the chosen region may be discarded. These design settings determine the space the network represents, independently of whether the cameras can see farther.

## Splat: combine features that land in the same cell

After transformation, the method assigns candidate features to cells of a spatial grid. Features sharing a cell are aggregated. In the BEV construction, information across height is pooled into a horizontal representation that a two-dimensional network can process.

A cell may receive contributions from several pixels, depths, and cameras. If the geometry and depth allocation are useful, those contributions can reinforce a consistent interpretation of the scene. A later BEV network combines nearby cells and produces task outputs.

Aggregation also loses provenance unless the representation explicitly preserves it. A summed feature does not inherently tell the next layer which camera supplied each component. The architecture and learned channels determine how much source-specific information survives.

More contributions are not always better. Several cameras can share a systematic calibration error, and an incorrect depth distribution can place strong evidence in the wrong cells. Fusion combines evidence; it does not make all contributing estimates independent or correct.

## Why this is more than warping a road image

A simple ground-plane transformation assumes each relevant pixel lies on the road surface. That can work for road markings under suitable geometry, but it misplaces elevated parts of objects. A truck roof and the road beneath it project differently because they lie at different heights.

Lifting considers depth along each ray before pooling into BEV. It therefore provides a route for elevated visual evidence to contribute according to an estimated three-dimensional location. The final horizontal compression remains a design choice with limits, but it is not the same operation as assuming all pixels are ground points.

Nor is the output a stitched photograph from above. The BEV grid contains learned channels. A decoder may turn them into a vehicle mask or road map, but those visible predictions are only one interpretation of the internal features.

This makes the representation reusable. Different heads can read the same spatial features for different tasks, provided training supplies the necessary targets and the feature capacity is sufficient.

## What does Shoot refer to?

The original LSS work also considered planning using predicted BEV costs and candidate trajectories. This is the “Shoot” part of its name: candidate motions can be evaluated against the spatial representation to select a plan.

Later papers frequently reuse the lifting and aggregation idea while building a different prediction system. Calling an encoder “LSS-style” does not mean the whole original planning procedure is present. When reading a method, identify which components are actually used.

This is a useful habit beyond LSS. A model name can become shorthand for one operation even though the original paper proposed a larger system. Accurate comparisons should describe the implemented computation rather than relying entirely on a familiar label.

For this series, the lasting bridge is from multi-camera image features to a shared metric representation. Planning will return in Chapter 21, after we have understood more of the information the representation can carry.

## What supervises the depth weights?

In an end-task training setup, depth-related parameters can receive gradients through the final BEV objective. That means the model can learn where to place evidence because some placements make the output better. It does not guarantee a physically accurate or calibrated depth distribution at every pixel.

Explicit depth supervision provides additional constraints. [BEVDepth, by Li and colleagues, AAAI 2023](https://arxiv.org/abs/2206.10092), studies this issue for camera BEV detection. It is a useful follow-up because it asks whether better geometric guidance improves the representation used by the detector.

The supervision source must be described. Lidar-derived depth labels can be used in training while the deployed model takes only images. This is different from using lidar as an inference input, and comparisons should distinguish the two.

Depth accuracy and task accuracy are related but not identical. A task can tolerate some errors or exploit context, while a depth benchmark may emphasize different regions. Both should be inspected when making claims about what the network has learned.

## Two cameras contributing to one location

Suppose two calibrated cameras both observe part of the truck. Their corresponding feature locations need not have the same pixel coordinates or even similar appearances. After candidate depths are transformed into the vehicle frame, useful contributions can nevertheless reach the same BEV neighborhood.

If one camera places the truck too far away, its evidence lands in different cells. A later network may resolve the inconsistency using context, but the pooling step itself does not know which estimate is correct. This example explains both the appeal of a shared spatial grid and the continued importance of depth estimation. Geometric alignment creates an opportunity for agreement; it does not enforce the truth of every contributing feature.

## Check your understanding

Why are features spread over several depths instead of immediately placed at one distance? The image may support several plausible depths. Retaining weights allows later processing to use that ambiguity rather than committing to a single possibly wrong point.

Is a BEV cell a ground-plane photograph pixel? No. It is a location in a metric feature grid, potentially containing pooled evidence from several heights and cameras.

Next we will reverse the direction of information gathering: start with a spatial query and ask which image evidence should update it. That is the central intuition behind the BEVFormer chapter.

{% include perception-series-nav.html %}
