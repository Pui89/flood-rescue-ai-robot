# Pui89 AI Robotics — Open-Source and Commercial IP Policy

This is an engineering policy draft, not legal advice. Obtain qualified legal advice before licensing, patent filing, collecting sensitive data, or signing commercial agreements.

## Open-source-first approach

Pui89 should use open standards and reusable upstream projects wherever practical, publish useful research artifacts, and make commercial value through dependable integration, validated performance, support, domain expertise, and customer outcomes.

Potential public assets:
- Architecture and interface specifications.
- Simulation worlds and synthetic test scenarios.
- Reproducible evaluation scripts and aggregate results.
- Generic ROS 2 integrations.
- Selected datasets with documented rights.
- Documentation, example applications, and non-sensitive demos.

Potential commercial services/assets:
- Integration and deployment.
- Customer-specific configuration and support.
- Hosted fleet monitoring and operations.
- Model evaluation and domain adaptation.
- Data curation services and permissioned customer datasets.
- Managed updates and support commitments.

Do not promise exclusivity over open-source components or datasets whose terms grant broad rights to others.

## Existing repository license obligations

The three existing Pui89 project repositories have been described as MIT-licensed. Verify each repository's current LICENSE file and contribution history before relying on that description.

MIT-licensed code can generally be used commercially if the license conditions are followed, including retaining the copyright and permission notice. Do not imply that existing MIT-licensed code has become proprietary merely because it is used in a commercial product.

For future code, decide the license before accepting external contributions. If the project is intended to remain permissively open, use a consistent license and contributor policy. Keep proprietary modules in clearly separated repositories or services only where the separation is technically and legally sound.

## Third-party review

For every dependency, model, dataset, simulator asset, hardware driver, and pretrained weight, record:
- Name, version, source URL, and checksum where practical.
- Software license and model-specific license.
- Commercial use and redistribution rights.
- Attribution, notice, source disclosure, or share-alike obligations.
- Dataset consent, privacy, and usage restrictions.
- Known patents, export restrictions, and relevant contractual terms.
- Intended use in product, cloud, or edge deployment.

Important: source-code license and model-weight license can differ. An open repository does not automatically mean its weights, training data, or commercial use are unrestricted.

## IP and public disclosure

Before publishing a potentially patentable invention, discuss it with a qualified patent professional. Public disclosure can affect patent rights in some jurisdictions. Keep dated invention records and distinguish third-party components from original work.

Do not claim that a patent has been filed or granted unless documentary evidence exists.

## Data governance

- Obtain documented permission for all collected data.
- Avoid collecting personal or sensitive data unless necessary and lawful.
- Define retention, access, deletion, and security controls.
- Separate public benchmark data from customer-confidential data.
- Do not publish identifiable footage or location data without appropriate rights.
- Record dataset provenance and annotation guidelines.
- Never fabricate or silently relabel test data to improve results.

## Security and release hygiene

- Never commit API keys, passwords, private keys, or customer secrets.
- Use secret scanning and dependency scanning.
- Publish a vulnerability reporting process in SECURITY.md.
- Generate a software bill of materials for release artifacts.
- Pin versions, sign releases where feasible, and document update/rollback procedures.
