# Security Policy

This robot operates in environments where compromise can create physical risk.

## Security boundary

AI models are untrusted decision-support components. No VLM, generative model, remote API, dashboard or cloud service may bypass the deterministic safety supervisor or emergency-stop path.

## Required production controls

- unique device identity and certificate-based authentication;
- mutual TLS for network services;
- role-based access control and MFA;
- segmented control, AI, management and cloud networks;
- signed firmware, containers, configurations and AI models;
- SHA-256 integrity and provenance metadata;
- anti-rollback OTA updates;
- protected audit logs;
- SBOM and dependency scanning;
- secrets outside Git;
- credential/certificate revocation;
- incident response and safe-stop procedures;
- offline-safe operation when cloud connectivity fails.

## AI security

Treat prompts, images, audio, sensor streams and model outputs as untrusted input. Prompt injection, adversarial scenes, corrupted sensor data and model hallucination must not create direct actuator authority.

Security should be managed together with trustworthy-AI practices such as validity, reliability, safety, security, resilience, accountability and transparency. citeturn0search3turn0search5

## Disclosure

Report suspected vulnerabilities privately through GitHub security channels when available. Do not publish exploitable details before a fix or coordinated disclosure.

This policy is an engineering baseline, not a claim of certification or field security.
