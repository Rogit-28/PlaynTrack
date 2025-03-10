from __future__ import annotations

from pathlib import Path


def main() -> None:
    dataset_dir = Path("data/datasets/openttgames/test")
    dataset_dir.mkdir(parents=True, exist_ok=True)
    print("Dataset directory ready at", dataset_dir.resolve())
    print("Download OpenTTGames test videos from https://lab.osai.ai/")
    print("Place test videos and JSON annotations in data/datasets/openttgames/test")


if __name__ == "__main__":
    main()
