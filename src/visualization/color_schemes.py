from __future__ import annotations

from typing import Tuple

from src.core.config import VisualizationConfig


def speed_color(speed_kmh: float, config: VisualizationConfig) -> Tuple[int, int, int]:
    if speed_kmh < 30:
        return config.speed_color_low
    if speed_kmh < 50:
        return config.speed_color_mid
    return config.speed_color_high
