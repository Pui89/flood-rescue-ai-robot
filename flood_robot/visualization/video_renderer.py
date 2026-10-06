from __future__ import annotations

import cv2
import numpy as np


class DemoVideoRenderer:
    def __init__(self, width: int = 640, height: int = 480):
        self.width = width
        self.height = height

    def render(self, frame: np.ndarray, depth_map: np.ndarray, tracked_objects: list, hazard_map: np.ndarray) -> np.ndarray:
        output = frame.copy()
        depth_vis = np.clip(depth_map, 0.0, 1.0)
        depth_vis = (depth_vis * 255).astype(np.uint8)
        depth_vis = cv2.applyColorMap(depth_vis, cv2.COLORMAP_JET)

        overlay = cv2.addWeighted(output, 0.7, depth_vis, 0.3, 0)

        if hazard_map is not None:
            hazard_vis = np.uint8(np.clip(hazard_map, 0.0, 1.0) * 255)
            hazard_vis = cv2.applyColorMap(hazard_vis, cv2.COLORMAP_HOT)
            overlay = cv2.addWeighted(overlay, 1.0, hazard_vis, 0.25, 0)

        for obj in tracked_objects:
            x1, y1, x2, y2 = map(int, obj.bbox)
            cv2.rectangle(overlay, (x1, y1), (x2, y2), (0, 255, 0), 2)
            cv2.putText(
                overlay,
                f"T{obj.track_id}",
                (x1, max(0, y1 - 10)),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.5,
                (255, 255, 255),
                1,
                cv2.LINE_AA,
            )

        cv2.putText(
            overlay,
            "Flood Rescue AI Robot - real time",
            (12, 24),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.7,
            (255, 255, 255),
            2,
            cv2.LINE_AA,
        )
        return overlay


__all__ = ["DemoVideoRenderer"]
