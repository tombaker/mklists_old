"""@@@Docstring"""

import os
from mklists.constants import CONFIG_YAMLFILE_NAME, RULE_YAMLFILE_NAME
from mklists.utils import get_listdir_pathnames_under_cwd


def test_get_listdir_pathnames_under_cwd(tmpdir):
    """List data directories found under project root."""
    tmpdir.join(CONFIG_YAMLFILE_NAME).write("config stuff")
    tmpdira = tmpdir.mkdir("a")
    tmpdira.join(RULE_YAMLFILE_NAME).write("some rules")
    tmpdirb = tmpdira.mkdir("b")
    tmpdirb.join(RULE_YAMLFILE_NAME).write("some more rules")
    os.chdir(tmpdir)
    expected = [os.path.join(tmpdir, "a"), os.path.join(tmpdir, "a/b")]
    assert get_listdir_pathnames_under_cwd(tmpdir) == expected
