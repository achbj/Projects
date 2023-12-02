import cv2
import os
import dlib
import numpy as np
from scipy.spatial.distance import euclidean

# Initialize Dlib's face detector and facial landmark predictor
detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor('shape_predictor_68_face_landmarks.dat')
face_rec_model = dlib.face_recognition_model_v1('dlib_face_recognition_resnet_model_v1.dat')

def extract_face_encoding(image_path):
    try:
      if not os.path.exists(image_path):
          print(f"File not found: {image_path}")
          return None
      image = cv2.imread(image_path)
      print(f"Image loaded: {image is not None}")

      gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
      faces = detector(gray, 1)

      print(f"Number of faces detected: {len(faces)}")

      if len(faces) > 0:
          face = faces[0]
          shape = predictor(gray, face)
          face_encoding = np.array(face_rec_model.compute_face_descriptor(image, shape))
          return face_encoding
      else:
          return None
    except Exception as e:
        print(f"Error during processing: {e}")
        return None
    

def generate_frames(video_path, face_encoding, person_name):
    cap = cv2.VideoCapture(video_path)

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = detector(gray, 1)

        for face in faces:
            shape = predictor(gray, face)
            current_face_encoding = np.array(face_rec_model.compute_face_descriptor(frame, shape))

            # Compare the face encoding with the reference encoding
            if euclidean(face_encoding, current_face_encoding) < 0.6:  # Threshold for recognition
                # Draw rectangle and put name on the frame
                cv2.rectangle(frame, (face.left(), face.top()), (face.right(), face.bottom()), (0, 255, 0), 2)
                cv2.putText(frame, person_name, (face.left() + 6, face.bottom() - 6), cv2.FONT_HERSHEY_SIMPLEX, 1.0, (255, 255, 255), 1)

        # Encoding the processed frame
        ret, buffer = cv2.imencode('.jpg', frame)
        frame = buffer.tobytes()

        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

    cap.release()
