---
title: "How Self-Driving Cars See — 01: What Does a Car Need to Know at an Intersection?"
date: 2026-09-10
series_number: 1
read_time: false
permalink: /autonomous-driving-perception/01-intersection/
excerpt: "Follow one car toward a crossing to understand perception, tracking, prediction, and the information that connects them."
tags:
  - autonomous vehicles
  - perception
  - deep learning
  - perception series
---

{% include perception-series-nav.html %}

Imagine sitting in a car approaching an intersection. A delivery truck is parked near the corner. A pedestrian stands beside it. The traffic light is green, and a cyclist is moving along the right side of the road.

You can describe the scene in one sentence. A computer needs something more precise. Where is the pedestrian relative to the car? Is the cyclist moving into its path? Does the green light control this lane? What part of the pavement is hidden behind the truck?

These questions explain why autonomous driving perception has changed so much. Finding familiar objects in a picture is useful, but driving also requires distance, motion, road structure, and an honest account of what cannot be seen.

We will return to this intersection throughout the series, changing how the car represents it as we introduce each method.

## Start with the information a decision requires

Suppose the car needs to continue straight through the intersection. A navigation route can tell it which road to take. That route does not tell it whether someone has just stepped off the curb.

**Perception** is the process of estimating that description from sensor measurements. Cameras provide images. A laser scanner, usually called lidar, measures distances to surfaces. Radar provides measurements that can include distance and motion toward or away from the sensor. We will examine their differences in Chapter 2.

Sensor measurements are evidence, rather than ready-made answers. A camera records light, not a list of pedestrians. A lidar return indicates a measured surface point, not automatically the identity of the object that produced it. Software must interpret these measurements.

For our intersection, useful outputs include the truck's position and size, the pedestrian's location, the cyclist's motion, the lane boundaries, and the state of the relevant traffic light. These outputs need to share a meaningful coordinate system. “A pedestrian is at pixel 420” does not directly tell the car how much room it has to stop.

<figure>
  <a href="{{ '/images/perception-series/intersection.svg' | relative_url }}" aria-label="Open diagram at full size" style="width:100%;"><img src="{{ '/images/perception-series/intersection.svg' | relative_url }}" alt="Top view of a car approaching a crossing, with a parked truck beside the road, a pedestrian beyond the truck, and a cyclist to the right. A shaded area beyond the truck marks space the car cannot directly observe." width="720" height="625" style="height:auto;" loading="lazy"></a>
  <figcaption>A simplified intersection. The shaded region is hidden from the approaching car by the truck. Object positions are illustrative; the drawing is not to scale.</figcaption>
</figure>

## Finding an object is only the first step

An **object detector** estimates where objects are and assigns categories such as vehicle, pedestrian, or bicycle. In an image, it often draws a rectangle around each object. In three dimensions, it may estimate a box with a position, width, length, height, and orientation.

A box is a compact description. The planner does not need every paint mark on the truck to reason about passing it. It does need a useful estimate of the space the truck occupies. A three-dimensional box provides one approximation to that space.

The approximation has limits. A rectangle around a pedestrian contains background pixels. A box around a truck does not describe every mirror or open door. An object detector trained on a fixed list of categories may also struggle with an unusual object lying in the road.

Other outputs answer different questions. **Semantic segmentation** assigns a category to each image pixel or spatial element: road, sidewalk, vehicle, and so on. **Occupancy estimation** describes whether regions of space contain matter. These are different ways of representing the scene, and a driving system can use more than one.

