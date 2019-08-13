"""
run.py: return_ruleobj_list_from_rule_yamlfile
    Return list of rule objects from configuration and rule files.
    _rule_yamlfile_name=RULE_YAMLFILE_NAME
"""

import pytest
from mklists.rules import Rule
from mklists.run import return_ruleobj_list_from_rule_yamlfile


@pytest.mark.skip
def test_run_return_ruleobj_list_from_rule_yamlfile():
    """@@@Docstring"""
    ruleobj_list = return_ruleobj_list_from_rule_yamlfile()
    print(ruleobj_list)
    assert False
