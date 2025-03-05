# PlaynTrack
## Product Requirements Document (PRD)
### Real-Time Table Tennis Ball Tracking & Speed Estimation

---

## Document Control

| Attribute | Value |
|-----------|-------|
| **Version** | 1.0.0 |
| **Created** | 2026-01-21 |
| **Last Updated** | 2026-01-21 |
| **Status** | Draft - Awaiting Approval |
| **Author** | OpenCode |
| **Owner** | rogit |

---

## Table of Contents

1. [Executive Summary](#1-executive-summary)
2. [Problem Statement](#2-problem-statement)
3. [Goals & Objectives](#3-goals--objectives)
4. [Target Users](#4-target-users)
5. [Scope](#5-scope)
6. [Technical Requirements](#6-technical-requirements)
7. [System Architecture](#7-system-architecture)
8. [Module Specifications](#8-module-specifications)
9. [Data Requirements](#9-data-requirements)
10. [User Interface Specifications](#10-user-interface-specifications)
11. [Performance Requirements](#11-performance-requirements)
12. [Development Phases](#12-development-phases)
13. [Risk Assessment](#13-risk-assessment)
14. [Success Metrics](#14-success-metrics)
15. [Future Enhancements](#15-future-enhancements)
16. [Feature Tracker](#16-feature-tracker)
17. [Implementation Log](#17-implementation-log)
18. [Decision Log](#18-decision-log)
19. [Open Questions](#19-open-questions)
20. [Appendix](#20-appendix)

---

## 1. Executive Summary

### 1.1 Product Vision

PlaynTrack is a desktop application that analyzes recorded table tennis match videos using computer vision and deep learning to automatically detect the ball, calculate shot speeds, visualize trajectories, segment rallies/shots, and provide comprehensive match analytics through an interactive Gradio-based dashboard.

### 1.2 Key Value Propositions

- **Automated Analysis:** No manual annotation required - upload video, get insights
- **Speed Metrics:** Real-time km/h calculation for every shot
- **Visual Feedback:** AR-style trajectory overlays on exported videos
- **Rally Intelligence:** Auto-segmentation of rallies, shots, and bounces
- **Player Tracking:** Basic player position detection for context
- **Accessible Analytics:** Interactive dashboard for non-technical users

### 1.3 Target Platform

- **Type:** Desktop Application (Local Processing)
- **Interface:** Gradio Web UI (localhost)
- **OS:** Windows 10/11 (primary), Linux/macOS (secondary)

---

## 2. Problem Statement

### 2.1 Current Pain Points

| Pain Point | Description |
|------------|-------------|
| **Manual Review** | Coaches/players must watch entire matches manually to analyze performance |
| **No Speed Data** | Amateur players have no way to measure shot speeds without expensive equipment |
| **Tedious Clipping** | Extracting highlights requires manual video editing |
| **Lost Insights** | Subtle patterns (serve speed trends, rally length) are invisible without data |

### 2.2 Opportunity

Broadcast-level analytics (like those seen in professional tournaments) are inaccessible to amateur players, coaches, and enthusiasts. PlaynTrack democratizes this technology using commodity hardware (single camera + consumer GPU).

---

## 3. Goals & Objectives

### 3.1 Primary Goals

| ID | Goal | Success Criteria |
|----|------|------------------|
| G1 | Detect ball in 24+ FPS video | >80% detection accuracy on test videos |
| G2 | Calculate shot speed in km/h | <15% error margin vs. estimated ground truth |
| G3 | Visualize ball trajectory | Smooth trail rendering without jitter |
| G4 | Auto-segment rallies/shots | >85% correct segmentation on test matches |
| G5 | Provide interactive dashboard | User can upload, analyze, and export in <10 clicks |

### 3.2 Non-Goals (Out of Scope for MVP)

| Item | Reason |
|------|--------|
| Real-time/live processing | Requires strict latency constraints; post-match is sufficient |
| Multi-camera 3D tracking | Single camera only; noted as future enhancement |
| Shot type classification | Complex ML task; defer to v2 |
| Mobile app | Desktop-first; mobile is future roadmap |
| Cloud deployment | Local processing only for MVP |

---

## 4. Target Users

### 4.1 Primary Persona: Amateur Player

| Attribute | Value |
|-----------|-------|
| **Name** | Alex |
| **Profile** | Recreational table tennis player, plays 2-3x/week |
| **Goal** | Understand their playing style, track improvement |
| **Tech Comfort** | Can install software, comfortable with basic apps |
| **Pain Point** | No way to measure progress objectively |

### 4.2 Secondary Persona: Club Coach

| Attribute | Value |
|-----------|-------|
| **Name** | Coach Lin |
| **Profile** | Coaches youth table tennis at local club |
| **Goal** | Provide data-driven feedback to students |
| **Tech Comfort** | Moderate; uses video recording already |
| **Pain Point** | Time-consuming to review all student footage |

---

## 5. Scope

### 5.1 In Scope (MVP)

| Category | Features |
|----------|----------|
| **Input** | MP4 video upload (24-120 FPS, up to 1080p) |
| **Detection** | Ball detection using fine-tuned YOLOv8 |
| **Detection** | Player detection (bounding boxes) |
| **Tracking** | Kalman filter-based trajectory prediction |
| **Tracking** | Occlusion handling (up to 10 frames) |
| **Physics** | Table detection via corner/edge detection |
| **Physics** | Homography mapping (pixels → meters) |
| **Physics** | Speed calculation (km/h) |
| **Segmentation** | Rally detection (ball in play → point scored) |
| **Segmentation** | Shot detection (direction change events) |
| **Segmentation** | Bounce detection (table contact events) |
| **Visualization** | Ball trajectory trail overlay |
| **Visualization** | Speed text overlay (floating near ball) |
| **Visualization** | Color-coded speed (green/yellow/red) |
| **Dashboard** | Video upload interface |
| **Dashboard** | Processing progress indicator |
| **Dashboard** | Annotated video player |
| **Dashboard** | Rally timeline navigator |
| **Dashboard** | Shot statistics table |
| **Dashboard** | Speed over time chart |
| **Export** | Annotated video (MP4) |
| **Export** | Statistics data (CSV) |

### 5.2 Out of Scope (MVP)

| Feature | Rationale | Future Version |
|---------|-----------|----------------|
| Live streaming overlay | Latency requirements | v2.0 |
| Multi-camera support | Hardware complexity | v2.0 |
| Shot type classification | ML complexity | v2.0 |
| Spin detection | Requires high-speed camera | v3.0 |
| Player pose estimation | Scope creep | v2.0 |
| Cloud processing | Infrastructure cost | v2.0 |
| Mobile app | Platform complexity | v3.0 |
| Match score tracking | OCR complexity | v2.0 |

---

## 6. Technical Requirements

### 6.1 Hardware Requirements

| Component | Minimum | Recommended |
|-----------|---------|-------------|
| **GPU** | NVIDIA GTX 1060 (6GB) | NVIDIA RTX 4050+ |
| **CPU** | Intel i5 / AMD Ryzen 5 | Intel i7 / AMD Ryzen 7 |
| **RAM** | 8 GB | 16 GB |
| **Storage** | 10 GB free | 50 GB free (for datasets) |
| **OS** | Windows 10 | Windows 11 |

### 6.2 Software Requirements

| Component | Version | Purpose |
|-----------|---------|---------|
| **Python** | 3.10+ | Core runtime |
| **CUDA** | 11.8+ | GPU acceleration |
| **cuDNN** | 8.6+ | Deep learning optimization |

### 6.3 Development Environment

| Aspect | Specification |
|--------|---------------|
| **Target GPU** | NVIDIA RTX 4050 |
| **Primary OS** | Windows 11 |
| **Python Version** | 3.10 or 3.11 |
| **Package Manager** | pip with requirements.txt |
| **Virtual Environment** | venv (already exists at .venv) |

### 6.4 Tech Stack

| Layer | Technology | Justification |
|-------|------------|---------------|
| **Language** | Python 3.10+ | ML ecosystem, rapid prototyping |
| **ML Framework** | PyTorch 2.0+ | Industry standard, good GPU support |
| **Object Detection** | Ultralytics YOLOv8 | SOTA small object detection, easy fine-tuning |
| **Player Detection** | YOLOv8 (COCO pretrained) | Humans already in COCO dataset |
| **Tracking** | filterpy (Kalman) | Lightweight, well-documented |
| **Computer Vision** | OpenCV 4.8+ | Industry standard |
| **Math/Science** | NumPy, SciPy | Efficient numerical operations |
| **Dashboard** | Gradio 4.0+ | ML-focused, easy video handling |
| **Video Export** | FFmpeg (imageio-ffmpeg) | Industry standard codec support |
| **Configuration** | Pydantic + YAML | Type-safe config management |
| **Logging** | Python logging + Rich | Structured logs with pretty output |
| **Testing** | pytest | Standard Python testing |

---

## 7. System Architecture

### 7.1 High-Level Architecture

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                              PlaynTrack System                              │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │                         INPUT LAYER                                  │   │
│  │  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐                  │   │
│  │  │   Video     │  │   Config    │  │   Model     │                  │   │
│  │  │   Loader    │  │   Parser    │  │   Loader    │                  │   │
│  │  │  (MP4/AVI)  │  │   (YAML)    │  │  (Weights)  │                  │   │
│  │  └──────┬──────┘  └──────┬──────┘  └──────┬──────┘                  │   │
│  └─────────┼────────────────┼────────────────┼──────────────────────────┘   │
│            │                │                │                              │
│            ▼                ▼                ▼                              │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │                       PROCESSING LAYER                               │   │
│  │                                                                      │   │
│  │  ┌──────────────┐    ┌──────────────┐    ┌──────────────┐           │   │
│  │  │   Module A   │    │   Module A'  │    │   Module B   │           │   │
│  │  │    Ball      │    │   Player     │    │  Trajectory  │           │   │
│  │  │  Detection   │    │  Detection   │    │   Tracking   │           │   │
│  │  │  (YOLOv8)    │    │  (YOLOv8)    │    │  (Kalman)    │           │   │
│  │  └──────┬───────┘    └──────┬───────┘    └──────┬───────┘           │   │
│  │         │                   │                   │                    │   │
│  │         └─────────┬─────────┴─────────┬─────────┘                    │   │
│  │                   ▼                   ▼                              │   │
│  │         ┌──────────────┐    ┌──────────────┐                         │   │
│  │         │   Module C   │    │   Module E   │                         │   │
│  │         │   Physics    │    │    Event     │                         │   │
│  │         │   Engine     │    │  Segmenter   │                         │   │
│  │         │ (Homography) │    │(Rally/Shot)  │                         │   │
│  │         └──────┬───────┘    └──────┬───────┘                         │   │
│  │                │                   │                                 │   │
│  └────────────────┼───────────────────┼─────────────────────────────────┘   │
│                   │                   │                                     │
│                   ▼                   ▼                                     │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │                        OUTPUT LAYER                                  │   │
│  │                                                                      │   │
│  │  ┌──────────────┐    ┌──────────────┐    ┌──────────────┐           │   │
│  │  │   Module D   │    │  Analytics   │    │    Export    │           │   │
│  │  │     AR       │    │   Engine     │    │    Engine    │           │   │
│  │  │ Visualizer   │    │   (Stats)    │    │  (MP4/CSV)   │           │   │
│  │  └──────────────┘    └──────────────┘    └──────────────┘           │   │
│  │                                                                      │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
│                                      │                                      │
│                                      ▼                                      │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │                       PRESENTATION LAYER                             │   │
│  │                                                                      │   │
│  │                    ┌────────────────────┐                            │   │
│  │                    │   Gradio Dashboard │                            │   │
│  │                    │   (Web Interface)  │                            │   │
│  │                    └────────────────────┘                            │   │
│  │                                                                      │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

### 7.2 Data Flow

```
Video File (MP4)
       │
       ▼
┌──────────────┐
│ Frame        │──── frames[], fps, resolution
│ Extraction   │
└──────────────┘
       │
       ▼
┌──────────────┐     ┌──────────────┐
│ Ball         │     │ Player       │
│ Detector     │     │ Detector     │
└──────────────┘     └──────────────┘
       │                    │
       │ ball_detections[]  │ player_detections[]
       │                    │
       ▼                    ▼
┌─────────────────────────────────────┐
│           Tracker                    │
│  (Kalman Filter + Association)       │
└─────────────────────────────────────┘
       │
       │ trajectories[]
       ▼
┌──────────────┐     ┌──────────────┐
│ Event        │     │ Physics      │
│ Segmenter    │     │ Engine       │
└──────────────┘     └──────────────┘
       │                    │
       │ events[]           │ speeds[], distances[]
       │                    │
       ▼                    ▼
┌─────────────────────────────────────┐
│         Analytics Engine             │
│  (Aggregate stats per rally/match)   │
└─────────────────────────────────────┘
       │
       │ match_analytics{}
       ▼
┌──────────────┐     ┌──────────────┐
│ AR           │     │ Export       │
│ Visualizer   │     │ Engine       │
└──────────────┘     └──────────────┘
       │                    │
       ▼                    ▼
  Annotated Video      CSV Data
     (MP4)              File
```

### 7.3 Project Structure

```
PlaynTrack/
├── .venv/                      # Virtual environment (existing)
├── .git/                       # Git repository (existing)
│
├── src/                        # Source code
│   ├── __init__.py
│   ├── main.py                 # Entry point
│   │
│   ├── core/                   # Core abstractions
│   │   ├── __init__.py
│   │   ├── config.py           # Pydantic config models
│   │   ├── types.py            # Type definitions
│   │   └── exceptions.py       # Custom exceptions
│   │
│   ├── input/                  # Input layer
│   │   ├── __init__.py
│   │   ├── video_loader.py     # Video file handling
│   │   └── frame_buffer.py     # Frame buffering for batch processing
│   │
│   ├── detection/              # Module A: Object detection
│   │   ├── __init__.py
│   │   ├── ball_detector.py    # YOLOv8 ball detection
│   │   ├── player_detector.py  # YOLOv8 player detection
│   │   └── detector_base.py    # Abstract detector class
│   │
│   ├── tracking/               # Module B: Trajectory tracking
│   │   ├── __init__.py
│   │   ├── kalman_tracker.py   # Kalman filter implementation
│   │   ├── trajectory.py       # Trajectory data structures
│   │   └── association.py      # Detection-to-track association
│   │
│   ├── physics/                # Module C: Physics calculations
│   │   ├── __init__.py
│   │   ├── homography.py       # Pixel-to-world mapping
│   │   ├── table_detector.py   # Table corner detection
│   │   ├── speed_calculator.py # Velocity calculations
│   │   └── calibration.py      # Camera calibration helpers
│   │
│   ├── segmentation/           # Module E: Event segmentation
│   │   ├── __init__.py
│   │   ├── rally_detector.py   # Rally start/end detection
│   │   ├── shot_detector.py    # Individual shot detection
│   │   ├── bounce_detector.py  # Bounce event detection
│   │   └── event_types.py      # Event data structures
│   │
│   ├── visualization/          # Module D: AR visualization
│   │   ├── __init__.py
│   │   ├── trajectory_renderer.py  # Ball trail drawing
│   │   ├── speed_overlay.py    # Speed text rendering
│   │   ├── stats_overlay.py    # Statistics panel
│   │   └── color_schemes.py    # Speed-based coloring
│   │
│   ├── analytics/              # Analytics engine
│   │   ├── __init__.py
│   │   ├── match_stats.py      # Match-level statistics
│   │   ├── rally_stats.py      # Rally-level statistics
│   │   └── aggregator.py       # Stats aggregation
│   │
│   ├── export/                 # Export engine
│   │   ├── __init__.py
│   │   ├── video_exporter.py   # Annotated video export
│   │   └── csv_exporter.py     # Statistics CSV export
│   │
│   ├── pipeline/               # Orchestration
│   │   ├── __init__.py
│   │   ├── processor.py        # Main processing pipeline
│   │   └── batch_processor.py  # Batch frame processing
│   │
│   └── utils/                  # Utilities
│       ├── __init__.py
│       ├── logger.py           # Logging setup
│       ├── gpu_utils.py        # GPU detection/management
│       └── video_utils.py      # Video helper functions
│
├── dashboard/                  # Gradio application
│   ├── __init__.py
│   ├── app.py                  # Main Gradio app
│   ├── components/             # UI components
│   │   ├── __init__.py
│   │   ├── video_player.py     # Video player component
│   │   ├── timeline.py         # Rally timeline component
│   │   ├── stats_panel.py      # Statistics panel
│   │   └── charts.py           # Speed charts
│   └── handlers/               # Event handlers
│       ├── __init__.py
│       ├── upload_handler.py   # Video upload handling
│       └── export_handler.py   # Export handling
│
├── models/                     # Model weights (gitignored)
│   ├── .gitkeep
│   ├── ball_detector.pt        # Fine-tuned ball detection model
│   └── yolov8n.pt              # Pre-trained YOLO for players
│
├── data/                       # Data directory (gitignored)
│   ├── .gitkeep
│   ├── sample/                 # Sample videos for testing
│   ├── datasets/               # Training datasets
│   └── outputs/                # Processed outputs
│
├── configs/                    # Configuration files
│   ├── default.yaml            # Default configuration
│   ├── detection.yaml          # Detection parameters
│   └── visualization.yaml      # Visualization settings
│
├── tests/                      # Test suite
│   ├── __init__.py
│   ├── conftest.py             # Pytest fixtures
│   ├── test_detection/
│   ├── test_tracking/
│   ├── test_physics/
│   └── test_integration/
│
├── scripts/                    # Utility scripts
│   ├── download_models.py      # Download pre-trained models
│   ├── download_dataset.py     # Download OpenTTGames dataset
│   └── benchmark.py            # Performance benchmarking
│
├── docs/                       # Documentation
│   └── PRD.md                  # This document
│
├── requirements.txt            # Python dependencies
├── requirements-dev.txt        # Development dependencies
├── config.yaml                 # User configuration
├── .gitignore                  # Git ignore rules
└── README.md                   # Project README
```

---

## 8. Module Specifications

### 8.1 Module A: Ball Detection

#### 8.1.1 Overview

| Attribute | Value |
|-----------|-------|
| **Purpose** | Detect table tennis ball in each video frame |
| **Input** | RGB frame (numpy array) |
| **Output** | List of detections: `[(x, y, w, h, confidence)]` |
| **Model** | YOLOv8-nano or YOLOv8-small, fine-tuned |
| **Target Accuracy** | >80% mAP on test set |
| **Target Speed** | <20ms per frame on RTX 4050 |

#### 8.1.2 Technical Approach

1. **Base Model:** YOLOv8n (nano) - fastest, suitable for single small object
2. **Fine-tuning Dataset:** OpenTTGames test videos (~5GB)
3. **Data Augmentation:**
   - Synthetic motion blur (simulate 24-60 FPS blur)
   - Brightness/contrast variations
   - Scale variations (ball size changes with distance)
4. **Post-processing:**
   - Confidence threshold: 0.3 (tunable)
   - NMS threshold: 0.5
   - Single detection mode (only highest confidence if multiple)

#### 8.1.3 Challenges & Mitigations

| Challenge | Mitigation |
|----------|------------|
| Motion blur at low FPS | Train on blur-augmented data |
| Ball occluded by player | Pass to tracker for interpolation |
| Similar colored objects | Use temporal consistency |
| Variable ball sizes | Multi-scale training |

#### 8.1.4 API Specification

```python
class BallDetector:
    def __init__(self, model_path: str, config: DetectionConfig):
        """Initialize detector with model weights and config."""
        
    def detect(self, frame: np.ndarray) -> List[Detection]:
        """
        Detect ball in a single frame.
        
        Args:
            frame: BGR image (H, W, 3)
            
        Returns:
            List of Detection objects, sorted by confidence
        """
        
    def detect_batch(self, frames: List[np.ndarray]) -> List[List[Detection]]:
        """Batch detection for efficiency."""
        
@dataclass
class Detection:
    x: float          # Center X (pixels)
    y: float          # Center Y (pixels)
    width: float      # Bounding box width
    height: float     # Bounding box height
    confidence: float # Detection confidence (0-1)
    frame_idx: int    # Frame index
```

---

### 8.2 Module A': Player Detection

#### 8.2.1 Overview

| Attribute | Value |
|-----------|-------|
| **Purpose** | Detect players for context and segmentation assistance |
| **Input** | RGB frame (numpy array) |
| **Output** | List of player detections: `[(x, y, w, h, confidence, player_id)]` |
| **Model** | YOLOv8n pre-trained on COCO (person class) |
| **Target Accuracy** | >90% (pre-trained is sufficient) |

#### 8.2.2 Technical Approach

1. **Model:** YOLOv8n with COCO weights (no fine-tuning needed)
2. **Filter:** Only keep "person" class detections
3. **Association:** Track player IDs across frames (left player vs right player)

#### 8.2.3 API Specification

```python
class PlayerDetector:
    def __init__(self, model_path: str, config: DetectionConfig):
        """Initialize with pre-trained YOLO."""
        
    def detect(self, frame: np.ndarray) -> List[PlayerDetection]:
        """Detect players in frame."""
        
@dataclass
class PlayerDetection:
    x: float
    y: float
    width: float
    height: float
    confidence: float
    player_id: Optional[int]  # 0=left, 1=right, None=unassigned
```

---

### 8.3 Module B: Trajectory Tracking

#### 8.3.1 Overview

| Attribute | Value |
|-----------|-------|
| **Purpose** | Maintain continuous ball trajectory across frames |
| **Input** | Ball detections per frame |
| **Output** | Smoothed trajectory with interpolated positions |
| **Algorithm** | Kalman Filter with constant velocity model |
| **Occlusion Tolerance** | Up to 10 frames (configurable) |

#### 8.3.2 Technical Approach

1. **State Vector:** `[x, y, vx, vy]` (position + velocity)
2. **Measurement:** `[x, y]` (detected position)
3. **Prediction:** Linear motion model (constant velocity)
4. **Association:** IoU-based matching between prediction and detection
5. **Interpolation:** Cubic spline for missing frames

#### 8.3.3 Track Lifecycle

```
Detection → New Track (if no match)
         → Update Track (if match found)
         → Predict Only (if no detection, track still active)
         → Track Lost (if no detection for N frames)
```

#### 8.3.4 API Specification

```python
class KalmanTracker:
    def __init__(self, config: TrackingConfig):
        """Initialize tracker with config."""
        
    def update(self, detections: List[Detection], frame_idx: int) -> Trajectory:
        """
        Update tracker with new detections.
        
        Returns current trajectory state.
        """
        
    def get_trajectory(self) -> Trajectory:
        """Get complete trajectory with interpolation."""
        
@dataclass
class TrajectoryPoint:
    x: float
    y: float
    vx: float           # Velocity X (pixels/frame)
    vy: float           # Velocity Y (pixels/frame)
    frame_idx: int
    is_detected: bool   # True if detected, False if interpolated
    confidence: float
    
@dataclass
class Trajectory:
    points: List[TrajectoryPoint]
    track_id: int
```

---

### 8.4 Module C: Physics Engine

#### 8.4.1 Overview

| Attribute | Value |
|-----------|-------|
| **Purpose** | Convert pixel measurements to real-world units |
| **Input** | Trajectory (pixels), table corners, video FPS |
| **Output** | Speed (km/h), distance (meters) |
| **Method** | Homography transformation |

#### 8.4.2 Technical Approach

##### 8.4.2.1 Table Detection

1. **Edge Detection:** Canny edge detector
2. **Line Detection:** Hough transform for table lines
3. **Corner Extraction:** Intersection of detected lines
4. **Fallback:** Manual corner annotation UI

##### 8.4.2.2 Homography Calculation

```
Real-world table dimensions:
- Length: 2.74 m
- Width: 1.525 m
- Net height: 0.1525 m

Homography matrix H maps:
[x_pixel]     [x_world]
[y_pixel] → H × [y_world]
[1      ]     [1       ]
```

##### 8.4.2.3 Speed Calculation

```python
# Distance between consecutive trajectory points
dx_world = homography_transform(x2) - homography_transform(x1)
dy_world = homography_transform(y2) - homography_transform(y1)
distance = sqrt(dx_world² + dy_world²)  # meters

# Time between frames
time = 1 / fps  # seconds

# Speed
speed_mps = distance / time  # m/s
speed_kmh = speed_mps * 3.6  # km/h
```

#### 8.4.3 Limitations (Single Camera)

| Limitation | Impact | Mitigation |
|------------|--------|------------|
| No depth information | Can't measure Z-axis motion | Focus on horizontal speed |
| Perspective distortion | Speed varies with ball position | Use homography correction |
| Camera angle sensitivity | Different angles = different accuracy | Document recommended angles |

#### 8.4.4 API Specification

```python
class PhysicsEngine:
    def __init__(self, config: PhysicsConfig):
        """Initialize physics engine."""
        
    def calibrate(self, table_corners: List[Tuple[float, float]]) -> None:
        """
        Calibrate homography with table corners.
        
        Args:
            table_corners: 4 corner points in pixel coordinates
                          [(top_left), (top_right), (bottom_right), (bottom_left)]
        """
        
    def calculate_speed(self, p1: TrajectoryPoint, p2: TrajectoryPoint, fps: float) -> float:
        """
        Calculate speed between two trajectory points.
        
        Returns:
            Speed in km/h
        """
        
    def pixel_to_world(self, x: float, y: float) -> Tuple[float, float]:
        """Convert pixel coordinates to world coordinates (meters)."""
        
class TableDetector:
    def detect(self, frame: np.ndarray) -> Optional[List[Tuple[float, float]]]:
        """
        Auto-detect table corners.
        
        Returns:
            4 corner points or None if detection failed
        """
```

---

### 8.5 Module D: AR Visualization

#### 8.5.1 Overview

| Attribute | Value |
|-----------|-------|
| **Purpose** | Render visual overlays on video frames |
| **Input** | Original frame, trajectory, speed, events |
| **Output** | Annotated frame |
| **Rendering** | OpenCV drawing functions |

#### 8.5.2 Visual Elements

##### 8.5.2.1 Ball Trajectory Trail

| Property | Value |
|----------|-------|
| Style | Gradient line with decreasing opacity |
| Length | Last 15 frames (configurable) |
| Color | Speed-based (green→yellow→red) |
| Width | 3px at head, 1px at tail |

##### 8.5.2.2 Speed Overlay

| Property | Value |
|----------|-------|
| Position | Offset from ball (top-right) |
| Format | "XX km/h" |
| Font | Sans-serif, bold |
| Background | Semi-transparent black |
| Color | White text |

##### 8.5.2.3 Speed Color Coding

| Speed Range | Color | Hex Code |
|-------------|-------|----------|
| 0-30 km/h | Green | #00FF00 |
| 30-50 km/h | Yellow | #FFFF00 |
| 50+ km/h | Red | #FF0000 |

##### 8.5.2.4 Player Bounding Boxes (Optional)

| Property | Value |
|----------|-------|
| Style | Dashed rectangle |
| Color | Blue (#0066FF) |
| Label | "Player 1" / "Player 2" |

#### 8.5.3 API Specification

```python
class ARVisualizer:
    def __init__(self, config: VisualizationConfig):
        """Initialize visualizer."""
        
    def render(self, 
               frame: np.ndarray, 
               trajectory: Trajectory,
               speed: Optional[float],
               events: List[Event],
               players: List[PlayerDetection]) -> np.ndarray:
        """
        Render all overlays on frame.
        
        Returns:
            Annotated frame
        """
        
class TrajectoryRenderer:
    def render(self, frame: np.ndarray, trajectory: Trajectory) -> np.ndarray:
        """Draw trajectory trail."""
        
class SpeedOverlay:
    def render(self, frame: np.ndarray, speed: float, position: Tuple[int, int]) -> np.ndarray:
        """Draw speed text."""
```

---

### 8.6 Module E: Event Segmentation

#### 8.6.1 Overview

| Attribute | Value |
|-----------|-------|
| **Purpose** | Detect rallies, shots, and bounces automatically |
| **Input** | Full trajectory, player positions |
| **Output** | List of events with timestamps |

#### 8.6.2 Event Types

##### 8.6.2.1 Rally

| Property | Detection Logic |
|----------|-----------------|
| **Start** | Ball first appears after >2 second gap |
| **End** | Ball disappears for >2 seconds OR exits frame bounds |
| **Validation** | Minimum 2 shots to count as valid rally |

##### 8.6.2.2 Shot (Hit)

| Property | Detection Logic |
|----------|-----------------|
| **Trigger** | Sudden velocity direction change (>90°) |
| **Validation** | Ball near player bounding box at time of direction change |
| **Attribution** | Assign to nearest player |

##### 8.6.2.3 Bounce

| Property | Detection Logic |
|----------|-----------------|
| **Trigger** | Velocity Y changes from negative to positive (downward→upward) |
| **Validation** | Ball Y-coordinate near table plane |
| **Location** | Map to table half (left/right) |

#### 8.6.3 State Machine

```
                    ┌─────────────┐
                    │   IDLE      │
                    │ (No ball)   │
                    └──────┬──────┘
                           │ Ball detected
                           ▼
                    ┌─────────────┐
          ┌────────│  IN_RALLY   │────────┐
          │        │ (Ball in    │        │
          │        │   play)     │        │
          │        └──────┬──────┘        │
          │               │               │
    Shot detected    Bounce detected   Ball lost
          │               │               │
          ▼               ▼               ▼
    ┌──────────┐   ┌──────────┐   ┌──────────┐
    │  SHOT    │   │  BOUNCE  │   │  ENDING  │
    │ (Record) │   │ (Record) │   │ (Wait    │
    └────┬─────┘   └────┬─────┘   │ confirm) │
         │              │         └────┬─────┘
         └──────┬───────┘              │
                │                      │ Timeout
                ▼                      ▼
         ┌─────────────┐        ┌─────────────┐
         │  IN_RALLY   │        │   IDLE      │
         │ (Continue)  │        │ (Rally end) │
         └─────────────┘        └─────────────┘
```

#### 8.6.4 API Specification

```python
@dataclass
class Event:
    event_type: EventType  # RALLY_START, RALLY_END, SHOT, BOUNCE
    frame_idx: int
    timestamp: float       # seconds from video start
    position: Tuple[float, float]
    speed: Optional[float] # km/h at event time
    player_id: Optional[int]  # for SHOT events
    metadata: Dict[str, Any]
    
class EventType(Enum):
    RALLY_START = "rally_start"
    RALLY_END = "rally_end"
    SHOT = "shot"
    BOUNCE = "bounce"
    
class EventSegmenter:
    def __init__(self, config: SegmentationConfig):
        """Initialize segmenter."""
        
    def process(self, 
                trajectory: Trajectory, 
                players: List[List[PlayerDetection]],
                fps: float) -> List[Event]:
        """
        Process trajectory and detect all events.
        
        Returns:
            List of events sorted by frame_idx
        """
        
class RallyDetector:
    def detect(self, trajectory: Trajectory) -> List[Rally]:
        """Detect rally boundaries."""
        
@dataclass
class Rally:
    start_frame: int
    end_frame: int
    shots: List[Event]
    bounces: List[Event]
    duration: float  # seconds
```

---

### 8.7 Analytics Engine

#### 8.7.1 Computed Statistics

##### 8.7.1.1 Match-Level Stats

| Statistic | Calculation |
|-----------|-------------|
| Total rallies | Count of Rally objects |
| Average rally duration | Mean of rally durations |
| Longest rally | Max rally by shot count |
| Total shots | Sum of all shots |
| Max speed | Maximum speed across all shots |
| Average speed | Mean speed across all shots |

##### 8.7.1.2 Rally-Level Stats

| Statistic | Calculation |
|-----------|-------------|
| Rally duration | End time - start time |
| Shot count | Number of SHOT events |
| Bounce count | Number of BOUNCE events |
| Max speed | Maximum shot speed in rally |
| Average speed | Mean shot speed in rally |
| First shot speed | Speed of serve/return |

##### 8.7.1.3 Player-Level Stats (if player tracking enabled)

| Statistic | Calculation |
|-----------|-------------|
| Shots by player | Count shots attributed to each player |
| Average speed by player | Mean speed per player |
| Max speed by player | Max speed per player |

#### 8.7.2 API Specification

```python
@dataclass
class MatchAnalytics:
    total_duration: float
    total_rallies: int
    total_shots: int
    max_speed: float
    avg_speed: float
    longest_rally: Rally
    rallies: List[RallyAnalytics]
    speed_histogram: List[int]  # binned speed distribution
    
@dataclass
class RallyAnalytics:
    rally_id: int
    start_time: float
    end_time: float
    duration: float
    shot_count: int
    bounce_count: int
    max_speed: float
    avg_speed: float
    shots: List[ShotAnalytics]
    
@dataclass  
class ShotAnalytics:
    shot_id: int
    timestamp: float
    speed: float
    player_id: Optional[int]
    
class AnalyticsEngine:
    def compute(self, 
                events: List[Event],
                trajectory: Trajectory,
                fps: float) -> MatchAnalytics:
        """Compute all analytics from events."""
```

---

### 8.8 Export Engine

#### 8.8.1 Video Export

| Property | Value |
|----------|-------|
| Format | MP4 (H.264 codec) |
| Resolution | Same as input |
| FPS | Same as input |
| Quality | CRF 18 (high quality) |
| Audio | Preserved from original |

#### 8.8.2 CSV Export

##### 8.8.2.1 shots.csv

```csv
shot_id,rally_id,timestamp,frame,speed_kmh,player_id,position_x,position_y
1,1,2.34,56,45.2,0,320,180
2,1,2.89,69,38.7,1,960,200
...
```

##### 8.8.2.2 rallies.csv

```csv
rally_id,start_time,end_time,duration,shot_count,max_speed,avg_speed
1,2.00,8.50,6.50,12,67.3,42.1
2,10.20,15.80,5.60,8,55.2,38.9
...
```

##### 8.8.2.3 trajectory.csv

```csv
frame,timestamp,ball_x,ball_y,ball_detected,speed_kmh,event_type
0,0.000,320,180,true,0.0,
1,0.042,325,175,true,12.3,
...
56,2.333,340,160,true,45.2,shot
...
```

#### 8.8.3 API Specification

```python
class VideoExporter:
    def export(self,
               frames: Iterator[np.ndarray],
               output_path: str,
               fps: float,
               audio_source: Optional[str] = None) -> None:
        """Export annotated video with optional audio."""
        
class CSVExporter:
    def export_shots(self, analytics: MatchAnalytics, path: str) -> None:
        """Export shots to CSV."""
        
    def export_rallies(self, analytics: MatchAnalytics, path: str) -> None:
        """Export rallies to CSV."""
        
    def export_trajectory(self, trajectory: Trajectory, path: str) -> None:
        """Export full trajectory to CSV."""
```

---

## 9. Data Requirements

### 9.1 Training Data

#### 9.1.1 Primary Dataset: OpenTTGames

| Attribute | Value |
|-----------|-------|
| **Source** | https://lab.osai.ai/ |
| **Size** | ~35 GB total |
| **MVP Subset** | Test videos only (~5 GB) |
| **Format** | MP4 videos + JSON annotations |
| **FPS** | 120 FPS |
| **Resolution** | 1920x1080 |

#### 9.1.2 Dataset Download Plan

| Phase | Data | Size | Purpose |
|-------|------|------|---------|
| **MVP** | test_1.mp4 - test_7.mp4 | ~5 GB | Initial training + validation |
| **v1.1** | game_1.mp4 + markup | ~6 GB | Fine-tuning |
| **v1.2** | Full dataset | ~35 GB | Production model |

### 9.2 Test Data

#### 9.2.1 User-Provided Sample

| Attribute | Value |
|-----------|-------|
| **File** | `C:\Users\rogit\Downloads\RDT_20240918_150937.mp4` |
| **Purpose** | Real-world testing, validation |
| **FPS** | TBD (need to inspect) |
| **Resolution** | TBD |

### 9.3 Data Storage

```
data/
├── datasets/
│   └── openttgames/
│       ├── test/
│       │   ├── test_1.mp4
│       │   ├── test_1.json
│       │   └── ...
│       └── train/              # Added in v1.1+
│           ├── game_1.mp4
│           └── ...
├── sample/
│   └── user_sample.mp4         # Copy of user's test video
└── outputs/
    ├── annotated/              # Exported videos
    └── analytics/              # Exported CSVs
```

---

## 10. User Interface Specifications

### 10.1 Gradio Dashboard Layout

```
┌─────────────────────────────────────────────────────────────────────────────┐
│  PlaynTrack - Table Tennis Analytics                              [v1.0.0] │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  ┌─────────────────────────────────────────┐  ┌──────────────────────────┐ │
│  │                                         │  │    MATCH STATISTICS      │ │
│  │           VIDEO PLAYER                  │  │                          │ │
│  │                                         │  │  Total Rallies: 24       │ │
│  │      [Annotated video playback]         │  │  Total Shots: 187        │ │
│  │                                         │  │  Max Speed: 72.3 km/h    │ │
│  │                                         │  │  Avg Speed: 41.2 km/h    │ │
│  │                                         │  │                          │ │
│  │  [▶ Play] [⏸ Pause] [⏮][⏭] [1x ▼]     │  │  Longest Rally: #7       │ │
│  │                                         │  │    (18 shots)            │ │
│  └─────────────────────────────────────────┘  └──────────────────────────┘ │
│                                                                             │
│  ┌─────────────────────────────────────────────────────────────────────────┤
│  │  RALLY TIMELINE                                                         │
│  │  ══════════════════════════════════════════════════════════════════     │
│  │  │R1│  │R2│    │R3││R4│  │R5│      │R6│  │R7████│  │R8│   │R9│        │
│  │  ══════════════════════════════════════════════════════════════════     │
│  │  00:00          01:00          02:00          03:00          04:00      │
│  └─────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  ┌─────────────────────────────────────────────────────────────────────────┤
│  │  SPEED OVER TIME                                                        │
│  │  km/h                                                                   │
│  │  80 ┤                    ╭─╮         ╭──╮                               │
│  │  60 ┤      ╭─╮    ╭──╮  │ │   ╭─╮  │  │    ╭─╮                         │
│  │  40 ┤  ╭──╮│ │╭──╮│  ╰──╯ ╰───╯ ╰──╯  ╰────╯ ╰──                       │
│  │  20 ┤──╯  ╰╯ ╰╯  ╰╯                                                     │
│  │   0 ┼─────────────────────────────────────────────────────────────      │
│  │     00:00      01:00      02:00      03:00      04:00                   │
│  └─────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  ┌──────────────────────────────────────┐  ┌──────────────────────────────┐│
│  │  SHOT TABLE                          │  │  EXPORT OPTIONS              ││
│  │  ┌────┬────────┬────────┬─────────┐  │  │                              ││
│  │  │ #  │ Time   │ Speed  │ Player  │  │  │  [📹 Export Video]           ││
│  │  ├────┼────────┼────────┼─────────┤  │  │                              ││
│  │  │ 1  │ 00:02  │ 45 km/h│ Player 1│  │  │  [📊 Export CSV]             ││
│  │  │ 2  │ 00:03  │ 38 km/h│ Player 2│  │  │                              ││
│  │  │ 3  │ 00:04  │ 52 km/h│ Player 1│  │  │  Format: [MP4 ▼]             ││
│  │  │... │ ...    │ ...    │ ...     │  │  │  Quality: [High ▼]           ││
│  │  └────┴────────┴────────┴─────────┘  │  │                              ││
│  │  Showing 1-10 of 187  [<] [1] [2] [>]│  └──────────────────────────────┘│
│  └──────────────────────────────────────┘                                   │
│                                                                             │
├─────────────────────────────────────────────────────────────────────────────┤
│  ┌─────────────────────────────────────────────────────────────────────────┤
│  │  UPLOAD VIDEO                                                           │
│  │  ┌─────────────────────────────────────────────────────────────────┐    │
│  │  │                                                                 │    │
│  │  │     Drag and drop video file here                              │    │
│  │  │            or click to browse                                   │    │
│  │  │                                                                 │    │
│  │  │     Supported: MP4, AVI, MOV (24-120 FPS, up to 1080p)         │    │
│  │  │                                                                 │    │
│  │  └─────────────────────────────────────────────────────────────────┘    │
│  │                                                                         │
│  │  [🔄 Process Video]                                                     │
│  │                                                                         │
│  │  Processing: ████████████████████░░░░░░░░░░ 65% - Detecting ball...    │
│  └─────────────────────────────────────────────────────────────────────────┤
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

### 10.2 UI Components

| Component | Gradio Element | Description |
|-----------|----------------|-------------|
| Video Player | `gr.Video` | Playback with custom controls |
| Upload | `gr.File` / `gr.Video` | Drag-drop upload |
| Progress | `gr.Progress` | Processing progress bar |
| Stats Panel | `gr.Dataframe` / `gr.JSON` | Statistics display |
| Timeline | Custom HTML/JS | Rally navigator |
| Speed Chart | `gr.Plot` (Plotly) | Interactive speed graph |
| Shot Table | `gr.Dataframe` | Paginated shot list |
| Export Buttons | `gr.Button` + `gr.File` | Download triggers |

### 10.3 User Flow

```
1. User opens app (localhost:7860)
           │
           ▼
2. User uploads video file
           │
           ▼
3. User clicks "Process Video"
           │
           ▼
4. Progress bar shows processing stages:
   - Loading video... (5%)
   - Detecting table... (10%)
   - Detecting ball... (10-60%)
   - Tracking trajectory... (60-70%)
   - Detecting events... (70-80%)
   - Computing analytics... (80-90%)
   - Rendering overlays... (90-100%)
           │
           ▼
5. Results displayed:
   - Annotated video player
   - Match statistics
   - Rally timeline
   - Speed chart
   - Shot table
           │
           ▼
6. User can:
   - Play annotated video
   - Click on rallies to jump
   - View shot details
   - Export video/CSV
```

---

## 11. Performance Requirements

### 11.1 Processing Speed Targets

| Metric | Target | Notes |
|--------|--------|-------|
| **Detection (per frame)** | <30ms | YOLOv8n on RTX 4050 |
| **Total pipeline (per frame)** | <50ms | All modules combined |
| **1-minute video processing** | <3 minutes | 24 FPS = 1440 frames |
| **5-minute video processing** | <15 minutes | Target use case |

### 11.2 Accuracy Targets

| Metric | Target | Measurement |
|--------|--------|-------------|
| **Ball detection mAP** | >80% | On OpenTTGames test set |
| **Tracking continuity** | >90% | % frames with valid track |
| **Rally detection F1** | >85% | Precision/recall on manual labels |
| **Speed accuracy** | <15% error | Compared to estimated ground truth |

### 11.3 Resource Usage

| Resource | Limit | Notes |
|----------|-------|-------|
| **GPU VRAM** | <4 GB | RTX 4050 has 6GB |
| **System RAM** | <8 GB | For video buffering |
| **Disk (temp)** | <2x video size | For frame extraction |

---

## 12. Development Phases

### 12.1 Phase Overview

| Phase | Duration | Focus | Deliverable |
|-------|----------|-------|-------------|
| **Phase 1** | Week 1 | Foundation | Project structure, video I/O |
| **Phase 2** | Week 2-3 | Detection | Ball + player detection working |
| **Phase 3** | Week 3-4 | Tracking | Smooth trajectories |
| **Phase 4** | Week 4 | Segmentation | Rally/shot detection |
| **Phase 5** | Week 5 | Physics | Speed calculation |
| **Phase 6** | Week 5-6 | Visualization | AR overlays |
| **Phase 7** | Week 6-7 | Dashboard | Gradio UI complete |
| **Phase 8** | Week 7-8 | Polish | Testing, optimization, docs |

### 12.2 Phase 1: Foundation (Week 1)

#### 12.2.1 Objectives
- Set up project structure
- Implement video loading/frame extraction
- Set up configuration system
- Download initial models and data

#### 12.2.2 Tasks

| Task ID | Task | Priority | Status |
|---------|------|----------|--------|
| P1-001 | Create project directory structure | High | Pending |
| P1-002 | Create requirements.txt with dependencies | High | Pending |
| P1-003 | Implement config system (Pydantic + YAML) | High | Pending |
| P1-004 | Implement VideoLoader class | High | Pending |
| P1-005 | Implement FrameBuffer for batch processing | Medium | Pending |
| P1-006 | Set up logging with Rich | Medium | Pending |
| P1-007 | Create download script for models | Medium | Pending |
| P1-008 | Create download script for dataset | Medium | Pending |
| P1-009 | Set up pytest and initial test structure | Medium | Pending |
| P1-010 | Create .gitignore | Low | Pending |

#### 12.2.3 Acceptance Criteria
- [ ] Can load video and extract frames
- [ ] Configuration loads from YAML
- [ ] Logging outputs to console with colors
- [ ] Tests pass for video loading

---

### 12.3 Phase 2: Detection (Week 2-3)

#### 12.3.1 Objectives
- Implement ball detection using YOLOv8
- Implement player detection
- Fine-tune ball detection model

#### 12.3.2 Tasks

| Task ID | Task | Priority | Status |
|---------|------|----------|--------|
| P2-001 | Download YOLOv8n pre-trained weights | High | Pending |
| P2-002 | Implement BallDetector base class | High | Pending |
| P2-003 | Implement YOLO inference wrapper | High | Pending |
| P2-004 | Download OpenTTGames test videos | High | Pending |
| P2-005 | Convert OpenTTGames annotations to YOLO format | High | Pending |
| P2-006 | Fine-tune YOLOv8n on ball detection | High | Pending |
| P2-007 | Implement PlayerDetector (COCO person class) | Medium | Pending |
| P2-008 | Add motion blur augmentation to training | Medium | Pending |
| P2-009 | Evaluate detection accuracy on test set | Medium | Pending |
| P2-010 | Optimize batch inference | Low | Pending |

#### 12.3.3 Acceptance Criteria
- [ ] Ball detection >80% mAP on test videos
- [ ] Player detection >90% accuracy
- [ ] Inference <30ms per frame on RTX 4050
- [ ] Works on 24-120 FPS video

---

### 12.4 Phase 3: Tracking (Week 3-4)

#### 12.4.1 Objectives
- Implement Kalman filter tracker
- Handle occlusions gracefully
- Produce smooth trajectories

#### 12.4.2 Tasks

| Task ID | Task | Priority | Status |
|---------|------|----------|--------|
| P3-001 | Implement Kalman filter with filterpy | High | Pending |
| P3-002 | Implement detection-to-track association | High | Pending |
| P3-003 | Implement trajectory data structures | High | Pending |
| P3-004 | Handle track initialization/termination | High | Pending |
| P3-005 | Implement interpolation for missing frames | Medium | Pending |
| P3-006 | Add trajectory smoothing (optional) | Low | Pending |
| P3-007 | Test occlusion handling (up to 10 frames) | Medium | Pending |
| P3-008 | Visualize trajectories for debugging | Low | Pending |

#### 12.4.3 Acceptance Criteria
- [ ] Continuous trajectory through minor occlusions
- [ ] <5 pixel jitter in smooth motion
- [ ] Handles track loss/re-acquisition

---

### 12.5 Phase 4: Segmentation (Week 4)

#### 12.5.1 Objectives
- Detect rally boundaries
- Detect individual shots
- Detect bounces

#### 12.5.2 Tasks

| Task ID | Task | Priority | Status |
|---------|------|----------|--------|
| P4-001 | Implement Event data structures | High | Pending |
| P4-002 | Implement RallyDetector | High | Pending |
| P4-003 | Implement ShotDetector (velocity direction change) | High | Pending |
| P4-004 | Implement BounceDetector | Medium | Pending |
| P4-005 | Integrate player positions for shot attribution | Medium | Pending |
| P4-006 | Implement state machine for event flow | Medium | Pending |
| P4-007 | Test on sample videos | Medium | Pending |
| P4-008 | Tune detection thresholds | Low | Pending |

#### 12.5.3 Acceptance Criteria
- [ ] Rally detection F1 >85%
- [ ] Shot detection aligns with visual hits
- [ ] Events have correct timestamps

---

### 12.6 Phase 5: Physics (Week 5)

#### 12.6.1 Objectives
- Detect table corners
- Compute homography
- Calculate speeds in km/h

#### 12.6.2 Tasks

| Task ID | Task | Priority | Status |
|---------|------|----------|--------|
| P5-001 | Implement TableDetector (edge/corner detection) | High | Pending |
| P5-002 | Implement manual corner annotation fallback | Medium | Pending |
| P5-003 | Implement homography calculation | High | Pending |
| P5-004 | Implement pixel_to_world transformation | High | Pending |
| P5-005 | Implement SpeedCalculator | High | Pending |
| P5-006 | Handle edge cases (ball near frame edge) | Medium | Pending |
| P5-007 | Validate speeds against known references | Medium | Pending |
| P5-008 | Document accuracy limitations | Low | Pending |

#### 12.6.3 Acceptance Criteria
- [ ] Table detected in >80% of videos
- [ ] Manual fallback works smoothly
- [ ] Speed values in reasonable range (0-100 km/h)

---

### 12.7 Phase 6: Visualization (Week 5-6)

#### 12.7.1 Objectives
- Render trajectory trails
- Render speed overlays
- Color-code by speed

#### 12.7.2 Tasks

| Task ID | Task | Priority | Status |
|---------|------|----------|--------|
| P6-001 | Implement TrajectoryRenderer | High | Pending |
| P6-002 | Implement gradient trail with opacity | High | Pending |
| P6-003 | Implement SpeedOverlay | High | Pending |
| P6-004 | Implement color coding (green/yellow/red) | Medium | Pending |
| P6-005 | Implement player bounding box rendering | Low | Pending |
| P6-006 | Implement ARVisualizer orchestrator | High | Pending |
| P6-007 | Optimize rendering performance | Medium | Pending |
| P6-008 | Test visual quality on sample video | Medium | Pending |

#### 12.7.3 Acceptance Criteria
- [ ] Smooth, visually appealing trails
- [ ] Speed text readable and well-positioned
- [ ] Colors correctly reflect speed ranges

---

### 12.8 Phase 7: Dashboard (Week 6-7)

#### 12.8.1 Objectives
- Build Gradio interface
- Integrate all components
- Implement export functionality

#### 12.8.2 Tasks

| Task ID | Task | Priority | Status |
|---------|------|----------|--------|
| P7-001 | Create basic Gradio app structure | High | Pending |
| P7-002 | Implement video upload component | High | Pending |
| P7-003 | Implement processing progress bar | High | Pending |
| P7-004 | Implement video player for annotated output | High | Pending |
| P7-005 | Implement statistics panel | High | Pending |
| P7-006 | Implement rally timeline | Medium | Pending |
| P7-007 | Implement speed chart (Plotly) | Medium | Pending |
| P7-008 | Implement shot table with pagination | Medium | Pending |
| P7-009 | Implement video export | High | Pending |
| P7-010 | Implement CSV export | Medium | Pending |
| P7-011 | Style and polish UI | Low | Pending |
| P7-012 | Add error handling and user feedback | Medium | Pending |

#### 12.8.3 Acceptance Criteria
- [ ] End-to-end flow works (upload → process → view → export)
- [ ] Progress bar updates during processing
- [ ] All stats displayed correctly
- [ ] Exports work and files are valid

---

### 12.9 Phase 8: Polish (Week 7-8)

#### 12.9.1 Objectives
- Comprehensive testing
- Performance optimization
- Documentation

#### 12.9.2 Tasks

| Task ID | Task | Priority | Status |
|---------|------|----------|--------|
| P8-001 | Write unit tests for all modules | High | Pending |
| P8-002 | Write integration tests | High | Pending |
| P8-003 | Test with user's sample video | High | Pending |
| P8-004 | Profile and optimize bottlenecks | Medium | Pending |
| P8-005 | Add GPU memory management | Medium | Pending |
| P8-006 | Write README.md | Medium | Pending |
| P8-007 | Document configuration options | Low | Pending |
| P8-008 | Create user guide | Low | Pending |
| P8-009 | Final bug fixes | High | Pending |
| P8-010 | Tag v1.0.0 release | High | Pending |

#### 12.9.3 Acceptance Criteria
- [ ] All tests pass
- [ ] No critical bugs
- [ ] README complete
- [ ] Works on user's sample video

---

## 13. Risk Assessment

### 13.1 Technical Risks

| Risk | Probability | Impact | Mitigation |
|------|-------------|--------|------------|
| Ball detection fails on motion blur | Medium | High | Blur augmentation in training; fallback to interpolation |
| Table detection fails (unusual angle) | Medium | Medium | Manual corner annotation UI |
| Speed accuracy too low | Medium | Medium | Document limitations; focus on relative comparisons |
| GPU memory issues | Low | Medium | Batch size tuning; frame-by-frame fallback |
| Low FPS video quality | Medium | High | Design for 24 FPS minimum; warn users |

### 13.2 Schedule Risks

| Risk | Probability | Impact | Mitigation |
|------|-------------|--------|------------|
| Dataset download takes too long | Low | Low | Start with test videos only |
| Fine-tuning takes longer than expected | Medium | Medium | Use pre-trained TTNet weights as fallback |
| Gradio complexity | Low | Medium | Start with minimal UI, iterate |

### 13.3 Dependency Risks

| Risk | Probability | Impact | Mitigation |
|------|-------------|--------|------------|
| OpenTTGames unavailable | Low | High | Mirror dataset; use TrackNet as backup |
| Library version conflicts | Medium | Low | Pin all versions; use virtual env |
| CUDA compatibility issues | Low | Medium | Test early; document requirements |

---

## 14. Success Metrics

### 14.1 MVP Success Criteria

| Metric | Target | Priority |
|--------|--------|----------|
| Ball detection accuracy | >80% mAP | Must have |
| Processing speed | <3x video length | Must have |
| Rally detection accuracy | >85% F1 | Should have |
| Speed calculation | <15% error | Should have |
| User can complete full flow | <10 clicks | Must have |

### 14.2 User Satisfaction Metrics (Post-MVP)

| Metric | Target | Measurement |
|--------|--------|-------------|
| Task completion rate | >90% | User testing |
| Processing time acceptable | >80% users | Survey |
| Visualization quality | >4/5 rating | Survey |
| Would recommend | >70% | NPS-style question |

---

## 15. Future Enhancements

### 15.1 Version 2.0 Roadmap

| Feature | Description | Complexity |
|---------|-------------|------------|
| Shot type classification | Detect smash, drop, push, etc. | High |
| Player pose estimation | Analyze stance and technique | High |
| Live/streaming support | Real-time processing | High |
| Multi-camera support | 3D tracking | Very High |
| Score tracking | OCR-based score detection | Medium |
| Cloud deployment | Web-based processing | Medium |

### 15.2 Version 3.0 Roadmap

| Feature | Description | Complexity |
|---------|-------------|------------|
| Spin detection | High-speed camera required | Very High |
| Mobile app | iOS/Android companion | High |
| Coaching AI | Shot recommendation system | Very High |
| Tournament mode | Multi-match analysis | Medium |

---

## 16. Feature Tracker

### 16.1 MVP Features

| ID | Feature | Module | Priority | Status | Notes |
|----|---------|--------|----------|--------|-------|
| F001 | Video upload (MP4) | Input | P0 | Pending | |
| F002 | Frame extraction | Input | P0 | Pending | |
| F003 | Ball detection (YOLOv8) | Detection | P0 | Pending | |
| F004 | Player detection | Detection | P1 | Pending | |
| F005 | Kalman tracking | Tracking | P0 | Pending | |
| F006 | Occlusion handling | Tracking | P1 | Pending | |
| F007 | Table detection | Physics | P0 | Pending | |
| F008 | Homography calibration | Physics | P0 | Pending | |
| F009 | Speed calculation | Physics | P0 | Pending | |
| F010 | Rally detection | Segmentation | P0 | Pending | |
| F011 | Shot detection | Segmentation | P0 | Pending | |
| F012 | Bounce detection | Segmentation | P1 | Pending | |
| F013 | Trajectory trail | Visualization | P0 | Pending | |
| F014 | Speed overlay | Visualization | P0 | Pending | |
| F015 | Color coding | Visualization | P1 | Pending | |
| F016 | Gradio UI | Dashboard | P0 | Pending | |
| F017 | Video player | Dashboard | P0 | Pending | |
| F018 | Rally timeline | Dashboard | P1 | Pending | |
| F019 | Speed chart | Dashboard | P1 | Pending | |
| F020 | Shot table | Dashboard | P1 | Pending | |
| F021 | Video export | Export | P0 | Pending | |
| F022 | CSV export | Export | P1 | Pending | |

### 16.2 Feature Priority Legend

| Priority | Meaning |
|----------|---------|
| P0 | Must have for MVP |
| P1 | Should have for MVP |
| P2 | Nice to have for MVP |
| P3 | Future version |

---

## 17. Implementation Log

### 17.1 Log Format

```
| Date | Phase | Task ID | Description | Outcome | Notes |
|------|-------|---------|-------------|---------|-------|
```

### 17.2 Implementation History

| Date | Phase | Task ID | Description | Outcome | Notes |
|------|-------|---------|-------------|---------|-------|
| 2026-01-21 | 0 | - | PRD Created | Complete | v1.0.0 |
| | | | | | |

---

## 18. Decision Log

### 18.1 Log Format

```
| Date | Decision | Options Considered | Rationale | Impact |
|------|----------|-------------------|-----------|--------|
```

### 18.2 Decision History

| Date | Decision | Options Considered | Rationale | Impact |
|------|----------|-------------------|-----------|--------|
| 2026-01-21 | Use Gradio for UI | Streamlit, Gradio, Custom | Better ML integrations, video handling | Dashboard design |
| 2026-01-21 | Target 24+ FPS | 30+, 60+, 24+ | User has cinematic footage | Detection approach |
| 2026-01-21 | Single camera only | Single, Multi | Hardware simplicity | Physics accuracy limitations |
| 2026-01-21 | YOLOv8 for detection | YOLOv8, TrackNet, Custom | Balance of speed and accuracy | Model architecture |
| 2026-01-21 | Auto-segmentation | Manual, Auto, Both | Better UX, richer analytics | Scope increase |
| 2026-01-21 | Include player detection | Ball only, Ball + Player | Improves shot attribution | Slight complexity increase |
| 2026-01-21 | Start with test dataset | Full, Test only | Faster prototyping | May need full dataset later |

---

## 19. Open Questions

| ID | Question | Status | Owner | Resolution |
|----|----------|--------|-------|------------|
| Q001 | What is the FPS of user's sample video? | Open | Dev | Inspect video metadata |
| Q002 | Is RTX 4050 6GB VRAM sufficient for YOLOv8? | Open | Dev | Test during Phase 2 |
| Q003 | Exact OpenTTGames download procedure? | Open | Dev | Test download script |
| Q004 | Audio preservation in export needed? | Open | User | TBD |

---

## 20. Appendix

### 20.1 Reference Links

| Resource | URL |
|----------|-----|
| OpenTTGames Dataset | https://lab.osai.ai/ |
| TTNet Paper | https://arxiv.org/abs/2004.09927 |
| YOLOv8 Documentation | https://docs.ultralytics.com/ |
| Gradio Documentation | https://www.gradio.app/docs |
| OpenCV Documentation | https://docs.opencv.org/ |
| filterpy (Kalman) | https://filterpy.readthedocs.io/ |

### 20.2 Table Tennis Specifications

| Dimension | Value |
|-----------|-------|
| Table length | 2.74 m (9 ft) |
| Table width | 1.525 m (5 ft) |
| Table height | 0.76 m (2.5 ft) |
| Net height | 0.1525 m (6 in) |
| Ball diameter | 40 mm |
| Ball weight | 2.7 g |

### 20.3 Speed Reference (Professional Play)

| Shot Type | Typical Speed |
|-----------|---------------|
| Push/block | 10-30 km/h |
| Drive | 30-50 km/h |
| Loop | 40-70 km/h |
| Smash | 60-100+ km/h |
| Serve | 20-60 km/h |

### 20.4 Glossary

| Term | Definition |
|------|------------|
| **Rally** | Continuous play from serve until point scored |
| **Shot** | Single stroke by a player |
| **Bounce** | Ball contact with table surface |
| **Homography** | Transformation between 2D image plane and world plane |
| **Kalman Filter** | Algorithm for estimating state from noisy measurements |
| **mAP** | Mean Average Precision - detection accuracy metric |
| **NMS** | Non-Maximum Suppression - removes duplicate detections |
| **Occlusion** | Object hidden from view (by player, etc.) |

---

## Document Approval

| Role | Name | Date | Signature |
|------|------|------|-----------|
| Product Owner | rogit | | Pending |
| Developer | OpenCode | 2026-01-21 | ✓ |

---

*End of PRD v1.0.0*
