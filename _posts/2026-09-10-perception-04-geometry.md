---
title: 'How Self-Driving Cars See — 04: How does a pixel become a position on the road?'
date: '2026-09-10'
permalink: /autonomous-driving-perception/04-geometry/
excerpt: 'A detector says the pedestrian is near the right side of the image. The car needs to know something different: where is that person relative to the bumper and the road? Connecting those descriptions requires geometry. A neural network can estimate unknown quantities, but the coordinate systems still have to agree.'
tags:
- autonomous vehicles
- perception
- deep learning
- perception series
series_number: 4
read_time: false
---

{% include perception-series-nav.html %}

A detector says the pedestrian is near the right side of the image. The car needs to know something different: where is that person relative to the bumper and the road? Connecting those descriptions requires geometry. A neural network can estimate unknown quantities, but the coordinate systems still have to agree.

We will use a simple camera model and a few small calculations. The aim is to understand which information projection preserves and which information it loses. These ideas will later explain why lidar is useful, why camera depth is difficult, and how several cameras can contribute to a shared map.

## Coordinates describe a position relative to a chosen frame

A point does not have one universal set of numbers. Its coordinates depend on where the origin is and which directions the axes point. In a camera frame, the origin is often the camera center. In a vehicle frame, it may be a specified point on the car. In a map frame, it may be a fixed reference in the environment.

For this chapter, use a camera convention in which X points right, Y points down, and Z points forward. Other conventions are common, so never infer the convention just from the letter names. A point with coordinates (1, 0, 10), in meters, lies one meter to the camera's right and ten meters forward.

The **extrinsic calibration** describes how to transform coordinates between frames. It contains a rotation and a translation. Rotation changes how the axes are oriented; translation accounts for the offset between origins. A point measured by roof-mounted lidar must undergo such a transformation before it can be compared with a windshield camera's view.

Order matters. Rotating a point about one origin and then translating it generally differs from translating first and rotating afterward. Implementations therefore need an explicit convention for what a transform maps from and to. A plausible-looking picture is not enough to establish correctness.

## The pinhole model turns a 3D point into a pixel

Imagine a small opening through which light reaches a flat image plane. Similar triangles give a simple projection rule. If the horizontal focal length in pixel units is f, and the horizontal image center is c, then the projected horizontal position is:

**u = f × X / Z + c**

