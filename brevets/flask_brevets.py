"""
Replacement for RUSA ACP brevet time calculator
(see https://rusa.org/octime_acp.html)

"""

import os
import flask
from flask import request
import arrow  # Replacement for datetime, based on moment.js
import acp_times  # Brevet time calculations
import config

from pymongo import MongoClient
from mypymongo import brevet_insert, brevet_fetch

import logging


# set up Flask app
app = flask.Flask(__name__)
CONFIG = config.configuration()

# set up MongoDB connection
client = MongoClient('mongodb://' + os.environ['MONGODB_HOSTNAME'], 27017)

# use database "brevets"
db = client.brevets

# use collection "races"
collection = db.races


##################################################
################ MongoDB Functions ############### 
##################################################

# TODO:
# def get_brevet():
#     """
#     Obtains the newest document in the "races" collection in database "brevets".

#     Returns start time, distance, and controls (list of dictionaries) as list?
#     """
#     # Get documents (rows) in our collection (table),
#     # Sort by primary key in descending order and limit to 1 document (row)
#     # This will translate into finding the newest inserted document.

#     lists = collection.find().sort("_id", -1).limit(1)

#     # lists is a PyMongo cursor, which acts like a pointer.
#     # We need to iterate through it, even if we know it has only one entry:
#     for li in lists:
#         # We store all of our lists as documents with three fields:
#         ## start_time: begin time of the brevet
#         ## brevet_dist: distance of brevet
#         ## controls: list of controls 

#         # every control has four fields:
#         ## miles
#         ## km
#         ## open
#         ## close
#         return li["start_time"], li["brevet_dist"], li["controls"]

## TODO:
# def insert_brevet(title, items):
#     """
#     Inserts a new to-do list into the database "todo", under the collection "lists".
    
#     Inputs a title (string) and items (list of dictionaries)

#     Returns the unique ID assigned to the document by mongo (primary key.)
#     """
#     output = collection.insert_one({
#         "title": title,
#         "items": items})
#     _id = output.inserted_id # this is how you obtain the primary key (_id) mongo assigns to your inserted document.
#     return str(_id)



##################################################
################## Flask routes ################## 
##################################################

# AJAX request handlers
# These return JSON, rather than rendering pages.

# TODO: need to make 2 more app routes for insert and fetch
# get the info that JS gives them (in a similar way to kms, etc below):
# km = request.args.get('km', 999, type=float)


@app.route("/")
@app.route("/index")
def index():
    app.logger.debug("Main page entry")
    return flask.render_template('calc.html')


@app.errorhandler(404)
def page_not_found(error):
    app.logger.debug("Page not found")
    return flask.render_template('404.html'), 404


@app.route("/_calc_times")
def _calc_times():
    """
    Calculates open/close times from miles, using rules
    described at https://rusa.org/octime_alg.html.
    Expects one URL-encoded argument, the number of miles.
    """

    app.logger.debug("Got a JSON request")

    # TODO: handle errors by returning a JSON (?)
    # mentioned in lab, but idt its required, just good practice

    # get values from webpage
    km = request.args.get('km', 999, type=float)
    brevet_dist = request.args.get('brevet_dist', 999, type=float)
    start_time = request.args.get('start_time', type=str)

    # convert start_time string --> arrow object
    start_time_arrow = arrow.get(start_time, 'YYYY-MM-DD[T]HH:mm')

    # app.logger.debug(f"km = {km}")
    # app.logger.debug(f"brevet_dist = {brevet_dist}")
    # app.logger.debug(f"start_time = {start_time}")
    # app.logger.debug(f"start_time_arrow = {start_time_arrow}")
    # app.logger.debug(f"request.args: {request.args}")

    open_time = acp_times.open_time(km, brevet_dist, start_time_arrow).format('YYYY-MM-DDTHH:mm')    
    close_time = acp_times.close_time(km, brevet_dist, start_time_arrow).format('YYYY-MM-DDTHH:mm')

    result = {"open": open_time, "close": close_time}
    return flask.jsonify(result=result)


@app.route("/insert_brevet", methods=["POST"])
def insert():
    """
    /insert_brevet : inserts a brevet into the database.

    Accepts POST requests ONLY!

    JSON interface: gets JSON, responds with JSON
    """

    try:
        # Read the entire request body as a JSON
        # This will fail if the request body is NOT a JSON.
        input_json = request.json
        # if successful, input_json is automatically parsed into a python dictionary!
        
        # Because input_json is a dictionary, we can do this:
        start_time = input_json["start_time"] # Should be a string
        brevet_dist = input_json["brevet_dist"] # Should be a list of dictionaries
        controls = input_json["controls"]

        todo_id = insert_todo(title, items)

        return flask.jsonify(result={},
                        message="Inserted!", 
                        status=1, # This is defined by you. You just read this value in your javascript.
                        mongo_id=todo_id)
    except:
        # The reason for the try and except is to ensure Flask responds with a JSON.
        # If Flask catches your error, it means you didn't catch it yourself,
        # And Flask, by default, returns the error in an HTML.
        # We want /insert to respond with a JSON no matter what!
        return flask.jsonify(result={},
                        message="Oh no! Server error!", 
                        status=0, 
                        mongo_id='None')


# @app.route("/fetch_brevet")
# def fetch():
#     """
#     /fetch_brevet : fetches the newest brevet from the database.

#     Accepts GET requests ONLY!

#     JSON interface: gets JSON, responds with JSON
#     """
#     try:
#         title, items = get_todo()
#         return flask.jsonify(
#                 result={"title": title, "items": items}, 
#                 status=1,
#                 message="Successfully fetched a to-do list!")
#     except:
#         return flask.jsonify(
#                 result={}, 
#                 status=0,
#                 message="Something went wrong, couldn't fetch any lists!")




##################################################
################# Start Flask App ################ 
##################################################

app.debug = CONFIG.DEBUG
if app.debug:
    app.logger.setLevel(logging.DEBUG)

if __name__ == "__main__":
    print("Opening for global access on port {}".format(CONFIG.PORT))
    app.run(port=CONFIG.PORT, host="0.0.0.0")
