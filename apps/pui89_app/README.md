# PUI89 Flood Rescue AI Application

A simulation-first API for flood-scene reconnaissance and **human-supervised rescue decision support**. The current baseline processes structured candidate and hazard observations; it is not a trained victim detector, a hydrodynamic simulator, or a certified rescue system.

## Run
```bash
pip install -r apps/pui89_app/requirements.txt
uvicorn apps.pui89_app.main:app --reload
```
Interactive API: `http://127.0.0.1:8000/docs`.

## API
- `GET /health` — service status.
- `POST /analyze` — sensor-quality gate, candidate evidence review, hazard-aware route status.
- `GET /metrics` — request counters, not AI benchmark results.

Example:
```json
{
  "rgb_available": true,
  "thermal_available": true,
  "lidar_valid": true,
  "timestamp_skew_ms": 12,
  "water_depth_m": 0.25,
  "current_speed_mps": 0.2,
  "candidates": [{
    "track_id": "person-candidate-01",
    "visual_confidence": 0.88,
    "thermal_support": true,
    "track_stability_frames": 8,
    "distance_m": 6.2
  }]
}
```

## Safety
- Missing sensor evidence, stale timestamps, excessive water depth/current, or uncertain tracks lead to `SAFE_HOLD` or `HUMAN_REVIEW`.
- Candidate scores are heuristic evidence-ranking values, not probabilities or definitive victim identification.
- This service never issues movement commands and must not replace emergency services or trained rescue personnel.
- Thresholds are illustrative configuration defaults, not universally safe flood limits.

## Benchmark plan
Use labeled, consented datasets and simulator scenarios. Report detection precision/recall, time-to-detect, tracking continuity, localization error, hazard false negatives, route feasibility, latency, resource use, sensor-dropout behavior and sim-to-real gap. Do not mix simulated and field results.

## Tests
```bash
python -m unittest discover -s apps/pui89_app -p 'test_*.py' -v
```
