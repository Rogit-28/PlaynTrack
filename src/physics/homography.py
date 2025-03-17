from __future__ import annotations

from typing import List, Tuple

import cv2
import numpy as np

from src.core.config import PhysicsConfig


class Homography:
    def __init__(self, config: PhysicsConfig) -> None:
        self.config = config
        self.matrix: np.ndarray | None = None

    def calibrate(self, corners: List[Tuple[float, float]]) -> None:
        if len(corners) != 4:
            raise ValueError("Expected 4 table corners")
        world = np.array(
            [
                [0, 0],
                [self.config.table_length_m, 0],
                [self.config.table_length_m, self.config.table_width_m],
                [0, self.config.table_width_m],
            ],
            dtype=np.float32,
        )
        image = np.array(corners, dtype=np.float32)
        self.matrix, _ = cv2.findHomography(image, world)

    def pixel_to_world(self, point: Tuple[float, float]) -> Tuple[float, float]:
        if self.matrix is None:
            raise ValueError("Homography not calibrated")
        pts = np.array([[point]], dtype=np.float32)
        transformed = cv2.perspectiveTransform(pts, self.matrix)[0][0]
        return float(transformed[0]), float(transformed[1])
