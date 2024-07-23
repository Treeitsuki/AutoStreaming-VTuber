import gradio as gr
import threading
import time
from PIL import Image
from src.vvox import vvox_mic
from src.api import gen_chat_response_with_gpt4
from src.screenshot import take_screenshot
from src.screenshot import get_latest_screenshot

#キャラ選択
speaker = "3"    #ずんだもん

def process_and_speak(image):
        response_text = gen_chat_response_with_gpt4(image)
        vvox_mic(speaker, response_text)
        return response_text

def main():
    image = gr.Image(label="Image File", type="pil")
    output = gr.Textbox(label="Explanation")

    gr.Interface(fn=process_and_speak, inputs=image, outputs=output).launch()

if __name__ == "__main__":
    main()
