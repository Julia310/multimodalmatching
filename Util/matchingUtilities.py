import csv
import itertools
import pandas as pd
import logging
from statistics import median


def create_data_dict(data_path_list):
    """
        data_path_list: list of pathes to clean data csv
            in case of zalando, the list contains a single path,
            otherwise it includes two paths to Gerry Weber and Tommy Hilfiger clean data
        returns single dictionary containing either Zalando or Tommy Hilfiger / Gerry Weber data
            Example:
                {
                    {'N1241G08O-H12': ['Kapuzenpullover', 'arctic orange', '51.95', ...] }
                    {'N1242E11D-K13': ['kurze Sporthose', 'university red', '18.74', ...] }
                    {'NI121A0FA-E11': ['Jogginghose', 'iced lilac', '40.95', ...] }
                }
    """
    data_dict = dict()
    data_dict_list = []
    for path in data_path_list:
        data_dict_list.append(load_data_to_dict(path))
    if distinct_dict_keys_check(data_dict_list):
        for data_dict2 in data_dict_list:
            data_dict = {**data_dict, **data_dict2}
    else:
        raise Exception('Dictionaries contain same keys. Please make sure keys are distinct to merge dictionaries.')
    return data_dict


def load_data_to_dict(filename):
    """
        load data from csv to dictionary
    """
    file = open(filename, encoding='utf8')
    csv_reader = csv.reader(file)
    next(csv_reader)

    data_dict = {}

    for rec in csv_reader:
        data_dict[rec[0]] = rec[1:]

    return data_dict


def distinct_dict_keys_check(data_dict_list):
    """
        checks if two dictionary have the same keys (articleIds/MPNs) to merge them.
        Utilized Tommy Hilfiger and Gerry Weber
    """
    for i in range(len(data_dict_list)):
        for j in range(i + 1, len(data_dict_list)):
            for key in data_dict_list[i]:
                if key in data_dict_list[j]:
                    return False
    return True


def blocking(data_dict):
    """
        return blocking dictionary
        Example:
            blocking_dict = {'tommy hilfiger oberteile': [rec1_id, rec2_id, rec3_id, ...],
                               'tommy hilfiger hosen': [rec4_id, rec5_id, ...],
                                 ...
                            }
    """

    blocking_dict = {}
    ids = list(data_dict.keys())

    for id in ids:
        blocking_key = data_dict[id][3] + ' ' + data_dict[id][6]
        if not (blocking_key in blocking_dict):
            blocking_dict[blocking_key] = []
        blocking_dict[blocking_key].append(id)

    return blocking_dict


def blocks_statistics(data_dict, dataset_name):
    """
        Calculate and print some basic statistics about the generated blocks
    """

    blocks = len(data_dict)

    block_size_list = []
    for rec_id_list in data_dict.values():  # Loop over all blocks
        block_size_list.append(len(rec_id_list))

    logging.info(f'Dataset {dataset_name} number of blocks generated: %d' % blocks)
    logging.info('    Minimum block size: %d' % (min(block_size_list)))
    logging.info('    Average block size: %.2f' % \
                 (float(sum(block_size_list)) / len(block_size_list)))
    logging.info('    Median block size: %d' % (median(block_size_list)))
    logging.info('    Maximum block size: %d' % (max(block_size_list)))
    logging.info('')


def rename_df_columns(df, column_names):
    """
        Given the dataframe df with column names : 0, 1, 2...,
        renames the columns to e.g. : id, name, variant, price, ...
    """
    if len(df.columns) > len(column_names):
        df.drop(df.columns[len(df.columns) - (len(df.columns) - len(column_names)):], axis=1, inplace=True)

    column_names_dict = {}
    for i in range(len(df.columns)):
        column_names_dict[i] = column_names[i]

    df.rename(columns=column_names_dict, inplace=True)
    return df


