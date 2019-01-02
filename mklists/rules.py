"""Factory to create, self-test, and lightly correct a rule object."""

import re
from dataclasses import dataclass
from mklists.utils import has_valid_name, read_yamlfile_to_pyobject
from mklists import (
    NotIntegerError,
    BadFilenameError,
    SourceEqualsTargetError,
    SourceMatchpatternError,
    UninitializedSourceError,
)


@dataclass
class Rule:
    """Holds state and self-validation methods for a single rule.

    Fields:
        source_matchfield: part of data line matched to source_matchpattern.
        source_matchpattern: regex matched to part of source_matchfield.
        source: source of data lines to be matched against source_matchpattern.
        target: destination of data lines matching source_matchpattern.
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
        self._source_not_initialized_as_source()
        return True

    def _number_fields_are_integers(self):
        """Return True if source_matchfield, target_sortorder are integers."""
        for field in [self.source_matchfield, self.target_sortorder]:
            try:
                field = int(field)
            except TypeError:
                print(f"In rule: {self}")
                raise NotIntegerError(f"{field} must be an integer.")
        return True

    def _source_matchpattern_is_valid(self):
        """Returns True if source_matchpattern is valid regular expression."""
        try:
            re.compile(self.source_matchpattern)
        except re.error:
            print(f"source_matchpattern in rule: {self}")
            raise SourceMatchpatternError("is not valid a valid regex.")
        return True

    def _filenames_are_valid(self):
        """Returns True if filenames use only valid characters."""
        for filename in [self.source, self.target]:
            if not has_valid_name(filename):
                print(f"{repr(filename)} in rule: {self}")
                raise BadFilenameError("is not a valid filename.")
        return True

    def _source_is_not_equal_target(self):
        """Returns True if source is not equal to target."""
        if self.source == self.target:
            raise SourceEqualsTargetError("source must not equal target.")
        return True

    def _source_not_initialized_as_source(self):
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


def find_rulefiles():
    """
    Repository
    mydir/mklists.yaml - configuration
    mydir/.globalrules - global rules
    mydir/a/.rules     - list A rules
    mydir/b/.rules     - list B rules

    Rule- and config-finding algorithm:
    a. Look for mklists.yaml
       * in current directory, then
       * in parent directory
    b. When mklists.yaml found (i.e., in root directory)
       * look in root directory for (optional) .globalrules
       * look under all subdirectories for .rules files"""


def get_rules(valid_filename_chars, invalid_filename_patterns):
    """Find and load YAML rulefiles, returning Python list of rule objects."""

    # aggregated_rules_list = []
    # for rulefile_name in RULEFILE_NAME, LOCAL_RULEFILE_NAME:
    #     if rulefile_name:
    #         rules_list = read_yamlfile_to_pyobject(rulefile_name)
    #         aggregated_rules_list = aggregated_rules_list + rules_list

    ruleobj_list = []
    # for item in aggregated_rules_list:
    #    try:
    #        Rule(*item).is_valid
    #    except TypeError:
    #        raise BadYamlRuleError(f"Rule {repr(item)} is badly formed.")
    #    ruleobj_list.append(Rule(*item))

    return ruleobj_list


def get_rules2():
    rules_list = []
    try:
        rules_to_add = read_yamlfile_to_pyobject()
        rules_list.append(rules_to_add)
    except FileNotFoundError:
        print("File was not found")
    except TypeError:
        print("NoneType")
    return rules_list
