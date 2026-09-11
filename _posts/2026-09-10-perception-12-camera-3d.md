---
title: 'How Self-Driving Cars See — 12: Estimating three-dimensional objects with cameras'
date: '2026-09-10'
permalink: /autonomous-driving-perception/12-camera-3d/
excerpt: We can now build three-dimensional detections from lidar. What changes if the car uses cameras for this task? The output may still be a box in meters, but the geometry entering the system is less direct. Depth must be estimated from appearance, multiple views, time, or some combination.
tags:
- autonomous vehicles
- perception
- deep learning
- perception series
series_number: 12
read_time: false
---

{% include perception-series-nav.html %}

We can now build three-dimensional detections from lidar. What changes if the car uses cameras for this task? The output may still be a box in meters, but the geometry entering the system is less direct. Depth must be estimated from appearance, multiple views, time, or some combination.

Camera-based three-dimensional detection is not one method. This chapter compares three routes: estimate object properties directly, reconstruct depth and create points, or carry uncertain depth into a spatial feature representation. Each places the difficult inference at a different point in the pipeline.

## Direct regression predicts object properties from image features

A model can take image features and predict a three-dimensional center, dimensions, and orientation. The center may be represented through an image position and a depth estimate, then converted to camera or vehicle coordinates using calibration.

This gives the network a structured output without requiring a dense depth map for every pixel. It can focus training on annotated objects. The downside is that geometric inference is tightly tied to object detection and the appearance evidence available for each candidate.

