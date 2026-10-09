# Pui89 AI Robotics — Open-Source-First Technology Stack

This is a proposed stack, not a claim that every component is already integrated. Pin versions and test compatibility before deployment. Check each component's software license, model license, dataset terms, hardware-driver terms, and redistribution requirements independently.

## Core robotics
- **ROS 2** — middleware and robot interfaces: https://github.com/ros2/ros2
- **Nav2** — mobile robot navigation: https://github.com/ros-navigation/navigation2
- **MoveIt 2** — manipulation and motion planning: https://github.com/moveit/moveit2
- **Gazebo** — simulation: https://gazebosim.org/
- **ros2_control** — hardware interfaces and controllers: https://github.com/ros-controls/ros2_control
- **robot_localization** — state estimation: https://github.com/cra-ros-pkg/robot_localization
- **RViz** — visualization within ROS 2.

Use one supported ROS 2 distribution consistently across CI, development, and deployment. Confirm each robot's sensors, drivers, compute platform, and control hardware are supported.

## AI and perception
- **PyTorch** — model development: https://github.com/pytorch/pytorch
- **OpenCV** — image processing: https://github.com/opencv/opencv
- **Open3D** — 3D data processing: https://github.com/isl-org/Open3D
- **Hugging Face Transformers** — model integration: https://github.com/huggingface/transformers
- **ONNX Runtime** — cross-platform model inference: https://github.com/microsoft/onnxruntime
- **OpenVINO** — optional optimized inference for supported Intel hardware: https://github.com/openvinotoolkit/openvino
- **Ultralytics YOLO** — evaluate carefully: https://github.com/ultralytics/ultralytics. Its AGPL-3.0 and enterprise licensing terms may affect commercial distribution; do not assume it is permissively licensed.

Model selection is task- and hardware-dependent. Evaluate accuracy, latency, memory, power, quantization, robustness, model license, training-data terms, and commercial-use conditions. Do not add models just to make the architecture look larger.

## Data, experiment tracking, and model lifecycle
- **DVC** — dataset/model versioning: https://github.com/iterative/dvc
- **MLflow** — experiment tracking and model lifecycle: https://github.com/mlflow/mlflow
- **FiftyOne** — dataset inspection and error analysis: https://github.com/voxel51/fiftyone
- **CVAT** — image/video annotation: https://github.com/cvat-ai/cvat
- **Label Studio** — annotation workflows: https://github.com/HumanSignal/label-studio
- **Evidently** — data/model monitoring: https://github.com/evidentlyai/evidently

Never place private customer data, credentials, or restricted datasets in public repositories. Store dataset manifests and documentation publicly where appropriate, but gate actual data access according to consent and license.

## API and developer experience
- **FastAPI** — Python service APIs: https://github.com/fastapi/fastapi
- **Pydantic** — typed validation and schemas: https://github.com/pydantic/pydantic
- **OpenAPI** — documented API contract: https://www.openapis.org/
- **Docker Engine / Compose** — reproducible development and service packaging: https://github.com/docker/compose
- **uv** — Python project and dependency management: https://github.com/astral-sh/uv

A REST API must never be a direct, unrestricted actuator interface. Expose task requests through validation, authentication, explicit permissions, rate limits, and a safety-controlled ROS 2 boundary.

## Testing, security, and operations
- **pytest** — unit/integration tests: https://github.com/pytest-dev/pytest
- **pre-commit** — automated formatting/lint hooks: https://github.com/pre-commit/pre-commit
- **Ruff** — Python linting and formatting: https://github.com/astral-sh/ruff
- **mypy** — static type checking: https://github.com/python/mypy
- **Bandit** — Python security linting: https://github.com/PyCQA/bandit
- **pip-audit** — dependency vulnerability checks: https://github.com/pypa/pip-audit
- **Syft** — software bill of materials: https://github.com/anchore/syft
- **Grype** — vulnerability scanning: https://github.com/anchore/grype
- **OpenTelemetry** — traces, metrics, and logs: https://github.com/open-telemetry/opentelemetry-python
- **Prometheus** — metrics: https://github.com/prometheus/prometheus
- **Grafana** — dashboards: https://github.com/grafana/grafana

Use GitHub Actions or another CI system to run tests, linting, dependency checks, license inventory, and reproducible benchmark jobs. Pin dependencies and produce an SBOM for releases.

## Proposed repository layout

```text
pui89-embodied-ai/
  docs/
    architecture/
    safety/
    evaluation/
    data-governance/
    commercial/
  configs/
  schemas/
  packages/
    pui89_interfaces/
    pui89_sensor_health/
    pui89_perception/
    pui89_world_model/
    pui89_safety_gate/
    pui89_task_api/
    pui89_evaluation/
  integrations/
    ros2/
    simulation/
    hardware/
  tests/
    unit/
    integration/
    simulation/
    hardware_in_loop/
  benchmarks/
  deployment/
  scripts/
  LICENSE
  THIRD_PARTY_NOTICES.md
  SECURITY.md
  CONTRIBUTING.md
```

## Adoption order

1. ROS 2 + simulation + pytest.
2. Sensor schemas, health checks, logs, and safety-gate interfaces.
3. Existing perception modules and baseline metrics.
4. DVC/MLflow and dataset governance.
5. API, dashboard, and telemetry.
6. Hardware-in-the-loop, SBOM, vulnerability checks, and release automation.
7. Additional VLM/VLA/world-model components only when a benchmark demonstrates value.
