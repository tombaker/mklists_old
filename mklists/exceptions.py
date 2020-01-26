"""Exception classes for mklists."""


# General errors
class BadRegexError(SystemExit):
    """String does not compile as regular expression."""


class MissingArgumentError(SystemExit):
    """Function or argument is missing an argument."""


class MissingValueError(SystemExit):
    """Function or argument is missing a value."""


class RepoAlreadyInitialized(SystemExit):
    """Mklists repo has already been initialized."""


class NoBackupDirSpecifiedError(SystemExit):
    """No pathname for backup directory was specified."""


class RepoNotFoundError(SystemExit):
    """No mklists repo was found (eg, no "mklists.yml")."""


# ConfigError
class ConfigError(SystemExit):
    """Category of errors related to configuration."""


class BackupDepthUnspecifiedError(ConfigError):
    """Number of backups to keep is unspecified."""


class ConfigFileNotFoundError(ConfigError):
    """Hardwired configuration file 'mklists.yml' was not found."""


class ListdirNotAccessibleError(ConfigError):
    """Non-default data directory is not accessible.  @@@Is this even used?"""


class InitError(ConfigError):
    """Data directory has already been initialized."""


class RulefileNotFoundError(ConfigError):
    """Rule file was not found."""


# DataError
class DataError(SystemExit):
    """Superclass for errors relating to data."""


class BlankLinesError(DataError):
    """File contains blank lines."""


class NoDataError(DataError):
    """There is no data to process."""


class NotUTF8Error(DataError):
    """File is not UTF8-encoded."""


# RuleError
class RuleError(SystemExit):
    """Super-category for exceptions related to individual rules."""


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


class FilenameIsAlreadyDirnameError(RuleError):
    """Filename is already being used as a directory name."""


# RulesError
class RulesError(SystemExit):
    """Super-category for exceptions related to sets of rules."""


class BadRuleError(RulesError):
    """Rule is badly formed in YAML source."""


class NoRulefileError(RulesError):
    """Rule file not found or not accessible."""


class NoRulesError(RulesError):
    """No rules to process."""


class BadYamlError(RulesError):
    """File contains badly formatted YAML."""
