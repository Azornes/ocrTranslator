import os
import sys


def resolve_path(path):
    if getattr(sys, "frozen", False):
        # If the 'frozen' flag is set, we are in bundled-app mode!
        resolved_path = os.path.abspath(os.path.join(sys._MEIPASS, path))
    else:
        # Normal development mode. Use os.getcwd() or __file__ as appropriate in your case...
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
    path_service_account_creds = resolve_path("ocrTranslate/configs/service_account_creds.json")

    path_to_win_ocr = resolve_path("ocrTranslate/services/Get-Win10OcrTextFromImage.ps1")
