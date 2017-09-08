from collections import defaultdict
import glob
import os
import re

def shuffle(rules_list, globlines_list):
    """Rule = namedtuple('Rule', 'sourcematch_awkfield source_matchregex source target targetsort_awkfield')"""

    # Initialize dictionary mklists_dict (where everything happens) with:
    # -- key: source 
    # -- value: list of lines (previously aggregated from all text files in the working directory)
    mklists_dict = defaultdict(list)
    mklists_dict[rules_list[0].source] = globlines_list

    for rule in rules_list:
        for line in mklists_dict[rule.source]:
            awkfield    = rule.sourcematch_awkfield
            ethfield    = rule.sourcematch_awkfield - 1
            regex       = rule.source_matchregex
            target      = rule.target
            source      = rule.source
            eth_sortkey = rule.targetsort_awkfield - 1

            # if awkfield out of range, then source and target remain unchanged
            if awkfield > len(line.split()):
                continue                       

            # if awkfield is zero, then regex matched against entire line
            if awkfield == 0:                
                mklists_dict[target].extend([line for line in mklists_dict[source] if re.search(regex, line)])
                mklists_dict[source] = [line for line in mklists_dict[source] if not re.search(regex, line)]

            # if awkfield is greater than zero (and within range), then regex matched against specific field
            if awkfield > 0:
                mklists_dict[target].extend([line for line in mklists_dict[source] if re.search(regex, line.split()[ethfield])])
                mklists_dict[source] = [line for line in mklists_dict[source] if not re.search(regex, line.split()[ethfield])]
        
    return mklists_dict

if __name__ == "__main__":
    from collections import namedtuple
    Rule = namedtuple('Rule', 'sourcematch_awkfield source_matchregex source target targetsort_awkfield')
    globlines_list1 = [ 'two ticks\n', 'an ant\n', 'the mite\n' ]
    rules_list1 = [ Rule(2, 'i', 'a.txt', 'b.txt', 0) ]
    x = shuffle(rules_list1, globlines_list1)
    print(x)

    """
        if sort_order > 0:
            mklists_dict[target] according to targetsort_awkfield
    """
