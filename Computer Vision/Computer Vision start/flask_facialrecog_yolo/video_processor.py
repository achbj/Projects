import cv2
from facenet_pytorch import MTCNN, InceptionResnetV1
import torch
from yolov5 import YOLOv5
from PIL import Image

device = torch.device('cuda:0' if torch.cuda.is_available() else 'cpu')

# Initialize MTCNN for face detection
mtcnn = MTCNN(keep_all=True, device=device)

# Initialize InceptionResnetV1 for face recognition
resnet = InceptionResnetV1(pretrained='vggface2').eval().to(device)

# Load the YOLOv5 model
yolo_model = torch.hub.load('ultralytics/yolov5', 'yolov5s', pretrained=True)
yolo_model.eval().to(device)

def get_face_embedding(image):
    # Convert to RGB as MTCNN expects RGB images
    image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    # Detect faces
    boxes, _ = mtcnn.detect(image_rgb)

    if boxes is None:
        print("No faces detected.")
        return None, None

    # Extract the first detected face (for simplicity)
    box = boxes[0].astype(int)
    face = image_rgb[box[1]:box[3], box[0]:box[2]]

    # You can add face recognition/embedding code here

    return face, box

def process_video(input_video_path, output_video_path, face_image_path, person_name):
    # Load YOLOv5 model
    # yolo_model = YOLOv5("yolov5s.pt", device="cpu")

    # Read the face image and get its embedding
    face_image = cv2.imread(face_image_path)
    if face_image is None:
      print('----------------------------')
      print(f"Failed to load image from {face_image_path}")
      return
    face_embedding, _ = get_face_embedding(face_image)

    if face_embedding is None:
        print("No face detected in the reference image.")
        return

    cap = cv2.VideoCapture(input_video_path)
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = cap.get(cv2.CAP_PROP_FPS)

    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(output_video_path, fourcc, fps, (width, height))

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        # Face detection and recognition
        frame_embedding, box = get_face_embedding(frame)

        if frame_embedding is not None and torch.dist(face_embedding, frame_embedding) < 0.8:  # Threshold
            x, y, w, h = int(box[0]), int(box[1]), int(box[2]), int(box[3])
            cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
            cv2.putText(frame, person_name, (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

        # YOLO object detection
        results = yolo_model(frame)
        for result in results.xyxy[0]:  # Iterate over detections
            xmin, ymin, xmax, ymax, confidence, class_id = result
            label = f"{yolo_model.names[int(class_id)]}: {confidence:.2f}"
            cv2.rectangle(frame, (int(xmin), int(ymin)), (int(xmax), int(ymax)), (0, 0, 255), 2)
            cv2.putText(frame, label, (int(xmin), int(ymin - 10)), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)

        # Write the processed frame
        out.write(frame)

    cap.release()
    out.release()


