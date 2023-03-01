"""
Nose tests for mypymongo.py

Write your tests HERE AND ONLY HERE.
"""

from mypymongo import brevet_insert, brevet_fetch

import arrow
import nose
import logging

logging.basicConfig(format='%(levelname)s:%(message)s',
                    level=logging.WARNING)
log = logging.getLogger(__name__)


def test_brevet_insert():
    brevet_dist = 200
    start_time = "2021-01-01T00:00"
    controls = [
        {"miles": 0.000000, "km": 0, "open": start_time, "close": '2021-01-01T01:00', "location": 'starting line'},
        {"miles": 6.213710, "km": 10, "open": '2021-01-01T00:18', "close": '2021-01-01T01:30', "location": ''},
        {"miles": 34.175405, "km": 55, "open": '2021-01-01T01:37', "close": '2021-01-01T03:45', "location": ''},
        {"miles": 62.137100, "km": 100, "open": '2021-01-01T02:56', "close": '2021-01-01T06:40', "location": ''},
        {"miles": 93.205650, "km": 150, "open": '2021-01-01T04:25', "close": '2021-01-01T10:00', "location": 'Paris, TX'},
        {"miles": 124.274200, "km": 200, "open": '2021-01-01T05:53', "close": '2021-01-01T13:30', "location": 'Paris, France'},
        {"miles": 149.129040, "km": 240, "open": '2021-01-01T05:53', "close": '2021-01-01T13:30', "location": 'Paris Texas Again??'}
    ]

    inserted = brevet_insert(start_time, brevet_dist, controls)
    assert(inserted != None)


def test_brevet_fetch():
    brevet_dist = 200
    start_time = "2021-01-01T00:00"
    controls = [
        {"miles": 0.000000, "km": 0, "open": start_time, "close": '2021-01-01T01:00', "location": 'starting line'},
        {"miles": 6.213710, "km": 10, "open": '2021-01-01T00:18', "close": '2021-01-01T01:30', "location": ''},
        {"miles": 34.175405, "km": 55, "open": '2021-01-01T01:37', "close": '2021-01-01T03:45', "location": ''},
        {"miles": 62.137100, "km": 100, "open": '2021-01-01T02:56', "close": '2021-01-01T06:40', "location": ''},
        {"miles": 93.205650, "km": 150, "open": '2021-01-01T04:25', "close": '2021-01-01T10:00', "location": 'Paris, TX'},
        {"miles": 124.274200, "km": 200, "open": '2021-01-01T05:53', "close": '2021-01-01T13:30', "location": 'Paris, France'},
        {"miles": 149.129040, "km": 240, "open": '2021-01-01T05:53', "close": '2021-01-01T13:30', "location": 'Paris Texas Again??'}
    ]

    inserted = brevet_insert(start_time, brevet_dist, controls)

    fetched = brevet_fetch()
    fetched_tuple = (start_time, brevet_dist, controls)

    assert(fetched == fetched_tuple)

