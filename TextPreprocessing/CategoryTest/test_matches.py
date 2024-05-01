import os
import csv
import pandas as pd
import logging

gw = os.path.abspath('../../Datasets/clean_GerryWeber.csv')
th = os.path.abspath('../../Datasets/clean_TommyHilfiger.csv')
zal = os.path.abspath('../../Datasets/clean_Zalando.csv')

gw_zal = os.path.abspath('../../Datasets/matches_zalando_gerryweber.csv')
th_zal = os.path.abspath('../../Datasets/matches_zalando_tommyhilfiger.csv')


def test_matches(matches, df1, df2):
    file = open(matches)
    csv_reader = csv.reader(file)
    next(csv_reader)

    correct_count = 0
    wrong_count = 0

    for rec in csv_reader:
        cat1 = df1.loc[df1['id'] == rec[0]]['category'].tolist()[0]
        cat2 = df2.loc[df2['id'] == rec[1]]['category'].tolist()[0]

        if not cat1 == cat2:
            logging.info('================================================')

            logging.info(df1.loc[df1['id'] == rec[0]])
            logging.info(df2.loc[df2['id'] == rec[1]])

            logging.info('================================================')
            wrong_count += 1
        else:
            correct_count += 1

    logging.info('Matches found: ' + str(correct_count))
    logging.info('Not found: ' + str(wrong_count))


def main():
    """
        Test to check how many classified_matches will be lost after blocking by adding categories to the data
    """
    df2 = pd.read_csv(gw)
    df_zal = pd.read_csv(zal)
    test_matches(gw_zal, df_zal, df2)
    df2 = pd.read_csv(th)
    test_matches(th_zal, df_zal, df2)


if __name__ == "__main__":
    main()
