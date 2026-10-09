"""Dependency-free evidence grid for synthetic rescue mapping observations."""
from dataclasses import dataclass, field
from math import floor, isfinite

LABELS = {"water", "debris", "person", "vehicle", "building", "clear", "unknown"}
HAZARDS = {"water", "debris"}

@dataclass
class Cell:
    observations: int = 0
    hazard_observations: int = 0
    label_counts: dict = field(default_factory=dict)
    confidence_sum: float = 0.0
    sources: set = field(default_factory=set)

    @property
    def mean_confidence(self):
        return self.confidence_sum / self.observations if self.observations else None

    @property
    def dominant_label(self):
        if not self.label_counts:
            return "unknown"
        return sorted(self.label_counts, key=lambda x: (-self.label_counts[x], x))[0]

class EvidenceGrid:
    """Local grid; inputs are supplied observations, not sensor inference."""
    def __init__(self, width_m, height_m, resolution_m):
        for name, value in (("width_m", width_m), ("height_m", height_m), ("resolution_m", resolution_m)):
            if not isfinite(value) or value <= 0:
                raise ValueError(f"{name} must be finite and positive")
        cols, rows = width_m / resolution_m, height_m / resolution_m
        if abs(cols - round(cols)) > 1e-9 or abs(rows - round(rows)) > 1e-9:
            raise ValueError("dimensions must be integer multiples of resolution")
        self.width_m, self.height_m, self.resolution_m = float(width_m), float(height_m), float(resolution_m)
        self.cols, self.rows = int(round(cols)), int(round(rows))
        self.cells = {}

    def world_to_cell(self, x_m, y_m):
        if not isfinite(x_m) or not isfinite(y_m):
            raise ValueError("coordinates must be finite")
        if x_m < 0 or y_m < 0 or x_m >= self.width_m or y_m >= self.height_m:
            raise ValueError("observation outside map bounds")
        return floor(x_m / self.resolution_m), floor(y_m / self.resolution_m)

    def add_observation(self, x_m, y_m, label, confidence=1.0, source="unspecified"):
        if label not in LABELS:
            raise ValueError(f"unsupported label: {label}")
        if not isfinite(confidence) or not 0 <= confidence <= 1:
            raise ValueError("confidence must be finite and between 0 and 1")
        if not isinstance(source, str) or not source.strip():
            raise ValueError("source must be a non-empty string")
        key = self.world_to_cell(x_m, y_m)
        cell = self.cells.setdefault(key, Cell())
        cell.observations += 1
        cell.label_counts[label] = cell.label_counts.get(label, 0) + 1
        cell.hazard_observations += int(label in HAZARDS)
        cell.confidence_sum += confidence
        cell.sources.add(source)

    def to_dict(self):
        cells = []
        for (col, row), cell in sorted(self.cells.items(), key=lambda item: (item[0][1], item[0][0])):
            cells.append({"col": col, "row": row, "observations": cell.observations,
                "hazard_observations": cell.hazard_observations, "dominant_label": cell.dominant_label,
                "label_counts": dict(sorted(cell.label_counts.items())),
                "mean_input_confidence": cell.mean_confidence, "sources": sorted(cell.sources)})
        return {"schema_version": "1.0", "map_frame": "local_simulation", "origin_m": [0.0, 0.0],
            "width_m": self.width_m, "height_m": self.height_m, "resolution_m": self.resolution_m,
            "cols": self.cols, "rows": self.rows, "observed_cells": len(self.cells),
            "unknown_cells": self.cols * self.rows - len(self.cells), "cells": cells,
            "limitations": ["Supplied observations only; no sensor inference.",
                "Input confidence is not calibrated probability.", "No SLAM or navigation safety guarantee."]}
