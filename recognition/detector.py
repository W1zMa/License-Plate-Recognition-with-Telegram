import cv2
from ultralytics import YOLO


# Map character classes to actual characters
character_map = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 
                    'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 
                    'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 
                    'U', 'V', 'W', 'X', 'Y', 'Z']

# Load YOLOv8 models
license_plate_model = YOLO("weights/detection.pt")  # Replace with your license plate model
character_model = YOLO("weights/recognition.pt")          # Replace with your character model

# Open video or camera
def process_video(video_path: str):
    cap = cv2.VideoCapture(video_path)
    found_numbers = []

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        plates = license_plate_model(frame)

        for plate in plates[0].boxes:
            x1, y1, x2, y2 = map(int, plate.xyxy[0])
            cropped = frame[y1:y2, x1:x2]

            characters = character_model(cropped)
            detected = []

            for char in characters[0].boxes:
                x1c, y1c, x2c, y2c = map(int, char.xyxy[0])
                cls = int(char.cls[0])
                detected.append((cls, x1c))

            detected.sort(key=lambda c: c[1])
            plate_num = ''.join(character_map[c[0]] for c in detected)

            found_numbers.append(plate_num)

    cap.release()
    return found_numbers