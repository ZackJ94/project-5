
"""
interface for brevet interactions
mainly factored out for testing
"""

import os
from pymongo import MongoClient


# set up MongoDB connection
client = MongoClient('mongodb://' + os.environ['MONGODB_HOSTNAME'], 27017)

# use database "brevets"
db = client.brevets

# use collection "races"
collection = db.races


##################################################
################ MongoDB Functions ############### 
##################################################

def brevet_insert(start_time, brevet_dist, controls):
    """
    Inserts a new to-do list into the database "brevets", under the collection "races"
    Inputs a start time (string?), brev_dist (string?), and controls (list of dictionaries)
    Returns the unique ID assigned to the document by mongo (primary key.)
    """
    output = collection.insert_one({
        "start_time": start_time,
        "brevet_dist": brevet_dist,
        "controls": controls
        })
    
    #  this is how you obtain the primary key (_id) mongo assigns to your inserted document.
    _id = output.inserted_id
    return str(_id)


def brevet_fetch():
    """
    Obtains the newest document in the "races" collection in database "brevets"
    Returns start time, distance, and controls (list of dictionaries) as tuple
    """
    # Get documents (rows) in our collection (table),
    # Sort by primary key in descending order and limit to 1 document (row)
    # This will translate into finding the newest inserted document.
    lists = collection.find().sort("_id", -1).limit(1)

    # lists is a PyMongo cursor, which acts like a pointer.
    # We need to iterate through it, even if we know it has only one entry:
    for li in lists:
        return li["start_time"], li["brevet_dist"], li["controls"]
