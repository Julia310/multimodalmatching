from Database.dbContext import mysql_db
from Database.Models.matchingEvaluationModels import Matches, TrueMatches, TommyHilfigerIds, GerryWeberIds
import logging
from peewee import JOIN


class DbMatchesContextManager:
    """
        Persists classified and true classified_matches to database and enables methods to access these.
        Emables to receive data for the evaluation of threshold_classification of the whole matching process.
    """

    def __init__(self):
        self.connection = mysql_db
        self.classified_matches = Matches
        self.true_matches = TrueMatches
        self.batch_size = 1000
        self.tommy_hilfiger_ids = TommyHilfigerIds
        self.gerry_weber_ids = GerryWeberIds

    def save_match(self, article_ids):
        matches_dict = {
            'zal_id': article_ids[0],
            'th_gw_id': article_ids[1]
        }
        self.classified_matches.insert([matches_dict]).execute()

    def save_many_matches(self, matches):
        self.classified_matches.insert_many(matches).execute()

    def save_true_matches(self, matches):
        with self.connection.atomic():
            for idx in range(0, len(matches), self.batch_size):
                idx_max = len(matches)
                if idx + self.batch_size < idx_max:
                    idx_max = idx + self.batch_size
                val_to_table = matches[idx:idx_max]
                query = self.true_matches.insert_many(val_to_table)
                query.execute()
                logging.info(str(idx_max) + ' rows inserted')

    def \
            recreate_tables(self):
        if self.classified_matches.table_exists():
            self.classified_matches.drop_table()
        if self.true_matches.table_exists():
            self.true_matches.drop_table()
        if self.tommy_hilfiger_ids.table_exists():
            self.tommy_hilfiger_ids.drop_table()
        if self.gerry_weber_ids.table_exists():
            self.gerry_weber_ids.drop_table()
        self.true_matches.create_table()
        self.classified_matches.create_table()
        self.gerry_weber_ids.create_table()
        self.tommy_hilfiger_ids.create_table()

    def get_classification_evaluation_data(self, total_potential_matches):
        # number of true matches from database
        query = self.true_matches.select()
        total_true_matches = len(query)
        # number of classified matches
        query = self.classified_matches.select()
        classified_matches = len(query)
        # Join true matches and classified matches to get the number of true positives
        join_cond = (
                (Matches.zal_id == TrueMatches.zal_id) &
                (Matches.th_gw_id == TrueMatches.th_gw_id))
        query = (self.true_matches.select().join(self.classified_matches, JOIN.INNER, on=join_cond))
        true_positives = len(query)
        false_negatives = total_true_matches - true_positives
        false_positives = classified_matches - true_positives
        true_negatives = total_potential_matches - true_positives - false_negatives - false_positives

        return true_positives, false_positives, false_negatives, true_negatives

    def get_th_gw_classification_evaluation_data(self, total_potential_matches, data_alias):

        if data_alias == 'gw':
            table = GerryWeberIds
        else:
            table = TommyHilfigerIds

        # number of true matches from database
        join_cond = (table.ref_id == TrueMatches.th_gw_id)
        query = (self.true_matches.select().join(table, JOIN.INNER, on=join_cond))
        th_gw_total_true_matches = len(query)

        # number of classified matches
        join_cond = (table.ref_id == Matches.th_gw_id)
        query = (self.classified_matches.select().join(table, JOIN.INNER, on=join_cond))
        classified_matches = len(query)
        # Join true matches and classified matches to get the number of true positives
        join_cond = (
                (Matches.zal_id == TrueMatches.zal_id) &
                (Matches.th_gw_id == TrueMatches.th_gw_id))
        join_ref_table_cond = (
            (table.ref_id == TrueMatches.th_gw_id)
        )
        query = self.true_matches.select()
        query = query.join(self.classified_matches, JOIN.INNER, on=join_cond)
        query = query.join(table, JOIN.INNER, on=join_ref_table_cond)
        true_positives = len(query)
        false_negatives = th_gw_total_true_matches - true_positives
        false_positives = classified_matches - true_positives
        true_negatives = total_potential_matches - true_positives - false_negatives - false_positives

        return true_positives, false_positives, false_negatives, true_negatives

    def save_th_gw_ids(self, data_alias, ids):
        if data_alias == 'gw':
            table = self.gerry_weber_ids
        else:
            table = self.tommy_hilfiger_ids

        with self.connection.atomic():
            for idx in range(0, len(ids), self.batch_size):
                idx_max = len(ids)
                if idx + self.batch_size < idx_max:
                    idx_max = idx + self.batch_size
                val_to_table = ids[idx:idx_max]
                query = table.insert_many(val_to_table)
                query.execute()
                logging.info(str(idx_max) + ' rows inserted')


