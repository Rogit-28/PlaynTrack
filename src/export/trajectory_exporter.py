from __future__ import annotations

import csv
from pathlib import Path
from typing import List

from src.core.types import TrajectoryPoint
from src.segmentation.event_types import Event, EventType


def export_trajectory_csv(
    trajectory: List[TrajectoryPoint],
    events: List[Event],
    output_path: Path,
    fps: float,
) -> Path:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    event_map = {event.frame_idx: event.event_type for event in events}

    with output_path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.writer(handle)
        writer.writerow(
            [
                "frame",
                "timestamp",
                "ball_x",
                "ball_y",
                "ball_detected",
                "speed_kmh",
                "event_type",
            ]
        )
        for point in trajectory:
            event_type = event_map.get(point.frame_idx, "")
            writer.writerow(
                [
                    point.frame_idx,
                    point.frame_idx / fps if fps else 0.0,
                    point.x,
                    point.y,
                    point.is_detected,
                    point.speed_kmh or 0.0,
                    event_type.value if isinstance(event_type, EventType) else event_type,
                ]
            )
    return output_path
