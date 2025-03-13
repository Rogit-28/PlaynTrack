from __future__ import annotations

from typing import List

import numpy as np

from src.core.config import SegmentationConfig
from src.core.types import TrajectoryPoint


def detect_shots(trajectory: List[TrajectoryPoint], config: SegmentationConfig) -> List[int]:
    if len(trajectory) < 3:
        return []

    shot_frames: List[int] = []
    for prev_point, point, next_point in zip(trajectory, trajectory[1:], trajectory[2:]):
        v1 = np.array([point.x - prev_point.x, point.y - prev_point.y])
        v2 = np.array([next_point.x - point.x, next_point.y - point.y])
        if np.linalg.norm(v1) == 0 or np.linalg.norm(v2) == 0:
            continue
        angle = np.degrees(
            np.arccos(
                np.clip(
                    np.dot(v1, v2) / (np.linalg.norm(v1) * np.linalg.norm(v2)),
                    -1.0,
                    1.0,
                )
            )
        )
        if angle >= config.shot_angle_threshold_deg:
            shot_frames.append(point.frame_idx)
    return shot_frames
