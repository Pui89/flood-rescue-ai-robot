# PUI89 Benchmark

This benchmark defines the minimum evidence required before this autonomous flood-response project is described as field-validated.

## Benchmark principles
- Every result has a dataset/version identifier.
- Every result records hardware and model versions.
- Targets are never reported as achieved results.
- Test and training data are separated.
- Failure cases are retained.
- Unknown/OOD cases are evaluated explicitly.
- Safety metrics are reported separately from AI accuracy.

## Core benchmark
| Area | Metrics |
|---|---|
| Perception | person/object detection precision, recall, F1 |
| 3D/world model | localization error, map consistency |
| Navigation | waypoint success, obstacle avoidance, recovery success |
| Risk | SAFE/CAUTION/DANGEROUS/UNKNOWN calibration |
| Communications | mission continuity under link loss, recovery time |
| Operations | mission duration, mapped area/hour, energy/hour |
| Safety | unsafe-route rejection, emergency-stop verification, degraded-mode behavior |

## Required scenarios
- normal daylight;
- low light;
- rain/wet surfaces;
- occlusion;
- motion blur;
- sensor dropout;
- calibration error;
- communication loss;
- low battery;
- unexpected objects;
- out-of-distribution environment;
- conflicting sensor evidence;
- operator intervention;
- emergency stop.

## Reporting template
```text
experiment_id
dataset_version
hardware
sensor_configuration
model_version
software_commit
environment
scenario
metrics
confidence
uncertainty
OOD_score
failures
safety_events
operator_interventions
result
limitations
```

A benchmark result requires a defined protocol, reproducible configuration, measured data, comparison baseline, limitations and recorded failure cases.
