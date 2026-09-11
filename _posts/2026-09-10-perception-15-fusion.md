---
title: 'How Self-Driving Cars See — 15: Combining cameras, lidar, and radar'
date: '2026-09-10'
permalink: /autonomous-driving-perception/15-fusion/
excerpt: The camera recognizes the cyclist's appearance, while lidar samples surfaces near the estimated position. Radar may add evidence about relative motion. Combining them sounds straightforward until their coordinates, timestamps, uncertainties, and meanings disagree.
tags:
  - autonomous driving
series_number: 15
read_time: false
series: perception
---

{% include perception-series-nav.html %}

The camera recognizes the cyclist's appearance, while lidar samples surfaces near the estimated position. Radar may add evidence about relative motion. Combining them sounds straightforward until their coordinates, timestamps, uncertainties, and meanings disagree.

Sensor fusion is the problem of turning those different observations into a useful joint estimate. The key design choice is where the information meets: before feature extraction, inside the learned representation, or after separate predictions have already been made.

## Late fusion combines decisions

In **late fusion**, separate systems produce outputs such as detections or tracks, then another stage associates and combines them. A camera detector might report a pedestrian candidate while a lidar detector reports a nearby three-dimensional box.

The fusion stage needs to decide whether they refer to the same object. It may use projection, spatial distance, class compatibility, time, and uncertainty. Simply averaging coordinates is inappropriate when the coordinates describe different frames or different reference points.

This organization allows relatively independent components, but information has already been compressed. A camera feature suggesting an unusual obstacle may have been discarded if the camera detector did not emit a box. The fusion stage cannot recover evidence it never receives.

Late fusion also needs a policy for disagreement. One sensor may miss an object because of limited visibility, while another produces a false positive. Which output should be trusted depends on the measurement conditions and model reliability, not merely on which score is numerically larger.

## Earlier fusion combines richer measurements or features

At an earlier stage, a model can combine sensor measurements or attach image-derived features to lidar points. Richer information remains available, but the representations need careful alignment before a network can use them together.

