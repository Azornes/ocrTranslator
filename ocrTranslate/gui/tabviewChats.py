import asyncio
import sys
import time
from threading import Thread

from ocrTranslate.assets import Assets as assets

import customtkinter

from ocrTranslate.config_files import chatGpt, edgeGpt
from ocrTranslate.gui.auto_resize_text_box import AutoResizeTextBox


class TabviewChats(customtkinter.CTkTabview):
    def __init__(self, root, ai_services, send_message_icon, display_func = None):
        customtkinter.CTkTabview.__init__(self, root, width=25)
        self.root = root
        self.ai_services = ai_services
        self.send_message_icon = send_message_icon
        self.display_func = display_func

        self.textbox_chatgpt_frame = None
        self.textbox_chatgpt_send_frame = None
        self.button_send_message_chatgpt = None

        self.textbox_bing_frame = None
        self.textbox_bing_send_frame = None
        self.button_send_message_bing = None

        self.textbox_Bard_frame = None
        self.textbox_Bard_send_frame = None
        self.button_send_message_Bard = None

        method_name = 'tabview_chat_ai'
        self.grid(row=0, column=0, padx=(0, 20), pady=(5, 5), sticky="nsew")
        for ai_service in ai_services:
            self.add(str(ai_service[0]))
            self.tab(str(ai_service[0])).grid_columnconfigure(0, weight=1)  # configure grid of individual tabs
            self.tab(str(ai_service[0])).grid_rowconfigure(0, weight=1)  # configure grid of individual tabs
        setattr(self, method_name, self)
        for ai_service in ai_services:
            textbox_ai_frame = customtkinter.CTkTextbox(self.tab(ai_service[0]), undo=True, autoseparators=True)
            textbox_ai_frame.grid(row=0, column=0, padx=(0, 0), pady=(0, 0), sticky="nsew")
            textbox_ai_frame.tag_config("user_name", justify='left', foreground='white', font=customtkinter.CTkFont(size=14, weight="bold"))
            textbox_ai_frame.tag_config("user_message", justify='left', foreground='white')
            textbox_ai_frame.tag_config("chatbot_name", justify='left', foreground='lightblue', font=customtkinter.CTkFont(size=14, weight="bold"))
            textbox_ai_frame.tag_config("chatbot_message", justify='left', foreground='lightblue')

            textbox_ai_send_frame = AutoResizeTextBox(textbox_ai_frame)
            textbox_ai_send_frame.grid(row=1, column=0, padx=(15, 0), pady=(0, 0), sticky="nsew")
            button_send_message_ai = customtkinter.CTkButton(master=textbox_ai_send_frame, text="", fg_color="transparent", bg_color="transparent", border_width=0, width=26, anchor="left", height=26, text_color=("gray10", "#DCE4EE"), image=self.send_message_icon)
            button_send_message_ai.grid(row=0, column=1, padx=(14, 7), pady=(4, 0), sticky="e")
            textbox_ai_send_frame.button = button_send_message_ai

            method_name = 'textbox_{}_frame'.format(ai_service[0].lower().replace(" ", "_"))
            setattr(self, method_name, textbox_ai_frame)

            method_name = 'textbox_{}_send_frame'.format(ai_service[0].lower().replace(" ", "_"))
            setattr(self, method_name, textbox_ai_send_frame)

            method_name = 'button_send_message_{}'.format(ai_service[0].lower().replace(" ", "_"))
            setattr(self, method_name, button_send_message_ai)

        self.button_send_message_chatgpt.configure(command=lambda arg1=self.textbox_chatgpt_send_frame, arg2=self.textbox_chatgpt_frame, arg3="ChatGPT": self.send_message_button(arg1, arg2, arg3))
        self.button_send_message_bing.configure(command=lambda arg1=self.textbox_bing_send_frame, arg2=self.textbox_bing_frame, arg3="Bing": self.send_message_button(arg1, arg2, arg3))

    async def display_chat_ChatGPT(self, word, widget):
        async for response in chatGpt.run_chat_ai_async(word):
            widget.insert('end', response, 'chatbot_message')
        widget.insert('end', "\n\n")

    async def display_chat_Bing(self, word, widget):
        async for response in edgeGpt.run_chat_ai_async(word):
            widget.insert('end', response, 'chatbot_message')
        widget.insert('end', "\n\n")

    def send_message_button(self, textbox_ai_send_frame, textbox_ai_frame, name_service):
        thread = Thread(target=self.send_message_ai, args=(textbox_ai_send_frame, textbox_ai_frame, name_service,))
        thread.start()

    def send_message_ai(self, textbox_ai_send_frame, textbox_ai_frame, name_service):
        # root.loading_icon.start()
        message = textbox_ai_send_frame.get(0.0, 'end')
        print(message)
        textbox_ai_send_frame.delete(0.0, 'end')
        textbox_ai_frame.insert('end', f"You:\n", 'user_name')
        textbox_ai_frame.insert('end', f"{message}\n", 'user_message')
        textbox_ai_frame.insert('end', f"{name_service}:\n", 'chatbot_name')
        method_name = 'self.display_chat_{}'.format(name_service)
        method = eval(method_name)
        asyncio.run(method(message, textbox_ai_frame))

    def get_key(self, valu):
        for key, value in self.__dict__.items():
            # print(str(key) + " | " + str(value))
            if valu == str(value):
                return key
        return "key doesn't exist"
