import os
import csv
import random
from sklearn.model_selection import train_test_split
import numpy as np


def load_true_matches():
    true_match_files = [
        os.path.join(os.path.abspath('../Datasets'), 'matches_zalando_gerryweber.csv'),
        os.path.join(os.path.abspath('../Datasets'), 'matches_zalando_tommyhilfiger.csv')
    ]
    true_matches = []
    for filename in true_match_files:
        file = open(filename)
        csv_reader = csv.reader(file)
        next(csv_reader)

        for rec in csv_reader:
            true_matches.append(rec + [1])

    return true_matches


def data_to_csv(filename, data):
    filename = os.path.join(os.path.abspath('.'), filename)
    with open(filename, 'w', newline='') as csvfile:
        csv_writer = csv.writer(csvfile, delimiter=',',
                                quotechar='|', quoting=csv.QUOTE_MINIMAL)

        data = data.tolist()
        for i in range(len(data)):
            row = data[i]
            csv_writer.writerow(row)


def get_no_match_percentage(number_no_matches, true_no_matches):
    no_matches = 0
    keys = list(true_no_matches.keys())
    for key in keys:
        no_matches += len(true_no_matches[key])
    return float(number_no_matches) / float(no_matches)


class TrainingPreparation:

    def __init__(self, m_utilities, number_no_matches, matches_train_test_split, no_matches_train_test_split):
        self.true_matches = load_true_matches()
        self.number_no_matches = number_no_matches
        self.matches_train_test_split = matches_train_test_split
        self.no_matches_train_test_split = no_matches_train_test_split
        self.no_match_dict = self.get_true_no_match_dict(m_utilities.potential_matches)
        self.no_match_percentage = get_no_match_percentage(number_no_matches, self.no_match_dict)
        self.true_no_matches = self.get_true_no_matches()
        self.X_train, self.X_test, self.y_train, self.y_test = self.create_train_test_split()
        self.shuffle_train_test_data()
        self.batch_size = 100
        self.idx_min = 0
        self.idx_max = 100

    def get_true_no_matches(self):
        keys = list(self.no_match_dict.keys())
        no_matches = []
        for key in keys:
            no_matches += self.get_sublist(self.no_match_dict[key])
        return no_matches

    # get 10 percent of elements from list randomly
    def get_sublist(self, complete_list):
        percentage = self.no_match_percentage
        k = int(len(complete_list) * percentage)
        indices = random.sample(range(len(complete_list)), k)
        # indices = random.sample(range(len(complete_list)), no_matches_number)
        sublist = [complete_list[i] for i in indices]
        return sublist

    def get_true_no_match_dict(self, potential_matches):
        keys = potential_matches.keys()
        no_matches_dict = {}
        for key in keys:
            no_matches_dict[key] = []
            for potential_match in potential_matches[key]:
                if not list(potential_match) + [1] in self.true_matches:
                    no_matches_dict[key].append(list(potential_match) + [0])

        return no_matches_dict

    def create_train_test_split(self):
        self.true_matches = np.array(self.true_matches)
        self.true_no_matches = np.array(self.true_no_matches)
        X_train_match, X_test_match, y_train_match, y_test_match = train_test_split(self.true_matches[:, [0, 1]],
                                                                                    self.true_matches[:, 2],
                                                                                    train_size=self.matches_train_test_split,
                                                                                    shuffle=True)
        X_train_no_match, X_test_no_match, y_train_no_match, y_test_no_match = train_test_split(
            self.true_no_matches[:, [0, 1]], self.true_no_matches[:, 2], train_size=self.no_matches_train_test_split, shuffle=True)
        X_train = np.concatenate((X_train_match, X_train_no_match), axis=0)
        X_test = np.concatenate((X_test_match, X_test_no_match), axis=0)
        y_train = np.concatenate((y_train_match, y_train_no_match), axis=0)
        y_test = np.concatenate((y_test_match, y_test_no_match), axis=0)

        return X_train, X_test, y_train, y_test

    def shuffle_train_test_data(self):
        X_y_train = np.insert(self.X_train, 2, self.y_train, axis=1)
        X_y_test = np.insert(self.X_test, 2, self.y_test, axis=1)
        np.random.shuffle(X_y_train)
        np.random.shuffle(X_y_test)

        data_to_csv('test.csv', X_y_test)
        data_to_csv('train.csv', X_y_train)