[PointPainting, by Vora and colleagues, CVPR 2020](https://arxiv.org/abs/1911.10150), projects lidar points into image segmentation outputs and appends semantic scores to the points. A point-cloud detector then receives both geometry and image-derived category evidence.

The correspondence is geometrically understandable: a lidar point maps to an image location through calibration. But the projected image feature must refer to the same visible surface. Time differences, occlusion, and projection error can attach the wrong semantics to a point.

The method also samples camera information where lidar points exist. This can be useful for object detection, but it does not preserve every image location. A distant feature with no lidar return may have no point to which its evidence can be attached.



<figure>
  <a href="{{ '/images/perception-series/15.svg' | relative_url }}" aria-label="Open diagram at full size" style="width:100%;"><img src="{{ '/images/perception-series/15.svg' | relative_url }}" alt="Camera features and lidar features enter separate encoders, become aligned BEV grids, and join before the prediction head. A second small path shows independent detections joined afterward." width="720" height="535" style="height:auto;" loading="lazy"></a>
  <figcaption>Feature fusion retains information before final decisions. Late fusion combines already compressed outputs. Both require correspondence and timing. Original diagram for this series.</figcaption>
</figure>

## BEV provides a common place for features to meet

Camera features can be lifted or gathered into BEV, while lidar features can be encoded through voxels or pillars. If both grids use the same physical frame, range, and resolution, corresponding locations can be combined by a learned fusion module.

[BEVFusion, by Liu and colleagues, ICRA 2023](https://arxiv.org/abs/2205.13542), unifies camera and lidar features in BEV and supports several perception tasks. This chapter refers to that paper specifically, since more than one work has used the BEVFusion name.

The spatial interface is useful because each modality can use an encoder suited to its measurements before the features meet. Image appearance need not first be reduced to a box list, and lidar geometry need not be forced into an RGB-like input.

A shared lattice does not mean the features have identical semantics. A camera cell may contain evidence spread by uncertain depth; a lidar cell may summarize measured returns. The fusion network has to learn how those different signals should influence the output.

## Alignment errors create plausible but wrong combinations

Suppose a pedestrian stands next to a truck. A small projection shift can attach the pedestrian's image features to truck points, or move camera BEV evidence into the neighboring cell. Both sensors may be individually useful while their combined representation becomes inconsistent.

A timestamp difference creates a related problem. If the cyclist moves between the camera exposure and lidar observation, the two features describe different positions. Self-motion compensation aligns stationary surroundings, but moving objects may still require additional treatment.

Resolution differences also matter. One feature grid may be coarser than another. Resampling makes their array sizes compatible, but interpolation does not restore detail lost in the coarser representation. Compatibility of shapes is not the same as equality of information.

These are concrete reasons to test calibration perturbations, delays, and partial sensor coverage. They reveal whether a fusion method uses measurements consistently rather than merely benefiting from additional training inputs under ideal conditions.

## Radar introduces motion evidence and different ambiguity

Radar can contribute radial velocity as well as range-related information. As Chapter 2 explained, radial velocity is only one component of relative motion. A fusion method can combine that constraint with visual or geometric evidence, but should not treat it as a complete two-dimensional velocity vector.

Radar returns also differ from lidar samples. Their angular uncertainty and reflection behavior can be different, depending on the sensor. Assigning a return to a very precise BEV cell without representing that uncertainty may imply more spatial certainty than the measurement supports.

The [Simple-BEV study by Harley and colleagues, ICRA 2023](https://arxiv.org/abs/2206.07959), is useful context for studying sensor combinations and representation choices with relatively simple components. It encourages examining data and implementation choices rather than attributing every gain to architectural complexity.

For our cyclist, the ideal combination is not three copies of the same guess. It is complementary constraints: appearance suggesting identity, geometry restricting position, and motion measurements informing how the object is moving.

## More sensors do not imply independent errors

Two camera views can share the same illumination problem. A camera and lidar model may both depend on a common inaccurate calibration. Several learned heads may share a backbone that fails under the same unfamiliar input.

If errors are correlated, agreement is weaker evidence than it would be for independent measurements. A system that multiplies confidence values without understanding their dependence can become excessively certain.

Neural fusion often handles reliability implicitly through learned features. That can work well in the training distribution, but it makes evaluation under changed conditions especially important. The network may have learned to rely heavily on whichever modality was usually strongest during training.

A missing or degraded sensor is therefore not automatically handled just because two modalities were present. Training and testing must explicitly examine whether the system can detect degradation, use remaining evidence, and avoid interpreting missing data as a meaningful zero measurement.

## What a useful fusion experiment should isolate

Compare camera-only, lidar-only, and fused systems under clearly reported training and inference conditions. Keep track of image resolution, temporal input, augmentation, and model capacity. Otherwise the fused model may benefit from changes unrelated to the fusion mechanism.

Inspect where improvements occur. Does the camera help classify sparse distant points? Does lidar reduce visual depth error? Does radar improve motion estimates? Task-specific evidence is more informative than a single claim that fusion is better.

Then inspect failure cases. A gain on clean data can coexist with sensitivity to one obscured camera. A model may retain good average accuracy while becoming unstable at camera boundaries. These observations help establish the conditions under which the additional sensor is useful.

The computational cost must include all encoders and alignment operations. A cheap fusion layer does not make the complete multi-sensor system cheap. Hardware, sensor bandwidth, and timing influence the final tradeoff.

## The methodological change is an information interface

The important progression is from combining final decisions toward combining richer representations in a shared physical space. This gives the model more opportunities to resolve ambiguity before producing a compact output.

It also increases coupling. Errors in one branch can influence the shared features, and training must teach the system how to use conflicting evidence. The best interface depends on what the sensors measure and what the downstream task needs.

For our intersection, fusion can help place and identify the cyclist. It still does not reveal the pedestrian's intention or guarantee that the region behind the truck is clear. More evidence improves some estimates without changing the distinction between observed, inferred, and unknown.

## Check your understanding

Why can feature fusion preserve information that late fusion loses? It combines intermediate evidence before each sensor has reduced its observations to a final set of decisions. Weak but useful cues can remain available.

Why is a common BEV grid not enough by itself? Features must also correspond in time, geometry, and meaning. A shared array index does not prove that two observations describe the same physical event.

Next we will follow objects across time, separating the memory needed for tracking from the feature accumulation used to improve perception.

{% include perception-series-nav.html %}
