import argparse

from flood_robot.config import SystemConfig
from flood_robot.pipeline.rescue_pipeline import FloodRescuePipeline


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run the flood rescue AI robot in real time")
    parser.add_argument("--source", type=str, default="0", help="Video source: webcam index or video file path")
    parser.add_argument("--display", action="store_true", default=True, help="Display the live output window")
    parser.add_argument("--no-display", dest="display", action="store_false", help="Disable display")
    parser.add_argument("--max-frames", type=int, default=None, help="Optional cap on frames processed")
    parser.add_argument("--fps-limit", type=float, default=30.0, help="Maximum processing FPS")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    config = SystemConfig(stream_source=args.source, display=args.display, fps_target=int(args.fps_limit))
    pipeline = FloodRescuePipeline(config)
    pipeline.run_real_time(source=args.source, display=args.display, max_frames=args.max_frames)


if __name__ == "__main__":
    main()
