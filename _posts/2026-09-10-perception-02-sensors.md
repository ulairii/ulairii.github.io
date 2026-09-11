---
title: 'How Self-Driving Cars See — 02: What do cameras, lidar, and radar actually measure?'
date: '2026-09-10'
permalink: /autonomous-driving-perception/02-sensors/
excerpt: The cyclist from Chapter 1 is approaching the intersection at dusk. A camera records a small dark shape, lidar returns a few points from the bicycle and rider, and radar may report a reflection with a measured relative speed. These observations describe the same scene in very different ways.
tags:
- autonomous vehicles
- perception
- deep learning
- perception series
series_number: 2
read_time: false
---

{% include perception-series-nav.html %}

The cyclist from Chapter 1 is approaching the intersection at dusk. A camera records a small dark shape, lidar returns a few points from the bicycle and rider, and radar may report a reflection with a measured relative speed. These observations describe the same scene in very different ways.

Before asking which neural network to use, we need to understand the evidence. A model cannot reliably recover information simply because we would like that information to be present. Sensor physics determines what is measured, where measurements are missing, and which mistakes are plausible.

## A camera measures arriving light

A camera forms an image by focusing light onto a sensor. The image is a grid of pixels, each storing a response related to the light that reached that location during an exposure. Color channels help describe differences in appearance. This makes images useful for reading signals, finding painted markings, and recognizing objects.

The image has two spatial coordinates, usually called horizontal and vertical pixel positions. The world has three. A particular pixel identifies a direction from the camera, but it does not by itself specify how far along that direction a surface lies. A nearby small object and a distant large object can occupy similar areas in the image.

Cameras provide rich appearance information over many image locations, but their measurements depend on illumination and exposure. At night, a longer exposure can collect more light while increasing motion blur. A bright lamp and a dark pedestrian may require more brightness range than the imaging system can preserve at once. These effects happen before a detector begins its work.

A learned model can use context to estimate missing depth or recover likely object boundaries. That is inference from evidence and prior experience. It is different from directly measuring the distance to every visible pixel. Chapter 4 will make the geometric distinction precise.

## Lidar measures travel time or related ranging information

A common lidar design emits laser pulses and measures the time taken for reflected light to return. Because the pulse travels to a surface and back, distance is approximately the speed of light multiplied by the travel time, divided by two. Other lidar designs use different ranging mechanisms, but the central output is still distance along a measured direction.

Combining a distance with the direction of a beam gives a point in three-dimensional space. Many such returns form a **point cloud**. The cloud samples surfaces that produced detectable reflections. It is not a solid model of every object around the car, and a missing return does not automatically establish empty space.

Sampling matters. Imagine beams separated by a fixed angle. Farther from the sensor, the physical gap between adjacent beams is larger. A distant pedestrian may therefore receive fewer returns than a nearby truck. Increasing range does not preserve the same surface detail everywhere.

Materials and conditions also affect returns. Some surfaces reflect poorly toward the receiver; glass can produce more complicated observations than an opaque wall. Rain and fog can scatter light. A spinning scanner collects different directions at different times, so motion during a sweep can distort the apparent shape unless timing is handled carefully.



<figure>
  <a href="{{ '/images/perception-series/02.svg' | relative_url }}" aria-label="Open diagram at full size" style="width:100%;"><img src="{{ '/images/perception-series/02.svg' | relative_url }}" alt="Three panels compare a camera image grid, lidar surface points, and a radar return with radial velocity." width="720" height="460" style="height:auto;" loading="lazy"></a>
  <figcaption>The sensors provide different measurements. The radial velocity arrow points toward or away from the radar; it is not a complete motion vector. Original diagram for this series.</figcaption>
</figure>

## Radar measures reflected radio signals

Automotive radar transmits radio waves and analyzes the received signals. Many systems estimate distance, direction, and **radial velocity**: the component of relative motion along the line between sensor and reflector. A frequency change associated with relative motion helps make that velocity measurement possible.

