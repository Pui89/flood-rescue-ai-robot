# RescueBot Open-Source Roadmap

## Stage 0 — baseline
- [x] Dependency-free synthetic evidence grid.
- [x] JSON export and unit tests.
- [ ] Run tests locally in a clean environment.
- [ ] Confirm CI result after the workflow runs.

## Stage 1 — data contracts
- Define observations with timestamps, frame IDs, sensor health, calibration IDs, and provenance.
- Define map schema with origin, resolution, dimensions, frame, timestamp, and unknown representation.
- Add schema and compatibility tests.
- Distinguish model scores from calibrated probabilities.

## Stage 2 — evaluation
- Add permissioned, versioned labelled data or synthetic fixtures.
- Define map-cell metrics and spatial localization error.
- Report false positives, false negatives, and unknown coverage.
- Record commit, configuration, environment, and output hashes. Never invent results.

## Stage 3 — ROS 2 adapter
- Target Ubuntu 24.04 + ROS 2 Jazzy + Gazebo Harmonic after checking compatibility.
- Create typed ROS 2 messages and an adapter node.
- Add bag replay, timestamps, frame IDs, QoS, and stale-message rejection.
- Integrate Gazebo through ros_gz while keeping simulator dependencies optional for pure-Python tests.

## Stage 4 — simulation scenarios
- Add a simple mobile base and controlled test world.
- Simulate sensor dropout, occlusion, delayed messages, localization degradation, and network loss.
- Record maps and robot state without hazardous behaviors.
- Test safe-stop and unknown-space handling.

## Stage 5 — hardware-in-the-loop
- Only after simulation acceptance, connect real sensors and a robot.
- Verify emergency stop and independent watchdog.
- Perform controlled tests with trained operators and written hazard analysis.
- Obtain independent review before any deployment near floodwater or rescue operations.
