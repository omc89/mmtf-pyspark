#!/usr/bin/env python
'''
JpredDemo.py:


Authorship information:
    __author__ = "Mars (Shih-Cheng) Huang"
    __maintainer__ = "Mars (Shih-Cheng) Huang"
    __email__ = "marshuang80@gmail.com:
    __status__ = "Done"
'''

from pyspark import SparkConf, SparkContext, SQLContext
from mmtfPyspark.datasets import jpredDataset
import time


def main():
    start = time.time()

    conf = SparkConf().setMaster("local[*]") \
                      .setAppName("JpredDemo")
    sc = SparkContext(conf = conf)

    # Read Jpred Dataset
    res = jpredDataset.get_dataset()
    res.show(10)

    # Write to Json file
    res = res.coalesce(1)
    res.write.format("json").save("./JpredData3")


    end = time.time()

    print("Time: %f  sec." %(end-start))

    sc.stop()

if __name__ == "__main__":
    main()
