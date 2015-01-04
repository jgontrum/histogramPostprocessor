# -*- coding: utf-8 -*-
# !/usr/bin/env python
__author__ = 'Johannes Gontrum <gontrum@vogelschwarm.com>'

import CSVReader
import Datatools
import Analysis

sortedData = None

def __sort(sortedData, thresholdFunction):
    """
    Takes read in data from CSVReader.readCSV and merges it (defined by the fiven function)
    :param sortedData: output of CSVReader.readCSV
    :param thresholdFunction: Returns the next day/month/... for a given timestamp.
    :return: Sorted tuples of timestamp and a list of occurrences
    """
    mergedData = []
    currentList = []

    begin = sortedData[0][0]
    threshold = thresholdFunction(begin)

    # Sort and collect the data by month
    for timestamp, publisher, data in sortedData:
        if timestamp >= threshold:
            mergedData.append((begin, currentList))
            currentList = list()
            begin = threshold
            threshold = thresholdFunction(begin)
        currentList = Datatools.reduceLists(currentList, data)

    # Append the last month
    mergedData.append((begin, currentList))
    return mergedData

def getMonthlyHistogram(filename):
    global sortedData
    if sortedData == None:
        sortedData = CSVReader.readCSV(filename)
    return __sort(sortedData, lambda x: Datatools.getNextMonthTimestamp(x))

def getDaylyHistogram(filename):
    global sortedData
    if sortedData == None:
        sortedData = CSVReader.readCSV(filename)
    return __sort(sortedData, lambda x: Datatools.getNextDayTimestamp(x))