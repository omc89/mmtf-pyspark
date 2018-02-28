#!/usr/bin/env python
'''
readSequenceFromListTest.py: Example reading a list of PDB IDs from a local MMTF Hadoop sequence \
file into a tubleRDD.

Authorship information:
__author__ = "Mars (Shih-Cheng) Huang"
__maintainer__ = "Mars (Shih-Cheng) Huang"
__email__ = "marshuang80@gmail.com:
__status__ = "Warning"
'''

import unittest
from pyspark import SparkConf, SparkContext
from mmtfPyspark.io import mmtfReader


class ReadSequenceFileTest(unittest.TestCase):

    def setUp(self):
        conf = SparkConf().setMaster(
            "local[*]").setAppName('read_sequence_file')
        self.sc = SparkContext(conf=conf)

    def test_mmtf(self):
        path = './resources/files/'
        pdb = mmtfReader.readMmtfFiles(path, self.sc)

        self.assertTrue(pdb.count() == 3)

    def tearDown(self):
        self.sc.stop()


if __name__ == '__main__':
    unittest.main()
