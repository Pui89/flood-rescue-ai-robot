from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any

@dataclass
class Forecast:
    event: str
    probability: float
    horizon_seconds: float
    severity: str
    evidence: dict[str, Any] = field(default_factory=dict)

class EarlyWarningEngine:
    '''Conservative temporal warning layer. A learned predictor can be injected.'''
    def __init__(self, predictor=None, lookahead_seconds=5.0):
        self.predictor = predictor
        self.lookahead_seconds = lookahead_seconds

    def forecast(self, state):
        if self.predictor is not None:
            return list(self.predictor(state))
        warnings = []
        if state.get('visibility') in {'dark', 'low', 'fog', 'occluded'}:
            warnings.append(Forecast('low_visibility', 0.75, self.lookahead_seconds, 'warning'))
        if float(state.get('confidence', 1.0)) < 0.50:
            warnings.append(Forecast('perception_uncertain', 0.85, 0.0, 'critical'))
        if state.get('person_submersion_trend'):
            warnings.append(Forecast('submersion_or_drowning_risk', 0.80, self.lookahead_seconds, 'critical'))
        if state.get('debris_trajectory_conflict'):
            warnings.append(Forecast('debris_collision_risk', 0.80, self.lookahead_seconds, 'critical'))
        if state.get('route_blockage_predicted'):
            warnings.append(Forecast('route_blockage', 0.70, self.lookahead_seconds, 'warning'))
        return warnings