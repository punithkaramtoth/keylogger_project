import os
from datetime import datetime


try:
    import cv2
except ImportError:
    cv2 = None
    print("⚠️ OpenCV not available. Webcam features are disabled on this platform.")


def capture_webcam(output_folder):
   
    if cv2 is None:
        print("⚠️ Webcam not supported in this environment (OpenCV not available).")
        return None

    try:
        cap = cv2.VideoCapture(0) 
        if not cap.isOpened():
            print("⚠️ Unable to access the webcam.")
            return None

        ret, frame = cap.read()
        cap.release()

        if not ret:
            print("⚠️ Failed to capture image from webcam.")
            return None

        os.makedirs(output_folder, exist_ok=True)

        filename = f"webcam_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
        path = os.path.join(output_folder, filename)

        cv2.imwrite(path, frame)
        print(f"✅ Image captured successfully: {path}")
        return path

    except Exception as e:
        print(f"[Webcam Error] {e}")
        return None
