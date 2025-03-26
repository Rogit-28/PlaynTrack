from __future__ import annotations

from pathlib import Path
from typing import Optional

from src.analytics.match_stats import MatchStats
from src.core.types import TrajectoryPoint
from src.export.csv_exporter import export_rallies_csv, export_shots_csv
from src.export.trajectory_exporter import export_trajectory_csv
from src.segmentation.event_types import Event


def export_all_csv(
    match_stats: Optional[MatchStats],
    trajectory: list[TrajectoryPoint],
    events: list[Event],
    video_stem: str,
    fps: float,
    output_dir: Path | None = None,
) -> dict[str, Path]:
    """Export all CSV files and return a mapping of name → path."""
    if output_dir is None:
        output_dir = Path("data/outputs")
    output_dir.mkdir(parents=True, exist_ok=True)

    shots_path = output_dir / f"shots_{video_stem}.csv"
    rallies_path = output_dir / f"rallies_{video_stem}.csv"
    trajectory_path = output_dir / f"trajectory_{video_stem}.csv"

    if match_stats:
        export_shots_csv(match_stats, shots_path)
        export_rallies_csv(match_stats, rallies_path)
    export_trajectory_csv(trajectory, events, trajectory_path, fps)

    return {
        "shots": shots_path,
        "rallies": rallies_path,
        "trajectory": trajectory_path,
    }
