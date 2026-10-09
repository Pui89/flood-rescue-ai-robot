# Reproducible Benchmarks and Next-Stage Build Plan

Status: evaluation tooling and protocol; not evidence of field readiness.

## Current engineering gap

The architecture names advanced perception, multimodal reasoning, world models and navigation components. The hard proof is whether the full system works in repeatable scenarios, under sensor degradation, with measured latency and fail-safe behavior. Model names and architecture diagrams are not benchmark results. No result should be called field validated until the dataset, hardware, configuration, run date and repeated trials are published.

## Added benchmark metadata gate

The standard-library validator at `tools/validate_benchmark_report.py` rejects incomplete provenance, placeholder text, invalid timestamps and non-numeric/non-finite metric values.

```bash
python tools/validate_benchmark_report.py benchmarks/reports/example.json
pytest -q tests/test_benchmark_report_validator.py
```

The validator checks report structure only. It does not certify the truth of a metric, model quality, dataset quality or robot safety. Store actual reports under `benchmarks/reports/`; never commit invented results. Include the exact Git commit and model checkpoint hash in the report when available.

## Minimum scenario matrix

| Scenario | Required measurement |
|---|---|
| Clear daylight / baseline | victim detection precision, recall, F1; localization error |
| Rain, glare, low light, partial occlusion | per-condition recall and false-positive rate |
| Thermal-only or RGB-only degradation | detection quality and safe degradation behavior |
| Sensor dropout / stale timestamps | time to detect fault; safe-stop or hold behavior |
| GNSS-denied environment | localization drift, map consistency, mission completion |
| Blocked route / moving obstacle | collision count, minimum clearance, replanning latency |
| Network loss / delayed commands | watchdog response, stale-command rejection |
| Unknown object or uncertain victim | abstention rate and human-review trigger correctness |
| Repeated mission trials | completion rate, recovery rate, intervention count |
| Edge hardware | p50/p95 latency, FPS, peak RAM/VRAM, power draw |

Report each scenario separately; an aggregate score must not hide failures in the worst conditions. Use simulation first, controlled benign field trials second, and operational deployment only after independent safety review.

## Open-source stack to evaluate

Verify the exact version and license of every dependency before product distribution; transitive dependencies and model weights can have different terms.

- ROS 2 (Apache-2.0): https://github.com/ros2/ros2 — middleware, lifecycle nodes and integration boundary.
- Navigation2 (Apache-2.0): https://github.com/ros-navigation/navigation2 — navigation and recovery behaviors.
- Gazebo Sim (Apache-2.0): https://github.com/gazebosim/gz-sim — simulation and sensor/physics scenarios.
- MoveIt 2 (BSD-3-Clause): https://github.com/moveit/moveit2 — manipulation planning where an arm is present.
- Open3D (MIT): https://github.com/isl-org/Open3D — point clouds, geometry and 3D inspection.
- FiftyOne (Apache-2.0): https://github.com/voxel51/fiftyone — dataset curation, error analysis and slice evaluation.
- DVC (Apache-2.0): https://github.com/iterative/dvc — dataset/versioned experiment references.
- MLflow (Apache-2.0): https://github.com/mlflow/mlflow — experiment and artifact tracking.
- Cyclone DDS (EPL-2.0 or Apache-2.0, see project licensing): https://github.com/eclipse-cyclonedds/cyclonedds — ROS 2 DDS middleware option.
- OpenSSF Scorecard (Apache-2.0): https://github.com/ossf/scorecard — repository supply-chain posture checks.

Use these as candidates, not as a claim they are already integrated. For production, pin versions, scan dependencies, track model/data licenses, and generate an SBOM.

## Safety and release gates

1. No language model or learned policy directly bypasses a deterministic motion supervisor.
2. Emergency stop, watchdog, stale-message rejection and collision limits must be tested independently of the AI pipeline.
3. Fault-injection tests must prove safe behavior when sensors disagree, disappear or become stale.
4. Simulation success is not physical validation. Record sim-to-real gaps and repeat tests on the target hardware.
5. Never test flood mobility, water ingress or rescue manipulation around people without an independently reviewed test plan.

## Next implementation sequence

1. Build a frozen, versioned scenario set with held-out scenes and documented annotation policy.
2. Record ROS 2 bags or simulation episodes with synchronized timestamps and calibration metadata.
3. Add adapters and lifecycle/health monitoring for each physical sensor; make missing or stale inputs explicit.
4. Connect Nav2 and Gazebo through a simulation-first bring-up profile; test stop/recovery behavior.
5. Add benchmark report artifacts to CI and require human review for regressions in safety-critical slices.
6. Publish a model card, dataset card, failure taxonomy, test report and hardware bill of materials before claiming commercial readiness.

## Report template

A report must include `schema_version`, `project`, `run_id`, timezone-aware `run_date_utc`, `dataset{name,version,split}`, `model{name,version}`, `hardware{platform}`, `software{os,python}`, `config{seed}` and numeric `metrics`. Include metric definitions and confidence intervals in the accompanying report narrative when sample size permits.
