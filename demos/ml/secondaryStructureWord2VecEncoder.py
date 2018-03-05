#!/usr/bin/env python
'''secondaryStructureWord2VecEncoder.py

Authorship information:
    __author__ = "Mars (Shih-Cheng) Huang"
    __maintainer__ = "Mars (Shih-Cheng) Huang"
    __email__ = "marshuang80@gmail.com:
    __status__ = "Debug"
'''

from pyspark import SparkConf, SparkContext, SQLContext
from mmtfPyspark.ml import ProteinSequenceEncoder
from mmtfPyspark.mappers import StructureToPolymerChains
from mmtfPyspark.filters import ContainsLProteinChain
from mmtfPyspark.datasets import secondaryStructureSegmentExtractor
from mmtfPyspark.webFilters import Pisces
from mmtfPyspark.io import mmtfReader
import time

# TODO data count is more than Java


def main():
    '''This class creates a dataset of sequence segment derived from a
    non-redundant set. The dataset contains the sequence segment, the DSSP
    Q8 and DSSP Q3 code of the center residue in a sequence segment, and a
    Word2Vec encoding of the sequence segment.
    The Data is saved in JSON file specified by the user.
    '''

    start = time.time()

    conf = SparkConf() \
        .setMaster("local[*]") \
        .setAppName("secondaryStructureWord2VecEncodeDemo")
    sc = SparkContext(conf=conf)

    # Read MMTF Hadoop sequence file and create a non-redundant set
    # (<=20% seq. identity) of L-protein chains

    path = "../../resources/mmtf_reduced_sample/"

    sequenceIdentity = 20
    resolution = 2.0
    fraction = 0.1
    seed = 123

    pdb = mmtfReader \
        .read_sequence_file(path, sc) \
        .flatMap(StructureToPolymerChains()) \
        .filter(Pisces(sequenceIdentity, resolution)) \
        .filter(ContainsLProteinChain()) \
        .sample(False, fraction, seed)

    segmentLength = 11
    data = secondaryStructureSegmentExtractor.get_dataset(
        pdb, segmentLength).cache()

    # add Word2Vec encoded feature vector
    encoder = ProteinSequenceEncoder(data)
    n = 2
    windowSize = (segmentLength - 1) // 2
    vectorSize = 50
    data = encoder.overlapping_ngram_word2vec_encode(n, windowSize, vectorSize)

    data.printSchema()
    data.show(25, False)

    end = time.time()

    print("Time: %f  sec." % (end - start))

    sc.stop()


if __name__ == "__main__":
    main()
