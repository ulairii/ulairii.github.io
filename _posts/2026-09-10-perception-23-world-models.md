---
title: 'How Self-Driving Cars See — 23: Can a car predict how the world will change?'
date: '2026-09-10'
permalink: /autonomous-driving-perception/23-world-models/
excerpt: 'Imagine pausing our car before the crossing and asking two questions: what might happen if it slows down, and what might happen if it continues? A world model attempts to predict some aspect of the evolving environment, potentially conditioned on those different actions.'
tags:
  - autonomous driving
series_number: 23
read_time: false
series: perception
---

{% include perception-series-nav.html %}

Imagine pausing our car before the crossing and asking two questions: what might happen if it slows down, and what might happen if it continues? A world model attempts to predict some aspect of the evolving environment, potentially conditioned on those different actions.

This is broader than detecting the current truck and more demanding than generating an attractive driving video. The model's usefulness depends on what it predicts, whether actions actually control the prediction, and how errors behave over a sequence of imagined steps.

## A world model needs a defined state and transition

At a high level, a model receives a representation of the current situation and predicts a later one. That representation might be images, occupancy, object states, or a learned latent vector. The transition may also depend on the car's action and other conditioning information.

A **latent state** is an internal learned representation rather than a directly displayed scene. It can be compact and useful for planning, but its physical meaning is not automatically transparent. A decoder may turn it into images or other outputs for supervision and inspection.

The term world model covers many systems. Some predict observations without an action input. Others model action-conditioned transitions. Some are used only for generating training data; others participate in online planning. These roles should be specified before comparing claims.

For our intersection, the important question is whether the model preserves the cyclist, the hidden region, road geometry, and the consequences relevant to the proposed motion. A visually detailed sky is less important to that decision.

## Video generation learns a distribution of continuations

A generative model can learn to produce likely future frames from past frames and optional controls. It may compress images into tokens or latent features, model their evolution, and decode the resulting sequence back into pixels.

