import cv2
import os
from datetime import datetime

def capture_webcam(save_folder):
    # Try different camera indices if needed
    for cam_index in range(3):
        cap = cv2.VideoCapture(cam_index)
        if cap.isOpened():
            ret, frame = cap.read()
            cap.release()

            if ret:
                filename = f"webcam_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
                filepath = os.path.join(save_folder, filename)
                cv2.imwrite(filepath, frame)
                print(f"[DEBUG] Webcam image saved at: {filepath}")
                return filepath
            else:
                print(f"[ERROR] Failed to read frame from webcam index {cam_index}")
        else:
            print(f"[ERROR] Webcam index {cam_index} not available")

    raise Exception("Failed to capture image from webcam on any index")
