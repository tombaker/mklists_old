import os
import re
import string
import sys
import pprint
import yaml
from mklists import (
    GLOBAL_RULEFILE_NAME,
    GLOBAL_RULEFILE_STARTER_YAMLSTR,
    LOCAL_RULEFILE_NAME,
    LOCAL_RULEFILE_STARTER_YAMLSTR,
    MKLISTSRC_STARTER_DICT,
    MKLISTSRC_LOCAL_NAME,
    TIMESTAMP_STR,
    URL_PATTERN_REGEX,
    VALID_FILENAME_CHARS_STR,
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


def apply_overrides(settings_dict, overrides):
    """docstring"""
    overrides.pop("ctx", None)
    overrides = {
        key: overrides[key] for key in overrides if overrides[key] is not None
    }
    settings_dict.update(overrides)
    return settings_dict
