# Safety Architecture

The flood-rescue robot is a safety-critical robotics prototype. Foundation models, generative models and learned action policies are advisory components and must not bypass the deterministic control boundary.

## Control boundary

AI observation or proposal -> schema and provenance validation -> uncertainty and sensor-health checks -> collision, reachability and exclusion zones -> energy, communication and actuator limits -> human approval when required -> deterministic safety gate -> ROS 2 / hardware abstraction -> actuator.

## Required hold conditions

- missing or stale critical sensor data;
- timestamp or frame synchronization failure;
- contradictory modalities above configured tolerance;
- unknown or out-of-distribution scene;
- insufficient localization confidence;
- predicted collision or unsafe proximity;
- invalid actuator command or unavailable hardware;
- communication loss when local autonomy is not explicitly authorized;
- emergency-stop state.

## Evidence requirements

Each mission decision should retain, where available:

- mission and observation IDs;
- timestamps and sensor IDs;
- calibration/configuration version;
- model and Git versions;
- candidate detections and tracking state;
- uncertainty and sensor-health state;
- reviewer/policy decision;
- safety-gate result;
- command/result verification;
- failure and recovery events.

## Deployment rule

Simulation and recorded-data validation precede hardware tests. Hardware-in-the-loop precedes supervised field trials. Physical deployment requires an independently testable emergency-stop path and authorized operator control.
