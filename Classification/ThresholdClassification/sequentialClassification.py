from Classification.ThresholdClassification.thresholdPrediction import threshold_prediction
from tqdm import tqdm


class SequentialClassification:
    def __init__(self, db_context, sim_generator, m_utilities):
        self.db_context = db_context
        self.sim_generator = sim_generator
        self.potential_matches = m_utilities.get_potential_matches_as_flat_list()

    def conduct_classification(self):
        for i in tqdm(range(len(self.potential_matches)), desc='conduct threshold classification'):
            sim_dict = self.sim_generator.get_similarity_vector(self.potential_matches[i])
            if threshold_prediction(sim_dict) == 1:
                self.db_context.save_match((sim_dict['zal_id'], sim_dict['th_gw_id']))
