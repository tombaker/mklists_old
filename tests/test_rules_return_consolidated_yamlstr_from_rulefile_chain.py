"""@@@Docstring"""

import io
import pytest

from mklists.exceptions import RulefileNotFoundError
from mklists.rules import return_consolidated_yamlstr_from_rulefile_pathnames_list

#    io.open(rule_yamlfile_pathname, mode="w").write(TEST_RULES_YAMLSTR)
#    rule_yamlfile_pathname = os.path.join(tmpdir, RULE_YAMLFILE_NAME)

RULE_YAMLFILE_NAME = "mklists.yml"

TEST_RULES_YAMLSTR_A = r"""# Test rules for this module only.
- [1, 'NOW',        lines,     alines,           1]
"""  # Ensures that string ends with a '\n'.

TEST_RULES_YAMLSTR_B = r"""# Test rules for this module only.
- [1, 'LATER',      lines,     alines,           1]
"""  # Ensures that string ends with a '\n'.

TEST_RULES_YAMLSTR_C = r"""# Test rules for this module only.
- [0, '^2019|2020', lines,     blines,           1]
"""  # Ensures that string ends with a '\n'.

TEST_CONSOLIDATED_YAMLSTR = r"""# Test rules for this module only.
- [1, 'NOW',        lines,     alines,           1]
# Test rules for this module only.
- [1, 'LATER',      lines,     alines,           1]
# Test rules for this module only.
- [0, '^2019|2020', lines,     blines,           1]
"""  # Ensures that string ends with a '\n'.


@pytest.mark.skip
def test_return_consolidated_yamlstr_from_rulefile_pathnames_list(tmpdir):
    """Here: return_consolidated_yamlstr_from_rulefile_pathnames_list()
    called with _startdir_pathname as an argument."""
    tmpdira = tmpdir.mkdir("a")
    rulefilea = tmpdira.join(RULE_YAMLFILE_NAME)
    rulefilea.write(TEST_RULES_YAMLSTR_A)
    tmpdirb = tmpdira.mkdir("b")
    rulefileb = tmpdirb.join(RULE_YAMLFILE_NAME)
    rulefileb.write(TEST_RULES_YAMLSTR_B)
    tmpdirc = tmpdirb.mkdir("c")
    rulefilec = tmpdirc.join(RULE_YAMLFILE_NAME)
    rulefilec.write(TEST_RULES_YAMLSTR_C)
    expected = TEST_CONSOLIDATED_YAMLSTR
    assert (
        return_consolidated_yamlstr_from_rulefile_pathnames_list(
            [rulefilea, rulefileb, rulefilec]
        )
    ) == expected


@pytest.mark.skip
def test_return_consolidated_yamlstr_from_rulefile_pathnames_list_file_not_exist(
    tmpdir
):
    """Here: return_consolidated_yamlstr_from_rulefile_pathnames_list()
    called with _startdir_pathname as an argument."""
    tmpdira = tmpdir.mkdir("a")
    rulefilea = tmpdira.join(RULE_YAMLFILE_NAME)
    rulefilea.write(TEST_RULES_YAMLSTR_A)
    tmpdirb = tmpdira.mkdir("b")
    rulefileb = tmpdirb.join(RULE_YAMLFILE_NAME)
    rulefileb.write(TEST_RULES_YAMLSTR_B)
    tmpdirc = tmpdirb.mkdir("c")
    rulefilec = tmpdirc.join(RULE_YAMLFILE_NAME)
    rulefilec.write(TEST_RULES_YAMLSTR_C)
    with pytest.raises(RulefileNotFoundError):
        return_consolidated_yamlstr_from_rulefile_pathnames_list(
            [rulefilea, rulefileb, rulefilec, "rulefiled"]
        )
