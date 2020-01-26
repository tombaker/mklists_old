"""Returns pathname of HTML directory composed from arguments."""

import os
import pytest
from mklists.utils import return_htmldir_pathname

HTMLDIR_NAME = ".html"


@pytest.mark.skip
def test_utils_return_htmldir_pathname():
    """Returns pathname of HTML directory."""
    rootdir_pathname = "/Users/tbaker/tmp"
    htmldir_name = ".html"
    datadir_name = "agenda"
    expected = "/Users/tbaker/tmp/.html/agenda"
    assert (
        return_htmldir_pathname(
            rootdir_pathname=rootdir_pathname,
            htmldir_name=htmldir_name,
            datadir_name=datadir_name,
        )
        == expected
    )


@pytest.mark.skip
def test_utils_return_htmldir_pathname_rootdir_pathname_not_given():
    """Raises exception if argument rootdir_pathname not provided."""
    htmldir_name = ".html"
    datadir_name = "agenda"
    with pytest.raises(SystemExit):
        return_htmldir_pathname(
            rootdir_pathname=None, htmldir_name=htmldir_name, datadir_name=datadir_name
        )


@pytest.mark.skip
def test_utils_return_htmldir_pathname_htmldir_name_not_given():
    """Raises exception if argument htmldir_name not provided."""
    rootdir_pathname = "/Users/tbaker/tmp"
    datadir_name = "agenda"
    with pytest.raises(SystemExit):
        return_htmldir_pathname(
            rootdir_pathname=rootdir_pathname,
            htmldir_name=None,
            datadir_name=datadir_name,
        )


@pytest.mark.skip
def test_utils_return_htmldir_pathname_datadir_name_not_given(tmpdir):
    """Returns pathname of HTML directory."""
    # pylint: disable=unused-variable
    # Yes, by design.
    dirname, datadir_name = os.path.split(os.getcwd())
    os.chdir(tmpdir)
    rootdir_pathname = "/Users/tbaker/tmp"
    htmldir_name = ".html"
    expected = "/Users/tbaker/tmp/.html/" + datadir_name
    assert (
        return_htmldir_pathname(
            rootdir_pathname=rootdir_pathname,
            htmldir_name=htmldir_name,
            datadir_name=datadir_name,
        )
        == expected
    )
