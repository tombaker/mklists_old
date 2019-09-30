"""@@@Docstring"""

import io
import pytest
from mklists.constants import RULE_YAMLFILE_NAME
from mklists.rules import return_rulestring_list_from_rulefile_chain

#    io.open(rule_yamlfile_pathname, mode="w").write(TEST_RULES_YAMLFILE_STR)
#    rule_yamlfile_pathname = os.path.join(tmpdir, RULE_YAMLFILE_NAME)

TEST_RULES_YAMLFILE_STR_A = r"""# Test rules for this module only.
- [1, 'NOW',        lines,     alines,           1]"""

TEST_RULES_YAMLFILE_STR_B = r"""# Test rules for this module only.
- [1, 'LATER',      lines,     alines,           1]"""

TEST_RULES_YAMLFILE_STR_C = r"""# Test rules for this module only.
- [0, '^2019|2020', lines,     blines,           1]"""

TEST_RULES_YAMLFILE_SPLIT = [
    [0, ".", "x", "lines", 0],
    [1, "NOW", "lines", "alines", 1],
    [1, "LATER", "lines", "alines", 1],
    [0, "^2019|2020", "lines", "blines", 1],
]


@pytest.mark.now
def test_return_rulestring_list_from_rulefile_chain(tmpdir):
    """Here: return_rulestring_list_from_rulefile_chain()
    called with _startdir_pathname as an argument."""
    tmpdira = tmpdir.mkdir("a")
    rulefilea = tmpdira.join(RULE_YAMLFILE_NAME)
    rulefilea.write(TEST_RULES_YAMLFILE_STR_A)
    tmpdirb = tmpdira.mkdir("b")
    rulefileb = tmpdirb.join(RULE_YAMLFILE_NAME)
    rulefileb.write(TEST_RULES_YAMLFILE_STR_B)
    tmpdirc = tmpdirb.mkdir("c")
    rulefilec = tmpdirc.join(RULE_YAMLFILE_NAME)
    rulefilec.write(TEST_RULES_YAMLFILE_STR_C)
    expected = TEST_RULES_YAMLFILE_SPLIT
    assert (
        return_rulestring_list_from_rulefile_chain([rulefilea, rulefileb, rulefilec])
    ) == expected
