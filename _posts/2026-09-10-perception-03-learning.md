---
title: 'How Self-Driving Cars See — 03: How does a neural network learn to recognize a car?'
date: '2026-09-10'
permalink: /autonomous-driving-perception/03-learning/
excerpt: 'Imagine trying to describe a car with a list of rules: find two wheels, look for a windshield, then check for a roughly rectangular body. The rules might work for a clean side view. At our intersection, the parked truck hides half the car, the lighting changes, and the visible wheels may be tiny.'
tags:
  - autonomous driving
series_number: 3
read_time: false
series: perception
---

{% include perception-series-nav.html %}

Imagine trying to describe a car with a list of rules: find two wheels, look for a windshield, then check for a roughly rectangular body. The rules might work for a clean side view. At our intersection, the parked truck hides half the car, the lighting changes, and the visible wheels may be tiny.

Deep learning changes how the useful visual patterns are obtained. Instead of specifying every pattern by hand, we choose a model with adjustable parameters and train it on examples. The model learns computations that help produce the requested output. Understanding this process will make the later architectures much less mysterious.

## Features are measurements made useful for a task

A raw pixel describes local brightness or color. A **feature** is a transformed description intended to make some property easier to use. An edge response, for example, describes a local change in brightness. A more complex feature might respond to a combination of shapes and textures.

Before deep learning became widespread in vision, many successful approaches used manually designed features with a learned classifier. Researchers chose how to summarize gradients or local patterns, then fitted a decision rule. Learning itself was not new. One major change was learning multiple stages of the representation along with the prediction task.

A neural network is a sequence of parameterized operations. Its parameters are numbers adjusted during training. Early layers transform the input, later layers transform those results, and an output layer produces quantities such as class scores. A layer does not need a human-readable interpretation to be useful.

