from __future__ import annotations

import pytest

from src.core.config import PhysicsConfig, SegmentationConfig, TrackingConfig
from src.core.types import Detection, TrajectoryPoint
from src.tracking.kalman_tracker import KalmanTracker
from src.segmentation.event_segmenter import EventSegmenter
from src.segmentation.event_types import EventType
from src.analytics.aggregator import compute_match_stats
from src.analytics.match_stats import MatchStats
from src.physics.homography import Homography
from src.physics.speed_calculator import calculate_speed_kmh


# ---------------------------------------------------------------------------
# Full pipeline integration: Detection -> Tracker -> EventSegmenter -> Stats
# ---------------------------------------------------------------------------


def test_full_pipeline_data_flow():
    """End-to-end: create fake detections for 20 frames, track them through
    KalmanTracker, segment events, and compute match stats."""
    tracking_config = TrackingConfig()
    tracker = KalmanTracker(tracking_config)

    # Generate 20 detections moving in a line with a direction reversal at frame 10
    # to trigger a shot event
    for i in range(20):
        if i < 10:
            x = 100.0 + i * 10.0
        else:
            x = 100.0 + (20 - i) * 10.0
        y = 200.0
        det = Detection(x=x, y=y, width=10.0, height=10.0, confidence=0.9, frame_idx=i)
        trajectory = tracker.update([det], frame_idx=i)

    # trajectory now has 20 points
    assert len(trajectory.points) == 20
    assert trajectory.track_id >= 1

    # Segment events
    seg_config = SegmentationConfig(shot_angle_threshold_deg=45.0)
    fps = 30.0
    segmenter = EventSegmenter(seg_config, fps)
    events = segmenter.segment(trajectory.points, players_by_frame=None)

    # Must have at least rally start and rally end
    event_types = {e.event_type for e in events}
    assert EventType.RALLY_START in event_types
    assert EventType.RALLY_END in event_types

    # Events must be sorted by frame_idx
    frame_indices = [e.frame_idx for e in events]
    assert frame_indices == sorted(frame_indices)

    # Compute match stats
    stats = compute_match_stats(events)

    assert isinstance(stats, MatchStats)
    assert stats.total_rallies >= 1
    assert isinstance(stats.speed_histogram, list)
    assert isinstance(stats.rallies, list)
    assert isinstance(stats.shots, list)


# ---------------------------------------------------------------------------
# Homography -> SpeedCalculator integration
# ---------------------------------------------------------------------------


def test_homography_speed_calculator_integration():
    """Calibrate a Homography, then use calculate_speed_kmh to compute speed."""
    config = PhysicsConfig()
    hom = Homography(config)
    corners = [(100.0, 100.0), (500.0, 100.0), (500.0, 300.0), (100.0, 300.0)]
    hom.calibrate(corners)

    p1 = TrajectoryPoint(
        x=100.0,
        y=100.0,
        vx=0.0,
        vy=0.0,
        frame_idx=0,
        is_detected=True,
        confidence=0.9,
    )
    p2 = TrajectoryPoint(
        x=300.0,
        y=100.0,
        vx=0.0,
        vy=0.0,
        frame_idx=1,
        is_detected=True,
        confidence=0.9,
    )

    speed = calculate_speed_kmh(hom, p1, p2, fps=30.0)

    # The speed should be a positive float representing km/h
    assert speed > 0.0
    assert isinstance(speed, float)

    # Verify that a stationary ball yields 0 speed
    speed_zero = calculate_speed_kmh(hom, p1, p1, fps=30.0)
    assert speed_zero == pytest.approx(0.0, abs=0.01)
