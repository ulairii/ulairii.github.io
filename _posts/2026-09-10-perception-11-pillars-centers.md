---
title: 'How Self-Driving Cars See — 11: Turning a point cloud into a bird’s-eye view'
date: '2026-09-10'
permalink: /autonomous-driving-perception/11-pillars-centers/
excerpt: 'Most road users move across the ground plane, and many driving decisions depend strongly on horizontal position. That observation motivates a useful compromise: organize lidar points into vertical columns, encode each column, and process the result as a two-dimensional top view.'
tags:
  - autonomous driving
series_number: 11
read_time: false
series: perception
---

{% include perception-series-nav.html %}

Most road users move across the ground plane, and many driving decisions depend strongly on horizontal position. That observation motivates a useful compromise: organize lidar points into vertical columns, encode each column, and process the result as a two-dimensional top view.

This chapter connects two distinct ideas. PointPillars changes how points become features. CenterPoint changes how objects are represented at the detection output. Keeping those contributions separate makes it easier to understand later systems that combine similar encoders and heads in different ways.

## A pillar covers one horizontal cell through a height range

A voxel grid divides all three spatial axes. A **pillar** divides the horizontal plane but groups points across a selected vertical range into one column. The output lattice therefore has two spatial dimensions rather than three.

Points inside a pillar can still retain their height and relative coordinates as encoder inputs. Collapsing the lattice does not require deleting every height value before learning. A feature vector can encode useful vertical structure even though later convolution takes place on a horizontal grid.

However, the representation no longer maintains a separate spatial cell for every height interval. Two structures above one another must share the pillar's channel capacity. This can matter for overpasses, overhanging structures, and detailed clearance reasoning.

The useful question is therefore not “does BEV contain height?” in the abstract. Ask how height enters the representation, how it is compressed, and what outputs must recover from that compression. Different bird's-eye-view methods make different choices.

## PointPillars turns each column into a learned vector

