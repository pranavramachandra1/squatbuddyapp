from flask import Blueprint, request, jsonify
import os
import tempfile

from .services import process_video

main = Blueprint('main', __name__)

@main.route('/upload', methods=['POST'])
def upload_video():
    if 'video' not in request.files:
        return jsonify({"error": "No video file provided"}), 400

    video_file = request.files['video']
    
    # Create a temporary file that will hold the uploaded video.
    # Using delete=False allows us to pass the file path to cv2.VideoCapture.
    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp4") as temp_video:
        video_file.save(temp_video.name)
        temp_path = temp_video.name

    try:
        # Pass the temporary file path to your video processing function.
        result = process_video(temp_path)
        return jsonify({"message": result})
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        # Ensure the temporary file is removed after processing.
        os.remove(temp_path)
