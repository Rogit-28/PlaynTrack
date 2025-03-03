from __future__ import annotations

from collections import deque
from dataclasses import dataclass
from typing import Deque, Iterable, Iterator

import numpy as np


@dataclass
class FrameBatch:
    indices: list[int]
    frames: list[np.ndarray]


class FrameBuffer:
    def __init__(self, batch_size: int) -> None:
        self.batch_size = batch_size
        self._buffer: Deque[tuple[int, np.ndarray]] = deque()

    def add(self, frame_idx: int, frame: np.ndarray) -> None:
        self._buffer.append((frame_idx, frame))

    def has_batch(self) -> bool:
        return len(self._buffer) >= self.batch_size

    def pop_batch(self) -> FrameBatch:
        indices = []
        frames = []
        for _ in range(self.batch_size):
            frame_idx, frame = self._buffer.popleft()
            indices.append(frame_idx)
            frames.append(frame)
        return FrameBatch(indices=indices, frames=frames)

    def flush(self) -> Iterator[FrameBatch]:
        while self._buffer:
            batch = list(self._buffer)
            self._buffer.clear()
            indices = [item[0] for item in batch]
            frames = [item[1] for item in batch]
            yield FrameBatch(indices=indices, frames=frames)


def iter_batches(frames: Iterable[tuple[int, np.ndarray]], batch_size: int) -> Iterator[FrameBatch]:
    buffer = FrameBuffer(batch_size=batch_size)
    for frame_idx, frame in frames:
        buffer.add(frame_idx, frame)
        if buffer.has_batch():
            yield buffer.pop_batch()
    yield from buffer.flush()
