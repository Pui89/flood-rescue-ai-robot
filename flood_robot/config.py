from __future__ import annotations

from dataclasses import dataclass, field

import torch


@dataclass
class SystemConfig:
    image_size: tuple[int, int] = (640, 480)
    base_channels: int = 32
    model_device: str = field(default_factory=lambda: "cuda" if torch.cuda.is_available() else "cpu")
    confidence_threshold: float = 0.45
    max_age: int = 8
    distance_threshold: float = 35.0
    spatial_risk_temperature: float = 0.75
    fps_target: int = 30
    stream_source: int | str = 0
    display: bool = True

    def as_dict(self) -> dict:
        return {
            "image_size": self.image_size,
            "base_channels": self.base_channels,
            "model_device": self.model_device,
            "confidence_threshold": self.confidence_threshold,
            "max_age": self.max_age,
            "distance_threshold": self.distance_threshold,
            "spatial_risk_temperature": self.spatial_risk_temperature,
            "fps_target": self.fps_target,
            "stream_source": self.stream_source,
            "display": self.display,
        }


__all__ = ["SystemConfig"]
