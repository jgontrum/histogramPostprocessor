# -*- coding: utf-8 -*-
# !/usr/bin/env python
__author__ = 'Johannes Gontrum <gontrum@vogelschwarm.com>'

class Signature(object):
    def __init__(self):
        """
        Maps IDs to Objects and Objects to IDs.
        :return:
        """
        self.idToObject = {}
        self.objectToID = {}
        self.counter = 0

    def fromFile(self, filename):
        for line in open(filename, 'r'):
            id, keyword = line.split(',')
            keyword = keyword.rstrip() # remove linebreak
            self.idToObject[int(id)] = keyword
            self.objectToID[keyword] = int(id)
            self.counter = max(self.counter, int(id))

    def addObject(self, object):
        id = self.resolveObject(object)
        if id == None:
            self.idToObject[self.counter] = object
            self.objectToID[object] = self.counter
            self.counter += 1
            return self.counter - 1
        else:
            return id

    def resolveID(self, id):
        if id in self.idToObject:
            return self.idToObject[id]
        else:
            return None

    def resolveObject(self, object):
        if object in self.objectToID:
            return self.objectToID[object]
        else:
            return None

    def __str__ (self):
        ret = ""
        for i in range(self.counter):
            if i in self.idToObject:
                ret += str(i) + "\t <->  " + self.resolveID(i) + "\n"
        return ret[:-1]

class KeywordHierarchy(object):
    def __init__(self, filename, keywordSignature):
        """
        Displays the hierarchy of the keywords, as described in BMBF_Arbeitspapier_Keywords_Energiewende.pdf, pp.70
        :param filename:
        :return:
        """
        self.dimensionSignature = Signature()
        self.subdimensionSignature = Signature()

        self.dimensions = {}    # Maps a dimension to a list of subdimensions
        self.subdimensions = {} # Maps a subdimension to a list of keyword IDs

        for line in open(filename, 'r'):
            dimension, subdimension, keyword = line.split(',')

            dimensionID = self.dimensionSignature.addObject(dimension)
            subdimensionID = self.subdimensionSignature.addObject(subdimension)
            keyword = keyword.rstrip() # remove linebreak

            # Subdimension -> Keyword
            if subdimensionID in self.subdimensions:
                self.subdimensions[subdimensionID].add(keywordSignature.resolveObject(keyword))
            else:
                self.subdimensions[subdimensionID] = set([keywordSignature.resolveObject(keyword)])

            # Dimension -> Subdimensions
            if dimensionID in self.dimensions:
                self.dimensions[dimensionID].add(subdimensionID)
            else:
                self.dimensions[dimensionID] = set([subdimensionID])

    def getKeywordsForDimension(self, dimensionID):
        if dimensionID in self.dimensions:
            ret = []
            for subdimensionID in self.dimensions[dimensionID]:
                ret += self.getKeywordsForSubdimension(subdimensionID)
            return ret
        else:
            return []

    def getKeywordsForSubdimension(self, subdimensionID):
        if subdimensionID in self.subdimensions:
            return self.subdimensions[subdimensionID]
        else:
            return []
