"""Exception classes for mklists."""


# ConfigError
class ConfigError(SystemExit):
    """Category of errors related to configuration."""


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


class FilenameIsAlreadyDirnameError(RuleError):
    """Filename is already being used as a directory name."""


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
