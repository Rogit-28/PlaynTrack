from __future__ import annotations

from typing import List, Optional, Tuple

import cv2
import numpy as np


def _line_intersection(
    p1: Tuple[float, float],
    p2: Tuple[float, float],
    p3: Tuple[float, float],
    p4: Tuple[float, float],
) -> Optional[Tuple[float, float]]:
    """Compute intersection of two line segments (extended infinitely)."""
    x1, y1 = p1
    x2, y2 = p2
    x3, y3 = p3
    x4, y4 = p4

    denom = (x1 - x2) * (y3 - y4) - (y1 - y2) * (x3 - x4)
    if abs(denom) < 1e-8:
        return None

    t = ((x1 - x3) * (y3 - y4) - (y1 - y3) * (x3 - x4)) / denom
    ix = x1 + t * (x2 - x1)
    iy = y1 + t * (y2 - y1)
    return (ix, iy)


def _cluster_lines(
    lines: np.ndarray, angle_threshold: float = 15.0
) -> Tuple[List[np.ndarray], List[np.ndarray]]:
    """Separate detected lines into roughly horizontal and roughly vertical groups."""
    horizontal: List[np.ndarray] = []
    vertical: List[np.ndarray] = []

    for line in lines:
        x1, y1, x2, y2 = line[0]
        angle = abs(np.degrees(np.arctan2(y2 - y1, x2 - x1)))
        if angle < angle_threshold or angle > (180 - angle_threshold):
            horizontal.append(line[0])
        elif (90 - angle_threshold) < angle < (90 + angle_threshold):
            vertical.append(line[0])

    return horizontal, vertical


def _pick_extreme_lines(
    lines: List[np.ndarray], axis: int
) -> Optional[Tuple[np.ndarray, np.ndarray]]:
    """Pick the two most separated lines along the given axis (0=x, 1=y)."""
    if len(lines) < 2:
        return None

    midpoints = []
    for seg in lines:
        mid = (seg[axis] + seg[axis + 2]) / 2.0
        midpoints.append(mid)

    sorted_indices = np.argsort(midpoints)
    return lines[sorted_indices[0]], lines[sorted_indices[-1]]


def _order_corners(corners: List[Tuple[float, float]]) -> List[Tuple[int, int]]:
    """Order corners as top-left, top-right, bottom-right, bottom-left."""
    pts = np.array(corners, dtype=np.float32)
    centroid = pts.mean(axis=0)

    angles = np.arctan2(pts[:, 1] - centroid[1], pts[:, 0] - centroid[0])
    order = np.argsort(angles)
    ordered = pts[order]

    # Rearrange: top-left, top-right, bottom-right, bottom-left
    # After sorting by angle, we get a CCW or CW ordering
    # Find the top-left (smallest x+y sum) and rotate
    sums = ordered[:, 0] + ordered[:, 1]
    start = int(np.argmin(sums))
    ordered = np.roll(ordered, -start, axis=0)

    return [(int(round(p[0])), int(round(p[1]))) for p in ordered]


def detect_table_corners(frame: np.ndarray) -> Optional[List[Tuple[int, int]]]:
    """
    Detect the four corners of a table tennis table using edge and line detection.

    Returns 4 corner points ordered as [top-left, top-right, bottom-right, bottom-left],
    or None if detection fails.
    """
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)
    edges = cv2.Canny(blurred, 50, 150)

    lines = cv2.HoughLinesP(
        edges, 1, np.pi / 180, threshold=80, minLineLength=100, maxLineGap=15
    )
    if lines is None or len(lines) < 4:
        return None

    horizontal, vertical = _cluster_lines(lines)
    if len(horizontal) < 2 or len(vertical) < 2:
        return None

    h_pair = _pick_extreme_lines(horizontal, axis=1)
    v_pair = _pick_extreme_lines(vertical, axis=0)
    if h_pair is None or v_pair is None:
        return None

    h1, h2 = h_pair
    v1, v2 = v_pair

    h_lines = [
        ((int(h1[0]), int(h1[1])), (int(h1[2]), int(h1[3]))),
        ((int(h2[0]), int(h2[1])), (int(h2[2]), int(h2[3]))),
    ]
    v_lines = [
        ((int(v1[0]), int(v1[1])), (int(v1[2]), int(v1[3]))),
        ((int(v2[0]), int(v2[1])), (int(v2[2]), int(v2[3]))),
    ]

    corners: List[Tuple[float, float]] = []
    h, w = frame.shape[:2]
    for h_seg in h_lines:
        for v_seg in v_lines:
            pt = _line_intersection(h_seg[0], h_seg[1], v_seg[0], v_seg[1])
            if pt is not None and 0 <= pt[0] < w and 0 <= pt[1] < h:
                corners.append(pt)

    if len(corners) < 4:
        return None

    return _order_corners(corners[:4])
