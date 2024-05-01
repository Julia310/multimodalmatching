import pickle
import os
from sys import platform
from tqdm import tqdm
import numpy as np

MODEL_PATH = os.path.abspath(r'./random_forest.sav')
if 'linux' in platform:
    MODEL_PATH = os.path.abspath('./multimodalmatching/random_forest.sav')


class MLClassification:
    def __init__(self, db_context, sim_generator, m_utilities):
        self.classifier = self.load_classifier()
        self.potential_matches = m_utilities.get_potential_matches_as_flat_list()
        self.db_context = db_context
        self.sim_generator = sim_generator
        self.batch_size = 500

    def load_classifier(self):
        with open(MODEL_PATH, 'rb') as file:
            pickle_model = pickle.load(file)
        return pickle_model

    def get_similarities(self, article_ids):
        sim_vec = []
        sim_dict = self.sim_generator.get_similarity_vector(article_ids)
        sim_vec.append(sim_dict['name'])
        sim_vec.append(sim_dict['variant'])
        sim_vec.append(sim_dict['price'])
        sim_vec.append(sim_dict['image'])
        return sim_vec

    def conduct_classification(self):
        sim_vec_list = []
        classification_list = []
        for i in tqdm(range(len(self.potential_matches)), desc='conduct ml classification'):
            sim_vec_list.append(self.get_similarities(self.potential_matches[i]))
            classification_list.append(
                {'zal_id': self.potential_matches[i][0], 'th_gw_id': self.potential_matches[i][1]})

            if (i + 1) % self.batch_size == 0:

                predictions = self.classifier.predict(sim_vec_list)
                match_idx_list = np.where(predictions == 1)[0]
                classified_matches = [classification_list[i] for i in match_idx_list]
                sim_vec_list = []
                classification_list = []
                if len(classified_matches) > 0:
                    self.db_context.save_many_matches(classified_matches)
