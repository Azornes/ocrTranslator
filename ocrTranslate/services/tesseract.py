import os
from ocrTranslate.utils import parse_html_link
import pytesseract


class Tesseract:
    def __init__(self, path_to_tesseract_exe="", ) -> None:
        if os.path.exists(path_to_tesseract_exe):
            self.path_to_tesseract_exe = parse_html_link(path_to_tesseract_exe)
            pytesseract.pytesseract.tesseract_cmd = self.path_to_tesseract_exe
            self.is_active = True
        else:
            self.is_active = False

    def run_ocr(self, path_image: str) -> str:
        if self.is_active:
            result = pytesseract.image_to_string(path_image)
            print(result)
            return result
        else:
            return "Path to tesseract.exe is invalid"
