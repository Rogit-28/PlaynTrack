from __future__ import annotations

import cv2
import numpy as np


def render_stats(frame: np.ndarray, lines: list[str], origin: tuple[int, int] = (10, 30)) -> np.ndarray:
    x, y = origin
    for line in lines:
        cv2.putText(frame, line, (x, y), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
        y += 22
    return frame
