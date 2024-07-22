import base64
import io
import json
from PIL import Image
import gradio as gr
from openai import OpenAI
import requests
import pyaudio

SYSTEM_ROLE_CONTENT = "あなたは日本の実況者です。入力された画像を認識し、ゲーム実況者のような口調で実況してください。"
PROMPT_TEMPLATE = "入力された画像を実況者のように解説してください。"

def get_gpt_openai_apikey():
    with open("./secret.json") as f:
        secret = json.load(f)
    return secret["OPENAI_API_KEY"]


def encode_image(image):
    byte_arr = io.BytesIO()
    image.save(byte_arr, format='JPEG')
    base64_image = f"data:image/jpeg;base64,{base64.b64encode(byte_arr.getvalue()).decode()}"
    return base64_image

def create_message(system_role, prompt, image_base64):
    message = [
        {
            'role': 'system',
            'content': system_role
        },
        {
            'role': 'user',
            'content': [
                {
                    'type': 'text',
                    'text': prompt
                },
                {
                    'type': 'image_url',
                    'image_url': {
                        'url': image_base64
                    }
                },
            ]
        },
    ]
    return message


def gen_chat_response_with_gpt4(image):
    openai_client = OpenAI(api_key=get_gpt_openai_apikey())
    image_base64 = encode_image(image)
    messages = create_message(SYSTEM_ROLE_CONTENT, PROMPT_TEMPLATE, image_base64)

    response = openai_client.chat.completions.create(
        model='gpt-4o-2024-05-13',
        messages = messages,
        temperature = 0.1,
    )

    # print(response)
    return response.choices[0].message.content

def vvox_test(text):
    # エンジン起動時に表示されているIP、portを指定
    host = "127.0.0.1"
    port = 50021
    
    # 音声化する文言と話者を指定(3で標準ずんだもんになる)
    params = (
        ('text', text),
        ('speaker', 3),
    )
    
    # 音声合成用のクエリ作成
    query = requests.post(
        f'http://{host}:{port}/audio_query',
        params=params
    )
    
    # 音声合成を実施
    synthesis = requests.post(
        f'http://{host}:{port}/synthesis',
        headers = {"Content-Type": "application/json"},
        params = params,
        data = json.dumps(query.json())
    )
    
    # 再生処理
    voice = synthesis.content
    pya = pyaudio.PyAudio()
    
    # サンプリングレートが24000以外だとずんだもんが高音になったり低音になったりする
    stream = pya.open(format=pyaudio.paInt16,
                      channels=1,
                      rate=24000,
                      output=True)
    
    stream.write(voice)
    stream.stop_stream()
    stream.close()
    pya.terminate()

def main():
    def process_and_speak(image):
        response_text = gen_chat_response_with_gpt4(image)
        vvox_test(response_text)
        return response_text
    
    image = gr.Image(label="Image File", type="pil")
    output = gr.Textbox(label="Explanation")

    gr.Interface(fn=process_and_speak, inputs=image, outputs=output).launch()

if __name__ == "__main__":
    main()