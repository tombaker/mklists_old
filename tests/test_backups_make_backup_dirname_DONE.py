"""@@@Docstring"""

from mklists.backups import make_backupdir_pathname


def test_backups_make_backupdir_pathname():
    timestamp = "2019-01-03_1646_06488910"
    backup_shortname = "agenda"
    expected = "agenda/2019-01-03_1646_06488910"
    assert (
        make_backupdir_pathname(now=timestamp, backupdir_name=backup_shortname)
        == expected
    )
