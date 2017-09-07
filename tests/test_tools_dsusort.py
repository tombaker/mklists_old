import pytest
from tools import dsusort

input  = [
            'two ticks\n', 
            'an ant\n', 
            'the mite\n',
            'four\n'
         ]

def test_dsusort_field_out_of_range():
    output = ['four\n', 'an ant\n', 'the mite\n', 'two ticks\n']
    assert dsusort(input, 2) == output
