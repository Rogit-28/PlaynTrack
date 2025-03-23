from __future__ import annotations

import csv
from pathlib import Path

from src.analytics.match_stats import MatchStats


def export_shots_csv(match_stats: MatchStats, output_path: Path) -> Path:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with output_path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.writer(handle)
        writer.writerow(
            [
                "rally_id",
                "frame_idx",
                "timestamp",
                "speed_kmh",
                "player_id",
            ]
        )
        for shot in match_stats.shots:
            writer.writerow(
                [shot.rally_id, shot.frame_idx, shot.timestamp, shot.speed_kmh, shot.player_id]
            )
    return output_path


def export_rallies_csv(match_stats: MatchStats, output_path: Path) -> Path:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with output_path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.writer(handle)
        writer.writerow(
            [
                "rally_id",
                "start_time",
                "end_time",
                "duration",
                "shot_count",
                "bounce_count",
                "max_speed",
                "avg_speed",
            ]
        )
        for rally in match_stats.rallies:
            writer.writerow(
                [
                    rally.rally_id,
                    rally.start_time,
                    rally.end_time,
                    rally.duration,
                    rally.shot_count,
                    rally.bounce_count,
                    rally.max_speed,
                    rally.avg_speed,
                ]
            )
    return output_path
