from flask import Flask, request, render_template, redirect, url_for
import os
from video_processor import process_video

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads/'
app.config['PROCESSED_FOLDER'] = 'static/processed/'

os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
os.makedirs(app.config['PROCESSED_FOLDER'], exist_ok=True)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_files():
    if 'image' in request.files and 'video' in request.files:
        image_file = request.files['image']
        video_file = request.files['video']
        person_name = request.form['person_name']

        image_path = os.path.join(app.config['UPLOAD_FOLDER'], image_file.filename)
        video_path = os.path.join(app.config['UPLOAD_FOLDER'], video_file.filename)
        processed_video_filename = 'processed_' + video_file.filename
        processed_video_path = os.path.join(app.config['PROCESSED_FOLDER'], processed_video_filename)

        image_file.save(image_path)
        video_file.save(video_path)

        process_video(video_path, processed_video_path, image_path, person_name)
        
        return redirect(url_for('display_video', filename=processed_video_filename))

    return "File not uploaded", 400

@app.route('/video/<filename>')
def display_video(filename):
    return render_template('display_video.html', filename=filename)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8100)
