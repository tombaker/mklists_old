"""Utilities used by other modules"""


import os
import re
import glob
import yaml
import datetime
from mklists import (
    URL_PATTERN_REGEX,
    INVALID_FILENAME_PATS,
    VALID_FILENAME_CHARS_STR,
    BadYamlError,
    DatadirNotAccessibleError,
    NotUTF8Error,
)


def get_timestamped_dirname_for_cwd():
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H%M_%S%f")
    cwd_name = os.path.split(os.getcwd())[1]
    return "_".join([cwd_name, timestamp])


def keep_latest_x_list_values(some_list):
    """Maybe split into two functions:
    * Read dict, get key/values for 'mklists_2018...'
    * Keep just the last x number

    @@@Unfinished
    """
    y = defaultdict(list)
    for item in some_list:
        y[item.split("_")[0]].append(item)


def read_yamlfile_return_pyobject(yamlfile_name):
    """Returns Python object parsed from YAML-format file."""
    try:
        return yaml.safe_load(open(yamlfile_name))
    except yaml.YAMLError:
        raise BadYamlError(f"Bad YAML format in {repr(yamlfile_name)}.")


def write_yamlstr_to_yamlfile(yamlfile_name, yamlstr):
    """Writes string in YAML format to file."""
    with open(yamlfile_name, "w") as fout:
        fout.write(yamlstr)


def is_file(object_path):
    """Returns True if object is a file."""
    if not os.path.isfile(object_path):
        return False
    return True


def has_valid_name(
    listfile_name,
    bad_patterns=INVALID_FILENAME_PATS,
    valid_chars=VALID_FILENAME_CHARS_STR,
):
    """Return True if filename has no invalid characters or patterns.

    Used to stop execution of mklists if data folder has files that
    should not be processed, such as temporary or backup files.
    """
    for bad_pattern in bad_patterns:
        if re.search(bad_pattern, listfile_name):
            print(
                f"Bad pattern {repr(bad_pattern)} "
                f"in filename {repr(listfile_name)}."
            )
            return False
    for char in listfile_name:
        if char not in valid_chars:
            print(f"{repr(char)} is not a valid filename character.")
            return False
    return True


def is_utf8_encoded(file_name):
    """Returns True if file is UTF8-encoded.

    Raises:
        NotUTF8Error: if file is not UTF8-encoded.
    """
    try:
        open(file_name).read()
    except UnicodeDecodeError:
        raise NotUTF8Error(f"{repr(file_name)} is not in UTF-8 format.")
    return True


def has_no_blank_lines(text_file):
    """Returns True if file has no blank lines.

    Note: Does not test whether text_file is a text file."""
    with open(text_file) as fin:
        for line in fin:
            if not line.rstrip():
                return False
    return True


def linkify(string_raw):
    """docstring"""
    if "<a href=" in string_raw:
        return string_raw
    return re.compile(URL_PATTERN_REGEX).sub(
        r'<a href="\1">\1</a>', string_raw
    )


def ls_visible(cwd=os.getcwd()):
    """Do I need to break this out into separate function?"""
    os.chdir(cwd)
    return [name for name in glob.glob("*")]
