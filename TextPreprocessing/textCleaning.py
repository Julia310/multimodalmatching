import re
from num2words import num2words
import logging


def replace_specific_letters(text):
    text = text.replace('ä', 'ae')
    text = text.replace('ö', 'oe')
    text = text.replace('ü', 'ue')
    text = text.replace('ß', 'ss')
    return text


def replace_numerical_substrings(text):
    text = text.replace('1er', 'einer')
    text = text.replace('2er', 'zweier')
    text = text.replace('3er', 'dreier')
    text = text.replace('4er', 'vierer')
    text = text.replace('5er', 'fünfer')
    text = text.replace('6er', 'sechser')
    text = text.replace('1/2', 'einhalb')
    text = text.replace('3/4', 'dreiviertel')
    text = text.replace('7/8', 'siebenachtel')
    text = text.replace('4me', ' for me')
    text = text.replace('4all', ' for all')
    return text


def replace_year(text):
    year = re.findall('[1-2][0-9][0-9][0-9]', text)
    if len(year) > 0:
        year = year[0]
        year_str = num2words(int(year), to='year', lang='de')
        text = text.replace(str(year), year_str)
    return text

def replace_float(text):
    float_list = year = re.findall('[1-9][0-9][,][1-9]', text)
    for i in range(len(float_list)):
        num = str(float_list[i])
        num = num.replace(',', '.')
        num_str = num2words(float(num), lang='de')
        num = num.replace('.', ',')
        text = text.replace(num, num_str)
        #logging.info(text)
    return text


def replace_int(text):
    numbers_list = re.findall(r'\d{1,3}', text)
    for i in range(len(numbers_list)):
        num = str(numbers_list[i])
        num_str = num2words(int(num), lang='de')
        text = text.replace(num, num_str)
    return text


def remove_special_chars(text):
    for i in text:
        if not (i.isalnum() or i == ' ' or i == '-'):
            logging.info(text)
            break

    #_RE_COMBINE_WHITESPACE = re.compile(r"\s+")
    #new_text = _RE_COMBINE_WHITESPACE.sub(" ", new_text).strip()

    return text


def has_numbers(inputString):
    if any(char.isdigit() for char in inputString):
        logging.info(inputString)
        return True
    return False


def clean_price(price):
    price = num2words(float(price), lang='de', to='currency')
    return price


def replace_special_chars(text):
    text = text.replace(' / ', ' ')
    text = text.replace('¸', '')
    return text


def clean_variant(variant):
    variant = variant.lower()
    variant = variant.replace(' /', '/')
    variant = variant.replace('/ ', '/')
    variant = variant.replace('/', ', ')
    return variant


def clean_name(name):
    name = replace_numerical_substrings(name)
    #name = replace_year(name)
    #name = replace_float(name)
    #name = replace_int(name)
    name = replace_special_chars(name)
    #hasnumbers(name)
    #name = remove_special_chars(name)
    return name


def clean_text(text, column):
    if column == 'price':
        text = clean_price(text)
    elif column == 'variant':
        text = clean_variant(text)
    elif column == 'name':
        text = clean_name(text)

    return text


def clean_columns(df, columns):
    """
        Cleans given columns in dataframe.
    """
    for col in columns:
        df[col] = df[col].map(
            lambda x: clean_text(x, col)
        )
    return df
