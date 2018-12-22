"""Utilities used by other modules"""


import os
import re
import glob
import yaml
import datetime
from mklists import (
    TIMESTAMP_STR,
    URL_PATTERN_REGEX,
    INVALID_FILENAME_PATTERNS,
    VALID_FILENAME_CHARACTERS_STR,
    BadYamlError,
    DatadirNotAccessibleError,
)


def get_timestamped_dirname_for_cwd():
    timestamp = TIMESTAMP_STR
    cwd_name = os.path.split(os.getcwd())[1]
    return "_".join([cwd_name, timestamp])


def keep_latest_x_list_values(some_list):
    """Maybe split into two functions:
    * Read dict, get key/values for 'mklists_2018...'
    * Keep just the last x number

    @@@Unfinished"""
    y = defaultdict(list)
    for item in some_list:
        y[item.split("_")[0]].append(item)


def read_yamlfile_to_pyobject(yamlfile_name):
    """Returns Python object parsed from given YAML-format file."""
    try:
        return yaml.safe_load(open(yamlfile_name))
    except yaml.YAMLError:
        raise BadYamlError(f"Bad YAML in {repr(yamlfile_name)}.")


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
    for bad_pat in INVALID_FILENAME_PATTERNS:
        if re.search(bad_pat, file_name):
            print(f"{repr(file_name)} matches bad pattern {repr(bad_pat)}.")
            return False
    for char in file_name:
        if char not in VALID_FILENAME_CHARACTERS_STR:
            print(f"{repr(file_name)} has invalid character {repr(char)}.")
            return False
    return True


def linkify(string):
    """Return string with URLs wrapped in A_HREF tags."""
    if "<a href=" in string:
        return string
    return re.compile(URL_PATTERN_REGEX).sub(r'<a href="\1">\1</a>', string)


def ls_visible(cwd=os.getcwd()):
    """Return list of visible files in given directory (default: '.')."""
    os.chdir(cwd)
    return [name for name in glob.glob("*")]
