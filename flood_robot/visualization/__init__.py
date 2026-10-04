import imageio.v3 as iio
import numpy as np
from PIL import Image, ImageDraw


class DemoVideoRenderer:
    def __init__(self, fps: int = 8):
        self.fps = fps

    @staticmethod
    def _annotate_frame(frame: np.ndarray, label: str = "Flood Rescue") -> np.ndarray:
        image = Image.fromarray(frame).convert("RGB")
        draw = ImageDraw.Draw(image)
        draw.rectangle((20, 20, 200, 70), fill=(20, 20, 20, 200))
        draw.text((30, 30), label, fill=(255, 255, 255))
        return np.array(image)

    def save_gif(self, frames: list[np.ndarray], output_path: str) -> str:
        annotated = [self._annotate_frame(frame) for frame in frames]
        iio.imwrite(output_path, annotated, format="GIF", fps=self.fps)
        return output_path

    def save_png(self, frame: np.ndarray, output_path: str) -> str:
        image = Image.fromarray(frame)
        image.save(output_path)
        return output_path
