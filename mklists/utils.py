"""Utilities used by other modules"""

import os
import re
import glob
import yaml
from .constants import (
    CONFIG_YAMLFILE_NAME,
    INVALID_FILENAME_PATTERNS,
    RULE_YAMLFILE_NAME,
    TIMESTAMP_STR,
    URL_PATTERN_REGEX,
    VALID_FILENAME_CHARACTERS_REGEX,
)
from .exceptions import BadFilenameError, BadYamlError, ConfigFileNotFoundError


def make_backupdir_name(now=TIMESTAMP_STR, listdir_name=None):
    """@@@Docstring"""
    return os.path.join(listdir_name, now)


def make_htmlstr_from_textstr(string):
    """Return string with URLs wrapped in A_HREF tags."""
    if "<a href=" in string:
        return string
    return re.compile(URL_PATTERN_REGEX).sub(r'<a href="\1">\1</a>', string)


def get_listdir_names_under_rootdir(rootdir_name="."):
    """Return list of all data directories under a given root directory.
    By definition, a data directory is a directory with a '.rules' file."""
    listdirs = []
    for (dirpath, __, filenames) in os.walk(rootdir_name):
        if RULE_YAMLFILE_NAME in filenames:
            listdirs.append(os.path.join(dirpath))
    return listdirs


def get_listdir_shortname(listdir=os.getcwd(), rootdir=None):
    return listdir[len(rootdir) :].strip("/").replace("/", "_")


def get_listfile_names(listdir_name=os.getcwd()):
    """Return names of visible files with names that are valid as listfiles."""
    os.chdir(listdir_name)
    all_listfile_names = []
    for filename in [name for name in glob.glob("*") if os.path.isfile(name)]:
        if not has_valid_name(filename):
            raise BadFilenameError(f"{repr(filename)} has bad characters or patterns.")
        all_listfile_names.append(filename)
    return all_listfile_names


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


def get_rootdir_name(path="."):
    """Return project rootdir when executed in the rootdir or in a listdir."""
    os.chdir(path)
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


def update_settings_dict_from_config_yamlfile(settings_dict=None, overrides=None):
    """Inject dictionary B into A, ignoring keys in B with value None."""
    overrides = {key: overrides[key] for key in overrides if overrides[key] is not None}
    settings_dict.update(overrides)
    return settings_dict


def write_yamlstr_to_yamlfile(yamlstr, yamlfile_name):
    """Write YAML string to YAML file."""
    with open(yamlfile_name, "w") as fout:
        fout.write(yamlstr)
