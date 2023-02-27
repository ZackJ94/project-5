"""
Nose tests for mypymongo.py

Write your tests HERE AND ONLY HERE.
"""

# FIXME: python refactored this import automatically, is it working?
from brevets.mypymongo import brevet_insert, brevet_fetch

import arrow
import nose    # Testing framework
import logging

logging.basicConfig(format='%(levelname)s:%(message)s',
                    level=logging.WARNING)
log = logging.getLogger(__name__)


# TODO: copy basic structure of test_acp_times.py for test cases here
