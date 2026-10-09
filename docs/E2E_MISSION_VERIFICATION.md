# Executable End-to-End Flood Mission Reference

## What this delivers

This change adds a reproducible software vertical slice:

1. Read a versioned mission packet from JSON.
2. Validate the occupancy grid, coordinates, sensor-health flags and emergency-stop state.
3. Fail closed if any declared sensor is unhealthy or the emergency stop is active.
4. Plan a deterministic four-connected grid route around blocked cells and supplied hazard cells.
5. Check whether a supplied person-candidate record exists.
6. Emit an explicit status, route, safety/review state, limitations and SHA-256 integrity digest.
7. Verify the report and exercise the CLI in automated tests.

This is an **executable simulation/data-contract baseline**, not proof of a complete autonomous physical robot. The grid and person candidates are provided by the input file; the module does not run a detector, build a map from raw sensors, estimate water current/depth, run ROS 2/Nav2, or move hardware.

## Run it

From the repository root with Python 3.10+:

```bash
python -m flood_robot.e2e_mission --input examples/e2e_flood_mission.json --output mission-report.json
python -c "import json; from flood_robot.e2e_mission import verify_report; r=json.load(open('mission-report.json', encoding='utf-8')); print('integrity_ok=', verify_report(r), 'status=', r['status'])"
```

The module uses only the Python standard library. Run its tests with pytest installed:

```bash
python -m pytest tests/test_e2e_mission.py -q
```

Expected successful example status: `PLAN_READY_FOR_REVIEW`. This means only that the supplied synthetic input passed the reference checks and a grid route was found. It does **not** mean a real person was detected or that the route is safe in floodwater.

## Fail-closed behavior

- Sensor-health entry missing/false/non-true: the mission abstains.
- Emergency stop active: the mission abstains and does not propose a route.
- No route: status is `NO_SAFE_ROUTE`.
- No valid person candidate: status is `HUMAN_REVIEW`.
- Every report requires human review and sets `actuator_authorized=false`.
- No function in this module issues a robot-control command.

The SHA-256 field detects accidental changes when verified against the report content. It is not keyed, signed, authenticated or tamper-proof against an actor who can rewrite both the report and digest.

## Next integration gates before claiming real end-to-end

1. Replace synthetic grid input with timestamped, calibrated ROS 2 sensor messages and health diagnostics.
2. Integrate a validated perception adapter; track person candidates with timestamps, bounding boxes/3D positions, confidence calibration and provenance.
3. Build and maintain a map from tested SLAM/depth/LiDAR components; propagate uncertainty and unknown space.
4. Replace this 2D grid reference with Nav2 costmaps/planners and validated flood-specific no-go constraints.
5. Add simulation tests in Gazebo or Isaac Sim, including sensor dropout, glare, darkness, current, map drift, communications loss and blocked routes.
6. Run software-in-the-loop, hardware-in-the-loop and supervised field trials with quantitative metrics.
7. Validate an independent hardware emergency stop and deterministic safety controller. AI outputs must never bypass them.
8. Pin dependency/model versions, review all licenses, produce an SBOM, and publish reproducible benchmark results.

Do not connect this reference planner directly to motors, thrusters, manipulators or autonomous deployment. Physical deployment remains disabled until the above gates are reviewed and passed.
