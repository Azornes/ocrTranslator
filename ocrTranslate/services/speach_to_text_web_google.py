import threading
import time
from tkinter import *
from selenium import webdriver
from selenium.common import JavascriptException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from ocrTranslate.langs import convert_language_sst
from ocrTranslate.assets import Assets as assets

class SpeechRecognitionGUI:
    def __init__(self, start_button=None, change_language_button=None, text_box=None, combobox_sst_language=None):
        self.options = webdriver.ChromeOptions()
        self.options.add_argument("use-fake-ui-for-media-stream")
        # self.options.add_argument('headless')
        # self.options.add_argument('--headless')
        self.driver = webdriver.Chrome(chrome_options=self.options)
        # driver.get("data:text/html;charset=utf-8," + html_content)
        self.driver.get(assets.path_web_speech_demo)
        self.driver.minimize_window()
        self.combobox_sst_language = combobox_sst_language
        self.combobox_sst_language.configure(command=self.change_language)
        self.start_button = start_button
        # command = self.start_button._command
        # if callable(command):
        #     print("callable")
        #     self.start_button.configure(command=lambda: command() or self.on_start_button_click())
        # else:
        #     print("callable2")
        #     self.start_button.configure(command=self.on_start_button_click)
        self.start_button.configure(command=self.on_start_button_click)
        self.text_box = text_box
        self.thread = threading.Thread(target=lambda: None)

    def change_language(self, option):
        # from selenium.webdriver.support.ui import Select
        # select = Select(self.driver.find_element(By.ID, "select_language"))
        # select.select_by_visible_text("Deutsch")
        # print(option)
        # print(convert_language_sst(language_sst=option))
        script = f"for (var i = select_dialect.options.length - 1; i >= 0; i--) {{select_dialect.remove(i);}} select_dialect.options.add(new Option('{option}', '{convert_language_sst(language_sst=option)}'));"
        #script = '''for (var i = select_dialect.options.length - 1; i >= 0; i--) {{select_dialect.remove(i);}} select_dialect.options.add(new Option("Polski", "pl-PL"));'''
        # print(script)
        self.driver.execute_script(script)

    def on_start_button_click(self):
        try:
            self.driver.execute_script("startButton();")
        except JavascriptException:
            pass
        time.sleep(0.1)
        if not self.thread.is_alive():
            self.thread = threading.Thread(target=self.update_recognized_text)
            self.thread.start()

    def update_recognized_text(self):
        # print("update_recognized_text")
        recognizing = self.driver.execute_script("return recognizing;")
        self.start_button.start_button(started_animation=recognizing)
        if recognizing:
            self.text_box.insert("0.0", "\n")
        while recognizing:
            recognizing = self.driver.execute_script("return recognizing;")
            # print(recognizing)
            text_output_final = self.driver.find_element(By.ID, "final_span")
            recognized_text = text_output_final.text
            text_output_interim = self.driver.find_element(By.ID, "interim_span")
            recognized_text = recognized_text + text_output_interim.text
            # print(recognized_text)
            self.text_box.delete("0.0", "0.0 lineend")
            # response = recognized_text[len(prev_text):]
            # prev_text = recognized_text
            self.text_box.insert("0.0 lineend", recognized_text)
            time.sleep(0.1)
        # print(recognizing)
        self.start_button.start_button(started_animation=recognizing)

# if __name__ == "__main__":
#     SpeechRecognitionGUI()
