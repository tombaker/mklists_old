"""Module for functions that have following side effects::
* move files between directories
* write to files on disk"""


def move_certain_listfiles_to_other_directories(files2dirs_dict=None):
    """Args: files2dirs_dict: filename (key) and destination directory (value)"""


def move_old_listfiles_to_backupdir(backupdir, backups=2):
    """
    if backups is less than two, then backups = 2 - "mandatory"
    If 'backup' is True:
    before writing data_dict contents to disk,
    creates timestamped backup directory in specified backup_dir,
    and moves all visible files in data directory to backup directory.
    Make time-stamped directory in BACKUP_DIR_NAME (create constant!)
    Create: backup_dir_timestamped = os.path.join(backup_dir, TIMESTAMP_STR)
    Move existing files to backup_dir
    Delete oldest backups:
    delete_oldest_backup(backup_dir, backups):
        lsd_visible = [item for item in glob.glob('*')
                       if os.path.isdir(item)]
        while len(lsd_visible) > backups:
            file_to_be_deleted = get_lsvisible_names.pop()
            rm file_to_be_deleted
    for file in filelist:
        shutil.move(file, backup_dir)

    Note: there should never be a situation where listfiles have
    been deleted and the data in memory has not yet been written to disk.
    Therefore, there should _always_ be at least one backup."""


def write_yamlstr_to_yamlfile(yamlstr, yamlfile_name):
    """Write YAML string to YAML file."""
    with open(yamlfile_name, "w") as fout:
        fout.write(yamlstr)