[FCOS3D, by Wang and colleagues, ICCV Workshops 2021](https://arxiv.org/abs/2104.10956), is a primary example of one-stage monocular three-dimensional detection. It adapts dense image-based prediction to geometric object properties. The paper is useful for seeing how the outputs and assignment rules must change when moving from two to three dimensions.

Direct prediction is not inherently free of geometry. Projection rules can still connect outputs to physical coordinates, and losses can encode geometric relationships. “Direct” describes where the predictions are made, not an absence of mathematical structure.

## Dense depth creates a different intermediate representation

Another approach estimates depth across the image. Given a pixel, its camera ray, and its estimated depth, the system can reconstruct a three-dimensional point. Repeating this produces a point cloud inferred from the camera.

[Pseudo-LiDAR, by Wang and colleagues, CVPR 2019](https://arxiv.org/abs/1812.07179), explores using reconstructed visual depth as point-cloud input for three-dimensional detection. It highlights that the representation used after depth estimation can strongly affect downstream performance.

The name should not obscure the source of evidence. These are inferred points, not laser measurements. If depth is wrong, the reconstructed geometry is wrong even if the resulting cloud looks familiar to a lidar detector.

A visual depth map can also be much denser than an actual lidar scan. That density supplies more samples of the model's estimate, not necessarily more independent physical evidence. Thousands of consistently misplaced points can reinforce an incorrect surface.



<figure>
  <a href="{{ '/images/perception-series/12.svg' | relative_url }}" aria-label="Open diagram at full size" style="width:100%;"><img src="{{ '/images/perception-series/12.svg' | relative_url }}" alt="Camera features branch into direct box prediction, depth-to-point-cloud reconstruction, and depth-weighted spatial features." width="720" height="490" style="height:auto;" loading="lazy"></a>
  <figcaption>Camera 3D methods differ in where they estimate geometry and which intermediate representation they retain. Original diagram for this series.</figcaption>
</figure>

## Depth errors stretch geometry along viewing rays

For a fixed pixel direction, changing estimated depth moves the reconstructed point along that ray. Nearby pixels on a truck side can therefore form a distorted surface if their depth errors differ. A clean image boundary does not guarantee a clean three-dimensional boundary.

The error can be especially troublesome near occlusion edges. Pixels on the truck and pixels on the background belong to different depths. A depth estimate that blends across the boundary can create points in the empty gap between surfaces.

Stereo helps by supplying another view, but correspondence errors remain possible. Monocular methods rely more strongly on appearance and learned geometric regularities. Neither should be described only by the visual sharpness of a displayed depth map.

For detection, the most relevant depth quality may be near object surfaces and centers rather than averaged uniformly across the image. A model can reduce overall depth error by improving large easy regions while still leaving difficult road users poorly localized.

## Training-time sensors and inference-time sensors are different

A camera-only inference model may use lidar-derived depth or three-dimensional boxes during training. That is a valid design, but the distinction must be stated. “Camera-only” often describes the inputs required when the trained model runs, not every source of supervision used to create it.

Likewise, a pretrained depth estimator may have learned from additional datasets. Those data can supply valuable priors, but they affect comparisons with a model trained only on the target benchmark. Training resources belong in the experimental description.

[BEVDepth, by Li and colleagues, AAAI 2023](https://arxiv.org/abs/2206.10092), uses explicit depth supervision and camera information to improve the depth estimation supporting camera BEV detection. It provides an example of treating geometric supervision as a central component rather than assuming the final detection loss will teach everything equally well.

Supervision itself can be incomplete. Projected lidar samples do not cover every image pixel, and visibility must be handled carefully. A sparse depth label should not be interpreted as a dense, perfectly observed surface without understanding how it was generated.

## A distribution can retain several depth possibilities

Instead of predicting one depth, a model can assign weights to discrete depth intervals. For one image location, it might place substantial weight at two candidate distances. This retains more ambiguity than choosing one value immediately.

Suppose the possibilities are 10 and 30 meters. Their mean is 20 meters, but a surface may not exist there at all. Carrying the two hypotheses separately can preserve information that averaging loses. The later network can use other cameras, context, or temporal evidence to resolve the ambiguity.

A discrete distribution is still an approximation. Its range excludes distances outside the selected interval, and its bins limit how finely uncertainty is represented. The learned weights also need not be calibrated probabilities merely because they sum to one.

The next chapter will use this representation to move image features into a top view. This is a transition from estimating isolated object properties toward building a shared spatial representation that can support multiple tasks.

## Camera geometry must travel with the features

A camera network often receives resized or cropped images. Chapter 4 showed that those operations change the relation between pixels and rays. Any reconstruction or projection stage must use the corresponding camera geometry.

Different camera rigs can have different focal lengths, heights, and orientations. A model may encounter the same apparent object size at different metric distances under different intrinsics. Providing geometry explicitly can help, but training coverage and architecture still influence transfer.

A model can also use positional information embedded in features. The important question is whether the representation actually encodes the geometric relationship needed by the transformation, and whether it remains correct after preprocessing.

This is why camera 3D detection should not be reduced to adding a depth output to an image detector. Its measurements, supervision, coordinate transformations, and output conventions form one connected problem.

## What to compare across the three routes

For direct object prediction, inspect missed detections and geometric errors on matched objects. For depth-to-point reconstruction, inspect both the depth estimate and how the detector handles its distortions. For spatial feature lifting, inspect whether features are assigned to useful locations and whether later tasks can correct ambiguity.

Runtime boundaries differ as well. A separate depth model plus a point-cloud detector may cost more than either stage alone. A dense lifting operation can create large intermediate arrays. Direct prediction may be compact but still require a substantial image backbone.

None of these architectural observations establishes a universal ranking. A fair comparison controls data, input resolution, camera configuration, temporal context, and evaluation protocol. Improvements can come from stronger supervision or larger image features as well as from the intermediate representation.

For our truck, the practical target remains the same: useful geometry in a common physical frame, accompanied by appropriate uncertainty. The routes differ in how they derive that target from incomplete visual evidence.

## Inspect one object through the pipeline

For the parked truck, inspect the input crop, predicted depth near its edges, reconstructed points if present, and the final box. If the image boundary is correct but the reconstructed side bends into the background, the error began before the box head. If the points are reasonable but the box heading is wrong, the later detector deserves closer inspection.

This sequence makes debugging concrete. Looking only at the final score cannot distinguish errors in visual recognition, depth, coordinate transformation, and object fitting. The same decomposition helps evaluate a paper: an intermediate representation is valuable when it changes the relevant failure mode, not merely because it looks more like a familiar sensor output.

## Check your understanding

Does a dense pseudo point cloud contain direct range measurements? No. Its coordinates inherit the accuracy and assumptions of visual depth estimation. More reconstructed points do not necessarily mean more independent evidence.

Can a camera-only model have used lidar during training? Yes. The inference input and the supervision source are separate properties that should both be reported.

Next we will follow image evidence into a shared top-view grid, step by step, through Lift-Splat-Shoot.

{% include perception-series-nav.html %}
