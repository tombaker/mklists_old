"""@@@Docstring"""

from mklists.utils import make_backupdir_name


def test_utils_make_backupdir_name():
    timestamp = "2019-01-03_1646_06488910"
    cwd_shortname = "agenda"
    expected = "agenda/2019-01-03_1646_06488910"
    assert make_backupdir_name(listdir_name=cwd_shortname, now=timestamp) == expected
