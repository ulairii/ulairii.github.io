---
title: '01: Image perception: R-CNN, YOLO, and FCN'
date: '2026-09-10'
permalink: /autonomous-driving-perception/01-image-detection/
excerpt: 'Deep learning first changed autonomous-driving perception by replacing hand-designed image features with features
  learned from data. The useful history is not a list of bigger networks. It is a sequence of changes to where computation
  happens and what a network predicts: image categories, proposed regions, dense boxes, and pixel labels.'
tags:
- autonomous driving
series: perception
series_number: 1
read_time: false
reading_minutes: 6
redirect_from:
- /autonomous-driving-perception/01-intersection/
- /autonomous-driving-perception/03-learning/
- /autonomous-driving-perception/05-region-detection/
- /autonomous-driving-perception/06-fast-detection/
- /autonomous-driving-perception/07-segmentation/
---

{% include perception-series-nav.html %}

Deep learning first changed autonomous-driving perception by replacing hand-designed image features with features learned from data. The useful history is not a list of bigger networks. It is a sequence of changes to **where computation happens and what a network predicts**: image categories, proposed regions, dense boxes, and pixel labels.

[AlexNet — Krizhevsky, Sutskever, and Hinton, NeurIPS 2012](https://papers.nips.cc/paper/4824-imagenet-classification-with-deep-convolutional-neural-networks) helped establish the strength of learned convolutional features for image classification. The detection papers below adapted that success to locating objects rather than assigning one label to a whole image.

A few terms are enough to start. A *feature map* is a grid of learned descriptors extracted from an image. A *backbone* produces that grid. A *head* converts it into a task output, such as a vehicle box or a road label. Training adjusts these components to reduce an error measured against annotations.

## R-CNN to Faster R-CNN: share the expensive work

[R-CNN — Girshick et al., CVPR 2014](https://arxiv.org/abs/1311.2524) combined an external region-proposal algorithm with a convolutional network. Each proposed image crop was processed separately, then classified. Its methodological contribution was to make learned visual features useful for object localization, but overlapping crops repeated much of the same computation.

[Fast R-CNN — Girshick, ICCV 2015](https://arxiv.org/abs/1504.08083) moved the backbone before the region step. Run the network once over the image, extract a fixed-size feature for each proposal, and predict its category and box adjustment. The proposals still came from a separate algorithm; feature extraction became shared.

[Faster R-CNN — Ren et al., NeurIPS 2015](https://arxiv.org/abs/1506.01497) then learned proposals with a region proposal network on the shared feature map. A first stage suggests promising regions; a second classifies and refines them. This is the meaning of a **two-stage detector**, not two completely independent image networks.

The practical lesson is broader than detection: moving a repeated operation onto a shared representation can matter as much as changing the backbone.

<figure>
  <a href="{{ '/images/driving-papers/01.svg' | relative_url }}" style="width:100%;" aria-label="Open architecture diagram at full size"><img src="{{ '/images/driving-papers/01.svg' | relative_url }}" alt="Image perception: R-CNN, YOLO, and FCN: a comparison of the information passed between the methods' main stages." width="760" height="460" style="height:auto;" loading="lazy"></a>
  <figcaption>Original schematic of the methods discussed here; simplified information flow, not a reproduction of a paper's complete architecture.</figcaption>
</figure>

## YOLO and RetinaNet: predict densely, then fix the training imbalance

[YOLO — Redmon et al., CVPR 2016](https://arxiv.org/abs/1506.02640) treated detection as a single network prediction from the image. Its original grid-based design directly produced boxes and class information. This reduced the machinery around region proposals and made the speed–localization tradeoff central to detector design. Modern YOLO variants differ substantially; the original paper should not be used to explain every later version.

Dense prediction creates a training problem: most candidate locations are background. A loss can become dominated by already-easy negatives. [RetinaNet — Lin et al., ICCV 2017](https://arxiv.org/abs/1708.02002) addressed this with focal loss, which reduces the contribution of confidently classified examples. Its feature pyramid also supports detection at several scales.

For a car, those scales are operationally meaningful. A nearby bus occupies many pixels; a distant pedestrian may occupy very few. Increasing input resolution, preserving fine features, and choosing the training loss are different ways of addressing that difficulty, with different costs.

## FCN: road layout needs more than boxes

[Fully Convolutional Networks — Long et al., CVPR 2015](https://arxiv.org/abs/1411.4038) adapted classification networks to dense semantic prediction. Coarse, high-level features are upsampled and combined with finer information so that the output assigns a class to each pixel.

A box answers “where is this object?” Semantic segmentation answers “which image regions are road, sidewalk, or vehicle?” It does not automatically separate two adjacent vehicles into different instances, recover their distance, or identify a drivable route.

This distinction explains why detection and segmentation developed alongside each other. They offer different interfaces to the rest of the driving system.

| Design | Main output | Important design choice |
|---|---|---|
| Faster R-CNN | Object boxes and classes | Refine a selected set of regions |
| YOLO / RetinaNet | Object boxes and classes | Predict over many image locations |
| FCN | A class at each pixel | Preserve spatial detail during upsampling |

## The limitation that pushed perception into 3D

These outputs are tied to the camera image. A box can be accurate in pixels while the object's distance remains uncertain. The planner needs quantities in physical space: position, size, heading, motion, and the road around them.

A calibrated camera maps a 3D point to an image location, but one image location corresponds to a ray through space. Depth chooses a point along that ray. Learning a better image detector does not remove this ambiguity.

That is the transition to the next papers: retain learned features, but build representations whose coordinates match the world in which the vehicle must act. Image detection remains useful inside these systems; it is not a discarded historical stage.

{% include perception-series-nav.html %}
