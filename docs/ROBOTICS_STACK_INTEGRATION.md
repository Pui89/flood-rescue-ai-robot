# Robotics stack integration: ROS 2, Nav2, Gazebo Sim and Open3D

## Status and scope

This document defines the intended integration boundary and staged implementation. It does **not** claim that the four projects are already installed, wired to hardware, or validated. ROS 2 nodes, driver packages, robot descriptions, and controller configuration must be implemented and tested against the actual hardware and chosen ROS 2 distribution.

Use ROS 2 as the sensor/control interface, Nav2 for mobile reconnaissance navigation, Gazebo Sim for reproducible disaster-scene testing, and Open3D for point-cloud processing and 3D hazard mapping.

## Components and licenses

| Component | Role in this repository | Upstream project | Upstream license |
|---|---|---|---|
| ROS 2 | Middleware, typed messages, services/actions, TF transforms, lifecycle and diagnostics | [ros2/ros2](https://github.com/ros2/ros2) | Apache-2.0 |
| Nav2 | Mobile-base localization/navigation, costmaps, planning and behavior trees; use only where a mobile base exists | [ros-navigation/navigation2](https://github.com/ros-navigation/navigation2) | Apache-2.0 |
| Gazebo Sim | Physics/sensor simulation and repeatable robot-scene testing | [gazebosim/gz-sim](https://github.com/gazebosim/gz-sim) | Apache-2.0 |
| Open3D | Point-cloud filtering, registration and 3D geometry processing | [isl-org/Open3D](https://github.com/isl-org/Open3D) | MIT |

Check the exact release tag and transitive dependency licenses before distributing a product. These are upstream project licenses, not a substitute for auditing the installed package set.

## Architecture

```text
Cameras / LiDAR / IMU / GNSS
  -> ROS 2 drivers + time synchronization + TF
  -> perception / victim hypotheses / hazard extraction
  -> Open3D point-cloud processing + 3D map
  -> Nav2 costmaps + planner + controller
  -> deterministic safety supervisor
  -> base controller
  -> mission state + telemetry + human-reviewed report

Gazebo Sim + ROS-Gazebo bridge:
  flood-like terrain / obstacles / sensor dropouts / communication faults
```

## Staged implementation

1. **Environment baseline:** choose one supported ROS 2 distribution and matching Ubuntu / Gazebo release. Pin OS image, package versions, Python environment and model artifacts in the deployment record.
2. **ROS 2 interface contract:** define topic/action/service names, message types, units, timestamps, frame IDs, QoS and lifecycle behavior. Keep hardware drivers separate from model logic.
3. **Simulation:** add a versioned URDF/Xacro or SDF robot model, sensor models, world files and launch configuration. Bridge only the required Gazebo topics.
4. **Perception / geometry:** use Open3D only for valid point-cloud data; document calibration, coordinate frames, units and confidence/uncertainty.
5. **Navigation:** configure Nav2 only for a mobile base. Use conservative behavior around unknown space and fail closed when required sensors or transforms are unavailable.
6. **Safety boundary:** AI proposes; deterministic checks validate; controllers execute; independent state/telemetry verifies the result. Include a hardware emergency stop for physical testing.
7. **Hardware-in-the-loop:** validate one subsystem at a time before complete missions. Simulation results must be reported separately from real-robot results.

### Flood-rescue-specific integration order
1. Establish timestamp, frame ID, sensor-health and calibration contracts for every input.
2. Build a correct TF tree and verify map/odom/base and sensor frames before evaluating navigation.
3. Use Open3D for point-cloud filtering, registration and geometry-derived obstacles only after validating units and sensor calibration.
4. Feed Nav2 a conservative, uncertainty-aware costmap; unobserved or unreliable regions must not be silently treated as safe.
5. Use Gazebo Sim to test blocked routes, degraded sensing, localization loss, communication loss, emergency stop and return-to-safe-state behavior.
6. Keep victim detections as hypotheses with confidence and evidence; require human review for consequential rescue decisions.
7. Report mission success, map/localization error, victim precision/recall, time-to-observation, route completion, energy and safe-stop/recovery outcomes.

## Environment preflight

A small environment checker is provided at `tools/check_robotics_stack.py`. Run it from a shell with the chosen ROS 2 environment sourced:

```bash
source /opt/ros/$ROS_DISTRO/setup.bash
python tools/check_robotics_stack.py
# Use --strict in a configured deployment image / CI environment:
python tools/check_robotics_stack.py --strict
```

The checker verifies discoverability of the ROS 2 CLI, Nav2 packages, Gazebo ROS bridge packages, Gazebo Sim CLI, and the Open3D Python module. It is not an end-to-end integration test. Package availability and command behavior can vary by ROS 2 / Gazebo distribution; use the official installation instructions and lock the exact versions for your chosen target.

- [ROS 2 documentation](https://docs.ros.org/)
- [Nav2 documentation](https://docs.nav2.org/)
- [Gazebo documentation](https://gazebosim.org/docs/)
- [Open3D documentation](https://www.open3d.org/docs/)

## Acceptance gates before claiming integration

- A clean environment can install the pinned dependencies from documented steps.
- Automated tests verify topic/message contracts, frame IDs, timestamps, units and missing-data behavior.
- Simulation launches deterministically and sensor topics are bridged as expected.
- Failure-injection tests cover stale data, missing transforms, sensor dropout, communications loss and emergency stop.
- Hardware tests report latency, CPU/GPU/RAM/power, mission success and failures under documented conditions.
- Benchmark reports label each result as simulation, recorded-data replay, or real hardware.

Do not report the stack as "integrated" or "production-ready" until the relevant acceptance gates pass on the intended platform.
