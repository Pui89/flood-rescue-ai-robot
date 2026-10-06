"""High-level reasoning adapter for flood-rescue robotics.

A VLM/reasoning model interprets multimodal scene state and proposes priorities.
It never commands motors or bypasses the deterministic safety controller.
"""

from dataclasses import dataclass, field
from typing import Any, Callable, Dict, List, Optional


@dataclass
class RescueReasoningDecision:
    priority: str
    rationale: str
    confidence: float
    next_steps: List[str] = field(default_factory=list)
    target_id: Optional[str] = None
    requires_human_review: bool = False


class FloodRescueReasoner:
    """Adapter boundary for Qwen3-VL or another multimodal reasoning model."""

    def __init__(self, model: str = "Qwen3-VL", infer: Optional[Callable[[Dict[str, Any]], Dict[str, Any]]] = None):
        self.model = model
        self.infer = infer

    def decide(self, scene: Dict[str, Any]) -> RescueReasoningDecision:
        if self.infer is None:
            return self._conservative_fallback(scene)
        raw = self.infer({
            "model": self.model,
            "task": "flood_rescue_reasoning",
            "scene": scene,
            "constraints": [
                "never_control_motors_directly",
                "treat_unseen_as_unknown",
                "never_infer_person_absence_from_missing_detection",
                "prefer_reobserve_when_visibility_is_uncertain",
                "safety_gate_has_final_authority",
            ],
        })
        return RescueReasoningDecision(
            priority=str(raw.get("priority", "observe")),
            rationale=str(raw.get("rationale", "")),
            confidence=float(raw.get("confidence", 0.0)),
            next_steps=list(raw.get("next_steps", [])),
            target_id=raw.get("target_id"),
            requires_human_review=bool(raw.get("requires_human_review", False)),
        )

    def _conservative_fallback(self, scene: Dict[str, Any]) -> RescueReasoningDecision:
        visibility = scene.get("visibility", "UNKNOWN")
        if visibility in {"UNSEEN", "UNKNOWN", "OCCLUDED", "LOW_VISIBILITY"}:
            return RescueReasoningDecision(
                "reobserve",
                "Scene visibility is insufficient for confident rescue planning.",
                0.40,
                ["scan_with_thermal_or_nir", "refresh_depth_or_lidar", "rebuild_local_map"],
            )
        if scene.get("person_at_risk"):
            return RescueReasoningDecision(
                "assist_person",
                "A person-at-risk signal is present; route the candidate plan through the safety gate.",
                0.65,
                ["confirm_person", "estimate_safe_approach", "request_human_review_if_uncertain"],
                str(scene.get("target_id", "")),
            )
        return RescueReasoningDecision("patrol", "No critical target is verified.", 0.50, ["scan_next_sector"])
