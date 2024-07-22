import gradio as gr
from src.vvox import vvox
from src.api import gen_chat_response_with_gpt4

def main():
    def process_and_speak(image):
        response_text = gen_chat_response_with_gpt4(image)
        vvox(response_text)
        return response_text
    
    image = gr.Image(label="Image File", type="pil")
    output = gr.Textbox(label="Explanation")

    gr.Interface(fn=process_and_speak, inputs=image, outputs=output).launch()

if __name__ == "__main__":
    main()