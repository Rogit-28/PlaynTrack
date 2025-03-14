from __future__ import annotations

from typing import List

from src.core.types import TrajectoryPoint


def detect_bounces(trajectory: List[TrajectoryPoint]) -> List[int]:
    if len(trajectory) < 3:
        return []

    bounce_frames: List[int] = []
    for prev_point, point, next_point in zip(trajectory, trajectory[1:], trajectory[2:]):
        if prev_point.vy < 0 <= next_point.vy:
            bounce_frames.append(point.frame_idx)
    return bounce_frames
