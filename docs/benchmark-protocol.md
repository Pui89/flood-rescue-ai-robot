# Flood Recon Benchmark Protocol

**Status:** protocol specification; no performance results are implied by this document.  
**Applies to:** PUI89 Flood Recon software and Jetson Orin / AGX Orin deployment candidates.

## 1. Rules for a valid benchmark

1. Publish the commit SHA, clean/dirty working-tree status, run command, configuration hash, and environment manifest.
2. Identify exact hardware SKU, RAM, carrier board, storage, power mode, cooling, JetPack/L4T, CUDA, TensorRT, OS, ROS 2 distribution, driver and model versions.
3. Identify dataset name/version, license, split, sequence IDs, label schema and preprocessing. Keep test scenes separated by collection session where possible to reduce leakage.
4. Never report an unmeasured value as a result. Mark missing metrics as **not measured** and distinguish targets from observations.
5. Publish raw per-frame/per-sequence outputs, aggregate summaries, failure cases, and scripts needed to reproduce the result, subject to dataset privacy and license restrictions.
6. Run timed workloads after documented warm-up. Report run count, median, p95, spread and dropped/invalid samples. Include cold-start and recovery tests separately.
7. Do not compare results across different hardware, precision modes, sensor inputs or dataset splits without identifying the differences.

## 2. Test conditions

- **Replay:** deterministic recorded sensor streams; fixed clock or recorded timestamps; no network required unless explicitly under test.
- **Integration:** real sensor drivers and timestamps, calibration files pinned by hash, synchronized clocks and documented sensor placement.
- **Jetson sustained load:** representative mission workload under intended enclosure and cooling; monitor temperature, clocks, power and throttling for the full run.
- **Fault injection:** sensor dropout, stale timestamps, time skew, corrupt frames, inference timeout, process crash, network loss, disk pressure and low battery where applicable.
- **HIL / motion tests:** secured test stand or controlled closed area, physical emergency stop, spotter and documented risk assessment. Do not use floodwater or public rescue scenes as a first test environment.

## 3. Metrics and definitions

| Area | Metric | Definition / reporting requirement |
|---|---|---|
| Perception | Per-class precision, recall, F1 | Publish class definitions, matching rule, confidence threshold and confusion matrix. |
| False alerts | False alerts per operating hour | State what counts as an alert and how ground truth is adjudicated. |
| Localization | Absolute / relative trajectory error | Name tool, alignment method, coordinate frame and reference quality. |
| Mapping | Map error and coverage | State units, resolution, evaluation mask and reference-map method. |
| Unknown space | Unknown-area fraction | Report separately; never count unknown as safe or traversable. |
| Runtime | End-to-end latency p50 / p95 / max | Include capture-to-output stages, warm-up, sample count and dropped frames. |
| Throughput | FPS and dropped/stale-frame rate | Report input rate and whether frame skipping is allowed. |
| Resources | RAM, GPU memory, CPU/GPU utilization | Report peak and sustained values with sampling interval. |
| Power/thermal | Board power, temperature, throttle events | Identify measurement source, power mode, cooling and ambient temperature. |
| Reliability | Crash/restart/recovery time | Include fault type, recovery policy and required operator action. |
| Safety | Gate response and stop latency | Measure each injected fault; report every failure, not just aggregate pass rate. |

## 4. Raw result bundle

Each run should create a unique folder such as results/<date>_<commit>_<device>/ containing:

- manifest.json: commit, run ID, dataset/split, config hash, hardware/software inventory and command.
- metrics.json: machine-readable metric values, units, sample counts and not-measured fields.
- per_frame.csv or per_sequence.csv: raw timestamps, predictions, labels and errors as allowed.
- resource_log.csv: utilization, memory, temperature, power, clocks and throttling samples.
- events.jsonl: sensor faults, warnings, safety-gate decisions, restarts and operator interventions.
- stdout.log, stderr.log and exit code.
- plots/: generated charts with plotting script and input-data references.
- README.md: exact reproduction command and known limitations.

Never commit credentials, private location data, identifiable bystander imagery, or restricted dataset samples. Publish checksums for large artifacts hosted elsewhere.

## 5. Proposed acceptance gates

These are **proposed engineering gates**, not measured results or certification criteria. Set numeric thresholds after a representative baseline, hazard analysis and stakeholder review.

- **Perception:** class-specific precision/recall thresholds justified by risk; critical misses reviewed individually.
- **Mapping:** documented error/coverage thresholds on held-out sequences; unknown regions remain explicit.
- **Runtime:** p95 latency and frame-drop limits met during sustained Jetson runs without unreported throttling.
- **Robustness:** every mandatory fault-injection case produces the expected safe degraded state or stop; any failure blocks progression.
- **Reproducibility:** another operator can reproduce the summary from the raw result bundle and pinned environment.
- **Field readiness:** approved risk assessment, emergency-stop validation, operator procedure, rollback plan and sign-off required before controlled field trials.

## 6. Benchmark reporting template

For each metric publish: name, value, unit, sample_count, mean, median, p95, standard deviation where meaningful, dataset version, hardware, software commit, config hash, run ID, limitations, and raw artifact URI.

A benchmark without its conditions and raw evidence is not a validated result.