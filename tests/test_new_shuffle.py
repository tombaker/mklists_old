import pytest
from new_shuffle import shuffle
from collections import namedtuple

Rule = namedtuple('Rule', 'source_matchfield source_matchregex source target target_sortfield')

globlines_list1 = [ 'two ticks\n', 'an ant\n', 'the mite\n' ]

rules_list1 = [ Rule(2, 'i', 'a.txt', 'b.txt', 0) ]

print(rules_list1)

def test_shuffle():
    output = {
            'a.txt': ['an ant\n'],
            'b.txt': ['two ticks\n', 'the mite\n']
        }
    assert shuffle(rules_list1, globlines_list1) == output
