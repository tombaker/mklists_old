"""move_datafiles_to_backupdir()

Edit /Users/tbaker/github/tombaker/mklists/mklists/backups.py
"""

import os
from mklists.backups import move_datafiles_to_backupdir


def test_backups_move_datafiles_to_backupdir(tmpdir):
    """Function move_datafiles_to_backupdir() uses output of
    return_backupdir_pathname(), emulated here by assembling the
    backupdir_pathname from its components:

    * return_backupdir_pathname:rootdir_pathname => here: tmpdir
      * default: generated by return_rootdir_pathname()
    * return_backupdir_pathname:_backupdir_pathname   => here: backups
      * default: backups:BACKUPDIR_NAME
    * return_backupdir_pathname:backup_shortname  => here: shortname
      * default: generated by return_backupdir_shortname()
    * return_backupdir_pathname:_timestamp_str    => here: timestamp
      * default: backups:TIMESTAMP_STR

    """
    backups = ".backups"
    shortname = "agenda"
    timestamp = "2019-07-26_0758_06488910"
    tmpdir_backupdir = tmpdir.mkdir(backups)
    tmpdir_backupdir_agenda = tmpdir_backupdir.mkdir(shortname)
    backupdir_fullpath = tmpdir_backupdir_agenda.mkdir(timestamp)
    tmpdir_agendadir = tmpdir.mkdir(shortname)
    tmpdir_agendadir.join("file_a").write("some content")
    tmpdir_agendadir.join("file_b").write("some content")
    ls_agendadir_before = sorted(
        os.listdir(tmpdir_agendadir)
    )  # stand-in for return_visiblefiles_list()
    move_datafiles_to_backupdir(
        datadir_pathname=tmpdir_agendadir,
        datadir_filenames=ls_agendadir_before,  # try putting sorted... here
        backupdir_pathname=backupdir_fullpath,
    )
    expected = ["file_a", "file_b"]
    assert sorted(os.listdir(backupdir_fullpath)) == expected
    assert sorted(os.listdir(tmpdir_agendadir)) == []

    # print(f"ls_agendadir_before = {ls_agendadir_before}")
    # print(f"expected = {expected}")
    # print(f"ls_backupdir_agenda = {ls_backupdir_agenda}")
