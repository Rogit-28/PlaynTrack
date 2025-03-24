from __future__ import annotations

from pathlib import Path
from typing import Iterable, List

import numpy as np

from src.core.config import VisualizationConfig
from src.export.video_exporter import export_video
from src.segmentation.event_types import Event
from src.visualization.ar_visualizer import render_overlay


def export_annotated_video(
    frames: Iterable[np.ndarray],
    trajectory: List,
    events: List[Event],
    players_by_frame: List[List] | None,
    output_path: Path,
    fps: float,
    config: VisualizationConfig,
) -> Path:
    rendered_frames = []
    frame_size = None
    for idx, frame in enumerate(frames):
        if frame_size is None:
            frame_size = (frame.shape[1], frame.shape[0])
        players = players_by_frame[idx] if players_by_frame and idx < len(players_by_frame) else None
        rendered_frames.append(render_overlay(frame.copy(), trajectory, events, config, players))

    if frame_size is None:
        raise ValueError("No frames to export")

    return export_video(rendered_frames, output_path, fps, frame_size)
