# Safety and Operating Boundaries

**Status:** research prototype. This document is not a certification, complete hazard analysis, or authorization to operate.

## Intended use

PUI89 Flood Recon is intended to support supervised reconnaissance, hazard observation, mapping and evidence collection in a defined and controlled operating domain. Outputs are decision support for trained human operators.

## Out of scope unless separately engineered and approved

- Entering floodwater, swift water, submerged spaces or unstable structures.
- Physical rescue, victim extraction, medical decisions or life-critical intervention.
- Unsupervised operation near the public, responders, vehicles, power lines or other hazards.
- Treating AI classifications, map colors or route suggestions as guarantees of safety.
- Using this prototype as the sole basis for evacuation, rescue or infrastructure decisions.

## Known failure modes

- Glare, darkness, rain, fog, spray, turbidity, reflections, occlusion and low contrast.
- Sensor contamination, miscalibration, vibration, water ingress, condensation or thermal drift.
- Stale timestamps, clock drift, dropped/corrupt frames, sensor disconnection or conflicting sensors.
- Out-of-distribution scenes, false positives, missed hazards, incorrect depth and map drift.
- Battery depletion, overheating, compute overload, storage exhaustion, network loss and process crashes.
- Unreliable GNSS, communications interruption and changes in terrain or water level after mapping.

## Required design controls

1. **Human supervision:** an identified operator must understand system state, take control and stop the robot.
2. **Independent safety supervisor:** AI models must not override emergency-stop logic or bypass motion interlocks.
3. **Fail-safe data handling:** stale, missing, invalid or conflicting sensor data must be surfaced. Degraded state should reduce capability or stop motion according to risk assessment.
4. **Unknown means unknown:** unobserved, occluded or low-confidence regions must not be marked safe or traversable by default.
5. **Emergency stop:** physical emergency stop and operator override must be validated on integrated hardware before motion tests.
6. **Auditability:** log health state, sensor faults, map/model versions, operator interventions, safety decisions and software/configuration identity.
7. **Cybersecurity:** authenticate update sources, minimize exposed services, protect secrets, and document access control and patching.
8. **Privacy:** minimize collection of faces, license plates, precise private locations and bystander data; restrict access and retention.

## Test progression

- Begin with simulation and recorded-data replay.
- Move to bench tests with actuators disabled.
- Perform hardware-in-the-loop and fault injection in a secured test area.
- Conduct supervised trials only after risk review, site authorization, trained personnel, emergency procedures and rollback plan.
- Do not use real flood conditions as an initial validation environment.

## Stop conditions

Stop the test and secure the robot if an emergency stop fails, the safety supervisor becomes unavailable, critical sensors are invalid, localization is lost beyond the approved limit, thermal/power limits are exceeded, the operator cannot intervene, or the robot behaves unexpectedly.

Thresholds must be selected for the actual robot and operating domain. Generic values are not proof of safety.

## Release gate

No public or commercial deployment should proceed until operator procedures, system-specific risk assessment, emergency-stop tests, fault-injection evidence, cybersecurity review, applicable legal/regulatory review and insurance requirements have been addressed. Obtain independent professional review for any life-safety application.

**Important:** This software may fail. A hazard map is not a guarantee that an area is safe, and a successful demo is not evidence of field readiness.