import os
from pymongo import MongoClient


"""
we are creating an interface like this for testing.
Easiest test to write would be to just insert a brevet, 
then find that brevet and check if the two match:)

Should just be a couple lines, but writing it in the flask file
would make it harder to work with and test
"""

client = MongoClient('mongodb://' + os.environ['MONGODB_HOSTNAME'], 27017)
db = client.mydb

def brevet_insert(start_time, brev_dist, checkpoints):
    pass

def brevet_find():
    # return start_time, brevet_dist, checkpoints
    # [dont have to follow this exactly]
    pass
