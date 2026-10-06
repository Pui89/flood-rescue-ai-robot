# Embodied AI Stack for Flood Rescue

This upgrade adds a perception, prediction, planning and safety architecture for difficult flood scenes.

## Model stack

| Layer | Open model/tool | Role |
|---|---|---|
| Fast detection | YOLO family | Real-time people, debris, boat, vehicle and obstacle detection |
| Segmentation | SAM 3 | Open-vocabulary masks, occlusion boundaries and video tracking |
| Large vision | Qwen3-VL | Image/video reasoning, spatial understanding and occlusion analysis |
| Robot learning | LeRobot | Dataset, teleoperation, training and deployment |
| Large action / VLA | SmolVLA, pi0/pi0.5, X-VLA, VLA-JEPA | Candidate robot actions from vision/state/instructions |
| World model | V-JEPA2 / VLA-JEPA | Future-state and video prediction |
| 3D | RGB-D + LiDAR + Open3D | Metric geometry and traversability |
| Realistic 3D simulation | NVIDIA Isaac Sim + Isaac Lab | Physics, synthetic video and sim-to-real |
| Navigation | ROS 2 + Nav2 | Risk-aware navigation |
| Manipulation | MoveIt 2 + OMPL/RRT* | Collision-aware motion planning |
| Night perception | Thermal + NIR + RGB + depth/LiDAR | Low-light and darkness perception |

## Architecture

RGB / thermal / NIR / depth / LiDAR / IMU -> YOLO + SAM3 + tracking -> 3D semantic world model -> Qwen3-VL + future-state predictor -> task planner -> LeRobot VLA -> deterministic safety gate -> ROS2/Nav2 + MoveIt2/RRT* -> robot -> action verification.

Large vision and action models are policy/reasoning components. They must never bypass deterministic safety checks or directly drive motors.

## Visibility and unknown-state model

- VISIBLE: confidently observed and localized.
- OCCLUDED: partially blocked by debris, spray, vegetation or another person.
- UNSEEN: outside sensor coverage or disappeared from the observation stream.
- UNKNOWN: sensor/model disagreement is too high for a safe classification.
- PREDICTED_HAZARD: future collision, submersion, collapse, debris impact or blockage is forecast.
- WARNING: slow, stop or re-plan.
- EMERGENCY: safe stop and retract.

Never infer that a person is absent just because detection disappeared.

## Early warning targets

Person drifting toward deeper water; partial submersion/drowning risk; moving debris; floating-object collision; unstable ground; water/current changes; human or animal entering the safety zone; camera obstruction; severe glare; depth/LiDAR failure; wheel slip; excessive tilt; actuator overload; low battery; communication loss; model uncertainty.

## Darkness

Use thermal for heat signatures, NIR/low-light cameras for texture, and depth/LiDAR for geometry. If confidence drops, mark LOW_VISIBILITY and reduce speed or stop. RGB enhancement alone must not be treated as reliable geometry.

## Realistic 3D video

Isaac Sim/Isaac Lab should generate physically based floodwater, rain, fog, glare, night lighting, floating debris, partially submerged people, moving vehicles, blocked routes, robot motion, sensor noise and occlusion. Generate ground truth for masks, depth, 3D poses, trajectories and collision events. Synthetic footage should be labeled as simulation when presented publicly.

## Training loop

Real demonstrations + public datasets -> LeRobotDataset -> Isaac synthetic scenes -> YOLO/SAM3/Qwen3-VL/VLA training -> uncertainty and anomaly tests -> simulation stress tests -> controlled real-world test -> supervised deployment.