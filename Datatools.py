# -*- coding: utf-8 -*-
# !/usr/bin/env python
__author__ = 'Johannes Gontrum <gontrum@vogelschwarm.com>'

from operator import itemgetter
import IntervalFinder
import pytz
from datetime import datetime,timedelta
import calendar

deTimezone = pytz.timezone("Europe/Berlin")

"""
Let list1 and list2 be two lists of tuples. This reduce function
will merge the list by summing up the second values of the tuples.
"""
def reduceLists(list1, list2):
    returnList = list()
    mergedList = sorted(list1 + list2, key=itemgetter(0))

    index = 0

    while index < len(mergedList):
        endIndex = IntervalFinder.getEndOfCurrentInterval(mergedList, index)

        sum = 0
        key = mergedList[index][0]
        for i in range(index, endIndex):
            sum += mergedList[i][1]

        returnList.append((key, sum))

        index = endIndex

    return returnList

def sumTupleList(tupleList):
    ret = 0
    for key, value in tupleList:
        ret += value
    return value

"""
Takes the UNIX timestamp of the current day and returns
the timestamp of the next day at 0:00 o'clock.
"""
def getNextDayTimestamp(currentday):
    dt = getGermanTimestamp(currentday)
    midnight = dt.replace(hour=0, minute=0, second=0, microsecond=0)
    tomorrow = midnight + timedelta(days=1)
    # Convert it to a timestamp and back again to avoid problems with DST
    ts = calendar.timegm(tomorrow.timetuple())
    nextday = getGermanTimestamp(ts).replace(hour=0)
    return calendar.timegm(nextday.utctimetuple())


"""
Like getNextDayTimestamp, but returns the timestamp of
the first day of the next month at 0:00 o'clock.
"""
def getNextMonthTimestamp(currentmonth):
    dt = getGermanTimestamp(currentmonth)
    midnight = dt.replace(hour=0, minute=0, second=0, microsecond=0)
    nextday = midnight.replace(day=calendar.monthrange(midnight.year, midnight.month)[1]).astimezone(deTimezone) + timedelta(days=1)
    # Convert it to a timestamp and back again to avoid problems with DST
    ts = calendar.timegm(nextday.timetuple())
    nextday = getGermanTimestamp(ts).replace(hour=0)
    return calendar.timegm(nextday.utctimetuple())

""" Returns a datetime object fromt a UNIX timestamp that is interpreted in the right timezone """
def getGermanTimestamp(timestamp):
    return datetime.fromtimestamp(timestamp, tz=deTimezone)