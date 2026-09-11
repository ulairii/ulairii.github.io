---
title: 'How Self-Driving Cars See — 08: Why a correct image box is not enough'
date: '2026-09-10'
permalink: /autonomous-driving-perception/08-why-3d/
excerpt: A box fits the parked truck perfectly in the camera image. Its category is correct, its score is high, and its visible outline is clear. Can the car now decide how much space remains beside it? Not yet. The box describes where the truck appears, not where its surfaces lie in meters.
tags:
- autonomous vehicles
- perception
- deep learning
- perception series
series_number: 8
read_time: false
---

{% include perception-series-nav.html %}

A box fits the parked truck perfectly in the camera image. Its category is correct, its score is high, and its visible outline is clear. Can the car now decide how much space remains beside it? Not yet. The box describes where the truck appears, not where its surfaces lie in meters.

This chapter connects the image methods we have studied to the three-dimensional methods that follow. The central issue is information: which physical properties can change while leaving a similar image, and what extra evidence could distinguish those possibilities?

## Image overlap and physical overlap are different

A cyclist may overlap the truck's box in the image while remaining several meters in front of it. Another cyclist may appear just outside the box while passing dangerously close to its side. Perspective does not preserve physical separation in a simple image-distance measure.

A planner typically needs geometry in a common physical frame. It must compare the car's intended path with the estimated positions and extents of nearby objects. Pixel coordinates from different cameras cannot be directly compared as if they were meters on one map.

Chapter 4 showed why: projecting a point divides its lateral coordinates by depth. Different three-dimensional points can lie on the same camera ray. A detector's success at image localization does not remove that ambiguity.

This does not make image detection unhelpful. Finding the truck restricts where to inspect appearance and which geometric assumptions might apply. It simply leaves additional quantities to estimate before the image description becomes a metric scene description.

## Size can suggest depth, if the size assumption is right

Under a simplified pinhole model, an upright object of physical height H projects to an image height h approximately proportional to focal length f divided by depth Z. Rearranging gives **Z ≈ f × H / h** under the relevant geometric assumptions.

For an illustrative pedestrian with H = 1.7 meters, f = 800 pixels, and h = 68 pixels, the estimate is 20 meters. If the visible height is only 54 pixels because the legs are hidden, using it as the full height gives about 25.2 meters. The apparent geometry alone does not identify the cause.

Actual people have different heights. The object may lean, the road may slope, and the camera may tilt. A network can learn patterns associated with these variations, but the calculation reveals why an assumed physical size is a source of uncertainty rather than a direct range measurement.

A crop can also hide useful context. The same resized pedestrian crop might originate from different image locations and scales. If those original quantities are discarded, some geometric evidence disappears. Features useful for classification and features useful for physical localization need not be identical.



<figure>
  <a href="{{ '/images/perception-series/08.svg' | relative_url }}" aria-label="Open diagram at full size" style="width:100%;"><img src="{{ '/images/perception-series/08.svg' | relative_url }}" alt="A small nearby object and a larger distant object have the same apparent image height. A separate top view shows their different physical positions." width="720" height="460" style="height:auto;" loading="lazy"></a>
  <figcaption>Similar image extent can correspond to different metric geometry. The example illustrates ambiguity rather than a measured experiment. Original diagram for this series.</figcaption>
</figure>

## A 3D box introduces more unknowns

A common three-dimensional detection output includes a center position, three dimensions, and a heading angle. In road scenes, heading is often rotation around an approximately vertical axis. Some methods or applications estimate additional orientation components, velocity, or uncertainty.

The center may be the geometric center or another specified reference point. That convention matters. A box reported at its bottom center cannot be compared directly with one reported at its full-volume center without conversion. Coordinate frames and units must be stated alongside the numbers.

Orientation also changes the space an object occupies. A long truck turning across a lane can have a similar center position but a very different footprint from one aligned with the road. A class label and center point alone can miss that distinction.

The **amodal** extent of an object refers to its full estimated shape or box even when part is hidden. Predicting that extent requires inference beyond directly visible surfaces. An annotation may supply the target, but the model still has to infer it from incomplete observations at test time.

