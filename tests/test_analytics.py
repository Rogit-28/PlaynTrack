from __future__ import annotations

import pytest

from src.analytics.aggregator import compute_match_stats
from src.analytics.match_stats import MatchStats, RallyStats, ShotStats
from src.segmentation.event_types import Event, EventType


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _event(
    event_type: EventType, frame_idx: int, speed: float = None, player_id: int = None
) -> Event:
    return Event(
        event_type=event_type,
        frame_idx=frame_idx,
        timestamp=frame_idx / 30.0,
        position=(0.0, 0.0),
        speed=speed,
        player_id=player_id,
    )


# ---------------------------------------------------------------------------
# compute_match_stats tests
# ---------------------------------------------------------------------------


def test_compute_match_stats_with_rallies_and_shots():
    """A complete rally with shots should produce correct stats."""
    events = [
        _event(EventType.RALLY_START, frame_idx=0),
        _event(EventType.SHOT, frame_idx=10, speed=50.0, player_id=1),
        _event(EventType.BOUNCE, frame_idx=15),
        _event(EventType.SHOT, frame_idx=20, speed=60.0, player_id=2),
        _event(EventType.RALLY_END, frame_idx=30),
    ]
    stats = compute_match_stats(events)

    assert stats.total_rallies == 1
    assert stats.total_shots == 2
    assert stats.max_speed == 60.0
    assert stats.avg_speed == pytest.approx(55.0)
    assert len(stats.rallies) == 1
    assert stats.rallies[0].shot_count == 2
    assert stats.rallies[0].bounce_count == 1


def test_compute_match_stats_with_empty_events():
    stats = compute_match_stats([])

    assert stats.total_rallies == 0
    assert stats.total_shots == 0
    assert stats.max_speed == 0.0
    assert stats.avg_speed == 0.0
    assert stats.rallies == []
    assert stats.shots == []


# ---------------------------------------------------------------------------
# MatchStats tests
# ---------------------------------------------------------------------------


def test_match_stats_speed_histogram_bins():
    """Histogram should bin shot speeds correctly with 10 km/h bin width."""
    shots = [
        ShotStats(
            rally_id=1, frame_idx=10, timestamp=0.33, speed_kmh=5.0, player_id=None
        ),
        ShotStats(
            rally_id=1, frame_idx=20, timestamp=0.66, speed_kmh=15.0, player_id=None
        ),
        ShotStats(
            rally_id=1, frame_idx=30, timestamp=1.0, speed_kmh=25.0, player_id=None
        ),
    ]
    stats = MatchStats(
        total_duration=1.0,
        total_rallies=1,
        total_shots=3,
        max_speed=25.0,
        avg_speed=15.0,
        rallies=[],
        shots=shots,
    )

    # max_speed=25, bin_width=10 -> max_bin = 25//10 + 1 = 3 bins: [0-10), [10-20), [20-30)
    assert len(stats.speed_histogram) == 3
    assert stats.speed_histogram[0] == 1  # 5 km/h -> bin 0
    assert stats.speed_histogram[1] == 1  # 15 km/h -> bin 1
    assert stats.speed_histogram[2] == 1  # 25 km/h -> bin 2


def test_match_stats_post_init_auto_builds_histogram():
    """__post_init__ should auto-build the histogram when not provided."""
    stats = MatchStats(
        total_duration=0.0,
        total_rallies=0,
        total_shots=0,
        max_speed=0.0,
        avg_speed=0.0,
        rallies=[],
        shots=[],
    )
    # Empty shots -> empty histogram
    assert stats.speed_histogram == []


# ---------------------------------------------------------------------------
# Dataclass creation tests
# ---------------------------------------------------------------------------


def test_shot_stats_creation():
    shot = ShotStats(
        rally_id=1, frame_idx=10, timestamp=0.33, speed_kmh=55.0, player_id=1
    )
    assert shot.rally_id == 1
    assert shot.speed_kmh == 55.0
    assert shot.player_id == 1


def test_rally_stats_creation():
    rally = RallyStats(
        rally_id=1,
        start_time=0.0,
        end_time=2.0,
        duration=2.0,
        shot_count=4,
        bounce_count=3,
        max_speed=80.0,
        avg_speed=60.0,
    )
    assert rally.rally_id == 1
    assert rally.duration == 2.0
    assert rally.max_speed == 80.0
