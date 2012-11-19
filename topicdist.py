#!/usr/bin/env python
# -*- coding: utf-8 -*-

import argparse
import os.path
from collections import defaultdict, OrderedDict
from rbo_calc import calc_rbo


class Topic(object):
    def __init__(self):
        self._tuples = []
        self._sorted = False

    def sort(self):
        if not self._sorted:
            self._tuples.sort()
        self._sorted = True

    @property
    def words(self):
        self.sort()
        return zip(*self._tuples)[1]

    @property
    def weghts(self):
        self.sort()
        return zip(*self._tuples)[0]

    def append(self, weight, word):
        self._tuples.append((weight, word))

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
                for an, akey in enumerate(self.keysorder[aname]):
                    for bkey in self.keysorder[bname][an+1:]:
                        yield (self.getid(aname, akey), self.topics[aname][akey]), (self.getid(bname, bkey), self.topics[bname][bkey])


def get_topicdict(f):
    topicdict = defaultdict(Topic)
    for line in f:
        fields = line.decode('utf-8').strip('\n, ').split(',')
        word = fields[0]
        weights = [float(w) for w in fields[1:]]
        for topicnum,weight in enumerate(weights):
            if weight > 0:
                topicdict[topicnum].append(weight, unicode(word))
    return topicdict

def run_rbo(atopic, btopic, pvalue):
    return calc_rbo(atopic.words, btopic.words, pvalue)
    print ','.join([unicode(s) for s in [calc_rbo(awords, bwords, pvalue), a_id, b_id]])

def run_bow(atopic, btopic, parameter=None):
    aset = set(atopic.words)
    bset = set(btopic.words)
    return len(aset.intersection(bset))/float(len(aset.union(bset)))

DISTANCE_FUNCTIONS = {
        None: lambda a,b,p: -1,
        'rbo': run_rbo,
        'bow': run_bow
        }

def run_distance_function(function, topics, parameter, onlybest=False):
    maxdist = 0
    current = None
    besttopic = None
    for (a_id, atopic), (b_id, btopic) in topics.iterpairs():
        distance = DISTANCE_FUNCTIONS[function](atopic, btopic, parameter)
        if onlybest:
            if current is None:
                current = a_id
            elif current == a_id:
                if maxdist < distance:
                    maxdist = distance
                    besttopic = b_id
                continue
            else:
                print ','.join([unicode(s) for s in [maxdist, current, besttopic]])
                current = a_id
                maxdist = 0
                besttopic = None
        else:
            print ','.join([unicode(s) for s in [distance, a_id, b_id]])

def main():
    aparser = argparse.ArgumentParser(description="Run simmetric likelihood measures for given topics pairwise")
    aparser.add_argument("infile", nargs="*", help="Input file (topic-term-distribution.csv or document-topic-distributions.csv)")
    aparser.add_argument("-f", "--function", choices=DISTANCE_FUNCTIONS, default=None)
    aparser.add_argument("-p", help="Persistence value for RBO (default 0.98)", default=0.98, type=float)
    aparser.add_argument("-b", "--best", help="Show only best match (maximum likelihood)", action='store_true')
    args = aparser.parse_args()

    topics = TopicArray()

    for csv in args.infile:
        with open(csv) as f:
            topics.add(os.path.dirname(csv), get_topicdict(f))

    run_distance_function(args.function, topics, parameter=args.p, onlybest=args.best)

if __name__ == "__main__":
    main()
