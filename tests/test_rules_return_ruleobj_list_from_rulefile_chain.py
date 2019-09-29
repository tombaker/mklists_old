"""
run.py: return_ruleobj_list_from_rulefile_chain
    Return list of rule objects from configuration and rule files.
"""

import io
import os
import pytest
from mklists.rules import Rule, return_ruleobj_list_from_rulefile_chain
from mklists.constants import RULE_YAMLFILE_NAME

TEST_RULES_YAMLFILE_STR = r"""# Test rules for this module only.
- [0, '.',          x,         lines,            0]
- [1, 'NOW',        lines,     alines,           1]
- [1, 'LATER',      lines,     alines,           1]
- [0, '^2019|2020', lines,     blines,           1]"""


@pytest.mark.skip
def test_run_return_ruleobj_list_from_rulefile_chain(tmpdir):
    """@@@Docstring"""
    os.chdir(tmpdir)
    rule_yamlfile_pathname = os.path.join(tmpdir, RULE_YAMLFILE_NAME)
    io.open(rule_yamlfile_pathname, mode="w").write(TEST_RULES_YAMLFILE_STR)
    ruleobj_list = return_ruleobj_list_from_rulefile_chain(
        _config_yamlfile=None, _rule_yamlfile_name=None, _verbose=None
    )
    assert io.open(rule_yamlfile_pathname).read() == TEST_RULES_YAMLFILE_STR
