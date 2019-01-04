"""Utilities used by other modules"""


import os
import re
import glob
import yaml
from mklists import (
    CONFIGFILE_NAME,
    LOCAL_RULEFILE_NAME,
    INVALID_FILENAME_PATTERNS,
    RULEFILE_NAME,
    TIMESTAMP_STR,
    URL_PATTERN_REGEX,
    VALID_FILENAME_CHARACTERS_REGEX,
    BadYamlError,
    ConfigFileNotFoundError,
)


def find_datadirs_under_project_rootdir(rootdir="."):
    """Return list of all data directories under a given root directory.
    By definition, a data directory is a directory with either a
    '.rules' or '.localrules' file."""
    datadirs = []
    for (dirpath, dirs, files) in os.walk(rootdir):
        if (RULEFILE_NAME in files) or (LOCAL_RULEFILE_NAME in files):
            datadirs.append(os.path.join(dirpath))
    return datadirs


def find_project_rootdir(path="."):
    """Return project rootdir when executed in the rootdir or in a datadir."""
    os.chdir(path)
    while True:
        ls_cwd = os.listdir()
        if RULEFILE_NAME in ls_cwd:
            os.chdir(os.pardir)
            continue
        elif LOCAL_RULEFILE_NAME in ls_cwd:
            os.chdir(os.pardir)
        else:
            break

    if CONFIGFILE_NAME in os.listdir():
        return os.getcwd()
    else:
        raise ConfigFileNotFoundError(f"No {CONFIGFILE_NAME} found. Try mklists init.")


def generate_timestamped_backupdir_name(now=TIMESTAMP_STR, here=os.getcwd()):
    """@@@Docstring"""
    return os.path.join(here, now)


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


def linkify(string):
    """Return string with URLs wrapped in A_HREF tags."""
    if "<a href=" in string:
        return string
    return re.compile(URL_PATTERN_REGEX).sub(r'<a href="\1">\1</a>', string)


def read_yaml_configfile_to_pyobject(yamlfile_name):
    """Returns Python object parsed from given YAML-format file."""
    try:
        return yaml.safe_load(open(yamlfile_name))
    except yaml.YAMLError:
        raise BadYamlError(f"Badly formatted YAML in {repr(yamlfile_name)}.")
    except FileNotFoundError:
        raise ConfigFileNotFoundError(f"YAML file {repr(yamlfile_name)} not found.")


def update_settings_dict(settings_dict=None, overrides=None):
    """Inject dictionary B into A, ignoring keys in B with value None."""
    overrides = {key: overrides[key] for key in overrides if overrides[key] is not None}
    settings_dict.update(overrides)
    return settings_dict


def write_yamlstr_to_yamlfile(yamlfile_name, yamlstr):
    """Write YAML string to YAML file."""
    with open(yamlfile_name, "w") as fout:
        fout.write(yamlstr)


def ls_visible_files(cwd=os.getcwd()):
    """Return list of visible files in given directory (default: '.')."""
    os.chdir(cwd)
    return [name for name in glob.glob("*") if os.path.isfile(name)]


# Structure will be:
# _backups/a/2018-12-31
# _backups/a/2019-01-01
# _backups/b/...
