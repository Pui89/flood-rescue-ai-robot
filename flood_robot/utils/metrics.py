from __future__ import annotations

from typing import Iterable

import numpy as np


def compute_depth_metrics(predictions: Iterable[np.ndarray], targets: Iterable[np.ndarray]) -> dict[str, float]:
    preds = [np.asarray(p, dtype=np.float32).ravel() for p in predictions]
    targs = [np.asarray(t, dtype=np.float32).ravel() for t in targets]
    if len(preds) != len(targs):
        raise ValueError("Prediction and target lengths must match")

    errors = []
    for pred, target in zip(preds, targs):
        errors.append(np.mean(np.abs(pred - target)))

    return {
        "mae": float(np.mean(errors)) if errors else 0.0,
    }


__all__ = ["compute_depth_metrics"]
