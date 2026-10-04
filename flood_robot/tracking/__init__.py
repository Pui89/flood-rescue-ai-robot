from __future__ import annotations

from dataclasses import dataclass

import numpy as np


@dataclass
class TrackedObject:
    track_id: int
    bbox: tuple[float, float, float, float]
    centroid: tuple[float, float]
    age: int = 1
    hits: int = 1

    def update(self, bbox: tuple[float, float, float, float], centroid: tuple[float, float]) -> None:
        self.bbox = bbox
        self.centroid = centroid
        self.age = 1
        self.hits += 1


class CustomObjectTracker:
    def __init__(self, max_age: int = 8, distance_threshold: float = 35.0) -> None:
        self.max_age = max_age
        self.distance_threshold = distance_threshold
        self.tracks: list[TrackedObject] = []
        self.next_id = 1

    @staticmethod
    def _centroid(bbox: tuple[float, float, float, float]) -> tuple[float, float]:
        x1, y1, x2, y2 = bbox
        return ((x1 + x2) / 2.0, (y1 + y2) / 2.0)

    def track(self, detections: list[tuple[float, float, float, float]]) -> list[TrackedObject]:
        if not detections:
            for track in self.tracks:
                track.age += 1
            self.tracks = [track for track in self.tracks if track.age <= self.max_age]
            return self.tracks

        current_centroids = [self._centroid(det) for det in detections]
        assigned = np.zeros(len(detections), dtype=bool)

        for track in self.tracks:
            best_index = None
            best_distance = np.inf
            for det_index, centroid in enumerate(current_centroids):
                if assigned[det_index]:
                    continue
                distance = np.linalg.norm(np.array(centroid) - np.array(track.centroid))
                if distance < best_distance:
                    best_distance = distance
                    best_index = det_index

            if best_index is not None and best_distance < self.distance_threshold:
                track.update(detections[best_index], current_centroids[best_index])
                assigned[best_index] = True

        for det_index, det in enumerate(detections):
            if assigned[det_index]:
                continue
            self.tracks.append(
                TrackedObject(
                    track_id=self.next_id,
                    bbox=det,
                    centroid=self._centroid(det),
                    age=1,
                    hits=1,
                )
            )
            self.next_id += 1

        survivors = []
        for track in self.tracks:
            track.age += 1
            if track.age <= self.max_age:
                survivors.append(track)
        self.tracks = survivors
        return self.tracks
