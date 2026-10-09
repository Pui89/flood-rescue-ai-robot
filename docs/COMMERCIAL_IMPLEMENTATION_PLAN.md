# PUI89 Flood Rescue AI Robot — Commercial Implementation Plan

**Target hardware:** NVIDIA Jetson Orin family, with AGX Orin as the high-compute reference platform  
**Initial product:** supervised autonomous flood reconnaissance and hazard mapping  
**Release posture:** edge AI decision support and mapping first; no autonomous entry into moving/deep water or physical victim extraction in the first commercial release  
**Status:** implementation plan, not evidence that planned modules are already implemented or field validated

## 1. Product definition

### First product to sell

**PUI89 Flood Recon** is an edge-deployed robot payload/software system that surveys a bounded flood-affected area, builds a robot-frame or georeferenced hazard map, identifies possible people and obstacles, reports uncertainty and sensor health, and exports an auditable mission report for an operator.

The first release should prioritize:
- live and recorded RGB/RGB-D input, with optional thermal and LiDAR where supported;
- person/object candidate detection and tracking;
- obstacle, water-edge, debris, blocked-route, and unknown-area annotations, distinguishing observed evidence from inferred hazards;
- local 3D mapping and robot pose when compatible sensors are available;
- operator-supervised route suggestions and safe-stop behavior;
- offline-first operation with local mission storage and delayed upload;
- a mission report containing maps, time-stamped observations, model/configuration versions, uncertainties, incidents, and operator actions.

The first release should **not** claim validated victim rescue, safe autonomous navigation through floodwater, reliable water-depth estimation from RGB alone, all-weather performance, certified life-safety performance, or untested waterproofing. Treat water boundaries, current, depth, debris stability, and traversability as uncertain unless independently measured by suitable sensors.

### Buyers and initial use cases

- emergency-management teams conducting reconnaissance from a safe, controlled boundary;
- municipal and infrastructure teams inspecting flooded roads, facilities, and access routes;
- research and training organizations running repeatable flood-response exercises.

Sell the initial capability as **reconnaissance and hazard-mapping support**, not a replacement for trained responders.

## 2. Recommended system architecture

    RGB / RGB-D / Thermal / LiDAR / IMU / GNSS (if available)
                             |
                   Calibration + Time Sync
                             |
                 Sensor Health / Quality Gate
                             |
           Person / Object / Hazard Candidate Perception
               |                             |
       DINOv2 embeddings (optional)    Anomalib score (optional)
               |                             |
               +---- Evidence association ---+
                             |
             Localization + 3D Mapping Backend
           Open3D tools / optional nvblox or SLAM
                             |
              Versioned 3D/4D Mission World Model
                             |
          Uncertainty / Stale Data / UNKNOWN State
                             |
             Hazard Map + Route Proposal + Evidence
                             |
              Operator / Mission Policy Approval
                             |
           Independent Deterministic Safety Monitor
                             |
           ROS 2 / Nav2 (only after integration gate)
                             |
                  Authorized robot interface
                             |
           Verification / Audit / Mission Report

A learned model may propose a detection, semantic label, anomaly score, or summary. It must not be the sole authority for whether terrain is safe, whether water is traversable, or whether an actuator may move. Keep the emergency stop and safety control path independent of foundation-model inference and cloud/network connectivity.

## 3. Commercially usable component shortlist

Licenses below describe the main repository license or commonly published code license, not a blanket legal conclusion about every model weight, dataset, dependency, container, or hardware SDK. Before shipping, pin an exact commit/release and archive its license files and notices in an SBOM.

