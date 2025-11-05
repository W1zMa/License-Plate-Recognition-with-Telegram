import cv2
import os
from ultralytics import YOLO


character_map = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 
                    'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 
                    'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 
                    'U', 'V', 'W', 'X', 'Y', 'Z']

BASE_DIR = os.path.dirname(__file__)
weights_dir = os.path.join(BASE_DIR, "weights")

license_plate_model = YOLO(os.path.join(weights_dir, "detection.pt"))
character_model = YOLO(os.path.join(weights_dir, "recognition.pt"))       

def process_video(file_path: str):
    cap = cv2.VideoCapture(file_path)
    fps_number = 0
    fps = cap.get(cv2.CAP_PROP_FPS)
    found_numbers = []
    found_numbers_ = set()

    while cap.isOpened():
        ret, frame = cap.read()
        fps_number += 1
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
                cls = int(char.cls)
                conf = float(char.conf[0])
                detected.append((conf, cls, x1c))

            detected.sort(key=lambda c: c[2])
            plate_num = ''.join(character_map[c[1]] for c in detected)
            avg_conf = sum(c[0] for c in detected) / len(detected) * 100
            if fps == 0:
                time_code = 0
            else:    
                time_code = fps_number / fps

            if file_path.lower().split('.')[-1] == 'mp4':
                
                if plate_num in found_numbers_:
                    continue
                if avg_conf < 85.0:
                    continue
                found_numbers_.add(plate_num)

            found_numbers.append({
                "plate": plate_num,
                'accuracy': round(avg_conf, 2),
                'timecode': round(time_code, 2)
            })

    cap.release()
    return found_numbers

#process_video()