---
title: 'How Self-Driving Cars See — 22: Learning beyond the labeled examples'
date: '2026-09-10'
permalink: /autonomous-driving-perception/22-pretraining/
excerpt: Our detector has learned from carefully labeled driving scenes. It still encounters unfamiliar vehicles, unusual road equipment, and situations too rare to label exhaustively. One response is to begin with representations learned from a much broader collection of images, videos, or image-text pairs.
tags:
  - autonomous driving
series_number: 22
read_time: false
series: perception
---

{% include perception-series-nav.html %}

Our detector has learned from carefully labeled driving scenes. It still encounters unfamiliar vehicles, unusual road equipment, and situations too rare to label exhaustively. One response is to begin with representations learned from a much broader collection of images, videos, or image-text pairs.

Pretraining changes where a model gets its knowledge. Language can also change how tasks and categories are specified. These developments can help perception, but broad visual or verbal knowledge is not the same as accurate geometry, calibrated uncertainty, or dependable driving behavior.

## Pretraining supplies a starting representation

A model can first learn from a large source dataset, then be adapted to a smaller driving task. The source objective might use category labels, image-text pairs, or relationships constructed from the data itself. The resulting parameters initialize or provide features for the downstream model.

This idea predates recent foundation models. We saw pretrained image features in R-CNN. What changes with scale is the breadth of data, model capacity, and range of tasks for which the representation may be useful.

A frozen backbone provides features without updating its parameters during downstream training. Fine-tuning updates some or all of them. These choices affect computational cost, adaptation, and the risk of losing useful general features.

Transfer must be measured. A representation that distinguishes many object categories may still need adaptation to tiny distant road users or precise depth. A broad pretraining dataset does not guarantee that the particular deployment conditions are covered well.

## Self-supervised learning creates targets from the data

**Self-supervised learning** uses training signals derived from the observations rather than requiring a human category label for every example. Methods can compare transformed views, predict missing content, or train a student representation to match a teacher under specified transformations.

