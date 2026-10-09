# Third-Party Licensing and Provenance Policy

This policy covers source code, libraries, container images, datasets, pretrained model code, model weights, documentation, fonts, icons and other assets used in PUI89 Flood Recon.

**The root LICENSE applies to original website/project material only where PUI89 owns the rights to license it. It does not relicense third-party components.** This document is a compliance workflow, not legal advice.

## Required inventory

Maintain a machine-readable software bill of materials (SBOM) and reviewed inventory for every release. For each item record:

- Name, version, source URL, commit or artifact digest.
- Direct/transitive dependency status and intended use.
- License identifier and a copy/link to applicable license or terms.
- Copyright and required attribution/notice text.
- Source changes, patches and distribution method.
- Dataset/model name, version, provenance, intended-use restrictions and redistribution rights.
- Reviewer, review date, unresolved questions and approval status.

## Review rules

1. Review the exact pinned release and files to be shipped. Do not infer a complete license from a repository landing page or default branch.
2. Inspect transitive dependencies, bundled code, firmware, drivers, containers, SDKs and platform-specific terms.
3. Treat model code, pretrained weights, training data, evaluation datasets and generated outputs as separate licensing questions.
4. Verify commercial use, modification, redistribution, attribution, notice, source-disclosure, patent, acceptable-use and field-of-use terms before inclusion.
5. Keep a THIRD_PARTY_NOTICES file with required notices and provide corresponding source/license material where required.
6. Block release when terms are unclear or incompatible with intended distribution; replace the component or obtain written permission.
7. Re-review licenses when versions, weights, datasets, build options or distribution channels change.

## Candidate component register (not an approval list)

| Component | Upstream | Initial review note |
|---|---|---|
| Open3D | https://github.com/isl-org/Open3D | Main project is MIT-licensed; review exact release and bundled dependencies. |
| ONNX Runtime | https://github.com/microsoft/onnxruntime | Main project is MIT-licensed; review execution providers and packaged binaries. |
| DINOv2 | https://github.com/facebookresearch/dinov2 | Verify code license and exact checkpoint/weight terms separately. |
| Anomalib | https://github.com/open-edge-platform/anomalib | Review repository license, model artifacts, datasets and optional dependencies. |
| ROS 2 | https://github.com/ros2/ros2 | Packages have different licenses; inspect every shipped package. |
| Nav2 | https://github.com/ros-navigation/navigation2 | Package and dependency licenses vary; generate an SBOM for the chosen release. |
| nvblox | https://github.com/nvidia-isaac/nvblox | Review exact release, included third-party code and NVIDIA terms. |
| Isaac ROS Visual SLAM | https://github.com/NVIDIA-ISAAC-ROS/isaac_ros_visual_slam | Review package, SDK, binary and NVIDIA platform terms. |
| Ultralytics | https://github.com/ultralytics/ultralytics | AGPL-3.0 and commercial licensing options may apply; legal review before proprietary distribution. |
| OpenCV | https://github.com/opencv/opencv | Review selected modules, build flags and third-party codecs/dependencies. |
| PyTorch | https://github.com/pytorch/pytorch | Review exact release, bundled libraries and separately licensed model artifacts. |
| Eclipse Cyclone DDS | https://github.com/eclipse-cyclonedds/cyclonedds | Review exact version and transitive dependencies. |

This is a starting point only. It does not assert every component has been adopted, approved, or included in a release.

## Datasets and model weights

For every dataset/checkpoint, record original source, exact version or hash, license/terms, commercial-use permission, redistribution permission, attribution, provenance, known limitations and evaluation split. A permissive software license does not automatically grant rights to model weights or training data. Do not redistribute artifacts unless their terms permit it.

## Website assets

Original HTML/CSS/JS and original diagrams created for this project may be covered by the root MIT license where owned by PUI89. Third-party logos, product marks, fonts, icons, images and copied diagrams retain their respective terms and must not be assumed MIT-licensed.

## Release checklist

- [ ] Dependency lock files and SBOM generated.
- [ ] Direct and transitive licenses reviewed for commercial distribution.
- [ ] Model weights and datasets reviewed independently from model code.
- [ ] Required notices, attribution and license texts included.
- [ ] Source-offer or source-disclosure obligations reviewed.
- [ ] NVIDIA/Jetson SDK, firmware, drivers and container terms reviewed.
- [ ] No unknown-license dependency remains in the shipped build.
- [ ] Review archived with release tag and artifact hashes.