# OCR_Translator
Convert Capture Image To Text(with BaiduOCR, GoogleOCR, Capture2Text) and
translate text(with Google, Chatgpt, DeepL)
---
### dependency
1. [Python 3.9](https://www.python.org/downloads/release/python-390/).
2. [Capture2Text](https://sourceforge.net/projects/capture2text/).

to working you need create config.ini and generate [service_account_creds.json](https://developers.google.com/workspace/guides/create-credentials?hl=pl).
### how look example config.ini
```
[ChatGPT]
ApiKey = your_ApiKey
session_token = "your_session_token"
email = your_email
password = your_password

[Baidu]
AppId = your_appid
ApiKey = your_ApiKey
SecretKey = your_SecretKey

[Capture2Text]
path_to_Capture2Text_CLI_exe = C:\Program Files\Capture2Text\Capture2Text_CLI.exe
```

at this moment only supported chatgpt identification by email and password.

### how to get session token to chatgpt free (WIP)
1. Login to https://chat.openai.com
2. Open Console in your google chrome -> Application -> Storage -> Cookies -> https://chat.openai.com -> Value from __Secure-next-auth.session-token
