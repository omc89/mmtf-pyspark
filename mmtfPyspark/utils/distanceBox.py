#!/user/bin/env python
'''
distanceBox.py:

This code is a modification from BioJava's distanceBox class

Reference:
    https://github.com/biojava/biojava/blob/359dce819e7678879ae41301b11fa268f92e81d1/biojava-structure/src/main/java/org/biojava/nbio/structure/symmetry/geometry/DistanceBox.java

Authorship information:
    __author__ = "Mars (Shih-Cheng) Huang"
    __maintainer__ = "Mars (Shih-Cheng) Huang"
    __email__ = "marshuang80@gmail.com:
    __status__ = "debug"
'''
import numpy as np
from collections import defaultdict

class DistanceBox(object):

    offset = [
        0 + ( 0 * 10000) + ( 0 * 1000000000),
	   -1 + (-1 * 10000) + (-1 * 1000000000),
	   -1 + (-1 * 10000) + ( 0 * 1000000000),
	   -1 + (-1 * 10000) + ( 1 * 1000000000),
	   -1 + ( 0 * 10000) + (-1 * 1000000000),
	   -1 + ( 0 * 10000) + ( 0 * 1000000000),
	   -1 + ( 0 * 10000) + ( 1 * 1000000000),
	   -1 + ( 1 * 10000) + (-1 * 1000000000),
	   -1 + ( 1 * 10000) + ( 0 * 1000000000),
	   -1 + ( 1 * 10000) + ( 1 * 1000000000),
		0 + (-1 * 10000) + (-1 * 1000000000),
		0 + (-1 * 10000) + ( 0 * 1000000000),
		0 + (-1 * 10000) + ( 1 * 1000000000),
		0 + ( 0 * 10000) + (-1 * 1000000000),
		0 + ( 0 * 10000) + ( 1 * 1000000000),
		0 + ( 1 * 10000) + (-1 * 1000000000),
		0 + ( 1 * 10000) + ( 0 * 1000000000),
		0 + ( 1 * 10000) + ( 1 * 1000000000),
		1 + (-1 * 10000) + (-1 * 1000000000),
		1 + (-1 * 10000) + ( 0 * 1000000000),
		1 + (-1 * 10000) + ( 1 * 1000000000),
		1 + ( 0 * 10000) + (-1 * 1000000000),
		1 + ( 0 * 10000) + ( 0 * 1000000000),
		1 + ( 0 * 10000) + ( 1 * 1000000000),
		1 + ( 1 * 10000) + (-1 * 1000000000),
		1 + ( 1 * 10000) + ( 0 * 1000000000),
		1 + ( 1 * 10000) + ( 1 * 1000000000)
        ]

    def __init__(self, binWidth):

        self.inverseBinWidth = 1.0/binWidth
        self.hashMap = defaultdict(list)


    def add_point(self, point, pointName):

        i = np.rint(float(point[0]) * self.inverseBinWidth)
        j = np.rint(float(point[1]) * self.inverseBinWidth)
        k = np.rint(float(point[2]) * self.inverseBinWidth)
        location = i + (j*10000) + (k*1000000000)

        #print(location, pointName)

        #if location in self.hashMap:
        #    print(location)
        #    print(self.hashMap[location])
        #self.hashMap[location] = self.hashMap[location].append(pointName)

        self.hashMap[location].append(pointName)

        #else:
        #    self.hashMap[location] = [pointName]


    def get_neighbors(self, point):

        i = np.rint(float(point.x) * self.inverseBinWidth)
        j = np.rint(float(point.y) * self.inverseBinWidth)
        k = np.rint(float(point.z) * self.inverseBinWidth)
        location = i + (j*10000) + (k*1000000000)

        box = self.get_box_two(location)

        return box


    def get_box_two(self, location):

        return [self.hashMap[location + off] for off in self.offset \
                if (location + off) in self.hashMap]


    def getIntersection(self, distanceBox):

        intersection = []
        checkedLocations = set()

        for location in self.hashMap.keys():

            overlap = False

            for off in self.offset:

                loc = location + off

                if loc in distanceBox.hashMap:
                    overlap = True

                    break

            if overlap:

                for off in self.offset:

                    loc = location + off

                    if loc in checkedLocations:
                        continue

                    checkedLocations.add(loc)
                    if loc in self.hashMap:
                        intersection += self.hashMap[loc]

        return intersection
