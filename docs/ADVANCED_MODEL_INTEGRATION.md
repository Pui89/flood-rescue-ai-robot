# Advanced Model Integration

This document adds four model families to the flood-rescue embodied-AI roadmap.

## LTX-2.5-Diffusers — generative video / simulation augmentation

LTX-2.5 is a video/audio foundation model supporting image-to-video, video-to-video and multimodal audio/video generation. It is used here for synthetic scenario generation, not direct robot control.

Uses:
- night rain and fog variants
- water reflections and glare
- debris motion
- partial occlusion of people
- rare rescue situations
- camera obstruction and degraded visibility
- video augmentation for LeRobot/perception evaluation

Use Isaac Sim/Isaac Lab for physically grounded simulation and LTX-2.5 for visual diversity. Generated data must be labeled synthetic and should not replace physics-based ground truth.

## MiniMax H3 Turbo LoRA — synthetic video/audio scenarios

The referenced Hugging Face Space is a MiniMax-H3 Turbo LoRA video-generation demo with synchronized soundtrack. It is useful as an offline dataset/scenario generator, especially for audio-visual rescue scenes. The Space is not part of the robot's safety-critical runtime.

Uses:
- rare-event video prototypes
- warning-sound / communication scenarios
- difficult weather and visibility variations
- pre-training and stress-test media

Production use requires license, content, provenance and safety review.

## Google Gemma 4 31B IT — multimodal flood-rescue reasoning

Gemma 4 31B IT is integrated as the high-capacity multimodal reasoning layer for image + text flood-scene interpretation. The official Hugging Face model card supports the Transformers image-text-to-text pipeline and direct AutoProcessor/AutoModelForMultimodalLM loading; vLLM serving is also supported. The model repository is about 62.6 GB, so weights are downloaded at runtime rather than committed to Git.

Uses:
- victim and person-at-risk verification
- flood scene and spatial-context reasoning
- debris, route and occlusion analysis
- thermal/NIR/depth/LiDAR cross-check interpretation
- active-perception recommendations
- rescue-plan cross-checking before candidate actions

Recommended flow:

RGB / thermal / NIR / depth / LiDAR -> perception + tracking -> 3D semantic world state -> Gemma 4 31B IT -> structured rescue decision -> action/VLA candidate -> deterministic safety gate

Gemma is advisory only. It does not directly control motors, navigation actuators or rescue mechanisms. Unseen or occluded people remain unknown, and uncertain model output falls back to re-observation and human review.

## NVIDIA GR00T N1.7 3B — embodied robot policy

GR00T N1.7 3B is integrated as an action-policy candidate for embodied learning. It belongs after perception/reasoning and before the deterministic safety layer.

Recommended flow:

Qwen3-VL/Gemma4 -> task/skill goal -> GR00T candidate action -> safety gate -> controller

Train/adapt it for the specific flood robot embodiment with demonstrations and simulation before physical deployment.

## FLUX 3 Action Base — world-action model

FLUX 3 Action Base is an open-weights 7B world-action model conditioning on camera frames, robot state and text instructions and predicting action chunks together with future video. Its model card states that the base is an adaptation component, not a complete robot policy, and that new embodiments require their own action heads.

Therefore it is registered as a research/action-prediction component rather than a drop-in controller.

Every output must pass workspace limits, human exclusion zones, collision checking, force/torque limits, sensor-health checks and emergency-stop logic.

## Combined architecture

RGB / Thermal / NIR / Depth / LiDAR / IMU
                  |
          YOLO + SAM3 + tracking
                  |
        3D semantic world state
                  |
       Qwen3-VL + Gemma 4 E4B
                  |
        V-JEPA2 future prediction
                  |
       GR00T N1.7 + FLUX 3 Action
                  |
        candidate action set
                  |
      DETERMINISTIC SAFETY GATE
                  |
        ROS2 / Nav2 / MoveIt2
                  |
                ROBOT

Offline simulation/data branch:
Isaac Sim/Isaac Lab + LTX-2.5 + MiniMax H3
                  |
       synthetic rare-event data
                  |
       LeRobot + evaluation suite

## Safety rule

Generative video models never control the robot. Action models only propose candidate actions. The deterministic safety controller has final authority, with human oversight for uncertain or high-consequence rescue operations.
