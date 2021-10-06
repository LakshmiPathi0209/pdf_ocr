"""
    File 	        : CustomeExecption.py
    Package         :
    Description     :
    Project Name    : pdf_ocr
    Created by lakshmipathi on 08/05/21
"""

from dataclasses import dataclass


@dataclass
class ExceptionConstants:
    exception_string_map = {
        "noLang": "Language is not specified"
    }


class OCRException(Exception):
    def __init__(self, message):
        super(OCRException, self).__init__(message)


class NoLangException(OCRException):
    def __init__(self, message=None):
        super(NoLangException, self).__init__(message if message else ExceptionConstants.exception_string_map["noLang"])
