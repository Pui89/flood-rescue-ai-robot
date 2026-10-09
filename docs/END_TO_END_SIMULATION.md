# End-to-End Flood Rescue Software Baseline

This repository now has an executable, deterministic reference flow:

**normalized sensor/perception hypotheses → quality gate → timestamp alignment → victim/hazard hypothesis aggregation → collision-check gate → human approval gate → proposal and audit report.**

## Run

```bash
python -m pip install -e ".[dev]"
python demo_end_to_end.py
python -m pytest tests/test_end_to_end.py -q
```

The demo uses synthetic, hand-authored observations. It does not run a detector, a physics engine, or a real robot. Victim/hazard candidates are upstream hypotheses, not verified facts.

## Safety invariants

- Reject invalid or low-quality sensor observations.
- Reject temporal fusion when timestamps exceed the configured skew.
- Block a plan if independent collision validation has not passed.
- Require human mission approval.
- Never issue actuator commands; an approved output is still only a proposal.
- Preserve evidence identifiers and an audit-oriented record.

## Current limitations and next gates

This module does not implement physical sensor drivers, real perception inference, calibrated localization, a validated collision checker, hydrodynamics, robot dynamics, ROS 2 control, or hardware-in-the-loop tests. The `collision_check_passed` input is an externally supplied assertion, not a collision checker. Before any field use, implement and independently test a collision checker against a validated robot model, connect a physics-backed simulator (e.g. Gazebo Sim or Isaac Sim), evaluate recorded flood scenarios, and document quantitative metrics and failures. Never use synthetic demo outputs as benchmark claims.
