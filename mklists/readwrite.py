"""Read-write module

Functions with side effects such as:
* reading files from disk
* writing to files on disk
* modifying data structures in memory
"""

import os
import re
import string
import sys
import pprint
import yaml
from mklists import (
    GLOBAL_RULEFILE_NAME,
    GLOBAL_RULEFILE_STARTER_YAMLSTRING,
    LOCAL_RULEFILE_NAME,
    LOCAL_RULEFILE_STARTER_YAMLSTRING,
    MKLISTSRC_STARTER_DICT,
    MKLISTSRC_LOCAL_NAME,
    TIMESTAMP,
    URL_PATTERN,
    VALID_FILENAME_CHARS,
    BadFilenameError,
    BadYamlError,
    BadYamlRuleError,
    BlankLinesError,
    ConfigFileNotFoundError,
    DatadirHasNonFilesError,
    InitError,
    NoDataError,
    NoRulesError,
    NotUTF8Error,
)
from mklists.rules import Rule


def read_overrides_from_file(configfile_name):
    """docstring"""
    return yaml.load(open(configfile_name).read())


def apply_overrides(context, overrides):
    """docstring"""
    overrides.pop("ctx", None)
    overrides = {
        key: overrides[key] for key in overrides if overrides[key] is not None
    }
    context.update(overrides)
    return context


def write_yamlstr_to_yamlfile(yamlfile_name, yamlstr):
    """Writes string in YAML format to file."""
    with open(yamlfile_name, "w") as fout:
        fout.write(yamlstr)


def read_yamlfile_return_pyobject(yamlfile_name):
    """Returns Python object parsed from YAML-format file."""
    try:
        return yaml.safe_load(open(yamlfile_name))
    except yaml.YAMLError:
        raise BadYamlError(f"Bad YAML format in {repr(yamlfile_name)}.")


def get_rules(local_rulefile_name=None, global_rulefile_name=None):
    aggregated_rules_list = []
    for rulefile_name in global_rulefile_name, local_rulefile_name:
        if rulefile_name:
            rules_list = read_yamlfile_return_pyobject(rulefile_name)
            aggregated_rules_list = aggregated_rules_list + rules_list
    ruleobj_list = []
    for item in aggregated_rules_list:
        try:
            Rule(*item).is_valid
        except TypeError:
            raise BadYamlRuleError(f"Rule {repr(item)} is badly formed.")
        ruleobj_list.append(Rule(*item))

    return ruleobj_list


def get_rules2(lrules=LOCAL_RULEFILE_NAME, grules=GLOBAL_RULEFILE_NAME):
    rules_list = []
    try:
        rules_to_add = read_yamlfile_return_pyobject(grules)
        rules_list.append(rules_to_add)
    except FileNotFoundError:
        print("File was not found")
    except TypeError:
        print("NoneType")
    return rules_list

    # for rulefile_name in grules, lrules:
    #     if rulefile_name:
    #         rules_list = rules_list + rules_list
    # ruleobj_list = []
    # for item in rules_list:
    #     try:
    #         Rule(*item).is_valid
    #     except TypeError:
    #         raise BadYamlRuleError(f"Rule {repr(item)} is badly formed.")
    #     ruleobj_list.append(Rule(*item))

    # return ruleobj_list


def write_initial_configfile(settings_dict=None, verbose=False):
    """Writes initial configuration file to disk (or just says it will).
    * If configfile already exists, exits suggesting to first delete.
    * If configfile not found, creates new file using current settings.
    """
    if os.path.exists(configfile_name):
        raise InitError(
            f"To re-initialize, first delete {repr(configfile_name)}."
        )
    else:
        print(
            f"Creating default {repr(configfile_name)}. "
            f"Customize as needed."
        )
        with open(configfile_name, "w") as fout:
            fout.write(yaml.safe_dump(settings_dict, default_flow_style=False))


def write_initial_rulefiles(
    global_rulefile_name=GLOBAL_RULEFILE_NAME,
    local_rulefile_name=LOCAL_RULEFILE_NAME,
    globalrules_content=GLOBAL_RULEFILE_STARTER_YAMLSTRING,
    localrules_content=LOCAL_RULEFILE_STARTER_YAMLSTRING,
    verbose=False,
):
    """Generate default rule (and global rule) configuration files.

        Checks whether current settings name non-default rule files.
        If either rule file already exists, leaves untouched.
        Creates rule files with default contents.
    """
    for file, content in [
        (global_rulefile_name, globalrules_content),
        (local_rulefile_name, localrules_content),
    ]:
        if file:
            if os.path.exists(file):
                print(f"Found existing {repr(file)} - leaving untouched.")
            else:
                print(
                    f"Creating starter rule file {repr(file)} "
                    "from built-in settings - can be customized."
                )
                with open(file, "w") as fout:
                    fout.write(content)


def get_datalines(ls_visible=[], but_not=None):
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
        raise NoDataError("No data to process!")
    return datalines


def _get_filelines(thing_in_directory, invalid_patterns=None):
    all_lines = []
    if not is_file(thing_in_directory):
        print("All visible objects in current directory must be files.")
        raise DatadirHasNonFilesError(f"{thing_in_directory} is not a file.")
    if not has_valid_name(thing_in_directory, invalid_patterns):
        print(
            "Invalid filename patterns are intended to detect the "
            "presence of backup files, temporary files, and the like."
        )
        raise BadFilenameError(
            f"{repr(thing_in_directory)} matches one of " "{invalid_patterns}."
        )
    if not is_utf8_encoded(thing_in_directory):
        print("All visible files in data directory must be UTF8-encoded.")
        raise NotUTF8Error(f"File {thing_in_directory} is not UTF8-encoded.")
    with open(thing_in_directory) as rfile:
        for line in rfile:
            if not line:
                raise BlankLinesError(
                    f"{thing_in_directory} is not valid as "
                    "data because it has blank lines."
                )
            all_lines.append(line)

    return all_lines


def move_datafiles_to_backup(backup_depth=None):
    """
    Make time-stamped directory in BACKUP_DIR_NAME (create constant!)
    Create: backup_dir_timestamped = '/'.join([backup_dir, TIMESTAMP])
    Move existing files to backup_dir
    Delete oldest backups:
    delete_oldest_backup(backup_dir, backup_depth):
        lsd_visible = [item for item in glob.glob('*')
                       if os.path.isdir(item)]
        while len(lsd_visible) > backup_depth:
            file_to_be_deleted = ls_visible.pop()
            rm file_to_be_deleted
    for file in filelist:
        shutil.move(file, backup_dir)
    """


def write_data_to_files(datalines_d=None, verbose=False):
    pass


# Write urlified data files to urlify_dir.
def write_data_urlified_to_files(
    datalines_d={}, urlify_dir=None, verbose=False
):
    """Something like: def removefiles(targetdirectory):
    pwd = os.getcwd()
    abstargetdir = absdirname(targetdirectory)
    if os.path.isdir(abstargetdir):
        os.chdir(abstargetdir)
        files = datals()
        if files:
            for file in files:
                os.remove(file)
        os.chdir(pwd)
    """
    print(f"* Move files outside datadir as per ['files2dirs'].")


def move_files_to_external_directories(files2dirs_dict=None):
    """
    Args:
        files2dirs_dict: filename (key) and destination directory (value)
    """
