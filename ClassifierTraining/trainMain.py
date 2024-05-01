from Database.DbContextManager.dbEmbeddingContextManager import DbEmbeddingContextManager
from ClassifierTraining.trainingPreparation import TrainingPreparation
from ClassifierTraining.trainClassifier import TrainClassifier
from Util.matchingUtilities import MatchingUtilities
import os

clean_zalando_path = os.path.join(os.path.abspath('../Datasets'), 'clean_Zalando.csv')
clean_tommyh_path = os.path.join(os.path.abspath('../Datasets'), 'clean_TommyHilfiger.csv')
clean_gerryw_path = os.path.join(os.path.abspath('../Datasets'), 'clean_GerryWeber.csv')


def train_classifier(m_utilities, db_embedding_manager=False):
    # TrainingPreparation(m_utilities, number_no_matches = 90000, matches_train_test_split = 0.5, no_matches_train_test_split=2.0/3.0)
    train_classifier_obj = TrainClassifier(db_embedding_manager)
    #train_classifier_obj.train_classifier()
    train_classifier_obj.test_classifier()


def main():
    db_embedding_manager = DbEmbeddingContextManager()
    m_utilities = MatchingUtilities([clean_zalando_path], [clean_tommyh_path, clean_gerryw_path])
    train_classifier(m_utilities, db_embedding_manager)


if __name__ == "__main__":
    main()
