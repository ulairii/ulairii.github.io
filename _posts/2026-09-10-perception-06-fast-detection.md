---
title: 'How Self-Driving Cars See — 06: Detecting objects fast enough to drive'
date: '2026-09-10'
permalink: /autonomous-driving-perception/06-fast-detection/
excerpt: The pedestrian has begun moving toward the crossing. An accurate detection returned too late describes where the person used to be. This makes speed a practical requirement, but reducing computation can remove exactly the small details needed to detect a distant road user.
tags:
  - autonomous driving
series_number: 6
read_time: false
series: perception
---

{% include perception-series-nav.html %}

The pedestrian has begun moving toward the crossing. An accurate detection returned too late describes where the person used to be. This makes speed a practical requirement, but reducing computation can remove exactly the small details needed to detect a distant road user.

The next methodological change reorganized detection around predictions made directly from feature maps. We will use the original YOLO and SSD as historical examples, then examine why dense prediction introduces its own training and evaluation problems.

## What one-stage detection changes

In the two-stage design from Chapter 5, one stage proposes regions and another classifies and refines them. A **one-stage detector** predicts categories and geometry over image features without a separate region-classification stage. It still contains many layers and can use several output branches.

The [original YOLO paper by Redmon and colleagues, CVPR 2016](https://arxiv.org/abs/1506.02640), framed detection as a unified prediction of boxes and category information from an image. Its grid-based output was one specific design. Later methods sharing the YOLO name changed many details, so we should not attribute every later feature to the original paper.

Think of the image representation as carrying evidence at different locations. A prediction head reads that evidence and reports candidate objects. Different methods choose different box encodings, reference shapes, assignment rules, and ways to handle object scale.

“One-stage” is therefore an architectural category rather than a complete specification. It also does not establish a fixed speed ranking: input resolution, network size, hardware, and post-processing can make two implementations behave very differently.

## Object size determines where detail is available

Our truck occupies a large part of the image. The distant cyclist might occupy only a small patch. If a feature map is much smaller than the original image, the cyclist may influence just one or two feature locations, mixed with background.

Higher-resolution features preserve finer spatial detail, but cost more memory and computation. Lower-resolution features summarize larger image regions and may contain stronger context. Combining them helps a detector handle objects at different scales.

[SSD, by Liu and colleagues, ECCV 2016](https://arxiv.org/abs/1512.02325), makes predictions from multiple feature maps and uses default boxes with different scales and aspect ratios. Its output adjusts those boxes and assigns category scores. This is a concrete example of using several representation scales within one-stage detection.

The deeper lesson is that one output resolution rarely serves every object equally well. A large vehicle and a tiny traffic light pose different sampling problems even when the category classifier is strong. Small-object performance depends on whether enough useful evidence survives to reach the head.



<figure>
  <a href="{{ '/images/perception-series/06.svg' | relative_url }}" aria-label="Open diagram at full size" style="width:100%;"><img src="{{ '/images/perception-series/06.svg' | relative_url }}" alt="A large truck is represented on a coarse grid while a small cyclist needs a finer grid. Predictions from both scales contribute boxes." width="720" height="460" style="height:auto;" loading="lazy"></a>
  <figcaption>Fine and coarse feature maps serve different object sizes. The grids illustrate sampling, not a particular network’s exact dimensions. Original diagram for this series.</figcaption>
</figure>

## Dense prediction creates many easy background examples

If a detector makes predictions at many locations and scales, most candidates do not correspond to an object. Our road image contains large areas of sky, pavement, walls, and other background. Those locations can vastly outnumber the positive training examples.

A naive sum of losses can let easy negative examples dominate the update. The model may spend much of its training effort improving predictions that were already nearly correct while receiving relatively little useful signal from difficult foreground objects.

**Focal loss** changes how classification errors are weighted. In [the RetinaNet paper by Lin and colleagues, ICCV 2017](https://arxiv.org/abs/1708.02002), it reduces the influence of well-classified examples so training can emphasize harder cases. This addresses a particular imbalance in dense detection; it does not automatically solve every form of dataset imbalance.

For example, a rare type of bicycle may still be absent from training. Reweighting existing examples cannot create observations of it. Background imbalance, class frequency, and unfamiliar appearances are related but distinct problems requiring different evidence and interventions.

## How a prediction becomes responsible for an object

A training algorithm must decide which candidate predicts the cyclist. In anchor-based designs, overlap or other geometric rules can connect reference boxes to annotations. Other detectors use locations near an object center, distances to boundaries, or learned matching procedures.

This assignment influences the learning problem. If no suitable candidate is treated as positive for a very small object, its features may never receive the intended training signal. If too many ambiguous candidates are assigned, duplicates and conflicting targets can become harder to manage.

Imagine a cyclist next to the truck edge. At a coarse location, the receptive field contains evidence from both. The head must use its features and target rules to produce the appropriate class and geometry. Merely adding another category output does not guarantee that the features distinguish the two instances.

This is why detector comparisons should report more than a backbone name. An improvement might come from assignment, loss weighting, feature resolution, augmentation, or the prediction head. Each changes what information is available or how training rewards its use.

## Removing duplicates still takes work

Dense predictions often produce several boxes around the same object. Many one-stage detectors use non-maximum suppression, introduced in Chapter 5, to reduce them. Candidate filtering and suppression are part of the complete runtime.

The number of candidates can change with image resolution and implementation settings. Keeping more candidates may preserve difficult objects but increase later work. Raising a score threshold can reduce workload while removing low-confidence true detections.

A particularly crowded scene can behave differently from an empty highway. Average processing time alone can conceal the cases where post-processing becomes expensive. The system needs to be evaluated over the kinds of scenes in which it will operate.

Suppression can also interact with small objects. A cyclist partially overlapping a vehicle in the image is still a separate road user. Whether suppression compares candidates within one class or across classes changes the risk of losing such a detection.

## Speed needs a complete measurement boundary

A paper may report network inference time while an application experiences additional costs: image decoding, resizing, sensor synchronization, data transfers, and result processing. A fair comparison defines which steps are included.

**Latency** is the time an individual input takes to produce its result. **Throughput** is how many inputs are processed per unit time. Batching several images can improve throughput without giving each image a lower latency. These quantities should not be substituted for one another.

The hardware also matters. An operation that performs well on one GPU may be poorly supported on a smaller deployment device. Memory movement can become as important as arithmetic. Counting parameters or mathematical operations alone does not fully describe runtime.

For our intersection, the relevant question is how old the cyclist estimate is when the planner uses it. That age includes sensor collection and all processing delays. A faster detector helps only within the context of that complete timing path.

## What did this branch change in the larger history?

One-stage methods showed that object detection could be organized as direct predictions over shared features, with computation concentrated in a unified network. Multi-scale features and better training losses then addressed weaknesses exposed by that organization.

This did not make region-based methods disappear. Different settings favor different choices, and later detectors borrow ideas across categories. The historical story is a growing collection of ways to allocate computation and supervision, not a clean sequence of winners.

For driving, both families still return limited descriptions. Even a fast, accurate image detector does not directly produce a metric map of the road. It may also describe a lane or a large irregular obstacle poorly with rectangles. We will soon need different output representations.

Before leaving detection, notice the recurring design question: where should computation be spent? On candidate regions, every grid location, several image scales, or selected queries? That same question reappears in three-dimensional and sparse perception.

## A threshold example

Suppose a detector produces ten true cyclist detections and ten false alarms at a low score threshold. Raising the threshold removes eight false alarms but also removes three real cyclists. Precision improves because a larger share of the remaining predictions is correct; recall falls because fewer of the real cyclists are retained. Those two effects should be visible in the evaluation, rather than hidden behind the selected operating point.

The appropriate threshold depends on how the output is used. A downstream tracker may recover some weak detections using history, while a system that discards them immediately loses that opportunity. This is an illustrative counting example, not a result from a named detector. It shows why confidence filtering is a decision about information retention as well as runtime.

## Check your understanding

Why can shrinking an image hurt a distant cyclist more than a nearby truck? The cyclist starts with fewer pixels. Reducing resolution can erase its distinguishing structure before the model has a chance to recognize it.

Does one-stage mean there is no post-processing? No. Many such detectors still filter and suppress predicted boxes. The complete pipeline matters when measuring speed.

Can a high average frame rate prove a detector is suitable for driving? No. Accuracy in relevant conditions, latency distribution, sensor timing, and integration all need attention. Next, we will replace boxes with pixel-level descriptions and see what that gains.

{% include perception-series-nav.html %}
