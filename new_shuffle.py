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
    Rule = namedtuple('Rule', 'source_matchfield source_matchregex source target target_sortfield')

    source_matchfield = 0 should mean "anywhere in the (unsplit) line, as in awk"

    Expected rules should look something like this:
    [
        Rule(source_matchfield='a', source_matchregex='b', source='c', target='d', target_sortfield='e'), 
        Rule(source_matchfield='f', source_matchregex='g', source='h', target='i', target_sortfield='j')
    ]
    """

    # Initialize dictionary mklists_dict (where everything happens) with:
    # -- key: source 
    # -- value: list of lines (previously aggregated from all text files in the working directory)
    mklists_dict = defaultdict(list)
    mklists_dict[rules_list[0].source] = globlines_list

    for rule in rules_list:
        for line in rule.source:
            matchfield = rule.source_matchfield
            regex      = rule.source_matchregex
            print(matchfield)
            print(matchfield - 1)

            """
            # if matchfield out of range, then source and target remain unchanged
            if matchfield > len(line.split()):
                continue                       

            # if matchfield is zero, then regex matched to entire line
            if matchfield == 0:                
                mklists_dict[target].extend([line for line in mklists_dict[source] if re.search(regex, line)])
                mklists_dict[source] = [line for line in mklists_dict[source] if not re.search(regex, line)]

            # if matchfield is greater than zero (and within range), then regex matched to specific field
            """
            if matchfield > 0:
                print(mklists_dict[source])
                mklists_dict[target].extend([line for line in mklists_dict[source] if re.search(regex, line.split()[matchfield - 1])])
                mklists_dict[source] = [line for line in mklists_dict[source] if not re.search(regex, line.split()[matchfield - 1])]
        
        return mklists_dict

if __name__ == "__main__":
    from collections import namedtuple
    Rule = namedtuple('Rule', 'source_matchfield source_matchregex source target target_sortfield')
    globlines_list1 = [ 'two ticks\n', 'an ant\n', 'the mite\n' ]
    rules_list1 = [ Rule(2, 'i', 'a.txt', 'b.txt', 0) ]
    x = shuffle(rules_list1, globlines_list1)
    print(x)

    """
    for rule in rules:
        mklists_dict[source] = [line for line in lines if not re.search(searchkey, line)] # over-writes
        mklists_dict[target].append([line for line in lines if re.search(searchkey, line)]) # appends
        if sort_order > 0:
            mklists_dict[target] according to target_sortfield

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
