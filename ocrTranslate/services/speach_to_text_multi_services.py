import asyncio
import threading
import time
from typing import AsyncGenerator
import speech_recognition as sr
from speech_recognition import WaitTimeoutError
import multiprocessing.pool
import functools

from ocrTranslate.langs import convert_language_sst


def timeout(max_timeout):
    """Timeout decorator, parameter in seconds."""

    def timeout_decorator(item):
        """Wrap the original function."""

        @functools.wraps(item)
        def func_wrapper(*args, **kwargs):
            """Closure for function."""
            pool = multiprocessing.pool.ThreadPool(processes=1)
            async_result = pool.apply_async(item, args, kwargs)
            # raises a TimeoutError if execution exceeds max_timeout
            return async_result.get(max_timeout)

        return func_wrapper

    return timeout_decorator


class VoiceRecognizerMulti:
    def __init__(self, start_button=None, text_box=None, combobox_sst_language=None, language='pl-pl', name_service="google"):
        self.language = language
        self.stop = False
        self.combobox_sst_language = combobox_sst_language
        self.buttons_sst_list = start_button
        self.sst_frame_textbox_list = text_box
        self.name_service = name_service

        for button in self.buttons_sst_list:
            button.configure(command=lambda b=button: self.on_start_button_click(b))

        self.thread = threading.Thread(target=lambda: None)

    def change_language(self):
        self.language = convert_language_sst(self.combobox_sst_language.get())
        print(self.language)

    def on_start_button_click(self, button = None):
        self.change_language()
        text_box = None
        if button is not None:
            for iteration, button2 in enumerate(self.buttons_sst_list):
                if button == button2:
                    text_box = self.sst_frame_textbox_list[iteration]
                    break
        print("klik")
        if not self.thread.is_alive():
            self.stop = True
            self.thread = threading.Thread(target=self.recognize_voice_wrapper, args=(button, text_box))
            self.thread.start()
        else:
            self.stop = False

    @timeout(20.0)
    def listen_voice2(self, source):
        r = sr.Recognizer()
        r.pause_threshold = 0.4
        r.non_speaking_duration = 0.39
        r.phrase_threshold = 0.3
        audio = r.listen(source, 1)
        return audio

    def listen_voice(self) -> AsyncGenerator[sr.AudioData, None]:
        import speech_recognition as sr
        sr = sr.Microphone()
        print(self.stop)
        with sr as source:
            while self.stop:
                try:
                    audio = self.listen_voice2(source)
                except WaitTimeoutError:
                    continue
                except Exception as e:
                    print("Error: " + str(e))
                    continue
                yield audio
        print("koniec")

    def recognize_voice(self, r, response, textbox):
        try:
            method_name = 'r.recognize_{}'.format(self.name_service.lower())
            method = eval(method_name)
            query = method(response, language=self.language)
            #query = r.recognize_whisper(response, language="english")
            print(f"{query}")
            textbox.insert("0.0 lineend", " " + query)
        except Exception as e:
            print("Error: " + str(e))
            query = "Nie rozpoznano"
            print(f"{query}")

    def recognize_voice_wrapper(self, button, textbox):
        print("start animacja")
        button.start_button(started_animation=self.stop)
        for button2 in self.buttons_sst_list:
            if button != button2:
                button2.configure(state="disabled")

        if textbox.get("0.0", "0.0 lineend") != "":
            textbox.insert("0.0", "\n")
        r = sr.Recognizer()
        for response in self.listen_voice():
            print("koniec2")
            threading.Thread(target=self.recognize_voice, args=(r, response, textbox, )).start()

        print("koniec3")
        for button2 in self.buttons_sst_list:
            button2.configure(state="normal")
        print("koniec animacja")
        button.start_button(started_animation=self.stop)


    def run(self):
        self.thread = threading.Thread(target=self.recognize_voice_wrapper)
        self.thread.start()

    def start(self, name_service):
        self.name_service = name_service
        for button in self.buttons_sst_list:
            button.configure(command=lambda b=button: self.on_start_button_click(b))


# if __name__ == "__main__":
#     VoiceRecognizer().run()
