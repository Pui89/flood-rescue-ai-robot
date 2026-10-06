from __future__ import annotations
from dataclasses import dataclass
from typing import Any

@dataclass
class ActionDecision:
    approved: bool
    reason: str
    action: Any = None

class VLAGuard:
    '''Safety boundary between LeRobot/VLA policies and robot actuators.'''
    def __init__(self, min_confidence=0.70):
        self.min_confidence = min_confidence

    def validate(self, action, *, confidence, collision_free, human_too_close=False, emergency=False):
        if emergency:
            return ActionDecision(False, 'emergency_stop')
        if human_too_close:
            return ActionDecision(False, 'human_exclusion_zone')
        if not collision_free:
            return ActionDecision(False, 'collision_check_failed')
        if confidence < self.min_confidence:
            return ActionDecision(False, 'action_uncertainty')
        return ActionDecision(True, 'approved', action)