from __future__ import annotations

import numpy as np
import torch

from flood_robot.config import SystemConfig
from flood_robot.models.depth_estimator import DepthEstimator
from flood_robot.spatial.feature_extractor import SpatialFeatureExtractor
from flood_robot.tracking.object_tracker import CustomObjectTracker


class FloodRescuePipeline:
    def __init__(self, config: SystemConfig | None = None) -> None:
        self.config = config or SystemConfig()
        self.depth_model = DepthEstimator(in_channels=3, base_channels=self.config.base_channels)
        self.depth_model.eval()
        self.object_tracker = CustomObjectTracker(
            max_age=self.config.max_age,
            distance_threshold=self.config.distance_threshold,
        )
        self.feature_extractor = SpatialFeatureExtractor(risk_temperature=self.config.spatial_risk_temperature)

    def process_frame(
        self,
        rgb_frame: np.ndarray,
        detections: list[tuple[float, float, float, float]] | None = None,
    ) -> dict:
        if detections is None:
            detections = []

        tensor = torch.from_numpy(rgb_frame).permute(2, 0, 1).float() / 255.0
        tensor = tensor.unsqueeze(0).to(self.config.model_device)

        with torch.no_grad():
            depth_map = self.depth_model(tensor).squeeze(0).cpu()

        tracked_objects = self.object_tracker.track(detections)
        spatial = self.feature_extractor.extract(depth_map, [obj.bbox for obj in tracked_objects])

        return {
            "depth_map": depth_map,
            "tracked_objects": [
                {
                    "track_id": obj.track_id,
                    "bbox": obj.bbox,
                    "centroid": obj.centroid,
                    "age": obj.age,
                    "hits": obj.hits,
                }
                for obj in tracked_objects
            ],
            "risk_map": spatial["risk_map"],
            "hazard_score": spatial["hazard_score"],
        }
