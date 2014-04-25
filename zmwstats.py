#!/usr/bin/env python

import sys

from functools import partial
from itertools import imap,starmap,repeat,izip,chain
from operator import itemgetter
from collections import Counter

from pbcore.io import BasH5Reader

from misc import identityFunc

if not len(sys.argv) >= 2:
    sys.exit("zmwstats.py in.bas.h5 [in2.bas.h5]\n")


readers = imap(BasH5Reader, sys.argv[1:])

get_prod = lambda o : getattr(o, "zmwMetric")("Productivity")
get_rt = lambda o : getattr(o, "zmwMetric")("ReadType")

pcg = itemgetter(0,1,2)
rtg = itemgetter(0,1,2,3,4,5,6,7)

print "\t".join(["movie_name","sequencing_zmws","all_sequencing_zmws",
                 "prod_empty", "prod_productive", "prod_other",
                 "Empty", "FullHqRead0", "FullHqRead1", "PartialHqRead0",
                 "PartialHqRead1", "PartialHqRead2", "Multiload", "Indeterminate"])
for cell in readers:
    movieName = cell.movieName
    good_zmws_cnt =  len(cell.sequencingZmws)
    all_seq_zmws_cnt = len(cell.allSequencingZmws)

    zmwgetters = imap(itemgetter,cell.allSequencingZmws)
    allSeqZmws = list(starmap(apply, izip(zmwgetters, repeat([cell]))))
    raw_prods = imap(get_prod, allSeqZmws)

    prod_counts = Counter(raw_prods)
    prod_summary = pcg(prod_counts)

    read_type = imap(get_rt, allSeqZmws)
    read_type_counts = Counter(read_type)
    read_type_summary = rtg(read_type_counts)

    outdata = [movieName, good_zmws_cnt ,all_seq_zmws_cnt]
    outdata += list(prod_summary)
    outdata += list(read_type_summary)
    print "\t".join(map(str, outdata))
    cell.close()









