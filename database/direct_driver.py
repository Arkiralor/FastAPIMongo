"""
PyMongo for cases where we do not want to/cannot use AsyncIO for database queries.
"""

from pymongo import MongoClient
from settings.config import settings

cluster = MongoClient(settings.MONGO_URI)
py_db = cluster.fastapi