import argparse

from flood_robot.config import SystemConfig
from flood_robot.data.synthetic_scene import SyntheticFloodSceneGenerator
from flood_robot.models.depth_estimator import DepthEstimator


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Create a synthetic flood depth training scaffold")
    parser.add_argument("--epochs", type=int, default=20)
    parser.add_argument("--batch-size", type=int, default=8)
    parser.add_argument("--device", type=str, default="cuda")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    config = SystemConfig()
    generator = SyntheticFloodSceneGenerator(width=config.image_size[1], height=config.image_size[0])
    model = DepthEstimator(in_channels=3, base_channels=config.base_channels)

    print(f"Synthetic scene generator ready: {generator.width}x{generator.height}")
    print(f"Depth estimator created: {model.__class__.__name__}")
    print(f"Requested training config: epochs={args.epochs}, batch_size={args.batch_size}, device={args.device}")
    print("This project includes a training scaffold and can be extended to a real flood dataset.")


if __name__ == "__main__":
    main()
