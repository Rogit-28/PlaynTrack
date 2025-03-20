from __future__ import annotations

import cv2
import numpy as np


def render_speed(
    frame: np.ndarray, speed_kmh: float, position: tuple[int, int]
) -> np.ndarray:
    """Render speed text with semi-transparent black background near the ball."""
    text = f"{speed_kmh:.1f} km/h"
    font = cv2.FONT_HERSHEY_SIMPLEX
    font_scale = 0.6
    thickness = 2
    (text_w, text_h), baseline = cv2.getTextSize(text, font, font_scale, thickness)

    pad = 4
    x, y = position
    # Ensure the background stays within frame bounds
    bg_x1 = max(x - pad, 0)
    bg_y1 = max(y - text_h - pad, 0)
    bg_x2 = min(x + text_w + pad, frame.shape[1])
    bg_y2 = min(y + baseline + pad, frame.shape[0])

    # Semi-transparent black background
    overlay = frame.copy()
    cv2.rectangle(overlay, (bg_x1, bg_y1), (bg_x2, bg_y2), (0, 0, 0), -1)
    cv2.addWeighted(overlay, 0.6, frame, 0.4, 0, frame)

    # White text on top
    cv2.putText(
        frame,
        text,
        (x, y),
        font,
        font_scale,
        (255, 255, 255),
        thickness,
        cv2.LINE_AA,
    )
    return frame
