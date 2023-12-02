from flask import Flask, request, render_template, Response
import os
import face_recognizer  # Your custom module for face recognition
from face_recognizer import extract_face_encoding, generate_frames

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads/'

# Check if the uploads directory exists, and create it if it doesn't
if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_files():
    if request.method == 'POST':
        # Receive the files and the person's name from the form
        image_file = request.files['image']
        video_file = request.files['video']
        person_name = request.form['name']

        # Save the files in the UPLOAD_FOLDER
        image_path = os.path.join(app.config['UPLOAD_FOLDER'], image_file.filename)
        video_path = os.path.join(app.config['UPLOAD_FOLDER'], video_file.filename)

        print(f"Image path: {image_path}")
        print(f"Video path: {video_path}")

        image_file.save(image_path)
        video_file.save(video_path)

        # Process the files
        face_encoding = extract_face_encoding(image_path)
        print(f"Face encoding: {face_encoding is not None}")
        if face_encoding is not None:
            if face_encoding is not None:
                return Response(generate_frames(video_path, face_encoding, person_name),
                                mimetype='multipart/x-mixed-replace; boundary=frame')
            else:
                return "No face detected in the image or failed to process the image.", 400

        else:
            return "No face detected in the image or failed to process the image.", 400

        
    return "Invalid request", 400

if __name__ == '__main__':
    app.run(debug=True)
