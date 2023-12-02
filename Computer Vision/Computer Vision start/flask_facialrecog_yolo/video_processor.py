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

def get_face_embedding(image):
    # Convert to PIL Image
    pil_image = Image.fromarray(image)

    # Detect faces in the image
    boxes, _ = mtcnn.detect(pil_image)

    # If no faces are detected
    if boxes is None:
        return None, None

    # Extract the first face
    face = boxes[0]
    face_cropped = pil_image.crop((face[0], face[1], face[2], face[3]))

    # Transform the face for the model
    face_transformed = mtcnn(face_cropped)

    # Get the face embedding
    face_embedding = resnet(face_transformed.unsqueeze(0).to(device))

    return face_embedding, face

def process_video(input_video_path, output_video_path, face_image_path, person_name):
    # Load YOLOv5 model
    yolo_model = YOLOv5("yolov5s.pt", device="cpu")

    # Read the face image and get its embedding
    face_image = cv2.imread(face_image_path)
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

        if frame_embedding is not None:
            if torch.dist(face_embedding, frame_embedding) < 0.8:  # Threshold value
                x, y, w, h = int(box[0]), int(box[1]), int(box[2]), int(box[3])
                cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
                cv2.putText(frame, person_name, (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

        # YOLO object detection
        results = yolo_model.predict(frame)
        frame = yolo_model.annotate(frame, results)

        # Write the processed frame
        out.write(frame)

    cap.release()
    out.release()

