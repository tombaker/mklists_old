"""Factory to create, self-test, and lightly correct a rule object."""

import csv
import os
import re
from dataclasses import dataclass
from .booleans import filename_is_valid_as_filename, regex_is_valid_as_regex

from .config import RULES_CSVFILE_NAME, CONFIG_YAMLFILE_NAME
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

# pylint: disable=bad-continuation
# Black disagrees.


@preserve_cwd
def _return_rulefile_pathnames_list(
    startdir_pathname=os.getcwd(),
    rules_csvfile_name=RULES_CSVFILE_NAME,
    config_yamlfile_name=CONFIG_YAMLFILE_NAME,
):
    """Return chain of rule files leading from parent directories
    to starting directory (default: the current directory).

    Looks no higher than the root directory of a mklists repo, i.e., the
    directory with a YAML configuration file (by default "mklists.yml").

    Args:
        startdir_pathname:
        rules_csvfile_name:
        config_yamlfile_name:
    """
    os.chdir(startdir_pathname)
    rulefile_pathnames_list = []
    while rules_csvfile_name in os.listdir():
        rulefile_pathnames_list.insert(0, os.path.join(os.getcwd(), rules_csvfile_name))
        if config_yamlfile_name in os.listdir():
            break
        os.chdir(os.pardir)
    return rulefile_pathnames_list


def _return_rules_csvstr_from_rules_csvfile(filename=None):
    """Return string from given pipe-delimited CSV file."""
    try:
        return open(filename, newline="", encoding="utf-8-sig").read()
    except TypeError:
        raise NoRulefileError(f"No rule file specified.")
    except FileNotFoundError:
        raise NoRulefileError(f"Rule file not found.")


def _return_pyobj_from_rules_csvstr(csvstr=None):
    """Return list of lists, each with whitespace-stripped strings,
    given pipe-delimited CSV string."""
    field_names = [
        "source_matchfield",
        "source_matchregex",
        "source",
        "target",
        "target_sortfield",
        "comments",
    ]
    csv_reader = csv.DictReader(
        csvstr, fieldnames=field_names, delimiter="|", quoting=csv.QUOTE_NONE
    )
    pyobj = [list(dictrow.values()) for dictrow in [dict(row) for row in csv_reader]]
    pyobj_stripped = [[item.strip() for item in blist] for blist in pyobj]
    return pyobj_stripped


def _return_ruleobj_list_from_pyobj(pyobj=None):
    """Return list of Rule objects from CSV string."""
    if not pyobj:
        raise NoRulesError(f"No rules list specified.")
    ruleobj_list = []
    pyobj_filtered = [x for x in pyobj if re.match("[0-9]", x[0])]
    for item in pyobj_filtered:
        try:
            if Rule(*item).is_valid():
                ruleobj_list.append(Rule(*item))
        except MissingValueError:
            print(f"Skipping badly formed rule: {item}")
        except TypeError:
            raise BadRuleError(f"Rule {repr(item)} is badly formed.")
    if not ruleobj_list:
        raise NoRulesError(f"No rules found.")
    return ruleobj_list


def return_one_ruleobj_list_from_rulefile_pathnames_list(rulefile_pathnames_list=None):
    """Return list of Rule objects from pipe-delimited CSV file."""
    one_ruleobj_list = []
    for rulefile_pathname in rulefile_pathnames_list:
        csvstring = _return_rules_csvstr_from_rules_csvfile(rulefile_pathname)
        pyobject = _return_pyobj_from_rules_csvstr(csvstring)
        one_ruleobj_list.append(_return_ruleobj_list_from_pyobj(pyobject))
    return one_ruleobj_list


@dataclass
class Rule:
    """Holds state and self-validation methods for a single rule object.

    Fields:
        source_matchfield: data line field to be matched to source_matchpattern.
        source_matchpattern: regex matched to source_matchfield.
        source: filename of source of data lines to be matched to source_matchpattern.
        target: filename of destination of data lines that match source_matchpattern.
        target_sortorder: field on which target data lines are sorted.
        sources_list_is_initialized: when first instantiated, rule object...
        sources_list: for collecting list of declared sources."""

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
