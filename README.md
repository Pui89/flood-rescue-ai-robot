# Flood Rescue AI Robot

A safety-aware multimodal perception and robotics platform for flood rescue operations. The repository combines depth estimation, multi-object tracking, spatial hazard extraction, embodied AI, multimodal reasoning, world modeling and safety-aware robot action planning.

## Overview

## Professional Engineering Baseline

This repository is being developed as a safety-aware multimodal flood-rescue robotics platform. The engineering boundary is:

**AI proposes -> deterministic robotics validates -> safety system controls -> action is verified and logged.**

Key professional layers now documented in the repository:

- reproducible Python packaging with runtime, development and GPU dependency profiles;
- CI/security hardening with linting, tests, coverage, dependency review, CodeQL and Dependabot;
- sensor synchronization, calibration, health and provenance as first-class deployment requirements;
- explicit uncertainty, OOD, abstention and human-review states;
- 3D/4D world-model and evidence-provenance direction;
- simulation-first validation and a flood-specific robustness scenario matrix;
- deterministic collision, reachability, exclusion-zone and emergency-stop boundaries;
- benchmark definitions covering perception, tracking, navigation, robustness, calibration and safety.

See:

- [Engineering roadmap](docs/ENGINEERING_ROADMAP.md)
- [Safety architecture](docs/SAFETY_ARCHITECTURE.md)
- [Evaluation benchmark](docs/EVALUATION_BENCHMARK.md)
- [Simulation scenarios](docs/SIMULATION_SCENARIOS.md)

**Implementation status:** prototype/research engineering. No capability is presented as field-validated unless repeatable measurements are available.


Flood rescue requires robots to perceive unstable terrain, detect victims, avoid obstacles, and prioritize safe navigation under poor visual conditions. This project models that pipeline in a modular, deployable way.

## 3D Robot Concept

![Flood rescue robot concept](docs/robot_concept.svg)

![3D Flood Rescue AI Robot](docs/robot_concept_3d.svg)

**Concept features:** amphibious flotation and thrusters, RGB-D/thermal/NIR/LiDAR perception, rescue manipulator, 3D semantic world modeling, multimodal AI reasoning, and a deterministic safety gate.

See [docs/3D_ROBOT_CONCEPT.md](docs/3D_ROBOT_CONCEPT.md) for the design concept.

## Real-time upgrade

The system supports live processing from a webcam or RTSP stream. The pipeline estimates depth per frame, tracks detected objects, builds a hazard map, and overlays the result in a live OpenCV window.

## Embodied AI architecture

RGB / thermal / NIR / depth / LiDAR / IMU -> YOLO + SAM3 + tracking -> 3D semantic world model -> Qwen3-VL + Gemma 4 E4B reasoning -> V-JEPA2 future prediction -> GR00T N1.7 / FLUX 3 Action candidate actions -> deterministic safety gate -> ROS2/Nav2 + MoveIt2/RRT* -> robot -> action verification.

### Models and roles

- YOLO: fast detection and tracking.
- SAM 3: open-vocabulary segmentation, occlusion boundaries and video tracking.
- Qwen3-VL: primary multimodal scene and rescue reasoning.
- Gemma 4 31B IT: high-capacity multimodal flood-scene reasoning, victim verification, occlusion analysis, route/debris reasoning and rescue-plan cross-checking.
- Gemma 4 E4B-it: lightweight fallback multimodal reasoning.
- LeRobot: datasets, teleoperation, training and deployment.
- SmolVLA, pi0/pi0.5, X-VLA, VLA-JEPA: action/VLA candidates.
- NVIDIA GR00T N1.7 3B: embodied action-policy candidate for adaptation to the flood-robot embodiment.
- FLUX 3 Action Base: world-action adaptation base; not a complete robot policy and requires an embodiment-specific action head.
- V-JEPA2/VLA-JEPA: temporal world-model and future-state prediction.
- LTX-2.5-Diffusers: offline synthetic video/audio scenario generation and visual diversity.
- MiniMax H3 Turbo LoRA: offline synthetic audio-visual scenario generation and rare-event prototyping.
- RGB-D + LiDAR + Open3D: 3D semantic mapping.
- Thermal + NIR + depth/LiDAR: darkness and low-visibility perception.
- Isaac Sim + Isaac Lab: realistic 3D robot simulation, synthetic data and sim-to-real testing.

