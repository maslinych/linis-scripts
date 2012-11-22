#!/usr/bin/env python
# -*- coding: utf-8 -*-

# demystem.py - selects most frequent or first lemma from mystem -lcf output 

import sys
import re
import argparse

def lemselect(token, freqs=False):
    if re.match(r'^{[^}]+}$', token):
        lemmas = token.strip("{}").split("|")
        maxfreq = -1
        for l in lemmas:
            unfreq = l.split(":")
            if len(unfreq) == 1:
                freq = 0
            else:
                try:
                    freq = float(unfreq[1])
                except (ValueError):
                    return token
            if freq > maxfreq:
                maxfreq = freq
                lemma = unfreq[0]
        if freqs:
            return str(maxfreq) + " "
        else:
            return lemma.strip("?")
    else:
        if freqs:
            return "1 "
        else:
            return token



aparser = argparse.ArgumentParser(description="demystem")
aparser.add_argument("-f", "--freqs", action="store_true", help="show freqs instead of lemmas")
args = aparser.parse_args()

if __name__ == "__main__":
    for line in sys.stdin:
        for token in re.split(r'({[^}]+})', line.decode("utf-8")):
            sys.stdout.write(lemselect(token, args.freqs).encode("utf-8"))
        if args.freqs:
            sys.stdout.write("\n")
