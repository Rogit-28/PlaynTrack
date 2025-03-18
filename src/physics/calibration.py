from __future__ import annotations

from typing import List, Optional, Tuple

import cv2
import numpy as np

from src.physics.table_detector import detect_table_corners


# Known table dimensions in meters (ITTF regulation)
TABLE_LENGTH_M = 2.74
TABLE_WIDTH_M = 1.525


def get_reference_points() -> List[Tuple[float, float]]:
    """Return the four reference points of a regulation table in world coordinates (meters).

    Order: top-left, top-right, bottom-right, bottom-left.
    Origin is at the top-left corner of the table.
    """
    return [
        (0.0, 0.0),
        (TABLE_LENGTH_M, 0.0),
        (TABLE_LENGTH_M, TABLE_WIDTH_M),
        (0.0, TABLE_WIDTH_M),
    ]


def calibrate_from_frame(frame: np.ndarray) -> Optional[np.ndarray]:
    """Attempt automatic calibration by detecting the table in *frame*.

    Returns the 3x3 homography matrix or ``None`` if the table cannot be detected.
    """
    corners = detect_table_corners(frame)
    if corners is None or len(corners) < 4:
        return None
    return compute_homography(corners)


def compute_homography(
    pixel_corners: List[Tuple[int, int]],
    world_corners: Optional[List[Tuple[float, float]]] = None,
) -> Optional[np.ndarray]:
    """Compute a homography matrix from pixel corners to world coordinates.

    Parameters
    ----------
    pixel_corners:
        Four pixel-coordinate points of the table
        (top-left, top-right, bottom-right, bottom-left).
    world_corners:
        Corresponding real-world coordinates (meters). Defaults to regulation
        table dimensions if not provided.
    """
    if world_corners is None:
        world_corners = get_reference_points()

    src = np.array(pixel_corners, dtype=np.float32)
    dst = np.array(world_corners, dtype=np.float32)
    H, status = cv2.findHomography(src, dst)
    if H is None:
        return None
    return H


def pixel_to_world(H: np.ndarray, x: float, y: float) -> Tuple[float, float]:
    """Transform a single pixel coordinate to world coordinates using *H*."""
    pt = np.array([x, y, 1.0], dtype=np.float64)
    world = H @ pt
    world /= world[2]
    return (float(world[0]), float(world[1]))
