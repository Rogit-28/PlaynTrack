# PlaynTrack

A desktop application for analyzing recorded table tennis matches. PlaynTrack detects the ball, tracks trajectories, estimates shot speed, segments rallies, and provides an interactive Gradio dashboard for exploration and data export.

## Features

- **Ball Detection** — YOLOv8-based detector with configurable confidence and NMS thresholds
- **Player Detection** — Identifies and tracks players throughout the match
- **Kalman Tracking** — Smooth trajectory estimation using a 4-state Kalman filter
- **Rally Segmentation** — Automatic detection of rallies, shots, and bounces
- **Speed Estimation** — Real-world speed via homography-based pixel-to-meter conversion
- **Interactive Dashboard** — Gradio UI with video player, charts, tables, and export
- **CSV / Video Export** — Export annotated video, shot table, rally table, and trajectory data
- **GPU Acceleration** — Optional CUDA support for faster inference

## Quick Start

### Prerequisites

- Python 3.10+
- pip
- (Optional) NVIDIA GPU with CUDA for accelerated inference

### Installation

```bash
git clone https://github.com/Rogit-28/PlaynTrack.git
cd PlaynTrack
python -m venv .venv
source .venv/bin/activate   # Linux/macOS
# .venv\Scripts\activate    # Windows
pip install -r requirements.txt
```

### Download Models

```bash
python scripts/download_models.py
```

This prepares the `models/` directory with the required YOLOv8 weights.

### Run the Dashboard

```bash
python dashboard/app.py
```

Open the URL printed in the terminal (default: `http://127.0.0.1:7860`).

### CLI Usage

```bash
python src/main.py --input data/videos/match.mp4 --output data/outputs/annotated.mp4
```

## Project Structure

```
PlaynTrack/
├── config.yaml                  # Application configuration
├── configs/                     # Training configs (YOLO)
│   ├── train_ball.yaml
│   └── yolo_ball.yaml
├── dashboard/                   # Gradio web dashboard
│   ├── app.py                   # Main dashboard entry point
│   ├── components/              # UI components
│   │   ├── charts.py            # Speed charts (Plotly)
│   │   ├── stats_panel.py       # Statistics panel
│   │   ├── timeline.py          # Rally timeline
│   │   └── video_player.py      # Video component config
│   └── handlers/                # Request handlers
│       ├── upload_handler.py    # Upload validation
│       └── export_handler.py    # Export orchestration
├── docs/
│   └── PRD.md                   # Product Requirements Document
├── scripts/                     # Utility scripts
│   ├── benchmark.py             # Pipeline benchmarking
│   ├── convert_openttgames.py   # OpenTTGames JSON → YOLO labels
│   ├── download_dataset.py      # Download OpenTTGames dataset
│   ├── download_models.py       # Download/prepare models
│   └── prepare_yolo_dataset.py  # Frame + label extraction
├── src/                         # Core library
│   ├── main.py                  # CLI entry point
│   ├── core/                    # Config, types, exceptions
│   │   ├── config.py
│   │   ├── types.py
│   │   └── exceptions.py
│   ├── input/                   # Video loading & buffering
│   │   ├── video_loader.py
│   │   └── frame_buffer.py
│   ├── detection/               # Ball & player detection
│   │   ├── detector_base.py
│   │   ├── ball_detector.py
│   │   └── player_detector.py
│   ├── tracking/                # Kalman tracking & trajectory
│   │   ├── kalman_tracker.py
│   │   ├── trajectory.py
│   │   └── association.py
│   ├── physics/                 # Homography & speed calculation
│   │   ├── homography.py
│   │   ├── table_detector.py
│   │   ├── speed_calculator.py
│   │   └── calibration.py
│   ├── segmentation/            # Event detection & rally segmentation
│   │   ├── event_types.py
│   │   ├── event_segmenter.py
│   │   ├── rally_detector.py
│   │   ├── shot_detector.py
│   │   └── bounce_detector.py
│   ├── visualization/           # AR overlays & rendering
│   │   ├── ar_visualizer.py
│   │   ├── trajectory_renderer.py
│   │   ├── speed_overlay.py
│   │   ├── stats_overlay.py
│   │   ├── color_schemes.py
│   │   └── player_overlay.py
│   ├── analytics/               # Match statistics
│   │   ├── match_stats.py
│   │   └── aggregator.py
│   ├── export/                  # Data export
│   │   ├── video_exporter.py
│   │   ├── csv_exporter.py
│   │   ├── trajectory_exporter.py
│   │   └── annotated_exporter.py
│   ├── pipeline/                # Processing pipeline
│   │   ├── processor.py
│   │   └── annotated_pipeline.py
│   └── utils/                   # Shared utilities
│       ├── logger.py
│       ├── video_utils.py
│       └── gpu_utils.py
├── tests/                       # Test suite (pytest)
│   ├── conftest.py
│   ├── test_detection.py
│   ├── test_tracking.py
│   ├── test_physics.py
│   ├── test_segmentation.py
│   ├── test_analytics.py
│   └── test_integration.py
├── requirements.txt
└── requirements-dev.txt
```

