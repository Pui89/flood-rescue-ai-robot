"""Versioned 3D/4D rescue world model primitives.

The world model stores time-stamped, provenance-aware state. It is intentionally
model-agnostic: learned perception proposes observations; deterministic code
stores and validates state.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Dict, List, Optional, Tuple


class ObjectClass(str, Enum):
    PERSON = "person"
    HAZARD = "hazard"
    VEHICLE = "vehicle"
    STRUCTURE = "structure"
    WATER = "water"
    UNKNOWN = "unknown"


@dataclass(frozen=True)
class ObservationRef:
    sensor_id: str
    timestamp_ns: int
    frame_id: str
    calibration_id: str
    model_version: str


@dataclass
class WorldObject:
    object_id: str
    object_class: ObjectClass
    position_xyz_m: Tuple[float, float, float]
    velocity_xyz_mps: Tuple[float, float, float] = (0.0, 0.0, 0.0)
    confidence: float = 0.0
    covariance_xyz: Optional[Tuple[float, float, float]] = None
    occluded: bool = False
    dynamic: bool = False
    observations: List[ObservationRef] = field(default_factory=list)

    def validate(self) -> None:
        if not self.object_id:
            raise ValueError("object_id is required")
        if len(self.position_xyz_m) != 3 or len(self.velocity_xyz_mps) != 3:
            raise ValueError("position and velocity must be 3-vectors")
        if not 0.0 <= self.confidence <= 1.0:
            raise ValueError("confidence must be in [0, 1]")


@dataclass
class RescueWorldState:
    mission_id: str
    timestamp_ns: int
    frame_id: str
    sequence: int
    objects: Dict[str, WorldObject] = field(default_factory=dict)

    def upsert(self, obj: WorldObject) -> None:
        obj.validate()
        self.objects[obj.object_id] = obj

    def get(self, object_id: str) -> Optional[WorldObject]:
        return self.objects.get(object_id)

    def stale_after(self, max_age_ns: int, now_ns: int) -> List[str]:
        cutoff = now_ns - max_age_ns
        return [
            obj.object_id
            for obj in self.objects.values()
            if not obj.observations or max(ref.timestamp_ns for ref in obj.observations) < cutoff
        ]
