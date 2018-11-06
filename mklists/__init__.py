"""Marks mklists package directory, sets constants."""

import datetime

TIMESTAMP = datetime.datetime.now().strftime("%Y-%m-%d_%H%M%S_%f")

# 2018-11-05: Does it make a difference if this is a raw string?
URL_PATTERN = """((?:git://|http://|https://)[^ <>'"{}(),|\\^`[\]]*)"""

VALID_FILENAME_CHARS = """\
:@-_=.abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"""

INVALID_FILENAME_PATS = [r"\.swp$", r"\.tmp$", r"~$", r"^\."]

BACKUP_DIR_NAME = ".backups"

HTMLFILES_DIR_NAME = ".html"

MKLISTSRC_GLOBAL_NAME = "mklistsrc"
MKLISTSRC_LOCAL_NAME = ".mklistsrc"
# Do I need to turn this into a YAML string as well?
MKLISTSRC_STARTER_DICT = {
    "urlify": False,
    "backup_depth": 3,
    "verbose": False,
    "valid_filename_characters": VALID_FILENAME_CHARS,
    "invalid_filename_patterns": INVALID_FILENAME_PATS,
    "files2dirs": {},
}


GLOBAL_RULEFILE_NAME = ".globalrules"
GLOBAL_RULEFILE_STARTER_YAMLSTRING = """\
- [0,  '.',         lines,         todo.txt,   0]  # notes...
"""


LOCAL_RULEFILE_NAME = ".rules"
LOCAL_RULEFILE_STARTER_YAMLSTRING = """\
- [1,  'NOW',       todo.txt,      now.txt,    0]  # notes...
- [1,  'LATER',     todo.txt,      later.txt,  0]  # notes...
"""


class ConfigError(SystemExit):
    """Category of errors related to configuration"""


class ConfigFileNotFoundError(ConfigError):
    """Hardwired configuration file '.mklistsrc' was not found"""


class DatadirNotAccessibleError(ConfigError):
    """Non-default data directory is not accessible"""


class InitError(ConfigError):
    """Data directory has already been initialized"""


class RulefileNotFoundError(ConfigError):
    """Rule file was not found."""


# Errors related to data directory, used in datadir module
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


class RuleError(SystemExit):
    """Super-category for exceptions related to rules."""


class NotIntegerError(RuleError):
    """Value is not an integer."""


class BadFilenameError(RuleError, DataError):
    """Filename uses invalid characters or name patterns."""


class BadFileFormatError(DataError):
    """File is not in UTF-8 format."""


class SourceEqualsTargetError(RuleError):
    """Source equals target."""


class SourceMatchpatternError(RuleError):
    """Match pattern does not compile correctly as a regular expression."""


class UninitializedSourceError(RuleError):
    """Source has not been initialized as a source (has no precedent)."""


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


class RuleWarningError(Exception):
    """Super-category for warnings related to rules."""
