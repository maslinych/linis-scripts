#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import sys
import codecs
import csv
import cStringIO

class UnicodeWriter:
    """
    A CSV writer which will write rows to CSV file "f",
    which is encoded in the given encoding.
    """

    def __init__(self, f, dialect=csv.excel, encoding="utf-8", **kwds):
        # Redirect output to a queue
        self.queue = cStringIO.StringIO()
        self.writer = csv.writer(self.queue, dialect=dialect, **kwds)
        self.stream = f
        self.encoder = codecs.getincrementalencoder(encoding)()

    def writerow(self, row):
        self.writer.writerow([s.encode("utf-8") for s in row])
        # Fetch UTF-8 output from the queue ...
        data = self.queue.getvalue()
        data = data.decode("utf-8")
        # ... and reencode it into the target encoding
        data = self.encoder.encode(data)
        # write to the target stream
        self.stream.write(data)
        # empty queue
        self.queue.truncate(0)

    def writerows(self, rows):
        for row in rows:
            self.writerow(row)


# synopsis: <gcluto solution> <texts list> <outfile>

try:
    solution_file = sys.argv[1]
    txtlist = sys.argv[2]
    outfile = sys.argv[3]
except (IndexError):
    print "Usage: {0} <gcluto solution> <texts list> <outfile>".format(sys.argv[0])
    sys.exit(1)

outWriter = UnicodeWriter(open(outfile, 'wb'))

with codecs.open(solution_file, 'rb', encoding='utf-8') as sol:
    with codecs.open(txtlist, 'rb', encoding='cp1251') as txt:
        outWriter.writerows(zip([l.strip(os.linesep) for l in sol.readlines()[2:]], [l.strip(os.linesep) for l in txt.readlines()]))
