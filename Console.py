# -*- coding: utf-8 -*-
# !/usr/bin/env python
__author__ = 'Johannes Gontrum <gontrum@vogelschwarm.com>'

import sys
import Histogram
import LaTeXOutput
import Analysis
from SignatureReader import Signature, KeywordHierarchy

if len(sys.argv) != 5:
    print "Syntax: mia_result.csv signature.csv hierachy.csv [month/day]"
    sys.exit(1)

# Create Histogram.
print "Preparing data... "
histogram = None
if sys.argv[4] == 'month':
    histogram = Histogram.getMonthlyHistogram(sys.argv[1])
elif sys.argv[4] == 'day':
    histogram = Histogram.getDaylyHistogram(sys.argv[1])
else:
    print "Choose between 'month' and 'day'!"
    sys.exit(1)

# Read in the signature
keywordSignature = Signature()
keywordSignature.fromFile(sys.argv[2])

# Read in hierarchy
keywordHierarchy = KeywordHierarchy(sys.argv[3], keywordSignature)

print "Enter a command [help/exit]:"
# Console
input = None
while input != "exit":
    input = raw_input()
    if input == "help":
        print """Commands:
         help                  This help
         exit                  Leave the program
         show keywords         Show IDs of the keywords
         show subdimensions    Show IDs of the subdimensions
         show dimensions       Show IDs of the dimensions
         create general [.tex] [caption] Creates an overall histogram in the tex file.
         create [k/s/d] [.tex] [caption] [keywords/subdimensions/dimensions]"""
    if input == "show keywords" or input == "show k":
        print keywordSignature
    if input == "show subdimensions" or input == "show s":
        print keywordHierarchy.subdimensionSignature
    if input == "show dimensions" or input == "show d":
        print keywordHierarchy.dimensionSignature
    if input.startswith("create"):
        line = input.split()
        if len(line) < 4:
            print "Error: Not enough arguments given."
            continue
        mode = line[1]
        texfile = line[2]
        caption = line[3]

        # Catch general case
        if mode == "general" or mode == "g":
            histogram_data = Analysis.generalHistogram(histogram)
            if sys.argv[4] == 'month':
                LaTeXOutput.saveMonthlyHistogram(histogram_data, caption, texfile)
            else:
                LaTeXOutput.saveDaylyHistogram(histogram_data, caption, texfile)
            print "Histogram created."
            continue

        # More specific cases:
        ids = []
        for id in line[4].split(','):
            ids.append(int(id))

        # Find keywords
        keywords = []
        if mode == "k":
            keywords = ids
        if mode == "s":
            for subdimensionID in ids:
                keywords.append(keywordHierarchy.getKeywordsForSubdimension(subdimensionID))
        if mode == "d":
            for dimensionID in ids:
                keywords += list(keywordHierarchy.getKeywordsForDimension(dimensionID))

        # Processing the keywords
        print "Creating a histogram for keywords " , keywords
        histogram_data = Analysis.specificHistogram(histogram, keywords)
        if sys.argv[4] == 'month':
            LaTeXOutput.saveMonthlyHistogram(histogram_data, caption, texfile)
        else:
            LaTeXOutput.saveDaylyHistogram(histogram_data, caption, texfile)
        print "Histogram created."
        continue
