# PhD Research Program — Trustworthy Autonomous Flood-Rescue Robotics

## Research thesis

**How can a multimodal rescue robot maintain a trustworthy 4D understanding of a rapidly changing flood environment and make safe, uncertainty-aware rescue decisions under sensor degradation, communication loss, dynamic hazards, and limited human attention?**

This is a research direction, not a claim that the current repository has already answered the question.

## Central contribution

Build and experimentally validate a **Trustworthy 4D Rescue World Model (T4D-RWM)** that fuses heterogeneous sensing, tracks victims/hazards over time, predicts short-horizon scene evolution, quantifies uncertainty, detects out-of-distribution conditions, and converts those estimates into risk-aware mission decisions.

The important research contribution is the **closed loop from uncertainty to action**:

perception -> temporal world state -> prediction -> uncertainty/OOD -> rescue utility/risk -> action -> outcome -> belief update.

## Research questions

1. Can temporal multimodal fusion reduce victim/hazard localization error compared with single-frame or single-sensor systems?
2. Can calibrated uncertainty and explicit abstention reduce unsafe autonomous decisions under sensor degradation?
3. Can short-horizon prediction improve route selection in moving water, debris and dynamic-obstacle scenarios?
4. Can risk-aware active perception decide when the robot should reposition sensors rather than commit to a low-confidence rescue action?
5. Can a human-aware autonomy policy reduce operator workload while preserving rescue safety and mission success?

## Hypotheses

- H1: temporal multimodal fusion improves localization and tracking robustness under partial sensor failure.
- H2: uncertainty-aware abstention lowers unsafe-action rate at an acceptable mission-success cost.
- H3: predictive world modeling improves time-to-victim and route success in dynamic flood scenarios.
- H4: active perception reduces unnecessary motion and human interventions by acquiring information only when it changes a decision.
- H5: risk-aware human-robot teaming improves safety-adjusted rescue utility versus fully manual or fully autonomous baselines.

## Experimental design

Compare progressively stronger systems:

A. RGB detector + reactive navigation  
B. RGB-D/LiDAR fusion + tracking  
C. 4D world model  
D. 4D world model + uncertainty/OOD  
E. D + predictive planning  
F. E + active perception  
G. F + human-aware autonomy

Primary outcomes:
- victim localization error;
- track continuity;
- route success;
- time-to-victim;
- rescue success;
- unsafe-action rate;
- collision / near-miss rate;
- false/missed victim alerts;
- intervention rate;
- calibration error;
- energy per successful mission;
- compute/latency;
- degradation recovery time.

Every experiment must be repeated across seeds and scenario families, with held-out environments and failure cases.

## Evaluation matrix

Vary:
- daylight/night;
- heavy rain and spray;
- fog/smoke-like visibility degradation;
- glare/reflections;
- moving water;
- floating debris;
- partially submerged objects;
- occluded victims;
- sensor dropout and timestamp skew;
- GNSS degradation/denial;
- communication latency/dropout;
- changing terrain;
- unseen buildings/vegetation;
- different robot payloads and battery states.

## Reproducibility

Record dataset version, scenario seed, model/checkpoint, Git SHA, calibration version, hardware, ROS/software versions, latency, power, sensor health and all safety-gate decisions.

## Publication strategy

Potential papers:
1. multimodal 4D rescue world model;
2. uncertainty/OOD-aware rescue decision making;
3. predictive risk-aware navigation under dynamic flood hazards;
4. active perception for autonomous rescue;
5. human-aware rescue autonomy and operator workload.

The strongest PhD story is one coherent system and evaluation framework, not five unrelated model integrations.

## What would make the thesis genuinely novel

The contribution must beat credible baselines on a **held-out disaster benchmark** and demonstrate that uncertainty changes behavior safely. A paper is not strengthened merely by adding a larger VLM or more model names.

The repository should eventually release:
- benchmark specification;
- anonymized/consented dataset or dataset-generation pipeline;
- scenario definitions;
- evaluation scripts;
- model cards;
- failure taxonomy;
- reproducible experiment manifests;
- safety and ethics protocol.
