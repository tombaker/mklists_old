import pytest
from new_shuffle import shuffle
from collections import namedtuple

Rule = namedtuple('Rule', 'sourcematch_awkfield source_matchregex source target targetsort_awkfield')

def test_shuffle():
    rules_list1 = [ Rule(2, 'i', 'a.txt', 'b.txt', 0) ]
    globlines_list1 = ['two ticks\n', 'an ant\n', 'the mite\n']
    output = { 'a.txt': ['an ant\n'], 'b.txt': ['two ticks\n', 'the mite\n'] }
    assert shuffle(rules_list1, globlines_list1) == output

def test_shuffle_sort():
    rules_list1 = [ Rule(2, 'i', 'a.txt', 'b.txt', 1) ]
    globlines_list1 = ['two ticks\n', 'an ant\n', 'the mite\n']
    output = { 'a.txt': ['an ant\n'], 'b.txt': ['the mite\n', 'two ticks\n'] }
    assert shuffle(rules_list1, globlines_list1) == output
