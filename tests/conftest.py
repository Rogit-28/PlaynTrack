from __future__ import annotations

import pytest
import numpy as np

from src.core.types import Detection, PlayerDetection, TrajectoryPoint, Event
from src.core.config import (
    AppConfig,
    DetectionConfig,
    TrackingConfig,
    PhysicsConfig,
    SegmentationConfig,
    VisualizationConfig,
)


@pytest.fixture
def dummy_frame():
    """720p BGR frame filled with gray."""
    return np.full((720, 1280, 3), 128, dtype=np.uint8)


@pytest.fixture
def app_config():
    return AppConfig()


@pytest.fixture
def sample_detections():
    return [
        Detection(
            x=100.0, y=200.0, width=10.0, height=10.0, confidence=0.9, frame_idx=0
        ),
        Detection(
            x=105.0, y=195.0, width=10.0, height=10.0, confidence=0.7, frame_idx=1
        ),
        Detection(
            x=110.0, y=190.0, width=10.0, height=10.0, confidence=0.85, frame_idx=2
        ),
    ]


@pytest.fixture
def sample_trajectory():
    """10-point trajectory with varying velocities for testing."""
    points = []
    for i in range(10):
        points.append(
            TrajectoryPoint(
                x=100.0 + i * 10,
                y=200.0 - i * 5,
                vx=10.0,
                vy=-5.0,
                frame_idx=i,
                is_detected=True,
                confidence=0.9,
                speed_kmh=float(30 + i * 2),
            )
        )
    return points


@pytest.fixture
def sample_player_detections():
    return {
        0: [
            PlayerDetection(
                x=50.0,
                y=400.0,
                width=60.0,
                height=120.0,
                confidence=0.95,
                frame_idx=0,
                player_id=1,
            )
        ],
        1: [
            PlayerDetection(
                x=52.0,
                y=398.0,
                width=60.0,
                height=120.0,
                confidence=0.93,
                frame_idx=1,
                player_id=1,
            )
        ],
    }
