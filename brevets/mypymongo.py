
"""
we are creating this interface for testing.

Easiest test to write:
1. insert a brevet
2. find brevet
3. check if the two match :)
"""

import os
from pymongo import MongoClient


client = MongoClient('mongodb://' + os.environ['MONGODB_HOSTNAME'], 27017)

db = client.mydb

def brevet_insert(start_time, brev_dist, checkpoints):
    pass


def brevet_fetch():
    # return start_time, brevet_dist, checkpoints
    # [dont have to follow this exactly]
    pass
