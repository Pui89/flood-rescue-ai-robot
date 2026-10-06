# Reasoning Layer and Next Steps

The flood-rescue robot now has a high-level multimodal reasoning adapter for Qwen3-VL or another VLM/reasoning model.

## Layered architecture

RGB/thermal/NIR/depth/LiDAR -> YOLO/SAM3/tracking -> 3D world state -> reasoning model -> prediction/planner -> deterministic safety gate -> ROS2/robot controller.

The reasoning model proposes priorities and investigation steps. It cannot directly command motors.

## What to add next

1. **World model** — persistent 3D semantic map with people, obstacles, water, routes and uncertainty.
2. **Active perception** — investigate unseen/occluded regions instead of assuming absence.
3. **Predictive safety** — forecast collision, submersion, debris motion and route blockage several seconds ahead.
4. **Sensor fusion** — calibrated RGB/thermal/NIR/depth/LiDAR/IMU fusion with disagreement scoring.
5. **Rescue skill library** — approach, inspect, illuminate, communicate, deliver flotation aid, retreat and verify.
6. **Human-in-the-loop** — explicit operator approval for uncertain or high-consequence rescue actions.
7. **Fault detection** — camera obstruction, LiDAR/depth failure, wheel slip, actuator overload, communication loss and battery degradation.
8. **Persistent mission memory** — track people, hazards, visited zones, failed approaches and recovery history.
9. **Simulation/digital twin** — Isaac Sim/Isaac Lab scenarios for night, rain, fog, reflections, current, debris and occlusion.
10. **LeRobot datasets + evaluation** — record successful/failure/recovery episodes and measure detection recall, warning lead time, collision rate, rescue success and false alarms.

## Safety invariant

The reasoning/VLA stack may propose an action, but deterministic collision, human-exclusion, sensor-health and emergency-stop rules remain authoritative.
