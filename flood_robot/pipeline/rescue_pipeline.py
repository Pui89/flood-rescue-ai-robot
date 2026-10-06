from __future__ import annotations

import time
from typing import Any

import cv2
import numpy as np
import torch

from flood_robot.config import SystemConfig
from flood_robot.models.depth_estimator import DepthEstimator
from flood_robot.spatial.feature_extractor import SpatialFeatureExtractor
from flood_robot.tracking.object_tracker import CustomObjectTracker


class FloodRescuePipeline:
    def __init__(self, config: SystemConfig | None = None):
        self.config = config or SystemConfig()
        self.device = torch.device(self.config.model_device)
        self.depth_model = DepthEstimator(in_channels=3, base_channels=self.config.base_channels).to(self.device)
        self.depth_model.eval()
        self.tracker = CustomObjectTracker(max_age=self.config.max_age, distance_threshold=self.config.distance_threshold)
        self.spatial_extractor = SpatialFeatureExtractor(risk_temperature=self.config.spatial_risk_temperature)

    def _estimate_depth(self, frame: np.ndarray) -> np.ndarray:
        image = frame[:, :, ::-1].astype(np.float32) / 255.0
        tensor = torch.from_numpy(image).permute(2, 0, 1).unsqueeze(0).to(self.device)
        with torch.no_grad():
            depth = self.depth_model(tensor)
        depth_map = depth.squeeze(0).squeeze(0).detach().cpu().numpy()
        if depth_map.shape != frame.shape[:2]:
            depth_map = cv2.resize(depth_map, (frame.shape[1], frame.shape[0]), interpolation=cv2.INTER_LINEAR)
        return np.clip(depth_map, 0.0, 1.0)

    def process_frame(self, frame: np.ndarray, detections: list[tuple[int, int, int, int]] | None = None) -> dict[str, Any]:
        frame = np.asarray(frame)
        if frame.ndim != 3 or frame.shape[2] != 3:
            raise ValueError("Expected a BGR color frame with shape (H, W, 3)")

        depth_map = self._estimate_depth(frame)
        tracked_objects = self.tracker.update(detections or [])
        hazard_map = self.spatial_extractor.extract(frame, depth_map, tracked_objects)
        hazard_score = float(np.mean(hazard_map))

        return {
            "depth_map": depth_map,
            "hazard_map": hazard_map,
            "hazard_score": hazard_score,
            "tracked_objects": tracked_objects,
            "detections": detections or [],
            "timestamp": time.time(),
        }

    def run_real_time(self, source: int | str = 0, display: bool = True, max_frames: int | None = None) -> None:
        cap = cv2.VideoCapture(source)
        if not cap.isOpened():
            raise RuntimeError(f"Unable to open video source: {source}")

        renderer = None
        try:
            import flood_robot.visualization.video_renderer as vr
            renderer = vr.DemoVideoRenderer()
        except Exception:
            renderer = None

        frame_index = 0
        while True:
            ok, frame = cap.read()
            if not ok:
                break

            result = self.process_frame(frame)
            if renderer is not None:
                output = renderer.render(frame, result["depth_map"], result["tracked_objects"], result["hazard_map"])
            else:
                output = frame.copy()

            if display:
                cv2.imshow("Flood Rescue AI Robot", output)
                if cv2.waitKey(1) & 0xFF == ord("q"):
                    break

            frame_index += 1
            if max_frames is not None and frame_index >= max_frames:
                break

        cap.release()
        if display:
            cv2.destroyAllWindows()


__all__ = ["FloodRescuePipeline"]
