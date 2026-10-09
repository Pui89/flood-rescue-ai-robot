# PUI89 Flood Rescue — Commercial Open-Source Stack

**Status:** integration specification and implementation backlog. Listing a component here does not mean its runtime adapter is already implemented, hardware-tested, or field-validated.

## Objective

Build a commercially maintainable flood-reconnaissance and rescue-support platform around measurable reliability, safe control, deployment flexibility, evidence traceability, and supportability—not model count.

## Recommended stack and integration boundaries

| Component | Proposed role | Integration boundary | Commercial notes |
|---|---|---|---|
| [DINOv2](https://github.com/facebookresearch/dinov2) | General-purpose visual features for retrieval, representation learning, scene similarity, and downstream classifiers | Optional visual-embedding adapter; compare against task-specific baselines | Check the exact checkpoint and all dependencies. Do not assume every derivative checkpoint has the same license. |
| [Anomalib](https://github.com/open-edge-platform/anomalib) | Visual anomaly detection for unfamiliar debris, damaged equipment, scene changes, or sensor artifacts | Optional anomaly score plus calibrated threshold and explicit UNKNOWN state | Validate on flood-specific data; anomaly scores are not victim detectors or safety guarantees. |
| [Open3D](https://github.com/isl-org/Open3D) | Point-cloud processing, geometry, registration, and 3D inspection tools | Mapping/geometry module behind sensor-frame and timestamp contracts | Confirm performance and memory on target hardware. |
| [ROS 2 Navigation2](https://github.com/ros-navigation/navigation2) | Navigation behaviors, planning, recovery, and navigation lifecycle | ROS 2 nodes/actions; keep safety monitor and E-stop independent | Select ROS 2 distribution and Nav2 package versions together; test all plugins and hardware drivers. |
| [ONNX Runtime](https://github.com/microsoft/onnxruntime) | Portable inference and optional hardware execution providers | Model export/validation path; preserve a reference implementation for parity tests | Benchmark accuracy, latency, memory, and supported operators on the target device before switching production inference. |
| [nvblox](https://github.com/nvidia-isaac/nvblox) | GPU-accelerated 3D reconstruction and distance/occupancy representations where compatible | Optional mapping backend; input/output adapters must declare frames, timestamps, resolution, and unknown-space policy | NVIDIA GPU/platform requirements and distribution terms must be checked for the selected release. |
| [Isaac ROS Visual SLAM](https://github.com/NVIDIA-ISAAC-ROS/isaac_ros_visual_slam) | Candidate visual-inertial localization in supported NVIDIA deployments | Optional localization backend, with health checks and fallback behavior | Review the exact repository, package, and redistribution license before commercial distribution. |
| Existing detector / segmenter | Task-specific victim, person, debris, and obstacle perception | Keep model behind a versioned perception interface | **Important:** Ultralytics YOLO code is AGPL-3.0 by default; proprietary/commercial deployments may require a commercial license. Confirm with counsel/vendor before shipping. |
| Existing multimodal models | Evidence summarization and mission-assessment proposals | Advisory-only service; structured output validated against schema | Model access, redistribution, use restrictions, and serving terms vary by model/version. |

No one component is a complete rescue solution. The commercial product is the verified end-to-end system, including integration, diagnostics, safe fallback, deployment, and support.

## Architecture contract

```text
Sensors + Calibration + Time Sync
            |
            v
Sensor Health / Data Quality Gate
            |
            v
Task Perception + Tracking -----> Optional DINOv2 embeddings
            |                     Optional Anomalib anomaly scores
            v
3D Mapping / Localization <----- Open3D / nvblox / approved SLAM backend
            |
            v
World Model + Uncertainty + UNKNOWN
            |
            v
Mission Proposal (AI is advisory)
            |
            v
Human / Mission Policy Review
            |
            v
Independent Deterministic Safety Monitor
            |
            v
ROS 2 / Nav2 / Authorized Controller
            |
            v
Action Verification + Evidence + Audit Log
```

### Non-negotiable safety rules

1. No vision-language model or VLA directly writes motor commands.
2. Emergency stop and the safety monitor must remain independent of network access and generative inference.
3. A missing, stale, contradictory, or out-of-calibration sensor must trigger a declared degraded/UNKNOWN state—not silently become a normal observation.
4. Unknown space is not free space. The robot must not infer traversability from absent data.
5. Navigation commands must pass collision, geofence/exclusion-zone, speed, stability, actuator-limit, and mission-policy checks.
6. Human confirmation is required for high-risk rescue interaction until the relevant capability has been specifically safety-validated.
7. Every mission records software/model/configuration versions, sensor health, timestamps, decisions, overrides, safety events, and final outcomes.

## Commercial implementation phases

### Phase 0 — License and compatibility gate

- Create a software bill of materials (SBOM) and dependency lockfiles.
- Record component version, commit/tag, license, model-weight terms, attribution obligations, redistribution constraints, and intended product use.
- Review hardware support, ROS 2 distribution compatibility, CUDA/runtime requirements, and model export operator support.
- Do not bundle weights or SDKs into commercial installers until redistribution rights are confirmed.

### Phase 1 — Perception adapters

- Add a DINOv2 embedding adapter only for tasks where an embedding baseline improves a measurable metric.
- Add Anomalib as a separate anomaly channel; do not merge its score into victim confidence without calibration.
- Preserve the current task-specific detector as a baseline.
- Test missing images, corrupted frames, low light, glare, rain, water reflections, motion blur, occlusion, and distribution shift.

### Phase 2 — 3D mapping and navigation

- Define canonical ROS 2 frame names, timestamp rules, sensor extrinsics, and map resolution.
- Benchmark Open3D and, on supported NVIDIA hardware, nvblox against a repeatable mapping dataset.
- Integrate Nav2 in simulation first; test localization loss, blocked routes, recovery loops, stale transforms, and communication loss.
- Use visual-inertial SLAM only after checking hardware compatibility and localization-failure behavior.
- Do not enable physical motion until independent stop, speed limiting, and collision checks are verified.

### Phase 3 — Portable inference

- Export one eligible model to ONNX.
- Compare reference and ONNX outputs on a fixed test set using agreed tolerances.
- Measure p50/p95 latency, throughput, peak memory, power, thermal throttling, and accuracy on target hardware.
- Keep fallback inference and a rollback mechanism.

### Phase 4 — Product operations

- Fleet/robot registry, authenticated device identity, signed releases, secure update/rollback, and least-privilege credentials.
- Mission dashboard with robot health, sensor health, battery, localization confidence, current map, uncertainty, and operator overrides.
- Append-only event history and exportable mission evidence package.
- Offline operation and store-and-forward telemetry for poor-connectivity environments.
- Support runbooks, logs with secrets redacted, diagnostic bundle export, and defined update/support policy.

### Phase 5 — Release gate

Release only when the target configuration passes the benchmark suite, fault-injection suite, security review, operator acceptance, and field-trial approval. A documentation entry or passing simulation is not evidence of field readiness.

## Required benchmark matrix

| Area | Metrics |
|---|---|
| Victim/person detection | Precision, recall, F1, AP by visibility condition, false alarms per hour |
| Localization | Median and p95 position error, coordinate frame, distance, and confidence calibration |
| Tracking | ID switches, track fragmentation, reacquisition time |
| Anomaly detection | AUROC/AUPRC where meaningful, false alarm rate, missed anomaly rate, threshold calibration |
| Mapping | Map completeness, geometric error, obstacle/free-space consistency, map update latency |
| Localization/navigation | Localization error, mission completion, collision count, recovery success, operator interventions |
| Runtime | p50/p95 latency, FPS, CPU/GPU utilization, RAM/VRAM, power, thermal behavior |
| Resilience | Sensor dropout recovery, stale-data rejection, network-loss behavior, restart and rollback success |
| Safety | E-stop response, stop distance under defined conditions, geofence violations, safety-gate rejection tests |
| Commercial operations | Mission uptime, mean time to recover, maintenance hours, cost per mission, reproducibility |

Every result must include dataset/scenario ID, hardware, software commit, model/checkpoint hash, configuration, number of trials, failure cases, and confidence intervals where appropriate. Do not publish target values as achieved results.

## Suggested configuration

See [`config/open_source_stack.yaml`](../config/open_source_stack.yaml). Optional components are disabled by default until their adapter, license review, and validation gate are complete.
