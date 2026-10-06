from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any

@dataclass
class PerceptionState:
    detections: list[dict[str, Any]] = field(default_factory=list)
    masks: list[dict[str, Any]] = field(default_factory=list)
    tracks: list[dict[str, Any]] = field(default_factory=list)
    scene_description: str = ''
    visibility: str = 'normal'
    unknowns: list[str] = field(default_factory=list)
    confidence: float = 0.0

class AdvancedPerception:
    '''Optional adapter boundary for YOLO + SAM3 + Qwen3-VL.''''
    def __init__(self, detector=None, segmenter=None, vision_model=None):
        self.detector = detector
        self.segmenter = segmenter
        self.vision_model = vision_model

    def run(self, frame, *, prompt='Find people, hazards, occlusions and unknown objects.') -> PerceptionState:
        detections = self.detector(frame) if self.detector else []
        masks = self.segmenter(frame, detections) if self.segmenter else []
        scene = self.vision_model(frame, prompt) if self.vision_model else ''
        return PerceptionState(detections=detections, masks=masks, scene_description=str(scene), confidence=self._aggregate_confidence(detections))

    @staticmethod
    def _aggregate_confidence(detections):
        if not detections:
            return 0.0
        return sum(float(d.get('confidence', 0.0)) for d in detections) / len(detections)