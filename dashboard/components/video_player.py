from __future__ import annotations

from pathlib import Path
from typing import Optional


def get_video_component_config() -> dict:
    """Return default configuration for the Gradio video player component."""
    return {
        "label": "Annotated Video",
        "autoplay": False,
        "show_label": True,
        "interactive": False,
    }


def resolve_video_path(video_path: str | Path | None) -> Optional[str]:
    """Resolve a video path for the Gradio video component.

    Returns the string path if the file exists, otherwise None.
    """
    if video_path is None:
        return None
    path = Path(video_path)
    if path.exists():
        return str(path)
    return None
