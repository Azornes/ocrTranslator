<p align="center">
  <h1 align="center">OCR Translator</h1>
  <p align="center"><i>Convert captured images into text and then translate that text.</i></p>
</p>

<p align="center">
   <a href="https://github.com/Azornes/ocrTranslator/releases">
    <img alt="Downloads" src="https://img.shields.io/github/downloads/Azornes/ocrTranslator/latest/total?label=Downloads&style=flat-square">
   </a>
  <a href="https://visitorbadge.io/status?path=https%3A%2F%2Fgithub.com%2FAzornes%2FocrTranslator"><img src="https://api.visitorbadge.io/api/combined?path=https%3A%2F%2Fgithub.com%2FAzornes%2FocrTranslator&countColor=%2337d67a&style=flat-square&labelStyle=none" /></a>
    <img alt="python 3.9" src="https://img.shields.io/badge/python-3.9-3776AB?logo=Python&logoColor=FFFFFF&style=flat-square">
   </a>
</p>

---
With this app, you can select your preferred OCR and translation services. After clicking on START or using the keyboard shortcut Alt+Win+T, the program will launch and you can choose the area of the screen to scan for text using OCR. If you have selected a translation service, the text will then be automatically translated.

preview:

https://user-images.githubusercontent.com/20650591/233107070-f9a14ed8-5c77-4947-8fa5-8d1c86d4a04f.mp4

# 🔥 Features

