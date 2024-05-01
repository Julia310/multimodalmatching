from Database.Models.baseModel import BaseModel
from peewee import *

"""
    Models to save the classified ( Matches class ) and for persisting the true classified_matches ( TrueMatches class )
"""

class Matches(BaseModel):
    zal_id = CharField()
    th_gw_id = CharField()


class TrueMatches(BaseModel):
    zal_id = CharField()
    th_gw_id = CharField()


class TommyHilfigerIds(BaseModel):
    ref_id = CharField()


class GerryWeberIds(BaseModel):
    ref_id = CharField()
