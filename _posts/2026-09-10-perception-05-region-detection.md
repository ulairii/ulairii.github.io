---
title: 'How Self-Driving Cars See — 05: From recognizing a car to finding it in a picture'
date: '2026-09-10'
permalink: /autonomous-driving-perception/05-region-detection/
excerpt: The car is still approaching our intersection, but imagine its software can only classify an entire image. It can report that a vehicle is present somewhere. That answer leaves the planner with almost everything it needs to know still missing.
tags:
  - autonomous driving
series_number: 5
read_time: false
series: perception
---

{% include perception-series-nav.html %}

The car is still approaching our intersection, but imagine its software can only classify an entire image. It can report that a vehicle is present somewhere. That answer leaves the planner with almost everything it needs to know still missing.

Object detection adds locations and handles multiple objects. The important early change was to make learned image features useful for this larger task. Following R-CNN, Fast R-CNN, and Faster R-CNN reveals a sequence of concrete computational bottlenecks, rather than just a list of model names.

## A detector must return a set of answers

An image classifier usually produces a fixed set of category scores for one input. A detector must account for a variable number of objects. Our image might contain a truck, two cars, a pedestrian, and a bicycle, with different sizes and partial overlaps.

A common output is a list of boxes, each accompanied by a category and score. A two-dimensional box can be described by its left, top, right, and bottom coordinates, or by its center, width, and height. Either encoding provides image geometry rather than physical distance.

During training, predicted boxes must be related to annotated objects. A predicted rectangle that covers the truck should not be supervised as the pedestrian simply because both appear in the same image. Detection therefore involves assigning predictions to targets as well as learning features.

An overlap measure called **intersection over union**, or IoU, is often useful. It divides the area shared by two boxes by the area covered by either box. Identical boxes have IoU equal to one; disjoint boxes have zero. Matching policies and thresholds vary by method and evaluation protocol.

## R-CNN asks a classifier about candidate regions

