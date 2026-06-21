# AI-Based Road Accident Detection and Emergency Response System

A professional Flask dashboard for real-time smart traffic surveillance, YOLOv8 vehicle detection, hybrid accident alerting, timestamped snapshot capture, and exhibition-ready project demonstrations.

## Features

- Live server webcam monitoring with OpenCV MJPEG streaming.
- Browser webcam frame processing through `/api/detect_frame`.
- Video upload and processed playback.
- YOLOv8 vehicle detection for cars, motorcycles, buses, trucks, bicycles, and related classes.
- Automatic use of `models/accident.pt` when a custom accident model is available.
- Hybrid accident heuristic for demos when only a general YOLO vehicle model is present.
- Blinking warning state, confidence score, AM/PM time, alert sound, vehicle counters, chart, and snapshot preview.
- Timestamped accident snapshots in `static/captures/`.
- JSONL event log in `logs/accident_events.jsonl`.

## Project Structure

```text
.
├── app.py
├── requirements.txt
├── README.md
├── models/
│   └── accident.pt              # optional custom trained YOLOv8 accident model
├── services/
│   ├── __init__.py
│   ├── detector.py
│   └── video_stream.py
├── static/
│   ├── captures/
│   ├── css/styles.css
│   └── js/dashboard.js
├── templates/
│   └── index.html
├── uploads/
└── logs/
```

## Setup

Install Python 3.10 or newer, then run:

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
python app.py
```

Open:

```text
http://127.0.0.1:5000
```

On the first run with the default `yolov8n.pt`, Ultralytics may download the YOLOv8 weights. For offline demonstrations, place a valid YOLOv8 model file in `models/accident.pt` or set `YOLO_MODEL` to a local `.pt` file.

## Configuration

Environment variables:

```text
YOLO_MODEL=yolov8n.pt
YOLO_CONFIDENCE=0.35
ACCIDENT_DEMO_SENSITIVITY=0.62
SNAPSHOT_COOLDOWN_SECONDS=8
```

## Custom Accident Model

Train a YOLOv8 model with accident-related classes such as `accident`, `crash`, `collision`, or `road_accident`, then save it here:

```text
models/accident.pt
```

The backend automatically prefers this file over the default model.

## Notes for Demonstration

- Use **Server Cam** when the Flask machine has a webcam.
- Use **Browser Cam** when the browser should capture frames and send them to Flask.
- Use **Upload Video** for reliable exhibition demos with prepared traffic footage.
- Accident snapshots are rate-limited so one event does not create repeated duplicate captures.
