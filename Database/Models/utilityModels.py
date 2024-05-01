from Database.Models.baseModel import BaseModel
from peewee import *

"""
    Utility Model not required in the final pipeline.
    Utilized for similarity threshold exploration in the database
"""

class Similarities(BaseModel):
    zal_id = CharField()
    th_gw_id = CharField()
    name = FloatField()
    variant = FloatField()
    price = FloatField()
    image = FloatField()