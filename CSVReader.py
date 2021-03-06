# -*- coding: utf-8 -*-
# !/usr/bin/env python
__author__ = 'Johannes Gontrum <gontrum@vogelschwarm.com>'

import re
from operator import itemgetter
"""
Reads a CSV that is generated by request to MIA.
Returns a sorted list of triples of timestamp, publisher and bag of tuples.
"""
def readCSV(path):
    timestampPublisherDataTuples = list()
    firstline = True

    for line in open(path, 'r'):
        # Skip first line in file that describes the layout of the columns
        if firstline:
            firstline = False
            continue

        fields = line.split(";")
        # Assumption: Three columns: Publisher, Date, Bag of Tuples
        publisher = __removeQuotation(__removeEndline(fields[0]))
        timestamp = int(__removeQuotation(__removeEndline(fields[1]))) / 1000
        bag = __parseBag(__removeQuotation(__removeEndline(fields[2])))

        insert = (timestamp, publisher, bag)
        timestampPublisherDataTuples.append(insert)

    return sorted(timestampPublisherDataTuples, key=itemgetter(0))

def __removeEndline(word):
    ret = word
    if word[-1] == "\n":
        ret = ret[:-1]
    return ret

def __removeQuotation(word):
    ret = word
    if word[0] == '"':
        ret = ret[1:]
    if word[-1] == '"':
        ret = ret[0:-1]
    return ret

# Returns a list of tuples
def __parseBag(bag):
    returnList = list()
    # Remove curly brackets
    currentBag = bag[1:-1]

    # split with regex
    for item in re.split("\),\(|\(|\)", currentBag):
        if len(item) > 0:
            # item is styled like '3,5' (w/o the quotation marks)
            tupleRaw = item.split(",")
            tuple = (int(tupleRaw[0]), int(tupleRaw[1]))
            returnList.append(tuple)

    return returnList