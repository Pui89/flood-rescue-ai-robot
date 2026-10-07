# Engineering Roadmap

## Mission

Build a safety-aware multimodal flood-rescue robotics platform that can perceive degraded environments, maintain a time-varying world model, propose rescue missions, and execute only through deterministic safety-controlled robotics interfaces.

## Reference architecture

Sensors -> synchronization and calibration -> perception / segmentation / tracking -> multimodal evidence fusion -> 3D/4D world model -> victim and hazard assessment -> uncertainty / OOD / abstention -> mission proposal -> human review / policy -> deterministic safety gate -> ROS 2 / Nav2 / hardware abstraction -> action verification and audit.

**AI proposes. Deterministic robotics validates. Safety controls.**

## Professionalization priorities

1. Reproducible Python packaging and dependency profiles.
2. Continuous integration, linting, tests, coverage and supply-chain checks.
3. Sensor timestamps, calibration IDs, coordinate frames, health and provenance on every observation.
4. Explicit uncertainty, abstention, unknown and sensor-conflict states.
5. Grounded victim/hazard tracking with temporal continuity.
6. A versioned 3D/4D world model and evidence record.
7. Simulation and hardware-in-the-loop before physical deployment.
8. Human-supervised mission management.
9. Deterministic collision, reachability, exclusion-zone and emergency-stop gates.
10. Reproducible evaluation across perception, tracking, navigation, robustness and safety.
11. Release artifacts with provenance and SBOM metadata.

## Mission state machine

SEARCH -> LOCATE -> VERIFY -> PRIORITIZE -> PLAN -> REQUEST_APPROVAL -> EXECUTE -> VERIFY_OUTCOME -> REPORT

High-risk, contradictory, missing-sensor or out-of-distribution situations should transition to REQUEST_APPROVAL or HOLD, not autonomous execution.

## Model responsibility boundaries

| Component | Responsibility | Actuation authority |
|---|---|---|
| Detector | Fast object evidence | None |
| Segmentation | Pixel/region evidence | None |
| Thermal/NIR/depth/LiDAR | Complementary sensing | None |
| Qwen/Gemma | Evidence-grounded reasoning | None |
| Temporal/world model | State estimation and forecasting | None |
| VLA candidate | Proposed action | None |
| Nav2 / deterministic planner | Validated navigation command | Constrained |
| Safety gate | Collision/risk/authorization checks | Authoritative |
| E-stop | Emergency stop | Independent |

## Evaluation gates

Every new model or hardware configuration should report model version, dataset version, calibration version, Git SHA, runtime environment, sensor health, latency, uncertainty behavior and failure cases. Never publish synthetic or illustrative numbers as field validation.

## Release progression

Prototype -> multimodal perception -> 3D/4D world model -> simulation -> navigation -> human-supervised rescue -> hardware-in-loop -> field-validation candidate -> engineering release.
