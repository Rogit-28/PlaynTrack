# Future Features & Improvements

This file tracks features and improvements that are planned or were discussed for future versions of the PlaynTrack application.

## High Priority

*   **Fine-Tune YOLO Model:**
    *   Create a custom dataset of table tennis gameplay.
    *   Fine-tune the YOLOv8 model on this dataset to accurately detect not just the ball, but also the **paddles**. This is the most critical next step for improving detection accuracy and enabling more advanced analytics.

*   **Advanced Camera Calibration:**
    *   Implement a proper camera calibration process. This would involve using a calibration pattern (like a checkerboard) to determine the camera's intrinsic and extrinsic parameters.
    *   This will allow for a much more accurate conversion from pixel distances to real-world units (meters, cm), removing the dependency on a fixed camera angle and the simple "pixels-per-meter" approximation.

## Medium Priority

*   **Player Detection:**
    *   Extend the model to detect and track players. This would enable player-specific metrics.

*   **Post-Match Analysis Dashboard:**
    *   Create a separate dashboard view for post-match analysis.
    *   Display aggregated statistics, heatmaps of ball placement, rally length analysis, and other insights derived from the stored database data.

*   **Real Video Input:**
    *   Once the core logic is robust, switch from the synthetic video to handling real-world video files or live camera feeds. This will require more robust error handling for different lighting conditions and camera angles.

## Low Priority

*   **Multi-Camera Support:**
    *   Extend the system to ingest and synchronize feeds from multiple cameras for 3D trajectory reconstruction.
*   **AI Commentary:**
    *   Integrate a Large Language Model (LLM) to generate real-time commentary based on the game events detected.