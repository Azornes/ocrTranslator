import os
import sys


def resolve_path(path):
    if getattr(sys, "frozen", False):
        resolved_path = os.path.abspath(os.path.join(sys._MEIPASS, path))
    else:
        resolved_path = os.path.abspath(os.path.join(os.getcwd(), path))
    return resolved_path


if not os.path.exists(resolve_path("ocrTranslate/temp")):
    os.makedirs(resolve_path("ocrTranslate/temp"))

if not os.path.exists(resolve_path("ocrTranslate/configs")):
    os.makedirs(resolve_path("ocrTranslate/configs"))


class Assets:
    path_to_icon = resolve_path("ocrTranslate/assets/icon.ico")
    path_to_icon2 = resolve_path("ocrTranslate/assets/icon2.ico")
    reverse_icon = resolve_path("ocrTranslate/assets/reverse.png")

    path_to_tmp = resolve_path("ocrTranslate/temp/temp.bmp")
    path_to_tmp2 = resolve_path("ocrTranslate/temp/temp.png")
    path_to_tmp3 = resolve_path("ocrTranslate/temp/temp.gif")
    path_to_tmp4 = resolve_path("ocrTranslate/temp/screencapture.png")

    path_to_test_image = resolve_path("ocrTranslate/assets/test_image.png")
    path_to_point_image = resolve_path("ocrTranslate/assets/point.jpg")

    path_config_ini = resolve_path("ocrTranslate/configs/config.ini")
    path_web_speech_demo = resolve_path("ocrTranslate\services\webspeechdemo\webspeechdemo.html")
    path_service_account_creds = resolve_path("ocrTranslate/configs/service_account_creds.json")
    path_cookies_edge_gpt = resolve_path("ocrTranslate/configs/cookies.json")
    path_settings_gui = resolve_path("ocrTranslate/configs/settings.ini")

    path_to_win_ocr = resolve_path("ocrTranslate/services/Get-Win10OcrTextFromImage.ps1")

    path_to_home_dark = resolve_path("ocrTranslate/assets/home_dark.png")
    path_to_home_light = resolve_path("ocrTranslate/assets/home_light.png")
    path_to_settings_dark = resolve_path("ocrTranslate/assets/settings_dark.png")
    path_to_settings_light = resolve_path("ocrTranslate/assets/settings_light.png")
    path_to_loading_gif = resolve_path("ocrTranslate/assets/loading.gif")
    path_to_loading_png = resolve_path("ocrTranslate/assets/loading.png")
    path_to_microphone_active_png = resolve_path("ocrTranslate/assets/microphone_active.png")
    path_to_chatai_black = resolve_path("ocrTranslate/assets/chatai_black.png")
    path_to_chatai_white = resolve_path("ocrTranslate/assets/chatai_white.png")
    path_to_microphone_white = resolve_path("ocrTranslate/assets/microphone_white.png")
    path_to_send_message_black = resolve_path("ocrTranslate/assets/send_message_black.png")
    path_to_send_message_white = resolve_path("ocrTranslate/assets/send_message_white.png")
    path_to_open_side_menu_dark = resolve_path("ocrTranslate/assets/open_side_menu_dark.png")
    path_to_open_side_menu_white = resolve_path("ocrTranslate/assets/open_side_menu_white.png")