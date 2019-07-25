"""@@@Docstring

Edit /Users/tbaker/github/tombaker/mklists/mklists/backups.py
"""

from mklists.backups import make_backupdir_pathname


def test_backups_make_backupdir_pathname():
    root = "/Users/tbaker/tmp"
    backups = ".backups"
    shortname = "agenda"
    now = "2019-01-03_1646_06488910"
    expected = "/Users/tbaker/tmp/.backups/agenda/2019-01-03_1646_06488910"
    assert (
        make_backupdir_pathname(
            reporoot_pathname=root,
            backups_dirname=backups,
            backup_shortname=shortname,
            timestamp_name=now,
        )
        == expected
    )
