"""Returns pathname of HTML directory composed from arguments."""

import os
import pytest
from mklists.returns import get_htmldir_path

HTMLDIR_NAME = "_html"


@pytest.mark.skip
def test_utils_return_htmldir_pathname():
    """Returns pathname of HTML directory."""
    root = "/Users/tbaker/tmp"
    htmldir = "_html"
    datadir = "agenda"
    expected = "/Users/tbaker/tmp/_html/agenda"
    assert get_htmldir_path(root=root, htmldir=htmldir, datadir=datadir) == expected


@pytest.mark.skip
def test_utils_return_htmldir_pathname_rootdir_pathname_not_given():
    """Raises exception if argument root not provided."""
    htmldir = "_html"
    datadir = "agenda"
    with pytest.raises(SystemExit):
        get_htmldir_path(root=None, htmldir=htmldir, datadir=datadir)


@pytest.mark.skip
def test_utils_return_htmldir_pathname_htmldir_name_not_given():
    """Raises exception if argument htmldir not provided."""
    root = "/Users/tbaker/tmp"
    datadir = "agenda"
    with pytest.raises(SystemExit):
        get_htmldir_path(root=root, htmldir=None, datadir=datadir)


@pytest.mark.skip
def test_utils_return_htmldir_pathname_datadir_name_not_given(tmpdir):
    """Returns pathname of HTML directory."""
    # pylint: disable=unused-variable
    # Yes, by design.
    dirname, datadir = os.path.split(os.getcwd())
    os.chdir(tmpdir)
    root = "/Users/tbaker/tmp"
    htmldir = "_html"
    expected = "/Users/tbaker/tmp/_html/" + datadir
    assert get_htmldir_path(root=root, htmldir=htmldir, datadir=datadir) == expected
