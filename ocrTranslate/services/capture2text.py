import os
import subprocess

from ocrTranslate.assets import Assets as assets
from ocrTranslate.utils import parse_html_link


class Capture2Text:
    def __init__(self, path_to_Capture2Text_CLI_exe="", ) -> None:
        if os.path.exists(path_to_Capture2Text_CLI_exe):
            self.path_to_Capture2Text_CLI_exe = parse_html_link(path_to_Capture2Text_CLI_exe)
            self.is_active = True
        else:
            self.is_active = False

    def ocr_by_capture2text(self) -> str:
        result = subprocess.check_output(self.path_to_Capture2Text_CLI_exe + ' --image {path_to_tmp} '.format(path_to_tmp=assets.path_to_tmp) + '--output-format ${capture}')
        return result

