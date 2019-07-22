"""See
/Users/tbaker/github/tombaker/mklists/mklists/utils.py
"""

import os
from mklists.initialize import RULE_YAMLFILE_NAME, CONFIG_YAMLFILE_NAME
from mklists.utils import get_rootdir_pathname, get_rulefile_chain


def test_get_rulefile_chain_basic(tmpdir):
    """List data directories found under project root."""
    tmpdir.join(CONFIG_YAMLFILE_NAME).write("config stuff")
    tmpdir.join(RULE_YAMLFILE_NAME).write("some rules")
    tmpdira = tmpdir.mkdir("a")
    tmpdira.join(RULE_YAMLFILE_NAME).write("some rules")
    tmpdirb = tmpdira.mkdir("b")
    tmpdirb.join(RULE_YAMLFILE_NAME).write("some rules")
    tmpdirc = tmpdirb.mkdir("c")
    tmpdirc.join(RULE_YAMLFILE_NAME).write("some rules")
    os.chdir(tmpdirc)
    expected = [
        os.path.join(tmpdir, ".rules"),
        os.path.join(tmpdir, "a/.rules"),
        os.path.join(tmpdir, "a/b/.rules"),
        os.path.join(tmpdir, "a/b/c/.rules"),
    ]
    assert len(
        get_rulefile_chain(currentdir_pathname=tmpdirc, rootdir_pathname=tmpdir)
    ) == len(expected)
