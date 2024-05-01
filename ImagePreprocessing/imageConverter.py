import logging
import os
from PIL import Image
from tqdm import tqdm
import shutil


class ImageConverter:
    """
        Applied before executing pipeline
        Converts all the webp images to jpg
    """

    SRC_FOLDER_NAME_ABS = r'C:\Users\JPete\TommyHilfiger'
    TARGET_FOLDER_NAME_ABS = r'D:\pythonProject\MultiModalMatching\TommyHilfiger'

    TYPE_JPEG = '.jpeg'
    TYPE_JPG = '.jpg'
    TYPE_WEBM = '.webm'

    def __init__(self):
        self.conversion_path = r'D:\pythonProject\MultiModalMatching\TommyHilfiger'
        self.source_path = r'C:\Users\JPete\TommyHilfiger'
        self.tmp = ''

    def load_images_to_dict(self):
        list_of_files = []
        for root, dirs, files in tqdm(os.walk(self.source_path)):
            for file in files:
                list_of_files.append(self.source_path + '\\' + file)
        return list_of_files

    def convert_images(self, image_dict):
        for i in tqdm(range(len(image_dict))):
            image = image_dict[i]
            if not ('.jpg' in image or '.png' in image or '.jpeg' in image):
                try:
                    im = Image.open(image).convert("RGB")
                    file_path = image.replace(self.SRC_FOLDER_NAME_ABS, self.TARGET_FOLDER_NAME_ABS)
                except:
                    logging.info(f'skipped file {image}')
                    continue
                im.save(file_path + '.jpg')
            else:
                file_path = image.replace(self.SRC_FOLDER_NAME_ABS, self.TARGET_FOLDER_NAME_ABS)
                shutil.copy2(image, file_path)
        return ''


obj = ImageConverter()
list_of_files = obj.load_images_to_dict()
obj.convert_images(list_of_files)