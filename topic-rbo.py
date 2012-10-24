#!/usr/bin/env python
# -*- coding: utf-8 -*-

import argparse
import os.path
from collections import defaultdict, OrderedDict
from rbo_calc import calc_rbo

class TopicArray(object):
    def __init__(self):
        self.topics = {}
        self.keysorder = defaultdict(list)

    def getid(self, name, key):
        return ':'.join([unicode(i) for i in [name, key]])

    def add(self, name, topicdict):
        self.topics[name] = topicdict
        keys = topicdict.keys()
        keys.sort()
        for key in keys:
            self.keysorder[name].append(key)


    def iterpairs(self):
        names = self.keysorder.keys()
        names.sort()
        for nn, aname in enumerate(names):
            for bname in names[nn+1:]:
                for akey in self.keysorder[aname]:
                    for bkey in self.keysorder[bname]:
                        yield (self.getid(aname, akey), self.topics[aname][akey]), (self.getid(bname, bkey), self.topics[bname][bkey])


def get_topicdict(f):
    topicdict = defaultdict(list)
    for line in f:
        fields = line.decode('utf-8').strip('\n, ').split(',')
        word = fields[0]
        weights = [float(w) for w in fields[1:]]
        for topicnum,weight in enumerate(weights):
            if weight > 0:
                topicdict[topicnum].append((weight, unicode(word)))
    for wordlist in topicdict.itervalues():
        wordlist.sort()
    return topicdict

def run_rbo(topics, pvalue):
    for (a_id, atopic), (b_id, btopic) in topics.iterpairs():
        awords = zip(*atopic)[1]
        bwords = zip(*btopic)[1]
        print ','.join([unicode(s) for s in [calc_rbo(awords, bwords, pvalue), a_id, b_id]])

def main():
    aparser = argparse.ArgumentParser(description="Count RBO correlation for topic-term-distributions")
    aparser.add_argument("infile", nargs="*", help="Input file (topic-term-distribution.csv or document-topic-distributions.csv)")
    aparser.add_argument("-p", help="P-value (default 0.98)", default=0.98, type=float)
    args = aparser.parse_args()

    topics = TopicArray()

    for csv in args.infile:
        with open(csv) as f:
            topics.add(os.path.dirname(csv), get_topicdict(f))

    run_rbo(topics, args.p)

if __name__ == "__main__":
    main()
