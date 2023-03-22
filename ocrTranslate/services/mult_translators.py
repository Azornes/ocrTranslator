from ocrTranslate.langs import _langs
import translators as ts


class MultiTranslators:
    def __init__(self) -> None:
        print(ts.translators_pool)
        #ts.preaccelerate()

    def translate(self, word, language_from="auto", language_to="english", translator="bing"):
        _language_to = list(_langs.keys())[list(_langs.values()).index(language_to)]
        _language_from = list(_langs.keys())[list(_langs.values()).index(language_from)]
        words = ""
        if type(word) != str:
            for i in word:
                if i != "":
                    words = words + i + "\n"
        else:
            words = word

        print(ts.translators_pool)
        return ts.translate_text(query_text=words, translator=translator, from_language=_language_from, to_language=_language_to)
