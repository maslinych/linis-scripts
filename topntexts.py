#!/usr/bin/env python
import os
import sys
import codecs
from collections import defaultdict

# synopsis: <csv> <summary> <texts dir> <n> <outfile>

dtd = defaultdict(list)
topics = None

with codecs.open(sys.argv[1], encoding='utf-8') as csv:
    for line in csv:
        fields = line.split(',')
        if not topics:
            topics = range(len(fields)-1)
        for t in topics:
            dtd[t].append((float(fields[t+1]), fields[0]))

for topic,values in dtd.items():
    values.sort(reverse=True)

with codecs.open(sys.argv[2], 'rb', encoding='utf-8') as txt:
    summaries = txt.read().strip('\n').split('\n\n\n')

#with codecs.open
for topic,values in dtd.items():
    print "\n\n"
    print "###################################################################################################"
    print summaries[topic]
    for text in values[:int(sys.argv[4])]:
        print "\n"
        print '===', text[1], text[0], '==='
        with codecs.open(os.path.join(sys.argv[3], text[1]), 'rb', encoding='utf-8') as tf:
            print tf.read()
            

