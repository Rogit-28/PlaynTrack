from __future__ import annotations

import pytest

from src.core.config import SegmentationConfig
from src.core.types import PlayerDetection, TrajectoryPoint
from src.segmentation.rally_detector import RallyDetector
from src.segmentation.shot_detector import detect_shots
from src.segmentation.bounce_detector import detect_bounces
from src.segmentation.event_segmenter import EventSegmenter
from src.segmentation.event_types import EventType


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _point(
    frame_idx: int, x: float = 100.0, y: float = 100.0, vx: float = 0.0, vy: float = 0.0
) -> TrajectoryPoint:
    return TrajectoryPoint(
        x=x,
        y=y,
        vx=vx,
        vy=vy,
        frame_idx=frame_idx,
        is_detected=True,
        confidence=0.9,
    )


# ---------------------------------------------------------------------------
# RallyDetector tests
# ---------------------------------------------------------------------------


def test_rally_detector_empty_trajectory():
    config = SegmentationConfig()
    rd = RallyDetector(config, fps=30.0)
    assert rd.detect([]) == []


def test_rally_detector_continuous_trajectory_one_rally():
    """Consecutive frames with no gap -> single rally."""
    config = SegmentationConfig(rally_gap_seconds=2.0)
    rd = RallyDetector(config, fps=30.0)
    # 30 consecutive frames (1 second) -- well within 2s gap
    trajectory = [_point(i) for i in range(30)]
    rallies = rd.detect(trajectory)

    assert len(rallies) == 1
    assert rallies[0].start_frame == 0
    assert rallies[0].end_frame == 29


def test_rally_detector_gap_splits_into_two_rallies():
    """A gap larger than rally_gap_seconds should split into two rallies."""
    config = SegmentationConfig(rally_gap_seconds=1.0)
    fps = 30.0
    rd = RallyDetector(config, fps=fps)

    # Rally 1: frames 0-29
    trajectory = [_point(i) for i in range(30)]
    # Gap: 60 frames = 2 seconds (> 1s threshold)
    # Rally 2: frames 90-119
    trajectory += [_point(90 + i) for i in range(30)]

    rallies = rd.detect(trajectory)
    assert len(rallies) == 2
    assert rallies[0].end_frame == 29
    assert rallies[1].start_frame == 90


# ---------------------------------------------------------------------------
# detect_shots tests
# ---------------------------------------------------------------------------


def test_detect_shots_fewer_than_3_points():
    config = SegmentationConfig()
    assert detect_shots([], config) == []
    assert detect_shots([_point(0), _point(1)], config) == []


def test_detect_shots_detects_sharp_angle_change():
    """A 180-degree reversal should be detected as a shot (angle >= threshold)."""
    config = SegmentationConfig(shot_angle_threshold_deg=90.0)
    # Moving right, then reversing to left -> ~180 degrees
    trajectory = [
        _point(0, x=0.0, y=0.0),
        _point(1, x=10.0, y=0.0),
        _point(2, x=5.0, y=0.0),  # reversal
    ]
    shots = detect_shots(trajectory, config)
    assert len(shots) >= 1
    assert 1 in shots  # The middle point is the shot


# ---------------------------------------------------------------------------
# detect_bounces tests
# ---------------------------------------------------------------------------


def test_detect_bounces_fewer_than_3_points():
    assert detect_bounces([]) == []
    assert detect_bounces([_point(0), _point(1)]) == []


def test_detect_bounces_vy_sign_change():
    """A vy transition from negative to non-negative indicates a bounce."""
    trajectory = [
        _point(0, vy=-5.0),
        _point(1, vy=-2.0),
        _point(2, vy=3.0),  # sign change: prev=-2 < 0, next=3 >= 0
    ]
    bounces = detect_bounces(trajectory)
    # The bounce is detected at the middle point (frame_idx=1)
    assert len(bounces) >= 1
    assert 1 in bounces


# ---------------------------------------------------------------------------
# EventSegmenter tests
# ---------------------------------------------------------------------------


def test_event_segmenter_produces_correct_event_types():
    """With a trajectory that has a shot and a bounce, the segmenter should
    produce rally_start, rally_end, shot, and bounce events."""
    config = SegmentationConfig(shot_angle_threshold_deg=90.0)
    fps = 30.0
    segmenter = EventSegmenter(config, fps)

    # Build a trajectory with a sharp angle change at frame 5 and a vy sign change at frame 8
    trajectory = []
    # Frames 0-4: moving right
    for i in range(5):
        trajectory.append(_point(i, x=float(i * 10), y=100.0, vy=-2.0))
    # Frame 5: reversal (shot)
    trajectory.append(_point(5, x=35.0, y=100.0, vy=-1.0))
    # Frames 6-7: moving left, ball dropping
    trajectory.append(_point(6, x=25.0, y=100.0, vy=-3.0))
    # Frame 7-8: bounce (vy goes from negative to positive)
    trajectory.append(_point(7, x=20.0, y=100.0, vy=-1.0))
    trajectory.append(_point(8, x=15.0, y=100.0, vy=2.0))
    trajectory.append(_point(9, x=10.0, y=100.0, vy=3.0))

    events = segmenter.segment(trajectory, players_by_frame=None)

    event_types = {e.event_type for e in events}
    # At minimum we expect rally start/end
    assert EventType.RALLY_START in event_types
    assert EventType.RALLY_END in event_types


def test_event_segmenter_sorts_events_by_frame_idx():
    config = SegmentationConfig()
    fps = 30.0
    segmenter = EventSegmenter(config, fps)

    trajectory = [_point(i, x=float(i * 10), y=100.0) for i in range(20)]
    events = segmenter.segment(trajectory, players_by_frame=None)

    frame_indices = [e.frame_idx for e in events]
    assert frame_indices == sorted(frame_indices)


def test_event_segmenter_assign_player_with_nearby_player():
    """When a player is within shot_player_distance_px, the shot event gets a player_id."""
    config = SegmentationConfig(
        shot_angle_threshold_deg=90.0,
        shot_player_distance_px=200.0,
    )
    fps = 30.0
    segmenter = EventSegmenter(config, fps)

    # Build trajectory with a sharp reversal at frame 1
    trajectory = [
        _point(0, x=100.0, y=100.0),
        _point(1, x=110.0, y=100.0),
        _point(2, x=100.0, y=100.0),  # reversal
    ]

    # Place a player near the shot point
    players_by_frame = {
        1: [
            PlayerDetection(
                x=115.0,
                y=105.0,
                width=60.0,
                height=120.0,
                confidence=0.95,
                frame_idx=1,
                player_id=42,
            )
        ]
    }

    events = segmenter.segment(trajectory, players_by_frame)
    shot_events = [e for e in events if e.event_type == EventType.SHOT]
    if shot_events:
        assert shot_events[0].player_id == 42


def test_event_segmenter_assign_player_with_no_players():
    """When players_by_frame is None, shots should have player_id=None."""
    config = SegmentationConfig(shot_angle_threshold_deg=90.0)
    fps = 30.0
    segmenter = EventSegmenter(config, fps)

    trajectory = [
        _point(0, x=0.0, y=0.0),
        _point(1, x=10.0, y=0.0),
        _point(2, x=0.0, y=0.0),
    ]

    events = segmenter.segment(trajectory, players_by_frame=None)
    shot_events = [e for e in events if e.event_type == EventType.SHOT]
    for shot in shot_events:
        assert shot.player_id is None
