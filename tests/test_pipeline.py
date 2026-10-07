import numpy as np

from flood_robot.config import SystemConfig
from flood_robot.pipeline.rescue_pipeline import FloodRescuePipeline


def test_pipeline_processes_rgb_frame():
    config = SystemConfig(model_device="cpu", base_channels=4)
    pipeline = FloodRescuePipeline(config)
    frame = np.zeros((64, 96, 3), dtype=np.uint8)

    result = pipeline.process_frame(frame, detections=[])

    assert result["depth_map"].shape == (64, 96)
    assert result["hazard_map"].shape == (64, 96)
    assert 0.0 <= result["hazard_score"] <= 1.0
    assert result["tracked_objects"] == []
