from __future__ import annotations

from dataclasses import dataclass
from typing import Optional


@dataclass
class Detection:
    x: float
    y: float
    width: float
    height: float
    confidence: float
    frame_idx: int


@dataclass
class PlayerDetection:
    x: float
    y: float
    width: float
    height: float
    confidence: float
    frame_idx: int
    player_id: Optional[int] = None


@dataclass
class TrajectoryPoint:
    x: float
    y: float
    vx: float
    vy: float
    frame_idx: int
    is_detected: bool
    confidence: float
    speed_kmh: Optional[float] = None


@dataclass
class Event:
    event_type: str
    frame_idx: int
    timestamp: float
    position: tuple[float, float]
    speed: Optional[float] = None
    player_id: Optional[int] = None
    metadata: Optional[dict] = None
