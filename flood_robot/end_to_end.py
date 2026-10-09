"""Safety-gated end-to-end flood-rescue assessment baseline.

This deterministic software reference consumes normalized, upstream perception
hypotheses. It does not detect victims itself, simulate flood physics, or control
robot actuators. All mission actions remain proposals pending human review and
independent, validated collision/safety checks.
"""
from __future__ import annotations

from dataclasses import asdict, dataclass, field
from datetime import datetime
import hashlib
import json
from typing import Any, Iterable


@dataclass(frozen=True)
class RescueObservation:
    sensor_id: str
    modality: str
    timestamp: str
    quality: float
    candidates: tuple[dict[str, Any], ...] = ()
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass(frozen=True)
class EndToEndConfig:
    min_sensor_quality: float = 0.5
    max_timestamp_skew_seconds: float = 2.0
    min_victim_confidence: float = 0.65
    max_hazard_distance_m: float = 2.0


@dataclass
class RescueReport:
    status: str
    mission_id: str
    accepted_observations: int
    rejected_observations: int
    modalities: list[str]
    victim_hypotheses: list[dict[str, Any]]
    hazard_hypotheses: list[dict[str, Any]]
    plan_proposal: dict[str, Any]
    human_review_required: bool
    collision_check_verified: bool
    actuator_commands_sent: bool
    reasons: list[str]
    evidence_id: str
    audit_record: dict[str, Any]

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def _parse_time(value: str) -> datetime:
    parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    if parsed.tzinfo is None:
        from datetime import timezone
        parsed = parsed.replace(tzinfo=timezone.utc)
    return parsed


def _evidence_id(payload: dict[str, Any]) -> str:
    raw = json.dumps(payload, sort_keys=True, separators=(",", ":"), default=str).encode()
    return "rescue-" + hashlib.sha256(raw).hexdigest()[:16]


class EndToEndRescuePipeline:
    """Quality gate → scene hypotheses → risk flags → plan proposal → audit."""

    def __init__(self, config: EndToEndConfig | None = None):
        self.config = config or EndToEndConfig()

    def run(
        self,
        observations: Iterable[RescueObservation | dict[str, Any]],
        *,
        mission_id: str = "demo-mission",
        now: str | None = None,
        collision_check_passed: bool = False,
        human_approved: bool = False,
    ) -> RescueReport:
        received = [
            item if isinstance(item, RescueObservation) else RescueObservation(**item)
            for item in observations
        ]
        reasons: list[str] = []
        accepted: list[RescueObservation] = []
        rejected = 0
        for obs in received:
            reason = None
            if not obs.sensor_id or not obs.modality:
                reason = "missing_sensor_identity_or_modality"
            elif not 0.0 <= obs.quality <= 1.0:
                reason = "invalid_sensor_quality"
            elif obs.quality < self.config.min_sensor_quality:
                reason = "sensor_quality_below_threshold"
            else:
                try:
                    _parse_time(obs.timestamp)
                except (TypeError, ValueError):
                    reason = "invalid_timestamp"
            if reason:
                rejected += 1
                reasons.append(f"{obs.sensor_id or 'unknown'}:{reason}")
            else:
                accepted.append(obs)

        if accepted:
            times = [_parse_time(x.timestamp) for x in accepted]
            if (max(times) - min(times)).total_seconds() > self.config.max_timestamp_skew_seconds:
                rejected += len(accepted)
                accepted = []
                reasons.append("temporal_alignment_failed")

        victims: dict[str, dict[str, Any]] = {}
        hazards: dict[str, dict[str, Any]] = {}
        for obs in accepted:
            for raw in obs.candidates:
                kind = str(raw.get("kind", "unknown")).lower()
                confidence = raw.get("confidence", 0.0)
                if not isinstance(confidence, (int, float)) or not 0 <= confidence <= 1:
                    reasons.append("candidate_confidence_invalid")
                    continue
                item = dict(raw)
                item["source_sensor"] = obs.sensor_id
                item["source_modality"] = obs.modality.lower()
                if kind in {"person", "victim_candidate"}:
                    if confidence >= self.config.min_victim_confidence:
                        victims[str(raw.get("object_id", f"{obs.sensor_id}-victim-{len(victims)}"))] = item
                elif kind in {"hazard", "debris", "floodwater", "unstable_structure"}:
                    hazards[str(raw.get("object_id", f"{obs.sensor_id}-hazard-{len(hazards)}"))] = item

        modalities = sorted({x.modality.lower() for x in accepted})
        if not accepted:
            status = "SAFE_HOLD"
            reasons.append("no_usable_synchronized_sensor_evidence")
        elif not victims:
            status = "HUMAN_REVIEW"
            reasons.append("no_supported_victim_candidate")
        elif not collision_check_passed:
            status = "BLOCKED"
            reasons.append("independent_collision_check_not_verified")
        elif not human_approved:
            status = "HUMAN_REVIEW"
            reasons.append("human_mission_approval_required")
        else:
            status = "PROPOSAL_APPROVED_NOT_EXECUTED"
            reasons.append("proposal_approved_but_no_actuator_interface_exists")

        plan = {
            "action": "inspect_victim_candidates" if victims else "reobserve_scene",
            "target_ids": sorted(victims),
            "status": "PROPOSAL_ONLY",
            "requires_independent_collision_check": True,
            "requires_human_review": True,
        }
        payload = {
            "mission_id": mission_id,
            "status": status,
            "accepted": len(accepted),
            "rejected": rejected,
            "modalities": modalities,
            "victims": victims,
            "hazards": hazards,
            "plan": plan,
            "reasons": reasons,
        }
        record = {
            "mission_id": mission_id,
            "generated_at": now or datetime.now().astimezone().isoformat(),
            "evidence_digest": _evidence_id(payload),
            "disclaimer": "Perception hypotheses are unvalidated inputs, not verified victims or hazards.",
            "human_review_required": True,
            "actuator_commands_sent": False,
        }
        return RescueReport(
            status=status,
            mission_id=mission_id,
            accepted_observations=len(accepted),
            rejected_observations=rejected,
            modalities=modalities,
            victim_hypotheses=list(victims.values()),
            hazard_hypotheses=list(hazards.values()),
            plan_proposal=plan,
            human_review_required=True,
            collision_check_verified=bool(collision_check_passed),
            actuator_commands_sent=False,
            reasons=reasons,
            evidence_id=_evidence_id(payload),
            audit_record=record,
        )


def verify_rescue_report(report: RescueReport) -> list[str]:
    """Return invariant violations; an empty list means only internal checks passed."""
    errors = []
    if report.actuator_commands_sent:
        errors.append("actuator_commands_must_remain_disabled")
    if not report.human_review_required:
        errors.append("human_review_must_be_required")
    if report.status == "PROPOSAL_APPROVED_NOT_EXECUTED" and not report.collision_check_verified:
        errors.append("approved_proposal_requires_collision_check")
    if not report.evidence_id.startswith("rescue-"):
        errors.append("missing_evidence_id")
    return errors
