from flood_robot.config import SystemConfig
from flood_robot.data.synthetic_scene import SyntheticFloodSceneGenerator
from flood_robot.models.depth_estimator import DepthEstimator


def main() -> None:
    config = SystemConfig()
    generator = SyntheticFloodSceneGenerator(width=config.image_size[1], height=config.image_size[0])
    model = DepthEstimator(in_channels=3, base_channels=32)

    print("Synthetic scene generator ready:", generator.width, generator.height)
    print("Depth estimator created:", model.__class__.__name__)
    print("Ready for training on a real flood dataset or synthetic scene dataset.")


if __name__ == "__main__":
    main()
