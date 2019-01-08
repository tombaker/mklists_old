""" /Users/tbaker/github/tombaker/mklists/mklists/rules.py """

import pytest
from mklists.rules import _get_globalruleobjs_from_configfile


@pytest.mark.skip
def test_get_globalruleobjs_from_configfile(myrepo):
    """Given """
    return _get_globalruleobjs_from_configfile() == 2
