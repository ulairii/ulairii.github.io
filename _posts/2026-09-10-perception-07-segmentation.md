---
title: 'How Self-Driving Cars See — 07: Giving every pixel a meaning'
date: '2026-09-10'
permalink: /autonomous-driving-perception/07-segmentation/
excerpt: The detector has found the truck and cyclist. The car still needs to understand the road between them. A rectangle is a poor description of a curved lane boundary, the edge of a sidewalk, or an irregular patch of construction material.
tags:
- autonomous vehicles
- perception
- deep learning
- perception series
series_number: 7
read_time: false
---

{% include perception-series-nav.html %}

The detector has found the truck and cyclist. The car still needs to understand the road between them. A rectangle is a poor description of a curved lane boundary, the edge of a sidewalk, or an irregular patch of construction material.

Segmentation changes the output from a list of boxes to labels attached to spatial locations. This is a major shift in what the system is asked to preserve. Instead of only locating objects, the network must maintain enough detail to describe where one kind of surface ends and another begins.

## Semantic segmentation assigns a meaning to each pixel

In image **semantic segmentation**, each pixel receives a category such as road, sidewalk, vehicle, or pedestrian. The output is a grid aligned with the input image, though a network may compute it through intermediate resolutions.

The word “semantic” refers to the meaning of the category. It does not imply that the system understands every relationship in the scene. A road label says which category a pixel belongs to under the dataset's rules. It does not automatically encode whether the car is allowed to drive there.

Two nearby cars can receive the same category without being distinguished as separate objects. **Instance segmentation** adds that distinction, assigning pixels to individual object instances. The difference matters when tracking two pedestrians whose silhouettes overlap.

**Panoptic segmentation** combines instance distinctions for countable objects with semantic labels for regions such as road and sky. We do not need all three tasks to continue, but separating them prevents the word segmentation from hiding important differences in the output.

## Why an image classifier cannot simply paint a map

A classifier often compresses spatial information to decide whether an object is present somewhere. Segmentation needs a decision at many positions. A representation that has forgotten exactly where the evidence appeared cannot directly recover a sharp boundary.

