"""Deterministic, simulation-only flood mission pipeline.

This module proves a bounded software path from a JSON mission packet to a
route proposal and auditable report. It does NOT perform camera perception,
sensor fusion, ROS control, or physical actuation.
"""
from __future__ import annotations

import argparse
import hashlib
import heapq
import json
from pathlib import Path
from typing import Any


def _canonical_json(value: Any) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False)


def _validate_grid(grid: list[list[int]]) -> tuple[int, int]:
    if not grid or not grid[0]:
        raise ValueError("grid must be a non-empty rectangular matrix")
    width = len(grid[0])
    if any(len(row) != width for row in grid):
        raise ValueError("grid must be rectangular")
    if any(cell not in (0, 1) for row in grid for cell in row):
        raise ValueError("grid cells must be 0 (free) or 1 (blocked)")
    return len(grid), width


def _inside(point: list[int] | tuple[int, int], height: int, width: int) -> bool:
    return (
        isinstance(point, (list, tuple))
        and len(point) == 2
        and all(isinstance(v, int) and not isinstance(v, bool) for v in point)
        and 0 <= point[0] < height
        and 0 <= point[1] < width
    )


def plan_grid_route(
    grid: list[list[int]],
    start: list[int],
    goal: list[int],
    hazard_cells: list[list[int]] | None = None,
) -> list[list[int]] | None:
    """Return a deterministic 4-connected shortest route, or None if blocked."""
    height, width = _validate_grid(grid)
    if not _inside(start, height, width) or not _inside(goal, height, width):
        raise ValueError("start and goal must be in-bounds [row, column] coordinates")
    hazards = hazard_cells or []
    if any(not _inside(p, height, width) for p in hazards):
        raise ValueError("hazard cell is outside the grid")
    blocked = {
        (r, c)
        for r in range(height)
        for c in range(width)
        if grid[r][c] == 1
    }
    blocked.update((p[0], p[1]) for p in hazards)
    s, g = tuple(start), tuple(goal)
    if s in blocked or g in blocked:
        return None

    def heuristic(p: tuple[int, int]) -> int:
        return abs(p[0] - g[0]) + abs(p[1] - g[1])

    queue: list[tuple[int, int, tuple[int, int]]] = [(heuristic(s), 0, s)]
    came_from: dict[tuple[int, int], tuple[int, int] | None] = {s: None}
    cost = {s: 0}
    while queue:
        _, current_cost, current = heapq.heappop(queue)
        if current_cost != cost.get(current):
            continue
        if current == g:
            path = []
            node: tuple[int, int] | None = current
            while node is not None:
                path.append([node[0], node[1]])
                node = came_from[node]
            return list(reversed(path))
        for nxt in sorted(
            [(current[0] - 1, current[1]), (current[0], current[1] - 1),
             (current[0], current[1] + 1), (current[0] + 1, current[1])]
        ):
            if not (0 <= nxt[0] < height and 0 <= nxt[1] < width) or nxt in blocked:
                continue
            new_cost = current_cost + 1
            if new_cost < cost.get(nxt, 10**12):
                cost[nxt] = new_cost
                came_from[nxt] = current
                heapq.heappush(queue, (new_cost + heuristic(nxt), new_cost, nxt))
    return None


def run_mission(mission: dict[str, Any]) -> dict[str, Any]:
    """Run the reference mission and emit a fail-closed, integrity-checksummed report."""
    required = {"mission_id", "sensor_health", "grid", "start", "goal"}
    missing = sorted(required - mission.keys())
    if missing:
        raise ValueError(f"missing required mission fields: {', '.join(missing)}")
    if not isinstance(mission["sensor_health"], dict):
        raise ValueError("sensor_health must be an object")
    health = mission["sensor_health"]
    unhealthy = sorted(name for name, ok in health.items() if ok is not True)
    emergency_stop = mission.get("emergency_stop", False)
    if not isinstance(emergency_stop, bool):
        raise ValueError("emergency_stop must be boolean")

    grid = mission["grid"]
    height, width = _validate_grid(grid)
    start, goal = mission["start"], mission["goal"]
    hazards = mission.get("hazard_cells", [])
    if not isinstance(hazards, list):
        raise ValueError("hazard_cells must be a list")
    route = None
    if not unhealthy and not emergency_stop:
        route = plan_grid_route(grid, start, goal, hazards)

    detections = mission.get("detections", [])
    if not isinstance(detections, list):
        raise ValueError("detections must be a list")
    victim_candidates = [
        d for d in detections
        if isinstance(d, dict)
        and d.get("class_name") == "person_candidate"
        and isinstance(d.get("confidence"), (int, float))
        and not isinstance(d.get("confidence"), bool)
        and 0.0 <= d["confidence"] <= 1.0
    ]
    if unhealthy or emergency_stop:
        decision, reason = "ABSTAIN", "sensor_health_failure" if unhealthy else "emergency_stop_active"
    elif route is None:
        decision, reason = "NO_SAFE_ROUTE", "route_unavailable_or_blocked"
    elif not victim_candidates:
        decision, reason = "HUMAN_REVIEW", "no_valid_person_candidate"
    else:
        decision, reason = "PLAN_READY_FOR_REVIEW", "candidate_route_requires_operator_review"

    report: dict[str, Any] = {
        "schema_version": "pui89.flood-mission-report.v1",
        "mission_id": str(mission["mission_id"]),
        "status": decision,
        "reason": reason,
        "grid_shape": [height, width],
        "sensor_health": health,
        "unhealthy_sensors": unhealthy,
        "emergency_stop": emergency_stop,
        "person_candidates": len(victim_candidates),
        "route": route,
        "route_steps": max(0, len(route) - 1) if route else None,
        "safety_gate": "BLOCKED" if decision in {"ABSTAIN", "NO_SAFE_ROUTE"} else "REVIEW_REQUIRED",
        "execution_mode": "SIMULATION_ONLY",
        "human_review_required": True,
        "actuator_authorized": False,
        "limitations": [
            "Grid and detections are supplied inputs, not live perception outputs.",
            "This reference planner is not a validated flood-current, water-depth, or terrain model.",
            "No ROS command or physical actuator is invoked.",
        ],
    }
    report["evidence_sha256"] = hashlib.sha256(_canonical_json(report).encode("utf-8")).hexdigest()
    return report


def verify_report(report: dict[str, Any]) -> bool:
    """Verify report integrity against accidental edits; this is not a signature."""
    digest = report.get("evidence_sha256")
    if not isinstance(digest, str):
        return False
    unsigned = {key: value for key, value in report.items() if key != "evidence_sha256"}
    expected = hashlib.sha256(_canonical_json(unsigned).encode("utf-8")).hexdigest()
    return digest == expected


def main() -> None:
    parser = argparse.ArgumentParser(description="Run the simulation-only PUI89 flood mission pipeline")
    parser.add_argument("--input", required=True, help="Path to a mission JSON file")
    parser.add_argument("--output", default="-", help="Output report JSON path, or '-' for stdout")
    args = parser.parse_args()
    mission = json.loads(Path(args.input).read_text(encoding="utf-8"))
    report = run_mission(mission)
    serialized = json.dumps(report, indent=2, ensure_ascii=False) + "\n"
    if args.output == "-":
        print(serialized, end="")
    else:
        Path(args.output).write_text(serialized, encoding="utf-8")
    if not verify_report(report):
        raise SystemExit("internal report integrity verification failed")


if __name__ == "__main__":
    main()
