from revChatGPT.V1 import Chatbot as ChatbotFree


class ChatGPTFree:
    def __init__(self, email, password) -> None:
        if not email == "" and not password == "":
            self.email = email
            self.password = password
            self.chat_gpt_free = None
            self.is_active = True
            self.renew_chatbot_session()
        else:
            self.is_active = False

    def renew_chatbot_session(self):
        try:
            self.chat_gpt_free = ChatbotFree(config={"email": "{email}".format(email=self.email), "password": "{password}".format(password=self.password)})
        except Exception as e:
            self.is_active = False
            print(e)
            print("session token has been out of date, please renew token")

    async def translate_by_chat_gpt(self, word, language_to="English"):
        if self.is_active:
            words = ""
            if type(word) != str:
                for i in word:
                    if i != "":
                        words = words + i + "\n"
            else:
                words = word
            response = ""
            for data in self.chat_gpt_free.ask("Just translate the following sentence into {languageInText}, without any explanation and write only the translated sentence: {wordInText}".format(wordInText=words, languageInText=language_to)):
                response = data["message"]

            return response
        else:
            return "chatgpt non valid user date"
