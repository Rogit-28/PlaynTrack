from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List, Optional

from src.analytics.aggregator import compute_match_stats
from src.analytics.match_stats import MatchStats
from src.core.config import AppConfig
from src.core.types import Detection, PlayerDetection, TrajectoryPoint
from src.detection.ball_detector import BallDetector
from src.detection.player_detector import PlayerDetector
from src.input.video_loader import VideoLoader
from src.physics.homography import Homography
from src.physics.speed_calculator import calculate_speed_kmh
from src.physics.table_detector import detect_table_corners
from src.segmentation.event_segmenter import EventSegmenter
from src.segmentation.event_types import Event, EventType
from src.tracking.kalman_tracker import KalmanTracker


@dataclass
class PipelineResult:
    detections: Dict[int, List[Detection]]
    trajectory: List[TrajectoryPoint]
    events: List[Event]
    match_stats: Optional[MatchStats]
    fps: float
    player_detections: Dict[int, List[PlayerDetection]]


class VideoProcessor:
    def __init__(self, config: AppConfig) -> None:
        self.config = config
        self.detector = BallDetector(config.detection.ball_model_path, config.detection)
        self.player_detector = PlayerDetector(config.detection.player_model_path, config.detection)
        self.tracker = KalmanTracker(config.tracking)

    def run(self, video_path: Path) -> PipelineResult:
        loader = VideoLoader(video_path)
        metadata = loader.metadata()
        fps = metadata.fps
        detections: Dict[int, List[Detection]] = {}
        trajectory_points: List[TrajectoryPoint] = []
        player_detections: Dict[int, List[PlayerDetection]] = {}
        homography = Homography(self.config.physics)
        homography_ready = False

        for frame_idx, frame in loader.read_frames():
            if self.config.physics.enable_table_detection and not homography_ready:
                corners = detect_table_corners(frame)
                if corners:
                    homography.calibrate(corners)
                    homography_ready = True

            frame_detections = self.detector.detect(frame)
            for detection in frame_detections:
                detection.frame_idx = frame_idx
            detections[frame_idx] = frame_detections

            frame_players = self.player_detector.detect(frame)
            for player in frame_players:
                player.frame_idx = frame_idx
            player_detections[frame_idx] = frame_players

            trajectory = self.tracker.update(frame_detections, frame_idx)
            if trajectory.points:
                trajectory_points.append(trajectory.points[-1])

        events: List[Event] = []
        match_stats: Optional[MatchStats] = None
        if trajectory_points:
            segmenter = EventSegmenter(self.config.segmentation, fps)
            events = segmenter.segment(trajectory_points, player_detections)
            if homography_ready:
                events = self._attach_speeds(events, trajectory_points, homography, fps)
                self._attach_point_speeds(trajectory_points, homography, fps)
            match_stats = compute_match_stats(events)

        return PipelineResult(
            detections=detections,
            trajectory=trajectory_points,
            events=events,
            match_stats=match_stats,
            fps=fps,
            player_detections=player_detections,
        )

    def _attach_speeds(
        self,
        events: List[Event],
        trajectory_points: List[TrajectoryPoint],
        homography: Homography,
        fps: float,
    ) -> List[Event]:
        trajectory_map = {point.frame_idx: point for point in trajectory_points}
        updated: List[Event] = []
        for event in events:
            if event.event_type == EventType.SHOT:
                point = trajectory_map.get(event.frame_idx)
                prev_point = trajectory_map.get(event.frame_idx - 1)
                if point and prev_point:
                    event.speed = calculate_speed_kmh(homography, prev_point, point, fps)
            updated.append(event)
        return updated

    def _attach_point_speeds(
        self,
        trajectory_points: List[TrajectoryPoint],
        homography: Homography,
        fps: float,
    ) -> None:
        for prev_point, point in zip(trajectory_points, trajectory_points[1:]):
            point.speed_kmh = calculate_speed_kmh(homography, prev_point, point, fps)
