from secrets import compare_digest
from aip import AipOcr


class Baidu:
    def __init__(self, appid="", apikey="", secretkey="") -> None:
        self.baidu_client = None
        if not compare_digest(appid, "") and not compare_digest(apikey, "") and not compare_digest(secretkey, ""):
            self.appid = appid
            self.apikey = apikey
            self.secretkey = secretkey
            self.is_active = True
            self.renew_chatbot_session_password()
        else:
            self.is_active = False

    def renew_chatbot_session_password(self):
        try:
            self.baidu_client = AipOcr(self.appid, self.apikey, self.secretkey)
        except Exception as e:
            self.is_active = False
            print(e)
            print("appid or apikey or secretkey are invalid")

    def run_ocr(self, img) -> str:
        result = self.baidu_client.basicGeneral(img)
        result = self.get_result_text(result)
        return result

    def get_result_text(self, json):
        s = ''
        if json.__contains__('words_result_num') and json['words_result_num'] > 0:
            for i in range(0, json['words_result_num']):
                s += json['words_result'][i]['words']
                s += '\r\n'
        else:
            # s += '"text not found"！'
            s += ''
        return s
