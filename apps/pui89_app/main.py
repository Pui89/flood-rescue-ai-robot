"""PUI89 flood reconnaissance and human-supervised decision-support API."""
from __future__ import annotations

from collections import Counter
from typing import Literal

from fastapi import FastAPI
from pydantic import BaseModel, Field

app = FastAPI(title="PUI89 Flood Rescue AI", version="1.0.0",
              description="Flood reconnaissance evidence review. No autonomous rescue or actuator control.")
COUNTERS: Counter[str] = Counter()


class Candidate(BaseModel):
    track_id: str = Field(min_length=1, max_length=80)
    visual_confidence: float = Field(ge=0, le=1)
    thermal_support: bool = False
    track_stability_frames: int = Field(ge=0)
    distance_m: float = Field(ge=0)


class AnalyzeRequest(BaseModel):
    rgb_available: bool
    thermal_available: bool
    lidar_valid: bool
    timestamp_skew_ms: float = Field(ge=0)
    water_depth_m: float = Field(ge=0)
    current_speed_mps: float = Field(ge=0)
    candidates: list[Candidate] = Field(default_factory=list, max_length=500)


@app.get("/health")
def health():
    return {"status": "ok", "service": "flood-rescue-ai", "actuator_authority": False}


@app.get("/metrics")
def metrics():
    return {"requests_total": COUNTERS["analyze"], "metric_type": "service counters, not model-performance benchmarks"}


@app.post("/analyze")
def analyze(req: AnalyzeRequest):
    COUNTERS["analyze"] += 1
    sensor_reasons = []
    if not req.rgb_available:
        sensor_reasons.append("RGB_UNAVAILABLE")
    if not req.lidar_valid:
        sensor_reasons.append("LIDAR_INVALID")
    if req.timestamp_skew_ms > 50:
        sensor_reasons.append("TIMESTAMP_SKEW_EXCEEDED")
    if sensor_reasons:
        return {"status": "SAFE_HOLD", "sensor_reasons": sensor_reasons,
                "candidate_reviews": [], "route_status": "NOT_EVALUATED",
                "actuator_commands_sent": False}

    # Conservative illustrative limits; deployments must configure and validate them.
    hazard_reasons = []
    if req.water_depth_m > 0.30:
        hazard_reasons.append("WATER_DEPTH_ABOVE_ILLUSTRATIVE_LIMIT")
    if req.current_speed_mps > 0.30:
        hazard_reasons.append("CURRENT_ABOVE_ILLUSTRATIVE_LIMIT")
    route_status = "HUMAN_REVIEW" if hazard_reasons else "NOT_VALIDATED"
    reviews = []
    for c in req.candidates:
        reasons = []
        if c.visual_confidence < 0.75:
            reasons.append("VISUAL_EVIDENCE_UNCERTAIN")
        if req.thermal_available and not c.thermal_support:
            reasons.append("NO_THERMAL_CORROBORATION")
        if c.track_stability_frames < 4:
            reasons.append("TRACK_UNSTABLE")
        score = round(0.60 * c.visual_confidence
                      + 0.25 * float(c.thermal_support)
                      + 0.15 * min(c.track_stability_frames / 10, 1), 4)
        status: Literal["HUMAN_REVIEW", "INSUFFICIENT_EVIDENCE"] = (
            "HUMAN_REVIEW" if not reasons else "INSUFFICIENT_EVIDENCE")
        reviews.append({"track_id": c.track_id, "status": status,
                        "evidence_score": score, "reasons": reasons})
    reviews.sort(key=lambda x: x["evidence_score"], reverse=True)
    return {"status": "ANALYZED", "hazard_reasons": hazard_reasons,
            "route_status": route_status, "candidate_reviews": reviews,
            "actuator_commands_sent": False,
            "limitations": ["Evidence scores are heuristic, not calibrated probabilities.",
                            "No route is certified safe; trained human rescue authority remains essential."]}
