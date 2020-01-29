"""Return list of rule objects from rulefile chain from rootdir to current dir."""

import pytest
from mklists.rules import return_ruleobj_list_from_rulefiles


@pytest.mark.skip
def test_return_ruleobj_list_from_rulefiles():
    """@@@Docstring"""
    print(type(return_ruleobj_list_from_rulefiles))
    assert False
