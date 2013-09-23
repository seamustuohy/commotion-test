"""
Evaluation tests for Commotion Networks.

"""

import unittest
import time
import logging
import sys
import os

from tests import test_connection
from tests import test_load

def create_metric_dir():
	num = 1
        date_string = time.strftime("%Y-%m-%d")
	metric_dir = "logs/"+date_string+"("+str(num)+")"
	while os.path.isdir(metric_dir):
                num += 1
                metric_dir = "logs/"+date_string+"("+str(num)+")"
        os.makedirs(metric_dir, 0x1C0)
        return metric_dir

def create_runner(suite_type, verbosity_level=None, runner_type="text"):
    """creates a testing runner.

    suite_type: (string) suites to run [acceptable values = suite_types in build_suite()]
    runner_type: (string) type of runner to create. [implemented values = 'text']
    """
    metric_dir = create_metric_dir()
    f = None
    if runner_type == "text":
        runner = unittest.TextTestRunner(verbosity=verbosity_level)
    else:
        log_file = metric_dir+"/testSuite"
        f = open(log_file, "w")
        runner = unittest.TextTestRunner(f, verbosity=verbosity_level)
    print("LOGFILE: -> "+metric_dir)
    test_suite = build_suite(suite_type)
    runner.run (test_suite)
    if f:
        f.close()

def build_suite(suite_type):
    suite = unittest.TestSuite()
    suite_types = {"all": [test_connection.testFunctions, test_load.testFunctions], "connection":[test_connection.testFunctions]}
    for test_case in suite_types[suite_type]:
        suite.addTest (unittest.makeSuite(test_case))
    return suite


if __name__ == '__main__':
    """Creates argument parser for required arguments and calls test runner"""
    import argparse
    parser = argparse.ArgumentParser(description='openThreads test suite')
    parser.add_argument("-s", "--suite", nargs="?", default="all", const="all", dest="suite_type", metavar="SUITE", help="Pick a specific test suite")
    parser.add_argument("-v", "--verbosity", nargs="?", default=None, const=2, dest="verbosity_level", metavar="VERBOSITY", help="make test_suite verbose")
    parser.add_argument("-l", "--logfile", nargs="?", default="text", const="commotion_test.log", dest="logfile", metavar="LOGFILE", help="Specify an alternative logfile name")

    args = parser.parse_args()
    create_runner(args.suite_type, args.verbosity_level, args.logfile)

