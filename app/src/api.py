import json
from openai import OpenAI
import base64
import io

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