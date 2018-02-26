#!/usr/bin/env python
'''FilterByExperimentalMethods.py:

Example how to filter PDB entries by experimental methods.
To learn more about <a href="http://pdb101.rcsb.org/learn/guide-to-understanding-pdb-data/methods-for-determining-structure">experimental methods</a>

Authorship information:
    __author__ = "Mars (Shih-Cheng) Huang"
    __maintainer__ = "Mars (Shih-Cheng) Huang"
    __email__ = "marshuang80@gmail.com:
    __status__ = "Done"
'''

from pyspark import SparkConf, SparkContext
from mmtfPyspark.io import MmtfReader
from mmtfPyspark.filters import ExperimentalMethods


def main():
    path = "../../resources/mmtf_reduced_sample/"

    conf = SparkConf().setMaster("local[*]") \
        .setAppName("FilterByDExperimentalMethods")
    sc = SparkContext(conf=conf)

    MmtfReader.read_sequence_file(path, sc) \
        .filter(ExperimentalMethods(ExperimentalMethods.NEUTRON_DIFFRACTION,
                                    ExperimentalMethods.X_RAY_DIFFRACTION)) \
        .keys() \
        .foreach(lambda x: print(x))

    sc.stop()


if __name__ == "__main__":
    main()
