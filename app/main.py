import threading
import time
from PIL import Image
from src.vvox import vvox_mic
from src.api import gen_chat_response_with_gpt4
from src.screenshot import take_screenshot, get_latest_screenshot

# 画面キャプチャの準備時間と間隔
preparation = 5
interval = 120

#キャラ選択
spaker = "3"    #ずんだもん

def process_and_speak(image):
    response_text = gen_chat_response_with_gpt4(image)
    vvox_mic(spaker, response_text)
    return response_text

def screenshot():
    while True:
        time.sleep(preparation)
        take_screenshot()
        time.sleep(interval)

def get_image_from_screenshot():
    image_path = get_latest_screenshot()
    if image_path:
        return Image.open(image_path)
    return None

def main():
    # 画面キャプチャを開始
    screenshot_thread = threading.Thread(target=screenshot, daemon=True)
    screenshot_thread.start()
    
    while True:
        latest_screenshot = get_image_from_screenshot()
        if latest_screenshot:
            response = process_and_speak(latest_screenshot)
            print(response)
        else:
            print("No image available")
        time.sleep(interval)

if __name__ == "__main__":
    main()
