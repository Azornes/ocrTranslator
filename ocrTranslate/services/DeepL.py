import asyncio

import deepl
from ocrTranslate.langs import _langs


class DeepL:
    def __init__(self) -> None:
        self.email = None
        try:
            self.deepl_init = deepl.DeepLCLI("auto", "en")
        except Exception as e:
            self.deepl_init = None
            print(e)

    # deepl-translate library
    def translate_by_special_point_deepL_old(self, word, language_from="english", language_to="polish"):
        words = ""
        if type(word) != str:
            for i in word:
                if i != "":
                    words = words + i + "\n"
        else:
            words = word

        # print(str(word.replace("%0A", "")))
        result = deepl.translate(source_language=language_from, target_language=language_to, text=words)
        return result

    # deepl-cli library
    def translate_by_special_point_deepL(self, word, language_from="english", language_to="polish"):
        _language_to = list(_langs.keys())[list(_langs.values()).index(language_to)]
        _language_from = list(_langs.keys())[list(_langs.values()).index(language_from)]
        words = ""
        if type(word) != str:
            for i in word:
                if i != "":
                    words = words + i + "\n"
        else:
            words = word
        self.deepl_init.to_lang = _language_to
        self.deepl_init.from_lang = _language_from
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        result = self.deepl_init.translate(words)
        return result

