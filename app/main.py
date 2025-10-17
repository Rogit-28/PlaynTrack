from fastapi import FastAPI, Depends
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session
import cv2
from ultralytics import YOLO
import numpy as np
from sort.sort import Sort

# Project imports
from database import SessionLocal, init_db, get_db
from models import TrackedObject

app = FastAPI(title="PlaynTrack API")

@app.on_event("startup")
def on_startup():
    init_db()

# Load the YOLOv8 model
model = YOLO('yolov8n.pt')

# Initialize SORT tracker
tracker = Sort()

# Store tracker history (in-memory, for trajectory drawing)
tracked_objects_history = {}

# --- Constants for Speed Calculation ---
VIDEO_WIDTH = 1280
TABLE_TENNIS_TABLE_WIDTH_METERS = 2.74
PIXELS_PER_METER = VIDEO_WIDTH / TABLE_TENNIS_TABLE_WIDTH_METERS
FPS = 30

def video_processing_generator(db: Session):
    """
    Generator function to process video, detect & track the ball, and stream frames.
    Saves tracking data to the database.
    """
    video_path = 'data/video.mp4'
    cap = cv2.VideoCapture(video_path)

    if not cap.isOpened():
        print(f"Error: Could not open video {video_path}")
        return

    while True:
        success, frame = cap.read()
        if not success:
            cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
            continue

        results = model(frame, classes=[32], verbose=False)

        detections = []
        for r in results:
            for box in r.boxes:
                x1, y1, x2, y2 = box.xyxy[0].cpu().numpy()
                conf = box.conf[0].cpu().numpy()
                detections.append([x1, y1, x2, y2, conf])

        detections_np = np.array(detections)
        tracked_results = tracker.update(detections_np)

        for res in tracked_results:
            x1, y1, x2, y2, track_id = map(int, res)
            center_x, center_y = (x1 + x2) // 2, (y1 + y2) // 2

            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
            cv2.putText(frame, f"ID: {track_id}", (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

            speed_mps = 0
            if track_id in tracked_objects_history:
                prev_center, prev_trajectory = tracked_objects_history[track_id]
                pixel_distance = np.linalg.norm(np.array([center_x, center_y]) - np.array(prev_center))
                speed_pps = pixel_distance * FPS
                speed_mps = speed_pps / PIXELS_PER_METER

                new_trajectory = prev_trajectory + [(center_x, center_y)]
                if len(new_trajectory) > 30: new_trajectory.pop(0)
                tracked_objects_history[track_id] = ((center_x, center_y), new_trajectory)
            else:
                tracked_objects_history[track_id] = ((center_x, center_y), [(center_x, center_y)])

            # --- Database Persistence ---
            db_object = TrackedObject(
                track_id=track_id,
                x_coordinate=center_x,
                y_coordinate=center_y,
                speed_mps=speed_mps
            )
            db.add(db_object)
            db.commit()

            trajectory = tracked_objects_history[track_id][1]
            for i in range(1, len(trajectory)):
                cv2.line(frame, trajectory[i-1], trajectory[i], (0, 255, 255), 2)

            cv2.putText(frame, f"Speed: {speed_mps:.2f} m/s", (x1, y2 + 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)

        ret, buffer = cv2.imencode('.jpg', frame)
        if not ret: continue
        frame_bytes = buffer.tobytes()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')

@app.get("/")
def read_root():
    return {"message": "Welcome to the PlaynTrack API. Go to /stream for the video feed."}

@app.get("/stream")
def stream_video(db: Session = Depends(get_db)):
    return StreamingResponse(video_processing_generator(db=db), media_type='multipart/x-mixed-replace; boundary=frame')

@app.get("/api/latest_metrics")
def get_latest_metrics(db: Session = Depends(get_db)):
    """
    Endpoint to get the most recent metrics for the tracked object.
    """
    latest_entry = db.query(TrackedObject).order_by(TrackedObject.timestamp.desc()).first()
    if latest_entry:
        return {
            "track_id": latest_entry.track_id,
            "speed_mps": latest_entry.speed_mps,
            "timestamp": latest_entry.timestamp
        }
    return {"message": "No tracking data available yet."}