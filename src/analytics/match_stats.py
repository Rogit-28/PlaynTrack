from __future__ import annotations

from dataclasses import dataclass
from typing import List, Optional


@dataclass
class ShotStats:
    rally_id: int
    frame_idx: int
    timestamp: float
    speed_kmh: float
    player_id: Optional[int]


@dataclass
class RallyStats:
    rally_id: int
    start_time: float
    end_time: float
    duration: float
    shot_count: int
    bounce_count: int
    max_speed: float
    avg_speed: float


@dataclass
class MatchStats:
    total_duration: float
    total_rallies: int
    total_shots: int
    max_speed: float
    avg_speed: float
    rallies: List[RallyStats]
    shots: List[ShotStats]
    speed_histogram: List[int] = None  # type: ignore[assignment]

    def __post_init__(self) -> None:
        if self.speed_histogram is None:
            self.speed_histogram = self._build_histogram()

    def _build_histogram(self, bin_width: int = 10) -> List[int]:
        """Build a histogram of shot speeds using *bin_width* km/h bins."""
        if not self.shots:
            return []
        max_bin = int(self.max_speed // bin_width) + 1
        bins = [0] * max_bin
        for shot in self.shots:
            idx = min(int(shot.speed_kmh // bin_width), max_bin - 1)
            bins[idx] += 1
        return bins