- Desktop application with a user-friendly graphical user interface (GUI) provided by customtkinter.
- Ability to select preferred OCR and translation services.
- Option to run the program using either the START button or the keyboard shortcut (Alt+Win+T or bound from options).
- Capability to choose the area of the screen to scan for text using OCR and save the position (for example, when watching a movie and the subtitles always appear in one spot, so you don't have to select the text area again).
- Automatic translation of the captured text if a translation service has been selected.
- Ability to capture subtitles from movies or games by selecting the corresponding area of the screen and displaying the translated text next to them.
- Chat with chatGPT or edgeGPT.
- Ability to translate from the clipboard or manually entered text (similar to a typical translation app).
- Save all selected options and settings to a file and load them when the program is launched.

## Desktop App
Download the desktop app [here](https://github.com/Azornes/ocrTranslator/releases)
Tested only on Windows 10.

---
## Dependency
1. [Python 3.9](https://www.python.org/downloads/release/python-390/). (If you want run from source)
2. (optional) [Capture2Text](https://sourceforge.net/projects/capture2text/).
3. (optional) [Tesseract](https://github.com/UB-Mannheim/tesseract/wiki).
4. (optional) Google api generate a [service_account_creds.json](https://developers.google.com/workspace/guides/create-credentials). Then, put file into the `ocrTranslate/configs` directory.
<details>
<summary>

### 5. (optional) ChatGPT
> #### [Source](https://github.com/acheong08/ChatGPT)
</summary>

## Configuration
1. Create account on [OpenAI's ChatGPT](https://chat.openai.com/)
2. Save your email and password
### Authentication method: (Choose 1 and paste to app settings)

#### - Email/Password
> _Currently broken for free users. Do `export PUID="..."` if you have a plus account. The PUID is a cookie named `_puid`_
> Not supported for Google/Microsoft accounts.

#### - Access token
https://chat.openai.com/api/auth/session

</details>

<details>
  <summary>

### 6. (optional) EdgeGPT
> #### [Source](https://github.com/acheong08/ChatGPT)
  </summary>

<details>
  <summary>

#### Checking access (Required)

  </summary>

- Install the latest version of Microsoft Edge
- Alternatively, you can use any browser and set the user-agent to look like you're using Edge (e.g., `Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36 Edg/111.0.1661.51`). You can do this easily with an extension like "User-Agent Switcher and Manager" for [Chrome](https://chrome.google.com/webstore/detail/user-agent-switcher-and-m/bhchdcejhohfmigjafbampogmaanbfkg) and [Firefox](https://addons.mozilla.org/en-US/firefox/addon/user-agent-string-switcher/).
- Open [bing.com/chat](https://bing.com/chat)
- If you see a chat feature, you are good to go

</details>

<details>
  <summary>

#### Getting authentication (Required)

  </summary>

- Install the cookie editor extension for [Chrome](https://chrome.google.com/webstore/detail/cookie-editor/hlkenndednhfkekhgcdicdfddnkalmdm) or [Firefox](https://addons.mozilla.org/en-US/firefox/addon/cookie-editor/)
- Go to `bing.com`
- Open the extension
- Click "Export" on the bottom right, then "Export as JSON" (This saves your cookies to clipboard)
- Paste your cookies into a file `cookies.json`
- Paste your file `cookies.json` to `ocrTranslate/configs/`

</details>

</details>

---

# 📊 Tables with information

<details>
<summary>

### Supported OCR Services
</summary>

| ID  | OCR                                                                                                   | Internet/Local | Status |
|-----|-------------------------------------------------------------------------------------------------------|----------------|--------|
| 1   | [Google Vision Api](https://cloud.google.com/vision/docs/ocr)                                         | Internet       | stable |
| 2   | [Google Vision Free Demo](https://cloud.google.com/vision/docs/drag-and-drop)                         | Internet       | stable |
| 3   | [Baidu Api](https://intl.cloud.baidu.com/product/ocr.html)                                            | Internet       | stable |
| 4   | [Windows OCR](https://learn.microsoft.com/en-us/uwp/api/windows.media.ocr.ocrengine?view=winrt-22621) | Local          | stable |
| 5   | [Capture2Text](https://capture2text.sourceforge.net/)                                                 | Local          | stable |
| 6   | [Tesseract](https://tesseract-ocr.github.io/tessdoc/)                                                 | Local          | stable |
| 7   | [RapidOCR](https://github.com/RapidAI/RapidOCR)                                                       | Local          | stable |
</details>


<details>
<summary>

### Supported Translation Services
> #### [Source](https://github.com/uliontse/translators)
</summary>

| ID  | Translator                                                                        | Number of Supported Languages | Advantage                                                                                   | Service                                                                                                           | Status                          |
|-----|-----------------------------------------------------------------------------------|-------------------------------|---------------------------------------------------------------------------------------------|-------------------------------------------------------------------------------------------------------------------|---------------------------------|
| 1   | [Niutrans](https://niutrans.com/trans)                                            | 302                           | support the most languages in the world                                                     | [Northeastern University](http://english.neu.edu.cn/) / [Niutrans](https://github.com/NiuTrans), China            | /                               |
| 2   | [Alibaba](https://translate.alibaba.com)                                          | 221                           | support most languages, support professional field                                          | [Alibaba](https://damo.alibaba.com/about?lang=en), China                                                          | stable                          |
| 3   | [Baidu](https://fanyi.baidu.com)                                                  | 201                           | support most languages, support professional field, support Classical Chinese               | [Baidu](https://ir.baidu.com/company-overview), China                                                             | stable                          |
| 4   | [Iciba](https://www.iciba.com/fy)                                                 | 187                           | support the most languages in the world                                                     | [Kingsoft](https://www.wps.com/about-us/) / [Xiaomi](https://www.mi.com/us/about/), China                         | stable                          |
| 5   | [MyMemory](https://mymemory.translated.net)                                       | 151                           | support the most languages in the world, good at Creole English, Creole French              | [Translated](https://translatedlabs.com/welcome), Italy                                                           | stable                          |
| 6   | [Iflytek](https://fanyi.xfyun.cn/console/trans/text)                              | 140                           | support the most languages in the world                                                     | [Iflytek](https://www.iflytek.com/en/about-us.html), China                                                        | /                               |
| 7   | [Google](https://translate.google.com)                                            | 134                           | support more languages in the world                                                         | [Google](https://about.google/), America                                                                          | stable(offline in China inland) |
| 8   | [VolcEngine](https://translate.volcengine.com)                                    | 122                           | support more languages in the world, support professional field                             | [ByteDance](https://www.bytedance.com/en/), China                                                                 | /                               |
| 9   | [Lingvanex](https://lingvanex.com/demo)                                           | 112                           | support translation of different regions but the same language                              | [Lingvanex](https://lingvanex.com/about-us/), Cyprus                                                              | stable                          |
| 10  | [Bing](https://www.bing.com/Translator)                                           | 110                           | support more languages in the world                                                         | [Microsoft](https://www.microsoft.com/en-us/about), America                                                       | stable                          |
| 11  | [Yandex](https://translate.yandex.com)                                            | 102                           | support more languages in the world, support word to emoji                                  | [Yandex](https://yandex.com/company/), Russia                                                                     | /                               |
| 12  | [Itranslate](https://itranslate.com/webapp)                                       | 101                           | support translation of different regions but the same language, such as en-US, en-UK, en-AU | [Itranslate](https://itranslate.com/about), Austria                                                               | stable                          |
| 13  | [Sogou](https://fanyi.sogou.com)                                                  | 61                            | support more languages in the world                                                         | [Tencent](https://www.tencent.com/en-us/about.html), China                                                        | stable                          |
| 14  | [ModernMt](https://www.modernmt.com/translate)                                    | 56                            | open-source, support more languages in the world                                            | [Modernmt](https://github.com/modernmt) / [Translated](https://translatedlabs.com/welcome), Italy                 | stable                          |
| 15  | [SysTran](https://www.systran.net/translate/)                                     | 52                            | support more languages in the world                                                         | [SysTran](https://www.systran.net/about/), France                                                                 | stable                          |
| 16  | [Apertium](https://www.apertium.org/)                                             | 45                            | open-source                                                                                 | [Apertium](https://github.com/apertium)                                                                           | stable                          |
| 17  | [Reverso](https://www.reverso.net/text-translation)                               | 42                            | popular on Mac and Iphone                                                                   | [Reverso](https://www.corporate-translation.reverso.com/about-us), France                                         | stable                          |
| 18  | [CloudYi](https://www.cloudtranslation.com/#/translate)                           | 28                            | support main languages                                                                      | [Xiamen University](http://nlp.xmu.edu.cn/) / [CloudTranslation](https://www.cloudtranslation.com/#/about), China | stable                          |
| 19  | [Deepl](https://www.deepl.com/translator)                                         | 27                            | high quality to translate but response slowly                                               | [Deepl](https://jobs.deepl.com/l/en), Germany                                                                     | stable                          |
| 20  | [QQTranSmart](https://transmart.qq.com)                                           | 22                            | support main languages                                                                      | [Tencent](https://www.tencent.com/en-us/about.html), China                                                        | stable                          |
| 21  | [TranslateCom](https://www.translate.com/machine-translation)                     | 21                            | good at English translation                                                                 | [TranslateCom](https://www.translate.com/about-us), America                                                       | stable                          |
| 22  | [Tilde](https://translate.tilde.com/)                                             | 21                            | good at lv, de, fr translation                                                              | [Tilde](https://tilde.com/about), Latvia                                                                          | /                               |
| 23  | [QQFanyi](https://fanyi.qq.com)                                                   | 17                            | support main languages                                                                      | [Tencent](https://www.tencent.com/en-us/about.html), China                                                        | stable                          |
| 24  | [Argos](https://translate.argosopentech.com)                                      | 17                            | open-source                                                                                 | [Argos](https://github.com/argosopentech) / [Libre](https://github.com/LibreTranslate), America                   | stable                          |
| 25  | [TranslateMe](https://translateme.network/)                                       | 16                            | good at English translation                                                                 | [TranslateMe](https://translateme.network/our-team/) / [Neosus](https://neosus.net/about/), Lithuania             | stable                          |
| 26  | [Youdao](https://ai.youdao.com/product-fanyi-text.s)                              | 15                            | support main languages, high quality                                                        | [Netease](https://ir.netease.com/company-overview/corporate-profile), China                                       | stable                          |
| 27  | [Papago](https://papago.naver.com)                                                | 15                            | good at Korean translation                                                                  | [Naver](https://www.navercorp.com/en/naver/company), South Korea                                                  | stable                          |
| 28  | [Marai](https://miraitranslate.com/trial/)                                        | 15                            | good at Japanese translation                                                                | [MaraiTranslate](https://miraitranslate.com/en/company/), Japan                                                   | /                               |
| 29  | [Iflyrec](https://fanyi.iflyrec.com)                                              | 12                            | good at Chinese translation                                                                 | [Iflytek](https://www.iflytek.com/en/about-us.html), China                                                        | stable                          |
| 30  | [Yeekit](https://www.yeekit.com/site/translate)                                   | 10                            | support main languages                                                                      | [CTC](https://www.ctpc.com.cn/cms/enAboutUs.htm), China                                                           | stable                          |
| 31  | [LanguageWire](https://www.languagewire.com/en/technology/languagewire-translate) | 8                             | good at English translation                                                                 | [LanguageWire](https://www.languagewire.com/about-us), Denmark                                                    | stable                          |
| 32  | [Caiyun](https://fanyi.caiyunapp.com)                                             | 7                             | high quality to translate but response slowly, support professional field                   | [ColorfulClouds](http://caiyunapp.com/jobs/), China                                                               | stable                          |
| 33  | [Elia](https://elia.eus/translator)                                               | 6                             | good at Basque translation                                                                  | [Elhuyar](https://www.elhuyar.eus/eu/nor-gara), Spain                                                             | stable                          |
| 34  | [Judic](https://judic.io/en/translate)                                            | 4                             | good at European translation                                                                | [CrossLang](https://crosslang.com/about-us/), Belgium                                                             | stable                          |
| 35  | [Mglip](http://fy.mglip.com/pc)                                                   | 3                             | good at Mongolia translation                                                                | [Inner Mongolia University](https://www.imu.edu.cn/yw/Home.htm), China                                            | stable                          |
| 36  | [Utibet](http://mt.utibet.edu.cn/mt)                                              | 2                             | good at Tibet translation                                                                   | [Tibet University](http://www.utibet.edu.cn/), China                                                              | stable                          |


</details>

---
