from __future__ import annotations

from dataclasses import dataclass
from typing import List

from src.core.config import SegmentationConfig
from src.core.types import TrajectoryPoint


@dataclass
class Rally:
    start_frame: int
    end_frame: int
    duration: float
    shots: int


class RallyDetector:
    def __init__(self, config: SegmentationConfig, fps: float) -> None:
        self.config = config
        self.fps = fps

    def detect(self, trajectory: List[TrajectoryPoint]) -> List[Rally]:
        rallies: List[Rally] = []
        if not trajectory:
            return rallies

        gap_frames = int(self.config.rally_gap_seconds * self.fps)
        start = trajectory[0].frame_idx
        last_frame = trajectory[0].frame_idx
        for point in trajectory[1:]:
            if point.frame_idx - last_frame > gap_frames:
                rallies.append(
                    Rally(
                        start_frame=start,
                        end_frame=last_frame,
                        duration=(last_frame - start) / self.fps,
                        shots=0,
                    )
                )
                start = point.frame_idx
            last_frame = point.frame_idx

        rallies.append(
            Rally(
                start_frame=start,
                end_frame=last_frame,
                duration=(last_frame - start) / self.fps,
                shots=0,
            )
        )
        return rallies
