"""@@@Docstring"""

from mklists.utils import make_backup_dirname


def test_utils_make_backup_dirname():
    timestamp = "2019-01-03_1646_06488910"
    cwd_backup_shortname = "agenda"
    expected = "agenda/2019-01-03_1646_06488910"
    assert (
        make_backup_dirname(datadir_name=cwd_backup_shortname, now=timestamp)
        == expected
    )
