import argparse

import numpy as np

from flood_robot.config import SystemConfig
from flood_robot.data.synthetic_scene import SyntheticFloodSceneGenerator
from flood_robot.visualization.video_renderer import DemoVideoRenderer


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Generate a synthetic flood-rescue demo clip")
    parser.add_argument("--fps", type=int, default=8)
    parser.add_argument("--seconds", type=float, default=3.0)
    parser.add_argument("--output", type=str, default="demo_output/flood_scene.gif")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    config = SystemConfig()
    generator = SyntheticFloodSceneGenerator(width=config.image_size[1], height=config.image_size[0])
    renderer = DemoVideoRenderer(fps=args.fps)

    frames = [generator.generate_frame(t=t) for t in np.linspace(0.0, args.seconds, int(args.fps * args.seconds))]
    renderer.save_gif(frames, args.output)
    print(f"Saved demo animation to {args.output}")


if __name__ == "__main__":
    main()