[GAIA-1, by Hu and colleagues, released as a 2023 preprint](https://arxiv.org/abs/2309.17080), uses video, text, and action inputs to generate driving scenarios. It is a useful example of combining scene generation with control over aspects of the continuation.

The generated video can support data creation and exploration. But visual plausibility alone does not establish accurate metric geometry or interaction. A cyclist might change size subtly, disappear during occlusion, or move inconsistently while the sequence remains convincing at a glance.

The validation question must follow the intended use. A model used for appearance augmentation has different requirements from a model used to estimate collision consequences of a planned action. One visual-quality score cannot certify both.



<figure>
  <a href="{{ '/images/perception-series/23.svg' | relative_url }}" aria-label="Open diagram at full size" style="width:100%;"><img src="{{ '/images/perception-series/23.svg' | relative_url }}" alt="A current scene branches into two action-conditioned rollouts: slow down or continue. Each produces a predicted future that must be checked against evidence and task requirements." width="720" height="510" style="height:auto;" loading="lazy"></a>
  <figcaption>Action-conditioned alternatives are predictions, not observations of what would certainly happen. A useful model must respond consistently to the chosen action. Original diagram for this series.</figcaption>
</figure>

## Action conditioning is stronger than describing an action

Supplying the words “turn right” is not enough unless the generated transition follows a meaningful relation to that action. The model should change the vehicle's future position, viewpoint, and relevant interactions consistently with the specified control or trajectory.

Action definitions vary. An input may be steering and acceleration, a target waypoint, a planned trajectory, or a high-level instruction. Each carries different information and requires a different transition model.

Recorded data show the action that actually occurred and its observed continuation. They usually do not show what the same scene would have become under every alternative action. Learning reliable counterfactual responses therefore requires assumptions, diversity in data, or additional interactive evidence.

A model can exploit correlations instead. If turning actions usually occur in particular scene types, it may generate a plausible turn without accurately modeling the consequences of changing the action in an unusual setting. Controlled evaluations should test sensitivity to the action itself.

## Predicting in a latent space can reduce computation

Generating every pixel at every imagined step can be expensive. A model can instead predict a compact internal state and use it to score candidate actions or produce task-relevant outputs. This may focus capacity on information useful for driving.

[World4Drive, released in 2025](https://arxiv.org/abs/2507.00603), explores an intention-aware latent world model for end-to-end driving. It provides a concrete research example of connecting learned future representations to planning rather than treating video generation as the final product.

A compact state can omit information that later becomes important. If a small obstacle is not preserved, a planner using that state may never consider it. The training losses and evaluation determine whether the latent representation retains the required details.

An auxiliary reconstruction or perception objective can make some information easier to inspect. However, a good decoded image does not prove that every action-relevant quantity is represented accurately, and a poor-looking image does not necessarily imply every planning feature is useless.

## Errors compound during rollout

A one-step prediction can be close to the next observation. In a rollout, the model may feed its own predicted state into the next transition. Errors then become part of the input and can accumulate.

A slightly misplaced cyclist can lead to a wrong occlusion pattern, which changes later appearance and motion predictions. A small road-geometry error can shift the imagined camera path. The sequence can drift even if individual short-horizon predictions look reasonable.

Training may use true past observations more often than the model will receive during imagined rollout. This creates a difference between training inputs and its own imperfect generated states. Evaluation should therefore include the rollout lengths and conditions relevant to its use.

Replanning with fresh measurements can limit drift in an online system. The world model need not predict indefinitely, but it must be useful over the horizon for which its outputs influence a decision.

## The planner can exploit a model's mistakes

If an optimizer searches for actions with high predicted reward, it may discover actions that look good only because the world model is inaccurate there. This is a general issue in model-based decision making.

For example, a model might fail to represent a barrier under an unusual viewpoint. A planner could prefer a path through that region because the imagined future appears unobstructed. The action search amplifies the model's weakness instead of averaging it away.

Constraining the action space, using uncertainty, checking against explicit geometry, and updating with real observations are possible responses. Their value must be tested in the actual system rather than assumed from the presence of an uncertainty output.

The key distinction is between a model that predicts common logged futures and one that remains reliable under the actions a planner actively selects. The latter is a stronger requirement.

## Generated data can help while carrying its own bias

Synthetic scenes can vary lighting, traffic, and appearance without collecting a new physical drive for every variation. They may provide targeted examples or support testing of specific behaviors.

But the generator's distribution limits the result. Rare hazards absent from training may also be absent or unrealistic in generated scenes. Automatic labels must remain consistent with the generated geometry, especially across cameras and time.

Training and evaluating only within one generator can produce a misleading agreement. A model may learn the generator's artifacts and perform well on similar synthetic tests while transferring poorly to real observations. Independent real-data evaluation remains important.

Generated scenarios should also be distinguished from empirical evidence. A hypothetical illustration can explain a failure mechanism, but it is not a measured incident or a demonstrated success of a deployed system.

## What should a world-model evaluation measure?

Start with the task. For sensor simulation, inspect image quality, multi-view agreement, temporal consistency, geometry, and response to control. For planning, inspect how model use changes closed-loop behavior under defined scenarios.

Check object permanence: does the cyclist remain represented while hidden? Check physical consistency: do trajectories and viewpoints agree with motion? Check diversity: are meaningful alternatives represented, or does the model repeat one common future?

Uncertainty also needs attention. Multiple generated samples are not automatically a calibrated distribution. The frequency and coverage of predicted events should be compared with appropriate observations or controlled experiments.

Finally, report the boundaries. These papers demonstrate research directions and specific results. This chapter does not claim that generating video or predicting a latent state establishes general driving reliability.

## Check your understanding

Can a convincing video be a poor planning model? Yes. Small geometric or causal errors can matter for action selection even when the video looks natural.

Why is action-conditioned prediction difficult to validate from logs alone? A log records one realized action sequence and future, leaving alternative outcomes unobserved. Counterfactual claims need additional assumptions and evidence.

We have reached the frontier of the series. The final chapter returns to the original intersection and builds a practical checklist for judging every representation, from image boxes to world models.

{% include perception-series-nav.html %}
