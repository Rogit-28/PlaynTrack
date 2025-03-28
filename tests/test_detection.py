from __future__ import annotations

from pathlib import Path
from typing import List
from unittest.mock import MagicMock, patch

import numpy as np
import pytest

from src.core.config import DetectionConfig
from src.core.types import Detection, PlayerDetection
from src.detection.detector_base import DetectorBase
from src.detection.ball_detector import BallDetector
from src.detection.player_detector import PlayerDetector
from src.tracking.association import select_best_detection


# ---------------------------------------------------------------------------
# DetectorBase tests
# ---------------------------------------------------------------------------


def test_detector_base_is_abstract():
    """DetectorBase cannot be instantiated because detect() is abstract."""
    with pytest.raises(TypeError):
        DetectorBase()


class _ConcreteDetector(DetectorBase):
    """Minimal concrete subclass used only for testing the batch delegate."""

    def __init__(self):
        self.call_count = 0

    def detect(self, frame: np.ndarray) -> List[Detection]:
        self.call_count += 1
        return [
            Detection(x=1.0, y=2.0, width=3.0, height=4.0, confidence=0.8, frame_idx=0)
        ]


def test_detector_base_detect_batch_delegates_to_detect():
    """detect_batch should call detect once per frame and collect the results."""
    detector = _ConcreteDetector()
    frames = [np.zeros((10, 10, 3), dtype=np.uint8) for _ in range(3)]
    results = detector.detect_batch(frames)

    assert len(results) == 3
    assert detector.call_count == 3
    for batch in results:
        assert len(batch) == 1
        assert batch[0].confidence == 0.8


# ---------------------------------------------------------------------------
# BallDetector tests
# ---------------------------------------------------------------------------


def test_ball_detector_init_stores_config_and_model_path():
    config = DetectionConfig()
    detector = BallDetector(model_path=Path("models/ball.pt"), config=config)

    assert detector.model_path == Path("models/ball.pt")
    assert detector.config is config
    assert detector._model is None


def _make_mock_yolo_result(boxes_data):
    """Build a mock YOLO result object with the given (x1, y1, x2, y2, conf) tuples."""
    mock_result = MagicMock()
    mock_boxes = []
    for x1, y1, x2, y2, conf in boxes_data:
        box = MagicMock()
        box.xyxy = [np.array([x1, y1, x2, y2])]
        box.conf = [conf]
        box.cls = np.array([0])
        mock_boxes.append(box)

    # Use a MagicMock for boxes so it supports both iteration and .cls attribute
    boxes_mock = MagicMock()
    boxes_mock.__iter__ = MagicMock(return_value=iter(mock_boxes))
    boxes_mock.cls = np.array([0] * len(boxes_data))
    mock_result.boxes = boxes_mock
    return mock_result


@patch("src.detection.ball_detector.YOLO", create=True)
def test_ball_detector_detect_with_mocked_yolo(mock_yolo_cls, dummy_frame):
    """BallDetector.detect should parse YOLO results into Detection objects."""
    mock_model = MagicMock()
    mock_yolo_cls.return_value = mock_model

    result_obj = _make_mock_yolo_result([(10, 20, 30, 40, 0.95)])
    mock_model.predict.return_value = [result_obj]

    config = DetectionConfig()
    detector = BallDetector(model_path=None, config=config)
    # Manually inject the mock model so load() is bypassed
    detector._model = mock_model

    detections = detector.detect(dummy_frame)

    assert len(detections) == 1
    det = detections[0]
    assert det.x == pytest.approx(20.0)  # (10+30)/2
    assert det.y == pytest.approx(30.0)  # (20+40)/2
    assert det.width == pytest.approx(20.0)  # 30-10
    assert det.height == pytest.approx(20.0)  # 40-20
    assert det.confidence == pytest.approx(0.95)
    assert det.frame_idx == -1


# ---------------------------------------------------------------------------
# PlayerDetector tests
# ---------------------------------------------------------------------------


@patch("src.detection.player_detector.YOLO", create=True)
def test_player_detector_detect_with_mocked_yolo(mock_yolo_cls, dummy_frame):
    """PlayerDetector.detect should parse YOLO results into PlayerDetection objects,
    filtering to class 0 (person)."""
    mock_model = MagicMock()
    mock_yolo_cls.return_value = mock_model

    # Simulate two boxes: one person (cls=0) and one non-person (cls=1)
    mock_result = MagicMock()
    box_person = MagicMock()
    box_person.xyxy = [np.array([50, 100, 110, 340])]
    box_person.conf = [0.92]

    box_other = MagicMock()
    box_other.xyxy = [np.array([200, 200, 220, 220])]
    box_other.conf = [0.80]

    # Use a MagicMock for boxes so it supports both iteration and .cls attribute
    boxes_mock = MagicMock()
    boxes_mock.__iter__ = MagicMock(return_value=iter([box_person, box_other]))
    boxes_mock.cls = np.array([0, 1])
    mock_result.boxes = boxes_mock
    mock_model.predict.return_value = [mock_result]

    config = DetectionConfig()
    detector = PlayerDetector(model_path=None, config=config)
    detector._model = mock_model

    detections = detector.detect(dummy_frame)

    # Only the person box should be included
    assert len(detections) == 1
    assert detections[0].x == pytest.approx(80.0)  # (50+110)/2
    assert detections[0].confidence == pytest.approx(0.92)


# ---------------------------------------------------------------------------
# select_best_detection tests
# ---------------------------------------------------------------------------


def test_select_best_detection_returns_highest_confidence(sample_detections):
    best = select_best_detection(sample_detections)
    assert best is not None
    assert best.confidence == 0.9


def test_select_best_detection_returns_none_for_empty():
    assert select_best_detection([]) is None