[PointPillars, by Lang and colleagues, CVPR 2019](https://arxiv.org/abs/1812.05784), uses a PointNet-style encoder for points grouped into pillars, scatters the resulting features onto a two-dimensional grid, and applies a detection network.

“Scatter” here means placing each computed pillar feature at its corresponding horizontal grid location. The result is sometimes called a pseudo-image. Its channels contain learned point-cloud information, not ordinary RGB values.

A two-dimensional convolution can now combine neighboring pillar features. The same kinds of efficient grid operations used in image processing become available, but the grid is indexed in physical horizontal space rather than camera pixels.

For our intersection, a nearby truck and a distant truck of the same physical dimensions can occupy similar numbers of grid cells, assuming both lie within the selected region. This differs from an image, where perspective changes their apparent size with distance.



<figure>
  <a href="{{ '/images/perception-series/11.svg' | relative_url }}" aria-label="Open diagram at full size" style="width:100%;"><img src="{{ '/images/perception-series/11.svg' | relative_url }}" alt="Points at several heights enter one pillar feature. A top-view heatmap then marks an object center and predicts dimensions, height, and heading." width="720" height="460" style="height:auto;" loading="lazy"></a>
  <figcaption>The pillar encoder organizes measurements; the center head specifies detection outputs. These are separate choices. Original diagram for this series.</figcaption>
</figure>

## Bird's-eye view is a coordinate choice, not a sensor

A **bird's-eye view**, or BEV, usually describes a representation indexed over the horizontal plane around the car. It can be built from lidar, cameras, radar, or fused measurements. The name does not say how its features were obtained.

BEV is useful because physical relationships are easier to compare in a shared metric plane. Lane direction, object footprints, and distances to a planned path can be expressed without comparing unrelated camera pixels. The representation also gives multiple sensors a common place to contribute information.

But a BEV feature map is not necessarily a human-readable map. Each cell can hold dozens of learned channels. A later head may decode object boxes, road masks, or other quantities from them. Displaying one output should not be confused with displaying the entire internal representation.

Grid limits still apply. Resolution determines how finely positions are indexed, and the chosen range determines coverage. Fine localization can use predicted offsets within cells, but very coarse features can still merge evidence from nearby objects.

## Center-based detection chooses a different output reference

Many detectors predict adjustments to reference boxes. [CenterPoint, by Yin, Zhou, and Krähenbühl, CVPR 2021](https://arxiv.org/abs/2006.11275), represents objects through centers and predicts additional properties such as size, orientation, and velocity. It also studies refinement and tracking within that framework.

A center heatmap gives a score at each top-view location for whether an object center lies nearby. Additional outputs describe the object's geometry. A small local offset can correct the difference between the true center and the discrete grid location.

This avoids enumerating many reference-box orientations as the starting point for detection. It does not mean orientation is ignored. Heading still has to be estimated accurately because a long object's footprint changes as it turns.

CenterPoint is not synonymous with PointPillars. A center-based head can receive features from different encoders, including voxel-based ones. A pillar encoder can also feed a different detection head. The two ideas operate at different stages.

## A center can be predicted where there is no return

Lidar measures visible surfaces. The physical center of a vehicle may lie inside its body, with no direct return at that location. A center heatmap therefore represents an inferred object property, not a map of measured lidar hits.

Convolutional features combine evidence from surrounding surfaces to support that inference. The network can learn that a particular spatial arrangement is consistent with an object whose center lies between the visible parts.

This distinction helps interpret visualization. A bright center prediction in an apparently empty cell is not necessarily an error. The target is the object's reference position, while the sensor observes surfaces. Conversely, a surface point is not automatically a valid object center.

Occlusion makes the inference harder. If only a small piece of the truck is visible, estimating its full dimensions and center depends more strongly on learned shape patterns. That uncertainty should not disappear merely because the output uses a compact point representation.

## Orientation needs a sensible numerical representation

Angles wrap around. A heading just below 360 degrees is physically close to one just above zero, even though direct subtraction gives a large numerical difference. Training losses need to respect that periodicity or use a representation that handles it.

One common approach predicts sine and cosine components of the angle. Another combines discrete direction information with a continuous adjustment. The exact choice is method-specific, but the underlying issue comes from geometry rather than a network's expressive power.

Object symmetry can introduce additional ambiguity. A nearly symmetric visible shape may not reveal which end is the front. Motion and appearance can provide evidence beyond the static point arrangement. Different output properties can therefore benefit from different sensor information.

The same lesson applies to velocity. If it is predicted from a single sparse observation, it may rely heavily on learned correlations. Multiple aligned observations provide more direct evidence of movement, though they require careful timing and association.

## Efficiency changes the feasible design space

Moving much computation to a two-dimensional lattice can make a system easier to run within a limited budget. That savings can potentially be spent on a wider range, finer horizontal resolution, temporal input, or other tasks.

There is no guarantee that one simplification is best everywhere. A method that needs detailed vertical geometry may benefit from retaining a three-dimensional representation longer. A deployment device may also support some operations more efficiently than others.

The comparison should therefore include output requirements. Detecting road vehicles as boxes and estimating free clearance beneath an overhead structure are not identical tasks. A representation well suited to one may need additional features or heads for the other.

Nor should historical runtime numbers be treated as universal current performance. Different hardware, precision, input settings, and software implementations change the result. The methodological lesson is how the computation is organized and what information it compresses.

## Recovering a position inside a cell

Suppose a BEV grid uses cells 0.5 meters wide and a true center lies 0.1 meters from a selected cell reference. A head that predicts only the cell index must quantize the center. A head that also predicts the local offset can recover a finer coordinate.

That refinement does not mean the original feature resolution no longer matters. If two small objects produce indistinguishable features in one coarse neighborhood, an offset head may still have trouble separating them. Subcell regression improves the output parameterization; it does not restore every detail discarded by the encoder. Keep the sampling resolution and the numerical precision of the final coordinates separate when interpreting a result.

## Check your understanding

Does pillarization remove all height information? No. Heights can enter the learned pillar features. It removes a separate height axis from the spatial grid used by later two-dimensional operations.

Does center-based detection require a lidar return at the object center? No. The center is inferred from surrounding evidence and may lie inside the object.

We now have a metric top-view representation built from measured points. Next we return to cameras and ask how similar three-dimensional outputs can be estimated when depth is itself uncertain.

{% include perception-series-nav.html %}
