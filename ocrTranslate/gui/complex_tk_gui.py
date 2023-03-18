import customtkinter
from ocrTranslate.assets import Assets as assets
from ocrTranslate.gui.auto_complete_combobox import AutocompleteCombobox
from ocrTranslate.langs import _langs, services_translators_languages, _langs2

customtkinter.set_appearance_mode("System")  # Modes: "System" (standard), "Dark", "Light"
customtkinter.set_default_color_theme("blue")  # Themes: "blue" (standard), "green", "dark-blue"

result_boxes = []  # Result window identified earlier
from PIL import Image


class ComplexTkGui(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        # ||||||||||||||||||| configure window |||||||||||||||||||
        self.title("OCR_Translator")
        self.geometry(f"{1100}x{580}")

        # ||||||||||||||||||| configure grid layout |||||||||||||||||||
        self.grid_columnconfigure(0, weight=0)
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure(2, weight=1)
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=0)
        # ||||||||||||||||||| create sidebar frame with widgets |||||||||||||||||||

        self.rev_translate_icon = customtkinter.CTkImage(Image.open(assets.reverse_icon), size=(26, 26))

        # ||||||||||||||||||| create sidebar frame with widgets |||||||||||||||||||
        self.sidebar_frame = customtkinter.CTkFrame(self, width=100, corner_radius=0)

        self.logo_label = customtkinter.CTkLabel(self.sidebar_frame, text="OCR_Translator", font=customtkinter.CTkFont(size=20, weight="bold"))
        self.logo_label.grid(row=0, column=0, padx=20, pady=(20, 10))
        self.appearance_mode_label = customtkinter.CTkLabel(self.sidebar_frame, text="Appearance Mode:", anchor="w")
        self.appearance_mode_label.grid(row=1, column=0, padx=20, pady=(10, 0))
        self.appearance_mode_optionemenu = customtkinter.CTkOptionMenu(self.sidebar_frame, values=["Light", "Dark", "System"], command=self.change_appearance_mode_event)
        self.appearance_mode_optionemenu.grid(row=2, column=0, padx=20, pady=(10, 10))
        self.scaling_label = customtkinter.CTkLabel(self.sidebar_frame, text="UI Scaling:", anchor="w")
        self.scaling_label.grid(row=3, column=0, padx=20, pady=(10, 0))
        self.scaling_optionemenu = customtkinter.CTkOptionMenu(self.sidebar_frame, values=["80%", "90%", "100%", "110%", "120%"], command=self.change_scaling_event)
        self.scaling_optionemenu.grid(row=4, column=0, padx=20, pady=(10, 20))

        # ||||||||||||||||||| create scrollable frame |||||||||||||||||||
        self.scrollable_frame = customtkinter.CTkScrollableFrame(self, label_text="OCR Checker")
        self.scrollable_frame.grid(row=0, column=1, padx=(20, 0), pady=(20, 0), sticky="nsew")
        self.scrollable_frame.grid_columnconfigure((0, 1, 2, 3), weight=1)
        # self.scrollable_frame.grid_columnconfigure("all", weight=1)

        self.switch_ocr_google_api = None
        self.switch_ocr_google_free = None
        self.switch_ocr_baidu_api = None
        self.switch_ocr_capture2text = None
        self.switch_ocr_windows_local = None
        self.switches_ocr = []

        switchers = [("Google api",), ("Google Free",),
                     ("Baidu api",), ("Capture2Text",),
                     ("Windows local",),
                    ]

        rows = len(switchers)//2
        for i, switcher in enumerate(switchers):
            method_name = 'switch_ocr_{}'.format(switcher[0].lower().replace(" ", "_"))
            switch = customtkinter.CTkSwitch(self.scrollable_frame, text="Turn " + switcher[0])
            switch.grid(row=i // 2, column=(i % 2) + 1, padx=0, pady=(0, 10), sticky="NSEW")
            setattr(self, method_name, switch)
            self.switches_ocr.append(switch)

        self.switch_from_text = customtkinter.CTkSwitch(self.scrollable_frame, text="Only from below text", command=self.disable_all_ocr_switchers)
        self.switch_from_text.grid(row=rows+1, column=1, padx=0, pady=(0, 10), sticky="NSEW")

        self.switch_from_clipboard = customtkinter.CTkSwitch(self.scrollable_frame, text="Only from clipboard", command=self.disable_all_ocr_switchers)
        self.switch_from_clipboard.grid(row=rows+1, column=2, padx=0, pady=(0, 10), sticky="NSEW")

        # self.scrollable_frame_textbox = customtkinter.CTkTextbox(self, width=250)
        # self.scrollable_frame_textbox.grid(row=1, column=1,padx=(10, 10), pady=(10, 10), sticky="nsew")

        self.scrollable_frame_textbox = customtkinter.CTkTextbox(self.scrollable_frame, height=1500)
        self.scrollable_frame_textbox.grid(row=rows+2, column=0, columnspan=4, rowspan=10, padx=(10, 10), pady=(10, 10), sticky="NSEW")

        # ||||||||||||||||||| create tabview |||||||||||||||||||
        self.tabview = customtkinter.CTkTabview(self, width=25)
        self.tabview.grid(row=0, column=2, padx=(20, 20), pady=(3, 0), sticky="nsew")
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

        self.option_menu_translation = customtkinter.CTkOptionMenu(self.scrollable_frame_translation, dynamic_resizing=False, values=["Disabled", "GoogleFree", "ChatGPT", "DeepL", 'Alibaba', 'Argos', 'Baidu', 'Bing', 'Caiyun', 'Google', 'Iciba', 'Iflytek', 'Iflyrec', 'Itranslate', 'Lingvanex', 'Mglip', 'ModernMt', 'myMemory', 'Niutrans', 'Papago', 'qqFanyi', 'qqTranSmart', 'Reverso', 'Sogou', 'TranslateCom', 'Utibet', 'VolcEngine', 'Yandex', 'Youdao'], command=self.change_languages)
        self.option_menu_translation.grid(row=0, column=0, columnspan=3, padx=20, pady=(20, 10))

        self.switch_game_mode = customtkinter.CTkSwitch(self.scrollable_frame_translation, text="Turn game mode", )
        self.switch_game_mode.grid(row=1, column=0, padx=10, pady=(0, 20))

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

        self.translation_frame_textbox = customtkinter.CTkTextbox(self.scrollable_frame_translation, width=250, height=2000)
        self.translation_frame_textbox.grid(row=4, column=0, columnspan=3, padx=(10, 10), pady=(10, 10), sticky="nsew")

        # ||| Speech to Text tab |||
        self.label_tab_2 = customtkinter.CTkLabel(self.tabview.tab("Speech to Text"), text="WORK IN PROGRESS")
        self.label_tab_2.grid(row=0, column=0, padx=20, pady=20)

        # ||| Text to Speech tab |||
        self.label_tab_3 = customtkinter.CTkLabel(self.tabview.tab("Text to Speech"), text="WORK IN PROGRESS")
        self.label_tab_3.grid(row=0, column=0, padx=20, pady=20)

        # ||||||||||||||||||| create main entry and button |||||||||||||||||||
        self.button_start = customtkinter.CTkButton(master=self, text="START", fg_color="transparent", border_width=2, text_color=("gray10", "#DCE4EE"), command=self.pressed_print)
        self.button_start.grid(row=1, column=2, columnspan=2, padx=(20, 20), pady=(20, 20))
        self.button_options = customtkinter.CTkButton(master=self, text="Options", fg_color="transparent", border_width=2, text_color=("gray10", "#DCE4EE"), command=self.hide_show_side_bar)
        self.button_options.grid(row=1, column=1, padx=(20, 20), pady=(20, 20))

        # ||||||||||||||||||| set default values |||||||||||||||||||
        self.appearance_mode_optionemenu.set("Dark")
        self.scaling_optionemenu.set("100%")
        self.option_menu_translation.set("Disabled")

    def hide_show_side_bar(self):
        if self.sidebar_frame.winfo_manager() == "grid":
            self.sidebar_frame.grid_forget()
        else:
            self.sidebar_frame.grid(row=0, column=0, rowspan=4, sticky="nsew")
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
        if self.option_menu_translation.get().lower() in services_translators_languages.keys():
            lista = services_translators_languages.get(self.option_menu_translation.get().lower(), [])
            c = [_langs.get(a, a) for a in lista]
            self.combobox_from_language.configure(completevalues=c)
            self.combobox_to_language.configure(completevalues=c)

            if self.combobox_from_language.get() not in c:
                self.combobox_from_language.set("auto")
            if self.combobox_to_language.get() not in c:
                self.combobox_to_language.set("")
        elif self.option_menu_translation.get() == "ChatGPT" or self.option_menu_translation.get() == "GoogleFree":
            self.combobox_from_language.configure(completevalues=list(_langs2.values()))
            self.combobox_to_language.configure(completevalues=list(_langs2.values()))

            if self.combobox_from_language.get() not in list(_langs2.values()):
                self.combobox_from_language.set("auto")
            if self.combobox_to_language.get() not in list(_langs2.values()):
                self.combobox_to_language.set("")



    def combo_pressed_print(self, test):
        print(test)
        print("button click")

    def sidebar_button_event(self):
        print("sidebar_button click")
        print(self.optionmenu_translation.get())


if __name__ == "__main__":
    app = ComplexTkGui()
    app.mainloop()
