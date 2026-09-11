---
title: 'How Self-Driving Cars See — 21: Does better perception produce better driving?'
date: '2026-09-10'
permalink: /autonomous-driving-perception/21-planning/
excerpt: Suppose a new detector improves its average score by finding more distant vehicles. At our intersection, it still places the cyclist slightly too close to the curb. The planner's response may barely improve, even though the perception benchmark does.
tags:
- autonomous vehicles
- perception
- deep learning
- perception series
series_number: 21
read_time: false
---

{% include perception-series-nav.html %}

Suppose a new detector improves its average score by finding more distant vehicles. At our intersection, it still places the cyclist slightly too close to the curb. The planner's response may barely improve, even though the perception benchmark does.

This gap motivates planning-oriented learning. Instead of optimizing every component only for its own isolated target, a system can train representations and tasks with the final driving objective in mind. The challenge is to preserve useful structure while allowing information and learning signals to cross task boundaries.

## A modular pipeline uses explicit interfaces

A conventional description separates perception, tracking, prediction, planning, and control. Each component receives an input, performs a task, and returns a defined output. An object list or map can be inspected and tested independently.

These interfaces provide clarity, but they also compress information. A detector may pass only a box and score, discarding feature evidence useful for prediction. A predictor may return a small set of paths without conveying how uncertain the initial observation was.

Errors can propagate. If the pedestrian is missed, a downstream predictor may have no entity to forecast. If the map connects the wrong lane, a planner can reason consistently over an incorrect road structure. Optimizing each module separately does not necessarily minimize the final effect.

This is a motivation for tighter coordination, not proof that explicit modules are inherently unsuitable. Their inspectability and well-defined contracts remain useful. The question is where sharing features or objectives addresses a real information loss.

## End-to-end describes a training or computation boundary

A detector trained from images to boxes can be end-to-end within that boundary. A model trained from sensors to a trajectory has a different boundary. A system that outputs a trajectory may still use a separate controller to produce steering and braking commands.

The phrase does not tell us whether intermediate outputs exist. An end-to-end trained network can still predict boxes, tracks, maps, and occupancy as auxiliary or structured components. Nor does it establish that all components are trained simultaneously from scratch.

When reading a paper, identify the actual input, output, supervision, training stages, and downstream controller. Those details are more informative than assuming that end-to-end means one undifferentiated network does everything.

This distinction also prevents false historical claims. Earlier learned controllers and later planning-oriented architectures occupy different points in a long research history. A recent model name should not be treated as the invention of the entire idea.



<figure>
  <a href="{{ '/images/perception-series/21.svg' | relative_url }}" aria-label="Open diagram at full size" style="width:100%;"><img src="{{ '/images/perception-series/21.svg' | relative_url }}" alt="One route passes explicit boxes and forecasts between separate tasks. A second route shares learned features across structured perception, prediction, and planning outputs, with training losses attached to several tasks." width="720" height="515" style="height:auto;" loading="lazy"></a>
  <figcaption>Joint learning can retain intermediate structure while allowing tasks to exchange features. A planned trajectory still needs execution and feedback. Original diagram for this series.</figcaption>
</figure>

## UniAD organizes tasks around planning

