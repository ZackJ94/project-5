"""
Nose tests for acp_times.py

Write your tests HERE AND ONLY HERE.
"""

from acp_times import open_time, close_time
import arrow

import nose    # Testing framework
import logging

logging.basicConfig(format='%(levelname)s:%(message)s',
                    level=logging.WARNING)
log = logging.getLogger(__name__)


# every test is a full race

def test_brevet1():
    start_time = arrow.get("2023-02-17 00:00", "YYYY-MM-DD HH:mm")
    dist = 200

    checkpoints = {
        0: (start_time, start_time.shift(hours=1)),
        50: (start_time.shift(hours=1, minutes=28), start_time.shift(hours=3, minutes=30)),
        150: (start_time.shift(hours=4, minutes=25), start_time.shift(hours=10)),
        200: (start_time.shift(hours=5, minutes=53), start_time.shift(hours=13, minutes=30))
    }

    # iterate through key/val pairs
    for km, time_tuple in checkpoints.items():
        checkpoint_open, checkpoint_close = time_tuple

        assert open_time(km, dist, start_time) == checkpoint_open
        assert close_time(km, dist, start_time) == checkpoint_close

def test_brevet2():
    start_time = arrow.get("2023-02-17 00:00", "YYYY-MM-DD HH:mm")
    dist = 200

    checkpoints = {
        0: (start_time, start_time.shift(hours=1)),
        60: (start_time.shift(hours=1, minutes=46), start_time.shift(hours=4)),
        120: (start_time.shift(hours=3, minutes=32), start_time.shift(hours=8)),
        175: (start_time.shift(hours=5, minutes=9), start_time.shift(hours=11, minutes=40)),
        200: (start_time.shift(hours=5, minutes=53), start_time.shift(hours=13, minutes=30)),
        220: (start_time.shift(hours=5, minutes=53), start_time.shift(hours=13, minutes=30))
    }

    # iterate through key/val pairs
    for km, time_tuple in checkpoints.items():
        checkpoint_open, checkpoint_close = time_tuple

        assert open_time(km, dist, start_time) == checkpoint_open
        assert close_time(km, dist, start_time) == checkpoint_close

def test_brevet3():
    start_time = arrow.get("2023-02-17 00:00", "YYYY-MM-DD HH:mm")
    dist = 1000

    checkpoints = {
        0: (start_time, start_time.shift(hours=1)),
        10: (start_time.shift(minutes=18), start_time.shift(hours=1, minutes=30)),
        20: (start_time.shift(minutes=35), start_time.shift(hours=2)),
        40: (start_time.shift(hours=1, minutes=11), start_time.shift(hours=3)),
        200: (start_time.shift(hours=5, minutes=53), start_time.shift(hours=13, minutes=20)),
        400: (start_time.shift(hours=12, minutes=8), start_time.shift(days=1, hours=2, minutes=40)),
        600: (start_time.shift(hours=18, minutes=48), start_time.shift(days=1, hours=16)),
        1000: (start_time.shift(days=1, hours=9, minutes=5), start_time.shift(days=3, hours=3)),
        1200: (start_time.shift(days=1, hours=9, minutes=5), start_time.shift(days=3, hours=3))
    }

    # iterate through key/val pairs
    for km, time_tuple in checkpoints.items():
        checkpoint_open, checkpoint_close = time_tuple

        assert open_time(km, dist, start_time) == checkpoint_open
        assert close_time(km, dist, start_time) == checkpoint_close

def test_brevet4():
    start_time = arrow.get("2023-02-17 00:00", "YYYY-MM-DD HH:mm")
    dist = 600

    checkpoints = {
        0: (start_time, start_time.shift(hours=1)),
        10: (start_time.shift(minutes=18), start_time.shift(hours=1, minutes=30)),
        199: (start_time.shift(hours=5, minutes=51), start_time.shift(hours=13, minutes=16)),
        201: (start_time.shift(hours=5, minutes=55), start_time.shift(hours=13, minutes=24)),
        599: (start_time.shift(hours=18, minutes=46), start_time.shift(days=1, hours=15, minutes=56)),
        601: (start_time.shift(hours=18, minutes=48), start_time.shift(days=1, hours=16))
    }

    # iterate through key/val pairs
    for km, time_tuple in checkpoints.items():
        checkpoint_open, checkpoint_close = time_tuple

        assert open_time(km, dist, start_time) == checkpoint_open
        assert close_time(km, dist, start_time) == checkpoint_close

def test_brevet5():
    start_time = arrow.get("2023-02-17 00:00", "YYYY-MM-DD HH:mm")
    dist = 1000

    checkpoints = {
        0: (start_time, start_time.shift(hours=1)),
        1: (start_time.shift(minutes=2), start_time.shift(hours=1, minutes=3)),
        1000: (start_time.shift(days=1, hours=9, minutes=5), start_time.shift(days=3, hours=3))
    }

    # iterate through key/val pairs
    for km, time_tuple in checkpoints.items():
        checkpoint_open, checkpoint_close = time_tuple

        assert open_time(km, dist, start_time) == checkpoint_open
        assert close_time(km, dist, start_time) == checkpoint_close