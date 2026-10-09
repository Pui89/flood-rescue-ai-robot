# PUI89 Flood Rescue Commercial Readiness Checklist

Use this as a release gate, not as a claim that the product is already production-ready. Record evidence links and the person responsible for each item.

## 1. Legal and software supply chain

- [ ] Generate an SBOM for the exact release.
- [ ] Pin dependencies and model checkpoints by version/hash.
- [ ] Verify code license, model-weight license, dataset license, SDK terms, and redistribution rights separately.
- [ ] Review Ultralytics YOLO licensing for proprietary/commercial distribution before shipping.
- [ ] Review NVIDIA repository/package terms for each bundled component.
- [ ] Preserve attribution, notices, and required license files.
- [ ] Scan dependencies and container images for known vulnerabilities.
- [ ] Ensure no credentials, customer footage, location data, or secrets are committed.

## 2. Robot and sensor engineering

- [ ] Document target robot, payload, dimensions, mass, center of gravity, buoyancy/stability limits, IP rating, temperature range, ingress protection, and maintenance needs.
- [ ] Validate sensor mounts, calibration, time synchronization, vibration, water droplets, glare, fog, thermal reflections, and partial sensor obstruction.
- [ ] Document localization limits in GNSS-denied environments.
- [ ] Measure battery endurance under representative payload, current, temperature, and communications conditions.
- [ ] Define safe behavior for loss of propulsion, localization, compute, network, and power.

## 3. Software and safety

- [ ] All robot commands pass through an allowlisted, deterministic control interface.
- [ ] Emergency stop is independent of model inference and remote connectivity.
- [ ] Stale or contradictory sensor data is rejected or explicitly marked degraded.
- [ ] Unknown space is treated conservatively.
- [ ] Speed, stability, collision, geofence, payload, and actuator limits are enforced.
- [ ] Fault injection covers camera/LiDAR/IMU dropout, clock drift, corrupt frames, GPU failure, node crash, network loss, and low battery.
- [ ] Recovery and safe-stop behavior is measured and documented.
- [ ] Logs redact secrets and access to telemetry is authenticated and authorized.

## 4. Verification and evidence

- [ ] Dataset splits prevent leakage across locations, missions, and time periods.
- [ ] Benchmarks include normal, rare, degraded, and adversarial environmental conditions.
- [ ] Report precision/recall, false alarms, localization error, latency, uptime, recovery, interventions, and safety events.
- [ ] Each benchmark identifies hardware, software commit, checkpoint hash, configuration, trial count, and limitations.
- [ ] Compare the optimized inference engine with the reference implementation.
- [ ] Publish failures and known limitations alongside successful demonstrations.
- [ ] Simulated results, lab results, and field results are labeled separately.

## 5. Commercial operations

- [ ] Define Research, Professional, and Enterprise packages with explicit supported configurations.
- [ ] Provide install, upgrade, rollback, backup, and recovery instructions.
- [ ] Provide a mission evidence export and diagnostic bundle.
- [ ] Define user roles, access controls, audit retention, privacy, and incident response.
- [ ] Define offline operation and data synchronization behavior.
- [ ] Define service-level promises only where supported by measured evidence.
- [ ] Document support scope, maintenance schedule, spare parts, training, and warranty assumptions.
- [ ] Complete supervised field trials with trained operators before operational rescue use.

## Release decision

**Do not mark a checklist item complete without an evidence link or test record.** Passing software tests alone does not validate buoyancy, waterproofing, human rescue interaction, or real-world emergency response. Physical rescue capability requires qualified engineering and controlled testing.
