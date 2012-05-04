#!/usr/bin/env python
import os
import sys
import codecs
import textwrap
import re
from collections import defaultdict

# synopsis: <csv> <summary> <texts> <n> <outfile>

dtd = defaultdict(list)
topics = None
texts = {}

toptexts = int(sys.argv[4])

with codecs.open(sys.argv[1], 'r', encoding='utf-8') as csv:
    for line in csv:
        fields = line.strip('\n').split(',')
        if not topics:
            topics = range(len(fields)-1)
        for t in topics:
            dtd[t].append((float(fields[t+1]), str(fields[0])))


with codecs.open(sys.argv[2], 'rb', encoding='utf-8') as txt:
    summaries = txt.read().strip('\n').split('\n\n\n')

with codecs.open(sys.argv[3], 'r', encoding='utf-8') as clean:
    for line in clean:
        m = re.search(ur'^(?P<textid>[0-9]+),(?P<text>.*)$', line)
        try:
            texts[str(m.group('textid'))] = m.group('text')
        except (AttributeError):
            print 'BUG IN LINE', line

for topic,values in dtd.items():
    values.sort(reverse=True)

with codecs.open(sys.argv[5], 'wb', encoding='utf-8') as out:
    for topic,values in dtd.items():
        out.write("###################################################################################################\n")
        out.write(summaries[topic] + "\n")
        for text in values[:toptexts]:
            out.write("\n\n")
            out.write(u'=== {0}, {1} ===\n'.format(text[1], text[0]))
            try:
                out.write('\n'.join(textwrap.wrap(texts[text[1]])))
            except (KeyError):
                out.write('!!TEXT NOT FOUND!!')
        out.write("\n\n")
                