The [AlexNet paper by Krizhevsky, Sutskever, and Hinton, NeurIPS 2012](https://papers.nips.cc/paper/4824-imagenet-classification-with-deep-convolutional-neural-networks), is a useful historical anchor for large-scale learned image representations. It studied image classification. It did not itself provide a complete driving perception system, and we should keep that distinction when tracing the history.

## A convolution applies the same small calculation in many places

A convolutional layer moves a small collection of weights across an image or feature map. At each position, it combines nearby values. Reusing the weights allows the same local pattern to be detected in different parts of an image without learning an entirely separate detector for each position.

One small filter sees only a limited neighborhood. Stacking layers expands the region that can influence an output. A later feature can therefore combine evidence from parts that are farther apart. This region of influence is often called the **receptive field**.

A feature map also has channels. You can think of them as different learned measurements at each spatial location. They are not necessarily red, green, and blue after the first layer. One channel may respond to some useful pattern; another may encode information that is difficult to summarize in ordinary language.

Reducing spatial resolution makes later computation cheaper and lets features summarize a larger area. But it can also discard detail. This tradeoff will return when a distant pedestrian occupies only a few pixels, and again when a three-dimensional grid uses large cells to save memory.



<figure>
  <a href="{{ '/images/perception-series/03.svg' | relative_url }}" aria-label="Open diagram at full size" style="width:100%;"><img src="{{ '/images/perception-series/03.svg' | relative_url }}" alt="A training loop compares a prediction with a label, computes a loss, and updates model parameters. At inference the trained model uses measurements without access to the label." width="720" height="480" style="height:auto;" loading="lazy"></a>
  <figcaption>Training uses target answers to adjust parameters. At inference, the target answer is unavailable. Original diagram for this series.</figcaption>
</figure>

## Training needs a target and a way to measure error

Suppose we start with cropped images labeled “car” or “not car.” The model produces a score for each class. A **loss function** assigns a penalty based on how those scores relate to the correct label. Training changes the parameters to reduce the loss across examples.

For a position estimate, the target and loss differ. A model might predict a box center and receive a penalty for being far from the annotated center. A detector often combines classification loss with losses for geometric quantities. Their relative weights affect what errors the training process emphasizes.

**Backpropagation** computes how a small change in each parameter would affect the loss, using the chain rule from calculus. An optimizer uses those gradients to update parameters. Repeating this over many batches of examples can produce useful behavior even though no one wrote a rule describing each object appearance.

The target still defines what the model is rewarded for doing. If the annotation contains only object categories, the model is not automatically being taught precise three-dimensional geometry. If hidden objects are omitted by policy, the meaning of a missing annotation must be understood before interpreting predictions.

## A tiny example of learning the wrong clue

Imagine a training set where almost every truck appears on a bright highway and every bicycle appears on a dark street. A model might exploit the background because it is predictive in those examples. It can reduce training loss without learning the distinction we intended.

Now put the bicycle on the highway. The shortcut no longer works. This is a failure of **generalization**: performance on new examples differs from performance on the data used to fit the model. The training objective alone does not guarantee the right causal explanation.

A separate validation set helps choose settings, such as model size or the number of training steps. A test set should be reserved for the final evaluation. Repeatedly tuning based on test results makes the test less independent, even if no test image is used in a gradient update.

For driving, random image splitting can be particularly misleading. Adjacent frames from the same journey may look almost identical. If one frame goes into training and its neighbor goes into testing, the test may not measure adaptation to a genuinely different location or condition. Splits should reflect the intended use.

## Labels and augmentation shape what gets learned

An annotation is a human or automatically produced target, not a perfect copy of reality. Different annotators may draw slightly different boxes around an occluded person. An object may be too small to label confidently. A labeling policy may exclude classes that still matter on the road.

**Data augmentation** creates modified training examples, such as brightness changes or carefully adjusted geometric transformations. Its purpose is to expose the model to variation that should not change the desired answer, or to change the target consistently when the input changes.

Consistency is essential. If an image is resized, its pixel coordinates change. If it is used together with camera geometry, the corresponding camera parameters may also need updating. If a three-dimensional scene is rotated, its boxes and motion vectors must rotate with it. Otherwise augmentation creates contradictory supervision.

Augmentation also has limits. Making a daytime image darker is not a complete simulation of night, with different exposure, noise, lights, and visibility. It can be useful while still leaving a gap between transformed examples and the actual deployment environment.

## A backbone and a head divide responsibilities

Later papers frequently describe a **backbone** and a **head**. The backbone computes a reusable representation. The head converts that representation into a task-specific output, such as class scores, box coordinates, or a depth distribution. These are convenient names for parts of a computation.

A backbone can be **pretrained** on one task, then adapted to another. Pretraining may supply useful visual features before the smaller task-specific dataset is used. The [R-CNN paper by Girshick and colleagues, CVPR 2014](https://arxiv.org/abs/1311.2524), is an early example connecting a pretrained convolutional representation to object detection.

Transfer does not mean every useful property carries over. A classifier can tolerate some changes in object position because the category remains the same. A localization system must preserve enough spatial detail to report where the object is. The downstream task influences which features and training procedures are appropriate.

## What changes when training ends?

During **inference**, the trained parameters are used to process new measurements. The model does not get to compare its answer with a ground-truth label before returning a prediction. A confidence score comes from the model's computation; it is not a certificate that the answer has been externally checked.

Training and inference also have different resource needs. Training stores information required for gradient computation and processes many repeated examples. Inference must satisfy the deployed system's timing and memory constraints. A method that is easy to train on a large server may still be unsuitable for the computer in a vehicle.

When a paper says a model is “end-to-end,” ask which endpoints it means. It may mean that image features and detection outputs are trained together. It need not mean that raw sensor input is connected all the way to steering. We will keep checking that phrase throughout the series.

## Check your understanding

A model has a very low training loss but misses cyclists at a new intersection. What should you inspect? The training examples, labels, data split, and differences in viewing conditions are all plausible causes. Increasing the model size is only one possible response, and may not address the problem.

A network predicts “car” correctly. Has it learned the distance to the car? Not necessarily. Its target may never have required distance, and the features sufficient for classification need not resolve it.

We can now separate the learning machinery from the problem being learned. Next comes the geometry that connects image positions to physical space, before we build the first detectors.

{% include perception-series-nav.html %}
