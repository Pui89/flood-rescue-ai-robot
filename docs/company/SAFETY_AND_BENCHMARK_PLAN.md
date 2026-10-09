# Pui89 AI Robotics — Safety and Benchmark Plan

**Purpose:** make progress measurable and prevent research demos from being mistaken for field-ready systems.

## Evidence levels

- **L0 — Design:** architecture or requirement documented.
- **L1 — Unit-tested:** isolated functions pass automated tests.
- **L2 — Simulation-tested:** repeatable simulator scenarios pass.
- **L3 — Hardware-in-the-loop:** real compute/sensors/controllers tested without hazardous autonomous operation.
- **L4 — Controlled physical trial:** supervised test in a controlled environment.
- **L5 — Pilot evidence:** documented trial with a real user, acceptance criteria, incident process, and operational limits.

Every README and demo should label its evidence level. Do not describe a capability as field-validated unless the evidence supports it.

## Required safety boundary

1. Validate sensor timestamps, calibration state, data freshness, and health.
2. Reject malformed, stale, out-of-range, or contradictory inputs.
3. Treat AI/VLM/VLA outputs as proposals, not actuator authority.
4. Validate proposed tasks against geofences, robot limits, collision checks, speed limits, and operator permissions.
5. Use an independent emergency stop and hardware watchdog where applicable.
6. Define safe behavior for sensor loss, compute overload, low battery, communication loss, and localization failure.
7. Require operator confirmation for high-consequence actions.
8. Log the request, evidence, decision, safety checks, result, and software/model versions.
9. Test safe-stop behavior on the actual hardware before enabling motion.
10. Conduct hazard analysis and seek qualified independent review before field deployment.

Software checks alone do not certify a robot as safe.

## Benchmark protocol

Every result must record:
- Git commit and dirty/clean working-tree status.
- Dataset version, split, license/consent provenance, and exclusions.
- Model weights and configuration hashes.
- Hardware, OS, ROS 2 distribution, runtime versions, power mode, and sensor configuration.
- Warm-up policy, run count, repetitions, and confidence intervals where meaningful.
- Evaluation script version and raw machine-readable output.
- Known limitations, failed cases, and any manual intervention.

Never train on the test split. Keep a held-out test set and report uncertainty or variation rather than one cherry-picked run.

## Perception metrics

- Precision, recall, F1, per-class metrics, and mAP where applicable.
- False-positive and false-negative rates at a stated threshold.
- Performance by lighting, weather, distance, occlusion, and sensor configuration.
- Calibration and abstention/OOD performance where relevant.
- Latency percentiles (p50/p95/p99), throughput, memory, power, and thermal behavior.

## Spatial and navigation metrics

- Localization error against a stated reference.
- Mapping completeness/consistency.
- Task completion rate across predefined scenarios.
- Collision and near-miss counts.
- Emergency-stop and recovery behavior.
- Human intervention rate.
- Communications-loss and sensor-failure recovery.
- Energy consumed per task where measurable.

## RescueBot scenarios

Begin in simulation and dry controlled environments; do not use live floodwater or real rescue victims as an initial test environment.

- Static and moving obstacles.
- Reflective/wet surfaces and visually confusing scenes.
- Water-edge exclusion zones.
- Human/animal/vehicle detections with explicit false-alarm analysis.
- RGB-D or LiDAR dropout.
- Sensor time skew and stale frames.
- Localization degradation.
- Lost network and delayed commands.
- Low battery and compute overload.
- Emergency-stop activation and restart authorization.

Initial release criteria must be set before each benchmark. Publish measured results, including failures, rather than inventing target achievements after the test.

## AgriBot scenarios

- Different coconut sizes, maturity labels, lighting, backgrounds, and occlusions.
- Height and 3D localization error.
- False detection and missed detection rates.
- Wind and foliage movement.
- Arm reachability and collision checks in simulation.
- Gripper/tool success and failure rates only when physical testing exists.
- Human exclusion zone, emergency stop, and safe recovery tests.

Do not test an autonomous cutter or elevated manipulator around people before a qualified risk assessment and controlled safety validation.

## SecureBot limitations

- Treat model outputs as anomaly-screening hypotheses, not proof of drug identity.
- Cameras, thermal, NIR, depth, and LiDAR alone must not be represented as reliable chemical identification without a validated physical sensing method and suitable reference data.
- Use human review, audit trails, and explicit abstention.
- Measure false positives, false negatives, subgroup/environmental variation, calibration, and reviewer disagreement.
- Do not autonomously accuse, restrain, seize property, or trigger enforcement based on model output.

## Release checklist

- [ ] Unit and integration tests pass.
- [ ] Simulation benchmark is reproducible.
- [ ] Safety failure modes are documented and tested.
- [ ] Model and data licenses are reviewed.
- [ ] Secrets and private data are excluded.
- [ ] SBOM and dependency vulnerability report are generated.
- [ ] Limitations and evidence level are visible in documentation.
- [ ] Hardware tests and operator instructions exist before physical deployment.