## Configuration

Application settings live in `config.yaml`:

```yaml
video:
  min_fps: 24
  max_fps: 120
  max_resolution: [1920, 1080]
  batch_size: 8

detection:
  confidence_threshold: 0.3
  nms_threshold: 0.5
  max_detections: 5

tracking:
  max_missed_frames: 10
  smoothing_window: 5

physics:
  table_length_m: 2.74
  table_width_m: 1.525
  enable_table_detection: true

segmentation:
  rally_gap_seconds: 2.0
  min_shots_per_rally: 2
  shot_angle_threshold_deg: 90.0

visualization:
  trail_length: 15
  show_player_boxes: true
  show_stats_panel: true
```

## Scripts

| Script | Purpose |
|--------|---------|
| `download_models.py` | Prepare `models/` directory with YOLO weights |
| `download_dataset.py` | Download OpenTTGames test dataset |
| `convert_openttgames.py` | Convert OpenTTGames JSON annotations to YOLO format |
| `prepare_yolo_dataset.py` | Extract frames and labels for YOLO training |
| `benchmark.py` | Measure pipeline throughput and per-frame latency |

## Dataset

PlaynTrack uses the [OpenTTGames](https://lab.osai.ai/) dataset for training and evaluation. Run the download and conversion scripts to prepare the data:

```bash
python scripts/download_dataset.py
python scripts/convert_openttgames.py
python scripts/prepare_yolo_dataset.py
```

## Running Tests

```bash
pip install -r requirements-dev.txt
pytest tests/ -v
```

## Tech Stack

| Component | Library |
|-----------|---------|
| Object Detection | [Ultralytics YOLOv8](https://docs.ultralytics.com/) |
| Tracking | [FilterPy](https://filterpy.readthedocs.io/) (Kalman filter) |
| Computer Vision | [OpenCV](https://opencv.org/) |
| Config | [Pydantic v2](https://docs.pydantic.dev/) + PyYAML |
| Dashboard | [Gradio](https://gradio.app/) |
| Charts | [Plotly](https://plotly.com/python/) + Matplotlib |
| Data | [Pandas](https://pandas.pydata.org/) + NumPy |

## Architecture

```
Video File
  │
  ▼
VideoLoader ──► BallDetector + PlayerDetector
                      │
                      ▼
               KalmanTracker
                      │
                      ▼
               EventSegmenter ──► RallyDetector
                      │            ShotDetector
                      │            BounceDetector
                      ▼
              compute_match_stats
                      │
        ┌─────────────┼─────────────┐
        ▼             ▼             ▼
   AR Visualizer   Dashboard    CSV Export
  (annotated MP4)  (Gradio)    (shots/rallies/trajectory)
```

## Performance Targets

| Metric | Target |
|--------|--------|
| Detection accuracy | > 85% mAP@0.5 |
| Tracking consistency | > 90% ID retention |
| Processing speed | > 15 FPS (GPU) |
| Speed estimation error | < 10% |

## License

This project is intended for educational and research purposes.

## Acknowledgments

- [OpenTTGames](https://lab.osai.ai/) for the table tennis dataset
- [Ultralytics](https://ultralytics.com/) for YOLOv8
- [FilterPy](https://github.com/rlabbe/filterpy) for Kalman filter implementation
