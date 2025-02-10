import os
import cv2
import requests
import numpy as np
import base64
from openai import OpenAI
import google.generativeai as genai
from dotenv import load_dotenv
from pathlib import Path

from .prompts import *

# model service endpoint:
endpoint_url = "https://squatbuddymodel-492294139533.us-central1.run.app/predict_batch"

# gemini:
model = genai.GenerativeModel(model_name="gemini-1.5-flash")

client = OpenAI(
    api_key=os.environ.get("OPENAI_API_KEY"),
)

def process_video(path: str):

    # Extract frames from video
    results = _extract_frame_data(path)

    # Generate feedback based on results
    feedback = _generate_feedback(results)

    return feedback

def _extract_frame_data(path: str, batch_size=10, sample_rate=3):
    """
    Extracts frames from a video, sampling at a defined interval,
    batches them, and sends to API.
    
    Args:
        path (str): Path to video file
        batch_size (int): Number of frames per request
        sample_rate (int): Process only 1 frame out of every 'sample_rate' frames.
    """
    print("Starting batch processing...")

    vidcap = cv2.VideoCapture(path)
    success, image = vidcap.read()
    
    results = np.zeros(8)
    batch = []
    frame_count = 0

    while success:
        # Only process frames if they meet the sampling condition
        if frame_count % sample_rate == 0:
            # Preprocess frame
            image = _correct_rotation(image, path)

            # Convert to bytes
            _, buffer = cv2.imencode(".jpg", image)
            image_bytes = buffer.tobytes()
            batch.append(image_bytes)

            # Send batch when full
            if len(batch) == batch_size:
                response = _send_batch(batch)
                results += response
                batch = []  # Reset batch

        success, image = vidcap.read()
        frame_count += 1

    # Send remaining frames
    if batch:
        response = _send_batch(batch)
        results+=response

    vidcap.release()
    print("Batch processing complete!")
    return results

def _correct_rotation(image, path):
    """Rotates the image if the video contains EXIF rotation metadata."""
    vidcap = cv2.VideoCapture(path)
    rotate_code = None

    rotation_flag = vidcap.get(cv2.CAP_PROP_ORIENTATION_META)

    if rotation_flag == 90:
        rotate_code = cv2.ROTATE_90_CLOCKWISE
    elif rotation_flag == 180:
        rotate_code = cv2.ROTATE_180
    elif rotation_flag == 270:
        rotate_code = cv2.ROTATE_90_COUNTERCLOCKWISE

    if rotate_code is not None:
        image = cv2.rotate(image, rotate_code)

    return image

def _send_batch(batch):
    """Sends a batch of images to the API (JSON with base64-encoded frames)."""
    headers = {"Content-Type": "application/json"}
    json_data = {"frames": [base64.b64encode(img).decode() for img in batch]}

    response = requests.post(endpoint_url, json=json_data, headers=headers)
    if response.status_code == 200:
        return _process_response(response.json())
    else:
        return []

def _process_response(response):
    
    formatted_results = np.zeros(8)

    for vector in response.get("predictions", []):
        # Extract the class label and confidence from the prediction
        formatted_results += np.array(vector[0])

    return formatted_results

def _generate_feedback(results, prompt = FEEDBACK_PROMPT):

    prompt = get_prompt(results, prompt)

    response = model.generate_content([prompt])

    return response.text