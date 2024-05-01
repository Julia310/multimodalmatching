import os
import sys
import logging

conf_path = os.getcwd()
sys.path.append(conf_path)

from TextPreprocessing.textPreprocessing import preprocess_text_data
from EmbeddingCreation.createTextEmbedding import ManageTextEmbeddings
from EmbeddingCreation.createImageEmbedding import ManageImageEmbeddings
from Util.matchingUtilities import MatchingUtilities
from Util.trueMatches import TrueMatches
from Util.mappingTableUtils import MappingTablesUtils
from Util.similarityGenerator import SimilarityGenerator
from time import time
from Classification.ThresholdClassification.parallelClassification import ParallelClassification
from Classification.ThresholdClassification.sequentialClassification import SequentialClassification
from Classification.MLClassification.mlClassification import MLClassification
from Database.DbContextManager.dbEmbeddingContextManager import DbEmbeddingContextManager
from Database.DbContextManager.dbMatchingEvaluationManager import DbMatchesContextManager
from Database.DbContextManager.dbUtilityContextManager import DbUtilityContextManager
from dataAlias import ZALANDO_TABLE_ALIAS, TOMMYH_GERRYW_TABLE_ALIAS
from Evaluation.classificationEvaluation import classification_evaluation, th_gw_classification_evaluation
from Evaluation.blockingEvaluation import blocking_evaluation

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
os.environ["TOKENIZERS_PARALLELISM"] = 'true'


def config_logger():
    logging.basicConfig(format='%(asctime)s: %(message)s', level=logging.INFO)


def preprocess_data():
    logging.info('Start preparing data for embedding creation')
    start = time()
    logging.info('Start processing')
    datasets = preprocess_text_data()
    logging.info('Init Matching Util')
    m_utilities = MatchingUtilities([datasets[-1]], datasets[:-1])
    logging.info('Data prepared for embedding creation in ' + str("{:8.2f}".format((time() - start) / 60.0)) + ' seconds')
    return m_utilities


def recreate_database_tables(db_embedding_manager, db_matches_manager, db_utility_manager):
    db_embedding_manager.recreate_tables()
    db_matches_manager.recreate_tables()
    db_utility_manager.recreate_tables()


def create_text_embeddings(m_utilities, db_embedding_manager):
    # ##### Text Embedding ######
    start = time()
    logging.info('Start creating text embeddings')
    text_data_df1, text_data_df2 = m_utilities.get_matching_text_data_as_df(column_names=['name', 'variant', 'price'])
    text_to_embeddings_obj = ManageTextEmbeddings(
        'sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2',
        text_data_df1,
        text_data_df2,
        ZALANDO_TABLE_ALIAS,
        TOMMYH_GERRYW_TABLE_ALIAS,
        db_embedding_manager)
    text_to_embeddings_obj.manage_embeddings()
    logging.info('Text embeddings created and saved in ' + str("{:8.2f}".format((time() - start) / 60.0)) + ' minutes')


def create_image_embeddings(m_utilities, db_embedding_manager):
    # ###### Image Embedding ######
    logging.info('Start creating and saving image embeddings')
    start = time()
    image_list1, image_list2 = m_utilities.get_matching_image_path_list(ZALANDO_TABLE_ALIAS, TOMMYH_GERRYW_TABLE_ALIAS)
    images_to_embeddings = ManageImageEmbeddings(
        image_list1,
        image_list2,
        ZALANDO_TABLE_ALIAS,
        TOMMYH_GERRYW_TABLE_ALIAS,
        db_embedding_manager
    )
    images_to_embeddings.generate_embeddings()
    logging.info('Image embeddings created and saved in ' + str("{:8.2f}".format((time() - start) / 60)) + ' minutes')


def threshold_classification(m_utilities, db_matches_manager=None, db_embedding_manager=None, multi = True):
    start = time()
    if multi:
        parallel_classification = ParallelClassification(m_utilities)
        parallel_classification.conduct_classification()
    else:
        sim_generator = SimilarityGenerator(db_embedding_manager)
        sequential_classification = SequentialClassification(db_matches_manager, sim_generator, m_utilities)
        sequential_classification.conduct_classification()
    logging.info('Classification performed in ' + str("{:8.2f}".format((time() - start) / 60)) + ' minutes')


def ml_classification(m_utilities, db_matches_manager=None, db_embedding_manager=None):
    start = time()
    sim_generator = SimilarityGenerator(db_embedding_manager)
    classification = MLClassification(db_matches_manager, sim_generator, m_utilities)
    classification.conduct_classification()
    logging.info('Classification performed in ' + str("{:8.2f}".format((time() - start) / 60)) + ' minutes')


def evaluation_data_to_database(db_matches_manager):
    ##### TRUE MATCHES TO DB #####
    true_matches = TrueMatches(db_matches_manager)
    true_matches.save_matches_to_db()

    ##### SAVE MAPPING IDS #####
    mapping_table_utils = MappingTablesUtils(db_matches_manager)
    mapping_table_utils.mapping_ids_to_database()


def evaluation(m_utilities, db_matches_manager):
    logging.info('')
    blocking_evaluation(m_utilities)

    th_gw_classification_evaluation("th", db_matches_manager, m_utilities)
    logging.info('')
    th_gw_classification_evaluation("gw", db_matches_manager, m_utilities)
    logging.info('')
    classification_evaluation(db_matches_manager, m_utilities)


def main():
    matching_start = time()

    # ##### MAIN UTILITIES #####
    config_logger()
    m_utilities = preprocess_data()
    # ##### MAIN UTILITIES #####

    # ##### DATABASE CONNECTION #####
    db_embedding_manager = DbEmbeddingContextManager()
    db_matches_manager = DbMatchesContextManager()
    db_utility_manager = DbUtilityContextManager()
    # ##### DATABASE CONNECTION #####

    # ##### RECREATE TABLES #####
    recreate_database_tables(db_embedding_manager, db_matches_manager, db_utility_manager)
    # ##### RECREATE TABLES #####

    # ##### CREATING EMBEDDINGS #####
    create_text_embeddings(m_utilities, db_embedding_manager)
    create_image_embeddings(m_utilities, db_embedding_manager)
    # ##### CREATING EMBEDDINGS #####

    # ##### SAVE DATA FOR EVALUATION #####
    evaluation_data_to_database(db_matches_manager)
    # ##### SAVE DATA FOR EVALUATION #####

    # ##### CONDUCTING CLASSIFICATION #####
    ml_classification(m_utilities, db_matches_manager, db_embedding_manager)
    #threshold_classification(m_utilities, db_matches_manager, db_embedding_manager, multi=False)
    #threshold_classification(m_utilities)
    # ##### CONDUCTING CLASSIFICATION #####'''

    # ##### EVALUATION #####
    evaluation(m_utilities, db_matches_manager)
    # ##### EVALUATION #####

    logging.info('Products matched in ' + str("{:8.2f}".format((time() - matching_start) / (60 * 60))) + ' hours')


if __name__ == "__main__":
    main()
