from __future__ import annotations

from typing import List

from src.analytics.match_stats import MatchStats, RallyStats, ShotStats
from src.segmentation.event_types import Event, EventType


def compute_match_stats(events: List[Event]) -> MatchStats:
    shots: List[ShotStats] = []
    rallies: List[RallyStats] = []
    current_rally_start = None
    current_rally_id = 0
    rally_shots: List[ShotStats] = []
    rally_bounces = 0
    max_speed = 0.0

    for event in events:
        if event.event_type == EventType.RALLY_START:
            current_rally_start = event.timestamp
            current_rally_id += 1
            rally_shots = []
            rally_bounces = 0
        elif event.event_type == EventType.BOUNCE:
            rally_bounces += 1
        elif event.event_type == EventType.SHOT:
            speed = event.speed or 0.0
            max_speed = max(max_speed, speed)
            rally_shots.append(
                ShotStats(
                    rally_id=current_rally_id,
                    frame_idx=event.frame_idx,
                    timestamp=event.timestamp,
                    speed_kmh=speed,
                    player_id=event.player_id,
                )
            )
            shots.append(rally_shots[-1])
        elif event.event_type == EventType.RALLY_END and current_rally_start is not None:
            end_time = event.timestamp
            duration = max(end_time - current_rally_start, 0.0)
            shot_count = len(rally_shots)
            avg_speed = sum(shot.speed_kmh for shot in rally_shots) / shot_count if shot_count else 0.0
            rally_max_speed = max((shot.speed_kmh for shot in rally_shots), default=0.0)
            rallies.append(
                RallyStats(
                    rally_id=current_rally_id,
                    start_time=current_rally_start,
                    end_time=end_time,
                    duration=duration,
                    shot_count=shot_count,
                    bounce_count=rally_bounces,
                    max_speed=rally_max_speed,
                    avg_speed=avg_speed,
                )
            )
            current_rally_start = None

    total_duration = rallies[-1].end_time if rallies else 0.0
    total_shots = len(shots)
    avg_speed = sum(shot.speed_kmh for shot in shots) / total_shots if total_shots else 0.0

    return MatchStats(
        total_duration=total_duration,
        total_rallies=len(rallies),
        total_shots=total_shots,
        max_speed=max_speed,
        avg_speed=avg_speed,
        rallies=rallies,
        shots=shots,
    )
