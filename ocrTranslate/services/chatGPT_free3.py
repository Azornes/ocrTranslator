import uuid

from revChatGPT.V1 import Chatbot as ChatbotFree
from secrets import compare_digest

from ocrTranslate.utils import format_words, format_words2
import json

class ChatGPTFree:
    def __init__(self, email="", password="", session_token="", access_token="") -> None:
        self.chat_gpt_free = None
        self.error_message = "Not initialized, go to Settings and enter your access token"
        if not compare_digest(email, "") and not compare_digest(password, ""):
            self.email = email
            self.password = password
            self.error_message = "Your email or password is invalid"
            self.is_active = True
            self.renew_chatbot_session_password()
        elif not compare_digest(session_token, ""):
            self.session_token = session_token
            self.error_message = "Your session token is invalid"
            self.is_active = True
            self.renew_chatbot_session_token()
        elif not compare_digest(access_token, ""):
            self.access_token = access_token
            self.error_message = "Your access token is expired, please log in at https://chat.openai.com/ and next get the access token from the https://chat.openai.com/api/auth/session"
            self.is_active = True
            self.renew_chatbot_access_token()
        else:
            self.is_active = False

    def renew_chatbot_session_password(self):
        try:
            self.chat_gpt_free = ChatbotFree(config={"email": "{email}".format(email=self.email), "password": "{password}".format(password=self.password)})
        except Exception as e:
            self.is_active = False
            print(e)
            print("password or email are invalid")

    def renew_chatbot_session_token(self):
        try:
            self.chat_gpt_free = ChatbotFree(config={"session_token": "{session_token}".format(session_token=self.session_token)})
        except Exception as e:
            self.is_active = False
            print(e)
            print("session token has been out of date, please renew token")

    def renew_chatbot_access_token(self):
        try:
            self.chat_gpt_free = ChatbotFree(config={"access_token": "{access_token}".format(access_token=self.access_token)})
        except Exception as e:
            self.is_active = False
            print(e)
            print("access token has been out of date, please renew token")

    async def run_translate_async(self, word, language_to="English"):
        if self.is_active:
            words = format_words(word)
            prev_text = ""
            for data in self.chat_gpt_free.ask("Just translate the following sentence into {languageInText}, without any explanation and write only the translated sentence:\n{wordInText}".format(wordInText=words, languageInText=language_to)):
                response = data["message"][len(prev_text):]
                prev_text = data["message"]
                yield response
        else:
            yield self.error_message

    def run_translate(self, word, language_to="English", prompt=""):
        print("translate_by_chat_gpt")
        if self.is_active:
            words = format_words(word)
            if prompt == "":
                prompt = "Just translate the following sentence into {languageInText}, without any explanation and write only the translated sentence: {wordInText}".format(wordInText=words, languageInText=language_to)
            else:
                prompt = prompt + " " + words

            response = ""
            prev_text = ""
            #print(self.chat_gpt_free.conversation_id)
            #print(self.chat_gpt_free.parent_id)

            for data in self.chat_gpt_free.ask(prompt=prompt, conversation_id=str(uuid.uuid4())):
                response = data["message"]
                message = data["message"][len(prev_text):]
                print(message, end="", flush=True)
                prev_text = data["message"]
            print("")
            return response
        else:
            return self.error_message

    def run_chat_ai(self, prompt=""):
        print("run_chat_ai")
        if self.is_active:
            response = ""
            prev_text = ""

            for data in self.chat_gpt_free.ask(prompt=prompt, conversation_id=str(uuid.uuid4())):
                response = data["message"]
                message = data["message"][len(prev_text):]
                print(message, end="", flush=True)
                prev_text = data["message"]
            print("")
            return response
        else:
            return self.error_message

    async def run_chat_ai_async(self, prompt=""):
        if self.is_active:
            prev_text = ""
            try:
                for data in self.chat_gpt_free.ask(prompt=prompt):
                    response = data["message"][len(prev_text):]
                    prev_text = data["message"]
                    yield response
            except Exception as e:
                print(e)
                #res = json.loads(e.__dict__.get("message")).get("detail").get("message")
                #print(res)
                yield self.error_message
            print(self.chat_gpt_free.conversation_id)
        else:
            yield self.error_message