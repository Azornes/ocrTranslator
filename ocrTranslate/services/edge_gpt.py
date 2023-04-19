import os
import uuid

import asyncio
from enum import Enum

from EdgeGPT import Chatbot
from ocrTranslate.assets import Assets as assets

from secrets import compare_digest

from ocrTranslate.utils import format_words, format_words2

class ConversationStyle(Enum):
    creative = "h3imaginative,clgalileo,gencontentv3"
    balanced = "galileo"
    precise = "h3precise,clgalileo"

class EdgeGPTFree:
    def __init__(self, cookie_path="") -> None:
        self.edge_gpt_free = None
        if os.path.exists(cookie_path):
            self.cookie_path = cookie_path
            self.is_active = True
            self.renew_chatbot_cookies()
        else:
            self.is_active = False

    def renew_chatbot_cookies(self):
        try:
            self.edge_gpt_free = Chatbot(cookie_path=self.cookie_path)
        except Exception as e:
            self.is_active = False
            print(e)
            print("cookies has been out of date, please renew cookies")

    async def run_translate_async(self, word, language_to="English", prompt=""):
        if self.is_active:
            words = format_words(word)
            if prompt == "":
                prompt = "Please, translate the following text into {languageInText} yourself, without using a web translation service and without any explanation. Write only translated text. This is text to translate: {wordInText}".format(wordInText=words, languageInText=language_to)
            else:
                prompt = prompt + " " + words

            prev_text = ""
            async for data in self.edge_gpt_free.ask_stream(prompt=prompt, conversation_style="precise", wss_link="wss://sydney.bing.com/sydney/ChatHub"):
                print(data[0])
                print(data[1])
                if not data[0]:
                    response = data[1][len(prev_text):]
                    prev_text = data[1]
                    yield response
                else:
                    break
        else:
            yield "edgegpt non valid user date. Get cookies.json from bing.com"

    async def run_chat_ai(self, prompt=""):
        print("run_chat_ai")
        if self.is_active:
            response = await self.edge_gpt_free.ask(prompt=prompt, conversation_style="balanced", wss_link="wss://sydney.bing.com/sydney/ChatHub")
            return response
        else:
            return "edgegpt non valid user date"

    async def run_chat_ai_async(self, prompt=""):
        if self.is_active:
            prev_text = ""
            async for data in self.edge_gpt_free.ask_stream(prompt=prompt, conversation_style="balanced", wss_link="wss://sydney.bing.com/sydney/ChatHub"):
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
            yield "edgegpt non valid user date. Get cookies.json from bing.com"


def test_edge_gpt():
    try:
        edgeGpt = EdgeGPTFree(cookie_path="C:\Programowanie\Projekty\Python\HelpApps\ocrTranslator3\ocrTranslate\configs\cookies.json", )
    except KeyError:
        edgeGpt = EdgeGPTFree()

    async def display_chat_ChatGPT(word):
        async for response in edgeGpt.run_chat_ai_async(word):
            print(response)

    asyncio.run(display_chat_ChatGPT("caan you remember the first time you saw a computer?"))

    print(asyncio.run(edgeGpt.run_chat_ai("caan you remember the first time you saw a computer?")))
    print(asyncio.run(edgeGpt.run_chat_ai("what is your favorite color?")))

#test_edge_gpt()