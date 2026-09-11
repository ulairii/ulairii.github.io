---
title: '11: Efficient and generative planning: VAD and DiffusionDrive'
date: '2026-09-10'
permalink: /autonomous-driving-perception/11-vector-and-diffusion-planning/
excerpt: 'Two decisions shape a learned planner: how it represents the scene and how it represents possible actions. VAD changes
  the scene interface by using vectors for agents and map elements. DiffusionDrive changes trajectory generation by producing
  multiple alternatives through a short denoising process.'
tags:
- autonomous driving
series: perception
series_number: 11
read_time: false
reading_minutes: 5
---

{% include perception-series-nav.html %}

Two decisions shape a learned planner: how it represents the scene and how it represents possible actions. VAD changes the scene interface by using vectors for agents and map elements. DiffusionDrive changes trajectory generation by producing multiple alternatives through a short denoising process.

These are related developments, but one does not logically replace the other. A compact scene encoder and a generative trajectory decoder address different parts of the architecture.

## VAD: use agents and road vectors as planning structure

[VAD — Jiang et al., ICCV 2023](https://arxiv.org/abs/2303.12077) constructs vectorized agent motion and map representations for planning. The planner uses instance-level structure, with objectives that encourage consistency with agent motion and road geometry.

This reduces reliance on dense rasterized intermediate outputs as the interface to the planner. It does not mean every stage of the network is free of dense image or BEV computation; the important change is the representation passed into scene reasoning and planning.

Vectors make relationships such as distance to an agent trajectory or a road boundary explicit. They can also reduce the cost of processing large spatial output grids. The tradeoff is representational coverage: obstacles and geometry omitted from those vectors cannot contribute through that interface.

VAD is best read as a proposal about how much scene structure planning needs, with efficiency and behavior evaluated under the paper's experimental conditions.

## A single regression target is a restrictive action model

Suppose either yielding or proceeding later would be reasonable, depending on how an interaction develops. A network trained against one demonstrated trajectory observes only the choice the demonstrator made. It does not receive a complete catalog of safe alternatives.

Predicting several trajectories can represent such alternatives, but producing variety is only half the problem. The system also needs to rank candidates according to scene evidence, route intent, and driving quality. A collection containing one good path and many dangerous ones is not automatically a strong policy.

This distinction separates **generation** from **selection**. It also explains why generative modeling is a useful mechanism without being a complete planning objective.

## DiffusionDrive: start near plausible trajectories

[DiffusionDrive — Liao et al., CVPR 2025](https://arxiv.org/abs/2411.15139) uses a truncated diffusion process for end-to-end driving. Instead of beginning from unrestricted noise and requiring many refinement steps, it starts from noisy trajectory anchors representing different modes.

A scene-conditioned decoder denoises these candidates using a short schedule. The anchors provide a prior over plausible actions, while learned refinement adapts the trajectories to the current scene. The paper's reported configuration uses two denoising steps and evaluates planning on NAVSIM.

This is a design for reducing the runtime cost of diffusion-based action generation. Its contribution is not that diffusion removes planning constraints or guarantees safe samples. Candidate quality, scoring, and the evaluation protocol still matter.

The venue year is 2025; the first preprint appeared in 2024. That distinction is useful when placing it alongside other recent planning papers.

<figure>
  <a href="{{ '/images/driving-papers/11.svg' | relative_url }}" style="width:100%;" aria-label="Open architecture diagram at full size"><img src="{{ '/images/driving-papers/11.svg' | relative_url }}" alt="Efficient and generative planning: VAD and DiffusionDrive: a comparison of the information passed between the methods' main stages." width="760" height="460" style="height:auto;" loading="lazy"></a>
  <figcaption>Original schematic of the methods discussed here; simplified information flow, not a reproduction of a paper's complete architecture.</figcaption>
</figure>

## The larger pattern: spend computation on the decision

The connection I draw between VAD and DiffusionDrive is economical representation. VAD makes the scene interface more compact; DiffusionDrive narrows the distribution from which trajectory refinement begins. Both use structure to reduce work that a more generic model would otherwise have to perform.

This structure can also limit generalization. A finite set of scene entities may miss unusual geometry. A set of action anchors may poorly cover an uncommon maneuver. These are useful places to inspect a model's failure cases rather than assuming that a larger network will automatically compensate.

| Design choice | Potential benefit | Corresponding limitation |
|---|---|---|
| Vectorized scene | Compact actor and road relationships | Omitted geometry is harder to recover |
| Multiple trajectory candidates | Preserve distinct possible actions | Candidates still require useful ranking |
| Anchored denoising | Shorter refinement process | The prior influences candidate coverage |

A fair comparison must report total computation: sensor encoding, scene reasoning, candidate generation, candidate scoring, and any final optimization. Decoder speed alone is not the latency of the driving system. Likewise, a stronger logged planning score cannot establish interactive behavior without an evaluation that exercises those interactions.

{% include perception-series-nav.html %}
