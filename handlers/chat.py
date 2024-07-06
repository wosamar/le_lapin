import abc
import traceback

import requests
from google.generativeai.types import GenerationConfigDict, ContentDict

from settings import Settings
import google.generativeai as genai

settings = Settings()


class ChatBot(abc.ABC):
    error_message: str = "現在忙線中，嗶嗶"

    def gen_response(self, prompt: str):
        raise NotImplementedError("ChatBot must implement get_response.")


class GPT2ChatBot(ChatBot):
    api_url = "https://api-inference.huggingface.co/models/gpt2"
    headers = {"Authorization": f"Bearer {settings.HUGGING_FACE_TOKEN}"}

    def gen_response(self, prompt: str):
        response = requests.post(self.api_url, headers=self.headers, json={"inputs": prompt})
        if response.status_code == 200:
            res = response.json()[0].get('generated_text')
            return res
        else:
            print(response)
            return self.error_message


genai.configure(api_key=settings.GEMINI_API_KEY)


class GeminiChatBot(ChatBot):
    generation_config = GenerationConfigDict(**{
        "temperature": 1.6,
        "top_p": 0.95,
        "top_k": 64,
        "max_output_tokens": 8192,
        "response_mime_type": "text/plain",
    })

    model = genai.GenerativeModel(
        model_name="gemini-1.5-flash",
        generation_config=generation_config,
    )
    chat_session = None

    def __init__(self, prompt: str):
        self.chat_session = self.model.start_chat(
            history=[
                ContentDict(parts=[{'text': prompt}], role="user")

            ]
        )

    def gen_response(self, prompt: str):
        try:
            response = self.chat_session.send_message(prompt)
            # for content in self.chat_session.history:
            #     part = content.parts[0]
            #     print(content.role, "->", type(part).to_dict(part))
            #     print('-' * 80)

            return response.text
        except Exception:
            print(traceback.format_exc())
            return self.error_message
