import copy
import json
import subprocess
import sys
from pathlib import Path

import pytest

from flood_robot.e2e_mission import plan_grid_route, run_mission, verify_report

ROOT = Path(__file__).resolve().parents[1]


def example():
    return json.loads((ROOT / "examples/e2e_flood_mission.json").read_text(encoding="utf-8"))


def test_example_mission_produces_safe_reviewable_route():
    report = run_mission(example())
    assert report["status"] == "PLAN_READY_FOR_REVIEW"
    assert report["execution_mode"] == "SIMULATION_ONLY"
    assert report["human_review_required"] is True
    assert report["actuator_authorized"] is False
    assert report["route"][0] == [0, 0]
    assert report["route"][-1] == [6, 6]
    assert report["evidence_sha256"]
    assert verify_report(report)


def test_unhealthy_sensor_fails_closed():
    mission = example()
    mission["sensor_health"]["lidar"] = False
    report = run_mission(mission)
    assert report["status"] == "ABSTAIN"
    assert report["route"] is None
    assert report["actuator_authorized"] is False


def test_emergency_stop_blocks_route_proposal():
    mission = example()
    mission["emergency_stop"] = True
    report = run_mission(mission)
    assert report["status"] == "ABSTAIN"
    assert report["safety_gate"] == "BLOCKED"


def test_no_person_candidate_requires_review():
    mission = example()
    mission["detections"] = []
    assert run_mission(mission)["status"] == "HUMAN_REVIEW"


def test_blocked_goal_has_no_route():
    assert plan_grid_route([[0, 1], [0, 0]], [0, 0], [0, 1]) is None


def test_hazard_cells_are_not_traversed():
    route = plan_grid_route([[0, 0, 0], [0, 0, 0], [0, 0, 0]], [0, 0], [2, 2], [[1, 1]])
    assert route is not None
    assert [1, 1] not in route


def test_report_tampering_is_detected():
    report = run_mission(example())
    edited = copy.deepcopy(report)
    edited["route_steps"] = 999
    assert not verify_report(edited)


def test_cli_writes_machine_readable_report(tmp_path):
    output = tmp_path / "report.json"
    result = subprocess.run(
        [sys.executable, "-m", "flood_robot.e2e_mission",
         "--input", str(ROOT / "examples/e2e_flood_mission.json"),
         "--output", str(output)],
        cwd=ROOT, capture_output=True, text=True, check=False,
    )
    assert result.returncode == 0, result.stderr
    report = json.loads(output.read_text(encoding="utf-8"))
    assert verify_report(report)
    assert report["mission_id"] == "demo-flood-001"


def test_invalid_grid_is_rejected():
    with pytest.raises(ValueError, match="rectangular"):
        plan_grid_route([[0, 0], [0]], [0, 0], [1, 1])
