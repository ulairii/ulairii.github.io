---
title: 'How Self-Driving Cars See — 14: Letting a map query the images'
date: '2026-09-10'
permalink: /autonomous-driving-perception/14-bevformer/
excerpt: Lift-Splat-Shoot begins with image features and distributes them into space. Another strategy begins with a location in space and asks the images for relevant evidence. BEVFormer uses this second viewpoint to build a bird's-eye-view representation from multiple cameras and past information.
tags:
  - autonomous driving
series_number: 14
read_time: false
series: perception
---

{% include perception-series-nav.html %}

Lift-Splat-Shoot begins with image features and distributes them into space. Another strategy begins with a location in space and asks the images for relevant evidence. BEVFormer uses this second viewpoint to build a bird's-eye-view representation from multiple cameras and past information.

The word Transformer can make the method sound more mysterious than it is. We will separate three ingredients: a spatial query, geometric projection into the cameras, and learned aggregation of sampled features. Together they explain how the model decides where to gather information.

## A query is a request represented by numbers

In attention-based models, a **query** is a vector used to gather information from other vectors. Keys provide information used to assess relevance, and values provide the content to combine. The model learns transformations that make those comparisons useful for its training objective.

A simple attention operation computes scores between a query and several keys, normalizes the scores into weights, and forms a weighted combination of the values. The weights depend on the inputs and learned parameters. They are not direct measurements of physical visibility or guaranteed explanations of causation.

For example, suppose three value vectors describe candidate image regions. Weights of 0.2, 0.7, and 0.1 emphasize the second region. This is a way to select and mix evidence, not a hard rule that only one region is relevant.

