"""Marks mklists package directory, sets constants."""

import datetime

TIMESTAMP = datetime.datetime.now().strftime("%Y-%m-%d_%H%M%S_%f")

VALID_FILENAME_CHARS = """\
:@-_=.abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"""

MKLISTSRC = '.mklistsrc'

RULEFILE = '.rules'

STARTER_DEFAULTS = {
    'globalrules': '.globalrules',
    'rules': '.rules',
    'urlify': False,
    'urlify_dir': '.urlified',
    'backup': False,
    'backup_dir': '.backups',
    'backup_depth': 3,
    'readonly': False,
    'verbose': False,
    'valid_filename_characters': VALID_FILENAME_CHARS,
    'invalid_filename_patterns': [r'\.swp$', r'\.tmp$', r'~$', r'^\.'],
    'files2dirs': None}

STARTER_GRULES = """\
- [0,  '.',         lines,         todo.txt,   0]  # notes...
"""

STARTER_LRULES = """\
- [1,  'NOW',       todo.txt,      now.txt,    0]  # notes...
- [1,  'LATER',     todo.txt,      later.txt,  0]  # notes...
"""

# Errors related to configuration, used in cli module
class ConfigError(SystemExit):
    """Category of errors related to configuration"""

class ConfigFileNotFoundError(ConfigError):
    """Hardwired configuration file '.mklistsrc' was not found"""
    
class DatadirNotAccessibleError(ConfigError):
    """Non-default data directory is not accessible"""
    
class InitError(ConfigError):
    """Data directory has already been initialized"""

class NoRulefileSpecified(ConfigError):
    """Configuration does not even specify a rule file."""

# Errors related to data directory, used in datadir module
class DataError(SystemExit):
    """Superclass for errors relating to data."""

class BadFilenameError(DataError):
    """Filename is bad (ie, matches a blacklisted pattern)."""

class BlankLinesError(DataError):
    """File contains blank lines."""

class DatadirHasNonFilesError(DataError):
    """Data directory has visible non-file objects (eg, links, directories."""

class NoDataError(DataError):
    """There is no data to process."""

class NotUTF8Error(DataError):
    """File is not UTF8-encoded."""

# Errors related to an individual rule, used in rule module
class RuleError(SystemExit):
    """Super-category for exceptions related to rules."""

class NotIntegerError(RuleError):
    """Value is not an integer."""

class BadFilenameError(RuleError):
    """Filename uses character not in list of valid characters."""

class SourceEqualsTargetError(RuleError):
    """Source equals target."""

class SourceMatchpatternError(RuleError):
    """Match pattern does not compile correctly as a regular expression."""

class BadSourceError(RuleError):
    """Source has not been initialized as a source (has no precedent)."""

# Errors related to a set of rules, used in rules module
class RulesError(SystemExit):
    """Category of exceptions related to sets or rules."""

class BadYamlRuleError(RulesError):
    """Rule is badly formed in YAML source."""

class BadYamlError(RulesError):
    """YAML format of the file does not parse correctly."""

class RuleWarningError(Exception):
    """Super-category for warnings related to rules."""

class RuleFileNotFoundError(RuleWarningError):
    """Rule file not found or not accessible."""
