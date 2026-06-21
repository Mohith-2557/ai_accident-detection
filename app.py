from __future__ import annotations

import os
from pathlib import Path

from flask import Flask, jsonify, render_template, request, Response
from werkzeug.utils import secure_filename

from services.detector import RoadAccidentDetector
from services.video_stream import VideoStreamManager


BASE_DIR = Path(__file__).resolve().parent
ALLOWED_VIDEO_EXTENSIONS = {".mp4", ".avi", ".mov", ".mkv", ".webm"}

app = Flask(__name__)
app.config["MAX_CONTENT_LENGTH"] = 300 * 1024 * 1024
app.config["UPLOAD_FOLDER"] = BASE_DIR / "uploads"

detector = RoadAccidentDetector(
    model_dir=BASE_DIR / "models",
    capture_dir=BASE_DIR / "static" / "captures",
    log_dir=BASE_DIR / "logs",
)
streams = VideoStreamManager(detector, upload_dir=app.config["UPLOAD_FOLDER"])


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/video_feed")
def video_feed():
    return Response(
        streams.camera_frames(),
        mimetype="multipart/x-mixed-replace; boundary=frame",
    )


@app.route("/video_feed/upload/<source_id>")
def uploaded_video_feed(source_id: str):
    return Response(
        streams.upload_frames(source_id),
        mimetype="multipart/x-mixed-replace; boundary=frame",
    )


@app.route("/api/upload", methods=["POST"])
def upload_video():
    file = request.files.get("video")
    if file is None or not file.filename:
        return jsonify({"error": "No video file was provided"}), 400

    filename = secure_filename(file.filename)
    suffix = Path(filename).suffix.lower()
    if suffix not in ALLOWED_VIDEO_EXTENSIONS:
        return jsonify({"error": "Unsupported video format"}), 400

    file.filename = filename
    source_id = streams.register_upload(file)
    return jsonify({
        "source_id": source_id,
        "stream_url": f"/video_feed/upload/{source_id}",
        "message": "Video uploaded successfully",
    })


@app.route("/api/detect_frame", methods=["POST"])
def detect_frame():
    payload = request.get_json(silent=True) or {}
    frame = payload.get("frame")
    if not frame:
        return jsonify({"error": "Missing base64 frame"}), 400
    try:
        result = detector.process_base64_frame(frame)
    except ValueError as exc:
        return jsonify({"error": str(exc)}), 400
    return jsonify(result)


@app.route("/api/status")
def status():
    return jsonify(detector.get_state())


@app.errorhandler(413)
def upload_too_large(_error):
    return jsonify({"error": "Upload is too large. Please use a video below 300 MB."}), 413


if __name__ == "__main__":
    debug = os.getenv("FLASK_DEBUG", "0") == "1"
    app.run(host="0.0.0.0", port=5000, debug=debug, threaded=True)
