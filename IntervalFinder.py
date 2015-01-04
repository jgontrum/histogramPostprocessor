# -*- coding: utf-8 -*-
# !/usr/bin/env python
__author__ = 'Johannes Gontrum <gontrum@vogelschwarm.com>'

"""
TODO: docu
Returns a tuple of the first index and the last index in data.
"""
def getIntervalByTimestamp(data, begin, end):
    beginIndex = -1
    endIndex = -1

    for i in range(len(data)):
        timestamp = data[i][0]

        # still looking for the start index
        if beginIndex < 0:
            if timestamp >= begin:
                beginIndex = i
        # start index found, now searching the end index
        else:
            if timestamp >= end:
                endIndex = i
                return (beginIndex, endIndex)

    # No end index found: Set it to last index
    endIndex = len(data) - 1
    return (beginIndex, endIndex)



def getEndOfCurrentInterval(data, index):
    key = data[index][0]

    for i in range(index, len(data)):
        if data[i][0] != key:
            return i

    return len(data)




