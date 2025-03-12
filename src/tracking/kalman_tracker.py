from __future__ import annotations

from dataclasses import dataclass
from typing import List

import numpy as np
from filterpy.kalman import KalmanFilter

from src.core.config import TrackingConfig
from src.core.types import Detection, TrajectoryPoint
from src.tracking.trajectory import Trajectory


@dataclass
class TrackState:
    track_id: int
    tracker: KalmanFilter
    missed_frames: int
    trajectory: Trajectory


class KalmanTracker:
    def __init__(self, config: TrackingConfig) -> None:
        self.config = config
        self._next_id = 1
        self._state: TrackState | None = None

    def _init_filter(self, x: float, y: float) -> KalmanFilter:
        kf = KalmanFilter(dim_x=4, dim_z=2)
        kf.x = np.array([x, y, 0.0, 0.0])
        kf.F = np.array(
            [
                [1, 0, 1, 0],
                [0, 1, 0, 1],
                [0, 0, 1, 0],
                [0, 0, 0, 1],
            ]
        )
        kf.H = np.array(
            [
                [1, 0, 0, 0],
                [0, 1, 0, 0],
            ]
        )
        kf.P *= 10.0
        kf.R *= 0.1
        kf.Q *= 0.01
        return kf

    def update(self, detections: List[Detection], frame_idx: int) -> Trajectory:
        if not detections:
            if self._state is None:
                return Trajectory(track_id=0)
            self._state.missed_frames += 1
            self._state.tracker.predict()
            if self._state.missed_frames > self.config.max_missed_frames:
                self._state = None
                return Trajectory(track_id=0)
            point = self._create_point(frame_idx, detected=False)
            self._state.trajectory.add_point(point)
            return self._state.trajectory

        detection = max(detections, key=lambda det: det.confidence)
        if self._state is None:
            tracker = self._init_filter(detection.x, detection.y)
            trajectory = Trajectory(track_id=self._next_id)
            self._next_id += 1
            self._state = TrackState(
                track_id=trajectory.track_id,
                tracker=tracker,
                missed_frames=0,
                trajectory=trajectory,
            )
        else:
            self._state.tracker.predict()
            self._state.missed_frames = 0

        self._state.tracker.update(np.array([detection.x, detection.y]))
        point = self._create_point(frame_idx, detected=True, confidence=detection.confidence)
        self._state.trajectory.add_point(point)
        return self._state.trajectory

    def _create_point(
        self,
        frame_idx: int,
        detected: bool,
        confidence: float = 0.0,
    ) -> TrajectoryPoint:
        x, y, vx, vy = self._state.tracker.x
        return TrajectoryPoint(
            x=float(x),
            y=float(y),
            vx=float(vx),
            vy=float(vy),
            frame_idx=frame_idx,
            is_detected=detected,
            confidence=confidence,
            speed_kmh=None,
        )
