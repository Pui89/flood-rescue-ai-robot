from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class SafetyDecision:
    allowed: bool
    reason: str


def validate_proposed_action(
    *,
    sensor_health_ok: bool,
    localization_confidence: float,
    collision_free: bool,
    authorized: bool,
    emergency_stop: bool,
) -> SafetyDecision:
    """Deterministic software boundary for candidate actions.

    This function does not command hardware. It only accepts or blocks a
    proposed action before an authorized robotics control layer can consume it.
    """
    if emergency_stop:
        return SafetyDecision(False, "emergency_stop")
    if not sensor_health_ok:
        return SafetyDecision(False, "sensor_health")
    if localization_confidence < 0.8:
        return SafetyDecision(False, "low_localization_confidence")
    if not collision_free:
        return SafetyDecision(False, "collision_risk")
    if not authorized:
        return SafetyDecision(False, "operator_or_policy_not_authorized")
    return SafetyDecision(True, "validated")