[DINOv2, by Oquab and colleagues, TMLR 2024, first released in 2023](https://arxiv.org/abs/2304.07193), studies large-scale visual feature learning without manual semantic labels for its pretraining objective. It is a general visual representation method, not a complete autonomous driving system.

The choice of transformations matters. If two views are treated as equivalent, the representation is encouraged to preserve what they share. For a geometry task, some changes in position or scale may be important rather than something to ignore entirely.

“No manual labels” also does not mean “no assumptions.” Data selection, augmentation, architecture, teacher construction, and losses all shape the result. The method learns from a designed objective and a particular collection of observations.



<figure>
  <a href="{{ '/images/perception-series/22.svg' | relative_url }}" aria-label="Open diagram at full size" style="width:100%;"><img src="{{ '/images/perception-series/22.svg' | relative_url }}" alt="Broad image or image-text data produce pretrained features, then driving supervision adapts them into geometric outputs. Language can specify a task, but metric grounding remains a separate requirement." width="720" height="510" style="height:auto;" loading="lazy"></a>
  <figcaption>Pretraining broadens the source of information. Driving targets and evaluation still determine whether the resulting features support the required task. Original diagram for this series.</figcaption>
</figure>

## Image-text learning makes categories more flexible

[CLIP, by Radford and colleagues, ICML 2021](https://arxiv.org/abs/2103.00020), learns related image and text representations from paired data. A text description can then provide a way to compare an image with a concept that was not a fixed output class in a conventional classifier.

This supports **open-vocabulary** use: category descriptions can be supplied through language rather than only through a fixed classifier head. It does not mean every possible object will be recognized, or that similarity scores are calibrated probabilities.

For the road obstacle, language might help distinguish a fallen ladder from other equipment. But recognizing the phrase does not establish the ladder's precise position, dimensions, or collision-relevant extent. Those quantities need spatial evidence and appropriate outputs.

A model can also associate concepts through contextual shortcuts. A construction sign may make “roadwork” likely even if the actual obstacle is different. Evaluating local grounding is necessary when the answer must refer to a specific part of the scene.

## Vision-language models combine observations and instructions

A **vision-language model**, or VLM, processes visual input with language. It may answer questions, describe a scene, or produce structured outputs. A **vision-language-action model**, or VLA, additionally connects these inputs to actions or action-like outputs, depending on the system's definition.

[EMMA, by Hwang and colleagues, first released as a 2024 preprint](https://arxiv.org/abs/2410.23262), uses a multimodal model for driving-related outputs including trajectories, objects, and road graph elements. It illustrates a unified language-oriented interface for several driving tasks.

The output format matters. Coordinates expressed as text still need units, reference frames, valid ranges, and parsing. A syntactically plausible sentence can contain incorrect geometry. A fluent explanation is not an independent verification of the action it accompanies.

Likewise, a generated description may omit a small but important object. The task should be evaluated on the physical information required, not only on whether the prose sounds reasonable to a reader.

## Automatic labels can expand training data

A stronger model or offline pipeline can generate labels for additional observations. A smaller student model can then learn from those labels, perhaps with filtering, human correction, or uncertainty weighting. This is often called pseudo-labeling or knowledge distillation, depending on the setup.

The teacher may use information unavailable to the student at inference, such as additional sensors, future frames, or more computation. That can be useful: the training target is allowed to be better informed than the deployed input, as long as the distinction is explicit.

Teacher errors can propagate. If rare cyclists are systematically missed, automatically labeling more data can multiply that omission. Confidence filtering may preferentially retain easy examples, leaving the hardest cases underrepresented.

A data pipeline therefore needs quality checks on the labels themselves. More labeled frames are not automatically more diverse or more informative. The useful quantity is evidence covering the conditions and errors that matter for the downstream task.

## Data selection can matter as much as model size

Driving logs contain many repeated easy moments. Adding thousands of nearly identical straight-road frames may contribute less than adding a carefully chosen set of unusual intersections, weather conditions, or occlusions.

A selection process can prioritize uncertain predictions, disagreements, rare categories, or scenario diversity. Each criterion has biases. A model's uncertainty estimate may itself be unreliable, and disagreement does not always indicate a valuable training example.

Geographic and temporal separation help evaluate transfer. If pretraining or automatic labels include the test locations, the comparison may measure familiarity rather than adaptation. Large datasets make exact overlap harder to inspect, so provenance becomes more important.

Record the source data and training stages when comparing methods. A stronger backbone with extensive external pretraining and a model trained from scratch on a small benchmark do not differ only in architecture.

## General knowledge and metric grounding have different failure modes

A model may know that pedestrians often use crossings, yet place a particular pedestrian at the wrong depth. It may describe a signal correctly, yet associate it with the wrong lane. It may explain a cautious action while its predicted coordinates imply a different maneuver.

These are grounding failures: the abstract description is not correctly tied to the measured scene. Multi-view geometry, explicit coordinate outputs, task-specific supervision, and consistency checks can help, but each requires evaluation.

Language also creates an additional input channel. Road text, signs, and user instructions have different roles. A driving system needs a defined way to interpret relevant scene information without treating arbitrary visible text as an instruction to change its operating rules.

For this blog's scope, the lesson is simply to separate what a model can say from what it can locate, track, and use reliably. Claims about semantic breadth should not substitute for measurements of physical accuracy.

## Compute and timing remain part of the design

A large model can provide rich features but exceed the latency or memory budget of the deployed system. Distillation, smaller adapters, selective invocation, and specialized heads are possible ways to use its knowledge with different costs.

A language generation step can have variable runtime depending on output length and implementation. If the system needs frequent geometric updates, its architecture must account for that timing rather than assuming every task can wait for a long explanation.

The best use of a pretrained model may therefore be as a teacher, a feature extractor, or an auxiliary component, rather than the only online model. The choice should follow the task and available resources.

## Check your understanding

Does open vocabulary mean perfect unknown-object detection? No. It changes how concepts can be specified, but recognition, localization, and uncertainty still need evidence and testing.

Can automatic labels eliminate human judgment about data quality? No. They inherit the teacher's assumptions and errors, making targeted audits and provenance important.

Next we will consider models trained to predict how the scene itself changes, and distinguish generating convincing video from modeling the consequences of driving actions.

{% include perception-series-nav.html %}
