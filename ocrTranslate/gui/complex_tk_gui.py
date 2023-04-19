import base64
import configparser
import os

from tktooltip import ToolTip
import customtkinter

from ocrTranslate.assets import Assets as assets
from ocrTranslate.config_files import google_api, capture2Text, chatGpt, tesseract, baidu
from ocrTranslate.gui.AnimatedGif import AnimatedGif
from ocrTranslate.gui.auto_complete_combobox import AutocompleteCombobox
from ocrTranslate.gui.auto_resize_text_box import AutoResizeTextBox
from ocrTranslate.gui.tabviewChats import TabviewChats
from ocrTranslate.langs import _langs, services_translators_languages, _langs2

customtkinter.set_appearance_mode("System")  # Modes: "System" (standard), "Dark", "Light"
customtkinter.set_default_color_theme("blue")  # Themes: "blue" (standard), "green", "dark-blue"

result_boxes = []  # Result window identified earlier
from PIL import Image


def new_tag_config(self, tagName, **kwargs):
    return self._textbox.tag_config(tagName, **kwargs)


customtkinter.CTkTextbox.tag_config = new_tag_config


class ComplexTkGui(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        # ||||||||||||||||||| configure window |||||||||||||||||||
        self.title("OCR_Translator")
        self.geometry(f"{1100}x{580}")
        # ||||||||||||||||||| configure tooltip style |||||||||||||||||||
        tooltip_style = {"delay": 0.01, "follow": True, "parent_kwargs": {"bg": "black", "padx": 1, "pady": 1}, "fg": "white", "bg": "#1c1c1c", "padx": 4, "pady": 4}
        # ||||||||||||||||||| configure grid layout |||||||||||||||||||
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        # ||||||||||||||||||| load images |||||||||||||||||||
        self.rev_translate_icon = customtkinter.CTkImage(Image.open(assets.reverse_icon), size=(26, 26))
        self.send_message_icon = customtkinter.CTkImage(light_image=Image.open(assets.path_to_send_message_black), dark_image=Image.open(assets.path_to_send_message_white), size=(26, 26))
        self.chat_ai_icon = customtkinter.CTkImage(light_image=Image.open(assets.path_to_chatai_black), dark_image=Image.open(assets.path_to_chatai_white), size=(20, 20))
        self.home_image = customtkinter.CTkImage(light_image=Image.open(assets.path_to_home_dark), dark_image=Image.open(assets.path_to_home_light), size=(20, 20))
        self.settings_image = customtkinter.CTkImage(light_image=Image.open(assets.path_to_settings_dark), dark_image=Image.open(assets.path_to_settings_light), size=(20, 20))
        # ||||||||||||||||||| create sidebar frame with widgets |||||||||||||||||||
        self.sidebar_frame = customtkinter.CTkFrame(self, width=100, corner_radius=10)

        self.logo_label = customtkinter.CTkLabel(self.sidebar_frame, text="OCR_Translator", font=customtkinter.CTkFont(size=20, weight="bold"))
        self.logo_label.grid(row=0, column=0, padx=20, pady=(10, 10))

        self.sidebar_frame.grid_rowconfigure(4, weight=1)

        self.home_button = customtkinter.CTkButton(self.sidebar_frame, corner_radius=0, height=40, border_spacing=10, text="Home", fg_color="transparent", text_color=("gray10", "gray90"), hover_color=("gray70", "gray30"), image=self.home_image, anchor="w", command=self.home_button_event)
        self.home_button.grid(row=1, column=0, sticky="ew")
        self.chat_ai_button = customtkinter.CTkButton(self.sidebar_frame, corner_radius=0, height=40, border_spacing=10, text="Chat AI", fg_color="transparent", text_color=("gray10", "gray90"), hover_color=("gray70", "gray30"), image=self.chat_ai_icon, anchor="w", command=self.chat_ai_button_event)
        self.chat_ai_button.grid(row=2, column=0, sticky="ew")
        self.settings_button = customtkinter.CTkButton(self.sidebar_frame, corner_radius=0, height=40, border_spacing=10, text="Settings", fg_color="transparent", text_color=("gray10", "gray90"), hover_color=("gray70", "gray30"), image=self.settings_image, anchor="w", command=self.settings_button_event)
        self.settings_button.grid(row=3, column=0, sticky="ew")

        self.sidebar_button_save = customtkinter.CTkButton(self.sidebar_frame, text="Save Settings", command=self.save_setting)
        self.sidebar_button_save.grid(row=5, column=0, padx=20, pady=(10, 10))

        self.sidebar_button_load = customtkinter.CTkButton(self.sidebar_frame, text="Load Settings", command=self.load_setting)
        self.sidebar_button_load.grid(row=6, column=0, padx=20, pady=(10, 10))

        self.appearance_mode_label = customtkinter.CTkLabel(self.sidebar_frame, text="Appearance Mode:", anchor="w")
        self.appearance_mode_label.grid(row=7, column=0, padx=20, pady=(10, 0))
        self.appearance_mode_optionemenu = customtkinter.CTkOptionMenu(self.sidebar_frame, values=["Light", "Dark", "System"], command=self.change_appearance_mode_event)
        self.appearance_mode_optionemenu.grid(row=8, column=0, padx=20, pady=(10, 10))
        self.scaling_label = customtkinter.CTkLabel(self.sidebar_frame, text="UI Scaling:", anchor="w")
        self.scaling_label.grid(row=9, column=0, padx=20, pady=(10, 0))
        self.scaling_optionemenu = customtkinter.CTkOptionMenu(self.sidebar_frame, values=["80%", "90%", "100%", "110%", "120%"], command=self.change_scaling_event)
        self.scaling_optionemenu.grid(row=10, column=0, padx=20, pady=(10, 20))
        # section Home Frame
        # |_████████████████████████████████████████████████████████████████████|
        # |_________________________ create home frame _________________________|
        # |_████████████████████████████████████████████████████████████████████|
        self.home_frame = customtkinter.CTkFrame(self, corner_radius=0, fg_color="transparent")
        self.home_frame.grid_columnconfigure(0, weight=1)
        self.home_frame.grid_columnconfigure(1, weight=1)
        self.home_frame.grid_rowconfigure(0, weight=1)
        self.home_frame.grid_rowconfigure(1, weight=0)

        # ||||||||||||||||||| create scrollable frame |||||||||||||||||||
        self.scrollable_frame = customtkinter.CTkScrollableFrame(self.home_frame, label_text="OCR Checker")
        self.scrollable_frame.grid(row=0, column=0, padx=(0, 0), pady=(20, 0), sticky="nsew")
        self.scrollable_frame.grid_columnconfigure((0, 1, 2, 3), weight=1)
        # self.scrollable_frame.grid_columnconfigure("all", weight=1)

        self.switch_ocr_google_api = None
        self.switch_ocr_google_free = None
        self.switch_ocr_baidu_api = None
        self.switch_ocr_capture2text = None
        self.switch_ocr_windows_local = None
        self.switch_ocr_tesseract = None
        self.switch_ocr_rapidocr = None
        self.switches_ocr = []

        switchers = [("Google api",), ("Google Free",), ("Baidu api",), ("Capture2Text",), ("Windows local",), ("Tesseract",), ("RapidOCR",), ]

        rows = len(switchers) // 2
        for i, switcher in enumerate(switchers):
            method_name = 'switch_ocr_{}'.format(switcher[0].lower().replace(" ", "_"))
            switch = customtkinter.CTkSwitch(self.scrollable_frame, text="Turn " + switcher[0])
            switch.grid(row=i // 2, column=(i % 2) + 1, padx=0, pady=(0, 10), sticky="NSEW")
            setattr(self, method_name, switch)
            self.switches_ocr.append(switch)

        self.switch_from_text = customtkinter.CTkSwitch(self.scrollable_frame, text="Only from below text", command=self.disable_all_ocr_switchers)
        self.switch_from_text.grid(row=rows + 1, column=1, padx=0, pady=(0, 10), sticky="NSEW")
        ToolTip(self.switch_from_text, msg="Translate text only from below text box", **tooltip_style)

        self.switch_from_clipboard = customtkinter.CTkSwitch(self.scrollable_frame, text="Only from clipboard", command=self.disable_all_ocr_switchers)
        self.switch_from_clipboard.grid(row=rows + 1, column=2, padx=0, pady=(0, 10), sticky="NSEW")
        ToolTip(self.switch_from_clipboard, msg="Translate text only from clipboard", **tooltip_style)

        # self.scrollable_frame_textbox = customtkinter.CTkTextbox(self, width=250)
        # self.scrollable_frame_textbox.grid(row=1, column=1,padx=(10, 10), pady=(10, 10), sticky="nsew")

        self.scrollable_frame_textbox = customtkinter.CTkTextbox(self.scrollable_frame, height=1500, undo=True, autoseparators=True)
        self.scrollable_frame_textbox.grid(row=rows + 2, column=0, columnspan=4, rowspan=10, padx=(10, 10), pady=(10, 10), sticky="nsew")

        # ||||||||||||||||||| create tabview |||||||||||||||||||
        self.tabview = customtkinter.CTkTabview(self.home_frame, width=25)
        self.tabview.grid(row=0, column=1, padx=(20, 20), pady=(3, 0), sticky="nsew")
        self.tabview.add("Translation")
        self.tabview.add("Speech to Text")
        self.tabview.add("Text to Speech")
        self.tabview.tab("Translation").grid_columnconfigure(0, weight=1)  # configure grid of individual tabs
        self.tabview.tab("Translation").grid_rowconfigure(0, weight=1)  # configure grid of individual tabs
        self.tabview.tab("Speech to Text").grid_columnconfigure(0, weight=1)
        self.tabview.tab("Text to Speech").grid_columnconfigure(0, weight=1)
        # ||| Translation tab |||
        self.scrollable_frame_translation = customtkinter.CTkScrollableFrame(self.tabview.tab("Translation"))
        self.scrollable_frame_translation.grid(row=0, column=0, padx=(0, 0), pady=(0, 0), sticky="nsew")
        self.scrollable_frame_translation.grid_columnconfigure((0, 1, 2), weight=1)

        services_translators_languages_tab = ["Disabled", "ChatGPT", "EdgeGPT"]
        for a in services_translators_languages.keys():
            services_translators_languages_tab.append(a)

        self.option_menu_translation = customtkinter.CTkOptionMenu(self.scrollable_frame_translation, dynamic_resizing=False, values=services_translators_languages_tab, command=self.change_languages)
        self.option_menu_translation.grid(row=0, column=1, padx=20, pady=(20, 10))

        self.switch_window_mode = customtkinter.CTkSwitch(self.scrollable_frame_translation, text="Turn window mode", )
        self.switch_window_mode.grid(row=0, column=0, padx=(10, 0), pady=(20, 10))
        ToolTip(self.switch_window_mode, msg="Show an additional window with the translation or OCR.", **tooltip_style)

        self.switch_game_mode = customtkinter.CTkSwitch(self.scrollable_frame_translation, text="Turn game mode", )
        self.switch_game_mode.grid(row=1, column=0, padx=10, pady=(0, 20))
        ToolTip(self.switch_game_mode, msg="Show an additional window with the translation above the selected text. Click middle button of mouse to close window", **tooltip_style)

        self.loading_icon = AnimatedGif(self.scrollable_frame_translation, assets.path_to_loading_gif, 0.04, size=(50, 50))
        self.loading_icon.grid(row=1, column=1, rowspan=2, padx=0, pady=0, sticky="nsew")
        self.loading_icon.grid_save()

        self.switch_results_to_clipboard = customtkinter.CTkSwitch(self.scrollable_frame_translation, text="Results to Clipboard", )
        self.switch_results_to_clipboard.grid(row=1, column=2, padx=10, pady=(0, 20))

        self.label_from_language = customtkinter.CTkLabel(self.scrollable_frame_translation, text="From language:", anchor="w")
        self.label_from_language.grid(row=2, column=0, padx=(20, 0), pady=(0, 0))
        self.label_to_language = customtkinter.CTkLabel(self.scrollable_frame_translation, text="To language:", anchor="w")
        self.label_to_language.grid(row=2, column=2, padx=(0, 20), pady=(0, 0))

        self.combobox_from_language = AutocompleteCombobox(self.scrollable_frame_translation, completevalues=list(_langs2.values()))
        self.combobox_from_language.grid(row=3, column=0, padx=(20, 5), pady=(0, 0))
        self.button_reverse_language = customtkinter.CTkButton(master=self.scrollable_frame_translation, text="", fg_color="transparent", border_width=0, width=26, anchor="left", height=26, text_color=("gray10", "#DCE4EE"), image=self.rev_translate_icon, command=self.reverse_languages)
        self.button_reverse_language.grid(row=3, column=1, padx=(0, 0), pady=(0, 0))
        self.combobox_to_language = AutocompleteCombobox(self.scrollable_frame_translation, completevalues=list(_langs2.values()))
        self.combobox_to_language.grid(row=3, column=2, padx=(5, 20), pady=(0, 0))

        self.translation_frame_textbox = customtkinter.CTkTextbox(self.scrollable_frame_translation, width=250, height=1500, undo=True, autoseparators=True)
        self.translation_frame_textbox.grid(row=4, column=0, columnspan=3, padx=(10, 10), pady=(10, 10), sticky="nsew")

        # ||| Speech to Text tab |||
        self.label_tab_2 = customtkinter.CTkLabel(self.tabview.tab("Speech to Text"), text="WORK IN PROGRESS")
        self.label_tab_2.grid(row=0, column=0, padx=20, pady=20)

        # ||| Text to Speech tab |||
        self.label_tab_3 = customtkinter.CTkLabel(self.tabview.tab("Text to Speech"), text="WORK IN PROGRESS")
        self.label_tab_3.grid(row=0, column=0, padx=20, pady=20)

        # ||||||||||||||||||| create main entry and button |||||||||||||||||||
        self.button_options = customtkinter.CTkButton(master=self, corner_radius=0, height=20, width=20, border_spacing=0, text="", fg_color="transparent", text_color=("gray10", "gray90"), hover_color=("gray70", "gray30"), image=self.settings_image, anchor="w", command=self.hide_show_side_bar)
        # self.button_options = customtkinter.CTkButton(master=self, text="Options", fg_color="transparent", border_width=2, text_color=("gray10", "#DCE4EE"), width= 25, command=self.hide_show_side_bar)
        self.button_options.grid(row=0, column=0, padx=(0, 0), pady=(0, 0), sticky="nw")

        self.button_start = customtkinter.CTkButton(master=self.home_frame, text="START", fg_color="transparent", border_width=2, text_color=("gray10", "#DCE4EE"), command=self.pressed_print)
        self.button_start.grid(row=1, column=0, columnspan=2, padx=(20, 20), pady=5)
        self.seg_button_last_ocr_area = customtkinter.CTkSegmentedButton(self.home_frame)
        self.seg_button_last_ocr_area.grid(row=1, column=0, padx=(20, 10), pady=(10, 10), sticky="")
        self.seg_button_last_ocr_area.configure(values=["Off", "On", "Saved"])
        self.seg_button_last_ocr_area.winfo_children()[2].configure(state="disabled")
        ToolTip(self.seg_button_last_ocr_area.winfo_children()[0], msg="Off - the option is turned off.", **tooltip_style)
        ToolTip(self.seg_button_last_ocr_area.winfo_children()[1], msg="On - the next time the area will be saved.", **tooltip_style)
        ToolTip(self.seg_button_last_ocr_area.winfo_children()[2], msg="Saved - the area is already saved, and does not need to be selected again for the next OCR run.", **tooltip_style)

        # section Chat Ai Frame
        # |_██████████████████████████████████████████████████████████████████████|
        # |_________________________ create Chat Ai frame ________________________|
        # |_██████████████████████████████████████████████████████████████████████|

        self.chat_ai_frame = customtkinter.CTkFrame(self, corner_radius=0, fg_color="transparent")
        self.chat_ai_frame.grid_rowconfigure(0, weight=1)
        self.chat_ai_frame.grid_columnconfigure(0, weight=1)

        # ||||||||||||||||||| create tabview |||||||||||||||||||



        # self.tabviews_chat_ai = []
        # self.textbox_ai_frames = []
        # self.textbox_ai_send_frames = []
        # self.buttons_send_message_ai = []

        ai_services = [("ChatGPT",), ("Bing",), ("Bard",), ]

        for ai_service in ai_services:
            print(str(ai_service[0]))

        #for i in range(len(ai_services)):
        #    self.tabview_chat_ai1 = TabviewChats(self.chat_ai_frame, ai_services)

        self.tabview_chat_ai1 = TabviewChats(root = self.chat_ai_frame, ai_services=ai_services, send_message_icon=self.send_message_icon, column=0)

        # self.tabview_chat_ai = customtkinter.CTkTabview(self.chat_ai_frame, width=25)
        # self.tabview_chat_ai.grid(row=0, column=0, padx=(0, 20), pady=(5, 5), sticky="nsew")
        # self.tabview_chat_ai.add("ChatGPT")
        # self.tabview_chat_ai.add("Bing")
        # self.tabview_chat_ai.add("Bard")
        # self.tabview_chat_ai.tab("ChatGPT").grid_columnconfigure(0, weight=1)  # configure grid of individual tabs
        # self.tabview_chat_ai.tab("ChatGPT").grid_rowconfigure(0, weight=1)  # configure grid of individual tabs
        # self.tabview_chat_ai.tab("Bing").grid_columnconfigure(0, weight=1)  # configure grid of individual tabs
        # self.tabview_chat_ai.tab("Bing").grid_rowconfigure(0, weight=1)  # configure grid of individual tabs
        # # ||| ChatGPT tab |||
        # self.textbox_chatgpt_frame = customtkinter.CTkTextbox(self.tabview_chat_ai.tab("ChatGPT"), undo=True, autoseparators=True)
        # self.textbox_chatgpt_frame.grid(row=0, column=0, padx=(0, 0), pady=(0, 0), sticky="nsew")
        # self.textbox_chatgpt_frame.tag_config("user_name", justify='left', foreground='white', font=customtkinter.CTkFont(size=14, weight="bold"))
        # self.textbox_chatgpt_frame.tag_config("user_message", justify='left', foreground='white')
        # self.textbox_chatgpt_frame.tag_config("chatbot_name", justify='left', foreground='lightblue', font=customtkinter.CTkFont(size=14, weight="bold"))
        # self.textbox_chatgpt_frame.tag_config("chatbot_message", justify='left', foreground='lightblue')
        #
        # self.textbox_chatgpt_send_frame = AutoResizeTextBox(self.textbox_chatgpt_frame)
        # self.textbox_chatgpt_send_frame.grid(row=1, column=0, padx=(15, 0), pady=(0, 0), sticky="nsew")
        # self.button_send_message_chatgpt_ai = customtkinter.CTkButton(master=self.textbox_chatgpt_send_frame, text="", fg_color="transparent", bg_color="transparent", border_width=0, width=26, anchor="left", height=26, text_color=("gray10", "#DCE4EE"), image=self.send_message_icon)
        # self.button_send_message_chatgpt_ai.grid(row=0, column=1, padx=(14, 7), pady=(4, 0), sticky="e")
        # self.textbox_chatgpt_send_frame.button = self.button_send_message_chatgpt_ai
        # # ||| Bing tab |||
        # self.textbox_bing_frame = customtkinter.CTkTextbox(self.tabview_chat_ai.tab("Bing"), undo=True, autoseparators=True)
        # self.textbox_bing_frame.grid(row=0, column=0, padx=(0, 0), pady=(0, 0), sticky="nsew")
        # self.textbox_bing_frame.tag_config("user_name", justify='left', foreground='white', font=customtkinter.CTkFont(size=14, weight="bold"))
        # self.textbox_bing_frame.tag_config("user_message", justify='left', foreground='white')
        # self.textbox_bing_frame.tag_config("chatbot_name", justify='left', foreground='lightblue', font=customtkinter.CTkFont(size=14, weight="bold"))
        # self.textbox_bing_frame.tag_config("chatbot_message", justify='left', foreground='lightblue')
        #
        # self.textbox_bing_send_frame = AutoResizeTextBox(self.textbox_bing_frame)
        # self.textbox_bing_send_frame.grid(row=1, column=0, padx=(15, 0), pady=(0, 0), sticky="nsew")
        # self.button_send_message_bing_ai = customtkinter.CTkButton(master=self.textbox_bing_send_frame, text="", fg_color="transparent", bg_color="transparent", border_width=0, width=26, anchor="left", height=26, text_color=("gray10", "#DCE4EE"), image=self.send_message_icon)
        # self.button_send_message_bing_ai.grid(row=0, column=1, padx=(14, 7), pady=(4, 0), sticky="e")
        # self.textbox_bing_send_frame.button = self.button_send_message_bing_ai
        #
        # self.button_add_chat = customtkinter.CTkButton(master=self.chat_ai_frame, text="", fg_color="transparent", bg_color="transparent", border_width=0, width=26, anchor="left", height=26, text_color=("gray10", "#DCE4EE"), image=self.send_message_icon, command=self.add_new_chat)
        # self.button_add_chat.grid(row=0, column=0, padx=(14, 7), pady=(4, 0), sticky="w")

        # # ||||||||||||||||||| create tabview |||||||||||||||||||
        # self.tabview_chat_ai2 = customtkinter.CTkTabview(self.chat_ai_frame, width=25)
        # self.tabview_chat_ai2.grid(row=0, column=1, padx=(0, 20), pady=(5, 5), sticky="nsew")
        # self.tabview_chat_ai2.add("ChatGPT")
        # self.tabview_chat_ai2.add("Bing")
        # self.tabview_chat_ai2.add("Bard")
        # self.tabview_chat_ai2.tab("ChatGPT").grid_columnconfigure(0, weight=1)  # configure grid of individual tabs
        # self.tabview_chat_ai2.tab("ChatGPT").grid_rowconfigure(0, weight=1)  # configure grid of individual tabs
        # self.tabview_chat_ai2.tab("Bing").grid_columnconfigure(0, weight=1)  # configure grid of individual tabs
        # self.tabview_chat_ai2.tab("Bing").grid_rowconfigure(0, weight=1)  # configure grid of individual tabs
        #
        # self.tabview_chat_ai2.grid_forget()
        # self.tabview_chat_ai2.grid(row=0, column=1, padx=(0, 20), pady=(5, 5), sticky="nsew")

        # ||| text send to all |||
        self.textbox_chat_frame = AutoResizeTextBox(self.chat_ai_frame)
        self.textbox_chat_frame.grid(row=1, column=0, padx=(5, 20), pady=(15, 15), sticky="nsew")
        self.button_send_message_chat_ai = customtkinter.CTkButton(master=self.textbox_chat_frame, text="", fg_color="transparent", bg_color="transparent", border_width=0, width=26, anchor="left", height=26, text_color=("gray10", "#DCE4EE"), image=self.send_message_icon)
        self.button_send_message_chat_ai.grid(row=0, column=1, padx=(14, 7), pady=(4, 0), sticky="e")
        self.textbox_chat_frame.button = self.button_send_message_chat_ai

        # section Settings Frame
        # |_████████████████████████████████████████████████████████████████████████|
        # |_________________________ create settings frame _________________________|
        # |_████████████████████████████████████████████████████████████████████████|
        self.settings_frame = customtkinter.CTkFrame(self, corner_radius=0, fg_color="transparent")

        self.settings_frame.grid_rowconfigure(0, weight=1)
        self.settings_frame.grid_columnconfigure(0, weight=1)

        # ||||||||||||||||||| create tabview |||||||||||||||||||
        self.tabview_settings = customtkinter.CTkTabview(self.settings_frame, width=25)
        self.tabview_settings.grid(row=0, column=0, columnspan=2, padx=(0, 20), pady=(0, 20), sticky="nsew")
        self.tabview_settings.add("Services")
        self.tabview_settings.add("Other")
        self.tabview_settings.tab("Services").grid_columnconfigure(0, weight=1)  # configure grid of individual tabs
        self.tabview_settings.tab("Services").grid_rowconfigure(0, weight=1)  # configure grid of individual tabs
        self.tabview_settings.tab("Other").grid_columnconfigure(0, weight=1)  # configure grid of individual tabs
        self.tabview_settings.tab("Other").grid_rowconfigure(0, weight=1)  # configure grid of individual tabs

        # ||||||||||||||||||| create scrollable frame Services settings |||||||||||||||||||
        self.scrollable_settings_frame = customtkinter.CTkScrollableFrame(self.tabview_settings.tab("Services"), label_text="Services settings")
        self.scrollable_settings_frame.grid(row=0, column=0, padx=0, pady=0, sticky="nsew")
        self.scrollable_settings_frame.grid_columnconfigure(0, weight=0)
        self.scrollable_settings_frame.grid_columnconfigure(1, weight=1)

        self.entry_settings = []

        settings_dict = {'ChatGPT': ("ApiKey", 'session_token', "access_token", "email", "password"), 'Baidu': ("AppId", 'ApiKey', "SecretKey"), 'Capture2Text': ("path_to_Capture2Text_CLI_exe",), 'Tesseract': ("path_to_tesseract_exe",)}

        iterations = 0
        for service in settings_dict.items():
            label_main_name = 'label_{}'.format(service[0].lower().replace(" ", "_"))
            # print(label_main_name)
            label_main = customtkinter.CTkLabel(self.scrollable_settings_frame, text=service[0] + ":", anchor="w", font=customtkinter.CTkFont(size=14, weight="bold"))
            label_main.grid(row=iterations, column=0, padx=(5, 5), pady=(5, 5))
            setattr(self, label_main_name, label_main)
            iterations = iterations + 1
            for element in service[1]:
                label_name = 'label_{}_{}'.format(service[0].lower().replace(" ", "_"), element.lower().replace(" ", "_"))
                # print(label_name)
                label = customtkinter.CTkLabel(self.scrollable_settings_frame, text=element, anchor="w")
                label.grid(row=iterations, column=0, padx=(5, 5), pady=(5, 5), sticky="nsew")
                setattr(self, label_name, label)

                entry_name = 'entry_{}_{}'.format(service[0].lower().replace(" ", "_"), element.lower().replace(" ", "_"))
                # print(entry_name)
                entry = customtkinter.CTkEntry(self.scrollable_settings_frame, placeholder_text=element)
                entry.grid(row=iterations, column=1, padx=(5, 5), pady=(5, 5), sticky="nsew")
                setattr(self, entry_name, entry)
                self.entry_settings.append(entry)
                iterations = iterations + 1

        # ||||||||||||||||||| create scrollable frame Other settings |||||||||||||||||||
        self.scrollable_settings_frame_others = customtkinter.CTkScrollableFrame(self.tabview_settings.tab("Other"), label_text="Other settings")
        self.scrollable_settings_frame_others.grid(row=0, column=0, padx=0, pady=0, sticky="nsew")
        self.scrollable_settings_frame_others.grid_columnconfigure(0, weight=0)
        self.scrollable_settings_frame_others.grid_columnconfigure(1, weight=1)

        self.label_main_bindings = customtkinter.CTkLabel(self.scrollable_settings_frame_others, text="Bindings" + ":", anchor="w", font=customtkinter.CTkFont(size=14, weight="bold"))
        self.label_main_bindings.grid(row=0, column=0, padx=(5, 5), pady=(5, 5))

        self.label_binding_start_ocr = customtkinter.CTkLabel(self.scrollable_settings_frame_others, text="Bind START", anchor="w")
        self.label_binding_start_ocr.grid(row=1, column=0, padx=(5, 5), pady=(5, 5), sticky="nsew")

        key_combination = []

        def on_key_press(event):
            nonlocal key_combination
            separator = "_"
            if separator in event.keysym:
                first_part, second_part = event.keysym.split(separator, 1)
                new_string = separator.join([first_part])
            else:
                new_string = event.keysym
            if new_string not in key_combination:
                key_combination.append(new_string)

            self.entry_binding_start_ocr.configure(state="normal", border_color="orange")
            self.entry_binding_start_ocr.delete(0, 'end')
            self.entry_binding_start_ocr.insert(0, "+".join(key_combination))
            self.entry_binding_start_ocr.configure(state="readonly")

        def on_key_release(event):
            nonlocal key_combination
            self.entry_binding_start_ocr.configure(border_color="grey")
            self.label_binding_start_ocr.focus_set()
            key_combination = []

        def on_mouse_press(event):
            self.entry_binding_start_ocr.configure(state="readonly", border_color="orange")

        self.entry_binding_start_ocr = customtkinter.CTkEntry(self.scrollable_settings_frame_others, placeholder_text="")
        self.entry_binding_start_ocr.grid(row=1, column=1, padx=(5, 5), pady=(5, 5), sticky="nsew")
        self.entry_binding_start_ocr.bind("<KeyPress>", on_key_press)
        self.entry_binding_start_ocr.bind("<KeyRelease>", on_key_release)
        self.entry_binding_start_ocr.bind("<ButtonPress>", on_mouse_press)

        # |_████████████████████████████████████████████████████████████████████████|
        # |___________________________ set default values __________________________|
        # |_████████████████████████████████████████████████████████████████████████|
        self.seg_button_last_ocr_area.set("Off")
        self.appearance_mode_optionemenu.set("Dark")
        self.scaling_optionemenu.set("100%")
        self.option_menu_translation.set("Disabled")
        # select default frame
        self.select_frame_by_name("home")
        self.check_ocrs_are_active()

        self.load_setting()

    # section Functions
    # |_████████████████████████████████████████████████████████████████████████|
    # |___________________________ Functions __________________________|
    # |_████████████████████████████████████████████████████████████████████████|

    def add_new_chat(self):
        for i, tabview_chat in enumerate(self.tabviews_chat_ai):
            if tabview_chat.winfo_manager() == "grid":
                tabview_chat.grid_forget()
                self.chat_ai_frame.grid_columnconfigure((1, 2), weight=0)
            else:
                tabview_chat.grid(row=0, column=i, padx=(0, 20), pady=(5, 5), sticky="nsew")
                self.chat_ai_frame.grid_columnconfigure((0, 1, 2), weight=1)

    def clone_widget(self, widget, master=None):
        parent = master if master else widget.master
        cls = widget.__class__

        print(parent)
        print(cls)
        print(widget.configure())
        # Clone the widget configuration
        if widget.configure() != None:
            cfg = {key: widget.cget(key) for key in widget.configure()}
        else:
            cfg = {}
        cloned = cls(parent, **cfg)

        # Clone the widget's children
        for child in widget.winfo_children():
            child_cloned = self.clone_widget(child, master=cloned)
            print(child)
            if child.grid_info():
                grid_info = {k: v for k, v in child.grid_info().items() if k not in {'in'}}
                child_cloned.grid(**grid_info)
            elif child.place_info():
                place_info = {k: v for k, v in child.place_info().items() if k not in {'in'}}
                child_cloned.place(**place_info)
            else:
                try:
                    pack_info = {k: v for k, v in child.pack_info().items() if k not in {'in'}}
                    child_cloned.pack(**pack_info)
                except:
                    pass

        return cloned

    def hide_show_side_bar(self):
        if self.sidebar_frame.winfo_manager() == "grid":
            self.sidebar_frame.grid_forget()
        else:
            self.sidebar_frame.grid(row=0, column=0, rowspan=4, pady=(30, 0), padx=(0, 20), sticky="nsew")
            self.sidebar_frame.grid_columnconfigure(0, weight=1)

    def disable_all_ocr_switchers(self):
        if self.switch_from_text.get() == 1 or self.switch_from_clipboard.get() == 1:
            for switch_ocr in self.switches_ocr:
                switch_ocr.deselect()
                switch_ocr.configure(state="disabled")
            if self.switch_from_text.get() == 1:
                self.switch_from_clipboard.deselect()
                self.switch_from_clipboard.configure(state="disabled")
            if self.switch_from_clipboard.get() == 1:
                self.switch_from_text.deselect()
                self.switch_from_text.configure(state="disabled")
        else:
            for switch_ocr in self.switches_ocr:
                switch_ocr.configure(state="enabled")
            self.check_ocrs_are_active()

            self.switch_from_clipboard.configure(state="enabled")
            self.switch_from_text.configure(state="enabled")

    def open_input_dialog_event(self):
        dialog = customtkinter.CTkInputDialog(text="Type in a number:", title="CTkInputDialog")
        print("CTkInputDialog:", dialog.get_input())

    def change_appearance_mode_event(self, new_appearance_mode: str):
        customtkinter.set_appearance_mode(new_appearance_mode)

    def change_scaling_event(self, new_scaling: str):
        new_scaling_float = int(new_scaling.replace("%", "")) / 100
        customtkinter.set_widget_scaling(new_scaling_float)

    def pressed_print(self):
        print("button click")

    def reverse_languages(self):
        from_lang = self.combobox_from_language.get()
        to_lang = self.combobox_to_language.get()

        self.combobox_from_language.set(to_lang)
        self.combobox_to_language.set(from_lang)

    def change_languages(self, test):
        c = []
        if self.option_menu_translation.get() in services_translators_languages.keys():
            lista = services_translators_languages.get(self.option_menu_translation.get(), [])
            c = [_langs.get(a, a) for a in lista]
            self.combobox_from_language.configure(completevalues=c)
            self.combobox_to_language.configure(completevalues=c)

            if self.combobox_from_language.get() not in c:
                self.combobox_from_language.set("auto")
            if self.combobox_to_language.get() not in c:
                self.combobox_to_language.set("")
        elif self.option_menu_translation.get() == "ChatGPT" or self.option_menu_translation.get() == "GoogleFree" or self.option_menu_translation.get() == "EdgeGPT":
            self.combobox_from_language.configure(completevalues=list(_langs2.values()))
            self.combobox_to_language.configure(completevalues=list(_langs2.values()))

            if self.combobox_from_language.get() not in list(_langs2.values()):
                self.combobox_from_language.set("auto")
            if self.combobox_to_language.get() not in list(_langs2.values()):
                self.combobox_to_language.set("")

    def select_frame_by_name(self, name):
        # set button color for selected button
        self.home_button.configure(fg_color=("gray75", "gray25") if name == "home" else "transparent")
        self.settings_button.configure(fg_color=("gray75", "gray25") if name == "settings" else "transparent")
        self.chat_ai_button.configure(fg_color=("gray75", "gray25") if name == "chat_ai" else "transparent")

        # show selected frame
        if name == "home":
            self.home_frame.grid(row=0, column=1, sticky="nsew")
        else:
            self.home_frame.grid_forget()
        if name == "settings":
            self.settings_frame.grid(row=0, column=1, sticky="nsew")
        else:
            self.settings_frame.grid_forget()
        if name == "chat_ai":
            self.chat_ai_frame.grid(row=0, column=1, sticky="nsew")
        else:
            self.chat_ai_frame.grid_forget()

    def home_button_event(self):
        self.select_frame_by_name("home")

    def chat_ai_button_event(self):
        self.select_frame_by_name("chat_ai")

    def settings_button_event(self):
        self.select_frame_by_name("settings")

    def get_key(self, valu):
        for key, value in self.__dict__.items():
            # print(str(key) + " | " + str(value))
            if valu == str(value):
                return key
        return "key doesn't exist"

    def check_ocrs_are_active(self):
        if google_api.is_active:
            self.switch_ocr_google_api.configure(state="enabled")
        else:
            self.switch_ocr_google_api.deselect()
            self.switch_ocr_google_api.configure(state="disabled")

        if capture2Text.is_active:
            self.switch_ocr_capture2text.configure(state="enabled")
        else:
            self.switch_ocr_capture2text.deselect()
            self.switch_ocr_capture2text.configure(state="disabled")

        if tesseract.is_active:
            self.switch_ocr_tesseract.configure(state="enabled")
        else:
            self.switch_ocr_tesseract.deselect()
            self.switch_ocr_tesseract.configure(state="disabled")

        if baidu.is_active:
            self.switch_ocr_baidu_api.configure(state="enabled")
        else:
            self.switch_ocr_baidu_api.deselect()
            self.switch_ocr_baidu_api.configure(state="disabled")

    # save all gui elements into an ini file
    def save_setting(self, settings_name="settings", first_time=False):
        config = configparser.ConfigParser()
        if first_time:
            dict_settings = {"geometry": "1100x580+52+52"}
            dict_settings.update(self.save_mass_tree(self))
            config[settings_name] = dict_settings
        else:
            config.read(assets.path_settings_gui)
            dict_settings = {"geometry": self.geometry()}
            for key, value in dict_settings.items():
                config.set("settings", str(key), str(value))
            for key, value in self.save_mass_tree(self).items():
                config.set("settings", str(key), str(value))

        with open(assets.path_settings_gui, "w") as configfile:
            config.write(configfile)

        capture2Text.__init__(path_to_Capture2Text_CLI_exe=config["settings"]['entry_capture2text_path_to_capture2text_cli_exe'])
        tesseract.__init__(path_to_tesseract_exe=config["settings"]['entry_tesseract_path_to_tesseract_exe'])
        chatGpt.__init__(email=config["settings"]['entry_chatgpt_email'], password=config["settings"]['entry_chatgpt_password'], session_token=config["settings"]['entry_chatgpt_session_token'], access_token=config["settings"]['entry_chatgpt_access_token'])
        baidu.__init__(appid=config["settings"]['entry_baidu_appid'], apikey=config["settings"]['entry_baidu_apikey'], secretkey=config["settings"]['entry_baidu_secretkey'])

        self.disable_all_ocr_switchers()

    def save_mass(self, child, result={}):
        # print(child)
        if "checkbox" in child.winfo_name():
            # print("checkbox")
            # print(child.get())
            result[self.get_key(str(child))] = child.get()
        if "switch" in child.winfo_name():
            # print("switch")
            # print(child.get())
            result[self.get_key(str(child))] = child.get()
        if "ctkentry" in child.winfo_name():
            # print("ctkentry")
            # print(child.get())
            result[self.get_key(str(child))] = child.get()
        if "slider" in child.winfo_name():
            # print("slider")
            # print(child.get())
            result[self.get_key(str(child))] = child.get()
        if "segmented" in child.winfo_name():
            # print("segmented")
            # print(child.get())
            result[self.get_key(str(child))] = child.get()
        if "combobox" in child.winfo_name():
            # print("combobox")
            # print(child.get())
            result[self.get_key(str(child))] = child.get()
        if "optionmenu" in child.winfo_name():
            # print("optionmenu")
            # print(child.get())
            result[self.get_key(str(child))] = child.get().replace('%', '%%')
        if "textbox" in child.winfo_name():
            # print("textbox")
            # print(child.get(0.0, 'end-1c'))
            # print(str(child))
            # print(self.get_key(str(child)))
            # print(self.tabview_chat_ai1.get_key(str(child)))
            if self.get_key(str(child)) != "key doesn't exist":
                result[self.get_key(str(child))] = base64.b64encode(child.get("0.0", "end-1c").encode("utf-8")).decode("utf-8")
            else:
                result[self.tabview_chat_ai1.get_key(str(child))] = base64.b64encode(child.get("0.0", "end-1c").encode("utf-8")).decode("utf-8")
            #result[self.get_key(str(child))] = base64.b64encode(child.get("0.0", "end-1c").encode("utf-8")).decode("utf-8"),
        if "radiobutton" in child.winfo_name():
            print("radiobutton")
        return result

    def save_mass_tree(self, widget, dict_result_atr={}):
        dict_result_atr = self.save_mass(widget, dict_result_atr)
        for child in widget.winfo_children():
            dict_result_atr = self.save_mass_tree(child, dict_result_atr)
        # print(dict_result_atr)
        return dict_result_atr

    # load all gui elements from an ini file
    def load_mass(self, child, config, settings_name):
        # print(child)
        if "checkbox" in child.winfo_name():
            child.select() if int(config[settings_name][self.get_key(str(child))]) else child.deselect()
            if callable(child._command):
                child._command()
        if "switch" in child.winfo_name():
            child.select() if int(config[settings_name][self.get_key(str(child))]) else child.deselect()
            if callable(child._command):
                child._command()
        if "slider" in child.winfo_name():
            child.set(float(config[settings_name][self.get_key(str(child))]))
            if callable(child._command):
                child._command()
        if "segmented" in child.winfo_name():
            child.set(config[settings_name][self.get_key(str(child))])
            if callable(child._command):
                child._command()
        if "combobox" in child.winfo_name():
            child.set(config[settings_name][self.get_key(str(child))])
            if callable(child._command):
                child._command()
        if "ctkentry" in child.winfo_name():
            child.delete(0, "end")
            child.insert(0, config[settings_name][self.get_key(str(child))])
        if "textbox" in child.winfo_name():
            child.delete("0.0", "end")
            if self.get_key(str(child)) != "key doesn't exist":
                child.insert("0.0", base64.b64decode(config[settings_name][self.get_key(str(child))]).decode("utf-8"))
            else:
                child.insert("0.0", base64.b64decode(config[settings_name][self.tabview_chat_ai1.get_key(str(child))]).decode("utf-8"))
            #child.insert("0.0", base64.b64decode(config[settings_name][self.get_key(str(child))]).decode("utf-8"))
        if "radiobutton" in child.winfo_name():
            print("radiobutton")
        if "optionmenu" in child.winfo_name():
            # if re.search(r"ctkoptionmenu(?![\w\d\.])", str(child)):
            child.set(config[settings_name][self.get_key(str(child))])
            if callable(child._command):
                try:
                    child._command()
                except TypeError:
                    child._command(config[settings_name][self.get_key(str(child))])

    def load_mass_tree(self, widget, config={}, settings_name=""):
        self.load_mass(widget, config, settings_name)
        for child in widget.winfo_children():
            self.load_mass_tree(child, config, settings_name)

    def load_setting(self, settings_name="settings", first_time=False):
        config = configparser.ConfigParser()
        if not os.path.exists(assets.path_settings_gui) or first_time:
            self.save_setting(first_time=True)
            first_time = True
        config.read(assets.path_settings_gui)
        try:
            self.geometry(config[settings_name]["geometry"])
            self.load_mass_tree(self, config, settings_name)
            if first_time:
                self.geometry(f"{1100}x{580}")
        except KeyError:
            self.load_setting(first_time=True)


if __name__ == "__main__":
    app = ComplexTkGui()
    app.mainloop()
