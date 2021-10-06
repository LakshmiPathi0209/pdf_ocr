"""
    File 	        : _ocr.py
    Package         :
    Description     :
    Project Name    : pdf_ocr
    Created by lakshmipathi on 15/05/21
"""
import glob
import traceback
from dataclasses import dataclass
import os
import cv2
import numpy as np


@dataclass(frozen=True)
class ConstantDataClasses:
    tmp_image_path = "/tmp/ocr/"
    file_name = "image_to_process.jpg"
    row_crop = "ROWCROP"
    column_crop = "COLUMNCROP"
    final = "FINAL"


class _OCR(object):

    def __init__(self):
        if not os.path.exists(ConstantDataClasses.tmp_image_path):
            os.mkdir(ConstantDataClasses.tmp_image_path)

    def process_image(self, image_obj):
        file_path = f'{ConstantDataClasses.tmp_image_path}{ConstantDataClasses.file_name}'
        try:
            image_obj[0].save(file_path, 'JPEG')
            actual_image, opening = self._preprocessing(file_path)
            text = self._convert_image_to_string(actual_image)
            print(text)
            return text
        except Exception:
            traceback.print_stack()
            traceback.print_exc()

    def _preprocessing(self, file_name):
        '''Before conveting the image to the pytesseract the image is fed to this preprocessing'''
        # from utils import getIndexPositions,convt_to_list

        image = cv2.imread(file_name)
        gray = self._get_grayscale(image)
        noise_removed = self._remove_noise(gray)
        opening = self._opening1(noise_removed)
        opening = cv2.adaptiveThreshold(opening, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 81, 11)
        actual_image = image.copy()

        opening = opening / 255

        return actual_image, opening

    @staticmethod
    def _get_grayscale(image):
        return cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    @staticmethod
    def _remove_noise(image):
        return cv2.medianBlur(image, 5)

    @staticmethod
    def _opening1(image):
        kernel = np.ones((5, 5), np.uint8)
        return cv2.morphologyEx(image, cv2.MORPH_OPEN, kernel)

    @staticmethod
    def _convert_image_to_string(image):

        import pytesseract
        custom_config = r'--oem 3 --psm 6'
        text = pytesseract.image_to_string(image, lang='kan', config=custom_config)

        return text
