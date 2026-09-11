---
title: '12: Evaluating driving: nuPlan, PDM, NAVSIM, and world models'
date: '2026-09-10'
permalink: /autonomous-driving-perception/12-planning-evaluation/
excerpt: A historical account of driving methods can become misleading if it treats every reported score as evidence of the
  same capability. A detector, a motion predictor, and a sensor-to-trajectory policy solve different tasks. Even two planning
  papers may evaluate different inputs, horizons, actor behavior, or collision definitions.
tags:
- autonomous driving
series: perception
series_number: 12
read_time: false
reading_minutes: 6
redirect_from:
- /autonomous-driving-perception/23-world-models/
- /autonomous-driving-perception/24-evaluation/
---

{% include perception-series-nav.html %}

A historical account of driving methods can become misleading if it treats every reported score as evidence of the same capability. A detector, a motion predictor, and a sensor-to-trajectory policy solve different tasks. Even two planning papers may evaluate different inputs, horizons, actor behavior, or collision definitions.

The final methodological shift is therefore in evaluation: moving from matching recorded futures toward testing the consequences of the vehicle's own choices.

## nuPlan: actions change the vehicle state

[nuPlan — Caesar et al., 2021 benchmark paper](https://arxiv.org/abs/2106.11810) combines real driving logs with a planning simulator and planning-specific metrics. It supports evaluating a planner over rollouts rather than only measuring distance from an expert trajectory.

In a rollout, the planner chooses a motion, the simulated ego vehicle advances, and the planner receives another state. Errors can accumulate and recovery behavior becomes relevant. The behavior of surrounding actors depends on the configured simulation setting; “closed loop” alone does not say whether they react realistically to the ego vehicle.

nuPlan also allows planning to be studied with structured scene inputs. That is useful for isolating planning, but does not measure the complete perception-to-control system under raw sensor errors.

## PDM: a strong baseline can overturn the apparent story

[Parting with Misconceptions about Learning-based Vehicle Motion Planning — Dauner et al., CoRL 2023](https://arxiv.org/abs/2306.07962) separates precise short-term planning from long-horizon prediction of the ego vehicle's recorded behavior. Its PDM methods highlight the value of strong centerline and motion priors.

The study finds that simple designs can be highly competitive, and that an open-loop forecasting task can reward a model with surprisingly limited scene context. The PDM family includes different variants; PDM-Open and PDM-Closed should not be treated as interchangeable systems.

The methodological implication is important: if a model gains little from other-agent information on a benchmark, that may reveal a limitation of the task or metric. It does not establish that other agents are unnecessary for driving.

<figure>
  <a href="{{ '/images/driving-papers/12.svg' | relative_url }}" style="width:100%;" aria-label="Open architecture diagram at full size"><img src="{{ '/images/driving-papers/12.svg' | relative_url }}" alt="Evaluating driving: nuPlan, PDM, NAVSIM, and world models: a comparison of the information passed between the methods' main stages." width="760" height="460" style="height:auto;" loading="lazy"></a>
  <figcaption>Original schematic of the methods discussed here; simplified information flow, not a reproduction of a paper's complete architecture.</figcaption>
</figure>

## NAVSIM: a deliberate middle ground

[NAVSIM — Dauner et al., NeurIPS 2024](https://arxiv.org/abs/2406.15349) combines real observations with non-reactive simulation for scalable evaluation of proposed driving trajectories. It aims to provide more behavior-relevant evidence than plain trajectory distance without the expense of fully interactive sensor simulation.

Its non-reactive setting is a defining assumption. Other agents do not provide a fully realistic response to arbitrary ego actions, and this protocol should not be relabeled as unrestricted interactive closed-loop driving.

When reading DiffusionDrive or another NAVSIM result, the benchmark version and metric implementation belong alongside the score. A percentage or aggregate planning score cannot be compared directly with nuPlan or CARLA numbers simply because all concern driving.

| Evaluation | What can change | What it can miss |
|---|---|---|
| Open-loop trajectory comparison | The predicted trajectory | Consequences for later observations |
| Non-reactive simulation | Simulated ego motion | Responses of other road users |
| Interactive closed-loop simulation | Ego motion and modeled responses | Errors in the simulator itself |

## World models address a related, harder requirement

[GAIA-1 — Hu et al., 2023 preprint](https://arxiv.org/abs/2309.17080) generates driving video conditioned on information including video, text, and actions. It illustrates the ambition to learn how a scene could develop under different conditions rather than merely replaying a fixed recording.

That is relevant to training data and simulation, but realistic-looking video is not sufficient evidence of a valid decision simulator. Geometry, timing, collision outcomes, and responses to actions all matter. A model can generate a plausible scene while answering a counterfactual driving question incorrectly.

World models therefore extend the evaluation and training discussion; they should not be presented as having already resolved the limitations of established planning benchmarks.

## What changed across this series

The papers describe a progression of interfaces: image features became boxes and pixels; 3D encoders organized physical space; BEV and queries brought camera evidence into that space; tracks, maps, occupancy, and forecasts supplied structure for planning. Learned costs, joint task training, vectors, and generative decoders then changed how trajectories were chosen.

These branches remain active together. More integration can preserve evidence across tasks, while explicit structure can improve efficiency and inspectability. The strongest comparison identifies the representation, the supervision, and the evaluation boundary, then asks whether the claimed improvement survives a matched experiment.

That is the useful endpoint of a paper history: understanding why an architectural choice exists, what it leaves unresolved, and what kind of evidence would justify choosing it for a driving system.

{% include perception-series-nav.html %}