[UniAD, by Hu and colleagues, CVPR 2023](https://arxiv.org/abs/2212.10156), connects tracking, mapping, motion forecasting, occupancy-related prediction, and planning through a unified framework with query interfaces. It is a useful example of structured tasks designed to contribute to planning.

The methodological point is coordination. Information does not have to be reduced to separate final outputs before every interaction. Learned representations can be shared and combined so later tasks use evidence from earlier ones.

This does not mean detection labels become unnecessary or that intermediate errors disappear. Training still relies on objectives and data, and the architecture retains task structure. The final behavior depends on how those tasks are supervised and connected.

The paper's benchmark results support claims within its evaluated setting. They should not be expanded into a claim that all aspects of real-world autonomy have been established. We will distinguish logged planning metrics from closed-loop driving later in the chapter.

## Shared losses can help and conflict

A multi-task model might minimize a weighted sum of detection, mapping, forecasting, and planning losses. Each loss encourages a different property. The weights and training schedule influence which errors dominate learning.

A feature useful for identifying a vehicle category may differ from one useful for predicting its motion. Shared capacity can support both, but it can also create competition. More tasks are not automatically better merely because they are attached to the same backbone.

A planning loss can emphasize information relevant to the chosen action. Yet if the training data rarely contain a certain hazard, the model may receive little learning signal about it. Task alignment does not remove the need for coverage of difficult situations.

Intermediate supervision can help preserve interpretable quantities and prevent some shortcuts. But an auxiliary output is only useful evidence of internal behavior if it is meaningfully connected to the computation used for the final decision.

## Imitation learns from demonstrated behavior

Many learned driving systems use demonstrations: sensor observations paired with the motion taken by a human or another policy. **Imitation learning** trains the model to reproduce that behavior under the recorded conditions.

[TransFuser, by Chitta and colleagues, IEEE TPAMI 2023](https://arxiv.org/abs/2205.15997), studies transformer-based sensor fusion for driving through imitation. It offers another example of linking perception features to actions or waypoints, with closed-loop simulation as part of its evaluation.

Demonstrations provide concrete targets, but they do not show every acceptable action. Two drivers can navigate the same situation safely with slightly different paths or timing. A distance from the recorded trajectory is therefore not identical to a safety judgment.

The model can also exploit correlations that predict the demonstration without fully using the scene. If most examples continue straight at similar speeds, a simple motion prior may perform surprisingly well on some logged metrics. Strong baselines help reveal this possibility.

## Open-loop evaluation holds the recorded world fixed

In an **open-loop** evaluation, a model receives recorded inputs and its predictions are compared with labels or a recorded future. The model's action does not change the next observation in that log.

This makes evaluation reproducible and scalable. It can measure geometric accuracy or trajectory agreement on a defined dataset. But it does not fully test what happens after the model makes a different decision from the recorded driver.

A slightly wrong turn can place the car in a new viewpoint. The next input should then differ, and other road users may react. A log replay that continues along the original path cannot directly show that evolving interaction.

Thus a lower logged trajectory error is useful evidence about one task, not a complete demonstration of closed-loop competence. The interpretation must match the evaluation boundary.

## Closed-loop evaluation lets actions affect later observations

In **closed-loop** evaluation, the selected action changes the vehicle state and subsequent inputs. A simulator or controlled physical setting can then reveal compounding errors, recovery behavior, interactions, and the effect of delay.

The simulator must model enough of the relevant world for the test to be meaningful. Sensor rendering, vehicle dynamics, road-user behavior, and scenario selection can all affect the result. Passing one simulation suite does not establish performance in every environment.

Useful comparisons report completion, infractions, collisions under defined rules, comfort-related behavior, and the tested conditions. A policy that avoids incidents by never moving may fail the intended task. Progress and constraint satisfaction need to be considered together.

This returns us to the opening cyclist. We want to know whether the chosen motion leaves appropriate space and whether the system updates if the cyclist turns. Those are sequential questions that cannot be answered by one detection screenshot.

## Does planning-oriented learning eliminate perception?

No. A model that maps sensors to motion still needs to extract useful information from measurements, even if it does not expose every estimate as a named module. Perception can become less explicit without ceasing to exist as a computational responsibility.

Explicit representations remain useful for diagnosis, auxiliary training, and other system functions. Whether to retain boxes, maps, or occupancy depends on their value and cost. The design space includes many mixtures of learned and structured components.

The important methodological shift is to ask which information actually helps choose and execute motion, then examine whether isolated objectives preserve that information. This connects the earlier representation choices to the final purpose of the system.

## Check your understanding

Does end-to-end training require removing intermediate tasks? No. A jointly trained system can retain structured outputs and task-specific losses. The training boundary and internal organization are separate properties.

Does lower trajectory error on logged data prove better driving after a mistake? No. Closed-loop evaluation is needed to study how actions alter subsequent states and observations, within the limits of the test environment.

Next we will examine another source of change: large-scale pretraining and language, which can broaden the knowledge available to perception while introducing new questions about grounding and precision.

{% include perception-series-nav.html %}
