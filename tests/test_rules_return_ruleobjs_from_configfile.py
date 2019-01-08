""" /Users/tbaker/github/tombaker/mklists/mklists/rules.py """

import pytest
from mklists.rules import _return_globalruleobjs_from_configfile


@pytest.mark.skip
def test_return_globalruleobjs_from_configfile(myrepo):
    """Given """
    return _return_globalruleobjs_from_configfile() == 2
