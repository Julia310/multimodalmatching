from Database.dbContext import mysql_db
from Database.Models.utilityModels import Similarities


class DbUtilityContextManager:
    """
        Database context to save all calculated similarities of the potential classified_matches after performing blocking.
        Used to Explore different threshold_classification thresholds.
    """

    def __init__(self):
        self.connection = mysql_db
        self.similarities = Similarities
        self.batch_size = 1000

    def save_similarity_vector(self, similarity_dict):
        self.similarities.insert([similarity_dict]).execute()

    def recreate_tables(self):
        if self.similarities.table_exists():
            self.similarities.drop_table()
        self.similarities.create_table()
