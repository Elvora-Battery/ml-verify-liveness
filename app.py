import os
from flask import Flask, request, jsonify
from google.cloud import vision
from google.oauth2 import service_account

# Inisialisasi Flask app
app = Flask(__name__)

# Set up credentials (path to your service account key)
credentials = service_account.Credentials.from_service_account_file('json-key-file')
client = vision.ImageAnnotatorClient(credentials=credentials)

@app.route('/detect_liveness', methods=['POST'])
def detect_liveness():
    if 'file' not in request.files:
        return jsonify({"error": "No file uploaded"}), 400
    
    file = request.files['file']
    content = file.read()
    
    image = vision.Image(content=content)
    response = client.face_detection(image=image)

    # Check if faces are detected
    faces = response.face_annotations
    if not faces:
        return jsonify({"error": "No face detected"}), 400

    results = []
    for face in faces:
        face_data = {
            "joy_likelihood": face.joy_likelihood,
            "sorrow_likelihood": face.sorrow_likelihood,
            "anger_likelihood": face.anger_likelihood,
            "surprise_likelihood": face.surprise_likelihood,
            "head_tilt_angle": face.roll_angle,
            "smile_detected": face.joy_likelihood >= 3  # Joy likelihood >= "LIKELY"
        }
        results.append(face_data)

    if response.error.message:
        raise Exception(f'{response.error.message}')

    return jsonify(results)

if __name__ == '__main__':
    app.run(debug=True)
