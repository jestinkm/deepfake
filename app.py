from flask import Flask, request, jsonify
from flask_cors import CORS  # Import CORS
import cv2
import numpy as np
import face_recognition
import subprocess
import base64
import os

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

KNOWN_FACE = "gi.jpeg"  # Path to your known reference face image
PRIVATE_FOLDER = r"C:\fashion"  # Path to the private folder

# Load the known face image and encode it
known_image = face_recognition.load_image_file(KNOWN_FACE)
known_encoding = face_recognition.face_encodings(known_image)[0]

folder_open = False  # This will track whether the folder is open or closed

def open_folder():
    subprocess.Popen(["explorer", PRIVATE_FOLDER], shell=True)

def close_folder():
    os.system("taskkill /IM explorer.exe /F")  # Close any opened explorer windows
    os.system("start explorer")  # Re-open explorer to reset it

@app.route('/check_face', methods=['POST'])
def check_face():
    global folder_open  # Ensure we are modifying the global folder_open variable
    data = request.json
    image_data = data['image']

    try:
        # Convert base64 image to OpenCV format
        img = base64.b64decode(image_data)
        np_arr = np.frombuffer(img, np.uint8)
        frame = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)

        if frame is None:
            return jsonify({"status": "error", "message": "Failed to decode the image!"})

        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        # Detect faces in the image
        face_locations = face_recognition.face_locations(rgb_frame)
        face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)

        if len(face_encodings) == 0:
            return jsonify({"status": "no_faces", "message": "No faces found in the image."})

        found = False
        for encoding in face_encodings:
            matches = face_recognition.compare_faces([known_encoding], encoding)
            if True in matches:
                found = True
                break

        if found and not folder_open:
            open_folder()
            folder_open = True
            return jsonify({"status": "opened", "message": "Folder is opened!"})

        if not found and folder_open:
            close_folder()
            folder_open = False
            return jsonify({"status": "closed", "message": "Folder is closed!"})

        return jsonify({"status": "unchanged", "message": "No change!"})

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})

if __name__ == '__main__':
    app.run(debug=True)
