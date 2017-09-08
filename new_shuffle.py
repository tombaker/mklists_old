from collections import defaultdict
import glob
import os
import re

def get_globlines_list(cwd=os.getcwd()):
    """Something like:
    globlines_list = []
    for file in glob.glob('*'):
        globlines_list.append(file.readlines())
    return globlines_list
    """
    pass

def shuffle(rules_list, globlines_list):
    """
    Rule = namedtuple('Rule', 'sourcematch_awkfield source_matchregex source target targetsort_awkfield')

    sourcematch_awkfield = 0 should mean "anywhere in the (unsplit) line, as in awk"

    Expected rules should look something like this:
    [
        Rule(sourcematch_awkfield='a', source_matchregex='b', source='c', target='d', targetsort_awkfield='e'), 
        Rule(sourcematch_awkfield='f', source_matchregex='g', source='h', target='i', targetsort_awkfield='j')
    ]
    """

    # Initialize dictionary mklists_dict (where everything happens) with:
    # -- key: source 
    # -- value: list of lines (previously aggregated from all text files in the working directory)
    mklists_dict = defaultdict(list)
    mklists_dict[rules_list[0].source] = globlines_list
    ### print('mklists_dict is {}'.format(mklists_dict))

    for rule in rules_list:
        print(rule)
        ### print('mklists_dict[rule.source] is {}'.format(mklists_dict[rule.source]))
        for line in mklists_dict[rule.source]:
            awkfield = rule.sourcematch_awkfield
            ethfield = rule.sourcematch_awkfield - 1
            regex    = rule.source_matchregex
            target   = rule.target
            source   = rule.source
            ### print('awkfield is {}'.format(awkfield))
            ### print('ethfield is {}'.format(ethfield))

            # if awkfield out of range, then source and target remain unchanged
            if awkfield > len(line.split()):
                ### print('line is {}'.format(line))
                ### print('length of line is {}'.format(len(line.split())))
                ### print('awkfield is greater than field length of line')
                continue                       

            # if awkfield is zero, then regex matched to entire line
            if awkfield == 0:                
                ### print('awkfield is zero')
                mklists_dict[target].extend([line for line in mklists_dict[source] if re.search(regex, line)])
                mklists_dict[source] = [line for line in mklists_dict[source] if not re.search(regex, line)]

            # if awkfield is greater than zero (and within range), then regex matched to specific field
            if awkfield > 0:
                ### print('awkfield is greater than zero')
                ### print('mklists_dict is {}'.format(mklists_dict))
                ### print('mklists_dict[target] is {}'.format(mklists_dict[target])
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
    for rule in rules:
        mklists_dict[source] = [line for line in lines if not re.search(searchkey, line)] # over-writes
        mklists_dict[target].append([line for line in lines if re.search(searchkey, line)]) # appends
        if sort_order > 0:
            mklists_dict[target] according to targetsort_awkfield

    So why does this use append() - we want extend(), right?
    >>> x = [1, 2, 3, 4]
    >>> x.extend([5, 6, 7, 8])
    >>> x
    [1, 2, 3, 4, 5, 6, 7, 8]

    >>> x = [1, 2, 3, 4]
    >>> x.append([5, 6, 7, 8])
    >>> x
    [1, 2, 3, 4, [5, 6, 7, 8]]
    """
