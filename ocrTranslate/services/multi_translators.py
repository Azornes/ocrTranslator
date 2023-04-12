from requests import ReadTimeout
import translators as ts
from ocrTranslate.utils import format_words
from ocrTranslate.langs import convert_language


class MultiTranslators:
    def __init__(self) -> None:
        print(ts.translators_pool)  # ts.preaccelerate()

    def run_translate(self, word, language_from="auto", language_to="English", translator="bing"):
        _language_from, _language_to = convert_language(language_from, language_to)
        words = format_words(word)
        # print(ts.translators_pool)
        try:
            result = ts.translate_text(query_text=words, translator=translator, from_language=_language_from, to_language=_language_to, timeout=30)
        except ReadTimeout:
            result = "Timeout, service is busy, try again later"
        except ts.server.TranslatorError:
            result = "Bad language, choose another language"

        return result