Radial velocity is not the same as an object's full speed and direction. Suppose a cyclist moves almost sideways across the radar's view. The cyclist can move quickly while the distance to the radar changes only slowly. A small radial speed therefore does not establish that the cyclist is stationary.

A radar detection also need not coincide with an object's geometric center. Strong reflections may come from particular parts of a vehicle. Reflections involving other surfaces can create indirect paths, complicating the relationship between a measured return and the physical scene. Interpreting these signals still requires processing and often learned models.

Radar is useful in conditions where optical appearance is poor, but “works in bad weather” should not become “unaffected by weather.” Angular resolution, antenna arrangement, waveform, processing, and interference all matter. We should describe a specific sensor and task instead of assuming every radar offers the same information.

## Three sensors do not produce three interchangeable pictures

Consider a red traffic signal. Color is directly relevant to its meaning, so an image provides evidence that distance measurements alone do not contain. Now consider a plain truck side with little visual texture. Lidar may provide strong evidence of its range even when finding visual correspondences is difficult.

The point is complementarity. Different measurements can constrain different unknowns. If an image suggests a vehicle and lidar supplies nearby surface geometry, a fusion method may estimate its category and position more reliably than either observation alone. That improvement depends on associating the measurements correctly.

The [nuScenes dataset, introduced by Caesar and colleagues at CVPR 2020](https://arxiv.org/abs/1903.11027), includes cameras, lidar, and radar, making these combinations accessible to researchers. Its sensor configuration is a property of that dataset, not a universal recipe for autonomous vehicles. The [Waymo Open Dataset paper by Sun and colleagues, also CVPR 2020](https://arxiv.org/abs/1912.04838), provides another primary example of synchronized camera and lidar observations.

Neither dataset should be read as an experiment proving that one sensor combination is sufficient for every road. They provide measurements, annotations, and evaluation settings in which particular methods can be studied.

## Alignment has both a spatial and a temporal part

Suppose the camera sits behind the windshield while lidar is mounted on the roof. Their coordinates have different origins and orientations. **Calibration** provides the transformations needed to relate them. A point measured in lidar coordinates must be transformed before we can ask which camera pixel corresponds to it.

Even perfect spatial calibration is insufficient if the observations refer to different moments. If a cyclist moves at 5 meters per second, a 0.1-second difference corresponds to half a meter of travel. That simple calculation illustrates why timestamp errors can look like geometric disagreement.

There are also differences within a single sensor observation. A lidar sweep may take time to accumulate. Some cameras expose rows at slightly different times. The car can move while either observation is being collected. A practical perception system needs a policy for bringing these measurements to a common reference time.

The calibration matrices and timestamps may look like supporting metadata, but they can determine whether fusion helps. A powerful model can learn some tolerance to error. It does not remove the need to understand where its inputs came from.

## Choosing measurements starts with a question

For our cyclist, ask separately about category, distance, direction, and future behavior. Images may reveal appearance. Lidar may sample the rider's surfaces. Radar may constrain motion along its line of sight. Repeated observations can help estimate movement across the road. None directly reveals the cyclist's future intention.

Then ask about the scene we cannot observe. The truck still blocks some lines of sight. Adding another sensor at nearly the same position does not guarantee a view around that truck. Different materials interact with different signals, but ordinary sensor fusion should not be described as an ability to see through every obstacle.

Finally, consider failure detection. If one camera is obscured by dirt, its output may look different from the conditions used during training. If lidar produces fewer returns, the cause might be distance, material, or a sensor problem. Distinguishing those cases is part of interpreting evidence, rather than just running an object classifier.

## Check your understanding

A radar return reports nearly zero radial velocity. Can the object still move across the road? Yes. Sideways movement can have a small component along the sensor's line of sight. Recovering a full motion estimate requires more information or assumptions.

An image contains more pixels than a point cloud contains points. Does that make the image a more accurate distance sensor? No. The number of measurements and the physical quantity measured are different issues. More appearance samples do not automatically resolve depth ambiguity.

We now have three forms of evidence. Next we will see how training turns examples of such evidence into a model that makes useful predictions, and why success on familiar examples does not guarantee success on a new road.

{% include perception-series-nav.html %}
