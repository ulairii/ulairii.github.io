---
title: 'How Self-Driving Cars See — 19: What if the obstacle has no familiar name?'
date: '2026-09-10'
permalink: /autonomous-driving-perception/19-occupancy/
excerpt: A piece of construction material falls near the crossing. It is low, irregular, and unlike the categories in the detector's label list. The car needs to avoid it even if the software cannot give it a familiar name.
tags:
- autonomous vehicles
- perception
- deep learning
- perception series
series_number: 19
read_time: false
---

{% include perception-series-nav.html %}

A piece of construction material falls near the crossing. It is low, irregular, and unlike the categories in the detector's label list. The car needs to avoid it even if the software cannot give it a familiar name.

Occupancy perception describes space more directly. It asks whether locations contain matter, and sometimes what semantic category that matter belongs to. This broadens the output beyond a list of known object boxes, but raises difficult questions about resolution, visibility, and how training labels are obtained.

## Occupancy and semantic occupancy are different outputs

A geometric occupancy representation distinguishes occupied from unoccupied locations under a specified spatial discretization. **Semantic occupancy** additionally assigns categories to occupied regions, such as vehicle, road, or vegetation.

That extra semantic head can still have a fixed vocabulary. Occupancy does not magically create names for every object. Its advantage is that geometric obstruction can in principle be represented without fitting the scene entirely into a selected collection of object boxes.

We also need an epistemic distinction: a location may be unobserved. **Unknown** is not always an explicit output class in a particular benchmark, but it must be considered when interpreting labels and predictions. Some datasets handle it through visibility masks or ignored cells.

A model can infer occupancy in hidden regions using learned context. That is an estimate, not a direct measurement. The output format should not encourage us to forget where evidence is absent.

## A lidar ray gives more than one surface point

A detected return provides evidence of a reflecting surface near a measured distance. Under the sensor model and validity assumptions, the path before that return also provides evidence about free space along the beam. The region beyond the surface is generally not observed by that ray.

This creates a useful three-part picture: observed path, measured surface, and hidden continuation. A sparse point cloud stores the returns, but may not explicitly store all the free-space evidence along the beams. An occupancy labeling pipeline can use ray information to recover some of it.

The details matter for transparent surfaces, multiple returns, noise, and sensor limitations. Ray reasoning is a measurement model with assumptions, not a universal claim that every location before any return is perfectly known.

The truck makes the distinction easy to see. Its front-facing surface can be well measured while the space behind it remains hidden. A network predicting that hidden space is using prior knowledge and other observations, not seeing through the truck.



<figure>
  <a href="{{ '/images/perception-series/19.svg' | relative_url }}" aria-label="Open diagram at full size" style="width:100%;"><img src="{{ '/images/perception-series/19.svg' | relative_url }}" alt="A ray crosses green free-space cells, reaches an orange occupied surface cell, then enters purple unknown cells behind the surface." width="720" height="430" style="height:auto;" loading="lazy"></a>
  <figcaption>Free, occupied, and unknown describe different evidence states. Particular benchmarks may encode unknown through masks rather than a third predicted class. Original diagram for this series.</figcaption>
</figure>

## Dense 3D output demands a larger representation

A BEV grid indexes horizontal position. A three-dimensional occupancy grid also indexes height. This can distinguish an overhead structure from an obstacle at road level, provided the resolution and training data preserve the relevant geometry.

The memory growth from Chapter 10 returns. Fine cells over a large volume require many outputs and intermediate features. A model may use a compressed representation, sparse computation, multiple scales, or a decoder that reconstructs detailed occupancy from coarser features.

