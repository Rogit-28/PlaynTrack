from __future__ import annotations

import pandas as pd

from src.analytics.match_stats import MatchStats


def rally_timeline(match_stats: MatchStats | None) -> pd.DataFrame:
    if not match_stats:
        return pd.DataFrame()
    return pd.DataFrame(
        [
            {
                "rally_id": rally.rally_id,
                "start_time": rally.start_time,
                "end_time": rally.end_time,
                "duration": rally.duration,
            }
            for rally in match_stats.rallies
        ]
    )
