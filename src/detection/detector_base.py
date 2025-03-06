from __future__ import annotations

from abc import ABC, abstractmethod
from typing import List

import numpy as np

from src.core.types import Detection


class DetectorBase(ABC):
    @abstractmethod
    def detect(self, frame: np.ndarray) -> List[Detection]:
        raise NotImplementedError

    def detect_batch(self, frames: List[np.ndarray]) -> List[List[Detection]]:
        return [self.detect(frame) for frame in frames]
