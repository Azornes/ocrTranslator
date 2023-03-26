<p align="center">
  <h1 align="center">OCR Translator</h1>
  <p align="center"><i>Convert captured images into text and then translate that text.</i></p>
</p>

<p align="center">
   <a href="https://github.com/Azornes/ocrTranslator">
    <img alt="Visitors" src="https://shields-io-visitor-counter.herokuapp.com/badge?page=Azornes.ocrTranslator&color=1D70B8&logo=GitHub&logoColor=FFFFFF&style=flat-square">
   </a>
  <a href="https://www.python.org/">
    <img alt="python 3.9" src="https://img.shields.io/badge/python-3.9-3776AB?logo=Python&logoColor=FFFFFF&style=flat-square">
   </a>
</p>

---
With this app, you can select your preferred OCR and translation services. After clicking on START or using the keyboard shortcut Alt+Win+T, the program will launch and you can choose the area of the screen to scan for text using OCR. If you have selected a translation service, the text will then be automatically translated.

preview:
![](documentation_images/Showrun.gif)
---
### Dependency
1. [Python 3.9](https://www.python.org/downloads/release/python-390/).
2. (optional) [Capture2Text](https://sourceforge.net/projects/capture2text/).
3. (optional) [Tesseract](https://github.com/UB-Mannheim/tesseract/wiki).
4. (optional) Google api generate a [service_account_creds.json](https://developers.google.com/workspace/guides/create-credentials). Then, put file into the 'ocrTranslate/configs' directory.

<details>

<summary>

### (optional) ChatGPT
> #### [Source](https://github.com/acheong08/ChatGPT)
</summary>

## Configuration
1. Create account on [OpenAI's ChatGPT](https://chat.openai.com/)
2. Save your email and password
### Authentication method: (Choose 1 and paste to app settings)
#### - Email/Password
Not supported for Google/Microsoft accounts
#### - Session token
1. Login in to https://chat.openai.com
2. Open the console in Google Chrome -> Application -> Storage -> Cookies -> https://chat.openai.com -> Get the value from __Secure-next-auth.session-token
#### - Access token
https://chat.openai.com/api/auth/session
</details>


