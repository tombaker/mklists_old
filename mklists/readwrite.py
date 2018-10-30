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
from mklists import (VALID_FILENAME_CHARS, URL_PATTERN, TIMESTAMP, MKLISTSRC_NAME,
    BUILTIN_GRULES, BUILTIN_LRULES, BUILTIN_GRULEFILE_NAME, BUILTIN_MKLISTSRC,
    BUILTIN_LRULEFILE_NAME, BadFilenameError, BlankLinesError, 
    DatadirHasNonFilesError, InitError, NoDataError, NoRulesError,
    NotUTF8Error, BadYamlError, BadYamlRuleError, ConfigFileNotFoundError)
from mklists.rule import Rule


def write_yamlstr_to_yamlfile(yamlfile_name, yamlstr):
    """Writes string in YAML format to file."""
    with open(yamlfile_name, "w") as fout:
        fout.write(yamlstr)

def read_yamlfile_parseto_pyobject(yamlfile_name):
    """Returns Python object parsed from YAML-format file."""
    try:
        return yaml.safe_load(open(yamlfile_name))
    except yaml.YAMLError:
        raise BadYamlError(f"Bad YAML format in {repr(yamlfile_name)}.")

def get_rules(local_rulefile_name=None, global_rulefile_name=None):
    aggregated_rules_list = []
    for rulefile_name in global_rulefile_name, local_rulefile_name:
        if rulefile_name:
            rules_list = read_yamlfile_parseto_pyobject(rulefile_name)
            aggregated_rules_list = aggregated_rules_list + rules_list
    ruleobj_list = []
    for item in aggregated_rules_list:
        try:
            Rule(*item).is_valid
        except TypeError:
            raise BadYamlRuleError(f"Rule {repr(item)} is badly formed.")
        ruleobj_list.append(Rule(*item))
                
    return ruleobj_list

def update_config_from_file(file_name=MKLISTSRC_NAME, 
                            settings_dict=BUILTIN_MKLISTSRC,
                            verbose=False):
    """See ../tests/test_update.py"""

def write_initial_configfile(settings_dict=None,
                             configfile_name=MKLISTSRC_NAME,
                             dryrun=False,
                             verbose=False):
    """Writes initial configuration file to disk (or just says it will).
        If configfile already exists, exits suggesting to first delete.
        If configfile not found, creates new file using current settings.
        If 'dryrun' is ON, prints messages but does not write to disk.
    """
    if os.path.exists(configfile_name):
        raise InitError(f"To re-initialize, first delete {repr(configfile_name)}.")
    else:
        if dryrun:
            raise InitError(
                f"In read-only mode. Would have created {repr(configfile_name)}.")
        else:
            print(f"Creating default {repr(configfile_name)}. Customize as needed.")
            with open(configfile_name, 'w') as fout:
                fout.write(yaml.safe_dump(settings_dict, default_flow_style=False))


def apply_overrides_from_file(builtinctx_dict=BUILTIN_MKLISTSRC,
                                    configfile_name=MKLISTSRC_NAME,
                                    verbose=False):
    """Returns settings dict of built-ins updated from config file.

    Reads mklists config file from disk:
    * Settings read from file may override some of the builtin settings.
    * Handles empty config file.
    * If config file is not found, exits, advises to run `mklists init`.

    Args:
        configfile_name: name of config file, by default '.mklistsrc'.
        builtinctx_dict: dictionary with setting name (key) and value.

    Returns:
        updatedctx_dict: updated settings dictionary
    """
    try:
        loadedctx_dict = yaml.load(open(configfile_name).read())
        if not loadedctx_dict:
            loadedctx_dict = dict()
        updatedctx_dict = _update_config(builtinctx_dict, loadedctx_dict)
        if verbose:
            print(f"Updated context from {repr(configfile_name)}.")
        return updatedctx_dict
    except FileNotFoundError:
        raise ConfigFileNotFoundError(f"First set up with `mklists init`.")


def _update_config(given_settings=None, new_settings=None):
    """Returns settings with some values overridden by new settings."""
    given_settings.update(new_settings)
    return given_settings


def write_initial_rulefiles(global_rulefile_name=BUILTIN_GRULEFILE_NAME, 
                            local_rulefile_name=BUILTIN_LRULEFILE_NAME, 
                            globalrules_content=BUILTIN_GRULES,
                            localrules_content=BUILTIN_LRULES,
                            dryrun=False,
                            verbose=False):
    """Generate default rule (and global rule) configuration files.

        Checks whether current settings name non-default rule files.
        If either rule file already exists, leaves untouched.
        Creates rule files with default contents.
        If 'dryrun' is ON, prints messages but does not write to disk.
    """
    for file, content in [(global_rulefile_name, globalrules_content), 
                          (local_rulefile_name, localrules_content)]:
        if file:
            if os.path.exists(file):
                print(f"Found existing {repr(file)} - leaving untouched.")
            else:
                if dryrun:
                    print(f"['dryrun' is on] "
                          "Would have created {repr(file)}.")
                else:
                    print(f"Creating starter rule file {repr(file)} "
                          "from built-in settings - can be customized.")
                    with open(file, 'w') as fout:
                        fout.write(content)

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
    before writing mklists_dict contents to disk, 
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
    # for file in filelist:
    #     shutil.move(file, backup_dir)

def write_new_datafiles(datalines_d=None,
                        dryrun=False,
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
                             dryrun=True,  # later: ctx.obj['dryrun'],
                             verbose=False):
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
