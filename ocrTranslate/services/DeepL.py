import deepl
from ocrTranslate.langs import _langs


class DeepL:
    def __init__(self) -> None:
        self.email = None

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

        t = deepl.DeepLCLI(_language_from, _language_to)
        result = t.translate(words)
        return result

