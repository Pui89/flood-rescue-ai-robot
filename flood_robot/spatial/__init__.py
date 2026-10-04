from __future__ import annotations

import torch


class SpatialFeatureExtractor:
    def __init__(self, risk_temperature: float = 0.75) -> None:
        self.risk_temperature = risk_temperature

    def extract(
        self,
        depth_map: torch.Tensor,
        detections: list[tuple[float, float, float, float]],
    ) -> dict:
        device = depth_map.device

        if depth_map.dim() == 3:
            depth_map = depth_map.unsqueeze(0)

        if depth_map.dim() != 3:
            raise ValueError("depth_map must be a 2D or 3D tensor.")

        h, w = depth_map.shape[-2:]
        risk_map = torch.zeros_like(depth_map)
        center_y = torch.linspace(0.0, 1.0, h, device=device).view(-1, 1).expand(-1, w)
        danger_prior = 1.0 - center_y
        risk_map = depth_map * (0.2 + 0.8 * danger_prior)

        for x1, y1, x2, y2 in detections:
            x1_i, y1_i = max(0, int(x1)), max(0, int(y1))
            x2_i, y2_i = min(w, int(x2)), min(h, int(y2))
            if x2_i <= x1_i or y2_i <= y1_i:
                continue
            crop = torch.ones((1, y2_i - y1_i, x2_i - x1_i), device=device)
            risk_map[:, y1_i:y2_i, x1_i:x2_i] += crop * 0.4

        risk_map = torch.clamp(risk_map, 0.0, 1.0)
        hazard_score = float(risk_map.mean().item())
        return {
            "risk_map": risk_map,
            "hazard_score": hazard_score,
            "temperature": self.risk_temperature,
        }
