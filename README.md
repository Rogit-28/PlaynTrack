# PlaynTrack - Live Sports Analytics

## Vision

PlaynTrack is a real-time sports analytics platform that automatically processes video feeds to detect and track players and objects, calculate key performance metrics, and visualize the data. This MVP focuses on table tennis, providing real-time ball tracking and speed calculation on a local dashboard.

## System Architecture

The application is containerized using Docker and consists of three main services:

1.  **Backend (FastAPI):** Handles the core computer vision tasks. It ingests a video, uses a YOLOv8 model for ball detection, the SORT algorithm for tracking, calculates speed, and saves the data to PostgreSQL. It streams the processed video and exposes a REST API for metrics.
2.  **Frontend (Streamlit):** A web-based dashboard that displays the live processed video feed from the backend and shows key performance metrics like ball speed in real-time.
3.  **Database (PostgreSQL):** A persistent storage for all analytics data, such as object coordinates and calculated speed.

## How to Run

This project is designed for a local-first execution to be simple and cost-effective.

### Prerequisites

*   Docker and Docker Compose must be installed on your machine.

### Running the Application

1.  **Clone the repository:**
    ```bash
    git clone <repository-url>
    cd <repository-name>
    ```

2.  **Build and run the services:**
    From the root of the project directory, run the following command:
    ```bash
    docker-compose up --build
    ```
    This command will build the Docker images for the backend and frontend services and start all three containers (`backend`, `frontend`, `db`).

3.  **View the Dashboard:**
    Once the containers are running, open your web browser and navigate to:
    ```
    http://localhost:8501
    ```
    You should see the live dashboard with the processed video feed and real-time metrics.

4.  **Stopping the Application:**
    To stop the application, press `Ctrl+C` in the terminal where `docker-compose` is running, and then run:
    ```bash
    docker-compose down
    ```

## Technology Stack

*   **Core:** Python, FastAPI, OpenCV, FFmpeg, YOLOv8, SORT, PostgreSQL
*   **Frontend:** Streamlit
*   **Deployment:** Docker, Docker Compose