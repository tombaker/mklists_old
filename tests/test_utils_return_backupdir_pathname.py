"""Returns pathname of backup directory, composed from info provided in arguments.

Edit /Users/tbaker/github/tombaker/mklists/mklists/utils.py
"""

from mklists.config import return_backupdir_pathname


def test_backups_return_backupdir_pathname():
    """Returns pathname of backup directory where
    all needed info is provided in arguments.

    Args:
        _rootdir_pathname:
        _backupdir_subdir_name:
        _backupdir_shortname:
        _timestamp_str:

    """
    rootdir_pathname = "/Users/tbaker/tmp"
    backupdir_name = ".backups"
    backupdir_subdir_name = "agenda"
    timestamp_str = "2019-01-03_1646_06488910"
    expected = "/Users/tbaker/tmp/.backups/agenda/2019-01-03_1646_06488910"
    assert (
        return_backupdir_pathname(
            _rootdir_pathname=rootdir_pathname,
            _backupdir_subdir_name=backupdir_name,
            _backupdir_shortname=backupdir_subdir_name,
            _timestamp_str=timestamp_str,
        )
        == expected
    )
