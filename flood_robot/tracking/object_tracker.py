from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable

import numpy as np


@dataclass
class TrackedObject:
    track_id: int
    bbox: tuple[int, int, int, int]
    confidence: float
    age: int = 1

    @property
    def centroid(self) -> tuple[float, float]:
        x1, y1, x2, y2 = self.bbox
        return ((x1 + x2) / 2.0, (y1 + y2) / 2.0)


class CustomObjectTracker:
    def __init__(self, max_age: int = 8, distance_threshold: float = 35.0):
        self.max_age = max_age
        self.distance_threshold = distance_threshold
        self.tracks: dict[int, TrackedObject] = {}
        self.next_id = 1

    @staticmethod
    def _centroid(box: tuple[int, int, int, int]) -> tuple[float, float]:
        x1, y1, x2, y2 = box
        return ((x1 + x2) / 2.0, (y1 + y2) / 2.0)

    @staticmethod
    def _iou(box_a: tuple[int, int, int, int], box_b: tuple[int, int, int, int]) -> float:
        x1 = max(box_a[0], box_b[0])
        y1 = max(box_a[1], box_b[1])
        x2 = min(box_a[2], box_b[2])
        y2 = min(box_a[3], box_b[3])
        inter = max(0, x2 - x1) * max(0, y2 - y1)
        area_a = max(0, box_a[2] - box_a[0]) * max(0, box_a[3] - box_a[1])
        area_b = max(0, box_b[2] - box_b[0]) * max(0, box_b[3] - box_b[1])
        union = area_a + area_b - inter
        return 0.0 if union <= 0 else inter / union

    def update(self, detections: Iterable[tuple[int, int, int, int]]) -> list[TrackedObject]:
        dets = [tuple(map(int, det)) for det in detections]
        matched_track_ids: set[int] = set()
        active_tracks: list[TrackedObject] = []

        if self.tracks and dets:
            for track_id, track in self.tracks.items():
                best_idx = None
                best_score = -1.0
                for idx, det in enumerate(dets):
                    if idx in matched_track_ids:
                        continue
                    score = self._iou(track.bbox, det)
                    if score > best_score:
                        best_score = score
                        best_idx = idx
                if best_idx is not None and best_score > 0.1:
                    det = dets[best_idx]
                    track.bbox = det
                    track.age = 1
                    track.confidence = max(track.confidence, 0.5)
                    active_tracks.append(track)
                    matched_track_ids.add(best_idx)

        unmatched = [idx for idx in range(len(dets)) if idx not in matched_track_ids]
        for idx in unmatched:
            det = dets[idx]
            track = TrackedObject(track_id=self.next_id, bbox=det, confidence=0.7)
            self.next_id += 1
            self.tracks[track.track_id] = track
            active_tracks.append(track)

        for track_id in list(self.tracks.keys()):
            if track_id not in {t.track_id for t in active_tracks}:
                track = self.tracks[track_id]
                track.age += 1
                if track.age > self.max_age:
                    del self.tracks[track_id]
                else:
                    self.tracks[track_id] = track

        for track in active_tracks:
            self.tracks[track.track_id] = track

        return sorted(active_tracks, key=lambda t: t.track_id)


__all__ = ["CustomObjectTracker", "TrackedObject"]
