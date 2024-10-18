
from pymongo import MongoClient

dbconnection = MongoClient('mongodb://localhost:27017/')
db = dbconnection['Taxi']
