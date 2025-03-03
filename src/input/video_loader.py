from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

import cv2

from src.core.exceptions import VideoProcessingError


@dataclass
class VideoMetadata:
    path: Path
    fps: float
    frame_count: int
    width: int
    height: int


class VideoLoader:
    def __init__(self, path: Path) -> None:
        self.path = Path(path)
        if not self.path.exists():
            raise FileNotFoundError(f"Video not found: {self.path}")

    def open(self) -> cv2.VideoCapture:
        capture = cv2.VideoCapture(str(self.path))
        if not capture.isOpened():
            raise VideoProcessingError(f"Failed to open video: {self.path}")
        return capture

    def metadata(self) -> VideoMetadata:
        capture = self.open()
        fps = capture.get(cv2.CAP_PROP_FPS) or 0.0
        frame_count = int(capture.get(cv2.CAP_PROP_FRAME_COUNT) or 0)
        width = int(capture.get(cv2.CAP_PROP_FRAME_WIDTH) or 0)
        height = int(capture.get(cv2.CAP_PROP_FRAME_HEIGHT) or 0)
        capture.release()
        return VideoMetadata(
            path=self.path,
            fps=fps,
            frame_count=frame_count,
            width=width,
            height=height,
        )

    def read_frames(self):
        capture = self.open()
        frame_idx = 0
        while True:
            success, frame = capture.read()
            if not success:
                break
            yield frame_idx, frame
            frame_idx += 1
        capture.release()
