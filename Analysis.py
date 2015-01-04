# -*- coding: utf-8 -*-
# !/usr/bin/env python
__author__ = 'Johannes Gontrum <gontrum@vogelschwarm.com>'

import Datatools

def generalHistogram(data):
    """
    Creates a histogram for all words.
    :param data: Sorted tuples of timestamp and a list of occurrences
    :return: List of tuples of timestamp and count
    """
    ret = []
    for time, lst in data:
        ret.append((time, Datatools.sumTupleList(lst)))
    return ret


def specificHistogram(data, words):
    """
    Creates a histogram for given words.
    :param data: Sorted tuples of timestamp and a list of occurrences
    :param words: Collection of word ids to track
    :return: List of tuples of timestamp and count
    """
    ret = []
    for time, lst in data:
        score = 0
        for key, value in lst:
            if key in words:
                score += value
        ret.append((time, score))
    return ret