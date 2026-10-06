from __future__ import annotations

from dataclasses import dataclass

import numpy as np


@dataclass
class SyntheticFloodSceneGenerator:
    width: int = 640
    height: int = 480
    water_level: float = 0.35

    def generate_frame(self, frame_index: int = 0) -> np.ndarray:
        frame = np.zeros((self.height, self.width, 3), dtype=np.uint8)
        frame[:, :, 0] = 80
        frame[:, :, 1] = 130
        frame[:, :, 2] = 180

        for x in range(0, self.width, 80):
            frame[:, x : x + 10, :] = np.array([0, 120, 160], dtype=np.uint8)

        water_band = int(self.height * self.water_level)
        frame[water_band:, :, 0] = np.clip(frame[water_band:, :, 0] + 25, 0, 255)
        frame[water_band:, :, 1] = np.clip(frame[water_band:, :, 1] + 20, 0, 255)
        frame[water_band:, :, 2] = np.clip(frame[water_band:, :, 2] + 10, 0, 255)

        for i in range(3):
            px = 110 + ((frame_index * 17 + i * 95) % (self.width - 150))
            py = 160 + i * 40
            cv = [180, 220, 240][i]
            frame[py : py + 70, px : px + 40, :] = np.array([cv, cv - 15, cv - 40], dtype=np.uint8)

        return frame

    def generate_detections(self, frame_index: int = 0) -> list[tuple[int, int, int, int]]:
        offset = (frame_index * 7) % 30
        return [
            (120 + offset, 200, 160 + offset, 280),
            (260 + offset, 180, 310 + offset, 270),
            (420, 240, 470, 330),
        ]


__all__ = ["SyntheticFloodSceneGenerator"]
