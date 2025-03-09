from __future__ import annotations

from typing import List

from src.core.types import Detection


def select_best_detection(detections: List[Detection]) -> Detection | None:
    if not detections:
        return None
    return max(detections, key=lambda det: det.confidence)