Here, X and Z are coordinates in the camera frame, and u is a pixel coordinate. A corresponding equation gives the vertical position. Real camera models also handle effects such as lens distortion. The [OpenCV calibration documentation](https://docs.opencv.org/4.x/d9/d0c/group__calib3d.html) provides the standard pinhole formulation and definitions used in many implementations.

The focal lengths and image-center parameters form the camera's **intrinsic calibration**. They connect directions in camera coordinates to positions in the image. Intrinsics describe the imaging geometry; extrinsics describe the camera's placement relative to another frame.

For a numerical example, let f be 800 pixels and c be 640 pixels. Our point (1, 0, 10) projects to u = 720. Now double both X and Z: the point (2, 0, 20) also projects to 720. The image location alone cannot distinguish them.



<figure>
  <a href="{{ '/images/perception-series/04.svg' | relative_url }}" aria-label="Open diagram at full size" style="width:100%;"><img src="{{ '/images/perception-series/04.svg' | relative_url }}" alt="Two points at different distances lie on the same camera ray and project to the same image location." width="720" height="460" style="height:auto;" loading="lazy"></a>
  <figcaption>Projection divides by depth. Points along one ray can share a pixel, so recovering distance requires additional evidence. Original diagram for this series.</figcaption>
</figure>

## A pixel gives a ray, not a unique point

If we know u, f, and c, we can rearrange the equation to obtain X/Z. This gives a direction from the camera. The set of possible three-dimensional points extends along a ray. To choose a particular point, we need a distance or an additional constraint.

One possible constraint is that the point lies on a known ground plane. A ray can be intersected with that plane to estimate where a road point lies. This is useful for some road geometry problems, provided the assumption is appropriate.

It is unsuitable for every visible pixel. The top of the truck does not lie on the road. Treating it as a ground point moves it to the wrong place. A hill also violates a flat-ground assumption unless the local surface model is updated. A bird's-eye image produced by a simple ground-plane warp should therefore not be mistaken for a complete reconstruction of the scene.

This distinction motivates learned view transformation later in the series. Instead of sending every pixel to a predetermined ground location, a model can estimate where along the ray its evidence should contribute. That choice is still uncertain, even when represented by many learned parameters.

## Stereo adds a second view

Two cameras observe the same surface from different positions. If we can identify corresponding image points, the two viewing rays constrain a three-dimensional location. For a simplified rectified stereo pair, depth follows:

**Z = f × B / d**

B is the separation between the camera centers, called the baseline. The quantity d is the horizontal difference between corresponding pixel positions, called disparity. Rectification is a transformation that makes corresponding points lie along matching image rows under the model's assumptions.

With f = 800 pixels, B = 0.2 meters, and d = 8 pixels, the estimated depth is 20 meters. If disparity is measured as 7 pixels instead, the depth becomes about 22.9 meters. A one-pixel difference can therefore produce a substantial distance change.

Finding correspondences is its own problem. A blank truck side may contain many similar-looking locations. A reflective window can look different from different viewpoints. A surface visible in one camera may be hidden in the other. Stereo reduces ambiguity by adding evidence, but does not make every point easy to reconstruct.

## Image processing changes geometry too

Suppose an image is resized to half its original width. The horizontal pixel coordinates, horizontal focal length in pixels, and horizontal image-center coordinate must all scale consistently. Otherwise the same physical direction appears to point somewhere else in the model.

Cropping shifts the image origin. A point's coordinates must be expressed relative to the new crop, and the intrinsic parameters used with that crop must reflect the shift. Padding creates a similar bookkeeping requirement. These are small operations with potentially large downstream effects.

This becomes especially important in learned systems because image augmentation is common during training. If the pixels are transformed but the projection geometry is not, a model receives contradictory evidence. It may partially compensate during training, obscuring a bug that later appears under different conditions.

The same principle applies to flipping, rotating, or augmenting three-dimensional data. Points, boxes, velocity vectors, and sensor transformations have to describe one coherent transformed scene. Correctness depends on their relationships, not on any one array looking reasonable in isolation.

## Motion introduces another transformation

A camera mounted on a moving car does not keep the same pose in the world. A stationary pole changes coordinates in the camera frame as the car passes it. To combine observations across time, we need the relative pose between the earlier and later sensor frames.

If we transform an old point into the current vehicle frame using the car's motion, stationary structure can align. A moving cyclist still changes position after this compensation. The remaining difference may represent the cyclist's movement, measurement error, or both.

This explains why temporal fusion must distinguish self-motion from object motion. Applying the vehicle transform to every historical point does not freeze moving objects in place. Assuming it does can create duplicated or stretched shapes in an accumulated point cloud.

The reference time should also be explicit. A system might align observations to the latest camera exposure, the start of a lidar sweep, or another selected timestamp. Each choice can work if the transformations and downstream interpretation are consistent.

## Check a transformation with a physical example

Before trusting a large model, test simple geometry. A point directly ahead of a correctly modeled camera should project near the principal point. Moving the point farther away along the same ray should preserve its image location. A point behind the camera should not be treated as an ordinary visible point in front.

A lidar point on a visible truck edge should project near that edge when the sensors are calibrated and aligned in time. If all projected points shift in a similar direction, inspect the transformation conventions. If the mismatch changes with motion, timing may deserve attention.

These checks do not prove that a whole system is correct, but they make assumptions testable. They are especially useful because learned models can sometimes hide small inconsistencies by adapting to the training data.

## Check your understanding

Can a single pixel specify both direction and distance? Under the pinhole model, it specifies a direction once intrinsics are known. Distance requires another measurement, an assumption, or an estimate from learned context.

Can a road-plane transformation place the truck roof correctly on a top view? Not in general. The roof violates the plane assumption, so its apparent position can be wrong.

We now know why image recognition and physical localization are different tasks. Next, we return to the early deep learning era and examine how a classifier became a detector that finds objects within an image.

{% include perception-series-nav.html %}