| Component and exact upstream | License / commercial assessment | PUI89 use | Decision |
|---|---|---|---|
| [Open3D](https://github.com/isl-org/Open3D) | MIT for the main project; review bundled third-party components | Point-cloud utilities, geometry, registration, offline map inspection | **Adopt first** for geometry tooling |
| [ONNX Runtime](https://github.com/microsoft/onnxruntime) | MIT for the main project; execution providers and included runtimes have their own dependencies/terms | Portable inference path and repeatable model parity tests | **Adopt after baseline is measured** |
| [DINOv2](https://github.com/facebookresearch/dinov2) | Main code/model release states Apache-2.0; verify exact checkpoint and derivative weights | Optional embeddings for image retrieval, visual similarity, and downstream hazard classifier experiments | **Optional experiment**, not a required runtime dependency |
| [Anomalib](https://github.com/open-edge-platform/anomalib) | Apache-2.0 for repository; individual checkpoints/datasets/dependencies still need review | Separate anomaly channel for unusual debris/scene changes/sensor artifacts | **Optional experiment** after flood-domain validation |
| [ROS 2](https://github.com/ros2/ros2) and [Navigation2](https://github.com/ros-navigation/navigation2) | ROS/Nav2 packages can have different licenses; inspect each package.xml and license. Nav2 lists Apache-2.0, BSD-3-Clause and LGPL-2.1-or-later portions | Navigation lifecycle, planners, behaviors, recovery; only when a real robot interface exists | **Later stage**, simulation first |
| [nvblox](https://github.com/nvidia-isaac/nvblox) | Review exact tag/commit and all bundled third-party code; licensing may differ by branch/component | Optional GPU-accelerated RGB-D mapping on compatible NVIDIA stack | **Conditional**; legal and compatibility gate before distribution |
| [Isaac ROS Visual SLAM](https://github.com/NVIDIA-ISAAC-ROS/isaac_ros_visual_slam) | Review exact package and redistribution terms | Optional visual-inertial localization if camera/IMU and release compatibility are validated | **Conditional** |
| [Ultralytics](https://github.com/ultralytics/ultralytics) | AGPL-3.0 by default; a separate commercial license is offered. Proprietary product distribution needs a deliberate legal decision | Existing detector baseline if currently used | **Resolve license before commercial shipping** |
| [PyTorch](https://github.com/pytorch/pytorch) | BSD-style license for main project; bundled libraries/checkpoints have separate notices | Training and reference inference where compatible with JetPack | Keep as dev/reference path; don't assume desktop wheels work on Jetson |
| [OpenCV](https://github.com/opencv/opencv) | Apache-2.0 for OpenCV 4.x main project; separately review contrib modules/build options | Image/video I/O, transforms, overlays | Keep and pin the chosen build |
| [Cyclone DDS](https://github.com/eclipse-cyclonedds/cyclonedds) | Verify selected release and package terms | ROS 2 middleware candidate if required by selected ROS distribution | Use ROS distribution's supported default first |

### License controls

1. **Do not infer model-weight licensing from source-code licensing.** Record source, weights, datasets, tokenizer/config files, export artifacts, and inference runtime separately.
2. For every distributed component, store name, version/tag, commit SHA, source URL, SPDX expression, license file, notices, whether source is modified, whether weights are redistributed, and legal approval.
3. Keep a third-party notices bundle and generate an SBOM (for example CycloneDX/SPDX) for each release.
4. Never redistribute NVIDIA SDKs, containers, model weights, or other assets until their exact distribution terms are checked.
5. For Ultralytics-based models, decide between compliance with AGPL obligations and a commercial license before packaging proprietary software. This plan is engineering guidance, not legal advice.

## 4. Jetson Orin deployment strategy

### Reference hardware profiles

| Profile | Role | Design intent |
|---|---|---|
| Jetson Orin NX / Orin family module | Lower-cost edge pilot if present in the intended onboard range | Small detector, tracking, sensor-health checks, compact local map; defer large multimodal models to operator workstation/cloud if needed |
| Jetson AGX Orin | Reference onboard compute target | Concurrent perception, mapping, telemetry, local visualization/API where memory and thermal tests allow |
| External operator workstation | Optional, not safety-critical | Training, dataset review, heavy multimodal analysis, report generation, offline replay |

The exact Jetson module, RAM capacity, carrier board, JetPack/L4T release, CUDA/TensorRT versions, camera drivers, and sensor interfaces must be recorded before choosing binary packages. “Jetson Orin” alone is not a sufficient deployment target.

### Deployment rules

- Pin a tested JetPack/L4T release and build an immutable container/image for that release. Do not assume a desktop CUDA/PyTorch wheel is compatible with Jetson.
- Use vendor-supported TensorRT or ONNX Runtime execution providers only after output-parity tests. Keep a reference inference path.
- Measure sustained performance, not a short FPS burst: CPU/GPU utilization, RAM/VRAM, input/output latency, board power, temperature, throttling, and dropped frames.
- Test the complete sensor and compute stack in the actual enclosure. Water ingress, condensation, vibration, heat rejection, connector sealing, and battery brownout are hardware qualification tasks, not solved by AI code.
- Set bounded queues and an explicit stale-frame policy. Dropping an old camera frame is preferable to acting on stale data without warning.
- Keep the safety supervisor and emergency-stop path able to stop or inhibit motion when the inference process crashes or hangs.
- Default to offline operation; remote connectivity is for optional telemetry, not for the local safety loop.

Official Jetson reference: [Jetson Linux Developer Guide — Platform Power and Performance](https://docs.nvidia.com/jetson/archives/r39.2/DeveloperGuide/SD/PlatformPowerAndPerformance.html). Thermal behavior and throttling should be included in sustained-load tests.

## 5. Proposed repository implementation map

Paths marked **existing** are known repository files. Paths marked **planned** are recommended additions; create them in small, reviewable commits.

| File | Status | Responsibility |
|---|---|---|
| flood_robot/pipeline/rescue_pipeline.py | Existing import in demo | Keep as orchestration; delegate to small components instead of embedding all logic here |
| flood_robot/world_model.py | Existing | Versioned mission state, object observations, timestamps and provenance; extend with hazard-map records and validation as needed |
| flood_robot/config.py | Existing import in demo | Load validated configuration; no secrets in YAML |
| scripts/run_demo.py | Existing | Recorded/webcam demo; add a separate hardware entry point rather than making the demo issue robot commands |
| config/open_source_stack.yaml | Added in PR | Optional component manifest; components remain disabled until tests and license gates pass |
| config/flood_recon.yaml | Planned | Sensor IDs, frames, rates, thresholds, map resolution, stale-data limits, model IDs and runtime profile |
| flood_robot/sensors/contracts.py | Planned | Typed sensor sample, timestamp, calibration ID, health and provenance contracts |
| flood_robot/sensors/health_gate.py | Planned | Missing/stale/corrupt frame detection, clock skew checks, degraded-state emission |
| flood_robot/perception/interfaces.py | Planned | Model-agnostic detection/segmentation/embedding interface and typed outputs |
| flood_robot/perception/dinov2_adapter.py | Planned | Optional feature extraction; no hard dependency in core install |
| flood_robot/perception/anomaly_adapter.py | Planned | Optional Anomalib inference; returns a distinct anomaly result, not a victim score |
| flood_robot/mapping/interfaces.py | Planned | Map backend contract, coordinate frame and unknown-space semantics |
| flood_robot/mapping/open3d_backend.py | Planned | Offline point-cloud operations and mapping evaluation utilities |
| flood_robot/mapping/nvblox_backend.py | Planned, conditional | GPU backend behind optional dependency and platform guard |
| flood_robot/hazards/schema.py | Planned | Hazard type, geometry, evidence, uncertainty, severity, source, timestamp and expiry |
| flood_robot/hazards/fusion.py | Planned | Fuse evidence without silently converting anomaly scores into certainty |
| flood_robot/safety/supervisor.py | Planned if not already present | Deterministic command allowlist, hold/stop states, health gates and reason codes |
| flood_robot/telemetry/mission_log.py | Planned | Structured append-only event records, redaction and evidence provenance |
| scripts/jetson_preflight.py | Planned | Record device/runtime versions, available memory, model load status, sensor readiness and thermal telemetry |
| scripts/benchmark_flood_recon.py | Planned | Reproducible replay benchmark from a versioned dataset manifest |
| tests/unit/ | Planned organization | Schema, health, fusion, uncertainty and policy unit tests |
| tests/integration/ | Planned organization | Pipeline, adapter, mapping and evidence integration tests |
| tests/fault_injection/ | Planned organization | Sensor loss, stale frames, clock skew, process crash and network failure |
| benchmarks/flood_recon_v1.yaml | Added in PR | Scenario/metric protocol, not measured results |

Before adding a path, check the branch for an existing equivalent and extend it rather than creating duplicate implementations.

## 6. Integration order

### Step A — Baseline and reproducibility

1. Record current main commit and run the existing test suite on a supported development environment.
2. Save a baseline report for current demo throughput, detection output, memory, and known failure modes.
3. Create a small versioned dataset manifest with location/mission-separated train, validation and test partitions.
4. Add schema validation for configuration and mission event records.
5. Do not alter production inference and hardware control in the same commit.

### Step B — Sensor contracts and health gate

Implement sensors/contracts.py and sensors/health_gate.py. Every sample should include:
- sensor ID and modality;
- capture timestamp and monotonic receive timestamp;
- coordinate frame and calibration/configuration ID;
- dimensions/encoding or point-cloud schema;
- health state and explicit reason code;
- source file/sequence ID for replay.

Reject impossible dimensions, malformed data, stale timestamps, invalid calibration references, and out-of-order frames according to configurable policy. If a critical modality is missing, expose DEGRADED or UNKNOWN to the world model and UI.

### Step C — Perception adapters

Define a stable output schema for detections: class, score, bounding geometry, optional mask, frame ID, timestamp, model version and provenance. Keep DINOv2 embeddings and Anomalib scores in separate fields. Establish per-sensor baselines before attempting multimodal fusion.

Use deterministic post-processing and calibrated thresholds. The anomaly model may flag an unfamiliar region for review; it must not automatically label the region as a person, a safe route, or a dangerous route.

### Step D — Mapping and hazard layer

Start with offline/replay map evaluation using Open3D tools. Add a GPU mapping backend only if the selected Jetson/JetPack combination supports it and a measured benchmark justifies the added complexity.

Each hazard record should include:
- stable ID and hazard type (debris, blocked_route, water_edge_candidate, obstacle, unknown_region, etc.);
- geometry and coordinate frame;
- observed vs inferred status;
- timestamp, expiry/staleness and evidence references;
- confidence/uncertainty and supporting sensors;
- severity rubric and reviewer status.

A water-edge candidate is not a measured water depth or current. The system should show unknown regions distinctly and avoid marking unseen space as free.

### Step E — Mission report and operator workflow

Produce a local report with:
- mission ID, robot/device ID, timestamps and operator;
- map and route trace;
- hazard records with evidence thumbnails/frames;
- sensor-health gaps and localization confidence;
- model/checkpoint hashes, config hash and software commit;
- interventions, safety stops, failures, recovery actions;
- explicit limitations and unobserved regions.

Store locally first, use bounded storage and safe log rotation, and synchronize only after authenticated connection is available. Do not put secrets or unnecessary personal data into the report.

### Step F — Navigation integration (later)

Only after perception, mapping, health-gate and report layers pass their gates:
1. Choose a supported ROS 2 distribution compatible with the selected JetPack.
2. Integrate Nav2 in simulation using a declared robot model and realistic sensor topics.
3. Add localization-health checks, collision monitor, speed limits, geofence/exclusion zones, battery policy and stop conditions.
4. Test the stop path with the inference node killed, GPU inference stalled, localization lost, and network disconnected.
5. Start hardware-in-the-loop on a dry, controlled test course. Do not test autonomous navigation in moving floodwater as a first field trial.

## 7. Benchmark protocol and proposed release targets

The benchmark manifest in benchmarks/flood_recon_v1.yaml is the canonical protocol. It contains **proposed acceptance targets**, not current results. Tune thresholds to the risk assessment and customer requirements before a formal release.

| Metric | Why it matters | Suggested initial gate |
|---|---|---|
| Hazard/person candidate recall | Missed observations can mislead operators | Set per-class targets from annotated validation set; publish confidence intervals and false alerts |
| False alerts | Too many alerts can overload responders | Report false alerts per hour and per mapped area; set acceptance limit with users |
| Localization/map error | A map that is spatially wrong is unsafe to rely on | Report median and p95 against ground truth; use a target course and independent reference |
| End-to-end latency | Stale perception can invalidate a map | Measure capture-to-published-result p50/p95 under sustained load |
| Dropped/stale frames | Hidden data loss creates false confidence | Every drop/stale frame must be counted and surfaced; no silent stale output |
| Map completeness | Unobserved space must remain explicit | Report observed coverage and unknown area separately |
| Recovery | System must handle process and sensor faults | Every injected critical fault must enter a declared safe/degraded state |
| Thermal/power stability | Edge devices run under constrained power and cooling | Sustained workload test in final enclosure; no uncontrolled reset or silent throttling |
| Safety-gate tests | Safety must be testable without model quality | All defined invalid-command, stale-data, E-stop and lost-localization tests pass |
| Reproducibility | Commercial support requires repeatability | Same manifest/config produces comparable outputs; record commit, hardware, model hashes |

Use scenario groups: daylight, dusk/low light, rain/wet reflections, glare, occlusion, debris, flooded road edge, missing modality, timestamp skew, localization degradation, compute overload, battery warning, communication loss, reboot/recovery and unknown environment. Split data by site/mission/time to avoid leakage.

## 8. Staged roadmap and exit gates

| Stage | Work | Exit gate / evidence |
|---|---|---|
| 0. Product and legal baseline | Define first product boundary, hardware BOM, supported JetPack, component licenses, data governance and SBOM workflow | Approved product claims, target hardware sheet, license inventory and testable acceptance criteria |
| 1. Replay MVP | Reproducible replay, typed sensor contracts, health gate, detection baseline, mission logging | Existing tests pass; replay benchmark report generated; missing/stale data is explicit |
| 2. Recon map MVP | Hazard schema, Open3D utilities, map/coordinate-frame validation, evidence-linked report | Annotated dry-site dataset evaluated; localization/map error and unknown coverage reported |
| 3. Jetson edge pilot | Pinned JetPack image, optimized inference experiment, preflight script, power/thermal/latency monitoring | Sustained-load report on the exact target module and enclosure; parity and rollback verified |
| 4. Operator field pilot | Supervised surveys in a controlled, dry or otherwise approved test area; offline storage and operator review | Documented user acceptance, failures, recovery and limitations; no unapproved water entry |
| 5. Navigation HIL | ROS 2/Nav2 simulation, safety monitor, E-stop, sensor/process fault injection | Safety and HIL suite passes; independent E-stop test witnessed and recorded |
| 6. Limited commercial release | SBOM/notices, signed artifact/update procedure, install/support docs, operator training, acceptance test | Release checklist complete for the exact SKU; only evidence-backed claims in sales material |
| 7. Expansion | Add thermal/LiDAR, more models, fleet service, additional robot platforms | Each addition passes its own compatibility, license, benchmark and regression gates |

Do not assign calendar promises until hardware availability, staff capacity, target robot, sensors and test-site permissions are known. Each stage should produce an evidence artifact and a go/no-go decision.

## 9. Commercial packaging

- **PUI89 Research:** replay tools, datasets/manifests, benchmark reports and research integrations.
- **PUI89 Professional:** supported Jetson image, flood reconnaissance pipeline, local operator UI/report, documented sensor configuration and update/diagnostic procedure.
- **PUI89 Enterprise:** fleet management, identity and access control, signed updates, audit export, integration support and defined service/support terms.

Do not market the Professional or Enterprise tier as autonomous rescue until the relevant physical capabilities are independently validated. Quote support and uptime commitments only after operational evidence exists.

## 10. Definition of done for first paid pilot

- [ ] Product boundary and intended-use statement approved.
- [ ] Exact Jetson module, carrier, JetPack, sensor BOM and enclosure recorded.
- [ ] Reproducible dataset manifest and baseline report checked in.
- [ ] Health gate exposes stale, missing, corrupt and unsynchronized sensor data.
- [ ] Hazard map distinguishes observed, inferred and unknown regions.
- [ ] Mission evidence package is exportable and traceable.
- [ ] Sustained latency, memory, power and thermal results recorded on target hardware.
- [ ] Fault-injection suite verifies declared degraded/safe states.
- [ ] Component license review and SBOM completed for the exact release.
- [ ] Operator instructions, known limitations, recovery procedure and support scope delivered.
- [ ] Pilot conducted only in an approved environment with trained operators and a documented stop procedure.
