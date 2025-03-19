from __future__ import annotations

from typing import Iterable

import cv2
import numpy as np

from src.core.config import VisualizationConfig
from src.core.types import TrajectoryPoint
from src.visualization.color_schemes import speed_color


def render_trajectory(
    frame: np.ndarray,
    trajectory: Iterable[TrajectoryPoint],
    config: VisualizationConfig,
) -> np.ndarray:
    """Draw a gradient trajectory trail with decreasing opacity and varying width."""
    points = list(trajectory)[-config.trail_length :]
    if len(points) < 2:
        return frame

    overlay = frame.copy()
    n = len(points)

    for idx in range(1, n):
        alpha = (idx + 1) / n  # 0→1 from tail to head
        thickness = max(1, int(1 + 2 * alpha))  # 1px at tail → 3px at head
        base_color = speed_color(points[idx].speed_kmh or 0.0, config)
        color = (int(base_color[0]), int(base_color[1]), int(base_color[2]))

        pt1 = (int(points[idx - 1].x), int(points[idx - 1].y))
        pt2 = (int(points[idx].x), int(points[idx].y))
        cv2.line(overlay, pt1, pt2, color, thickness, cv2.LINE_AA)

    # Blend with decreasing opacity by mixing original and overlay
    cv2.addWeighted(overlay, 0.8, frame, 0.2, 0, frame)

    # Draw a solid circle at the head for visibility
    head = points[-1]
    head_color = speed_color(head.speed_kmh or 0.0, config)
    cv2.circle(
        frame,
        (int(head.x), int(head.y)),
        4,
        (int(head_color[0]), int(head_color[1]), int(head_color[2])),
        -1,
        cv2.LINE_AA,
    )

    return frame
