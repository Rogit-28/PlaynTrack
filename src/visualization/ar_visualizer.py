from __future__ import annotations

from typing import List

import numpy as np

from src.core.config import VisualizationConfig
from src.core.types import TrajectoryPoint
from src.segmentation.event_types import Event, EventType
from src.visualization.speed_overlay import render_speed
from src.visualization.stats_overlay import render_stats
from src.visualization.trajectory_renderer import render_trajectory


def render_overlay(
    frame: np.ndarray,
    trajectory: List[TrajectoryPoint],
    events: List[Event],
    config: VisualizationConfig,
    players: List | None = None,
) -> np.ndarray:
    frame = render_trajectory(frame, trajectory, config)

    for event in events:
        if event.event_type == EventType.SHOT and event.speed is not None:
            frame = render_speed(frame, event.speed, (int(event.position[0]) + 10, int(event.position[1]) - 10))

    if config.show_stats_panel:
        stats = [
            f"Shots: {sum(1 for e in events if e.event_type == EventType.SHOT)}",
            f"Rallies: {sum(1 for e in events if e.event_type == EventType.RALLY_START)}",
        ]
        frame = render_stats(frame, stats)

    if config.show_player_boxes and players:
        from src.visualization.player_overlay import render_players

        frame = render_players(frame, players)

    return frame
