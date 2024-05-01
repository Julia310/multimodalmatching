import os
import sys
import csv
import logging

CLEAN_GW = os.path.join(os.path.abspath('./Datasets'), 'clean_GerryWeber.csv')
CLEAN_TH = os.path.join(os.path.abspath('./Datasets'), 'clean_TommyHilfiger.csv')
if 'linux' in sys.platform:
    CLEAN_GW = os.path.join(os.path.abspath('./multimodalmatching/Datasets'), 'clean_GerryWeber.csv')
    CLEAN_TH = os.path.join(os.path.abspath('./MultiModalMatching/Datasets'), 'clean_TommyHilfiger.csv')


class MappingTablesUtils:

    def __init__(self, db_context):
        self.db_context = db_context
        self.gw_reader = csv.reader(open(CLEAN_GW))
        self.th_reader = csv.reader(open(CLEAN_TH))

    def zip_ref_id_list_to_dict(self, ids):
        id_list = list()
        for id in ids:
            id_list.append({"ref_id": id})
        return id_list

    def mapping_ids_to_database(self):
        th_ids = list(list(zip(*list(self.th_reader)[1:]))[0])
        th_id_dict = self.zip_ref_id_list_to_dict(th_ids)
        self.db_context.save_th_gw_ids("th", th_id_dict)
        logging.info('Tommy Hilfiger Ids saved to db for later evaluation')

        gw_ids = list(zip(*list(self.gw_reader)[1:]))[0]
        gw_id_dict = self.zip_ref_id_list_to_dict(gw_ids)
        self.db_context.save_th_gw_ids("gw", gw_id_dict)
        logging.info('Gerry Weber Ids saved to db for later evaluation')
