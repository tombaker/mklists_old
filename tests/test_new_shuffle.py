import pytest
from new_shuffle import shuffle
from collections import namedtuple

Rule = namedtuple('Rule', 'srcmatch_awkf srcmatch_rgx src trg trgsort_awkf')

def test_shuffle():
    rules_l1 = [ Rule(2, 'i', 'a.txt', 'b.txt', 0) ]
    globlines_l1 = ['two ticks\n', 'an ant\n', 'the mite\n']
    output = { 'a.txt': ['an ant\n'], 'b.txt': ['two ticks\n', 'the mite\n'] }
    assert shuffle(rules_l1, globlines_l1) == output

def test_shuffle_sort():
    rules_l1 = [ Rule(2, 'i', 'a.txt', 'b.txt', 1) ]
    globlines_l1 = ['two ticks\n', 'an ant\n', 'the mite\n']
    output = { 'a.txt': ['an ant\n'], 'b.txt': ['the mite\n', 'two ticks\n'] }
    assert shuffle(rules_l1, globlines_l1) == output
