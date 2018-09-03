"""Subroutines module

The now-archaic word "subroutine" sometimes referred to functions 
that had side effects such as reading from disk, creating files 
and modifying data structures in memory, as do all of these 
functions.
"""

import os
import re
import string
import pprint
import yaml
from mklists import (
    VALID_FILENAME_CHARS,
    URL_PATTERN,
    TIMESTAMP,
    MKLISTSRC,
    STARTER_GRULES,
    STARTER_LRULES,
    BadFilenameError,
    BlankLinesError,
    DatadirHasNonFilesError,
    InitError,
    NoDataError,
    NoRulesError,
    NotUTF8Error,
    RuleFileNotFoundError,
    BadYamlError, 
    BadYamlRuleError)
from mklists.rule import Rule


def set_data_directory(dirname):
    """Set current working directory for mklists (data)."""
    if dirname is not None:
        try:
            os.chdir(dirname)
            print(f"Setting {repr(dirname)} as data directory.")
        except FileNotFoundError:
            raise dirnameNotAccessibleError(f"{dirname} is not accessible.")

def load_mklistsrc(filename, context=None, verbose=False):
    try:
        with open(MKLISTSRC) as configfile:
            context.update(yaml.load(configfile))
        if verbose:
            print(f"Loading configuration file {repr(MKLISTSRC)}.")
    except FileNotFoundError:
        raise ConfigFileNotFoundError(f"First set up with `mklists init`.")

def write_initial_configfile(context=None,
                             filename=MKLISTSRC,
                             readonly=False,
                             verbose=False):
    """Writes initial configuration file to disk (or just says it will)."""
    if os.path.exists(filename):
        raise InitError(f"To re-initialize, first delete {repr(filename)}.")
    else:
        if readonly:
            print(f"['readonly' is on] Would have created {repr(filename)}.")
        else:
            print(f"Creating default {repr(filename)} - customize as needed.")
            with open(filename, 'w') as fout:
                yaml.safe_dump(context, sys.stdout, default_flow_style=False)

def write_initial_rulefiles(grules=None, 
                            lrules=None, 
                            valid_filename_chars=None,
                            readonly=False,
                            verbose=False):
    for file, content in [(grules, STARTER_GRULES), (lrules, STARTER_LRULES)]:
        if file:
            if os.path.exists(file):
                print(f"Found existing {repr(file)} - leaving untouched.")
            else:
                if readonly:
                    print(f"['readonly' is on] "
                          "Would have created {repr(file)}.")
                else:
                    print(f"Creating starter rule file {repr(file)} - "
                          "this is meant to be customized before use.")
                    with open(file, 'w') as fout:
                        fout.write(content)

def get_rules(grules=None,
              lrules=None,
              valid_filename_chars=None,
              verbose=False):
    rule_object_list = []
    for rulefile in grules, lrules:
        if rulefile:
            rule_object_list.extend(
                    parse_yamlrules(rulefile, valid_filename_chars))
        if not rule_object_list:
            raise NoRulesError("No rules to work with!")
    if verbose:
        pprint.pprint(rule_object_list)
    return rule_object_list

def parse_yamlrules(rulefile, good_chars=VALID_FILENAME_CHARS):
    """Returns list of rule objects from parsing a YAML-format rule file."""
    parsed_yaml = _parse_yaml(rulefile)
    rule_objects_list = _create_list_of_rule_objects(parsed_yaml)
    for rule_object in rule_objects_list:
        rule_object.is_valid(good_chars)
    return rule_objects_list

def _parse_yaml(rulefile):
    """Returns unvalidated list of split-out rule lines.
    
    Args:
        rulefile: a file of rules in YAML format

    Raises:
        ParserError??
    """
    list_parsed_from_yaml = []
    try:
        with open(rulefile) as rfile:
            list_parsed_from_yaml.extend(yaml.load(rfile))
    #except ParserError: # can this happen here?
    #    raise BadYamlError(f"YAML format of {rulefile} does not parse.")
    except FileNotFoundError:
        print(f"{repr(rulefile)} not found - skipping.")
    return list_parsed_from_yaml

