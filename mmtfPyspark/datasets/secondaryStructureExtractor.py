#!/user/bin/env python
'''secondaryStructureExtractor.py

Creates a dataset of 3-state secondary structure
(alpha, beta, coil) derived from the DSSP secondary structure
assignment. The dateset consists of three columns
with the fraction of alpha, beta and coil within a chain.
The input to this class must be a single protein chain.

Authorship information:
    __author__ = "Mars (Shih-Cheng) Huang"
    __maintainer__ = "Mars (Shih-Cheng) Huang"
    __email__ = "marshuang80@gmail.com:
    __status__ = "Done"
'''

from mmtfPyspark.ml import pythonRDDToDataset
from mmtfPyspark.utils import DsspSecondaryStructure
from pyspark.sql import Row


def getDataset(structure):
    '''Returns a dataset of 3-state secondary structure
    '''

    rows = structure.map(lambda x: getSecStructFractions(x)) #Map or flatMap

    # convert to dataset
    colNames = ["structureChainId", "sequence", "alpha", "beta",
                "coil", "dsspQ8Code", "dsspQ3Code"]

    return pythonRDDToDataset.getDataset(rows, colNames)


def getPythonRdd(structure):
    '''
    Returns a pythonRDD of 3-state secondary structure
    '''

    return structure.map(lambda x: getSecStructFractions(x))


def getSecStructFractions(t):
    '''
    Get factions of alpha, beta and coil within a chain
    '''

    key = t[0]
    structure = t[1]
    if structure.num_chains != 1:
        raise Exception("This method can only be applied to single polyer chain.")

    dsspQ8, dsspQ3 = '', ''

    helix = 0
    sheet = 0
    coil = 0
    dsspIndex = 0
    structureIndex = 0

    for code in structure.sec_struct_list:

        seqIndex = structure.sequence_index_list[structureIndex]

        while dsspIndex < seqIndex:
            dsspQ3 += "X"
            dsspQ8 += "X"
            dsspIndex += 1

        structureIndex += 1
        dsspQ8 += DsspSecondaryStructure.get_dssp_code(code).get_one_letter_code()
        dsspIndex += 1

        q3 = DsspSecondaryStructure.get_q3_code(code).name
        if q3 == "ALPHA_HELIX":
            helix += 1
            dsspQ3 += "H"
        elif q3 == "EXTENDED":
            sheet +=1
            dsspQ3 += "E"
        elif q3 == "COIL":
            coil += 1
            dsspQ3 += "C"

    while dsspIndex < len(structure.entity_list[0]['sequence']):
        dsspQ8 += "X"
        dsspQ3 += "X"
        dsspIndex += 1

    n = len(structure.sec_struct_list)

    helix /= n
    sheet /= n
    coil /= n

    return Row(key, structure.entity_list[0]['sequence'], helix, sheet,
               coil, dsspQ8, dsspQ3)
