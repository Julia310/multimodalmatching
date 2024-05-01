from Database.dbContext import mysql_db
from Database.Models.embeddingModels import ZalandoEmbeddings, TommyHGerryWEmbeddings
from tqdm import tqdm
import pickle
import logging


class DbEmbeddingContextManager:
    """
        Persists text and image embedding bytes and allows to access these by providing the corresponding articleId/MPN.
        Text Embeddings are initially inserted while image embeddings are added by updating the table rows.
    """

    def __init__(self):
        self.connection = mysql_db
        self.zalando_embeddings = ZalandoEmbeddings
        self.th_gw_embeddings = TommyHGerryWEmbeddings
        self.batch_size = 1000

    def save_zalando_embeddings(self, values):
        with self.connection.atomic():
            for idx in range(0, len(values), self.batch_size):
                idx_max = len(values)
                if idx + self.batch_size < idx_max:
                    idx_max = idx + self.batch_size
                val_to_table = values[idx:idx_max]
                query = self.zalando_embeddings.insert_many(val_to_table)
                query.execute()
                logging.info(str(idx_max) + ' rows inserted')

    def save_th_gw_embeddings(self, values):
        with self.connection.atomic():
            for idx in range(0, len(values), self.batch_size):
                idx_max = len(values)
                if idx + self.batch_size < idx_max:
                    idx_max = idx + self.batch_size
                val_to_table = values[idx:idx_max]
                query = self.th_gw_embeddings.insert_many(val_to_table)
                query.execute()
                logging.info(str(idx_max) + ' rows inserted')

    def update_zalando_image_by_article_id(self, batch):
        for data_dict in tqdm(batch, desc='Persist image embeddings    '):
            query = self.zalando_embeddings.update(
                image=data_dict['image'],
            ). \
                where(self.zalando_embeddings.articleId == data_dict['articleId'])
            query.execute()

    def update_th_gw_image_by_article_id(self, batch):
        for data_dict in tqdm(batch, desc='Persist image embeddings    '):
            query = self.th_gw_embeddings.update(
                image=data_dict['image'],
            ). \
                where(self.th_gw_embeddings.articleId == data_dict['articleId'])
            query.execute()

    def select_zalando_by_article_id(self, articleId):
        product = self.zalando_embeddings.select(). \
            where(articleId == self.zalando_embeddings.articleId).get()
        embeddings = {
            'name': pickle.loads(product.name),
            'variant': pickle.loads(product.variant),
            'price': product.price,
            'image': pickle.loads(product.image)
        }
        return embeddings

    def select_th_gw_by_article_id(self, articleId):
        product = self.th_gw_embeddings.select(). \
            where(articleId == self.th_gw_embeddings.articleId).get()
        embeddings = {
            'name': pickle.loads(product.name),
            'variant': pickle.loads(product.variant),
            'price': product.price,
            'image': pickle.loads(product.image)
        }
        return embeddings

    def recreate_tables(self):
        if ZalandoEmbeddings.table_exists():
            ZalandoEmbeddings.drop_table()
        if TommyHGerryWEmbeddings.table_exists():
            TommyHGerryWEmbeddings.drop_table()
        self.connection.create_tables([ZalandoEmbeddings, TommyHGerryWEmbeddings])
