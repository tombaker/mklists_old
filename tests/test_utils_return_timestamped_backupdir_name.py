"""@@@Docstring"""

from mklists.utils import construct_backupdir_name


def test_utils_construct_backupdir_name():
    timestamp = "2019-01-03_1646_06488910"
    cwd_shortname = "agenda"
    expected = "agenda/2019-01-03_1646_06488910"
    assert construct_backupdir_name(here=cwd_shortname, now=timestamp) == expected
