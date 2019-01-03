"""Utilities used by other modules"""


import os
import re
import glob
import yaml
from mklists import (
    CONFIGFILE_NAME,
    LOCAL_RULEFILE_NAME,
    RULEFILE_NAME,
    TIMESTAMP_STR,
    URL_PATTERN_REGEX,
    VALID_FILENAME_CHARACTERS_REGEX,
    BadYamlError,
    ConfigFileNotFoundError,
)


def find_project_root(path="."):
    """Return project root path when executed in root or data directory."""
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
        raise ConfigFileNotFoundError(
            f"{CONFIGFILE_NAME} not found. Was project initialized?"
        )


def generate_timestamped_backupdir_name(now=TIMESTAMP_STR, here=os.getcwd()):
    """@@@Docstring"""
    return os.path.join(here, now)


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


# Structure will be:
# _backups/a/2018-12-31
# _backups/a/2019-01-01
# _backups/b/...


def write_yamlstr_to_yamlfile(yamlfile_name, yamlstr):
    """Write YAML string to YAML file."""
    with open(yamlfile_name, "w") as fout:
        fout.write(yamlstr)


def is_file(object_path):
    """Return True if object is a file."""
    if not os.path.isfile(object_path):
        return False
    return True


def has_valid_name(file_name):
    """Return True if filename has no invalid characters or string patterns."""
    # for bad_pat in INVALID_FILENAME_PATTERNS:
    #    if re.search(bad_pat, file_name):
    #        print(f"{repr(file_name)} matches bad pattern {repr(bad_pat)}.")
    #        return False
    for char in file_name:
        if not bool(re.search(VALID_FILENAME_CHARACTERS_REGEX, char)):
            print(f"{repr(file_name)} has invalid character {repr(char)}.")
            return False
    return True


def ls_visible_files(cwd=os.getcwd()):
    """Return list of visible files in given directory (default: '.')."""
    os.chdir(cwd)
    return [name for name in glob.glob("*") if os.path.isfile(name)]
