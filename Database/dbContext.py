from sys import platform
from peewee import MySQLDatabase
from abc import ABC
from playhouse.shortcuts import ReconnectMixin
from playhouse.mysql_ext import MariaDBConnectorDatabase

"""
    Defines the database connection depending on OS.
"""

if 'linux' in platform:
    class ReconnectMySQLDatabase(ReconnectMixin, MariaDBConnectorDatabase, ABC):
        pass

    mysql_db = ReconnectMySQLDatabase('dbprak_09', user='dbprak_09', password='hDVNlxpQHZGQRbv',
                                      host='wdi13.informatik.uni-leipzig.de', port=3406)
else:
    mysql_db = MySQLDatabase('MatchingData', user='root', password='asdfghjkl'
                                                                   '.54321', host='127.0.0.1', port=3306)