[Fully Convolutional Networks, by Long, Shelhamer, and Darrell, CVPR 2015](https://arxiv.org/abs/1411.4038), adapted classification networks for dense prediction, using convolutional computation and upsampling to produce spatial outputs. Combining information from different depths helped connect coarse semantic evidence with finer spatial detail.

The key operation is not just enlarging a small image. Upsampling increases the number of output locations, but cannot by itself recreate details already discarded. Useful high-resolution evidence needs to survive through the architecture or be inferred from context.

Picture a narrow lane marking. After repeated downsampling, its signal may mix with adjacent road pixels. A decoder can use earlier features to recover its location more precisely. If the original measurement contains almost no visible marking, however, a crisp output may depend heavily on learned expectations.



<figure>
  <a href="{{ '/images/perception-series/07.svg' | relative_url }}" aria-label="Open diagram at full size" style="width:100%;"><img src="{{ '/images/perception-series/07.svg' | relative_url }}" alt="One scene is shown as a bounding box, semantic regions, and two separately labeled object instances." width="720" height="460" style="height:auto;" loading="lazy"></a>
  <figcaption>Boxes summarize extent; semantic masks label categories; instance masks distinguish individual objects. These outputs answer different questions. Original diagram for this series.</figcaption>
</figure>

## Context helps, but boundaries require detail

A small gray patch could be road, wall, or vehicle. Surrounding information helps determine its category. Larger receptive fields allow a prediction to depend on more context, but aggressive downsampling reduces spatial detail.

One way to increase the field of view without reducing resolution as much is **dilated convolution**, also called atrous convolution. It spaces the filter's sampling positions farther apart. Different spacing patterns inspect different extents of the feature map.

[DeepLab, by Chen and colleagues](https://arxiv.org/abs/1606.00915), studies atrous convolution and additional methods for improving semantic segmentation. It provides an important example of addressing context and boundary quality as separate concerns rather than relying solely on a deeper classifier.

A wider context is not always beneficial in every way. If the model learns that a region beside a road usually looks like a sidewalk, unusual construction can break that expectation. Context should help interpret evidence, while evaluation must check cases that depart from the common layout.

## Masks need their own training targets

A box annotation is relatively compact. Pixel-level annotation can require detailed tracing of boundaries and decisions about occlusion, reflections, transparent surfaces, and tiny regions. The model learns the annotation policy as well as the visual categories.

Training commonly penalizes incorrect class probabilities at labeled pixels. But pixels are not equally informative. A large area of easy sky can dominate the image, while the boundary of a distant pedestrian occupies very little space. Sampling and loss design influence which errors receive attention.

Some pixels may be marked as ignored because their category is uncertain or outside the evaluation policy. Ignored does not mean empty or harmless. It means the training or scoring procedure excludes that location according to a rule.

This distinction returns in occupancy learning, where some parts of space are never observed. Treating unknown locations as a particular class can teach a model a false certainty. Whenever a target grid appears, ask which cells were actually supervised and how their labels were produced.

## Lane markings need continuity and association

A lane marking can be segmented as a set of pixels. Driving often needs more: which pixels belong to the same boundary, how that boundary continues through a gap, and how adjacent lanes connect.

Suppose worn paint divides a line into three visible pieces. A correct semantic mask can label every visible piece while leaving their relationship unspecified. Another algorithm must connect them, or the model must predict a structured representation directly.

Traffic signals present a different association problem. A network may correctly segment a green lamp, yet the vehicle needs to know which lane or movement it controls. Appearance recognition and road interpretation remain separate responsibilities even when they share features.

For a general driving dataset with urban pixel labels, [Cityscapes, by Cordts and colleagues, CVPR 2016](https://arxiv.org/abs/1604.01685), is a useful source. Its annotation definitions illustrate why categories and instances must be specified carefully. A dataset's label set determines which distinctions a benchmark can measure.

## A mask is still an image-space description

A road mask follows perspective. Nearby pavement occupies many pixels; distant pavement occupies fewer. Equal-sized image regions do not correspond to equal-sized regions on the ground. A pixel count is therefore not a physical area measurement without geometry.

Likewise, a mask around the truck describes its visible image silhouette. It does not directly specify the truck's full three-dimensional volume or the space behind it. A perfectly outlined object can still have an uncertain distance.

This is why segmentation did not remove the need for three-dimensional perception. It increased spatial detail in the image representation. The next steps must connect that detail to depth and a shared physical coordinate frame.

The output can still be valuable before full reconstruction. It can identify road pixels, provide evidence for lane estimation, or support association between camera features and other sensors. Different representations often cooperate rather than replace one another.

## How segmentation is evaluated

For one category, intersection over union compares predicted and labeled pixels using the same overlap principle we used for boxes. Mean IoU averages category-level IoUs according to the benchmark's definition. It is useful, but compresses a spatially rich result into a small set of numbers.

A high score can coexist with a poorly localized thin boundary. A large road region contributes many pixels, while a small crossing feature may have a different operational importance. Category averages help expose some imbalance but still do not measure every consequence for driving.

Evaluation should therefore inspect examples by distance, object size, lighting, and boundary type. If the goal is lane following, continuity and geometric error may matter alongside pixel overlap. If the goal is detecting obstacles, instance distinctions and missed regions become important.

A colorful prediction image is an illustration, not an evaluation by itself. It can reveal systematic mistakes, but selected examples should be accompanied by a defined test protocol and measurements that match the intended task.

## A boundary example

Imagine a road region containing 10,000 labeled pixels and a narrow marking containing 100. Mislabeling 50 marking pixels changes very little of the whole image but removes half of that marking. A visual system used to follow the marking could be strongly affected.

This is why overall pixel accuracy can be misleading and why category-level metrics are useful. Even a category metric may not establish continuity: two masks can have similar overlap while one contains a gap at a critical bend. The output should be evaluated for the structure required by the application, with examples that expose the missing information. The numbers here are hypothetical and illustrate the difference between area and task importance.

## Check your understanding

Can a semantic mask tell two touching pedestrians apart? Not necessarily. Both may receive the same class label. Instance information is needed to represent them as separate objects.

Does a road mask establish a drivable path? No. Physical geometry, traffic rules, temporary restrictions, and other road users still matter. A class label is one source of evidence.

We have now expanded perception from naming objects to describing image regions. Next we will examine a more fundamental limitation: why correct image geometry can still leave the car uncertain about physical distance and collision risk.

{% include perception-series-nav.html %}
