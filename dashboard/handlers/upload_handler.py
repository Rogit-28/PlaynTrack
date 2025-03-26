from __future__ import annotations

from pathlib import Path
from typing import Optional

from src.core.config import AppConfig, load_config
from src.utils.video_utils import probe_video


def validate_upload(video_path: Path, config: Optional[AppConfig] = None) -> dict:
    """Validate an uploaded video file and return metadata.

    Returns a dict with ``valid`` (bool), ``metadata`` (dict), and ``error``
    (str or None).
    """
    if config is None:
        config = load_config(None)

    if not video_path.exists():
        return {"valid": False, "metadata": {}, "error": "File not found"}

    suffix = video_path.suffix.lower()
    if suffix not in {".mp4", ".avi", ".mov", ".mkv"}:
        return {
            "valid": False,
            "metadata": {},
            "error": f"Unsupported format: {suffix}",
        }

    metadata = probe_video(video_path)
    if not metadata:
        return {"valid": False, "metadata": {}, "error": "Unable to read video"}

    fps = metadata.get("fps", 0)
    if fps < config.video.min_fps:
        return {
            "valid": False,
            "metadata": metadata,
            "error": f"FPS too low ({fps:.1f}). Minimum is {config.video.min_fps}.",
        }

    width = metadata.get("width", 0)
    height = metadata.get("height", 0)
    max_w, max_h = config.video.max_resolution
    if width > max_w or height > max_h:
        return {
            "valid": False,
            "metadata": metadata,
            "error": f"Resolution {width}x{height} exceeds max {max_w}x{max_h}",
        }

    return {"valid": True, "metadata": metadata, "error": None}