def _create_list_of_rule_objects(rule_list_from_yaml: list = None):
    """Returns list of rule objects.

    Args:
        rule_list_from_yaml: list of unvalidated split-out rule lines.
    """
    list_of_rule_objects = []
    for item in rule_list_from_yaml:
        try:
            list_of_rule_objects.append(Rule(*item))
        except TypeError:
            raise BadYamlRuleError(f"{item} is badly formed.")
    # test here for NoRulesError - if function returns empty (False) rule list?
    # assert list_of_rule_objects, "something"?
    return list_of_rule_objects

def get_datalines(ls_visible=[],
              but_not=None):
    """Returns aggregated list of lines from data files.
    
    Mklists is very strict about contents of data directory.
    All exceptions encountered in this function, in _get_file(), 
    and in any of the functions called by _get_file(), will 
    result in exit from the program, with an error message about 
    what the user will need to correct in order to get it to run."""
    datalines = []
    for item in ls_visible:
        datalines.append(_get_filelines(item, invalid_patterns=but_not))
        if verbose:   
            print(f"Reading {repr(item)}.")
            print(datalines)  # 2018-09-02: just for debugging
    if not datalines:
        raise NoDataError('No data to process!')
    return datalines

def _get_filelines(thing_in_directory, 
                   invalid_patterns=None):
    all_lines = []
    if not is_file(thing_in_directory):
        print("All visible objects in current directory must be files.")
        raise DatadirHasNonFilesError(f'{thing_in_directory} is not a file.')
    if not has_valid_name(thing_in_directory, invalid_patterns):
        print("Invalid filename patterns are intended to detect the "
              "presence of backup files, temporary files, and the like.")
        raise BadFilenameError(f"{repr(thing_in_directory)} matches one of "
                               "{invalid_patterns}.")
    if not is_utf8_encoded(thing_in_directory):
        print("All visible files in data directory must be UTF8-encoded.")
        raise NotUTF8Error(f'File {thing_in_directory} is not UTF8-encoded.')
    with open(thing_in_directory) as rfile:
        for line in rfile:
            if not line:
                raise BlankLinesError(f"{thing_in_directory} is not valid as"
                                      "data because it has blank lines.")
            all_lines.append(line)

    return all_lines
    
def move_datafiles_to_backup(ls_visible=[],
                             backup=False,
                             backup_dir=None,
                             backup_depth=None):
    """If 'backup' is ON: 
    before writing datalines_dict contents to disk, 
    creates timestamped backup directory in specified backup_dir,
    and moves all visible files in data directory to backup directory.
    """
    # First, make time-stamped backup_dir (and backup_dir itself if not exist)
    # Move existing files to backup_dir
    # Delete oldest backups:
    # delete_oldest_backup(backup_dir, backup_depth):
    #     lsd_visible = [item for item in glob.glob('*') 
    #                    if os.path.isdir(item)]
    #     while len(lsd_visible) > backup_depth:
    #         file_to_be_deleted = ls_visible.pop()
    #         rm file_to_be_deleted

def write_new_datafiles(datalines_d=None,
                        readonly=False,
                        backup=False, 
                        backup_dir=None,
                        backup_depth=None,
                        verbose=False):
    # will call _move_datafiles_to_backup, using TIMESTAMP
    # Create: backup_dir_timestamped = '/'.join([backup_dir, TIMESTAMP])
    # @@@@
    pass

# Write urlified data files to urlify_dir.
def write_urlified_datafiles(datalines_d={},
                             urlify_dir=None,
                             readonly=True,  # later: ctx.obj['readonly'],
                             verbose=False):
    print(f"* Move files outside datadir as per ['files2dirs'].")
