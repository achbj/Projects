import cv2

def extract_frames(video_path):
    cap = cv2.VideoCapture(video_path)
    frames = []

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
        frames.append(frame)

    cap.release()
    if not frames:
        print("No frames extracted from the video.")
    return frames

def process_frames_and_reconstruct(frames, output_video_path):
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

    # Assuming all frames have the same size
    height, width, layers = frames[0].shape
    size = (width, height)
    fps = 25  # You can modify this based on your video's FPS

    out = cv2.VideoWriter(output_video_path, cv2.VideoWriter_fourcc(*'mp4v'), fps, size)

    if not out.isOpened():
        print("Failed to open video writer.")
        return

    for frame in frames:
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, 1.1, 4)

        for (x, y, w, h) in faces:
            cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)

        out.write(frame)
    out.release()
    print("Video processing complete, file saved to", output_video_path)

    out.release()