[SurroundOcc, by Wei and colleagues, ICCV 2023](https://arxiv.org/abs/2303.09551), predicts three-dimensional occupancy from multiple cameras using image-to-volume feature aggregation and three-dimensional processing. It is one example of making spatially detailed output a central training objective.

The decoder still estimates geometry from available observations. More output cells create a more expressive answer format, but do not create more sensor evidence. A fine-looking surface can be inferred incorrectly when depth or visibility is ambiguous.

## Where do dense labels come from?

Manually labeling every small cell in a three-dimensional scene is difficult. Many benchmarks build targets from lidar, annotations, multiple observations, and reconstruction procedures. The resulting labels can be much denser than any single sensor frame.

[Occ3D, by Tian and colleagues, NeurIPS 2023](https://arxiv.org/abs/2304.14365), introduces occupancy benchmarks and a visibility-aware label-generation pipeline. It makes supervision a major part of the problem rather than treating a dense target grid as automatically available.

Combining observations across time can reveal surfaces hidden in the current frame. But dynamic objects must be handled separately or aligned appropriately. Otherwise a moving vehicle can leave a trail of occupied cells in the reconstructed target.

Reconstruction also introduces assumptions when filling gaps. A mesh completion procedure can infer surfaces between measured points. Those inferred labels are useful training material, but their uncertainty and failure modes should be understood when interpreting benchmark scores.

## Training labels can know more than inference inputs

An offline label pipeline may use future observations to reconstruct what was behind the truck. A causal perception model can be trained to predict that target from current and past inputs. This is a legitimate learning setup when clearly defined.

It becomes misleading if future measurements are accidentally included in the model input or preprocessing while the result is described as online perception. Label construction and inference information must be audited separately.

The task's wording also matters. Predicting the current completed scene differs from predicting future occupancy. The first estimates present geometry, perhaps beyond direct visibility. The second estimates how geometry or objects will evolve over time.

Both can be called “prediction” in machine learning papers. Reading the timestamp of the target is therefore more reliable than inferring the task from that word alone. Chapter 20 will separate these temporal meanings.

## Unknown obstacles remain a generalization problem

A geometric occupancy model has an output format that can describe an unfamiliar shape. That does not guarantee it will detect every unfamiliar obstacle. It still learns from particular data and can miss small, distant, reflective, or weakly observed structures.

Cell size can erase thin geometry. A low obstacle may occupy only part of a cell, and the labeling rule determines whether that cell is considered occupied. Downstream planning needs to understand the discretization and any conservative margins applied.

Semantic labels can introduce additional failure modes. A surface might be geometrically detected but assigned the wrong class. Conversely, a plausible class prediction may accompany an incorrect occupied extent. Geometry and semantics should be evaluated separately where possible.

The useful methodological claim is modest: the representation does not require every obstacle to be approximated by a known-category box. Actual reliability still needs empirical evidence over the intended conditions.

## Occupancy is not the same as drivability

An empty sidewalk is not automatically an appropriate driving region. A low road surface is occupied matter, yet the car is expected to travel above it. Drivability depends on vehicle geometry, road rules, slope, clearance, and the intended motion.

A planner must therefore interpret occupancy relative to the vehicle's shape and trajectory. Checking only a center point can miss collisions with the vehicle body. Checking every occupied road cell without considering height would incorrectly reject normal driving.

Temporal behavior matters too. A cell currently empty may soon contain the cyclist. Static occupancy does not replace motion forecasting. The representation supplies one part of the information required for a decision.

This is why object tracks, maps, and occupancy can coexist. Tracks describe entities and motion; maps describe road structure; occupancy describes spatial extent. Each makes different questions easier to answer.

## How to read an occupancy result

Check the spatial range, cell resolution, input sensors, number of frames, and visibility mask. Then inspect the target-generation procedure. Two occupancy scores may refer to different amounts of observed and inferred space.

A common metric is IoU over occupied cells or semantic categories, but its interpretation depends on which cells count. A model evaluated only on visible cells solves a different problem from one evaluated across hidden regions as well.

Selected three-dimensional renderings can reveal shape quality, but they can also hide empty-space mistakes or uncertain regions. A useful visualization includes the sensor viewpoint and indicates which parts were observed.

## Resolution changes the question being labeled

Imagine a narrow pole crossing a voxel near its edge. Under an any-surface rule, a small intersection can make the whole cell occupied. Under a different sampling or labeling rule, the pole might be missed. The resulting occupied cells describe the discretized target, not the exact continuous surface.

A planner can account for grid resolution when checking vehicle clearance, but it must know what the cells mean. Refining the grid can improve shape detail while increasing memory and annotation demands. This is why occupancy results need both the spatial resolution and the label-generation definition. Without them, an apparently thick or thin obstacle in a rendering is difficult to interpret.

## Check your understanding

Does occupancy remove the need to understand uncertainty? No. The distinction between unoccupied and unobserved becomes especially important when every spatial cell receives an output.

Can an unfamiliar object be represented without naming it? Geometric occupancy can describe its occupied extent in principle. Whether the model detects it correctly remains a question of evidence, resolution, and generalization.

Next we will add time to spatial occupancy and distinguish current reconstruction, measured motion, and possible future scenes.

{% include perception-series-nav.html %}
