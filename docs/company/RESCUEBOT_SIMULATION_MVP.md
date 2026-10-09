# RescueBot Simulation MVP

## Goal

Create a small, testable baseline on a computer without physical hardware. This first increment aggregates synthetic, labelled reconnaissance observations into a 2D evidence grid. It is a prerequisite to ROS 2/Gazebo integration, not a substitute for it.

## Included

- Dependency-free Python evidence grid.
- Configurable dimensions and resolution.
- Rejection of invalid and out-of-bounds observations.
- Per-cell counts, labels, source provenance, and mean input score.
- Explicit unknown-cell count and JSON export.
- Standard-library unit tests.

## Run from repository root

    python -m simulation.rescue_mapping.demo --output /tmp/pui89-rescue-map.json
    python -m unittest discover -s tests/rescue_mapping -v

Python 3.10+ is required. No GPU or ROS 2 installation is needed for this baseline.

## Next integration

For Ubuntu 24.04, consider ROS 2 Jazzy with Gazebo Harmonic after checking current compatibility. References: https://docs.ros.org/en/jazzy/ and https://gazebosim.org/docs/harmonic/ros2_integration/ and https://github.com/gazebosim/ros_gz.

Planned modules: typed interfaces, mapping adapter, sensor-health checks, simulation bringup, and evaluation. Do not treat unknown cells as safe. Before navigation, test unknown-space policy, obstacle inflation, map-age limits, frame transforms, localization gates, emergency stop, and communication-loss behavior.

## Acceptance criteria

- Unit tests pass on supported Python.
- Demo writes valid JSON and repeat runs are deterministic.
- Invalid coordinates and scores fail explicitly.
- Documentation distinguishes synthetic inputs from real sensing.
- No actuator commands are produced.

## Non-goals

No flood simulation fidelity, person detection, rescue capability, SLAM, autonomous navigation, real-time performance, or physical safety claim is made.
