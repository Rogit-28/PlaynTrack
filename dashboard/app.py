import streamlit as st
import requests
import time

st.set_page_config(page_title="PlaynTrack Live Dashboard", layout="wide")

st.title("PlaynTrack - Live Sports Analytics")

st.header("Live Video Feed")
# The video stream from the backend will be displayed here.
st.image("http://backend:8000/stream", use_column_width=True)

st.header("Live Metrics")
speed_placeholder = st.empty()

# Continuously update metrics
while True:
    try:
        response = requests.get("http://backend:8000/api/latest_metrics", timeout=1)
        if response.status_code == 200:
            metrics = response.json()
            if "speed_mps" in metrics:
                speed_kph = metrics["speed_mps"] * 3.6
                speed_placeholder.metric(label="Ball Speed", value=f"{speed_kph:.2f} km/h")
            else:
                speed_placeholder.metric(label="Ball Speed", value="N/A")
        else:
            speed_placeholder.metric(label="Ball Speed", value="Error")
    except requests.exceptions.RequestException as e:
        speed_placeholder.metric(label="Ball Speed", value="Connecting...")

    time.sleep(0.5) # Refresh rate for metrics