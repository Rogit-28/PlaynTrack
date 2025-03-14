from __future__ import annotations

from typing import Dict, List

from src.core.config import SegmentationConfig
from src.core.types import PlayerDetection, TrajectoryPoint
from src.segmentation.event_types import Event, EventType
from src.segmentation.rally_detector import RallyDetector
from src.segmentation.shot_detector import detect_shots
from src.segmentation.bounce_detector import detect_bounces


class EventSegmenter:
    def __init__(self, config: SegmentationConfig, fps: float) -> None:
        self.config = config
        self.fps = fps

    def segment(
        self,
        trajectory: List[TrajectoryPoint],
        players_by_frame: Dict[int, List[PlayerDetection]] | None = None,
    ) -> List[Event]:
        rallies = RallyDetector(self.config, self.fps).detect(trajectory)
        shot_frames = set(detect_shots(trajectory, self.config))
        bounce_frames = set(detect_bounces(trajectory))

        events: List[Event] = []
        for rally in rallies:
            events.append(
                Event(
                    event_type=EventType.RALLY_START,
                    frame_idx=rally.start_frame,
                    timestamp=rally.start_frame / self.fps,
                    position=(0.0, 0.0),
                )
            )
            events.append(
                Event(
                    event_type=EventType.RALLY_END,
                    frame_idx=rally.end_frame,
                    timestamp=rally.end_frame / self.fps,
                    position=(0.0, 0.0),
                )
            )

        for point in trajectory:
            if point.frame_idx in shot_frames:
                player_id = self._assign_player(point, players_by_frame)
                events.append(
                    Event(
                        event_type=EventType.SHOT,
                        frame_idx=point.frame_idx,
                        timestamp=point.frame_idx / self.fps,
                        position=(point.x, point.y),
                        player_id=player_id,
                    )
                )
            if point.frame_idx in bounce_frames:
                events.append(
                    Event(
                        event_type=EventType.BOUNCE,
                        frame_idx=point.frame_idx,
                        timestamp=point.frame_idx / self.fps,
                        position=(point.x, point.y),
                    )
                )

        return sorted(events, key=lambda e: e.frame_idx)

    def _assign_player(
        self,
        point: TrajectoryPoint,
        players_by_frame: Dict[int, List[PlayerDetection]] | None,
    ) -> int | None:
        if not players_by_frame:
            return None
        candidates = players_by_frame.get(point.frame_idx, [])
        if not candidates:
            return None
        closest = None
        closest_dist = None
        for player in candidates:
            dx = point.x - player.x
            dy = point.y - player.y
            dist = (dx ** 2 + dy ** 2) ** 0.5
            if dist <= self.config.shot_player_distance_px:
                if closest_dist is None or dist < closest_dist:
                    closest_dist = dist
                    closest = player
        if closest and closest.player_id is not None:
            return closest.player_id
        return None
