from collections import defaultdict
import re


def apply_rules(rules_l, lines_l):

    all_d = defaultdict(list)
    initialized = False

    for rule in rules_l:

        [match_awkf, regexp, source, target, sort_awkf] = rule
        # insert ckrules() here, possibly redundantly
        match_awkf = int(match_awkf)
        sort_awkf = int(sort_awkf)

        if not initialized:
            all_d[source] = lines_l
            initialized = True

        apply_rule(match_awkf, regexp, source, target, sort_awkf, all_d)

    return all_d

def apply_rule(in_field, rgx, src, trg, sort_field, all):

    for line in all[src]:

        # skip match if in_field out of range
        if in_field > len(line.split()):
            continue

        # match against entire line if in_field exactly zero
        if in_field == 0:
            all[trg].extend([x for x in all[src] if re.search(rgx, x)])
            all[src] = [x for x in all[src] if not re.search(rgx, x)]

        # match given field if in_field greater than zero and within range
        if in_field > 0:
            y = in_field - 1
            all[trg].extend([x for x in all[src]
                             if re.search(rgx, x.split()[y])])
            all[src] = [x for x in all[src]
                        if not re.search(rgx, x.split()[y])]

        # sort target if sort_awkf greater than zero
        if sort_awkf:
            sort_ethf = sort_awkf - 1
            decorated = [(line.split()[sort_ethf], __, line)
                         for __, line in enumerate(all[trg])]
            decorated.sort()
            all[trg] = [line for ___, __, line in decorated]

    return all
