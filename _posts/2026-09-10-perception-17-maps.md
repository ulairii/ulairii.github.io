---
title: 'How Self-Driving Cars See — 17: Drawing lanes and intersections as a local map'
date: '2026-09-10'
permalink: /autonomous-driving-perception/17-maps/
excerpt: A green light is visible above our intersection. The car recognizes its color, but still needs to know which lane it controls. The road markings are partly worn, and one lane curves left while another continues straight. A collection of object boxes cannot describe these relationships.
tags:
- autonomous vehicles
- perception
- deep learning
- perception series
series_number: 17
read_time: false
---

{% include perception-series-nav.html %}

A green light is visible above our intersection. The car recognizes its color, but still needs to know which lane it controls. The road markings are partly worn, and one lane curves left while another continues straight. A collection of object boxes cannot describe these relationships.

Online mapping estimates local road structure from current and recent observations. The methodological change is from labeling scattered pixels to predicting geometric elements and, when required, their connections. This chapter separates a map's shape from its topology and explains why both can matter.

## A road mask does not specify a lane graph

Semantic segmentation can identify road pixels or lane markings. It gives a spatial label at each location. It does not automatically say which disconnected marking fragments belong to one boundary or which lane continues into which outgoing road.

A **polyline** represents a curve by an ordered sequence of points connected by straight segments. It is a compact way to describe a lane divider or road boundary. A polygon closes such a sequence to describe a region, such as a crossing area.

A **graph** adds relationships between elements. Nodes can represent lanes or other entities, and edges can represent connections or associations. The exact graph definition depends on the task, but it makes relationships explicit rather than leaving them implicit in a colored image.

Geometry and topology can be wrong independently. Two lane curves can be positioned accurately yet connected incorrectly. A route planner that follows the wrong connection can misunderstand the intersection despite a visually convincing map.

## Vector prediction changes the output space

A raster map stores values on a fixed grid. A vector map stores geometric elements, such as polylines, with a variable or bounded number of points. A model can predict those elements directly from sensor features instead of requiring a separate tracing algorithm after segmentation.

