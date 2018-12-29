"""Defines Mklists constants and exception classes."""

import datetime
import os

TIMESTAMP_STR = datetime.datetime.now().strftime("%Y-%m-%d_%H%M_%S%f")
URL_PATTERN_REGEX = """((?:git://|http://|https://)[^ <>'"{}(),|\\^`[\]]*)"""
VALID_FILENAME_CHARACTERS_STR = """\
:@-_=.abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"""
INVALID_FILENAME_PATTERNS = [r"\.swp$", r"\.tmp$", r"~$", r"^\."]

# 2018-11-12: Cannot just save string - must do:
# fout.write(yaml.safe_dump(settings_dict, default_flow_style=False))
# See /Users/tbaker/github/tombaker/mklists/mklists/cli_init.py
MKLISTS_YML_NAME = "mklists.yml"  # only in root directory
MKLISTS_YML_STARTER_DICT = {
    "html": False,
    "backups": 3,
    "verbose": False,
    "valid_filename_characters": VALID_FILENAME_CHARACTERS_STR,
    "invalid_filename_patterns": INVALID_FILENAME_PATTERNS,
    "files2dirs": {},
}

MKLISTSYML_YAMLSTR = """\
backups: 3
files2dirs: {}
html: false
invalid_filename_patterns: [\\.swp$, \\.tmp$, ~$, ^\\.]
valid_filename_characters: :@-_=.abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789
verbose: false
global_rules:
- [0, '.',        all_lines, lines,    0]
- [0, '^=',       all_lines, to_a.txt, 1]
- [0, '^201[89]', all_lines, to_b.txt, 1]
"""

GLOBAL_DIR = "."

LOCAL_DIR = os.path.join(GLOBAL_DIR, "lists")
LOCAL_RULEFILE_NAME = ".localrules"
RULEFILE_NAME = ".localrules"

RULEFILE_STARTER_YAMLSTR = """\
- [0, '.',       lines,      todo.txt,   0]
- [0, '.',       to_a.txt    todo.txt,   1]
- [1, 'NOW',     todo.txt,    now.txt,   1]
- [1, 'LATER',   todo.txt,  later.txt,   0]
"""

BACKUP_DIR_NAME = "backups"
HTMLFILES_DIR_NAME = "html"


# ConfigError
class ConfigError(SystemExit):
    """Category of errors related to configuration."""


class ConfigFileNotFoundError(ConfigError):
    """Hardwired configuration file 'mklists.yml' was not found."""


class DatadirNotAccessibleError(ConfigError):
    """Non-default data directory is not accessible."""


class InitError(ConfigError):
    """Data directory has already been initialized."""


class RulefileNotFoundError(ConfigError):
    """Rule file was not found."""


# DataError
class DataError(SystemExit):
    """Superclass for errors relating to data."""


class BlankLinesError(DataError):
    """File contains blank lines."""


class DatadirHasNonFilesError(DataError):
    """Data directory has visible non-file objects (eg, links, directories."""


class NoDataError(DataError):
    """There is no data to process."""


class NotUTF8Error(DataError):
    """File is not UTF8-encoded."""


class NotUTF8Error(DataError):
    """File is not in UTF-8 format."""


# RuleError
class RuleError(SystemExit):
    """Super-category for exceptions related to rules."""


class NotIntegerError(RuleError):
    """Value is not an integer."""


class BadFilenameError(RuleError, DataError):
    """Filename uses invalid characters or name patterns."""


class SourceEqualsTargetError(RuleError):
    """Source equals target."""


class SourceMatchpatternError(RuleError):
    """Match pattern does not compile correctly as a regular expression."""


class UninitializedSourceError(RuleError):
    """Source has not been initialized as a source (has no precedent)."""


# RulesError
class RulesError(SystemExit):
    """Category of exceptions related to sets or rules."""


class BadYamlRuleError(RulesError):
    """Rule is badly formed in YAML source."""


class NoRulefileError(RulesError):
    """Rule file not found or not accessible."""


class NoRulesError(RulesError):
    """No rules to process."""


class BadYamlError(RulesError):
    """File contains badly formatted YAML."""
