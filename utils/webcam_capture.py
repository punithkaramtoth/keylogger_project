import cv2
import os
from datetime import datetime

def capture_webcam(output_folder):
    try:
        cap = cv2.VideoCapture(0)  # Use default webcam

        if not cap.isOpened():
            raise Exception("Failed to open webcam")

        ret, frame = cap.read()
        cap.release()

        if not ret:
            raise Exception("Failed to capture image from webcam")

        filename = f"webcam_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
        path = os.path.join(output_folder, filename)
        cv2.imwrite(path, frame)
        return path

    except Exception as e:
        print(f"[Webcam Error] {e}")
        return None
