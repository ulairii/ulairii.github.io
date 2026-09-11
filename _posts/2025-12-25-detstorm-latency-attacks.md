---
title: 'Investigating Physical Latency Attacks Against Camera-Based Perception'
date: 2025-12-25
permalink: /posts/2025/12/detstorm-latency-attacks/
tags:
  - ai security
  - autonomous driving
series: paper-notes
---

In the rapidly evolving field of autonomous systems, visual perception is the cornerstone of safe navigation. A recent paper titled **"Investigating Physical Latency Attacks Against Camera-Based Perception"**, accepted to the 2025 IEEE Symposium on Security and Privacy (S&P), introduces a novel and concerning threat vector: **Detstorm**.

### The Problem: Latency as a Weapon
Denial-of-Service (DoS) attacks on autonomous vehicles (AVs) can be catastrophic. If an AV's perception system is delayed, even by a split second, it may fail to react to obstacles or pedestrians in time. Previous research into latency attacks has often been limited to:
*   **Digital-only attacks**: Simulations that cannot be easily replicated in the physical world.
*   **Unscalable physical patches**: Large, conspicuous patterns that block the camera's view, which are easily detectable and impractical to deploy discreetly.

The challenge was to create a *physically realizable* attack that could overwhelm the perception pipeline without requiring massive physical alterations to the scene.

### Proposed Method: Detstorm
The researchers propose **Detstorm**, a new attack method that exploits the computational bottlenecks in object detection pipelines.

#### 1. Concept
Detstorm works by flooding the object detector with a massive number of "ghost" adversarial objects. By forcing the system to process hundreds of non-existent detections, the pipeline's latency effectively creates a DoS condition.

#### 2. Design & Methodology
To achieve this in the real world, Detstorm uses **projector perturbations**—light patterns projected onto the scene. Key components of the design include:

*   **Evading NMS (Non-Maximum Suppression)**: Object detectors use NMS to filter out overlapping boxes for the same object. Detstorm optimizes its adversarial objects to specifically *evade* this filtering, ensuring that the system keeps as many false positives as possible.
*   **Zone Stitching**: Projecting a single coherent image that covers a large area is difficult. Detstorm uses a "zone stitching" process to recombine perturbation patterns into a single, contiguous image that can be projected physically and effectively.
*   **Greedy Zone Strategy**: The attack segments the environment into zones containing different object classes. It then employs a greedy algorithm to maximize the number of created objects within each specific zone.

### Effectiveness & Results
The paper presents rigorous evaluations in both simulated and real-world environments. The results are startling:
*   **506% increase** in the number of detected objects on average.
*   **Perception delays of up to 8.1 seconds**, which is an eternity in autonomous driving contexts.
*   The attack was proven to be physically realizable, capable of causing tangible consequences for real-world autonomous driving systems.

This research highlights a critical vulnerability in current perception architectures. As we move towards fully autonomous roads, defense mechanisms against not just misclassification, but *pipeline overload*, will be essential.

***
**Reference:**
R. Muller, R. Song, C. Wang, Y. Zhan, J.-P. Monteuuis, Y. Man, M. Li, R. Gerdes, J. Petit, and Z. B. Celik, "Investigating Physical Latency Attacks Against Camera-Based Perception," *2025 IEEE Symposium on Security and Privacy (S&P)*, 2025. DOI: [10.1109/SP61157.2025.00236](https://doi.org/10.1109/SP61157.2025.00236)
