from PIL import ImageGrab
import time
import os

# スクリーンショットを保存するディレクトリ
save_directory = "./screenshots"
os.makedirs(save_directory, exist_ok=True)

def take_screenshot():
    timestamp = time.strftime("%Y%m%d-%H%M%S")
    screenshot_filename = os.path.join(save_directory, f"screenshot_{timestamp}.png")
    screenshot = ImageGrab.grab()
    screenshot.save(screenshot_filename)

def get_latest_screenshot():
    files = sorted(os.listdir(save_directory), key=lambda x: os.path.getctime(os.path.join(save_directory, x)), reverse=True)
    if files:
        return os.path.join(save_directory, files[0])
    return None

