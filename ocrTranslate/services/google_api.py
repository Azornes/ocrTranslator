import io
import os
import platform
import subprocess

import wx.adv
from PIL.Image import Image

from google.cloud import texttospeech
from google.cloud.translate import TranslationServiceClient as TranslateClient
from google.cloud.vision import ImageAnnotatorClient
from google.oauth2 import service_account


class GoogleAPI:
    def __init__(self, path_service_account_creds="", ) -> None:
        if os.path.exists(path_service_account_creds):
            self.credentials = service_account.Credentials.from_service_account_file(path_service_account_creds)
            self.translate_client = TranslateClient(credentials=self.credentials)
            self.vision_client = ImageAnnotatorClient(credentials=self.credentials)
            self.text_to_speech_client = texttospeech.TextToSpeechClient(credentials=self.credentials)
            self.is_active = True
        else:
            self.is_active = False
        # stdout colors
        self.GREEN = "\033[92m"
        self.WARNING = "\033[93m"
        self.ENDCOLOR = "\033[0m"

    def text_to_wav(self, voice_name: str, text: str):
        language_code = "-".join(voice_name.split("-")[:2])
        text_input = texttospeech.SynthesisInput(text=text)
        voice_params = texttospeech.VoiceSelectionParams(language_code=language_code, name=voice_name)
        audio_config = texttospeech.AudioConfig(audio_encoding=texttospeech.AudioEncoding.LINEAR16)

        client = texttospeech.TextToSpeechClient(credentials=self.credentials)
        response = client.synthesize_speech(input=text_input, voice=voice_params, audio_config=audio_config)

        print(response)
        print(response.audio_content)

        filename = f"{language_code}.wav"
        with open(filename, "wb") as out:
            out.write(response.audio_content)
            print(f'Generated speech saved to "{filename}"')

        # np. jak wywolac funkcje: text_to_wav("pl-PL-Wavenet-B", "jakis tekst do powiedzenia a co?")

    # text_to_wav("pl-PL-Wavenet-B", "jakis tekst do powiedzenia a co?")

    def ocr_by_google_api(self, image: Image) -> str:
        """Detect text from PIL.Image data using Google Cloud Translate."""

        # Create bytestream of the given image
        bytes_io = io.BytesIO()
        image.save(bytes_io, 'png')
        bytes_io.seek(0)
        content = bytes_io.read()
        bytes_io.close()

        res = self.vision_client.text_detection({
            'content': content, })
        # print(res)

        annotations = res.text_annotations
        if len(annotations) > 0:
            text = annotations[0].description
        else:
            text = ""
        # print("Extracted text:\n {} from image ({} chars).".format(text, len(text)))
        # print("{}".format(text))

        '''
        # Filter small characters
        def _calc_height(word):
            """Calculate the height of the word boundary box."""
            ys = list(map(lambda v: v.y, word.bounding_box.vertices))
            return max(ys) - min(ys)
    
        texts = []
        max_height = 0
        for page in res.full_text_annotation.pages:
            for block in page.blocks:
                for paragraph in block.paragraphs:
                    max_height = max(max_height, max(map(_calc_height, paragraph.words)))
            for block in page.blocks:
                for paragraph in block.paragraphs:
                    for word in paragraph.words:
                        if _calc_height(word) > max_height * 0.60:
                            texts.append(''.join([symbol.text for symbol in word.symbols]))
                texts.append('\n')
        '''
        return "{}".format(text)

    def translate_by_google_api(self, text: str, target_language: str = 'en', source_language: str = 'ja') -> str:
        """
        from google.cloud import translate_v2 as translate2
        translate_client2 = translate2.Client(credentials=credentials)

        import six

        if isinstance(text, six.binary_type):
            text = text.decode("utf-8")

        # Text can also be a sequence of strings, in which case this method
        # will return a sequence of results for each text.
        result = translate_client2.translate(text, target_language=target)

        print(u"Text: {}".format(result["input"]))
        print(u"Translation: {}".format(result["translatedText"]))
        print(u"Detected source language: {}".format(result["detectedSourceLanguage"]))
        """
        return text

    def speech(self, text: str, langage_code: str = 'ja-JP') -> None:
        """Speak the text by Google Cloud Text-to-Speech voice synthesis."""

        # Create synthesis voice data
        temp_file = 'tmp.mp3'
        synthesis_input = texttospeech.types.SynthesisInput(text=text)
        voice = texttospeech.types.VoiceSelectionParams(language_code=langage_code, ssml_gender=texttospeech.enums.SsmlVoiceGender.FEMALE, )
        audio_config = texttospeech.types.AudioConfig(audio_encoding=texttospeech.enums.AudioEncoding.MP3)
        response = self.text_to_speech_client.synthesize_speech(synthesis_input, voice, audio_config)
        with open(temp_file, 'wb') as f:
            f.write(response.audio_content)

        # Play sound
        system = platform.system()
        if system == 'Windows':
            cmd = 'cmdmp3 {}'.format(temp_file)
            subprocess.call(cmd)
        else:
            wx.adv.Sound.PlaySound(temp_file, flags=wx.adv.SOUND_SYNC)

        # Windows has a problem in making temp files
        # ref: https://github.com/bravoserver/bravo/issues/111
        try:
            os.unlink(temp_file)
        except FileNotFoundError:
            pass
