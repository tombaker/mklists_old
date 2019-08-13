"""
run.py: return_ruleobj_list_from_rule_yamlfile
    Return list of rule objects from configuration and rule files.
"""

import io
import os
import pytest
from mklists.rules import Rule
from mklists.run import return_ruleobj_list_from_rule_yamlfile
from mklists.constants import RULE_YAMLFILE_NAME

TEST_RULES_YAMLFILE_STR = r"""# Test rules for this module only.
- [0, '.',          x,         lines,            0]
- [1, 'NOW',        lines,     alines,           1]
- [1, 'LATER',      lines,     alines,           1]
- [0, '^2019|2020', lines,     blines,           1]"""


def test_run_return_ruleobj_list_from_rule_yamlfile(tmpdir):
    """@@@Docstring"""
    os.chdir(tmpdir)
    rule_yamlfile_pathname = os.path.join(tmpdir, RULE_YAMLFILE_NAME)
    io.open(rule_yamlfile_pathname, mode="w").write(TEST_RULES_YAMLFILE_STR)
    # ruleobj_list = return_ruleobj_list_from_rule_yamlfile(
    #                   _rule_yamlfile_pathname=rule_yamlfile_pathname)
    assert io.open(rule_yamlfile_pathname).read() == TEST_RULES_YAMLFILE_STR
