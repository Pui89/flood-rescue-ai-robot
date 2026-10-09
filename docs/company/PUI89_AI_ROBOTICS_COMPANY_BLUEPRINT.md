# Pui89 AI Robotics — Company Blueprint

**Status:** Founder planning / research-stage. This document describes a proposed company and roadmap; it is not a claim of incorporation, customer contracts, field validation, or commercial certification.

## Company thesis

Pui89 AI Robotics develops open-source-first embodied-AI software for robots that must perceive, reason about, and safely operate in complex physical environments.

**Mission:** Build intelligent robots that perceive, understand, and act safely in the real world.

**Initial verticals**
1. **Pui89 RescueBot** — flood reconnaissance, hazard mapping, and operator-assistance research.
2. **Pui89 AgriBot** — agricultural perception and coconut-harvesting automation research.
3. **Pui89 SecureBot** — human-reviewed security screening and anomaly detection research; no unsupported chemical-identification claims.

## Business strategy

Start with software, integration, evaluation, and paid pilots rather than attempting to manufacture three complete robots immediately.

Potential offers, only after capability and demand are validated:
- Robotics AI integration and engineering services.
- Open SDK plus paid deployment, support, maintenance, and fleet-management services.
- Industry-specific perception/evaluation packages.
- Hardware-integrated systems through qualified partners.
- Eventually, complete robot products if pilots establish a repeatable need.

No prices, customer demand, or revenue are assumed in this plan. Validate willingness to pay through customer interviews and pilot proposals.

## Shared platform architecture

Sensors and robot state → timestamping/calibration/health checks → perception and tracking → spatial/world representation → uncertainty-aware AI assistance → task planner → deterministic safety checks → ROS 2 navigation/manipulation → action verification → telemetry, audit trail, and evaluation.

Foundation models must not directly publish motor commands. A separate, testable safety layer must validate motion requests, enforce limits and stop conditions, and fail safely when inputs or communications are unhealthy. Safety claims require independent engineering and physical testing.

## Differentiation

Do not claim a new foundation model merely because third-party models are integrated. Build evidence-backed advantages through:
- Well-documented, permissioned multimodal robotics datasets.
- Repeatable domain benchmarks and failure-case analysis.
- Sensor calibration and time synchronization.
- Uncertainty estimation, out-of-distribution detection, and abstention.
- Robust integration across hardware and ROS 2 interfaces.
- Measured deployment performance and safe operator workflows.

## First market hypothesis

Test two customer problems in parallel through interviews, but build one technical demonstration:
- **Flagship R&D:** RescueBot in simulation and controlled, non-hazardous environments.
- **Potential first commercial vertical:** AgriBot perception/monitoring, which may allow a more contained proof of value than autonomous flood rescue.

Choose the first paid pilot based on access to users, data, hardware, measurable return on investment, and safety burden—not enthusiasm alone.

## 90-day plan

### Days 1–15: Foundation
- Confirm scope, product claims, repository ownership, and third-party licenses.
- Establish a single architecture and common message/data contracts.
- Define baseline test cases and a reproducible development environment.
- Interview at least 10 potential users across agriculture, disaster response, and robotics integration.

### Days 16–30: Reproducible demo
- Build a simulation-first end-to-end path from sensor input to a logged, human-approved task proposal.
- Add health checks, structured logs, configuration files, and deterministic safety checks.
- Publish setup instructions and a small baseline benchmark with honest results.

### Days 31–60: Evidence
- Run repeatable simulation scenarios, including sensor dropouts and communication loss.
- Record failures, latency, resource use, intervention rate, and task success.
- Collect only data for which collection and usage permissions are documented.
- Demonstrate the system to prospective users and gather written feedback.

### Days 61–90: Pilot readiness
- Select one customer problem and define acceptance criteria with a prospective pilot partner.
- Prepare a pilot plan, safety case, data-protection plan, support boundaries, and cost estimate.
- Conduct hardware-in-the-loop and controlled physical tests before any public-road, floodwater, or unsupervised deployment.
- Decide whether evidence supports a paid pilot, further R&D, or a change of market.

## Success gates

Do not advance a stage just because code exists. Advance when the prior stage has repeatable evidence:
1. Reproducible setup and tests.
2. Stable simulation baseline.
3. Hardware-in-the-loop evidence.
4. Controlled physical demonstration.
5. Independent review of safety and limitations.
6. Pilot acceptance criteria agreed with a real user.
7. Pilot results and commercial case documented.

## Founder operating principles

- State what is implemented, simulated, planned, and physically validated separately.
- Do not invent benchmark numbers, customer logos, certifications, partnerships, or funding.
- Keep an issue tracker with acceptance criteria and evidence links.
- Prioritize a small number of reliable workflows over adding many models.
- Use open-source components with license and model-use review.
- Obtain legal, tax, insurance, privacy, and safety advice appropriate to the operating jurisdiction before commercial deployment.
