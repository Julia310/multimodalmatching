from sklearn.ensemble import RandomForestClassifier
import logging
from Util.similarityGenerator import SimilarityGenerator
import os
import csv
from tqdm import tqdm
from sklearn.metrics import confusion_matrix
import numpy as np
import pickle


class TrainClassifier:
    def __init__(self, db_embeddings_context_manager):
        self.classifier = RandomForestClassifier(random_state=42)
        self.comparison = SimilarityGenerator(db_embeddings_context_manager)
        self.train_file = open(os.path.join(os.path.abspath('.'), 'train.csv'))
        self.csv_reader_train = csv.reader(self.train_file)
        self.test_file = open(os.path.join(os.path.abspath('.'), 'test.csv'))
        self.csv_reader_test = csv.reader(self.test_file)
        self.batchsize = 1000

    def get_similarities(self, training = 1):
        if training == 1:
            rows = list(self.csv_reader_train)
        else:
            rows = list(self.csv_reader_test)
        X = []
        y = []
        for i in tqdm(range(len(rows)), desc='get similarities'):
            similarity_vec = []
            sim_row = self.comparison.get_similarity_vector(rows[i])
            similarity_vec.append(sim_row['name'])
            similarity_vec.append(sim_row['variant'])
            similarity_vec.append(sim_row['price'])
            similarity_vec.append(sim_row['image'])
            X.append(similarity_vec)
            y.append(int(rows[i][-1]))
        return X, y

    def test_classifier(self):
        X_test, y_test = self.get_similarities(training=0)
        y_pred = self.classifier.predict(np.array(X_test))
        logging.info(confusion_matrix(np.array(y_test), np.array(y_pred)))

    def train_classifier(self):
        X_train, y_train = self.get_similarities(training=1)
        self.classifier.fit(X=np.array(X_train), y=np.array(y_train))
        logging.info('Dumping random forest to file')
        filename = os.path.abspath(r'./random_forest.sav')
        with open(filename, 'wb') as file:
            pickle.dump(self.classifier, file)