[MapTR, by Liao and colleagues, ICLR 2023](https://arxiv.org/abs/2208.14437), models map elements with structured queries and handles equivalent point orderings during learning. It provides a clear example of treating map output as a set of geometric objects.

The representation can be compact. A long boundary may require only a sequence of coordinates instead of a dense grid over the whole area. But the number and placement of points limit the curves it can describe accurately.

A sharp bend may need more samples than a straight segment. A fixed point budget creates an approximation tradeoff. Vector output also does not automatically include uncertainty or connectivity unless those quantities are explicitly predicted or derived.



<figure>
  <a href="{{ '/images/perception-series/17.svg' | relative_url }}" aria-label="Open diagram at full size" style="width:100%;"><img src="{{ '/images/perception-series/17.svg' | relative_url }}" alt="A broken raster lane marking becomes a connected polyline, then a graph shows which lane leads straight and which turns." width="720" height="460" style="height:auto;" loading="lazy"></a>
  <figcaption>Pixels, vector geometry, and topology represent different levels of road structure. A correct curve does not guarantee a correct connection. Original diagram for this series.</figcaption>
</figure>

## Equivalent point orderings complicate supervision

Suppose a boundary is represented by points A, B, and C. Traversing the same undirected boundary as C, B, and A can describe identical geometry. A closed polygon can also have several equivalent starting points.

If training compares coordinate lists only in one arbitrary order, it can penalize a geometrically correct prediction. The target representation therefore needs a policy for equivalent permutations, or a loss and matching procedure that accounts for them.

This is related to the set issues in PointNet and object detection, but the structure differs. Points within a curve are connected, so arbitrary shuffling usually changes its shape. Only certain reorderings preserve the intended geometry.

Some elements are directed. A lane centerline may carry a travel direction, so reversing its order is not necessarily equivalent. The method and dataset must define which symmetries are valid for each element type.

## A model must match predicted elements to labeled elements

The order of lanes in an annotation file need not correspond to the order of predicted queries. Training therefore needs assignment between predicted and target map elements. Costs can include class and geometric similarity.

After assignment, the model receives supervision for the selected element's coordinates and attributes. Unmatched predictions may be trained as absent elements. The exact procedure determines how duplicates and missing curves are treated.

Imagine two parallel lane dividers. They are close in space and have similar shape. A matching rule must avoid swapping their supervision inconsistently, especially when parts are occluded or truncated at the local map boundary.

This is one reason structured prediction requires more than attaching a coordinate output to a network. The representation, equivalences, assignment, and losses need to agree on what counts as the same map element.

## Topology asks how the pieces relate

For our intersection, we need to know which incoming lane connects to which outgoing lane and which signal applies to a movement. These are relational questions beyond the shape of each individual curve.

[OpenLane-V2, by Wang and colleagues, NeurIPS 2023](https://arxiv.org/abs/2304.10440), introduces a benchmark for road-scene topology, including lanes, traffic elements, and their relationships. It is useful because it makes clear that detecting the pieces and reasoning about their associations are different evaluation targets.

A network might predict pairwise connection scores between lane elements or associations between lanes and traffic signals. Those outputs can support a graph used by downstream reasoning. Their reliability depends on seeing enough local structure and on the annotation conventions.

Two curves crossing in a top view do not necessarily connect. They may represent an overpass and the road below. Height and road context can therefore matter even when the final visualization is two-dimensional.

## Online local maps and stored maps serve different roles

A stored map can provide prior structure over a large region. Localization places the vehicle within that reference. An online local map estimates the currently observed surroundings, potentially including changes or temporary arrangements.

These sources can complement each other. A stored map may help interpret a partially hidden intersection, while current observations reveal construction that was not present when the map was made. Neither should be assumed perfect without checking how it was obtained and updated.

A claim of “map-free” driving often means a particular detailed stored map is not required at inference. It does not necessarily mean the system uses no route, no positional information, or no internally estimated road structure. Read the input definition.

Similarly, predicting a local vector map is not the same as solving global localization. The local coordinates may be accurate relative to the car while the global position remains uncertain. Different tasks need different reference frames.

## Temporal consistency is valuable but can preserve mistakes

Road structure is mostly persistent over short intervals, so previous observations can help fill temporary gaps. A boundary hidden behind the truck may have been visible moments earlier. Aligning and maintaining map features can improve consistency.

The car's pose estimate affects that alignment. Small errors can make a boundary drift or duplicate across frames. A model that averages history without accounting for this can produce a smooth but misplaced line.

Change also occurs. Temporary barriers, a lane closure, or newly visible paint may contradict the stored local estimate. A useful system must update rather than merely preserve its previous output.

The meaning of “online” should therefore include the information available at the moment of prediction. Using future frames to create evaluation targets is different from supplying those frames to the model itself.

## Evaluate geometry and relationships separately

A geometric metric can compare predicted points or curves with labels, using distances under a defined matching procedure. Such a score can reveal localization quality but may miss whether the correct lane connections were predicted.

Topology evaluation checks relationships among elements. A system might perform well on one and poorly on the other. Both should be considered when the intended application relies on structured road understanding.

Range, visibility, and map boundaries also affect results. A truncated curve at the edge of the evaluation region is not necessarily a complete lane. Comparing methods requires consistent definitions of which elements and relationships count.

For the reader, a useful visual check is to trace one legal movement through the predicted structure. Can you follow the incoming lane, identify the relevant signal, and reach the correct outgoing lane? This does not replace quantitative evaluation, but exposes what a static colorful rendering can hide.

## Check your understanding

Why can two point lists describe the same boundary? Some curves permit reversed order or alternative starting points without changing their geometry. Training must account for the valid equivalences.

Does an accurate local map prove accurate global localization? No. The coordinate frame and task differ. Relative road structure can be useful even with uncertainty in the vehicle's global pose.

Next we return to object perception and ask whether the model needs to compute a dense feature grid over all surrounding space, or whether selected object-centered locations can carry enough information.

{% include perception-series-nav.html %}
