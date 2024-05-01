from Database.Models.baseModel import BaseModel
from peewee import *

"""
    Models to save the embeddings as bytes with the price float value for later similarity computation
"""

class ZalandoEmbeddings(BaseModel):
    articleId = CharField(unique=True)
    name = BlobField()
    variant = BlobField()
    price = CharField()
    image = BlobField()


class TommyHGerryWEmbeddings(BaseModel):
    articleId = CharField(unique=True)
    name = BlobField()
    variant = BlobField()
    price = CharField()
    image = BlobField()
