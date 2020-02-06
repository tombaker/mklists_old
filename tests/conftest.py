"""@@@Docstring"""

import pytest
from pathlib import Path
from mklists.ruleclass import Rule
from mklists.constants import (
    CONFIGFILE_NAME,
    ROOTDIR_RULEFILE_NAME,
    DATADIR_RULEFILE_NAME,
)


@pytest.fixture()
def reinitialize_ruleclass_variables():
    """Class variables must be re-initialized:
        for each test of Rule.isrule
        for each test of x._source_filename_field_was_properly_initialized
        for each test of Rule.sources_list"""
    Rule.sources_list = []
    Rule.sources_list_is_initialized = False


@pytest.fixture(name="tmppath")
def fixture_tmpath():
    """Returns an instance of pathlib.Path because as of 2020,
    the 'py' library, with 'py.path' (and 'py.path.local') appear
    still to be in maintenance mode.

    https://py.readthedocs.io/en/latest/path.html"""


@pytest.fixture(name="myrepo")
def fixture_myrepo(tmp_path_factory):
    """Return temporary mklists repo 'myrepo'."""
    # pylint: disable=unused-variable
    # Not a problem; this is just a fixture.
    root_dir = tmp_path_factory.mktemp("myrepo")
    Path(root_dir).joinpath(CONFIGFILE_NAME).write_text("config stuff")
    Path(root_dir).joinpath(ROOTDIR_RULEFILE_NAME).write_text("rule stuff")
    Path(root_dir).joinpath("a/b/c").mkdir(parents=True, exist_ok=True)
    Path(root_dir).joinpath("a", DATADIR_RULEFILE_NAME).write_text("rule stuff")
    return root_dir
