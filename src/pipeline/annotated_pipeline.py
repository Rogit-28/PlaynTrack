from __future__ import annotations

from pathlib import Path

from src.core.config import AppConfig
from src.export.annotated_exporter import export_annotated_video
from src.export.csv_exporter import export_rallies_csv, export_shots_csv
from src.export.trajectory_exporter import export_trajectory_csv
from src.input.video_loader import VideoLoader
from src.pipeline.processor import PipelineResult, VideoProcessor


def run_with_export(
    config: AppConfig,
    video_path: Path,
    output_path: Path,
) -> tuple[PipelineResult, Path, Path, Path, Path]:
    processor = VideoProcessor(config)
    result = processor.run(video_path)

    loader = VideoLoader(video_path)
    frames = [frame for _, frame in loader.read_frames()]
    fps = config.video.export_fps or result.fps
    players_by_frame = [result.player_detections.get(idx, []) for idx in range(len(frames))]
    export_path = export_annotated_video(
        frames,
        result.trajectory,
        result.events,
        players_by_frame,
        output_path,
        fps,
        config.visualization,
    )

    shots_path = Path("data/outputs") / f"shots_{video_path.stem}.csv"
    rallies_path = Path("data/outputs") / f"rallies_{video_path.stem}.csv"
    trajectory_path = Path("data/outputs") / f"trajectory_{video_path.stem}.csv"

    if result.match_stats:
        export_shots_csv(result.match_stats, shots_path)
        export_rallies_csv(result.match_stats, rallies_path)
    export_trajectory_csv(result.trajectory, result.events, trajectory_path, fps)

    return result, export_path, shots_path, rallies_path, trajectory_path
