from __future__ import annotations

from dataclasses import dataclass, field
from typing import List

from src.core.types import TrajectoryPoint


@dataclass
class Trajectory:
    track_id: int
    points: List[TrajectoryPoint] = field(default_factory=list)

    def add_point(self, point: TrajectoryPoint) -> None:
        self.points.append(point)

    def latest(self) -> TrajectoryPoint | None:
        if not self.points:
            return None
        return self.points[-1]
