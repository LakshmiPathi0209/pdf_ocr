import traceback
from dataclasses import dataclass

import cv2

from CustomeExecption import NoLangException, OCRException
from _ocr import _OCR
import os


@dataclass(frozen=True)
class ConstantDataClasses:
    output_type_string = "text"
    output_type_txt = "txt"


class OCRManager(_OCR):

    def extract_text(self
                     , file_path
                     , lang='eng'
                     , output_type=ConstantDataClasses.output_type_string
                     , output_file_path=None
                     , translate=False
                     , translate_lang=None):
        """

        :param file_path: Input file path (either pdf or image)
        :param lang: language to read, Default language will be set to english
        :param output_type: Output format expected (text , pdf , txt)
        :param output_file_path: Specify the output file path
        :param translate: Should the text to be translated to another language
        :param translate_lang: Language to translate
        :return: String if output_type is default or text
        """
        if not file_path:
            raise OCRException("Please, specify the file path")
        if not lang:
            raise NoLangException

        if output_type == ConstantDataClasses.output_type_txt and not output_file_path:
            raise OCRException("Please, specify the output file path")

        if translate and not translate_lang:
            raise OCRException("Please, specify the translate language")

        args = [file_path, lang, output_type, output_file_path, translate, translate_lang]

        return {
            ConstantDataClasses.output_type_txt: lambda: self.get_ocr_text(*args),
            ConstantDataClasses.output_type_string: lambda: self.get_ocr_text(*args)
        }[output_type]()

    def get_ocr_text(self, file_path, lang, output_type, output_file_path, translate, translate_lang):
        from pdf2image import pdfinfo_from_path, convert_from_path
        page_text_content = ""
        try:
            file_type = file_path.split(".")[-1]
            if file_type == "pdf":
                pdf_info = pdfinfo_from_path(file_path, userpw=None, poppler_path=None)
                pages = pdf_info["Pages"]
                for page_index in range(1, pages+1):
                    page_image = convert_from_path(file_path, first_page=page_index, last_page=page_index + 1)
                    page_content = self.process_image(page_image)
                    page_text_content = f'{page_text_content}{page_content}'

            else:
                image = cv2.imread(file_path)
                page_text_content = self.process_image(image)
            if not translate:
                return page_text_content
            else:
                return ""
        except Exception as msg:
            print(msg)
            traceback.print_stack()

    def ocr_txt_doc(self, file_path, lang, output_type, output_file_path, translate, translate_lang):
        pass


if __name__ == "__main__":
    ocr_obj = OCRManager()
    ocr_obj.extract_text(file_path="trnaslate.pdf", lang="kan")
