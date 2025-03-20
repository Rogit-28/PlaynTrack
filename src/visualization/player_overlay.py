from __future__ import annotations

from typing import List

import cv2
import numpy as np

from src.core.types import PlayerDetection


def _draw_dashed_rect(
    frame: np.ndarray,
    pt1: tuple[int, int],
    pt2: tuple[int, int],
    color: tuple[int, int, int],
    thickness: int = 2,
    dash_length: int = 10,
) -> None:
    """Draw a dashed rectangle on *frame*."""
    x1, y1 = pt1
    x2, y2 = pt2

    edges = [
        ((x1, y1), (x2, y1)),  # top
        ((x2, y1), (x2, y2)),  # right
        ((x2, y2), (x1, y2)),  # bottom
        ((x1, y2), (x1, y1)),  # left
    ]

    for start, end in edges:
        dx = end[0] - start[0]
        dy = end[1] - start[1]
        length = max(int((dx**2 + dy**2) ** 0.5), 1)
        segments = length // dash_length

        for i in range(0, segments, 2):
            s = i / segments
            e = min((i + 1) / segments, 1.0)
            p1 = (int(start[0] + s * dx), int(start[1] + s * dy))
            p2 = (int(start[0] + e * dx), int(start[1] + e * dy))
            cv2.line(frame, p1, p2, color, thickness, cv2.LINE_AA)


def render_players(frame: np.ndarray, players: List[PlayerDetection]) -> np.ndarray:
    """Render player bounding boxes with dashed blue rectangles."""
    color = (255, 102, 0)  # BGR - blue-ish (#0066FF)
    for player in players:
        x1 = int(player.x - player.width / 2)
        y1 = int(player.y - player.height / 2)
        x2 = int(player.x + player.width / 2)
        y2 = int(player.y + player.height / 2)

        _draw_dashed_rect(frame, (x1, y1), (x2, y2), color, thickness=2, dash_length=10)

        label = (
            f"Player {player.player_id + 1}"
            if player.player_id is not None
            else "Player"
        )
        cv2.putText(
            frame,
            label,
            (x1, max(y1 - 5, 0)),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.5,
            color,
            2,
            cv2.LINE_AA,
        )
    return frame
