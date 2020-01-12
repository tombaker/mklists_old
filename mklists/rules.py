"""Factory to create, self-test, and lightly correct a rule object."""

import os
from dataclasses import dataclass
from .booleans import filename_is_valid_as_filename, regex_is_valid_as_regex

# @@@@ Defaults x 2
from .config import Defaults
from .decorators import preserve_cwd
from .exceptions import (
    BadFilenameError,
    BadRuleError,
    MissingValueError,
    NoRulefileError,
    NoRulesError,
    NotIntegerError,
    RulefileNotFoundError,
    SourceEqualsTargetError,
    SourceMatchpatternError,
    UninitializedSourceError,
)
from .run import read_yamlfile_return_yamlstr

# from .run import read_csvfile_return_csvstr
from .utils import return_pyobj_from_yamlstr

fixed = Defaults()

# pylint: disable=bad-continuation
# Black disagrees.


@preserve_cwd
def return_rulefile_pathnames_list(
    startdir_pathname=None,
    rule_csvfile_name=fixed.rule_csvfile_name,
    config_yamlfile_name=fixed.config_yamlfile_name,
):
    """Return chain of rule files leading from parent directories
    to starting directory (by default the current directory).

    Looks no higher than the root directory of a mklists repo, i.e., the
    directory with a YAML configuration file (by default "mklists.yml").

    Args:
        startdir_pathname:
        rule_csvfile_name:
        config_yamlfile_name:
    """
    if not startdir_pathname:
        startdir_pathname = os.getcwd()
    os.chdir(startdir_pathname)
    rulefile_pathnames_chain = []
    while rule_csvfile_name in os.listdir():
        rulefile_pathnames_chain.insert(0, os.path.join(os.getcwd(), rule_csvfile_name))
        if config_yamlfile_name in os.listdir():
            break
        os.chdir(os.pardir)

    return rulefile_pathnames_chain


def return_ruleobj_list_from_pyobj(list_of_lists):
    """Refactor return_ruleobj_list_from_csvfile"""
    pass


def return_ruleobj_list_from_csvfile(filename=None):
    """Return list of Rule objects given CSV string."""
    try:
        csvfile = open(filename, newline="", encoding="utf-8-sig")
    except TypeError:
        raise NoRulefileError(f"No rule file specified.")
    except FileNotFoundError:
        raise NoRulefileError(f"Rule file not found.")

    from csv import DictReader

    csv_obj = DictReader(csvfile)
    csv_ll = [list(dictrow.values()) for dictrow in [dict(row) for row in csv_obj]]

    ruleobj_list = []
    for row in csv_ll:
        single_rule_obj = Rule(*row)
        single_rule_obj.coerce_field_types()
        try:
            if single_rule_obj.is_valid():
                ruleobj_list.append(single_rule_obj)
        except MissingValueError:
            print(f"Skipping badly formed rule: {row}")
        except TypeError:
            raise BadRuleError(f"Rule {repr(row)} is badly formed.")

    if not ruleobj_list:
        raise NoRulesError(f"No rules found.")

    return ruleobj_list


@dataclass
class Rule:
    """Holds state and self-validation methods for a single rule object.

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

    def coerce_field_types(self):
        self.source_matchfield = int(self.source_matchfield)
        self.source_matchpattern = str(self.source_matchpattern)
        self.source = str(self.source)
        self.target = str(self.target)
        self.target_sortorder = int(self.target_sortorder)

    def is_valid(self):
        """Return True if Rule object passes all tests."""
        self._number_fields_are_integers()
        self._source_matchpattern_field_string_is_valid_as_regex()
        self._filename_fields_are_valid()
        self._source_filename_field_is_not_equal_target()
        self._source_filename_field_was_properly_initialized()
        return True

    def _filename_fields_are_valid(self):
        """Returns True if filenames use only valid characters."""
        for filename in [self.source, self.target]:
            if filename is None:
                print(f"{self}")
                raise MissingValueError(
                    f"'None' is not a valid value for 'source' or 'target'."
                )
            if not filename_is_valid_as_filename(filename):
                print(f"{self}")
                raise BadFilenameError(
                    f"'source' and 'target' must be valid filenames."
                )
        return True

    def _number_fields_are_integers(self):
        """Return True if source_matchfield, target_sortorder are integers."""
        for field in [self.source_matchfield, self.target_sortorder]:
            if field is None:
                raise MissingValueError(
                    f"'None' is not a valid value for 'source_matchfield' or 'target_sortorder'."
                )
            if not isinstance(field, int):
                print(f"In {self}:")
                raise NotIntegerError(
                    f"Values for 'source_matchfield' and 'target_sortorder' must be integers."
                )
        return True

    def _source_filename_field_was_properly_initialized(self):
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

    def _source_filename_field_is_not_equal_target(self):
        """Returns True if source is not equal to target."""
        if self.source == self.target:
            print(f"{self}")
            raise SourceEqualsTargetError("source must not equal target.")
        return True

    def _source_matchpattern_field_string_is_valid_as_regex(self):
        """Returns True if source_matchpattern is valid regular expression."""
        if self.source_matchpattern is None:
            raise MissingValueError(
                f"'None' is not a valid value for 'source_matchpattern'."
            )
        if not regex_is_valid_as_regex(self.source_matchpattern):
            print(f"{self}")
            raise SourceMatchpatternError(
                "Value for 'source_matchpattern' must be a valid regex."
            )
        return True
