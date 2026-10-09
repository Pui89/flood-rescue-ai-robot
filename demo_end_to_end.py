"""Synthetic software-only demo; no live sensors or robot actuators are used."""
import json
from flood_robot.end_to_end import EndToEndRescuePipeline

T0 = "2026-10-10T00:00:00+00:00"
observations = [
    {
        "sensor_id": "sim-rgb-01", "modality": "rgb", "timestamp": T0, "quality": 0.92,
        "candidates": [{"object_id": "victim-candidate-01", "kind": "victim_candidate",
                        "confidence": 0.88, "position_xyz_m": [2.0, 1.0, 0.0]}],
    },
    {
        "sensor_id": "sim-depth-01", "modality": "depth", "timestamp": T0, "quality": 0.95,
        "candidates": [{"object_id": "victim-candidate-01", "kind": "victim_candidate",
                        "confidence": 0.81, "position_xyz_m": [2.0, 1.0, 0.0]}],
    },
]
report = EndToEndRescuePipeline().run(observations, mission_id="synthetic-demo")
print(json.dumps(report.to_dict(), indent=2))
print("\nSynthetic inputs only. This is not validated victim detection or a physics simulation.")
