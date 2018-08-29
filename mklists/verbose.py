"""Verbose module"""

import sys
from mklists import NoRulefileSpecified


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
        print(f"Config points to global rule file: {globalrules}, "
               "which will load before local rule file.")
    else:
        print("Config does not point to an (optional) global rule file.")

    if rules:
        print(f"Config points to required local rule file: {rules}.")
    else:
        print(f"Uh-oh, config does not point to (required) local rule file.")
        print(f"    Try one of the following:")
        print(f"    1. Edit .mklistsrc, adding the line:")
        print(f"       rules: .rules")
        print(f"    2. Run `mklists --rule FILE`, where FILE is any rule file.")
        raise NoRulefileSpecified

    if urlify:
        print(f"Config sets 'urlify', so copies of TXT files into HTML.")
    else:
        print(f"Will NOT convert copies of TXT files into HTML.")

    sys.exit('exiting...')

    if ctx.obj['urlify_dir']:
        print(f"If urlify activated, files saved in {ctx.obj['urlify']}.")
    else:
        print(f"If urlify activated, would fail: no destination dir.")


    if backup:
        print("Will back up data files")
    else:
        print("Will not back up data files")

    if backup_dir:
        # Somewhere in module, calculate YYYYMMDD
        print("Will back up files to directory X/YYYYMMDD_hhmmss")

    if backup_depth:
        print("Will keep last {backup_depth} backups.")

    if readonly:
        print("Will stop short of writing to disk or moving files.")

    if valid_filename_characters:
        print("Filenames must consist only of the following characters:")
        print(f"{valid_filename_chars}")

    if files2dirs:
        print("Output file of given name to be moved to given directory.")

    print("Edit MKLISTSRC to change settings for future use")
