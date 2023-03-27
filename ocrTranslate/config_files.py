from configparser import RawConfigParser

from ocrTranslate.services.baidu import Baidu
from ocrTranslate.services.capture2text import Capture2Text
from ocrTranslate.services.google_free import GoogleFree
from ocrTranslate.services.google_api import GoogleAPI
from ocrTranslate.services.chatGPT_free3 import ChatGPTFree
from ocrTranslate.services.DeepL import DeepL
from ocrTranslate.services.mult_translators import MultiTranslators
from ocrTranslate.assets import Assets as assets
from aip import AipOcr

from ocrTranslate.services.tesseract import Tesseract

google_free = GoogleFree()
google_api = GoogleAPI(path_service_account_creds=assets.path_service_account_creds)

config = RawConfigParser()

# config.read(assets.path_config_ini)
#
# capture2Text = Capture2Text(path_to_Capture2Text_CLI_exe=config['Capture2Text']["path_to_Capture2Text_CLI_exe"])
# # chatGpt = ChatGPT(config['ChatGPT']["ApiKey"], "api")
# # chatGpt = ChatGPTFree(config['ChatGPT']["session_token"])
# chatGpt = ChatGPTFree(config['ChatGPT']["email"], config['ChatGPT']["password"])
# baidu_client = AipOcr(config['Baidu']["AppId"], config['Baidu']["ApiKey"], config['Baidu']["SecretKey"])

config.read(assets.path_settings_gui)

try:
    capture2Text = Capture2Text(path_to_Capture2Text_CLI_exe=config["settings"]['entry_capture2text_path_to_capture2text_cli_exe'])
except KeyError:
    capture2Text = Capture2Text()

try:
    tesseract = Tesseract(path_to_tesseract_exe=config["settings"]['entry_tesseract_path_to_tesseract_exe'])
except KeyError:
    tesseract = Tesseract()

try:
    chatGpt = ChatGPTFree(email=config["settings"]['entry_chatgpt_email'],
                          password=config["settings"]['entry_chatgpt_password'],
                          session_token=config["settings"]['entry_chatgpt_session_token'],
                          access_token=config["settings"]['entry_chatgpt_access_token']
                          )
except KeyError:
    chatGpt = ChatGPTFree()

try:
    baidu = Baidu(appid=config["settings"]['entry_baidu_appid'], apikey=config["settings"]['entry_baidu_apikey'], secretkey=config["settings"]['entry_baidu_secretkey'])
except KeyError:
    baidu = Baidu()


deepL = DeepL()
multi_translators = MultiTranslators()