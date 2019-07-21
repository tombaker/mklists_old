"""Utilities used by other modules"""

import datetime
import os
import re
import glob
import yaml
from .initialize import CONFIG_YAMLFILE_NAME, RULE_YAMLFILE_NAME
from .exceptions import BadFilenameError, BadYamlError, ConfigFileNotFoundError

BACKUPDIR_NAME = "_backups"
HTMLDIR_NAME = "_html"
INVALID_FILENAME_PATTERNS = [r"\.swp$", r"\.tmp$", r"~$", r"^\."]
TIMESTAMP_STR = datetime.datetime.now().strftime("%Y-%m-%d_%H%M_%S%f")
URL_PATTERN_REGEX = r"""((?:git://|http://|https://)[^ <>'"{}(),|\\^`[\]]*)"""
VALID_FILENAME_CHARACTERS_REGEX = r"[\-_=.,@:A-Za-z0-9]+$"


def get_datadir_shortname(datadir_pathname=os.getcwd(), rootdir_pathname=None):
    """See /Users/tbaker/github/tombaker/mklists/tests/test_utils_get_datadir_shortname_REDO.py
    @@@Redo this using os.path.basename"""
    return datadir_pathname[len(rootdir_pathname) :].strip("/").replace("/", "_")


def get_datadir_pathnames_under_cwd(rootdir_name="."):
    """Return list of all data directories under a given root directory.
    By definition, a data directory is a directory with a '.rules' file."""
    datadirs = []
    for (dirpath, __, filenames) in os.walk(rootdir_name):
        if RULE_YAMLFILE_NAME in filenames:
            datadirs.append(os.path.join(dirpath))
    return datadirs


def get_pyobj_from_yamlfile(yamlfile_name):
    """Returns Python object parsed from given YAML-format file."""
    try:
        yamlstr = open(yamlfile_name).read()
    except FileNotFoundError:
        raise ConfigFileNotFoundError(f"YAML file {repr(yamlfile_name)} not found.")

    try:
        return yaml.load(yamlstr)
    except yaml.YAMLError:
        raise BadYamlError(f"Badly formatted YAML in {repr(yamlfile_name)}.")


def get_rootdir_pathname(cwd=os.getcwd(), config_file_name=CONFIG_YAMLFILE_NAME):
    """Return repo root pathname when executed anywhere within repo.

    Args:

    See
    /Users/tbaker/github/tombaker/mklists/tests/test_utils_get_rootdir_pathname_REDO.py
    """
    os.chdir(cwd)
    while config_file_name not in os.listdir():
        cwd_before_changing = os.getcwd()
        os.chdir(os.pardir)
        if cwd_before_changing == os.getcwd():
            raise ConfigFileNotFoundError("No config file found - not a mklists repo.")
    else:
        return os.getcwd()


def ls_visible(datadir_name=os.getcwd()):
    """Return names of visible files with names that are valid as datafiles."""
    os.chdir(datadir_name)
    all_listfile_names = []
    for filename in [name for name in glob.glob("*") if os.path.isfile(name)]:
        if not has_valid_name(filename):
            raise BadFilenameError(f"{repr(filename)} has bad characters or patterns.")
        all_listfile_names.append(filename)
    return sorted(all_listfile_names)


def has_valid_name(filename, badpats=INVALID_FILENAME_PATTERNS):
    """Return True if filename has no invalid characters or string patterns.
    @@@Figure out how to pass in invalid filename patterns from context."""
    for badpat in badpats:
        if re.search(badpat, filename):
            return False
    for char in filename:
        if not bool(re.search(VALID_FILENAME_CHARACTERS_REGEX, char)):
            return False
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


def make_backupdir_name(now=TIMESTAMP_STR, datadir_name=None):
    """@@@Docstring"""
    return os.path.join(datadir_name, now)


def make_htmlstr_from_textstr(string):
    """Return string with URLs wrapped in A_HREF tags."""
    if "<a href=" in string:
        return string
    return re.compile(URL_PATTERN_REGEX).sub(r'<a href="\1">\1</a>', string)


def write_yamlstr_to_yamlfile(yamlstr, yamlfile_name):
    """Write YAML string to YAML file."""
    with open(yamlfile_name, "w") as fout:
        fout.write(yamlstr)