class MatchingUtilities:
    """
        Main Utility class of the matching project.
        Utilized for preparing data for image and text embedding creations and for providing the complete classified_matches
        before as well as the filtered potential matching after blocking to the classification and the evaluation tasks.

    """

    def __init__(self, data_path_list1, data_path_list2):
        self.zal_dict = create_data_dict(data_path_list1)
        self.th_dict = create_data_dict([data_path_list2[1]])
        self.gw_dict = create_data_dict([data_path_list2[0]])
        self.th_gw_dict = create_data_dict(data_path_list2)
        self.zalando_articles = len(list(self.zal_dict.keys()))
        self.tommyh_gerryw_articles = len(list(self.th_gw_dict.keys()))
        self.tommyh_articles = len(list(self.th_dict.keys()))
        self.gerryw_articles = len(list(self.gw_dict.keys()))
        self.block_dict_zal = blocking(self.zal_dict)
        self.block_dict_th = blocking(self.th_dict)
        self.block_dict_gw = blocking(self.gw_dict)
        self.block_dict_th_gw = blocking(self.th_gw_dict)
        self.print_blocks_statistics()
        self.potential_matches = self.create_potential_matches()
        self.remove_not_relevant_data_from_dict()

    def print_blocks_statistics(self):
        logging.info('')
        logging.info('Statistics of the generated blocks:')
        logging.info('')
        blocks_statistics(self.block_dict_zal, 'Zalando')
        blocks_statistics(self.block_dict_th, 'Tommy Hilfiger')
        blocks_statistics(self.block_dict_gw, 'Gerry Weber')

    def get_number_of_matching_candidates_before_blocking(self):
        """
            returns number of initial matching candidates before blocking for the final matching pipeline evaluation
        """
        return self.zalando_articles * self.tommyh_gerryw_articles

    def get_number_of_th_matching_candidates_before_blocking(self):
        """
           returns number of initial Tommy Hilfiger matching candidates before blocking for the final matching pipeline evaluation
        """
        return self.zalando_articles * self.tommyh_articles

    def get_number_of_gw_matching_candidates_before_blocking(self):
        """
           returns number of initial Gerry Weber matching candidates before blocking for the final matching pipeline evaluation
        """
        return self.zalando_articles * self.gerryw_articles

    def create_potential_matches(self):
        """
            returns potential classified_matches as dictionaries with blocking keys as dictionary keys
            Example:
                 potential_matches = { 'tommy hilfiger oberteile': [[zal_id1, th_gw_id1], [zal_id2, th_gw_id2], ...
                        ...
                }
        """
        keys = list(self.block_dict_th_gw.keys())

        potential_matches = {}

        cnt = 0
        for key in keys:
            if key in self.block_dict_zal:
                potential_matches[key] = list(itertools.product(self.block_dict_zal[key], self.block_dict_th_gw[key]))
                cnt += len(potential_matches[key])
        logging.info(f'Number of potential matches:             {cnt}')
        logging.info('')

        return potential_matches

    def remove_not_relevant_data_from_dict(self):
        """
            remove data from Zalando dictionary and the Tommy Hilfiger/Gerry Weber dictionary,
            if not the same blocking key exists for this data in the potential classified_matches dictionary
        """
        potential_matches_keys = list(self.potential_matches.keys())

        for data_dict in [self.zal_dict, self.th_gw_dict]:
            for key in list(data_dict.keys()):
                blocking_key = data_dict[key][3] + ' ' + data_dict[key][6]
                if not blocking_key in potential_matches_keys:
                    del data_dict[key]

    def get_potential_matches_as_flat_list(self):
        """
            transforms potential_matches dictionary with blocking keys to flat list
            Example:
                 potential_matches = { { 'tommy hilfiger oberteile': [[zal_id1, th_gw_id1], [zal_id2, th_gw_id2], ... ] }
                                       { 'gerry weber hosen': [[zal_id_x, th_gw_id_x], [zal_id_x+1, th_gw_id_x+1], ... ] }
                                        ... }
                Result:
                flat_list = [[zal_id1, th_gw_id1], [zal_id2, th_gw_id2], ... , [zal_id_x, th_gw_id_x], [zal_id_x+1, th_gw_id_x+1], ... ]
        """
        flat_list = list()
        keys = list(self.potential_matches.keys())
        for key in keys:
            flat_list += self.potential_matches[key]
        return flat_list

    def get_matching_text_data_as_df(self, column_names):
        """
            creates main dataframes for text data preprocessing with the given column_names
            ( = ['name', 'variant', 'price']) and articleIds as indices for zalando data
            while MPNs are used as indices in case of Gerry Weber / Tommy Hilfiger data
            These dataframes is required mainly for the text embedding creation process
        """
        df_zal = pd.DataFrame.from_dict(self.zal_dict, orient='index')
        df_zal = rename_df_columns(df_zal, column_names)

        df_th_gw = pd.DataFrame.from_dict(self.th_gw_dict, orient='index')
        df_th_gw = rename_df_columns(df_th_gw, column_names)

        return df_zal, df_th_gw

    def get_matching_image_path_list(self, data_alias_zal, data_alias_th_gw):
        """
            creates a list of dictionaries for the image preprocessing / image embedding generation process
        """
        image_list_zal = list({'articleId': key,
                               'path': self.zal_dict[key][4],
                               'brand': self.zal_dict[key][3],
                               'url': self.zal_dict[key][5],
                               'data_alias': data_alias_zal}
                              for key in list(self.zal_dict.keys()))

        image_list_th_gw = list({'articleId': key,
                                 'path': self.th_gw_dict[key][4],
                                 'brand': self.th_gw_dict[key][3],
                                 'url': self.th_gw_dict[key][5],
                                 'data_alias': data_alias_th_gw}
                                for key in list(self.th_gw_dict.keys()))
        return image_list_zal, image_list_th_gw
