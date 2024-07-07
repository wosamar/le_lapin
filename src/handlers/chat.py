import abc
import traceback

import requests
from google.generativeai.types import GenerationConfigDict, ContentDict, StopCandidateException
from google.generativeai.types.safety_types import SafetySettingOptions, HarmCategory, HarmBlockThreshold

from settings import Settings
import google.generativeai as genai

settings = Settings()


class ChatBot(abc.ABC):
    error_message: str = None

    def __init__(self, error_message):
        self.error_message = error_message

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

    def __init__(self, prompt: str, **kwargs):
        super(GeminiChatBot, self).__init__(**kwargs)
        self.chat_session = self.model.start_chat(
            history=[
                ContentDict(parts=[{'text': prompt}], role="user")

            ]
        )

    def gen_response(self, prompt: str):
        try:
            response = self.chat_session.send_message(
                content=prompt,
                safety_settings={
                    HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: HarmBlockThreshold.BLOCK_ONLY_HIGH,
                }
            )
            # for content in self.chat_session.history:
            #     part = content.parts[0]
            #     print(content.role, "->", type(part).to_dict(part))
            #     print('-' * 80)

            return response.text
        except StopCandidateException as ex:
            print(ex.__str__())
            return "無法回答這個問題 > <"
        except Exception:
            print(traceback.format_exc())
            return self.error_message
