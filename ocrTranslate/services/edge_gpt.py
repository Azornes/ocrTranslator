import os
import uuid

import asyncio
from EdgeGPT import Chatbot, ConversationStyle
from ocrTranslate.assets import Assets as assets

from secrets import compare_digest

from ocrTranslate.utils import format_words, format_words2


class EdgeGPTFree:
    def __init__(self, cookiePath="") -> None:
        self.edge_gpt_free = None
        if os.path.exists(cookiePath):
            self.cookie_path = cookiePath
            self.is_active = True
            self.renew_chatbot_cookies()
        else:
            self.is_active = False

    def renew_chatbot_cookies(self):
        try:
            self.edge_gpt_free = Chatbot(cookiePath=self.cookie_path)
        except Exception as e:
            self.is_active = False
            print(e)
            print("cookies has been out of date, please renew cookies")

    async def run_translate_async(self, word, language_to="English"):
        if self.is_active:
            words = format_words(word)
            prev_text = ""
            for data in self.chat_gpt_free.ask("Just translate the following sentence into {languageInText}, without any explanation and write only the translated sentence:\n{wordInText}".format(wordInText=words, languageInText=language_to)):
                response = data["message"][len(prev_text):]
                prev_text = data["message"]
                yield response
        else:
            yield "chatgpt non valid user date"

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
            return "chatgpt non valid user date"

    async def run_chat_ai(self, prompt=""):
        print("run_chat_ai")
        if self.is_active:
            response = await self.edge_gpt_free.ask(prompt=prompt, conversation_style=ConversationStyle.creative, wss_link="wss://sydney.bing.com/sydney/ChatHub")
            return response
        else:
            return "chatgpt non valid user date"

    async def run_chat_ai_async(self, prompt=""):
        if self.is_active:
            prev_text = ""
            async for data in self.edge_gpt_free.ask_stream(prompt=prompt, conversation_style=ConversationStyle.creative, wss_link="wss://sydney.bing.com/sydney/ChatHub"):
                #print(data[0])
                #print(data[1])
                if not data[0]:
                    response = data[1][len(prev_text):]
                    prev_text = data[1]
                    yield response
                #print(data)
                #print(data['item']['messages'][1]['text'])
                #response = data['item']['messages'][1]['text']
                #yield data
        else:
            yield "edgegpt non valid user date"


def test_edge_gpt():
    try:
        edgeGpt = EdgeGPTFree(cookiePath="C:\Programowanie\Projekty\Python\HelpApps\ocrTranslator3\ocrTranslate\configs\cookies.json", )
    except KeyError:
        edgeGpt = EdgeGPTFree()

    async def display_chat_ChatGPT(word):
        async for response in edgeGpt.run_chat_ai_async(word):
            print(response)

    asyncio.run(display_chat_ChatGPT("caan you remember the first time you saw a computer?"))

    print(asyncio.run(edgeGpt.run_chat_ai("caan you remember the first time you saw a computer?")))
    print(asyncio.run(edgeGpt.run_chat_ai("what is your favorite color?")))

#test_edge_gpt()