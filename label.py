#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import argparse
import collections
import gzip
from collections import defaultdict
import textwrap

aparser = argparse.ArgumentParser(description="Label words with their topic numbers")
aparser.add_argument("clean", help="clean.txt")
aparser.add_argument("datastate", help="data state file")
aparser.add_argument("filtered", help="filtered.csv")
args = aparser.parse_args()

src = {}
with open(args.clean) as clean:
    for line in clean:
        raw = line.decode('utf-8').strip()
        tid, txt = raw[:12], raw[13:]
        src[tid] = txt

with gzip.open(args.datastate) as datastate:
    with open(args.filtered) as filtered:
        for topicline in datastate:
            topicdata = topicline.decode('utf-8').strip().split(",")
            tid, terms = filtered.readline().decode('utf-8').strip().split(",")
            topicids = collections.deque(topicdata[1:])
            usedterms = collections.deque(terms.strip().split(" "))
            dicto = defaultdict(list)
            for i, w in zip(topicids, usedterms):
                dicto[i].append(w)
            sys.stdout.write("=== {} ===\n".format(tid).encode('utf-8'))
            sys.stdout.write(' '.join(textwrap.wrap(src[tid])).encode('utf-8'))
            sys.stdout.write("\n\n")
            for it in dicto.keys():
                sys.stdout.write(u"[{0}] {1}".format(it, ' '.join(dicto[it])).encode('utf-8'))
                sys.stdout.write("\n")
            #sys.stdout.write(' '.join([u"{0}[{1}]".format(w,t) for w,t in zip(usedterms, topicids)]).encode('utf-8'))
            sys.stdout.write("\n")
