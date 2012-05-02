#!/usr/bin/env python
# -*- coding: utf-8 -*-

# demystem.py - selects most frequent or first lemma from mystem -lcf output 

import sys
import re

def lemselect(token):
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
                #print '#', unfreq[0].encode("utf-8"), freq, maxfreq
                lemma = unfreq[0]
        return lemma.strip("?")
    else:
        return token

for line in sys.stdin:
    for token in re.split(r'({[^}]+})', line.decode("utf-8")):
        sys.stdout.write(lemselect(token).encode("utf-8"))

