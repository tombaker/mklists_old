"""Returns pathname of backup directory, composed from info provided in arguments.

Edit /Users/tbaker/github/tombaker/mklists/mklists/utils.py
"""

import pytest
from mklists.config import Defaults


@pytest.mark.skip
def test_backups_return_backupdir_pathname():
    """Returns pathname of backup directory where
    all needed info is provided in arguments.

    Args:
        _rootdir_pathname:
        _backupdir_name:
        _backupdir_shortname:
        _timestamp_str:

    """
    rootdir_pathname = "/Users/tbaker/tmp"
    backupdir_name = ".backups"
    backupdir_shortname = "agenda"
    timestamp_str = "2019-01-03_1646_06488910"
    expected = "/Users/tbaker/tmp/.backups/agenda/2019-01-03_1646_06488910"
    assert (
        Defaults.return_backupdir_pathname(
            rootdir_pathname=rootdir_pathname,
            backupdir_name=backupdir_name,
            backupdir_shortname=backupdir_shortname,
            timestamp_str=timestamp_str,
        )
        == expected
    )
