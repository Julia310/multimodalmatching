from peewee import Model
from Database.dbContext import mysql_db


class BaseModel(Model):
    """A base model that will use our database"""

    class Meta:
        database = mysql_db
