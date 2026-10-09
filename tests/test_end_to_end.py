from flood_robot.end_to_end import EndToEndRescuePipeline, verify_rescue_report

T0 = "2026-10-10T00:00:00+00:00"


def obs(sensor_id, modality, candidates=(), *, quality=0.9, timestamp=T0):
    return {
        "sensor_id": sensor_id,
        "modality": modality,
        "timestamp": timestamp,
        "quality": quality,
        "candidates": candidates,
    }


def victim():
    return {"object_id": "person-01", "kind": "victim_candidate", "confidence": 0.91,
            "position_xyz_m": [1.0, 2.0, 0.0]}


def test_full_path_is_only_approved_proposal_and_never_moves_robot():
    report = EndToEndRescuePipeline().run(
        [obs("rgb-1", "rgb", [victim()]), obs("depth-1", "depth", [victim()])],
        mission_id="test-01", now=T0, collision_check_passed=True, human_approved=True,
    )
    assert report.status == "PROPOSAL_APPROVED_NOT_EXECUTED"
    assert report.human_review_required is True
    assert report.actuator_commands_sent is False
    assert report.collision_check_verified is True
    assert report.evidence_id.startswith("rescue-")
    assert verify_rescue_report(report) == []


def test_collision_check_missing_blocks_plan():
    report = EndToEndRescuePipeline().run(
        [obs("rgb-1", "rgb", [victim()]), obs("depth-1", "depth", [victim()])],
        now=T0,
    )
    assert report.status == "BLOCKED"
    assert "independent_collision_check_not_verified" in report.reasons
    assert report.actuator_commands_sent is False


def test_low_quality_or_unsynchronized_inputs_safe_hold():
    report = EndToEndRescuePipeline().run(
        [obs("rgb-1", "rgb", [victim()], quality=0.1)],
        now=T0,
    )
    assert report.status == "SAFE_HOLD"
    assert report.accepted_observations == 0
    assert report.actuator_commands_sent is False

    misaligned = EndToEndRescuePipeline().run([
        obs("rgb-1", "rgb", [victim()]),
        obs("depth-1", "depth", [victim()], timestamp="2026-10-10T00:00:10+00:00"),
    ], now=T0)
    assert misaligned.status == "SAFE_HOLD"
    assert "temporal_alignment_failed" in misaligned.reasons


def test_report_is_json_serializable_and_keeps_human_review():
    import json
    report = EndToEndRescuePipeline().run([obs("rgb-1", "rgb", [victim()])], now=T0)
    assert json.loads(json.dumps(report.to_dict()))["human_review_required"] is True
    assert report.actuator_commands_sent is False
