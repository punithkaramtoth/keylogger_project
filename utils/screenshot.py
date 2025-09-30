from PIL import ImageGrab
from datetime import datetime
import os

def take_screenshot(save_folder):
    # Capture full screen
    screenshot = ImageGrab.grab()
    
    filename = f"screenshot_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
    filepath = os.path.join(save_folder, filename)
    screenshot.save(filepath)

    return filepath
