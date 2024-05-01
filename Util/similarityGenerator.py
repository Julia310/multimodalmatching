from math import *


def square_rooted(x):
    """
        Computes the length of the given vector x
    """
    return round(sqrt(sum([a * a for a in x])), 5)


def cosine_similarity(x, y):
    numerator = sum(a * b for a, b in zip(x, y))
    denominator = square_rooted(x) * square_rooted(y)
    return round(numerator / float(denominator), 3)


class SimilarityGenerator:
    """
        Class for similarity calculation to perform threshold_classification
    """
    def __init__(self, db_embeddings_context_manager):
        self.db_manager = db_embeddings_context_manager

    def get_similarity_vector(self, article_ids):
        """
            Given an articleId of Zalando and a MPN of Tommy Hilfiger / Gerry Weber data from the article_ids list,
            the embeddings for the corresponding attributes and the float value of the price are obtained from the
            database.
            Returns a dictionary with similarities for the appropriate attributes
            Example:
                 sim_vec = {
                    'zal_id': article_ids[0],
                    'th_gw_id':article_ids[1],
                    'name: 0.499,
                    'variant': 0.603,
                    'price': 0.85,
                    'image': 0.98
                }
        """

        sim_vec = {'zal_id': article_ids[0],
                   'th_gw_id':article_ids[1]}
        zalando_embeddings = self.db_manager.select_zalando_by_article_id(article_ids[0])
        th_gw_embeddings = self.db_manager.select_th_gw_by_article_id(article_ids[1])

        # name similarity
        zal_name = zalando_embeddings['name']
        th_gw_name = th_gw_embeddings['name']
        sim_vec['name'] = cosine_similarity(zal_name, th_gw_name)

        # variant similarity
        zal_variant = zalando_embeddings['variant']
        th_gw_variant = th_gw_embeddings['variant']
        sim_vec['variant'] = cosine_similarity(zal_variant, th_gw_variant)

        # price similarity
        zal_price = zalando_embeddings['price']
        th_gw_price = th_gw_embeddings['price']
        price_similarity = min(float(zal_price), float(th_gw_price)) / max(float(zal_price), float(th_gw_price))
        sim_vec['price'] = round(price_similarity, 3)

        # image similarity
        zal_image = zalando_embeddings['image']
        th_gw_image = th_gw_embeddings['image']
        sim_vec['image'] = cosine_similarity(zal_image, th_gw_image)
        return sim_vec
