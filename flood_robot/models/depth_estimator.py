from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

import numpy as np
import torch
from torch import nn


class ConvBlock(nn.Module):
    def __init__(self, in_channels: int, out_channels: int, kernel_size: int = 3, stride: int = 1):
        super().__init__()
        padding = kernel_size // 2
        self.block = nn.Sequential(
            nn.Conv2d(in_channels, out_channels, kernel_size=kernel_size, stride=stride, padding=padding, bias=False),
            nn.BatchNorm2d(out_channels),
            nn.ReLU(inplace=True),
        )

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        return self.block(x)


class DepthEstimator(nn.Module):
    def __init__(self, in_channels: int = 3, base_channels: int = 32):
        super().__init__()
        channels = base_channels
        self.encoder = nn.Sequential(
            ConvBlock(in_channels, channels),
            ConvBlock(channels, channels),
            nn.MaxPool2d(2),
            ConvBlock(channels, channels * 2),
            ConvBlock(channels * 2, channels * 2),
            nn.MaxPool2d(2),
        )
        self.head = nn.Sequential(
            ConvBlock(channels * 2, channels),
            nn.Conv2d(channels, 1, kernel_size=1),
            nn.Sigmoid(),
        )

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        if x.ndim == 3:
            x = x.unsqueeze(0)
        x = self.encoder(x)
        x = self.head(x)
        return x


@dataclass
class DepthEstimateResult:
    depth_map: np.ndarray
    confidence: float = 1.0
    metadata: dict[str, Any] = field(default_factory=dict)


__all__ = ["ConvBlock", "DepthEstimator", "DepthEstimateResult"]
