"""Utilities used by other modules."""

import datetime
import os
import re
import glob
import yaml
from .constants import (
    HTMLDIR_NAME,
    INVALID_FILENAME_PATTERNS,
    URL_PATTERN_REGEX,
    VALID_FILENAME_CHARACTERS_REGEX,
)
from .decorators import preserve_cwd
from .initialize import CONFIG_YAMLFILE_NAME, RULE_YAMLFILE_NAME
from .exceptions import (
    BadFilenameError,
    BadYamlError,
    ConfigFileNotFoundError,
    FilenameIsAlreadyDirnameError,
)


def return_datadir_pathnames_under_somedir(
    somedir_pathname=None, rulefile_name=RULE_YAMLFILE_NAME
):
    """Return list of data directories under a given directory.

    "Data directories": directories with rules files (by default: '.rules').

    Args:
        :somedir_pathname: Root of directory tree with data directories.
        :rulefile_name: Name of rule file (by default: '.rules').

    2019-07-22: Two scenarios?
    * mklists run         - runs in all data directories in repo
    * mklists run --here  - runs just in current directory
    """
    if not somedir_pathname:
        somedir_pathname = os.getcwd()
    datadirs = []
    for dirpath, dirs, files in os.walk(somedir_pathname):
        dirs[:] = [d for d in dirs if not d[0] == "."]
        if rulefile_name in files:
            datadirs.append(dirpath)
    return datadirs


def return_pyobj_from_config_yamlfile(yamlfile_name=None):
    """Returns Python object parsed from given YAML-format file."""
    try:
        yamlstr = open(yamlfile_name).read()
    except FileNotFoundError:
        raise ConfigFileNotFoundError(f"YAML file {repr(yamlfile_name)} not found.")

    try:
        return yaml.load(yamlstr)
    except yaml.YAMLError:
        raise BadYamlError(f"Badly formatted YAML in {repr(yamlfile_name)}.")


@preserve_cwd
def return_rootdir_pathname(cwd=None, configfile_name=CONFIG_YAMLFILE_NAME):
    """Return repo root pathname when executed anywhere within repo.

    Args:

    See
    /Users/tbaker/github/tombaker/mklists/tests/test_utils_return_rootdir_pathname_DONE.py
    """
    if not cwd:
        cwd = os.getcwd()
    while configfile_name not in os.listdir():
        cwd_before_changing = os.getcwd()
        os.chdir(os.pardir)
        if os.getcwd() == cwd_before_changing:
            raise ConfigFileNotFoundError("No config file found - not a mklists repo.")
    else:
        return os.getcwd()


@preserve_cwd
def return_rulefile_chain(
    start_pathname=None,
    rulefile_name=RULE_YAMLFILE_NAME,
    configfile_name=CONFIG_YAMLFILE_NAME,
):
    """Return list of rule files from parent directories and current directory.

    Looks no higher than root directory of mklists repo.

    Args:
        :start_pathname:
        :rulefile_name:
        :configfile_name:
    """
    if not start_pathname:
        start_pathname = os.getcwd()
    os.chdir(start_pathname)
    rulefile_pathnames_chain = []
    while rulefile_name in os.listdir():
        rulefile_pathnames_chain.insert(0, os.path.join(os.getcwd(), rulefile_name))
        if configfile_name in os.listdir():
            break
        os.chdir(os.pardir)

    return rulefile_pathnames_chain


@preserve_cwd
def ls_visiblefiles(datadir_name=None):
    """Return list of names of visible files with valid names.

    See /Users/tbaker/github/tombaker/mklists/mklists/utils.py
    """
    if not datadir_name:
        datadir_name = os.getcwd()
    os.chdir(datadir_name)
    all_listfile_names = []
    for filename in [name for name in glob.glob("*") if os.path.isfile(name)]:
        try:
            is_valid_as_filename(filename)
        finally:
            all_listfile_names.append(filename)
    return sorted(all_listfile_names)


def is_valid_as_filename(
    filename=None,
    current_dir=None,
    badpats=INVALID_FILENAME_PATTERNS,
    validchars_regex=VALID_FILENAME_CHARACTERS_REGEX,
):
    """Return True if filename:
    * has no invalid characters (override defaults in mklists.yml)
    * string patterns (override defaults in mklists.yml)
    * does not match name of an existing directory in current_dir

    """
    if not current_dir:
        current_dir = os.getcwd()
    for badpat in badpats:
        if re.search(badpat, filename):
            return False
    for char in filename:
        if not bool(re.search(validchars_regex, char)):
            return False
    if filename in [d for d in os.listdir() if os.path.isdir(d)]:
        raise FilenameIsAlreadyDirnameError(
            f"Filename {repr(filename)} is already used as a directory name."
        )
    return True


def is_line_match_to_rule(given_rule=None, given_line=None):
    """Returns True if data line matches pattern specified in given rule."""

    # Line does not match if given field greater than number of fields in line.
    if given_rule.source_matchfield > len(given_line.split()):
        return False

    # Line matches if given field is zero and pattern found anywhere in line.
    if given_rule.source_matchfield == 0:
        if re.search(given_rule.source_matchpattern, given_line):
            return True

    # Line matches if pattern is found in given field.
    if given_rule.source_matchfield > 0:
        eth = given_rule.source_matchfield - 1
        if re.search(given_rule.source_matchpattern, given_line.split()[eth]):
            return True

    return False


def make_htmlstr_from_textstr(string=None):
    """Return string with URLs wrapped in A_HREF tags."""
    if "<a href=" in string:
        return string
    return re.compile(URL_PATTERN_REGEX).sub(r'<a href="\1">\1</a>', string)


def write_yamlstr_to_yamlfile(yamlstr=None, yamlfile_name=None):
    """Write YAML string to YAML file."""
    with open(yamlfile_name, "w") as fout:
        fout.write(yamlstr)
