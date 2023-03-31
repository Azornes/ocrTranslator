from rapidocr_openvino import RapidOCR


class RapidOcr:
    def __init__(self) -> None:
        self.rapid_ocr = RapidOCR()

    def ocr_by_rapid(self, path: str) -> str:
        result, elapse = self.rapid_ocr(path)
        text_result = ""

        for res in result:
            print(res[1])
            text_result += res[1] + "\n"
        return text_result


# rapid_ocr = RapidOcr()
# rapid_ocr.ocr_by_rapid("C:\\Programowanie\\Projekty\\Python\\HelpApps\\ocrTranslator3\\ocrTranslate\\temp\\temp.png")