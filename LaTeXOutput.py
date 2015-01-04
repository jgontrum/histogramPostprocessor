# -*- coding: utf-8 -*-
# !/usr/bin/env python
__author__ = 'Johannes Gontrum <gontrum@vogelschwarm.com>'

import Datatools

def saveMonthlyHistogram(data, caption, file):
    __saveHistogram(data,caption,file, "%F")

def saveDaylyHistogram (data, caption, file):
    __saveHistogram(data, caption, file, "%F")

def __saveHistogram(data, caption, file, xcaption):
    outfile = open(file, 'w')

    static = """\\documentclass[11pt]{{article}}
\\usepackage[T1]{{fontenc}}
\\usepackage{{pgfplots}}
\\usetikzlibrary{{pgfplots.dateplot}}
\\usepgfplotslibrary{{dateplot}}
\\pgfplotsset{{compat=newest}}

\\begin{{document}}
    \\begin{{figure}}
        \\begin{{center}}
            \\begin{{tikzpicture}}
                \\begin{{axis}}[
                    width=0.9\\columnwidth,
                    height=0.3\\textheight,
                    date coordinates in=x,
                    xticklabel style= {{rotate=90,anchor=near xticklabel}},
                    xticklabel=\\day.\\month.\\year,
                    scaled x ticks=true
                    ]

                    \\addplot[ybar] coordinates {{
{0}
                    }};
                \\end{{axis}}
            \\end{{tikzpicture}}
        \\end{{center}}
        \\caption{{{1}}}
    \\end{{figure}}
\\end{{document}}"""


    # Data
    formatedData = ""
    for month, value in data:
        formatedData += "                        (" + str(Datatools.getGermanTimestamp(month).strftime(xcaption)) + "," + str(value) + ")\n"
    # Last static part
    outfile.write(static.format(formatedData, caption))