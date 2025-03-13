from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Optional


class EventType(str, Enum):
    RALLY_START = "rally_start"
    RALLY_END = "rally_end"
    SHOT = "shot"
    BOUNCE = "bounce"


@dataclass
class Event:
    event_type: EventType
    frame_idx: int
    timestamp: float
    position: tuple[float, float]
    speed: Optional[float] = None
    player_id: Optional[int] = None
    metadata: Optional[dict] = None
