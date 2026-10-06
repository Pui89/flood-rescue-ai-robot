from __future__ import annotations

import numpy as np


class SpatialFeatureExtractor:
    def __init__(self, risk_temperature: float = 0.75):
        self.risk_temperature = risk_temperature

    def extract(self, frame: np.ndarray, depth_map: np.ndarray, tracked_objects: list) -> np.ndarray:
        frame = np.asarray(frame)
        if depth_map is None or depth_map.size == 0:
            depth_map = np.zeros((frame.shape[0], frame.shape[1]), dtype=np.float32)
        depth_map = np.asarray(depth_map, dtype=np.float32)
        if depth_map.shape != frame.shape[:2]:
            depth_map = np.resize(depth_map, frame.shape[:2])

        normalized = np.clip(depth_map, 0.0, 1.0)
        hazard = 0.55 * (1.0 - normalized)
        brightness = np.mean(frame.astype(np.float32), axis=2) / 255.0
        hazard = hazard + 0.25 * (1.0 - brightness)

        for obj in tracked_objects:
            x1, y1, x2, y2 = map(int, obj.bbox)
            h0 = max(0, y1)
            h1 = min(frame.shape[0], y2)
            w0 = max(0, x1)
            w1 = min(frame.shape[1], x2)
            if h1 > h0 and w1 > w0:
                hazard[h0:h1, w0:w1] = np.maximum(hazard[h0:h1, w0:w1], 0.8)

        hazard = np.clip(hazard, 0.0, 1.0)
        return hazard


__all__ = ["SpatialFeatureExtractor"]
