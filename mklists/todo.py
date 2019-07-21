"""Todo"""


def delete_older_backups():
    """
    See /Users/tbaker/github/tombaker/mklists/tests/test_todo_delete_older_backups.py
    Count number of backups under this directory:
        Get short name of current data directory (get_datadir_shortname).
        Create list of directories under parent directory of backupdir.
            lsd_visible = [item for item in glob.glob('*') if os.path.isdir(item)]
            Example: if backup dir is
                mkrepo/_backups/a/2018-12-31.23414123
            Then parent is
                mkrepo/_backups/a
            Resulting list might be:
                [ '2018-12-31.23414123', '2019-01-01.12155264', '2019-02-02.02265324' ]
    Either:
        while len(lsd_visible) > backups:
            file_to_be_deleted = lsd_visible.pop(0)
            rm file_to_be_deleted
    Or:
        while len(directory_list) > backups:
            dir_to_delete = directory_list.pop(0)
            print(f"rm {dir_to_delete}")
    """


def move_certain_datafiles_to_other_directories(files2dirs_dict=None):
    """Args: files2dirs_dict: filename (key) and destination directory (value)
    See /Users/tbaker/github/tombaker/mklists/tests/test_todo_move_certain_datafiles_to_other_directories
    """


def write_datadict_to_htmlfiles_in_htmldir(datadict={}, verbose=False):
    """
    See /Users/tbaker/github/tombaker/mklists/tests/test_todo_write_datadict_to_htmlfiles_in_htmldir
    -- Create htmldir (if it does not already exist).
    -- Delete files in htmldir (if files already exist there).
    -- Write out contents of datadict to working directory:
       -- datadict keys are filenames.
          -- for each filename, add file extension '.html'
       -- datadict values are contents of files.
          -- filter each line through make_htmlstr_from_textstr.
    """
