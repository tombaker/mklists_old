"""Utility module"""

import os
import re
import string
import yaml
from mklists import (
    URL_PATTERN,
    MKLISTSRC,
    STARTER_GRULES,
    STARTER_LRULES,
    BadFilenameError,
    BlankLinesError,
    DatadirHasNonFilesError,
    InitError,
    NoDataError,
    NoRulesError,
    NotUTF8Error)

#def load_values(ctx, globalrules, rules,
#                            backup, backup_dir, backup_depth,
#                            urlify, urlify_dir,
#                            readonly, verbose):

def load_mklistsrc(filename, context=None):
    print(f"yeah! loading {filename}!")
    try:
        with open(MKLISTSRC) as configfile:
            context.update(yaml.load(configfile))
    except FileNotFoundError:
        raise ConfigFileNotFoundError(f"First set up with `mklists init`.")

def set_data_directory(dirname):
    """Set current working directory for mklists (data)."""
    if dirname is not None:
        try:
            os.chdir(dirname)
            print(f"Setting {repr(dirname)} as data directory.")
        except FileNotFoundError:
            raise dirnameNotAccessibleError(f"{dirname} is not accessible.")

def write_initial_rulefiles(grules=None, lrules=None):
    if not ctx.obj['rules']:   
        ctx.obj['rules'] = RULEFILE
    for file, content in [(ctx.obj['globalrules'], STARTER_GRULES),
                          (ctx.obj['rules'], STARTER_LRULES)]:
        if file:
            if os.path.exists(file):
                print(f"Found {repr(file)} - leaving untouched.")
            else:
                if ctx.obj['readonly']:
                    print(f"READONLY: would have created {repr(file)}.")
                else:
                    print(f"Creating {repr(file)} - tweak as needed.")
                    with open(file, 'w') as fout:
                        fout.write(content)

def get_rules(grules=None, lrules=[], good_chars=None):
    rule_object_list = []
    for rulefile in grules, lrules:
        if rulefile:
            print(rulefile)
            rule_object_list.extend(parse_yamlrules(rulefile, good_chars=good))
        if not rule_object_list:
            raise NoRulesError("No rules to work with!")
    return rule_object_list
    
def write_initial_configfile(filename=MKLISTSRC):
    """Writes initial configuration file to disk."""
    if os.path.exists(filename):
        raise InitError(f"To re-initialize, first delete {repr(filename)}.")
    else:
        if ctx.obj['readonly']:
            print(f"READONLY: would have created {repr(filename)}.")
        else:
            print(f"Creating default {repr(filename)} - customize as needed.")
            with open(filename, 'w') as fout:
                yaml.safe_dump(ctx.obj, sys.stdout, default_flow_style=False)

def get_lines(thing, invalid_patterns=None):
    all_lines = []
    if not is_file(thing):
        print("All visible objects in current directory must be files.")
        raise DatadirHasNonFilesError(f'{thing} is not a file.')
    if not has_valid_name(thing, bad_names=invalid_patterns):
        print("Invalid filename patterns are intended to detect the "
              "presence of backup files, temporary files, and the like.")
        raise BadFilenameError(f"{repr(thing)} matches one of "
                               "{ctx.obj['invalid_filename_patterns']}.")
    if not is_utf8_encoded(thing):
        print("All visible files in data directory must be UTF8-encoded.")
        raise NotUTF8Error(f'File {thing} is not UTF8-encoded.')
    with open(thing) as rfile:
        for line in rfile:
            if not line:
                print("No file in data directory may contain blank lines.")
                raise BlankLinesError(f'{repr(thing)} has blank lines.')
            all_lines.append(line)

    return all_lines

def is_file(object_path):
    """Returns True if object is a file.

    Raises:
        DatadirHasNonFilesError: if object is not a file.
    """
    if not os.path.isfile(object_path):
        return False
    return True

def has_valid_name(filename, bad_names):
    """Return True if no filenames match bad patterns.

    Used to block execution of mklists if the data
    folder has any files that should not be processed,
    such as temporary files or backup files.

    Raises:
        BadFilenameError: if filename matches a bad pattern.
    """
    for bad_pattern in bad_names:
        if re.search(bad_pattern, filename):
            print(f"{repr(bad_pattern)} in {filename}.")
            return False
    return True

# Note: is_utf8_encoded, has_no_blank_lines
def is_utf8_encoded(file):
    """Returns True if all data files are UTF8-encoded.

    Raises:
        UnicodeDecodeError: if any file is not UTF8-encoded.
    """
    try:
        open(file).read()
    except UnicodeDecodeError:
        return False
    return True

def has_no_blank_lines(text_file):
    """Note: Does not test whether test file"""
    for line in text_file:
        if not line:
            return False
    return True

def linkify(string_raw):
    if '<a href=' in string_raw:
        return string_raw
    return re.compile(URL_PATTERN).sub(r'<a href="\1">\1</a>', string_raw)