## Geometric constraints can reduce the search

One approach is to predict dimensions and orientation from appearance, then use camera geometry and the image box to constrain translation. [Deep3DBox, by Mousavian and colleagues, CVPR 2017](https://arxiv.org/abs/1612.00496), is an early example of combining learned object properties with geometric reasoning for three-dimensional boxes.

A useful way to understand this family is to separate the estimated quantities from the enforced relationships. A network predicts some unknowns. Projection equations connect those predictions to observed image geometry. Solving or optimizing those relationships produces a candidate three-dimensional configuration.

Constraints help only when their assumptions are suitable. If an image box is truncated at the frame edge, it may not reflect the full projected object. If the road-user category has highly variable dimensions, a tight size prior can be misleading. A geometry layer cannot repair incorrect premises automatically.

The benefit is that the method makes some relationships explicit. Instead of asking a network to discover every connection between pixels and meters implicitly, the architecture can encode known projection structure and focus learning on uncertain object properties.

## Additional views provide additional constraints

Stereo cameras observe a surface from separated viewpoints. Matching corresponding pixels can estimate depth by triangulation, as Chapter 4 explained. Several cameras on a car may also observe overlapping regions, although overlap, baseline, and viewing direction vary.

Video adds observations over time. If the camera moves and the scene is sufficiently constrained, the changing view provides geometric information. Moving objects complicate this because the camera and object can both change position between frames.

Lidar offers another route: measured surface distances. It does not require matching visual texture to recover a range, though it has its own sampling and reflection limitations. A detector can use that metric evidence directly or combine it with image features.

These are different ways of constraining the same unknown scene. They explain why the field developed camera-only, lidar-only, and fusion methods in parallel. Each route exposes a different balance of measurement quality, coverage, cost, and computation.

## Errors should be measured in the space where they matter

Imagine two predicted boxes with similar image overlap. One places a vehicle two meters too far away; the other has nearly correct depth but a slightly imperfect silhouette. Their implications for physical interaction can differ despite similar image-space scores.

Three-dimensional detection benchmarks therefore define geometric comparisons in physical coordinates. Some use three-dimensional or bird's-eye-view box overlap. The [nuScenes detection task](https://www.nuscenes.org/object-detection) also measures errors such as translation, scale, orientation, and velocity under its specified matching and scoring rules.

No single metric captures every consequence. A modest error beside the car can matter differently from the same error far outside the planned route. We still need task-level evaluation, but metric geometry makes the representation better suited to those questions.

Evaluation conventions must be read carefully. Results can depend on object range, visibility, class definitions, and the set of valid annotations. A score from one dataset is not directly interchangeable with a score from another merely because both are called three-dimensional detection accuracy.

## Three dimensions do not solve every representation problem

A box is still an approximation. It may include empty space around a motorcycle or omit fine structure such as an open door. A box-based model also usually predicts a selected category vocabulary rather than arbitrary surface geometry.

The road itself is not naturally described by a collection of vehicle boxes. Lane boundaries, curb shape, and empty space require other outputs. Later chapters will add vector maps and occupancy representations, while retaining object detections where they are useful.

Nor does a three-dimensional box describe the future. A current heading is not a promise that the object will continue straight. A velocity estimate is evidence about recent motion, not a complete behavior model. The separation between perception, tracking, and prediction remains important.

For our truck, the immediate gain is more modest and concrete: a representation in meters that can be compared with the car's position and intended motion. That is a substantial improvement even before all other problems are solved.

## Check your understanding

Why might estimating depth from a pedestrian's image height fail under occlusion? The visible height can be smaller than the projected full height, so treating it as the whole person can produce an excessive distance estimate.

Does a correct 3D center establish an accurate occupied region? No. Dimensions, orientation, and shape approximation also matter. A center is one part of the representation.

We are ready to examine the lidar branch. The next chapter begins with a surprising computational issue: a point cloud has useful three-dimensional coordinates, but lacks the regular ordering that makes image convolution convenient.

{% include perception-series-nav.html %}
