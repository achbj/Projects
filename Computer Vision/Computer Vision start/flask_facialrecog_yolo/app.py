from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['PROCESSED_FOLDER'] = 'static/processed'

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/object-detection', methods=['GET', 'POST'])
def object_detection():
    if request.method == 'POST':
        # Handle video upload and processing for object detection
        pass
    return render_template('object_detection.html')

@app.route('/people-detection', methods=['GET', 'POST'])
def people_detection():
    if request.method == 'POST':
        # Handle video upload and processing for people detection
        pass
    return render_template('people_detection.html')

@app.route('/face-recognition', methods=['GET', 'POST'])
def face_recognition():
    if request.method == 'POST':
        # Handle video upload and processing for face recognition
        pass
    return render_template('face_recognition.html')

if __name__ == '__main__':
    app.run(debug=True)
