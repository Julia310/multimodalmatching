from multiprocessing import Pool
from multiprocessing.pool import ThreadPool
from Database.DbContextManager.dbMatchingEvaluationManager import DbMatchesContextManager
from Database.DbContextManager.dbEmbeddingContextManager import DbEmbeddingContextManager
from Util.similarityGenerator import SimilarityGenerator
from Classification.ThresholdClassification.thresholdPrediction import threshold_prediction
import logging


def classification(args):
    ids = args['article_ids']
    sim_gen = args['sim_gen']
    sim_dict = sim_gen.get_similarity_vector(ids)
    prediction = threshold_prediction(sim_dict)
    if prediction == 1:
        return {'zal_id': sim_dict['zal_id'],
                'th_gw_id': sim_dict['th_gw_id']}
    else:
        return None


def thread_classification(potential_matches):
    context = DbMatchesContextManager()
    embed_context = DbEmbeddingContextManager()
    sim_gen = SimilarityGenerator(embed_context)
    pool = ThreadPool(10)
    chunk_size = 100
    chunks = [potential_matches[x:x + chunk_size] for x in range(0, len(potential_matches), chunk_size)]
    cnt = 0

    for chunk in chunks:
        cnt += 1
        arg_list = []
        for article_ids in chunk:
            arg_list.append({'article_ids': article_ids, 'sim_gen': sim_gen})
        prediction_list = pool.map(classification, arg_list)
        prediction_list = list(filter(None, prediction_list))
        context.save_many_matches(prediction_list)
        print(str(chunk_size * cnt) + ' classified_matches saved.')


def split(a, n):
    k, m = divmod(len(a), n)
    return (a[i*k+min(i, m):(i+1)*k+min(i+1, m)] for i in range(n))


class ParallelClassification:
    def __init__(self, m_utilities):
        self.processes = 4
        logging.info(f'number of processes {self.processes}')
        self.potential_matches = m_utilities.get_potential_matches_as_flat_list()

    def conduct_classification(self):
        chunks = split(self.potential_matches, self.processes)
        with Pool(self.processes) as pool:
            pool.map(thread_classification, chunks)






