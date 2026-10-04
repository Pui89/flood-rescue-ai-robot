import numpy as np

from flood_robot.config import SystemConfig
from flood_robot.pipeline.rescue_pipeline import FloodRescuePipeline


def main() -> None:
    config = SystemConfig()
    pipeline = FloodRescuePipeline(config)

    height, width = config.image_size
    frame = np.zeros((height, width, 3), dtype=np.uint8)
    frame[:, :, 0] = 80
    frame[:, :, 1] = 130
    frame[:, :, 2] = 180

    for x in range(0, width, 80):
        frame[:, x : x + 10, :] = np.array([0, 120, 160], dtype=np.uint8)

    object_boxes = [
        (120, 220, 160, 310),
        (250, 180, 300, 280),
        (420, 240, 470, 330),
    ]

    results = pipeline.process_frame(frame, detections=object_boxes)
    print(f"Depth shape: {results['depth_map'].shape}")
    print(f"Hazard score: {results['hazard_score']:.4f}")
    print(f"Tracked object count: {len(results['tracked_objects'])}")


if __name__ == "__main__":
    main()
