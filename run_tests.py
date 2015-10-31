#!/usr/bin/env python

r"""
Responsible for test running
"""

import os
import sys
import unittest
import argparse


if __name__ == "__main__":
    try:
        THIS = __file__
    except NameError:
        THIS = sys.argv[0]

    ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(THIS), '.'))
    TESTS_DIR = os.path.join(ROOT_DIR, 'tests/')

    PARSER = argparse.ArgumentParser(description="Runs test for sbtool.")
    PARSER.add_argument('--test_filter', dest='test_filter', action='store',
                        default="*", help='Test filter')

    ARGS = PARSER.parse_args()

    TESTS = unittest.TestLoader().discover(TESTS_DIR, pattern=ARGS.test_filter)
    unittest.TextTestRunner(verbosity=2).run(TESTS)
