import gradio as gr
import threading
import time
from src.vvox import vvox
from src.api import gen_chat_response_with_gpt4
from src.screenshot import take_screenshot
from src.screenshot import get_latest_screenshot

# 画面キャプチャの間隔
interval = 60

def process_and_speak(image):
    response_text = gen_chat_response_with_gpt4(image)
    vvox(response_text)
    return response_text

def screenshot():
    while True:
        take_screenshot()
        time.sleep(interval)

def get_image_from_screenshot():
    return get_latest_screenshot()

def main():
    # 画面キャプチャを開始
    screenshot_thread = threading.Thread(target=screenshot, daemon=True)
    screenshot_thread.start()
    
    # Gradioの設定
    def update(image):
        latest_screenshot = get_image_from_screenshot()
        if latest_screenshot:
            return process_and_speak(latest_screenshot)
        return "No image available"

    image = gr.Image(label="Image File", type="pil")
    output = gr.Textbox(label="Explanation")

    app = gr.Interface(fn=update, inputs=image, outputs=output, live=True)
    app.launch()

if __name__ == "__main__":
    main()
