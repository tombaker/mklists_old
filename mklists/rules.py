"""Rules module

* Initializes, self-tests, and lightly corrects the data object for a
  single rule.
* Applies rules, one by one, to process an aggregated list of datalines.
"""

import re
from collections import defaultdict
from dataclasses import dataclass
from mklists import (
    VALID_FILENAME_CHARS_STR,
    NoDataError,
    NoRulesError,
    NotIntegerError,
    BadFilenameError,
    SourceEqualsTargetError,
    SourceMatchpatternError,
    UninitializedSourceError,
)
from mklists.utils import has_valid_name


def apply_rules_to_datalines(ruleobjs_list=None, datalines_list=None):
    """Applies rules, one by one, to process an aggregated list of datalines.

    Args:
        ruleobjs_list: list of rule objects
        datalines_list: list of strings (all data lines)

    Returns:
        mklists_dict - dictionary where:
        * key: always a string that is valid as a filename
        * value: always a list of (part of the) data lines
    """
    mklists_dict = defaultdict(list)
    first_key_is_initialized = False

    if not ruleobjs_list:
        raise NoRulesError("No rules specified.")

    if not datalines_list:
        raise NoDataError("No data specified.")

    # Evaluate rules, one-by-one, to process entries in mklists_dict.
    for ruleobj in ruleobjs_list:

        # Initialize mklists_dict with first rule.
        #    key: valid filename (from 'source' field of first ruleobj)
        #    value: list of all data lines
        if not first_key_is_initialized:
            mklists_dict[ruleobj.source] = datalines_list
            first_key_is_initialized = True

        # Match lines in 'ruleobj.source' against 'rulesobj.regex'.
        #    append matching lines to value of 'ruleobj.target'
        #    remove matching lines from value of 'ruleobj.source'
        for line in mklists_dict[ruleobj.source]:
            if _line_matches(ruleobj, line):
                mklists_dict[ruleobj.target].extend([line])
                mklists_dict[ruleobj.source].remove(line)

        # Sort 'ruleobj.target' lines by field if sortorder was specified.
        if ruleobj.target_sortorder:
            eth_sortorder = ruleobj.target_sortorder - 1
            decorated = [
                (line.split()[eth_sortorder], __, line)
                for (__, line) in enumerate(mklists_dict[ruleobj.target])
            ]
            decorated.sort()
            mklists_dict[ruleobj.target] = [
                line for (___, __, line) in decorated
            ]

    return dict(mklists_dict)


def _line_matches(given_rule=None, given_line=None):
    """Returns True if data line matches pattern specified in given rule."""

    # Line does not match if given field greater than number of fields in line.
    if given_rule.source_matchfield > len(given_line.split()):
        return False

    # Line matches if given field is zero and pattern found anywhere in line.
    if given_rule.source_matchfield == 0:
        if re.search(given_rule.source_matchpattern, given_line):
            return True

    # Line matches if pattern is found in given field.
    if given_rule.source_matchfield > 0:
        eth = given_rule.source_matchfield - 1
        if re.search(given_rule.source_matchpattern, given_line.split()[eth]):
            return True

    return False


@dataclass
class Rule:
    """Holds fields and self-validation methods for a single rule.

    Dataclass Fields:
        source_matchfield: number of whitespace-delimited field matched
        source_matchpattern: regex for matching to source_matchfield value
        source: string valid as filename (uses valid characters)
        target: string valid as filename (uses valid characters)
        target_sortorder: field on which target value is to be sorted
    """

    source_matchfield: int = None
    source_matchpattern: str = None
    source: str = None
    target: str = None
    target_sortorder: int = 0

    sources_list_is_initialized = False
    sources_list = []

    def is_valid(self):
        """Returns True if Rule object passes all tests.

        * source_matchfield and target_sortorder are integers.
        * source_matchpattern is valid.
        * filenames consist of valid characters and patterns.
        * source does not equal target.
        * every source (except the first) has been previously declared.
        """
        self._number_fields_are_integers()
        self._source_matchpattern_is_valid()
        self._filenames_are_valid()
        self._source_is_not_equal_target()
        self._source_was_properly_registered()
        return True

    def _number_fields_are_integers(self):
        """Returns True if source_matchfield, target_sortorder are integers.
        Silently converts string integers into integers."""
        for field in [self.source_matchfield, self.target_sortorder]:
            if not isinstance(field, int):
                try:
                    field = int(field)
                except:
                    print(f"In rule: {self}")
                    raise NotIntegerError(f"{field} must be an integer.")
        return True

    def _source_matchpattern_is_valid(self):
        """Returns True if source_matchpattern is valid regular expression."""
        try:
            re.compile(self.source_matchpattern)
        except re.error:
            print(f"In rule: {self}")
            raise SourceMatchpatternError(
                f"source_matchpattern is not valid as a regex "
                "-- try escaping metacharacters."
            )
        return True

    def _filenames_are_valid(self):
        """Returns True if filenames use only valid characters.
        TODO Somehow combine this with utils:has_valid_name"""
        for filename in [self.source, self.target]:
            if not has_valid_name(filename):
                print(f"In rule: {self}")
                raise BadFilenameError(
                    f"{repr(filename)} is not a valid filename."
                )
        return True

    def _source_is_not_equal_target(self):
        """Returns True if source is not equal to target."""
        if self.source == self.target:
            raise SourceEqualsTargetError("source must not equal target.")
        return True

    def _source_was_properly_registered(self):
        """Returns True if 'source' filename is registered as a source."""
        if not Rule.sources_list_is_initialized:
            Rule.sources_list.append(self.source)
            Rule.sources_list_is_initialized = True
        if self.source not in Rule.sources_list:
            print(f"In rule: {self}")
            print(f"Rule.sources_list = {Rule.sources_list}")
            raise UninitializedSourceError(
                f"{repr(self.source)} not initialized."
            )
        if self.target not in Rule.sources_list:
            Rule.sources_list.append(self.target)
        return True
