from __future__ import annotations

import logging
from pathlib import Path
from typing import List

import numpy as np

from src.core.config import DetectionConfig
from src.core.types import PlayerDetection
from src.detection.detector_base import DetectorBase

logger = logging.getLogger(__name__)

FALLBACK_MODEL = "yolov8n.pt"


class PlayerDetector(DetectorBase):
    def __init__(self, model_path: Path | None, config: DetectionConfig) -> None:
        self.model_path = Path(model_path) if model_path else None
        self.config = config
        self._model = None

    def load(self) -> None:
        if self._model is not None:
            return
        from ultralytics import YOLO

        # Check if custom model exists, otherwise use fallback
        if self.model_path and self.model_path.exists():
            logger.info(f"Loading custom player detection model from {self.model_path}")
            self._model = YOLO(str(self.model_path))
        else:
            if self.model_path:
                logger.warning(
                    f"Custom player model not found at {self.model_path}, "
                    f"using {FALLBACK_MODEL} fallback"
                )
            else:
                logger.info(f"No custom player model specified, using {FALLBACK_MODEL} fallback")
            self._model = YOLO(FALLBACK_MODEL)  # Auto-downloads from Ultralytics

    def detect(self, frame: np.ndarray) -> List[PlayerDetection]:
        if self._model is None:
            self.load()

        results = self._model.predict(
            frame,
            conf=self.config.confidence_threshold,
            iou=self.config.nms_threshold,
            max_det=self.config.max_detections,
            verbose=False,
        )
        detections: List[PlayerDetection] = []
        for result in results:
            for box, cls in zip(result.boxes, result.boxes.cls):
                if int(cls) != 0:
                    continue
                x1, y1, x2, y2 = box.xyxy[0].tolist()
                confidence = float(box.conf[0])
                detections.append(
                    PlayerDetection(
                        x=(x1 + x2) / 2,
                        y=(y1 + y2) / 2,
                        width=x2 - x1,
                        height=y2 - y1,
                        confidence=confidence,
                        frame_idx=-1,
                    )
                )
        return detections
