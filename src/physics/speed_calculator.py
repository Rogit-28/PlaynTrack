from __future__ import annotations

from src.core.types import TrajectoryPoint
from src.physics.homography import Homography


def calculate_speed_kmh(
    homography: Homography,
    p1: TrajectoryPoint,
    p2: TrajectoryPoint,
    fps: float,
) -> float:
    x1, y1 = homography.pixel_to_world((p1.x, p1.y))
    x2, y2 = homography.pixel_to_world((p2.x, p2.y))
    distance = ((x2 - x1) ** 2 + (y2 - y1) ** 2) ** 0.5
    if fps <= 0:
        return 0.0
    speed_mps = distance * fps
    return speed_mps * 3.6
