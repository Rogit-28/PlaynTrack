from __future__ import annotations

import pytest

from src.core.config import TrackingConfig
from src.core.types import Detection, TrajectoryPoint
from src.tracking.trajectory import Trajectory
from src.tracking.kalman_tracker import KalmanTracker


# ---------------------------------------------------------------------------
# Trajectory tests
# ---------------------------------------------------------------------------


def _make_point(frame_idx: int = 0, x: float = 0.0, y: float = 0.0) -> TrajectoryPoint:
    return TrajectoryPoint(
        x=x,
        y=y,
        vx=0.0,
        vy=0.0,
        frame_idx=frame_idx,
        is_detected=True,
        confidence=0.9,
    )


def test_trajectory_creation():
    traj = Trajectory(track_id=1)
    assert traj.track_id == 1
    assert len(traj.points) == 0


def test_trajectory_add_point():
    traj = Trajectory(track_id=1)
    point = _make_point(frame_idx=0, x=10.0, y=20.0)
    traj.add_point(point)

    assert len(traj.points) == 1
    assert traj.points[0].x == 10.0


def test_trajectory_latest_returns_last_point():
    traj = Trajectory(track_id=1)
    traj.add_point(_make_point(frame_idx=0, x=1.0))
    traj.add_point(_make_point(frame_idx=1, x=2.0))
    traj.add_point(_make_point(frame_idx=2, x=3.0))

    latest = traj.latest()
    assert latest is not None
    assert latest.frame_idx == 2
    assert latest.x == 3.0


def test_trajectory_latest_returns_none_when_empty():
    traj = Trajectory(track_id=1)
    assert traj.latest() is None


# ---------------------------------------------------------------------------
# KalmanTracker tests
# ---------------------------------------------------------------------------


def _make_detection(
    x: float, y: float, confidence: float = 0.9, frame_idx: int = 0
) -> Detection:
    return Detection(
        x=x, y=y, width=10.0, height=10.0, confidence=confidence, frame_idx=frame_idx
    )


def test_kalman_tracker_init_default_config():
    config = TrackingConfig()
    tracker = KalmanTracker(config)

    assert tracker.config is config
    assert tracker._state is None
    assert tracker._next_id == 1


def test_kalman_tracker_update_with_detections_creates_track():
    config = TrackingConfig()
    tracker = KalmanTracker(config)

    detections = [_make_detection(x=100.0, y=200.0)]
    traj = tracker.update(detections, frame_idx=0)

    assert traj.track_id == 1
    assert len(traj.points) == 1
    assert traj.points[0].is_detected is True


def test_kalman_tracker_update_no_detections_returns_empty():
    """With no prior state and no detections, return empty trajectory with track_id=0."""
    config = TrackingConfig()
    tracker = KalmanTracker(config)

    traj = tracker.update([], frame_idx=0)

    assert traj.track_id == 0
    assert len(traj.points) == 0


def test_kalman_tracker_update_sequence_grows_trajectory():
    """Feed 5 detections sequentially; the trajectory should contain 5 points."""
    config = TrackingConfig()
    tracker = KalmanTracker(config)

    for i in range(5):
        detections = [_make_detection(x=100.0 + i * 5, y=200.0 - i * 2)]
        traj = tracker.update(detections, frame_idx=i)

    assert len(traj.points) == 5
    assert traj.track_id == 1


def test_kalman_tracker_missed_frame_increments():
    """After a detection, an empty update should increment missed_frames."""
    config = TrackingConfig()
    tracker = KalmanTracker(config)

    # Start tracking
    tracker.update([_make_detection(x=100.0, y=200.0)], frame_idx=0)
    assert tracker._state is not None
    assert tracker._state.missed_frames == 0

    # Miss a frame
    tracker.update([], frame_idx=1)
    assert tracker._state is not None
    assert tracker._state.missed_frames == 1


def test_kalman_tracker_track_loss_after_max_missed():
    """After max_missed_frames+1 empty calls, the track should be reset (state=None)."""
    config = TrackingConfig(max_missed_frames=3)
    tracker = KalmanTracker(config)

    # Start tracking
    tracker.update([_make_detection(x=100.0, y=200.0)], frame_idx=0)

    # Miss max_missed_frames frames (still within budget)
    for i in range(1, config.max_missed_frames + 1):
        traj = tracker.update([], frame_idx=i)
        assert tracker._state is not None  # still alive

    # One more miss goes over the limit
    traj = tracker.update([], frame_idx=config.max_missed_frames + 1)
    assert tracker._state is None
    assert traj.track_id == 0
