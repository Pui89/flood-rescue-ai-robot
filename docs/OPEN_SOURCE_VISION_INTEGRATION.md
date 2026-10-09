# Optional DINOv2 + Anomalib vision baseline

This repository can use the PUI89 optional vision adapters for flood reconnaissance and rescue-support research:

- [DINOv2](https://github.com/facebookresearch/dinov2) generic embeddings for comparing scenes, debris, infrastructure and visible objects.
- [Anomalib](https://github.com/open-edge-platform/anomalib) anomaly scores for unusual scene appearance or possible sensor/domain shift.

Neither model proves a person is present, determines water depth/current, detects chemical hazards reliably, or establishes that a route is safe. Anomaly scores are not danger probabilities. Use dedicated validated person detection, depth/water sensing, temporal tracking, uncertainty handling and operator confirmation.

## End-to-end and verification

The `pui89_vision` package provides optional adapters plus a deterministic `make_screening_record -> verify_screening_record -> human review` path. Missing evidence abstains; records always require human review and never authorize actuators. The checksum is not a digital signature. No model weights are downloaded automatically; inject explicitly loaded model objects and verify the exact model/checkpoint/dependency licenses.

Run `python -m unittest discover -s tests -v` for model-independent integrity tests. This does not establish rescue effectiveness or safe field operation. Benchmark by water level, rainfall, day/night, turbidity, occlusion, camera damage and sensor dropout. Report false negatives, false alarms, calibration, abstention coverage, latency and power. Require simulation, controlled trials, trained operator oversight and an independent safety supervisor before any hardware deployment.
