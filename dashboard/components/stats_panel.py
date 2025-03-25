from __future__ import annotations

import pandas as pd

from src.analytics.match_stats import MatchStats


def stats_summary(match_stats: MatchStats | None) -> dict:
    if not match_stats:
        return {}
    return {
        "total_rallies": match_stats.total_rallies,
        "total_shots": match_stats.total_shots,
        "max_speed": match_stats.max_speed,
        "avg_speed": match_stats.avg_speed,
    }


def shots_dataframe(match_stats: MatchStats | None) -> pd.DataFrame:
    if not match_stats:
        return pd.DataFrame()
    return pd.DataFrame(
        [
            {
                "rally_id": shot.rally_id,
                "frame_idx": shot.frame_idx,
                "timestamp": shot.timestamp,
                "speed_kmh": shot.speed_kmh,
                "player_id": shot.player_id,
            }
            for shot in match_stats.shots
        ]
    )


def rally_dataframe(match_stats: MatchStats | None) -> pd.DataFrame:
    if not match_stats:
        return pd.DataFrame()
    return pd.DataFrame(
        [
            {
                "rally_id": rally.rally_id,
                "start_time": rally.start_time,
                "end_time": rally.end_time,
                "duration": rally.duration,
                "shot_count": rally.shot_count,
                "bounce_count": rally.bounce_count,
                "max_speed": rally.max_speed,
                "avg_speed": rally.avg_speed,
            }
            for rally in match_stats.rallies
        ]
    )
