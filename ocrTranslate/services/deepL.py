import asyncio

import deepl
from ocrTranslate.langs import _langs, convert_language
from ocrTranslate.utils import format_words


class DeepL:
    def __init__(self) -> None:
        self.email = None
        try:
            self.deepl_init = deepl.DeepLCLI("auto", "en")
        except Exception as e:
            self.deepl_init = None
            print(e)

    # deepl-translate library
    def run_translate_old(self, word, language_from: str = "English", language_to: str = " Polish"):
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
    def run_translate(self, word, language_from: str = "English", language_to: str = "Polish"):
        self.deepl_init.from_lang, self.deepl_init.to_lang = convert_language(language_from, language_to)
        words = format_words(word)
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        result = self.deepl_init.translate(words)
        return result

    async def run_translate_async(self, word, language_from: str = "English", language_to: str = "Polish"):
        self.deepl_init.from_lang, self.deepl_init.to_lang = convert_language(language_from, language_to)
        words = format_words(word)
        return await self.deepl_init.translate_async(words)
