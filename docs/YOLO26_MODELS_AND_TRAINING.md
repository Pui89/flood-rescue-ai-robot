# YOLO26 Models & Training — Flood Rescue

Ultralytics YOLO26 is integrated as the fast visual proposal layer for flood victims, boats, vehicles, debris, floating objects and obstacles. Official YOLO26 supports seven task families with Train, Val, Predict and Export modes. citeturn0search1turn0search0

| Model | Filenames | Task | Training | Validation | Inference | Export |
|---|---|---|---|---|---|---|
| YOLO26 | `yolo26n.pt` · `yolo26s.pt` · `yolo26m.pt` · `yolo26l.pt` · `yolo26x.pt` | Detection | ✅ | ✅ | ✅ | ✅ |
| YOLO26-seg | `yolo26n-seg.pt` … `yolo26x-seg.pt` | Instance Segmentation | ✅ | ✅ | ✅ | ✅ |
| YOLO26-sem | `yolo26n-sem.pt` … `yolo26x-sem.pt` | Semantic Segmentation | ✅ | ✅ | ✅ | ✅ |
| YOLO26-depth | `yolo26n-depth.pt` … `yolo26x-depth.pt` | Depth Estimation | ✅ | ✅ | ✅ | ✅ |
| YOLO26-cls | `yolo26n-cls.pt` … `yolo26x-cls.pt` | Classification | ✅ | ✅ | ✅ | ✅ |
| YOLO26-pose | `yolo26n-pose.pt` … `yolo26x-pose.pt` | Pose / Keypoints | ✅ | ✅ | ✅ | ✅ |
| YOLO26-obb | `yolo26n-obb.pt` … `yolo26x-obb.pt` | Oriented Detection | ✅ | ✅ | ✅ | ✅ |

Start with `yolo26n.pt` or `yolo26s.pt` for onboard deployment and scale upward after measuring latency, memory and accuracy. `yolo26-p2.yaml` and `yolo26-p6.yaml` are architecture-only variants for custom training. citeturn0search1

## Install
```bash
python -m pip install -U ultralytics huggingface-hub
```

## Dataset
Example `data/flood_yolo26.yaml`:
```yaml
path: data/flood_yolo26
train: images/train
val: images/val
names:
  0: person
  1: child
  2: animal
  3: boat
  4: vehicle
  5: debris
  6: floating_object
  7: obstacle
  8: robot
```

## Training
```bash
yolo detect train model=yolo26n.pt data=data/flood_yolo26.yaml epochs=100 imgsz=640 batch=16
```
Python:
```python
from ultralytics import YOLO
model = YOLO("yolo26n.pt")
model.train(data="data/flood_yolo26.yaml", epochs=100, imgsz=640, batch=16)
```

## Validation
```bash
yolo detect val model=runs/detect/train/weights/best.pt data=data/flood_yolo26.yaml imgsz=640
```
Record mAP50, mAP50-95, precision, recall, per-class errors, latency and memory under rain, night, glare, reflections, occlusion, partial submersion and debris.

## Inference
```bash
yolo detect predict model=runs/detect/train/weights/best.pt source=data/flood_scenes imgsz=640
yolo detect predict model=runs/detect/train/weights/best.pt source=data/flood_scenes nms=False
```
`nms=False` selects YOLO26's end-to-end one-to-one/NMS-free head; the default uses the one-to-many head. citeturn0search1

## Export
```bash
yolo export model=runs/detect/train/weights/best.pt format=onnx
yolo export model=runs/detect/train/weights/best.pt format=engine
```
ONNX, TensorRT, TorchScript and OpenVINO are supported export targets. citeturn0search3turn0search6

## Robot Integration
```text
RGB / Thermal / NIR -> YOLO26 -> victim/hazard candidates
                                |
                         Depth + LiDAR + IMU
                                |
                         3D semantic map
                                |
                    Qwen3-VL / Gemma reasoning
                                |
                     rescue-plan proposal
                                |
                     uncertainty / OOD checks
                                |
                     deterministic safety gate
                                |
                         ROS2 / Nav2
```
YOLO26 remains perception-only. Detection confidence is not rescue authorization, and AI models do not directly command propulsion, manipulators or other actuators.