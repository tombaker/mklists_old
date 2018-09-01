"""Verbose module"""

import sys
from mklists import (
    NoRulefileSpecified,
    TIMESTAMP)


def explain_configuration(**kwargs):
    """docstring"""

    # short names - to keep line length short
    globalrules = kwargs['globalrules']
    rules = kwargs['rules']
    urlify = kwargs['urlify']
    urlify_dir = kwargs['urlify_dir']
    backup = kwargs['backup']
    backup_dir = kwargs['backup_dir']
    backup_depth = kwargs['backup_depth']
    readonly = kwargs['readonly']
    verbose = kwargs['verbose']
    valid_filename_characters = kwargs['valid_filename_characters']
    invalid_filename_patterns = kwargs['invalid_filename_patterns']
    files2dirs = kwargs['files2dirs']

    if globalrules:
        print(f"Global rule file {repr(globalrules)} "
               "(will load before local rule file).")
    else:
        print("Config does not point to an (optional) global rule file.")

    if rules:
        print(f"Local rule file (required): {repr(rules)}.")
    else:
        print(f"Uh-oh, config does not point to (required) local rule file.")
        print(f"    Try one of the following:")
        print(f"    1. Edit .mklistsrc, adding the line:")
        print(f"       rules: .rules")
        print(f"    2. Run `mklists --rule FILE`, pointing to any rule file.")
        raise NoRulefileSpecified

    if urlify:
        print(f"'urlify' option is ON, so TXT files will be copied, "
                "converted into HTML,")
        if urlify_dir:
            print("and saved in the {repr(urlify_dir)} directory.")
        else:
            print("however the option will fail "
                  "because no destination directory has been "
                  "specified for the urlified files.")
            print("Try editing '.mklistsrc', adding the line:")
            print(f"    urlify_dir: /path/to/some/directory")
            print(f"Then make sure that /path/to/some/directory exists.")
    else:
        print(f"'urlify' option is OFF, so TXT files will NOT "
                "be copied and converted into HTML.")

    if backup:
        backup_dir_timestamped = '/'.join([backup_dir, TIMESTAMP])
        print("'backup' option is ON, so data files will be backed up ")
        if backup_dir:
            print(f"...to the directory {repr(backup_dir_timestamped)}.")
        else:
            print("However, the command will fail "
                  "because no backup directory has been specified.")
            print("Try editing '.mklistsrc', adding the line:")
            print(f"    backup_dir: /path/to/some/directory")
            print(f"Then make sure that /path/to/some/directory exists.")
    else:
        print("Config does NOT set 'backup', "
              "so data files will NOT be backed up.")

    if backup_depth:
        print(f"...where the last {backup_depth} backups will be kept.")

    if readonly:
        print("Will stop short of writing to disk or moving files.")

    if valid_filename_characters:
        print(f"Valid filename characters: {valid_filename_characters}")

    if files2dirs:
        print("Output file of given name to be moved to given directory.")
    else:
        print("'files2dirs' option not set in MKLISTS - see documentation.")
