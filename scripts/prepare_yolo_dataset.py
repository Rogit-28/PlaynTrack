from __future__ import annotations

import shutil
from pathlib import Path
from typing import List

import cv2

from scripts.convert_openttgames import load_annotations, _yolo_line


def extract_frames(video_path: Path, output_dir: Path) -> List[Path]:
    output_dir.mkdir(parents=True, exist_ok=True)
    cap = cv2.VideoCapture(str(video_path))
    if not cap.isOpened():
        raise RuntimeError(f"Unable to open video: {video_path}")

    frame_paths: List[Path] = []
    frame_idx = 0
    while True:
        success, frame = cap.read()
        if not success:
            break
        frame_path = output_dir / f"{video_path.stem}_{frame_idx:06d}.jpg"
        cv2.imwrite(str(frame_path), frame)
        frame_paths.append(frame_path)
        frame_idx += 1
    cap.release()
    return frame_paths


def write_labels(
    annotations_path: Path,
    label_dir: Path,
    width: int,
    height: int,
    box_size: int,
) -> None:
    annotation = load_annotations(annotations_path)
    label_dir.mkdir(parents=True, exist_ok=True)
    for frame_idx, item in annotation.annotations.items():
        label_path = label_dir / f"{annotation.video_path.stem}_{frame_idx:06d}.txt"
        label_path.write_text(_yolo_line(item, width, height, box_size))


def prepare_dataset(
    dataset_dir: Path,
    output_dir: Path,
    split: str,
    box_size: int = 12,
) -> None:
    output_images = output_dir / "images" / split
    output_labels = output_dir / "labels" / split
    output_images.mkdir(parents=True, exist_ok=True)
    output_labels.mkdir(parents=True, exist_ok=True)

    for json_path in dataset_dir.glob("*.json"):
        video_path = json_path.with_suffix(".mp4")
        if not video_path.exists():
            continue
        frame_paths = extract_frames(video_path, output_images)
        cap = cv2.VideoCapture(str(video_path))
        width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        cap.release()
        write_labels(json_path, output_labels, width, height, box_size)


def main() -> None:
    dataset_dir = Path("data/datasets/openttgames/test")
    output_dir = Path("data/datasets/openttgames")
    prepare_dataset(dataset_dir, output_dir, split="val")
    print("Prepared dataset for YOLO at", output_dir.resolve())


if __name__ == "__main__":
    main()
