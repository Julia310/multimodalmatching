import cv2
import socket
import numpy as np
from urllib.request import Request, urlopen
import os
import io
from PIL import Image
from keras.applications.resnet import preprocess_input
from glob import glob
import logging
from dataAlias import ZALANDO_TABLE_ALIAS, TOMMYH_GERRYW_TABLE_ALIAS
from sys import platform

gerry_web_base_path = r'E:\ClusterImages\GerryWeber'
tommy_h_base_path = r"E:\ClusterImages\TommyHilfiger"
zalando_base_path = r"E:\ClusterImages\Zalando"
if 'linux' in platform:
    gerry_web_base_path = os.path.abspath(r'./Images/GerryWeber')
    tommy_h_base_path = os.path.abspath(r'./Images/TommyHilfiger')
    zalando_base_path = os.path.abspath(r'./Images/Zalando')


def get_and_preprocess_image(img_url_dict):
    """
        image_url_dict contains information for a single image.
        Example:
            {
                'articleId': 'T=121U089-K11',
                'path': 'image_name.jpg',
                'brand': jommy hilfiger',
                'url': 'https://...',
                'data_alias': 'zal'
            }
        Returns image_dict with the following information:
        image_dict = {'articleId': articleId/MPN, 'image': image_embedding}

    """
    image_dict = get_image(img_url_dict, True)
    if not image_dict:
        return image_dict
    return preprocess_image(image_dict)


def get_image(img_dict, file_system=False):
    """
        file_system is false by default.
        If false the image is read from disk otherwise the image is downloaded by given url
    """
    if file_system:
        return load_images_from_file_system(img_dict)
    return download_image(img_dict)


def load_images_from_file_system(img_dict):
    """
        Loads the image from filesystem if available and not corrupted, otherwise the image is downloaded.
    """
    brand = img_dict['brand']
    data_alias = img_dict['data_alias']
    base_path = get_base_path_by_brand_and_data_alias(brand, data_alias)

    file_path = os.path.join(base_path, img_dict["path"])
    file_result = glob(file_path + '*')
    if len(file_result) == 0:
        logging.info('File not found - trying to download file : :' + img_dict["path"])
        return download_image(img_dict)
    else:
        file = file_result[0]
        try:
            # rgb_image = Image.open(file).convert('RGB')
            # np_image = np.array(rgb_image)[:, :, ::-1].copy()
            np_image = cv2.imread(file)
            return {'articleId': img_dict['articleId'], 'image': np_image, 'file': file}

        except:
            logging.info('Local file corrupt - DELETE THIS: ' + file_path)
            logging.info('Ignoring file and trying to download')
            return download_image(img_dict)


def download_image(img_url_dict):
    img_url = img_url_dict['url']
    timeout = 20
    socket.setdefaulttimeout(timeout)

    req = Request(img_url,
                  headers={'User-Agent': 'Mozilla/5.0 Windows NT 6.1; WOW64; rv:12.0 Gecko/20100101 Firefox/12.0'})
    with urlopen(req) as response:
        img_bytes = response.read()
        arr = np.asarray(bytearray(img_bytes), dtype=np.uint8)
        save_image_to_file_local(img_bytes, img_url_dict)
        img = cv2.imdecode(arr, -1)
        return {'articleId': img_url_dict['articleId'], 'image': img}


def save_image_to_file_local(img_bytes, img_url_dict):
    """
        persist image on disk after download
    """
    image = Image.open(io.BytesIO(img_bytes))

    file_path = os.path.join(get_base_path_by_brand_and_data_alias(img_url_dict['brand'], img_url_dict['data_alias']),
                             img_url_dict['path'])
    if img_url_dict['brand'] == 'tommy hilfiger' and img_url_dict['data_alias'] == TOMMYH_GERRYW_TABLE_ALIAS:
        file_path = file_path + '.jpg'
    image.save(file_path)
    logging.info('==>image saved under ' + file_path)


def get_base_path_by_brand_and_data_alias(brand, data_alias):
    base_path = ""
    if brand == 'gerry weber' and data_alias == TOMMYH_GERRYW_TABLE_ALIAS:
        base_path = gerry_web_base_path
    if brand == 'tommy hilfiger' and data_alias == TOMMYH_GERRYW_TABLE_ALIAS:
        base_path = tommy_h_base_path
    if data_alias == ZALANDO_TABLE_ALIAS:
        base_path = zalando_base_path
    return base_path


def preprocess_image(image_dict):
    """
        Resizes the image and adds a dimension with subsequent image preprocessing for the keras Resnet model.
    """
    articleId = image_dict['articleId']
    img = image_dict['image']
    try:
        img = cv2.resize(img, (224, 224), interpolation=cv2.INTER_AREA)
    except Exception as e:
        print(str(e))
        print(image_dict['file'])

    img = img.reshape((1,) + img.shape)
    img = preprocess_input(img)

    return {'articleId': articleId, 'image': img}
