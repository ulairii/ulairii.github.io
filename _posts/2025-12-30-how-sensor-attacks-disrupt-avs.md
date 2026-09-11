---
title: "SoK: How Sensor Attacks Disrupt Autonomous Vehicles: An End-to-end Analysis, Challenges, and Missed Threats"
date: 2025-12-30
permalink: /posts/2025/12/sok-sensor-attacks-avs/
tags:
  - ai security
  - autonomous driving
series: paper-notes
---

Autonomous vehicles (AVs)—including self-driving cars, robots, and drones—rely heavily on multi-modal sensor pipelines to operate safely. However, these sensors are known to be vulnerable to adversarial attacks. A major gap in current research is the lack of a systematic ecosystem view: how exactly do sensor-induced errors propagate through the interconnected modules of an AV to eventually cause physical harm?

A new paper titled **"SoK: How Sensor Attacks Disrupt Autonomous Vehicles: An End-to-end Analysis, Challenges, and Missed Threats"** aims to bridge this gap.

## The Gap: From Sensor Error to Physical Impact

Existing research often focuses on compromising a single sensor or algorithm. This paper takes a step back to provide a comprehensive survey and analysis across different platforms, sensing modalities, and attack methods.

## The Framework: Modeling Error Propagation

At the core of this paper is a graph-based framework designed to map the journey of an attack:
1.  **Injection:** How attacks inject errors into the system.
2.  **Propagation:** The conditions under which these errors travel through modules—from perception and localization to planning and control.
3.  **Impact:** When and how these errors manifest as physical consequences.

## Key Findings & Missed Threats

Through this systematic analysis, the authors uncovered significant insights:

*   **8 Key Findings:**
    1.  **Perception Sensitivity:** Attacks on perception sensors often require minimal physical impact to cause system failure.
    2.  **Localization Drift:** Localization sensors are susceptible to attacks that induce small, cumulative errors leading to significant deviations over time.
    3.  **Fusion Vulnerability:** Attacks targeting sensor fusion modules can be highly effective by exploiting inconsistencies between different sensor modalities.
    4.  **Context Dependency:** The propagation of sensor-induced errors is highly dependent on the AV's operational context and environmental conditions.
    5.  **Redundancy Bypass:** Redundancy in sensing and processing can be bypassed by sophisticated attacks that understand the system's failover logic.
    6.  **ML Black-Boxes:** Machine learning components within the pipeline are major targets due to their black-box nature and sensitivity to input perturbations.
    7.  **Indirect Control Impact:** Attacks on the planning and control modules, although less direct, can cause dangerous physical actions by exploiting model inaccuracies.
    8.  **Testing Gaps:** End-to-end testing and validation are crucial but often insufficient to uncover complex attack vectors involving multiple system components.

*   **12 Missed Threats:**
    1.  **Multi-sensor Coordination:** Multi-sensor coordinated attacks that exploit cross-modal dependencies.
    2.  **Physical Environment:** Attacks leveraging the physical environment to manipulate sensor readings (e.g., reflections, occlusions).
    3.  **Temporal Dynamics:** Attacks exploiting the temporal dynamics of sensor data and system processing.
    4.  **Adversarial ML on Fusion:** Adversarial machine learning attacks specifically targeting sensor fusion algorithms.
    5.  **Edge Cases:** Attacks exploiting edge cases and corner cases in perception and planning algorithms.
    6.  **Communication Channels:** Attacks targeting communication between AV modules or between AV and infrastructure.
    7.  **Subtle Degradation:** Attacks that induce subtle, long-term degradation of system performance rather than immediate failure.
    8.  **Human Interaction:** Exploitation of human-in-the-loop systems and their interaction with the AV.
    9.  **Side-channels:** Attacks leveraging side-channel information (e.g., power consumption, EM emissions) to infer system state or inject faults.
    10. **Learning Mechanisms:** Attacks against the AV's learning and update mechanisms, poisoning data or models.
    11. **Multi-AV Interaction:** Exploiting the interaction between multiple AVs or between AVs and other road users.
    12. **Simulation Exploits:** Attacks targeting simulation environments used for AV testing and a false sense of security.

This Systematization of Knowledge (SoK) serves as a critical wake-up call and a roadmap for future defense strategies, emphasizing that securing individual sensors is not enough—we must secure the entire pipeline.

[Read the full paper on arXiv](https://arxiv.org/abs/2509.11120)
[Download PDF](https://arxiv.org/pdf/2509.11120)
