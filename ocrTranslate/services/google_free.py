import os
import re
import time
import logging
import base64
import requests

from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from pyshadow.main import Shadow

from ocrTranslate.assets import Assets as assets
from ocrTranslate.utils import list_to_string
from ocrTranslate.langs import _langs


class GoogleFree:
    def __init__(self, ) -> None:
        self.script_string: str = "var items = {}; for (index = 0; index < arguments[0].attributes.length; ++index) { items[arguments[0].attributes[index].name] = arguments[0].attributes[index].value }; return items;"
        with open(assets.path_to_test_image, 'rb') as img:
            print("Initializing ocr_google_free...")
            b64_string = base64.b64encode(img.read())
            self.ocr_google_free(b64_string.decode('utf-8'))
        # stdout colors
        self.GREEN: str = "\033[92m"
        self.WARNING: str = "\033[93m"
        self.ENDCOLOR: str = "\033[0m"

    def print_web_element(self, web_element_info):
        driver = web_element_info.parent

        attributes_element_dict = driver.execute_script(self.script_string, web_element_info)
        element_text = web_element_info.text
        element_size = web_element_info.size
        element_location = web_element_info.location

        print("█▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀█")
        print(web_element_info)
        print("attributes: " + str(attributes_element_dict))
        print('element.text: {0}'.format(element_text))
        print('size: {0}'.format(element_size))
        print('location: {0}'.format(element_location))
        print("█▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄█")

    def show_captcha(self, driver):
        print("Spawning browser for google captcha...")
        print("Scroll down on site to resolve captcha")
        #file_path = "file:///" + os.getcwd() + "/GoogleFreeVision/1.html"
        file_path = "https://cloud.google.com/vision"
        #file_path = "https://cloud.google.com/vision/docs/drag-and-drop"
        driver.get(file_path)
        # print(driver.page_source)

        shadow = Shadow(driver)
        shadow.set_explicit_wait(5, 1)  # delay

        #iframe = shadow.find_element("body > div > p > cloudx-demo > iframe:nth-child(1)")  # Iframe #documents object
        iframe = shadow.find_element("#section-2 > div > cloudx-demo > iframe:nth-child(1)")  # Iframe #documents object

        driver.switch_to.frame(iframe)  # switching to #documents
        shadow = Shadow(driver)

        shadowDrop = shadow.find_element("div:nth-child(3) > div > label")
        shadowDrop = shadow.get_next_sibling_element(shadowDrop)
        # print_web_element(shadowDrop)

        # makes the item visible
        driver.execute_script("arguments[0].setAttribute(arguments[1], arguments[2]);", shadowDrop, "style", "display:inline-block!important")

        # shadowDrop.click()
        shadowDrop.send_keys(assets.path_to_point_image)

        shadowDrop = shadow.get_parent_element(shadowDrop)
        # self.print_web_element(shadowDrop)
        shadowDrop = shadow.get_parent_element(shadowDrop)
        # self.print_web_element(shadowDrop)
        shadowDrop = shadow.get_next_sibling_element(shadowDrop)
        # self.print_web_element(shadowDrop)
        shadowDrop = shadow.get_next_sibling_element(shadowDrop)
        # self.print_web_element(shadowDrop)

        style_element1 = driver.execute_script(self.script_string, shadowDrop)
        while True:
            style_element = driver.execute_script(self.script_string, shadowDrop)
            # print(style_element1)
            if style_element != style_element1:
                break
            time.sleep(1)
        print("Success resolve captcha, despawning browser...")
        driver.close()

    def refresh_session(self):
        option = Options()
        option.add_argument('--headless')

        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument('--user-agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.104 Safari/537.36"')

        driver = webdriver.Chrome(options=chrome_options)

        self.show_captcha(driver)

    def translate_by_special_point_google(self, word, language_to: str = "en") -> str:

        _language_to = list(_langs.keys())[list(_langs.values()).index(language_to)]
        words = ""
        if type(word) != str:
            for i in word:
                if i != "":
                    words = words + i + "%0A"
        else:
            words = word

        url = "https://clients5.google.com/translate_a/t?client=dict-chrome-ex&sl=auto&tl={language_to}&q=".format(language_to=_language_to) + words
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.104 Safari/537.36'}

        request_result = requests.get(url, headers=headers).json()
        # pprint.pprint(request_result)
        # print('[In English]: ' + request_result['alternative_translations'][0]['alternative'][0]['word_postproc'])
        # print('[Language Dectected]: ' + request_result['src'])

        # print(request_result)
        list_of_words_translated = []

        # line = request_result['sentences'][0]['trans']

        # print(line)

        # print(range(len(request_result['sentences'])))
        # for x in range(len(request_result['sentences'])):
        #    # print(request_result['sentences'][x]['trans'])
        #    line = request_result['sentences'][x]['trans'].strip().replace('\n', '')
        #    list_of_words_translated.append(line)

        # for x in range(len(request_result)):
        # print(request_result['sentences'][x]['trans'])
        # line = request_result[0][0].strip().replace('\n', '')
        # list_of_words_translated.append(line)
        line = request_result[0][0].strip().replace('\n', ' ')
        list_of_words_translated.append(line)

        result = list_to_string(list_of_words_translated)
        return result

    def ocr_google_free(self, image: str) -> str:
        token = "03AG"

        url = "https://cxl-services.appspot.com/proxy"
        querystring = {"url": "https://vision.googleapis.com/v1/images:annotate", "token": token}

        payload = "{\"requests\":[{\"image\":{\"content\":\"" + image + "\"},\"features\":[{\"type\":\"LANDMARK_DETECTION\",\"maxResults\":50},{\"type\":\"FACE_DETECTION\",\"maxResults\":50},{\"type\":\"OBJECT_LOCALIZATION\",\"maxResults\":50},{\"type\":\"LOGO_DETECTION\",\"maxResults\":50},{\"type\":\"LABEL_DETECTION\",\"maxResults\":50},{\"type\":\"DOCUMENT_TEXT_DETECTION\",\"maxResults\":50},{\"type\":\"SAFE_SEARCH_DETECTION\",\"maxResults\":50},{\"type\":\"IMAGE_PROPERTIES\",\"maxResults\":50},{\"type\":\"CROP_HINTS\",\"maxResults\":50}],\"imageContext\":{\"cropHintsParams\":{\"aspectRatios\":[0.8,1,1.2]}}}]}"

        headers = {'sec-ch-ua': "\" Not A;Brand\";v=\"99\", \"Chromium\";v=\"96\", \"Google Chrome\";v=\"96\"", 'dnt': "1", 'sec-ch-ua-mobile': "?0", 'user-agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36", 'sec-ch-ua-platform': "\"Windows\"", 'content-type': "text/plain;charset=UTF-8", 'accept': "*/*", 'sec-fetch-site': "cross-site", 'sec-fetch-mode': "cors", 'sec-fetch-dest': "empty", 'cache-control': "no-cache"}

        response = requests.request("POST", url, data=payload, headers=headers, params=querystring)

        # print(response.status_code)
        # print(response.reason)

        if response.status_code == 200:
            try:
                response_json = response.json()
            except Exception:
                logging.exception("An exception was thrown!")

            try:
                text = response_json.get("responses")[0].get("fullTextAnnotation").get("text")
            except Exception:
                logging.exception("An exception was thrown!")
                text = "text not found"
            print("OCR text by Google Free: ")
            print(text)
        else:
            print("Code Error: " + str(response.status_code) + " Reason Error: " + str(response.reason) + "\nError occurs in ocr_google_free")
            text = "text not found"
            self.refresh_session()

        return text

    def ocr_google_free_get_token(self):
        url = "https://www.google.com/recaptcha/api2/anchor"

        headers = {'sec-ch-ua': "\" Not A;Brand\";v=\"99\", \"Chromium\";v=\"96\", \"Google Chrome\";v=\"96\"", 'sec-ch-ua-mobile': "?0", 'sec-ch-ua-platform': "\"Windows\"", 'upgrade-insecure-requests': "1", 'dnt': "1", 'user-agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36", 'accept': "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9", 'sec-fetch-site': "cross-site", 'sec-fetch-mode': "navigate", 'sec-fetch-dest': "iframe", 'cache-control': "no-cache"}

        response = requests.request("GET", url, headers=headers)
        print(response.text)

        m = re.findall(r'(?<=<input type="hidden" id="recaptcha-token" value=").*?(?=">)', response.text)
        print(m[0])
