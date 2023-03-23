from configparser import RawConfigParser

from ocrTranslate.services.capture2text import Capture2Text
from ocrTranslate.services.google_free import GoogleFree
from ocrTranslate.services.google_api import GoogleAPI
from ocrTranslate.services.chatGPT_free3 import ChatGPTFree
from ocrTranslate.services.DeepL import DeepL
from ocrTranslate.services.mult_translators import MultiTranslators
from ocrTranslate.assets import Assets as assets
from aip import AipOcr

google_free = GoogleFree()
google_api = GoogleAPI(path_service_account_creds=assets.path_service_account_creds)

config = RawConfigParser()
config.read(assets.path_config_ini)

capture2Text = Capture2Text(path_to_Capture2Text_CLI_exe=config['Capture2Text']["path_to_Capture2Text_CLI_exe"])
# chatGpt = ChatGPT(config['ChatGPT']["ApiKey"], "api")
# chatGpt = ChatGPTFree(config['ChatGPT']["session_token"])
chatGpt = ChatGPTFree(config['ChatGPT']["email"], config['ChatGPT']["password"])
deepL = DeepL()

baidu_client = AipOcr(config['Baidu']["AppId"], config['Baidu']["ApiKey"], config['Baidu']["SecretKey"])

multi_translators = MultiTranslators()