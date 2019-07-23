"""@@@Docstring"""

from mklists.utils import make_backupdir_name


def test_utils_make_backupdir_name():
    timestamp = "2019-01-03_1646_06488910"
    cwd_backup_shortname = "agenda"
    expected = "agenda/2019-01-03_1646_06488910"
    assert (
        make_backupdir_name(datadir_name=cwd_backup_shortname, now=timestamp)
        == expected
    )
