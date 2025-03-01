from __future__ import annotations

from pathlib import Path
from typing import Optional

from pydantic import BaseModel, Field


class VideoConfig(BaseModel):
    min_fps: int = Field(24, ge=1, description="Minimum supported FPS")
    max_fps: int = Field(120, ge=1, description="Maximum supported FPS")
    max_resolution: tuple[int, int] = Field((1920, 1080), description="Max resolution (W,H)")
    export_fps: Optional[int] = Field(None, description="Override export FPS")
    batch_size: int = Field(8, ge=1, description="Batch size for inference")


class DetectionConfig(BaseModel):
    ball_model_path: Optional[Path] = Field(Path("models/ball_detector.pt"))
    player_model_path: Optional[Path] = Field(Path("models/player_detector.pt"))
    confidence_threshold: float = Field(0.3, ge=0.0, le=1.0)
    nms_threshold: float = Field(0.5, ge=0.0, le=1.0)
    max_detections: int = Field(5, ge=1)


class TrackingConfig(BaseModel):
    max_missed_frames: int = Field(10, ge=0)
    smoothing_window: int = Field(5, ge=1)


class PhysicsConfig(BaseModel):
    table_length_m: float = Field(2.74, gt=0)
    table_width_m: float = Field(1.525, gt=0)
    enable_table_detection: bool = Field(True)


class SegmentationConfig(BaseModel):
    rally_gap_seconds: float = Field(2.0, ge=0.0)
    min_shots_per_rally: int = Field(2, ge=1)
    shot_angle_threshold_deg: float = Field(90.0, ge=0.0)
    shot_player_distance_px: float = Field(120.0, ge=0.0)


class VisualizationConfig(BaseModel):
    trail_length: int = Field(15, ge=1)
    speed_color_low: tuple[int, int, int] = Field((0, 255, 0))
    speed_color_mid: tuple[int, int, int] = Field((0, 255, 255))
    speed_color_high: tuple[int, int, int] = Field((0, 0, 255))
    show_player_boxes: bool = Field(True)
    show_stats_panel: bool = Field(True)


class AppConfig(BaseModel):
    video: VideoConfig = Field(default_factory=VideoConfig)
    detection: DetectionConfig = Field(default_factory=DetectionConfig)
    tracking: TrackingConfig = Field(default_factory=TrackingConfig)
    physics: PhysicsConfig = Field(default_factory=PhysicsConfig)
    segmentation: SegmentationConfig = Field(default_factory=SegmentationConfig)
    visualization: VisualizationConfig = Field(default_factory=VisualizationConfig)


def load_config(path: Optional[Path] = None) -> AppConfig:
    if path is None:
        return AppConfig()

    import yaml

    config_path = Path(path)
    data = yaml.safe_load(config_path.read_text())
    return AppConfig(**(data or {}))