Public research datasets make these distinctions concrete. The [Waymo Open Dataset perception paper](https://arxiv.org/abs/1912.04838), by Sun and colleagues, describes camera and lidar data with object annotations for studying perception. Measurements and annotations are separate: researchers train models to recover useful descriptions from the measurements.

## A cyclist in two pictures: detection becomes tracking

Now consider two images taken a short time apart. Both contain a cyclist. Are the two detections the same person? How far has that person moved?

**Tracking** connects observations across time. It maintains an estimate of an object's identity and state as new measurements arrive. That state might contain position, direction, and speed. Linking observations allows the system to estimate motion and keep some continuity when an object is briefly obscured.

The car's own movement complicates this task. A stationary truck appears to move across the camera image as the car passes it. To estimate the truck's movement in the world, the system must account for the movement of the sensor itself.

This is one reason a single image is often insufficient. A sequence provides evidence about change, but that evidence has to be aligned. Simply averaging recent positions can make a moving cyclist appear behind their actual location.

The [nuScenes tracking task](https://www.nuscenes.org/tracking) explicitly builds on object detection by following objects over time. Detecting an object again and recognizing it as the same object are separate problems.

## What is happening now, and what might happen next?

Tracking estimates motion from observations. **Prediction** estimates possible future behavior. A cyclist moving straight now may turn at the intersection. A pedestrian standing still may begin to cross.

The distinction matters because the future is not directly measured. The system can observe a pedestrian's recent positions and use the road layout as context, but it cannot read the pedestrian's intention. A useful prediction may therefore describe several possible paths, with uncertainty about which will occur.

**Planning** uses the estimated scene, possible future behavior, route, and driving constraints to choose the car's own motion. It might choose a path and speed that leave more room beside the cyclist, or slow down before reaching the region hidden by the truck.

**Control** then turns the chosen motion into steering, braking, and acceleration commands. As new measurements arrive, the process repeats. The chosen plan must be updated because people move, observations change, and the car does not follow every command perfectly.

<figure>
  <a href="{{ '/images/perception-series/driving-tasks.svg' | relative_url }}" aria-label="Open diagram at full size" style="width:100%;"><img src="{{ '/images/perception-series/driving-tasks.svg' | relative_url }}" alt="Sensor measurements feed perception and tracking, which describe the current scene. Prediction estimates possible future motion. Planning selects the car's motion, and control produces steering and braking commands. Position, road layout, and route also inform the process." width="690" height="635" style="height:auto;" loading="lazy"></a>
  <figcaption>A teaching diagram of the main tasks. Real systems may share a network across tasks, exchange additional information, or organize these computations differently.</figcaption>
</figure>

These names describe responsibilities, not a rule that each responsibility must have its own neural network. Later, we will study methods that train several tasks together. [UniAD, by Hu and colleagues](https://arxiv.org/abs/2212.10156), is one example of organizing perception and prediction around the needs of planning.

## The road matters as much as the objects

An object list cannot fully describe our intersection. The car also needs to know where lanes run, where crossing is expected, and which movements the road allows.

A painted line is useful evidence, but its meaning depends on its surroundings. Two visible line segments may belong to the same lane boundary. An arrow may indicate a turning lane. A traffic signal has to be associated with the movement it controls; recognizing its color alone is insufficient.

A map can supply some of this structure. **Localization** estimates where the car is relative to a reference frame, often a map. Local road perception estimates the structure currently visible around the vehicle. Both are useful when road markings are worn, the car passes through an intersection, or temporary construction changes the layout.

We should also separate empty space from usable road. A sidewalk may contain no obstacles and still be unsuitable for the car's intended path. Knowing that a region is unoccupied does not establish that driving there is permitted or appropriate.

## Hidden does not mean empty

Return to the truck. It blocks part of the scene. If the detector reports no pedestrian behind it, that may simply mean the sensors have no direct evidence from that region.

This is **occlusion**: one object blocks the view of another region or object. A system that treats every unobserved region as empty can produce a confident but misleading description of the world.

There are several kinds of uncertainty here. The truck's visible edge may be measured imprecisely. A small visible shape may be difficult to classify. The region behind the truck may have no direct observation at all. Those situations should not automatically receive the same treatment.

Nor is a detector's confidence score a complete answer. A high score for “truck” does not establish that its distance is accurate, that its surroundings are empty, or that it will remain stationary. Confidence needs to be interpreted in relation to the quantity being estimated.

Later chapters will explain how depth distributions, temporal information, and occupancy representations address parts of this problem. None gives a sensor the ability to directly see through an opaque truck.

## Why time belongs in the description

A scene estimate also has an age. Measurements take time to collect and process. While the software is working, the car and nearby road users continue moving.

For an illustrative calculation, a car traveling at 10 meters per second covers 1 meter in 0.1 seconds. That is just distance equal to speed multiplied by time; it is not a stopping-distance estimate. It shows why an accurate position measured a moment ago may need updating before it is used.

This makes timestamps and motion estimates part of the practical problem. It also explains why a method's accuracy cannot be judged in isolation from how quickly and consistently it runs on the available hardware.

This series examines how representations preserve useful information while keeping computation manageable.

## What to carry into the next chapter

Our car needs more than object names. It needs positions and shapes in a shared space, identities and motion across time, road structure, and uncertainty about observations. Prediction uses that description to consider what may happen. Planning chooses the car's response, and control executes it.

As you read the series, ask three questions about each method: What measurements enter it? What description of the world comes out? What important information can that description lose?

Try those questions on the opening scene. If a detector finds the truck and cyclist perfectly, can it conclude the hidden crossing is clear? No: correct detections of visible objects do not resolve an unobserved region. If the traffic light is green, is its color enough to choose the car's motion? No: the system still needs the relevant lane, nearby road users, and possible conflicts.

In Chapter 2, we will look at the evidence available to answer these questions: what cameras, lidar, and radar actually measure, and why their errors differ.

---

All diagrams in this chapter were created for this series. The linked papers and dataset documentation provide further reading; no prior knowledge of them is required.

{% include perception-series-nav.html %}
