"""Factory to create, self-test, and lightly correct a rule object."""

import os
from dataclasses import dataclass
from .booleans import filename_is_valid_as_filename, regex_is_valid_as_regex
from .constants import CONFIG_YAMLFILE_NAME, RULE_YAMLFILE_NAME
from .decorators import preserve_cwd
from .exceptions import (
    BadFilenameError,
    BadYamlRuleError,
    NoRulesError,
    NotIntegerError,
    RulefileNotFoundError,
    SourceEqualsTargetError,
    SourceMatchpatternError,
    UninitializedSourceError,
)
from .utils import return_pyobj_from_yamlstr, return_yamlstr_from_yamlfile


@dataclass
class Rule:
    """Holds state and self-validation methods for a single rule.

    Fields:
        source_matchfield: data line field to be matched to source_matchpattern.
        source_matchpattern: regex matched to source_matchfield.
        source: filename of source of data lines to be matched to source_matchpattern.
        target: filename of destination of data lines that match source_matchpattern.
        target_sortorder: field on which target data lines are sorted.
    """

    source_matchfield: int = None
    source_matchpattern: str = None
    source: str = None
    target: str = None
    target_sortorder: int = 0

    sources_list_is_initialized = False
    sources_list = []

    def is_valid(self):
        """Return True if Rule object passes all tests."""
        self._number_fields_are_integers()
        self._source_matchpattern_is_valid()
        self._filenames_are_valid()
        self._source_is_not_equal_target()
        self._source_is_initialized_as_source()
        return True

    def _number_fields_are_integers(self):
        """Return True if source_matchfield, target_sortorder are integers."""
        for field in [self.source_matchfield, self.target_sortorder]:
            if not isinstance(field, int):
                print(f"In {self}:")
                raise NotIntegerError(f"{repr(field)} must be an integer.")
        return True

    def _source_matchpattern_is_valid(self):
        """Returns True if source_matchpattern is valid regular expression."""
        if not regex_is_valid_as_regex(self.source_matchpattern):
            print(f"source_matchpattern in rule: {self}")
            raise SourceMatchpatternError("is not valid a valid regex.")
        return True

    def _filenames_are_valid(self):
        """Returns True if filenames use only valid characters."""
        for filename in [self.source, self.target]:
            if not filename_is_valid_as_filename(filename):
                print(f"{repr(filename)} in rule: {self}")
                raise BadFilenameError("is not a valid filename.")
        return True

    def _source_is_not_equal_target(self):
        """Returns True if source is not equal to target."""
        if self.source == self.target:
            raise SourceEqualsTargetError("source must not equal target.")
        return True

    def _source_is_initialized_as_source(self):
        """Returns True if 'source' filename was initialized as a source."""
        if not Rule.sources_list_is_initialized:
            Rule.sources_list.append(self.source)
            Rule.sources_list_is_initialized = True
        if self.source not in Rule.sources_list:
            print(f"In rule: {self}")
            print(f"Rule.sources_list = {Rule.sources_list}")
            raise UninitializedSourceError(f"{repr(self.source)} not initialized.")
        if self.target not in Rule.sources_list:
            Rule.sources_list.append(self.target)
        return True


@preserve_cwd
def return_rulefile_pathnames_chain_as_list(
    _startdir_pathname=None,
    _rule_yamlfile_name=RULE_YAMLFILE_NAME,
    _config_yamlfile_name=CONFIG_YAMLFILE_NAME,
):
    """Return chain of rule files leading from parent directories
    to starting directory (by default the current directory).

    Looks no higher than the root directory of a mklists repo, i.e., the
    directory with a YAML configuration file (by default "mklists.yml").

    Args:
        _startdir_pathname:
        _rule_yamlfile_name:
        _config_yamlfile_name:
    """
    if not _startdir_pathname:
        _startdir_pathname = os.getcwd()
    os.chdir(_startdir_pathname)
    rulefile_pathnames_chain = []
    while _rule_yamlfile_name in os.listdir():
        rulefile_pathnames_chain.insert(
            0, os.path.join(os.getcwd(), _rule_yamlfile_name)
        )
        if _config_yamlfile_name in os.listdir():
            break
        os.chdir(os.pardir)

    return rulefile_pathnames_chain


def return_consolidated_yamlstr_from_rulefile_chain(_rulefile_pathnames_chain=None):
    """Return list of rule strings from chain of rulefile pathnames."""

    rulestring_list = []
    for pathname in _rulefile_pathnames_chain:
        for line in open(pathname).splitlines():
            rulestring_list.extend(line)
    if not rulestring_list:
        raise NoRulesError("No rules were found.")

    return rulestring_list


def return_ruleobj_list_from_consolidate_yamlstr(_split_rulestring_list=None):
    """Return list of rule objects from list of rule strings."""
    ruleobj_list = []
    for line in _split_rulestring_list:
        try:
            Rule(*line).is_valid
        except TypeError:
            raise BadYamlRuleError(f"Rule {repr(line)} is badly formed.")
        ruleobj_list.append(Rule(*line))

    if not ruleobj_list:
        raise NoRulesError(f"No rules found.")

    return ruleobj_list
