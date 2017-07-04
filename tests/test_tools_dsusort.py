import pytest
from utilities import dsusort

def test_dsusort():
    input = ['two ticks\n', 'an ant\n', 'the mite\n']
    output = ['an ant\n', 'the mite\n', 'two ticks\n']
    assert dsusort(input, 2) == output

def test_dsusort_field_out_of_range():
    input = ['two ticks\n', 'an ant\n', 'the mite\n', 'four\n']
    output = ['four\n', 'an ant\n', 'the mite\n', 'two ticks\n']
    assert dsusort(input, 2) == output
