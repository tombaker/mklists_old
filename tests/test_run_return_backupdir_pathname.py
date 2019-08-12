"""@@@Docstring

Edit /Users/tbaker/github/tombaker/mklists/mklists/backups.py
"""

from mklists.backups import return_backupdir_pathname


def test_backups_return_backupdir_pathname():
    """@@@Docstring"""
    root = "/Users/tbaker/tmp"
    backups = ".backups"
    shortname = "agenda"
    now = "2019-01-03_1646_06488910"
    expected = "/Users/tbaker/tmp/.backups/agenda/2019-01-03_1646_06488910"
    assert (
        return_backupdir_pathname(
            _rootdir_pathname=root,
            _backupdir_pathname=backups,
            _backupdir_shortname=shortname,
            _timestamp_str=now,
        )
        == expected
    )
