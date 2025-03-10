from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, Iterable, List, Tuple

import cv2


@dataclass
class FrameAnnotation:
    frame_idx: int
    x: float
    y: float


@dataclass
class VideoAnnotations:
    video_path: Path
    annotations: Dict[int, FrameAnnotation]


def load_annotations(json_path: Path) -> VideoAnnotations:
    data = json.loads(json_path.read_text())
    annotations: Dict[int, FrameAnnotation] = {}
    for frame_str, coords in data.items():
        frame_idx = int(frame_str)
        x, y = coords
        if x < 0 or y < 0:
            continue
        annotations[frame_idx] = FrameAnnotation(frame_idx=frame_idx, x=x, y=y)
    video_path = json_path.with_suffix(".mp4")
    return VideoAnnotations(video_path=video_path, annotations=annotations)


def _yolo_line(annotation: FrameAnnotation, width: int, height: int, box_size: int) -> str:
    x_center = annotation.x / width
    y_center = annotation.y / height
    w = box_size / width
    h = box_size / height
    return f"0 {x_center:.6f} {y_center:.6f} {w:.6f} {h:.6f}"


def convert_video(annotation: VideoAnnotations, output_dir: Path, box_size: int = 12) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    cap = cv2.VideoCapture(str(annotation.video_path))
    if not cap.isOpened():
        raise RuntimeError(f"Unable to open video: {annotation.video_path}")

    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    frame_idx = 0

    while True:
        success, frame = cap.read()
        if not success:
            break
        label_path = output_dir / f"{annotation.video_path.stem}_{frame_idx:06d}.txt"
        if frame_idx in annotation.annotations:
            label_path.write_text(
                _yolo_line(annotation.annotations[frame_idx], width, height, box_size)
            )
        else:
            label_path.write_text("")
        frame_idx += 1

    cap.release()


def convert_dataset(dataset_dir: Path, output_dir: Path, box_size: int = 12) -> None:
    json_files = list(dataset_dir.glob("*.json"))
    for json_path in json_files:
        annotations = load_annotations(json_path)
        convert_video(annotations, output_dir, box_size=box_size)


def main() -> None:
    dataset_dir = Path("data/datasets/openttgames/test")
    output_dir = Path("data/datasets/openttgames/yolo_labels")
    convert_dataset(dataset_dir, output_dir)
    print(f"Converted labels saved to {output_dir.resolve()}")


if __name__ == "__main__":
    main()
