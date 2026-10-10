# Cost Safety, Billing and External-Service Policy

**Purpose:** keep this repository local-first and reduce accidental paid-service use. This document is a policy, not a guarantee that GitHub or third-party providers cannot bill an account.

## Defaults
- Local execution, synthetic/recorded-data tests, and local simulation are the default.
- Do not automatically provision cloud GPUs, cloud infrastructure, hosted robots, managed databases, paid AI APIs, or paid telemetry services.
- Any paid or remote service must be optional, disabled by default, and documented with pricing, rate limits, privacy implications, and a local alternative.
- Do not commit API keys, tokens, cloud credentials, payment details, environment files, or sensitive sensor/case data.
- Model weights, datasets, simulators, and hosted endpoints can have separate licences, download/storage costs, quotas, and fees. Check the exact provider terms before use.

## Project-specific note
This is a flood-rescue research prototype, not a validated emergency-response product. Keep ROS 2, simulation, SLAM, and replay tests local by default.
Live camera/RTSP, MQTT, WebSocket, remote AI, and telemetry functions can expose data and may incur costs depending on the endpoint you configure. Do not send data to hard-coded unknown endpoints.

## Before running or merging code
1. Inspect source code, notebooks, dependency manifests, Docker/Compose files, ROS launch files, and GitHub Actions workflows for remote endpoints, cloud provisioning, paid APIs, telemetry uploads, auto-downloads, and unbounded retry loops.
2. Keep remote integrations off unless deliberately configured. Missing credentials should disable an optional integration or fail clearly; code must not create resources or accounts automatically.
3. Review data leaving the machine, model licences, download sizes, and any provider's current pricing.
4. For CI, prefer bounded unit tests and linting; do not run paid inference, rent GPUs, deploy cloud resources, or connect to physical hardware automatically.
5. Use least-privilege workflow permissions, sensible timeouts, and reviewed third-party actions.

## GitHub and provider billing checklist
- Review GitHub Billing & Licensing, usage, Actions, Codespaces, Packages, and any metered features in account/organization settings.
- Disable unused features/workflows. Set budgets and alerts where offered, and verify whether they stop usage or only send notifications.
- Check every separate cloud/AI provider billing dashboard. GitHub settings cannot enforce another provider's spending limits.
- Review past invoices and usage records. A repository change cannot cancel an existing balance, reverse a retroactive charge, or decide whether a provider may bill for earlier usage.
- For a suspected incorrect charge, contact the provider's official billing support promptly with invoice references and usage dates.

## Local-first operation
Follow the repository's local installation and test instructions. Inspect dependencies before installing. Avoid live-stream, cloud, or hosted-model features unless you intentionally configure them.

## Change-control rule
Any change adding an external endpoint, API key, cloud resource, auto-download, telemetry export, or paid service must update this file and explain the service, default state, data leaving the machine, cost limits/disable steps, licence/pricing, and local alternative.

**No billing guarantee:** this repository cannot inspect personal billing settings, guarantee that a provider will not apply a later charge, or prevent charges caused by credentials, services, or resources configured outside the repository.