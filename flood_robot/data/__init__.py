from __future__ import annotations

import numpy as np


class SyntheticFloodSceneGenerator:
    def __init__(self, width: int = 640, height: int = 480):
        self.width = width
        self.height = height

    def generate_frame(self, t: float = 0.0) -> np.ndarray:
        frame = np.zeros((self.height, self.width, 3), dtype=np.uint8)
        wave = np.sin(np.linspace(0.0, 2.0 * np.pi, self.width))

        for y in range(self.height):
            depth = 0.5 + 0.18 * np.sin((y / self.height) * 10.0 + t)
            water_color = np.array([int(60 + depth * 40), int(110 + depth * 60), int(150 + depth * 80)], dtype=np.uint8)
            frame[y, :, :] = water_color

        water_pattern = ((wave + np.sin(np.linspace(0.0, 3.0 * np.pi, self.width) + t)) * 10).astype(np.int32)
        for x in range(self.width):
            stripe_y_start = int(self.height * 0.55 + water_pattern[x])
            stripe_y_end = self.height
            frame[stripe_y_start:stripe_y_end, x, :] = np.clip(frame[stripe_y_start:stripe_y_end, x, :] + 10, 0, 255)

        rescue_rectangle = (int(self.width * 0.12), int(self.height * 0.42), int(self.width * 0.18), int(self.height * 0.68))
        self._draw_person(frame, rescue_rectangle, color=(255, 255, 255), confidence=0.96)

        debris_rectangle = (int(self.width * 0.45), int(self.height * 0.55), int(self.width * 0.67), int(self.height * 0.82))
        self._draw_debris(frame, debris_rectangle)

        return frame

    @staticmethod
    def _draw_person(frame: np.ndarray, box: tuple[int, int, int, int], color: tuple[int, int, int], confidence: float) -> None:
        x0, y0, x1, y1 = box
        cv = np.array(color, dtype=np.uint8)
        frame[y0:y1, x0:x1, :] = cv * 0.5 + frame[y0:y1, x0:x1, :] * 0.5

    @staticmethod
    def _draw_debris(frame: np.ndarray, box: tuple[int, int, int, int]) -> None:
        x0, y0, x1, y1 = box
        debris = np.array([160, 140, 120], dtype=np.uint8)
        frame[y0:y1, x0:x1, :] = debris

        for y in range(y0, y1, 12):
            frame[y:y+3, x0:x1, :] = np.array([100, 90, 85], dtype=np.uint8)
