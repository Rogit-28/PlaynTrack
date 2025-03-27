from __future__ import annotations

from pathlib import Path
import sys

import gradio as gr

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from src.core.config import load_config
from dashboard.components.charts import speed_chart
from dashboard.components.stats_panel import (
    rally_dataframe,
    shots_dataframe,
    stats_summary,
)
from dashboard.components.timeline import rally_timeline
from dashboard.handlers.upload_handler import validate_upload
from src.pipeline.annotated_pipeline import run_with_export
from src.utils.video_utils import probe_video


CONFIG = load_config(Path("config.yaml") if Path("config.yaml").exists() else None)


def analyze_video(video_path: str, progress=gr.Progress()) -> tuple:
    """Process an uploaded video through the full PlaynTrack pipeline."""
    if not video_path:
        raise gr.Error("Please upload a video first.")

    path = Path(video_path)
    validation = validate_upload(path, CONFIG)
    if not validation["valid"]:
        raise gr.Error(validation["error"])

    progress(0.05, desc="Loading video...")
    metadata = probe_video(path)

    progress(0.10, desc="Initializing pipeline...")
    output_path = Path("data/outputs") / f"annotated_{path.stem}.mp4"
    output_path.parent.mkdir(parents=True, exist_ok=True)

    progress(0.15, desc="Detecting ball & players...")
    result, export_path, shots_path, rallies_path, trajectory_path = run_with_export(
        CONFIG,
        path,
        output_path,
    )

    progress(0.85, desc="Computing analytics...")
    metadata["detections"] = sum(len(items) for items in result.detections.values())
    metadata["trajectory_points"] = len(result.trajectory)
    if result.match_stats:
        metadata.update(stats_summary(result.match_stats))

    progress(0.95, desc="Preparing results...")
    shots_df = shots_dataframe(result.match_stats)
    rallies_df = rally_dataframe(result.match_stats)
    timeline_df = rally_timeline(result.match_stats)
    chart = speed_chart(result.match_stats)

    progress(1.0, desc="Done!")

    return (
        str(export_path),
        metadata,
        str(shots_path),
        str(rallies_path),
        str(trajectory_path),
        str(export_path),
        shots_df,
        rallies_df,
        timeline_df,
        chart,
    )


def build_app() -> gr.Blocks:
    with gr.Blocks(
        title="PlaynTrack - Table Tennis Analytics",
        theme=gr.themes.Soft(),
    ) as demo:
        gr.Markdown(
            "# 🏓 PlaynTrack\n"
            "### Table Tennis Ball Tracking & Speed Estimation\n"
            "Upload a match video to detect the ball, track trajectories, estimate shot speeds, "
            "and explore comprehensive match analytics."
        )

        # Upload section
        with gr.Accordion("📤 Upload Video", open=True):
            with gr.Row():
                video_input = gr.Video(label="Input Video")
                analyze_button = gr.Button(
                    "🔄 Process Video", variant="primary", scale=0
                )

        # Results section
        with gr.Row():
            video_output = gr.Video(label="Annotated Video")
            with gr.Column():
                gr.Markdown("### 📊 Match Statistics")
                metadata_output = gr.JSON(label="Video Metadata & Stats")

        # Rally timeline
        with gr.Accordion("📅 Rally Timeline", open=True):
            timeline_table = gr.Dataframe(label="Rally Timeline", interactive=False)

        # Speed chart
        with gr.Accordion("📈 Speed Over Time", open=True):
            speed_plot = gr.Plot(label="Shot Speed Over Time")

        # Detailed tables
        with gr.Row():
            with gr.Column():
                gr.Markdown("### 🎯 Shot Table")
                shots_table = gr.Dataframe(label="Shots", interactive=False)
            with gr.Column():
                gr.Markdown("### 🏐 Rally Table")
                rallies_table = gr.Dataframe(label="Rallies", interactive=False)

        # Export section
        with gr.Accordion("💾 Export Files", open=False):
            with gr.Row():
                video_download = gr.File(label="Annotated Video (MP4)")
                shots_csv = gr.File(label="Shots CSV")
                rallies_csv = gr.File(label="Rallies CSV")
                trajectory_csv = gr.File(label="Trajectory CSV")

        analyze_button.click(
            fn=analyze_video,
            inputs=video_input,
            outputs=[
                video_output,
                metadata_output,
                shots_csv,
                rallies_csv,
                trajectory_csv,
                video_download,
                shots_table,
                rallies_table,
                timeline_table,
                speed_plot,
            ],
        )

    return demo


def main() -> None:
    app = build_app()
    app.launch()


if __name__ == "__main__":
    main()
