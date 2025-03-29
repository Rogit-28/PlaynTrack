from __future__ import annotations

"""Benchmark script for measuring PlaynTrack pipeline performance."""

import time
from pathlib import Path

from src.core.config import AppConfig, load_config
from src.input.video_loader import VideoLoader
from src.utils.logger import setup_logger

logger = setup_logger()


def benchmark_video_loading(video_path: Path) -> dict:
    """Benchmark video loading and frame extraction speed."""
    loader = VideoLoader(video_path)
    metadata = loader.metadata()
    total_frames = metadata.frame_count

    start = time.perf_counter()
    count = 0
    for _ in loader.read_frames():
        count += 1
    elapsed = time.perf_counter() - start

    return {
        "total_frames": total_frames,
        "frames_read": count,
        "elapsed_s": round(elapsed, 3),
        "fps_throughput": round(count / elapsed, 1) if elapsed > 0 else 0,
    }


def benchmark_pipeline(video_path: Path, config: AppConfig) -> dict:
    """Benchmark the full processing pipeline."""
    from src.pipeline.processor import VideoProcessor

    processor = VideoProcessor(config)

    start = time.perf_counter()
    result = processor.run(video_path)
    elapsed = time.perf_counter() - start

    loader = VideoLoader(video_path)
    metadata = loader.metadata()
    total_frames = metadata.frame_count

    return {
        "total_frames": total_frames,
        "trajectory_points": len(result.trajectory),
        "events": len(result.events),
        "elapsed_s": round(elapsed, 3),
        "fps_throughput": round(total_frames / elapsed, 1) if elapsed > 0 else 0,
        "ms_per_frame": round(elapsed * 1000 / total_frames, 1)
        if total_frames > 0
        else 0,
    }


def main() -> None:
    import argparse

    parser = argparse.ArgumentParser(description="Benchmark PlaynTrack pipeline")
    parser.add_argument("video", type=Path, help="Path to input video")
    parser.add_argument("--config", type=Path, default=None, help="Config YAML path")
    parser.add_argument(
        "--loading-only", action="store_true", help="Only benchmark video loading"
    )
    args = parser.parse_args()

    config = load_config(args.config)

    logger.info("Benchmarking video loading...")
    loading_result = benchmark_video_loading(args.video)
    logger.info("Loading: %s", loading_result)

    if not args.loading_only:
        logger.info("Benchmarking full pipeline...")
        pipeline_result = benchmark_pipeline(args.video, config)
        logger.info("Pipeline: %s", pipeline_result)


if __name__ == "__main__":
    main()
