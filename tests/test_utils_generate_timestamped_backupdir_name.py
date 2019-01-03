"""@@@Docstring"""

from mklists.utils import generate_timestamped_backupdir_name


def test_utils_generate_timestamped_backupdir_name():
    timestamp = "2019-01-03_1646_06488910"
    cwd = "agenda"
    expected = "agenda/2019-01-03_1646_06488910"
    assert generate_timestamped_backupdir_name(here=cwd, now=timestamp) == expected