The [R-CNN paper by Girshick and colleagues, CVPR 2014](https://arxiv.org/abs/1311.2524), used a region-proposal method to identify candidate object locations, extracted convolutional features from the regions, and classified them. It also used a learned adjustment to improve box localization.

The proposal stage narrows the search. Instead of testing every possible rectangle, it suggests regions that might contain objects. Those proposals do not have to know the final object class. A later classifier examines their learned features.

This division makes sense for our intersection. One proposal might cover the whole truck. Others might cover its cab, a nearby pedestrian, or background. Classification and geometric refinement help turn that messy candidate set into useful detections.

The expensive part is repeated image processing. Many proposals overlap, so computing a deep representation separately for each region repeats work on much of the same image. It is similar to reading the same paragraph again for every possible phrase someone might ask about.



<figure>
  <a href="{{ '/images/perception-series/05.svg' | relative_url }}" aria-label="Open diagram at full size" style="width:100%;"><img src="{{ '/images/perception-series/05.svg' | relative_url }}" alt="R-CNN computes features for separate crops; Fast R-CNN shares image features; Faster R-CNN also learns proposals from the shared feature map." width="720" height="495" style="height:auto;" loading="lazy"></a>
  <figcaption>The progression moves repeated work into a shared image representation, then makes proposal generation learned. Original diagram for this series.</figcaption>
</figure>

## Fast R-CNN shares the expensive image computation

[Fast R-CNN, introduced by Girshick at ICCV 2015](https://arxiv.org/abs/1504.08083), processes the image with a convolutional network and then extracts a fixed-size feature representation for each proposed region. Its region-of-interest pooling lets differently sized regions feed a common prediction structure.

The practical change is where the crop happens. Rather than repeatedly processing cropped pixels, the system computes a shared feature map and gathers region features from it. The network can then classify the region and predict box adjustments.

A fixed-size region representation is convenient because the following layers expect a consistent shape. Pooling summarizes the values in spatial bins. This operation sacrifices some spatial precision, a detail that later region extraction methods would revisit.

Sharing computation does not mean all objects receive identical information. Each region selects a different portion of the common feature map. The shared image features capture local and contextual evidence, while the region operation gathers evidence relevant to a particular candidate.

## Faster R-CNN learns where to propose regions

After image feature extraction became shared, generating proposals outside the network remained a separate cost. [Faster R-CNN, by Ren and colleagues, NeurIPS 2015](https://arxiv.org/abs/1506.01497), introduced a region proposal network that uses shared convolutional features to predict candidate boxes and objectness scores.

An **anchor** is a reference box with a selected location, size, and shape. The proposal network predicts adjustments relative to such reference boxes. It also estimates whether the region is likely to contain an object, without yet needing the final fine-grained category decision.

The second stage examines proposed regions for classification and further refinement. That is why the method is called two-stage detection. Both stages are learned, and much computation is shared. “Two-stage” describes this organization; it does not mean one stage must run on a CPU and another on a GPU.

The reference boxes provide a way to parameterize the search. They are not a guarantee that real objects match the chosen shapes. Training teaches the network how to adjust them, and design choices influence which sizes and aspect ratios are represented conveniently.

## Classification and box refinement teach different behavior

Suppose a proposed box contains the whole truck plus a strip of road. Its class can be correct while its location is imperfect. A classification loss rewards recognizing the truck; a box loss encourages boundaries that better match the annotation.

Now consider a box that covers only a wheel. It might contain a strong visual cue, but it does not describe the desired object extent. Training targets and assignment rules determine whether that candidate is treated as positive, negative, or ignored.

This is a general lesson for later chapters. Correct semantics do not imply correct geometry. A network can be good at recognizing a vehicle while being less accurate about its exact boundary, orientation, or depth. Separate outputs and losses help specify which quantities matter.

Labels also impose conventions. For an occluded pedestrian, should the box cover only the visible part or the estimated full body? Datasets may use different policies. A prediction can look reasonable to a person and still disagree with the benchmark's target definition.

## Why several boxes appear around one truck

Nearby proposals can all classify the same truck correctly. The detector therefore needs a way to reduce redundant outputs. **Non-maximum suppression**, usually abbreviated NMS, keeps a high-scoring box and removes sufficiently overlapping alternatives according to a chosen rule.

For two boxes around the same truck, this often gives the desired result. For two pedestrians standing close together, aggressive suppression can remove a real object. The overlap threshold balances duplicate removal against the risk of merging nearby instances.

NMS uses scores and geometry; it does not fully understand whether two detections refer to one physical entity. More sophisticated alternatives exist, but the basic example shows why the last processing step can affect recall even when the neural network found useful evidence.

A detector is therefore more than a backbone architecture. Candidate generation, assignment, loss design, thresholds, and post-processing all contribute to behavior. Comparing two systems requires understanding which of these ingredients changed.

## What this contributed to driving perception

The region-based progression offered a practical path from general image recognition to locating road users. Learned features could handle visual variation more flexibly than a small set of hand-designed appearance rules, while shared computation made using those features more affordable.

These papers were developed and evaluated as general object detection methods. Their role in this series is to explain reusable mechanisms, not to suggest that their original benchmark results established complete driving capability. A road application still needs suitable categories, training data, timing, and evaluation.

Our truck also exposes the limits of the output. A two-dimensional box does not say how far away the truck is. A single frame does not establish its motion. A category list does not represent every possible obstacle. Each limitation motivates later changes in the representation and task.

The improvement from R-CNN to Faster R-CNN is best understood as changing how the same broad question is computed: which image regions contain objects, and what are their boxes? Other branches will change that organization more substantially.

## Check your understanding

Why did sharing a feature map save work? Overlapping candidate regions no longer required separate deep processing of largely repeated image pixels. Region-specific predictions could reuse one image representation.

Why can a correctly classified box still be a poor detection? Its boundaries may be inaccurate, it may duplicate another prediction, or it may fail the target annotation convention. Detection quality combines several requirements.

In the next chapter, we will examine approaches that predict detections directly over feature maps without a separate region-classification stage, and why small distant objects make speed difficult to optimize.

{% include perception-series-nav.html %}