## Gemma 4 31B IT multimodal reasoning

The repository integrates [google/gemma-4-31B-it](https://huggingface.co/google/gemma-4-31B-it) as a multimodal reasoning model for flood-rescue scene interpretation. It accepts image + text inputs through Transformers and can also be served with vLLM. The model weights are downloaded at runtime and are not committed to this repository.

Recommended flow:

RGB / thermal / NIR / depth / LiDAR -> perception + tracking -> 3D semantic scene -> **Gemma 4 31B IT** -> structured rescue decision -> VLA/action candidates -> deterministic safety gate.

Gemma 4 31B IT is advisory only: it cannot directly command motors, navigation actuators, or rescue mechanisms. Unknown or occluded people/objects must be re-observed, and every candidate action remains subject to collision checking, exclusion zones, sensor-health checks and emergency-stop logic.

## Safety

Foundation, generative and action models never bypass deterministic safety. Reasoning models propose priorities; action models propose candidate actions. Collision checking, human-exclusion zones, sensor-health checks, force/torque limits and emergency-stop logic remain authoritative.

See docs/EMBODIED_AI_STACK.md, docs/ADVANCED_MODEL_INTEGRATION.md, config/ai_stack.yaml, config/advanced_models.yaml and config/safety_forecasting.yaml.

## Installation

```bash
git clone https://github.com/Pui89/flood-rescue-ai-robot.git
cd flood-rescue-ai-robot
python -m venv .venv
source .venv/bin/activate
pip install -U pip
pip install -e .
```

## Usage

Run the live real-time demo from a webcam:

```bash
python scripts/run_demo.py --source 0 --display
```

Run from an RTSP stream:

```bash
python scripts/run_demo.py --source "rtsp://username:password@ip:554/stream"
```

Run the smoke test:

```bash
pytest tests/test_tracker.py -q
```

## 3D / 4D Realistic Flood Rescue Robot Concept

![Realistic 3D/4D Flood Rescue Robot](docs/flood_rescue_robot_3d_4d_concept.svg)

The concept shows the flood-response robot operating in a dynamic disaster scene with RGB-D/LiDAR perception, thermal sensing, victim tracking, an articulated rescue arm, and a time-aware 4D trajectory.

- [3D/4D concept image](docs/flood_rescue_robot_3d_4d_concept.svg)
- [3D/4D video preview](docs/flood_rescue_robot_3d_4d_preview.mp4)

## Pipeline Overview

**Sense → Perceive → Localize → Reason → Plan → Safety Gate → Navigate → Rescue → Verify → Report**

![Pipeline overview](docs/flood_rescue_robot_3d_4d_concept.svg)

See the full architecture and mission flow in [docs/PIPELINE_OVERVIEW.md](docs/PIPELINE_OVERVIEW.md).


## Research, competition and commercialization

This project is being developed on three parallel tracks:

- **Real-world rescue robotics:** rugged mobility, multimodal sensing, GNSS-denied navigation, rescue payloads, degraded-mode operation and deterministic safety.
- **World-class competition:** a complete end-to-end mission demonstration with quantified victim localization, dynamic hazard avoidance, recovery, energy and operator-intervention metrics.
- **PhD research:** a proposed **Trustworthy 4D Rescue World Model (T4D-RWM)** connecting multimodal perception, temporal prediction, uncertainty/OOD, active perception and risk-aware action. See [PhD research program](docs/PHd_RESEARCH_PROGRAM.md).

See also:
- [Competition & product plan](docs/COMPETITION_AND_PRODUCT_PLAN.md)
- [Research dataset specification](docs/RESEARCH_DATASET_SPEC.md)
- [Cybersecurity policy](SECURITY.md)
- [3D/4D world model implementation](flood_robot/world_model.py)

The project should not be judged by the number of AI models integrated. The key engineering target is **measurable end-to-end rescue performance under uncertainty and failure**.

## News

- Project updates, perception and embodied-AI integrations, simulation assets, safety changes, and evaluation milestones are tracked through Git history and project documentation.
- New capabilities are labeled by implementation status and are not presented as validated field performance unless measured results are available.

## Online API

**Status: Prototype / planned.**

A future service layer can expose perception, victim/obstacle localization, hazard mapping, route planning, rescue-plan proposals, telemetry, and safety-state inspection without allowing foundation models to directly control actuators.

Example request:

```json
{
  "request_id": "example-001",
  "modalities": ["rgb", "depth", "thermal", "lidar"],
  "mode": "rescue_assessment",
  "mission_id": "flood-01"
}
```

Example response:

```json
{
  "request_id": "example-001",
  "decision": "HUMAN_REVIEW",
  "victim_candidates": [],
  "hazards": [],
  "confidence": 0.0,
  "uncertainty": 0.0,
  "safety_gate": "NOT_EXECUTED",
  "evidence_provenance": {}
}
```

These are interface examples only, not measured performance. A production API should authenticate requests, validate schemas, preserve evidence provenance, and keep reasoning separate from deterministic control and emergency-stop paths.

## Online App

**Status: Prototype / planned.**

The planned web application can provide:

- live RGB/RGB-D/thermal/LiDAR sensor health
- synchronized flood-scene and robot views
- victim and hazard candidate visualization
- 3D semantic map and 4D trajectory view
- route/rescue-plan inspection
- uncertainty, occlusion, and sensor-health indicators
- robot telemetry and mission state
- safety-gate and emergency-stop state
- human review/approval workflow
- evidence provenance and audit history

The app is intended for monitoring and human oversight; it must not provide unrestricted AI-to-motor control.

## System Overview

```text
RGB / RGB-D / Thermal / NIR / LiDAR / IMU
                  |
          Sensor Synchronization
                  |
        Quality + Health Gate
                  |
   Detection + Segmentation + Tracking
                  |
       3D Semantic World Model
                  |
     Victim / Hazard Assessment
                  |
      Multimodal Scene Reasoning
                  |
       Temporal / 4D Prediction
                  |
       Route + Rescue Planning
                  |
        Uncertainty / OOD Checks
                  |
       HUMAN REVIEW / POLICY
                  |
       Deterministic Safety Gate
                  |
        ROS 2 / Nav2 / MoveIt 2
                  |
             Robot + Tools
                  |
       Action Verification + Report
```

The architecture intentionally separates multimodal reasoning from authoritative robot control.

## Model Variants and Input Specifications

| Variant | Input | Primary role | Status |
|---|---|---|---|
| RGB perception | RGB image/video | Person, vehicle, debris, structure detection | Prototype |
| RGB-D | RGB + aligned depth | 3D localization and geometry | Prototype |
| Thermal | Thermal image/video | Low-light and heat-signature evidence | Prototype |
| NIR | NIR image/video | Low-visibility complementary evidence | Planned |
| LiDAR | Point cloud | Mapping, obstacle geometry, free space | Prototype |
| Multimodal | RGB-D + thermal + LiDAR + optional NIR | Evidence fusion | Prototype |
| Temporal / 4D | Sequential multimodal observations | Tracking, motion and future-state estimation | Prototype |
| Open-set / anomaly | Multimodal features | Unknown/degraded-scene handling | Planned |
| Qwen3-VL | Image + text/evidence metadata | High-level multimodal rescue reasoning | Prototype |
| Gemma 4 31B IT | Image + text/evidence metadata | High-capacity reasoning and cross-checking | Prototype |
| VLA candidates | Vision/state/action context | Future embodied-action research | Planned |

Actual camera resolution, depth range, LiDAR density/FOV, thermal/NIR bands, FPS, calibration, synchronization and preprocessing depend on deployed hardware. Dataset and sensor provenance should be recorded for reproducibility.

## YOLO26 Models & Training

Integrated Ultralytics YOLO26 model matrix, flood-rescue dataset schema, training, validation, inference, export and robot integration workflow: [docs/YOLO26_MODELS_AND_TRAINING.md](docs/YOLO26_MODELS_AND_TRAINING.md).

## Model Architecture

The system is organized into six functional layers:

1. **Perception** — detection, segmentation, tracking, depth estimation and sensor-quality checks.
2. **Spatial intelligence** — RGB-D/LiDAR fusion, 3D semantic mapping, terrain and obstacle geometry.
3. **Temporal intelligence** — target-state estimation, tracking continuity and 4D future-state prediction.
4. **Multimodal reasoning** — Qwen3-VL/Gemma reasoning over grounded observations and metadata.
5. **Planning** — navigation, reachability, collision-aware rescue planning and task sequencing.
6. **Safety/control** — deterministic validation followed by ROS2/Nav2/MoveIt2 execution and verification.

```text
Sensors
  -> Perception
  -> 3D/4D World Model
  -> Multimodal Reasoning
  -> Plan Proposal
  -> Uncertainty/OOD Checks
  -> Deterministic Safety Gate
  -> ROS2/Nav2/MoveIt2
  -> Robot
  -> Verify + Log
```

Foundation and generative models are advisory components. They are never the final authority for actuation.

## Recommended Workflow

1. Calibrate RGB, depth, thermal/NIR and LiDAR sensors.
2. Verify timestamps, extrinsics, synchronization and sensor health.
3. Acquire flood-scene observations and reject degraded inputs when necessary.
4. Detect and track victims, obstacles, vehicles, structures and debris.
5. Fuse depth/LiDAR into a 3D semantic world model.
6. Track relevant targets and hazards over time.
7. Generate a route/rescue-plan proposal using deterministic planners plus approved AI reasoning.
8. Check uncertainty, missing modalities, occlusion, reachability, collision risk and exclusion zones.
9. Escalate ambiguous or high-risk situations to human review.
10. Run the deterministic safety gate and emergency-stop checks.
11. Execute only through validated ROS2/Nav2/MoveIt2 interfaces.
12. Verify the outcome and record telemetry, evidence provenance, failures and recovery actions.

## Local Deployment

**Status: Local development / prototype deployment.** Physical deployment must remain behind deterministic safety controls and authorized robot interfaces.

### Requirements

- Python 3.x
- Git
- PyTorch and project dependencies
- ROS 2/Nav2/MoveIt 2 for optional physical integration
- RGB/RGB-D/thermal/NIR/LiDAR/IMU hardware as configured
- Optional NVIDIA GPU
- Optional Isaac Sim, Isaac Lab or Gazebo

### Clone and Install

```bash
git clone https://github.com/Pui89/flood-rescue-ai-robot.git
cd flood-rescue-ai-robot
python -m venv .venv
source .venv/bin/activate
# Windows PowerShell:
# .venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -e .
```

### Validate the Environment

```bash
python --version
python -m pip check
pytest tests/test_tracker.py -q
```

Run the full test suite when available:

```bash
pytest -q
```

### Run the Local Demo

Webcam:

```bash
python scripts/run_demo.py --source 0 --display
```

RTSP:

```bash
python scripts/run_demo.py --source "rtsp://username:password@ip:554/stream"
```

Start with recorded or simulated data when validating new sensors, models or deployment configurations.

### Recommended Deployment Sequence

```text
Recorded / Simulated Data
        |
Environment + Dependency Validation
        |
Sensor Calibration + Time Synchronization
        |
Perception + Tracking
        |
3D Semantic World Model
        |
Multimodal Evidence + Reasoning
        |
Uncertainty / OOD Assessment
        |
Human Review / Mission Policy
        |
Deterministic Safety Gate
        |
ROS 2 / Nav2 / MoveIt 2
        |
Authorized Robot Interface
        |
Action Verification + Audit Log
```

### Sensor Deployment Checklist

Record sensor model/configuration, resolution, frame rate, FOV/range, intrinsic/extrinsic calibration, timestamp synchronization, preprocessing/model versions, sensor-health state, missing modalities, mission identifier, evidence provenance, reviewer decision and outcome.

Missing, degraded or contradictory modalities should preserve uncertainty or `UNKNOWN` rather than forcing a confident rescue classification.

### ROS 2 / Robotics Integration Boundary

```text
Sensors -> Perception -> 3D/4D World Model -> Reasoning
                                                   |
                                                   v
                                             Human Review
                                                   |
LiDAR + Depth + IMU -> SLAM -> Planner -> Safety Gate -> ROS 2
```

Foundation, generative and action models must not directly command motors, propulsion, manipulators or other actuators. Deterministic collision checks, exclusion zones, sensor-health checks, force/torque limits and emergency-stop behavior remain authoritative.

### Troubleshooting

- **Install fails:** verify Python and project packaging/dependencies.
- **Tests fail:** fix the local environment before physical deployment.
- **Camera/RTSP fails:** check permissions, stream URL, network access and OpenCV backend.
- **Sensor data is missing/unsynchronized:** stop and correct calibration/time synchronization.
- **ROS 2 unavailable:** use recorded data or simulation.
- **Low confidence or modality disagreement:** retain uncertainty and escalate to human review.

### Development Principle

Validate recorded/simulated data first, then perception, uncertainty and safety behavior, and only then connect hardware incrementally. No unvalidated foundation-model output may bypass the deterministic safety layer or directly actuate the robot.
## Full 2K-Workflow

**2K is a target high-resolution workflow, not a guaranteed camera specification.**

```text
2K RGB acquisition
      -> quality + synchronization checks
      -> resize/crop/preprocess
      -> person/victim/hazard detection
      -> segmentation + tracking
      -> thermal/NIR/depth/LiDAR alignment
      -> 3D semantic fusion
      -> 4D target/hazard-state tracking
      -> multimodal reasoning
      -> uncertainty / OOD assessment
      -> route + rescue-plan proposal
      -> deterministic safety gate
      -> human review / authorized execution
      -> action verification
      -> provenance + telemetry + audit log
```

Actual throughput and latency depend on camera, GPU/CPU, memory, preprocessing, model size, sensor synchronization and deployment configuration.

## Prompting Guidance

Foundation models should act as evidence-grounded reasoning assistants, not unrestricted robot controllers.

Recommended prompt structure:

```text
ROLE:
Flood-rescue evidence and planning assistant.

INPUT:
Only supplied RGB/RGB-D/thermal/NIR/LiDAR observations,
robot state, target metadata and explicit safety constraints.

TASK:
1. Summarize observable evidence.
2. Identify victim/hazard candidates and missing or degraded modalities.
3. Report contradictions, occlusion and uncertainty.
4. Propose a high-level rescue/navigation plan.
5. Preserve UNKNOWN when evidence is insufficient.
6. Recommend HUMAN_REVIEW when risk or uncertainty is high.

CONSTRAINTS:
Do not invent observations.
Do not inflate confidence.
Do not bypass deterministic safety rules.
Do not issue unrestricted motor commands.
Do not execute outside the validated control layer.
```

Gemma, Qwen and other foundation models remain subordinate to deterministic safety logic and authorized robot-control policy.

## License

MIT. See the repository license for the applicable terms. Third-party models, datasets, simulators, SDKs and checkpoints may have separate licenses and usage restrictions.

## Contact Us

GitHub: [Pui89/flood-rescue-ai-robot](https://github.com/Pui89/flood-rescue-ai-robot)

Use GitHub Issues and Discussions for technical questions, collaboration, bug reports, feature requests, and research/engineering feedback.
