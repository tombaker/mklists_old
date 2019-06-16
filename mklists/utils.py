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


def get_cwd_basename(listdir=os.getcwd(), rootdir=None):
    """@@@Redo this using os.path.basename"""
    return listdir[len(rootdir) :].strip("/").replace("/", "_")


def get_listdir_pathnames_under_cwd(rootdir_name="."):
    """Return list of all data directories under a given root directory.
    By definition, a data directory is a directory with a '.rules' file."""
    listdirs = []
    for (dirpath, __, filenames) in os.walk(rootdir_name):
        if RULE_YAMLFILE_NAME in filenames:
            listdirs.append(os.path.join(dirpath))
    return listdirs


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


def get_rootdir_pathname(here="."):
    """Return project rootdir when executed in the rootdir or in a listdir."""
    os.chdir(here)
    while True:
        ls_cwd = os.listdir()
        if RULE_YAMLFILE_NAME in ls_cwd:
            os.chdir(os.pardir)
            continue
        else:
            break

    if CONFIG_YAMLFILE_NAME in os.listdir():
        return os.getcwd()
    else:
        raise ConfigFileNotFoundError(
            f"No {CONFIG_YAMLFILE_NAME} found. Try mklists init."
        )


def get_visiblefile_names_in_listdir(listdir_name=os.getcwd()):
    """Return names of visible files with names that are valid as listfiles."""
    os.chdir(listdir_name)
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


def make_backupdir_name(now=TIMESTAMP_STR, listdir_name=None):
    """@@@Docstring"""
    return os.path.join(listdir_name, now)


def make_htmlstr_from_textstr(string):
    """Return string with URLs wrapped in A_HREF tags."""
    if "<a href=" in string:
        return string
    return re.compile(URL_PATTERN_REGEX).sub(r'<a href="\1">\1</a>', string)


def update_config_dict_from_config_yamlfile(config_dict=None, overrides=None):
    """Inject dictionary B into A, ignoring keys in B with value None."""
    overrides = {key: overrides[key] for key in overrides if overrides[key] is not None}
    config_dict.update(overrides)
    return config_dict


def write_yamlstr_to_yamlfile(yamlstr, yamlfile_name):
    """Write YAML string to YAML file."""
    with open(yamlfile_name, "w") as fout:
        fout.write(yamlstr)
