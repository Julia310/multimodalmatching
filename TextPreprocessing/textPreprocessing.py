import pandas as pd
from TextPreprocessing.textCleaning import clean_columns
import os
from TextPreprocessing.addCategories import add_categories
from sys import platform


clean_zalando_path = os.path.abspath('./Datasets/clean_Zalando.csv')
zalando_path = os.path.abspath('./Datasets/Zalando.csv')
clean_tommyh_path = os.path.abspath('./Datasets/clean_TommyHilfiger.csv')
tommyh_path = os.path.abspath('./Datasets/TommyHilfiger.csv')
clean_gerryw_path = os.path.abspath('./Datasets/clean_GerryWeber.csv')
gerryw_path = os.path.abspath('./Datasets/GerryWeber.csv')
if 'linux' in platform:
    clean_zalando_path = os.path.abspath('./multimodalmatching/Datasets/clean_Zalando.csv')
    zalando_path = os.path.abspath('./multimodalmatching/Datasets/Zalando.csv')
    clean_tommyh_path = os.path.abspath('./multimodalmatching/Datasets/clean_TommyHilfiger.csv')
    tommyh_path = os.path.abspath('./multimodalmatching/Datasets/TommyHilfiger.csv')
    clean_gerryw_path = os.path.abspath('./multimodalmatching/Datasets/clean_GerryWeber.csv')
    gerryw_path = os.path.abspath('./multimodalmatching/Datasets/GerryWeber.csv')


def adjust_brand(input_string):
    if 'gerry weber' in input_string:
        return 'gerry weber'
    if 'tommy' in input_string:
        return 'tommy hilfiger'
    return input_string


def get_first_image_url(urls, dataset):
    """
        Select only url of the first image belonging to a product,
        in case the image is not available or corrupted to download later.
    """
    if dataset == 'th':
        url = urls.split(',')[0]
    elif dataset == 'z':
        url = 'https' + urls.split('https')[1]
    else:
        url = urls.split(',')[0]
    return url


def url_to_file_name(url, dataset):
    """
        Preprocess url in case image is not available or corrupted to download later
    """
    if dataset in ['th', 'z']:
        file_name = url.split('/')[-1]
        file_name_clean = file_name.split('?')[0]
    else:
        file_name_clean = url.split('/')[-1]

    return file_name_clean


def zalando_preprocessing():
    if not os.path.exists(clean_zalando_path):
        #df = pd.read_csv(zalando_path, on_bad_lines='skip', verbose=False)
        df = pd.read_csv(zalando_path, error_bad_lines=False, verbose=False)
        df = df[["ArticleId", "ProductName", "Color", "Price", 'ImageUrl', "Brand"]]
        df.rename(columns={'ArticleId': 'id', 'ProductName': 'name', 'Color': 'variant', 'Price': 'price',
                           'ImageUrl': 'image', 'Brand': 'brand'}, inplace=True)

        df["name"] = df["name"].apply(lambda x: x.split(';')[0].split(' - ')[-2])

        df = clean_columns(df, ['name', 'variant'])

        df["brand"] = df["brand"].apply(lambda x: x.lower())
        df["brand"] = df["brand"].apply(lambda x: adjust_brand(x))

        df["variant"] = df["variant"].apply(lambda x: x.lower())
        df["image_url"] = df["image"].apply(lambda x: get_first_image_url(x, 'z'))
        df["image_name"] = df["image_url"].apply(lambda x: url_to_file_name(x, 'z'))
        df = df[["id", "name", "variant", "price", "brand", "image_name", "image_url"]]

        add_categories(df)
        df.to_csv(clean_zalando_path, index=False)


def tommyh_preprocessing():
    if not os.path.exists(clean_tommyh_path):
        df = pd.read_csv(tommyh_path)
        df = df[['MPN', 'name', 'variant', 'price', 'images']]
        df.rename(columns={'MPN': 'id', 'images': 'image'}, inplace=True)

        df = clean_columns(df, ['name', 'variant'])
        df = df.assign(brand="tommy hilfiger")

        df["variant"] = df["variant"].apply(lambda x: x.lower())
        df["image_url"] = df["image"].apply(lambda x: get_first_image_url(x, 'th'))
        df["image_name"] = df["image_url"].apply(lambda x: url_to_file_name(x, 'th'))
        df = df[["id", "name", "variant", "price", "brand", "image_name", "image_url"]]

        add_categories(df)
        df.to_csv(clean_tommyh_path, index=False)


def gerryw_preprocessing():
    if not os.path.exists(clean_gerryw_path):
        df = pd.read_csv(gerryw_path)
        df = df[['MPN', 'name', 'variant', 'price', 'images']]
        df.rename(columns={'MPN': 'id', 'images': 'image'}, inplace=True)

        df = clean_columns(df, ['name', 'variant'])
        df = df.assign(brand="gerry weber")

        df["variant"] = df["variant"].apply(lambda x: x.lower())
        df["image_url"] = df["image"].apply(lambda x: get_first_image_url(x, 'gw'))
        df["image_name"] = df["image_url"].apply(lambda x: url_to_file_name(x, 'gw'))
        df = df[["id", "name", "variant", "price", "brand", "image_name", "image_url"]]

        add_categories(df)
        df.to_csv(clean_gerryw_path, index=False)


def preprocess_text_data():
    """
        Creates the following csv files with preprocessed data for matching:
            ../Datasets/clean_GerryWeber.csv,
            ../Datasets/clean_TommyHilfiger.csv,
            ../Datasets/clean_Zalando.csv,
        Subsequently these three paths are returned
    """
    tommyh_preprocessing()
    gerryw_preprocessing()
    zalando_preprocessing()

    clean_datasets = [
        clean_gerryw_path,
        clean_tommyh_path,
        clean_zalando_path
    ]

    return clean_datasets
