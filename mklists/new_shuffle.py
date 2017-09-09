from collections import defaultdict
import glob
import os
import re

def shuffle(rules_l, globlines_l):
    """Rule = namedtuple('Rule', 'srcmatch_awkf srcmatch_rgx src trg trgsort_awkf')"""

    # Initialize dictionary mkl_d (where everything happens) with:
    # -- key: rule.source
    # -- value: globlines_l, an aggregated list of lines from all text files in working directory
    mkl_d = defaultdict(list)
    mkl_d[rules_l[0].src] = globlines_l

    for rule in rules_l:
        for ln in mkl_d[rule.src]:
            awkf    = rule.srcmatch_awkf
            ethf    = rule.srcmatch_awkf - 1
            rgx     = rule.srcmatch_rgx
            trg     = rule.trg
            src     = rule.src

            # if awkf out of range, then src and trg remain unchanged
            # in srcmatch_awkf, zero means "match against entire line"
            if awkf > len(ln.split()):
                continue                       

            # if awkf is zero, then regex matched against entire line
            if awkf == 0:                
                mkl_d[trg].extend([ln for ln in mkl_d[src] if re.search(rgx, ln)])
                mkl_d[src] = [ln for ln in mkl_d[src] if not re.search(rgx, ln)]

            # if awkf greater than zero (and within range), regex matched against specific field
            if awkf > 0:
                mkl_d[trg].extend([ln for ln in mkl_d[src] if re.search(rgx, ln.split()[ethf])])
                mkl_d[src] = [ln for ln in mkl_d[src] if not re.search(rgx, ln.split()[ethf])]

            # sort mkl_d[trg], dsu-style, if trgsort_awkf greater than zero (note: zero is false)
            # in trgsort_awkf, zero means "no sort order specified"
            if rule.trgsort_awkf:
                eth_sortkey = rule.trgsort_awkf - 1
                decorated = [(ln.split()[eth_sortkey], i, ln) for i, ln in enumerate(mkl_d[trg])]
                decorated.sort()
                mkl_d[trg] = [ln for grade, i, ln in decorated]
        
    return mkl_d

