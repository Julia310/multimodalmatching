import keras.models
from keras.applications.resnet import ResNet50
from ImagePreprocessing.imageBatchIterator import ImageBatchIterator
from multiprocessing.pool import ThreadPool
from ImagePreprocessing.imagePreprocessing import get_and_preprocess_image
import os
import numpy as np
from tqdm import tqdm
import pickle
from dataAlias import ZALANDO_TABLE_ALIAS, TOMMYH_GERRYW_TABLE_ALIAS
from sys import platform

MODEL_PATH = os.path.join(os.path.abspath(r'EmbeddingCreation'), 'Model', 'resnet50.h5')
if 'linux' in platform:
    MODEL_PATH = os.path.join(os.path.abspath('./multimodalmatching/EmbeddingCreation'), 'Model', 'resnet50.h5')


class ImageEmbeddingGenerator:
    """
        Generates images embeddings with the keras ResNet50 models
    """

    def __init__(self):
        self.image_size = [224, 224, 3]
        self.model = self.instantiate_model()

    def instantiate_model(self):
        if not os.path.exists(MODEL_PATH):
            model = ResNet50(input_shape=self.image_size, weights='imagenet', include_top=False)
            model.save(MODEL_PATH, save_format='h5')
        else:
            model = keras.models.load_model(MODEL_PATH, compile=False)
        return model

    def get_image_embedding(self, img_dict):
        image = img_dict['image']
        embedding = self.model.predict(image, verbose=0)[0]
        embedding = np.mean(embedding, axis=0)
        vector = np.mean(embedding, axis=0)
        img_byte_dict = {'articleId': img_dict['articleId'], 'image': pickle.dumps(vector)}
        return img_byte_dict


class ManageImageEmbeddings:
    """
        Serves as the interface between image prepocessing, embedding generation and image persisting.
        Obtains the image embedding from the ImageEmbeddingGenerator class.
    """
    def __init__(self, image_list_zal, image_list_th_gw, data_alias_zal, data_alias_th_gw, db_embedding_manager):
        self.image_batch_iterator_zal = ImageBatchIterator(image_list_zal)
        self.image_batch_iterator_th_gw = ImageBatchIterator(image_list_th_gw)
        self.data_alias_zal = data_alias_zal
        self.data_alias_th_gw = data_alias_th_gw
        self.processes = 4
        self.pool = ThreadPool(self.processes)
        self.image_embedding_generator = ImageEmbeddingGenerator()
        self.db_manager = db_embedding_manager

    def process_image_batches(self, image_batch_iterator, data_alias, multi=False):
        batch = image_batch_iterator.next_batch()
        while batch is not None:
            embeddings = []

            # If multi is true the image preprocessing step is performed by multiple threads.
            if multi:
                img_batch = self.pool.map(get_and_preprocess_image, batch)
            else:
                img_batch = self.preprocess_image_batch(batch)

            for img_data in tqdm(img_batch, desc='Create embeddings from batch'):
                embeddings.append(self.image_embedding_generator.get_image_embedding(img_data))

            self.save_image_embeddings(embeddings, data_alias)
            batch = image_batch_iterator.next_batch()

    def preprocess_image_batch(self, batch):
        image_list = []
        for i in tqdm(range(len(batch)), f'Preprocess image batch      '):
            image = batch[i]
            if get_and_preprocess_image(image):
                image_list.append(get_and_preprocess_image(image))
        return image_list

    def generate_embeddings(self):
        self.process_image_batches(self.image_batch_iterator_zal, self.data_alias_zal)
        self.process_image_batches(self.image_batch_iterator_th_gw, self.data_alias_th_gw)

    def save_image_embeddings(self, embeddings, data_alias):
        if data_alias == ZALANDO_TABLE_ALIAS:
            self.db_manager.update_zalando_image_by_article_id(embeddings)
        else:
            self.db_manager.update_th_gw_image_by_article_id(embeddings)
