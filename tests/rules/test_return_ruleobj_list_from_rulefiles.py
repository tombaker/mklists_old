"""Return list of rule objects from rule files."""

import os
import pytest
from pathlib import Path
from mklists.rules import (
    return_ruleobj_list_from_rulefiles,
    _return_listrules_from_rulefile_list,
    _return_rulefile_chain,
)
from mklists.ruleclass import Rule
from mklists.exceptions import NoRulefileError
from mklists.constants import (
    CONFIGFILE_NAME,
    DATADIR_RULEFILE_NAME,
    ROOTDIR_RULEFILE_NAME,
)

# pylint: disable=unused-argument
# In tests, fixture arguments may look like they are unused.

ROOTDIR_RULESTR = "0|.|x|lines|0|A comment\n"
DIRA_RULESTR = "1|NOW|lines|alines|1|Another comment\n" "1|LATER|lines|alines|1|\n"
DIRB_RULESTR = "0|^2019 ..|lines|blines|1|\n"
RULEOBJ_LIST = [
    Rule(
        source_matchfield=0,
        source_matchpattern=".",
        source="x",
        target="lines",
        target_sortorder=0,
    ),
    Rule(
        source_matchfield=1,
        source_matchpattern="NOW",
        source="lines",
        target="alines",
        target_sortorder=1,
    ),
    Rule(
        source_matchfield=1,
        source_matchpattern="LATER",
        source="lines",
        target="alines",
        target_sortorder=1,
    ),
    Rule(
        source_matchfield=0,
        source_matchpattern="^2019 ..",
        source="lines",
        target="blines",
        target_sortorder=1,
    ),
]


@pytest.mark.skip
@pytest.mark.rules
def test_return_ruleobj_list_from_rulefiles(tmp_path):
    """@@@Docstring."""
    os.chdir(tmp_path)
    Path(tmp_path).joinpath(CONFIGFILE_NAME).write_text("config stuff")
    rulefile0 = Path(tmp_path).joinpath(ROOTDIR_RULEFILE_NAME)
    rulefile0.write_text(ROOTDIR_RULESTR)
    ab = Path(tmp_path).joinpath("a/b")
    ab.mkdir(parents=True, exist_ok=True)
    rulefile1 = Path(tmp_path).joinpath("a", DATADIR_RULEFILE_NAME)
    rulefile1.write_text(DIRA_RULESTR)
    rulefile2 = Path(tmp_path).joinpath("a/b", DATADIR_RULEFILE_NAME)
    rulefile2.write_text(DIRB_RULESTR)
    os.chdir(ab)
    rulefile_chain = _return_rulefile_chain()
    assert rulefile_chain == [rulefile0, rulefile1, rulefile2]
    expected = RULEOBJ_LIST
    real = return_ruleobj_list_from_rulefiles()
    assert real == expected


@pytest.mark.skip
@pytest.mark.rules
def test_return_listrules_from_rulefile_list_rulefile_not_specified(tmp_path):
    """@@@Docstring."""
    with pytest.raises(NoRulefileError):
        _return_listrules_from_rulefile_list(csvfile=None)


# PYOBJ_JUST_STRINGS = [
#     ["0", ".", "x", "lines", "0"],
#     ["1", "NOW", "lines", "alines", "1"],
#     ["1", "LATER", "lines", "alines", "1"],
#     ["0", "^2019 ..", "lines", "blines", "1"],
# ]
#
#
# PYOBJ_WITH_INTEGERS = [
#     [0, ".", "x", "lines", 0],
#     [1, "NOW", "lines", "alines", 1],
#     [1, "LATER", "lines", "alines", 1],
#     [0, "^2020", "lines", "blines", 1],
# ]