[DETR, by Carion and colleagues, ECCV 2020](https://arxiv.org/abs/2005.12872), is an important visual-detection example of learned queries and set prediction. BEVFormer uses queries for a different spatial role: maintaining a grid of BEV features. Similar machinery can serve different representations.

## BEV queries are tied to spatial locations

[BEVFormer, by Li and colleagues, ECCV 2022](https://arxiv.org/abs/2203.17270), uses grid-shaped BEV queries with spatial cross-attention and temporal self-attention. The queries provide a persistent organization for information around the vehicle.

Each horizontal grid location is associated with reference points at selected heights. Those three-dimensional reference points can be projected into camera images using calibration. Cameras whose fields of view contain the projection can supply features for updating the query.

A BEV query is therefore not the same as an object hypothesis. It represents information associated with a spatial cell, whether or not an object center occupies that cell. A later task head interprets the completed representation.

This spatial anchoring gives the model a geometric starting point. Rather than comparing every cell with every image pixel indiscriminately, it gathers evidence near projections related to that cell. Learned sampling and weighting then refine how the evidence is used.



<figure>
  <a href="{{ '/images/perception-series/14.svg' | relative_url }}" aria-label="Open diagram at full size" style="width:100%;"><img src="{{ '/images/perception-series/14.svg' | relative_url }}" alt="A top-view query has reference points at several heights. Their projections identify image locations in two cameras, whose sampled features update the query." width="720" height="520" style="height:auto;" loading="lazy"></a>
  <figcaption>Geometry supplies reference locations; learned attention gathers nearby evidence. A projected point is not automatically visible through an occluding object. Original diagram for this series.</figcaption>
</figure>

## Deformable sampling limits the amount of attention

Full attention between a large BEV grid and every feature location from several cameras would be expensive. **Deformable attention** gathers a limited set of sampled features around reference locations, with learned offsets and weights.

This reduces the number of comparisons and lets the model adjust where it samples. If the most useful evidence lies slightly away from a nominal projection, a learned offset can reach it. The sampling still depends on a finite budget and the features available at those locations.

[Deformable DETR, by Zhu and colleagues, ICLR 2021](https://arxiv.org/abs/2010.04159), provides background for this attention family. BEVFormer adapts related ideas to multi-camera spatial and temporal representation building.

Offsets should not be described as perfect geometric correction. They may compensate for some uncertainty, but an incorrect calibration or an object hidden in every camera remains a problem. Sampling flexibility cannot guarantee access to evidence that was never observed.

## Several heights help connect a ground location to image evidence

A horizontal cell alone does not specify one camera pixel because objects can extend above the ground. Sampling reference heights gives several possible projections associated with the same horizontal location. Evidence from an elevated truck surface can therefore inform a BEV cell.

This does not make the output a full-resolution three-dimensional volume. Height-related evidence is collected into a feature vector indexed on a two-dimensional lattice. The representation can carry vertical information in channels while still compressing the explicit height axis.

The height choices and image feature resolution influence coverage. A thin structure between sampled locations may be difficult to capture. Learned offsets and contextual features can help, but the underlying sampling remains an architectural decision.

This is a useful comparison with LSS. LSS distributes image features over candidate depths and pools them. BEVFormer starts from spatial references and gathers image features. Both use geometry, learned features, and a finite representation of space.

## History can update what the current image does not show clearly

A previous BEV representation may contain useful evidence about the cyclist before the truck blocked part of the view. Temporal attention lets the current representation incorporate past information rather than rebuilding everything from the latest images alone.

The car has moved, so historical spatial features need alignment using self-motion information. A previous cell at one vehicle-relative coordinate may correspond to a different current coordinate. Without alignment, stationary structure can appear to move or blur.

Object motion remains after self-motion compensation. The cyclist may have advanced while the truck stayed still. Temporal aggregation therefore needs flexibility beyond a single rigid transform if it is to use moving-object evidence effectively.

History is not automatically trustworthy. A mistaken earlier estimate can persist through the memory. Temporal methods must be evaluated for recovery as well as stability: when new evidence contradicts the stored feature, does the system update appropriately?

## The BEV representation serves downstream heads

After spatial and temporal updates, a task head can predict boxes or map-related outputs from the BEV features. The attention layers construct a representation; the head and losses define what the system is trained to extract from it.

A feature grid can support several tasks, but shared computation alone does not guarantee that their needs align. Fine lane boundaries and object motion may require different details. Capacity, resolution, and supervision affect whether one representation supports both well.

This is why comparing architectures requires more than observing that both use a Transformer. The location of queries, positional information, sampling rules, temporal inputs, and output tasks are often more informative than the general network family.

For our intersection, the practical gain is a common spatial memory that can gather evidence from different cameras and times. Whether it is useful depends on geometric consistency and the quality of the predictions decoded from it.

## Attention does not remove the camera depth problem

A spatial reference can project to an image location even when the reference lies behind a visible surface. The camera observes the front surface along the ray, not every point that projects there. Geometric projection establishes a candidate correspondence, not proof of visibility.

The learned model must use appearance, context, multiple views, and supervision to interpret such ambiguity. It can still make depth and occlusion errors. A neat attention visualization should not be mistaken for a verified three-dimensional explanation of the scene.

The same caution applies to confidence. Strong attention to an image region indicates a computation performed by the model. It does not by itself establish that the resulting box position is accurate or that the region beyond it is empty.

A meaningful evaluation should inspect geometric errors, temporal behavior, camera coverage, and sensitivity to calibration alongside aggregate detection scores. These checks connect the internal mechanism to the actual task.

## What one query can actually receive

Consider a BEV cell beside the truck. One reference height projects onto a visible truck panel, while another projects onto background above it. The query gathers different features from those locations and learns how to combine them for its output task.

The operation has not directly measured a vertical column. It has collected image evidence associated with several geometric hypotheses. The task loss can encourage a useful representation, but deciding what occupies the cell still involves inference. Thinking through one query in this way keeps the method understandable without attributing a physical meaning to every attention weight or assuming that every projected reference point corresponds to a visible surface.

## Check your understanding

How does the information flow differ from LSS? LSS starts with image locations and sends weighted features into space. BEVFormer starts with spatial queries and gathers relevant image features. Both eventually build a BEV representation.

Why are several reference heights useful? A horizontal cell can contain evidence at different vertical positions, each projecting differently into a camera. The samples help gather that evidence before compression.

Can a query see through the truck because its reference point projects into the image? No. Projection does not establish visibility. Next we will combine different sensor types in a shared representation and examine when their evidence truly complements one another.

{% include perception-series-nav.html %}
