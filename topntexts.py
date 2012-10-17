#!/usr/bin/env python
import os
import codecs
import textwrap
import re
import argparse
from collections import defaultdict

# synopsis: <csv> <summary> <texts> <n> <outfile>
aparser = argparse.ArgumentParser(description='Print top N texts for each topic based on LDA results')
aparser.add_argument('csv', help='Main LDA results file (document-topics-distribution.csv)')
aparser.add_argument('summary', help='File with topic top-words (summary.txt)')
aparser.add_argument('texts', help='File with source texts suitable for reading (clean.txt)')
aparser.add_argument('n', type=int, help='Number of top texts to print for each topic')
aparser.add_argument('outfile', help='Output file')
args = aparser.parse_args()


dtd = defaultdict(list)
topics = None
texts = {}

with codecs.open(args.csv, 'r', encoding='utf-8') as csv:
    for line in csv:
        fields = line.strip('\n').split(',')
        if not topics:
            topics = range(len(fields)-1)
        for t in topics:
            dtd[t].append((float(fields[t+1]), str(fields[0])))


with codecs.open(args.summary, 'rb', encoding='utf-8') as txt:
    summaries = txt.read().strip('\n').split('\n\n\n')

with codecs.open(args.texts, 'r', encoding='utf-8') as clean:
    for line in clean:
        m = re.search(ur'^(?P<textid>[0-9]+),(?P<text>.*)$', line)
        try:
            texts[str(m.group('textid'))] = m.group('text')
        except (AttributeError):
            print 'BUG IN LINE', line

for topic,values in dtd.items():
    values.sort(reverse=True)

with codecs.open(args.outfile, 'wb', encoding='utf-8') as out:
    for topic,values in dtd.items():
        out.write("###################################################################################################\n")
        out.write(summaries[topic] + "\n")
        for text in values[:args.n]:
            out.write("\n\n")
            out.write(u'=== {0}, {1} ===\n'.format(text[1], text[0]))
            try:
                out.write('\n'.join(textwrap.wrap(texts[text[1]])))
            except (KeyError):
                out.write('!!TEXT NOT FOUND!!')
        out.write("\n\n")
                

