import pytest
from new_shuffle import shuffle
from collections import namedtuple

Rule = namedtuple('Rule', 'matchfield_int matchfield_regex sourcename_key targetname_key targetsort_int')

globlines_list1 = [
       'two ticks\n', 
       'an ant\n', 
       'the mite\n'
    ]

rules_list1 = [
        Rule(2, 'i', 'a.txt', 'b.txt', 0)
    ]

def test_shuffle():
    output = {
            'a.txt': ['an ant\n'],
            'b.txt': ['the mite\n', 'two ticks\n']
        }
    assert shuffle(rules_list1, globlines_list1) == output
