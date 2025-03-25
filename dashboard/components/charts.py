from __future__ import annotations

import pandas as pd
import plotly.express as px

from src.analytics.match_stats import MatchStats


def speed_chart(match_stats: MatchStats | None):
    if not match_stats or not match_stats.shots:
        return None
    df = pd.DataFrame(
        [
            {
                "timestamp": shot.timestamp,
                "speed_kmh": shot.speed_kmh,
                "rally_id": shot.rally_id,
            }
            for shot in match_stats.shots
        ]
    )
    fig = px.line(df, x="timestamp", y="speed_kmh", color="rally_id", markers=True)
    fig.update_layout(title="Shot Speed Over Time", xaxis_title="Time (s)", yaxis_title="Speed (km/h)")
    return fig
