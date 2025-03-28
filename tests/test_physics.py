from __future__ import annotations

import numpy as np
import pytest

from src.core.config import PhysicsConfig
from src.core.types import TrajectoryPoint
from src.physics.homography import Homography
from src.physics.speed_calculator import calculate_speed_kmh
from src.physics.calibration import (
    get_reference_points,
    compute_homography,
    pixel_to_world,
)
from src.physics.table_detector import (
    _line_intersection,
    _cluster_lines,
    _order_corners,
)


# ---------------------------------------------------------------------------
# Homography class tests
# ---------------------------------------------------------------------------

# Four pixel corners forming a simple rectangle used throughout these tests.
_TABLE_CORNERS = [(100.0, 100.0), (500.0, 100.0), (500.0, 300.0), (100.0, 300.0)]


def test_homography_init_stores_config():
    config = PhysicsConfig()
    hom = Homography(config)

    assert hom.config is config
    assert hom.matrix is None


def test_homography_calibrate_with_4_corners():
    config = PhysicsConfig()
    hom = Homography(config)
    hom.calibrate(_TABLE_CORNERS)

    assert hom.matrix is not None
    assert hom.matrix.shape == (3, 3)


def test_homography_calibrate_raises_with_wrong_corner_count():
    config = PhysicsConfig()
    hom = Homography(config)

    with pytest.raises(ValueError, match="Expected 4 table corners"):
        hom.calibrate([(0, 0), (1, 1)])


def test_homography_pixel_to_world_raises_when_not_calibrated():
    config = PhysicsConfig()
    hom = Homography(config)

    with pytest.raises(ValueError, match="not calibrated"):
        hom.pixel_to_world((100.0, 100.0))


def test_homography_pixel_to_world_returns_floats():
    config = PhysicsConfig()
    hom = Homography(config)
    hom.calibrate(_TABLE_CORNERS)

    result = hom.pixel_to_world((300.0, 200.0))

    assert isinstance(result, tuple)
    assert len(result) == 2
    assert isinstance(result[0], float)
    assert isinstance(result[1], float)


# ---------------------------------------------------------------------------
# calculate_speed_kmh tests
# ---------------------------------------------------------------------------


def _make_traj_point(x: float, y: float, frame_idx: int = 0) -> TrajectoryPoint:
    return TrajectoryPoint(
        x=x,
        y=y,
        vx=0.0,
        vy=0.0,
        frame_idx=frame_idx,
        is_detected=True,
        confidence=0.9,
    )


def test_calculate_speed_kmh_with_known_homography():
    """Calibrate with known corners, then compute speed between two points.
    The top-left corner maps to (0, 0) world, top-right to (2.74, 0)."""
    config = PhysicsConfig()
    hom = Homography(config)
    hom.calibrate(_TABLE_CORNERS)

    # Points at opposite ends of the table top edge (pixel y=100)
    p1 = _make_traj_point(x=100.0, y=100.0, frame_idx=0)
    p2 = _make_traj_point(x=500.0, y=100.0, frame_idx=1)

    speed = calculate_speed_kmh(hom, p1, p2, fps=30.0)
    # Distance should be ~2.74 m (table length), speed = 2.74 * 30 * 3.6 = ~295.92 km/h
    assert speed > 0.0
    assert speed == pytest.approx(2.74 * 30.0 * 3.6, rel=0.01)


def test_calculate_speed_kmh_returns_zero_when_fps_zero():
    config = PhysicsConfig()
    hom = Homography(config)
    hom.calibrate(_TABLE_CORNERS)

    p1 = _make_traj_point(x=100.0, y=100.0)
    p2 = _make_traj_point(x=200.0, y=100.0)

    assert calculate_speed_kmh(hom, p1, p2, fps=0) == 0.0


# ---------------------------------------------------------------------------
# calibration module tests
# ---------------------------------------------------------------------------


def test_get_reference_points_returns_4():
    pts = get_reference_points()
    assert len(pts) == 4
    for pt in pts:
        assert len(pt) == 2
        assert isinstance(pt[0], float)
        assert isinstance(pt[1], float)


def test_compute_homography_returns_3x3():
    pixel_corners = [(100, 100), (500, 100), (500, 300), (100, 300)]
    H = compute_homography(pixel_corners)
    assert H is not None
    assert H.shape == (3, 3)


def test_pixel_to_world_from_calibration():
    pixel_corners = [(100, 100), (500, 100), (500, 300), (100, 300)]
    H = compute_homography(pixel_corners)
    assert H is not None

    wx, wy = pixel_to_world(H, 100.0, 100.0)
    # Top-left pixel corner should map to world origin (0, 0)
    assert wx == pytest.approx(0.0, abs=0.01)
    assert wy == pytest.approx(0.0, abs=0.01)


# ---------------------------------------------------------------------------
# table_detector helper tests
# ---------------------------------------------------------------------------


def test_line_intersection_known_lines():
    """Two lines that cross at a known point."""
    # Line 1: from (0,0) to (10,10), Line 2: from (10,0) to (0,10)
    # Intersection at (5, 5)
    result = _line_intersection((0.0, 0.0), (10.0, 10.0), (10.0, 0.0), (0.0, 10.0))
    assert result is not None
    assert result[0] == pytest.approx(5.0)
    assert result[1] == pytest.approx(5.0)


def test_line_intersection_parallel_returns_none():
    """Two parallel horizontal lines should return None."""
    result = _line_intersection((0.0, 0.0), (10.0, 0.0), (0.0, 5.0), (10.0, 5.0))
    assert result is None


def test_cluster_lines_separates_horizontal_and_vertical():
    """Create lines with known angles and verify clustering."""
    # Horizontal line (angle ~ 0)
    h_line = np.array([[0, 100, 200, 100]])
    # Vertical line (angle ~ 90)
    v_line = np.array([[100, 0, 100, 200]])

    lines = np.array([h_line[0], v_line[0]]).reshape(-1, 1, 4)
    horizontal, vertical = _cluster_lines(lines)

    assert len(horizontal) >= 1
    assert len(vertical) >= 1


def test_order_corners_produces_correct_ordering():
    """Given four unordered corners, _order_corners should produce TL, TR, BR, BL."""
    # Shuffle corners intentionally
    corners = [(500.0, 300.0), (100.0, 100.0), (500.0, 100.0), (100.0, 300.0)]
    ordered = _order_corners(corners)

    assert len(ordered) == 4
    # Top-left should have smallest x+y sum
    tl = ordered[0]
    sums = [p[0] + p[1] for p in ordered]
    assert (tl[0] + tl[1]) == min(sums)
