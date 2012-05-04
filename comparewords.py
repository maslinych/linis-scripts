#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
import codecs
from collections import defaultdict

topics = defaultdict(list)

with codecs.open(sys.argv[1], 'r', encoding="utf-8") as i:
    for line in i:
        fields = line.strip('\n').split(',')
        topics[fields[0]].append((fields[1], set(fields[2:])))

with codecs.open(sys.argv[2], 'w', encoding='utf-8') as o:
    for topic, words in topics.items():
        o.write(topic + ",")
        slices, slicewords = zip(*words)
        common = slicewords[0].intersection(*slicewords[1:])
        o.write(u'{0}\ncommon({0}):: {1}\n'.format(len(common), u' '.join(common)))
        for sli,wl in words:
            o.write(u'specific to {0}:: {1}\n'.format(sli, u' '.join(wl.difference(common))))





