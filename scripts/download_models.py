from __future__ import annotations

from pathlib import Path


def main() -> None:
    models_dir = Path("models")
    models_dir.mkdir(parents=True, exist_ok=True)
    print("Models directory ready at", models_dir.resolve())
    print("Download YOLOv8n weights: https://github.com/ultralytics/assets/releases/")
    print("Place ball detector weights at models/ball_detector.pt")


if __name__ == "__main__":
    main()
