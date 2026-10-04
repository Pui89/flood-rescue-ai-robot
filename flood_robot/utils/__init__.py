from __future__ import annotations

import numpy as np


def compute_depth_metrics(pred: np.ndarray, target: np.ndarray) -> dict:
    diff = np.abs(pred - target)
    mae = float(np.mean(diff))
    rmse = float(np.sqrt(np.mean(diff ** 2)))
    return {"mae": mae, "rmse": rmse}
