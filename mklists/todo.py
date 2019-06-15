"""Todo"""

# import os
# from .utils import get_rootdir_pathname


def delete_older_backups():
    """
    Count number of backups under this directory:
        Get short name of current data directory (get_cwd_basename).
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


def get_ctxobj_from_config_yamlfile():
    """"""


def move_certain_listfiles_to_other_directories(files2dirs_dict=None):
    """Args: files2dirs_dict: filename (key) and destination directory (value)"""


def move_existing_listfiles_to_backupdir(backupdir, backups=2):
    """
    Get number of backups as configuring (config['backups']
        If backups less than two, then backups = 2 ("mandatory")
    Create a backup directory.
        Generate a name for backupdir (make_backupdir_name).
        Make dir: hard-coded parent dirname (_html) plus generated timestamped name.
    Get list of existing visible files in data directory.
    Move all visible files in data directory to backupdir.
        for file in filelist:
            shutil.move(file, backupdir)
    """


def move_listfiles_from_currentdir_to_backupdir(files=None):
    """
    -- Move existing files from working directory to backupdir.
    """


def write_datadict_to_htmlfiles_in_htmldir(datadict={}, verbose=False):
    """
    -- Create htmldir (if it does not already exist).
    -- Delete files in htmldir (if files already exist there).
    -- Write out contents of datadict to working directory:
       -- datadict keys are filenames.
          -- for each filename, add file extension '.html'
       -- datadict values are contents of files.
          -- filter each line through make_htmlstr_from_textstr.
    """


def write_initial_rule_yamlfiles():
    pass
