"""Verbose module

2018-09-05: removed assignment to local short names - using sets['x']
            but this is _untested_
"""

import sys
from mklists import (
    NoRulefileSpecified,
    MKLISTSRC_NAME,
    TIMESTAMP)


def explain(**sets):
    """docstring"""

    if sets['globalrules']:
        print(f"Global rule file {repr(sets['globalrules'])} "
               "(will load before local rule file).")
    else:
        print("Config does not point to an (optional) global rule file.")

    if sets['rules']:
        print(f"Local rule file (required): {repr(sets['rules'])}.")
    else:
        print(f"Uh-oh, config does not point to (required) local rule file.")
        print(f"    Try one of the following:")
        print(f"    1. Edit .mklistsrc, adding the line:")
        print(f"       rules: .rules")
        print(f"    2. Run `mklists --rule FILE`, pointing to any rule file.")
        raise NoRulefileSpecified

    if sets['urlify']:
        print(f"'urlify' option is ON, so TXT files will be copied, "
                "converted into HTML,")
        if sets['urlify_dir']:
            print("and saved in the {repr(sets['urlify_dir'])} directory.")
        else:
            print("...however the option will fail "
                  "because no destination directory has been "
                  "specified for the urlified files.")
            print(f"Try editing {repr(sets[MKLISTSRC_NAME])}, adding the line:")
            print(f"    urlify_dir: /path/to/some/directory")
            print(f"Then make sure that /path/to/some/directory exists.")
    else:
        print(f"'urlify' option is OFF, so TXT files will NOT "
                "be copied and converted into HTML.")

    if sets['backup']:
        backup_dir_timestamped = '/'.join([sets['backup_dir'], TIMESTAMP])
        print("'backup' option is ON, so data files will be backed up ")
        if backup_dir:
            print(f"...to the directory {repr(backup_dir_timestamped)}.")
            print(f"...where the {repr(sets['backup_depth'])} most "
                   "recent backups will be kept.")
        else:
            print("...however the command will fail "
                  "because no backup directory has been specified.")
            print(f"Try editing {repr(sets[MKLISTSRC_NAME])}, adding the line:")
            print(f"    backup_dir: /path/to/some/directory")
            print(f"Then make sure that /path/to/some/directory exists.")
    else:
        print("Config does NOT set 'backup', "
              "so data files will NOT be backed up.")

    if sets['backup_depth']:
        print(f"...where last {sets['backup_depth']} backups will be kept.")

    if sets['readonly']:
        print("Will stop short of writing to disk or moving files.")

    if sets['valid_filename_characters']:
        print(f"Valid filename characters: "
               "{sets['valid_filename_characters']}")

    if sets['files2dirs']:
        print("Output file of given name to be moved to given directory.")
    else:
        print(f"'files2dirs' option not set in "
               "{repr(sets[MKLISTSRC_NAME])} - see documentation.")
