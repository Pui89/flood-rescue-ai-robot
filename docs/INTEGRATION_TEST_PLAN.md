# PUI89 Flood Recon — Integration and Fault-Injection Test Plan

**Scope:** first commercial product for supervised flood reconnaissance and hazard mapping on NVIDIA Jetson Orin / AGX Orin. This is a test specification; passing status must be backed by actual CI, replay, HIL, or field evidence.

## Test layers

1. **Unit:** pure schema, timestamp, confidence, map geometry, hazard fusion, policy and report tests.
2. **Adapter contract:** each detector, embedding model, anomaly model, mapper and inference backend must pass the same interface tests.
3. **Pipeline integration:** recorded sensors → health gate → perception → world model/map → hazard report.
4. **Replay benchmark:** fixed dataset manifest, pinned configuration, metrics and artifact output.
5. **Fault injection:** controlled corruption, dropout, clock skew, stale frames, node crashes, storage exhaustion, GPU stall, network loss and low-battery event.
6. **Hardware-in-the-loop:** target Jetson, camera/IMU/LiDAR drivers, power/thermal telemetry and independently testable E-stop.
7. **Controlled field trial:** approved site, trained operators, documented stop conditions and post-run review.

## Proposed test files

| Path | Purpose |
|---|---|
| tests/unit/test_sensor_contracts.py | Required fields, invalid dimensions, timestamp/frame/calibration validation |
| tests/unit/test_health_gate.py | Missing, stale, out-of-order, corrupt and unsynchronized samples |
| tests/unit/test_hazard_schema.py | Valid hazard types, coordinate frames, expiry, evidence and uncertainty |
| tests/unit/test_hazard_fusion.py | Conflicting modalities, duplicate evidence, UNKNOWN propagation |
| tests/unit/test_mission_log.py | Event ordering, provenance, secret redaction, rotation and write failures |
| tests/integration/test_replay_pipeline.py | Recorded input through end-to-end report |
| tests/integration/test_perception_adapters.py | Adapter output schema and deterministic post-processing |
| tests/integration/test_mapping_backend.py | Frame conventions, map validity, missing depth and invalid points |
| tests/integration/test_onnx_parity.py | Reference vs exported model outputs within declared tolerances |
| tests/fault_injection/test_sensor_dropout.py | Each critical modality disappears at runtime |
| tests/fault_injection/test_timestamp_skew.py | Clock offset, reordered frames and stale transform |
| tests/fault_injection/test_process_failure.py | Perception/mapping node crash, restart and state recovery |
| tests/fault_injection/test_network_loss.py | No cloud connection, delayed telemetry and reconnection |
| tests/fault_injection/test_resource_pressure.py | Memory pressure, slow inference, storage exhaustion and thermal throttle |
| tests/hil/test_estop_and_hold.py | Physical E-stop and command inhibit on critical fault |
| tests/hil/test_jetson_sustained_load.py | Sustained end-to-end load and telemetry on exact SKU |

These are proposed paths. Create only the tests appropriate to the actual repository layout and available hardware; do not claim they pass until implemented and run.

## Required scenarios and expected outcomes

| ID | Injection / scenario | Expected outcome | Evidence |
|---|---|---|---|
| INT-001 | Valid synchronized RGB input | Valid perception result with timestamps and model version | JSONL log + output |
| INT-002 | Missing depth stream | Degraded state; no fabricated 3D position | Unit/integration result |
| INT-003 | Frame older than configured maximum age | Rejected or marked stale; cannot update current safe map as fresh | Test log |
| INT-004 | Clock skew beyond threshold | Fusion held/UNKNOWN; diagnostic reason emitted | Test log |
| INT-005 | Invalid calibration ID or frame | Sample rejected with explicit error | Test log |
| INT-006 | Corrupt/empty frame | Pipeline remains alive; invalid sample counted | Test log |
| INT-007 | Contradictory camera/LiDAR evidence | Conflict preserved; no silent certainty increase | Evidence bundle |
| INT-008 | Anomalib flags an unfamiliar patch | Separate anomaly event; not auto-labeled as person or safe/unsafe traversability | Output schema assertion |
| INT-009 | DINOv2 adapter unavailable | Core pipeline runs without optional adapter or fails startup clearly according to configuration | Startup log |
| INT-010 | Mapping backend unavailable | No stale map presented as current; explicit degraded mode | Integration log |
| INT-011 | ONNX vs reference mismatch | Release gate fails; fallback retained | Parity report |
| INT-012 | GPU inference stalls | Watchdog/health gate detects deadline miss; motion inhibited if relevant | HIL/simulation trace |
| INT-013 | Network disconnected | Local sensing/logging continues; safety loop unaffected | Replay/HIL log |
| INT-014 | Disk full or log write failure | Operator alert; safe bounded behavior; no false claim of saved evidence | Integration result |
| INT-015 | Process restart | Model/config identity reloaded; mission state reconciled; no stale command replay | Restart trace |
| INT-016 | E-stop activated | Actuator command inhibited via independent path | Witnessed HIL record |
| INT-017 | Low battery event | Mission policy requests return/stop according to configured robot capability; no assumed return if localization is invalid | HIL record |
| INT-018 | Unknown environment | Unknown region rendered separately from known free space | Map artifact |
| INT-019 | Rain/glare/occlusion | Metrics reported by condition; confidence/unknown behavior evaluated | Benchmark report |
| INT-020 | Sustained target-hardware load | p50/p95 latency, dropped frames, power, memory and thermal state captured over a defined duration | Jetson report |

## Benchmark reporting requirements

Every run records:
- experiment ID, date, operator, dataset version and scenario;
- Git commit, configuration hash, model/checkpoint hashes and inference backend;
- Jetson SKU, RAM, carrier board, JetPack/L4T, CUDA/TensorRT/ONNX Runtime versions;
- sensor model, calibration, frame rates and synchronization;
- input frame count, processed count, dropped/stale/corrupt counts;
- p50/p95/p99 latency, throughput, peak memory, power, temperatures and throttling events;
- per-class precision/recall, false alerts, map error, coverage and unknown-area ratio where ground truth exists;
- fault injected, expected behavior, actual behavior, failure artifacts and pass/fail reviewer.

Do not combine simulation, lab, HIL and field results into a single unlabeled score.

## Release gates

- **G1 — Software:** unit and adapter tests pass; critical schema and health-gate tests have no known failures.
- **G2 — Replay:** benchmark is reproducible and failure cases are retained.
- **G3 — Edge:** target Jetson sustains the declared workload within the approved thermal, power and latency envelope.
- **G4 — Safety:** E-stop, command inhibit, stale-data and lost-localization tests pass in simulation/HIL before any mobile trial.
- **G5 — Commercial:** SBOM, license notices, install/update/rollback instructions, privacy/security review, operator manual and known limitations are ready.
- **G6 — Pilot:** controlled pilot is approved by responsible operators; every incident is reviewed before expansion.

A failure of a safety gate is a stop-ship issue, not a warning that can be averaged against model accuracy.
