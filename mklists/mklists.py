from collections import defaultdict
import re


def apply_rules(rules_l, lines_l):
    """\
    Input:
    -- rules_l: list of five-item rules
    -- lines_l: list of lines from all text files in working directory
    
    Initializes result with 'source' name as per rules_l, line 1, field 3
    -- key: rules_l[0][2]
    -- value: lines from all text files in working directory

    Returns:
    -- result_d
    """

    result_d = defaultdict(list)
    initialized = False

    for rule in rules_l:

        [match_awkfield, rgx, source, target, sort_awkfield] = rule
        match_awkfield = int(match_awkfield)
        sort_awkfield = int(sort_awkfield)

        if not initialized:
            result_d[source] = lines_l
            initialized = True

        for line in result_d[source]:

            # if match_awkfield out of range, source and target unchanged
            if match_awkfield > len(line.split()):
                continue

            # if match_awkfield is exactly zero, match against entire line
            if match_awkfield == 0:
                result_d[target].extend([x for x in result_d[source]
                                         if re.search(rgx, x)])
                result_d[source] =      [x for x in result_d[source]
                                         if not re.search(rgx, x)]

            # if match_awkfield greater than zero and within range, match it
            if match_awkfield > 0:
                y = match_awkfield - 1
                result_d[target].extend([x for x in result_d[source]
                                         if re.search(rgx, x.split()[y])])
                result_d[source] =      [x for x in result_d[source]
                                         if not re.search(rgx, x.split()[y])]

            # if sort_awkfield greater than zero, sort target dsu-style
            if sort_awkfield:
                sort_ethfield = sort_awkfield - 1
                decorated = [(line.split()[sort_ethfield], __, line)
                             for __, line in enumerate(result_d[target])]
                decorated.sort()
                result_d[target] = [line for ___, __, line in decorated]

    return result_d
