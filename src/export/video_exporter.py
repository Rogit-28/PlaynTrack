from __future__ import annotations

from pathlib import Path
from typing import Iterable, Optional

import cv2
import numpy as np


def export_video(
    frames: Iterable[np.ndarray],
    output_path: Path,
    fps: float,
    frame_size: tuple[int, int],
) -> Path:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    fourcc = cv2.VideoWriter_fourcc(*"mp4v")
    writer = cv2.VideoWriter(str(output_path), fourcc, fps, frame_size)

    for frame in frames:
        writer.write(frame)

    writer.release()
    return output_path
