"""Rule module docstring"""

import re
import string
from collections import defaultdict
from dataclasses import dataclass
from mklists import (
    VALID_FILENAME_CHARS,
    NoDataError,
    NoRulesError,
    NotIntegerError,
    BadFilenameError,
    SourceEqualsTargetError,
    SourceMatchpatternError,
    UninitializedSourceError)

def apply_rules_to_datalines(rules_list=None, datalines_list=None):
    """Applies rules, one by one, to process a list of datalines.

    Args:
        rules_list: list of rule objects
        datalines_list: list of all data lines

    Returns:
        mklists_dict - dictionary where:
        * key: always a string that is valid as a filename
        * value: always a list of (part of the) data lines
    """
    mklists_dict = defaultdict(list)
    first_key_is_initialized = False

    if not rules_list:
        raise NoRulesError("No rules specified.")

    if not datalines_list:
        raise NoDataError("No data specified.")

    # Evaluate rules, one-by-one, to process entries in mklists_dict.
    for rule in rules_list:

        # Initialize dictionary with first entry with the first rule:
        #    key: a valid filename (from 'source' field of the first rule)
        #    value: all data lines (consolidated from all files on disk)
        if not first_key_is_initialized:
            mklists_dict[rule.source] = datalines_list
            first_key_is_initialized = True

        # Evaluate 'source' lines against the rule
        #    append matching lines to value of 'rule.target'
        #    remove matching lines from value of 'rule.source'
        for line in mklists_dict[rule.source]:
            if _line_matches(rule, line):
                mklists_dict[rule.target].extend([line])
                mklists_dict[rule.source].remove(line)

        # Sort matching lines by field - if a valid sortorder was specified.
        if rule.target_sortorder:
            eth_sortorder = rule.target_sortorder - 1
            decorated = [(line.split()[eth_sortorder], __, line)
                         for (__, line) 
                         in enumerate(mklists_dict[rule.target])]
            decorated.sort()
            mklists_dict[rule.target] = [line for (___, __, line) 
                                        in decorated]

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
        source_matchpattern: regular expression to be matched
        source: a string valid as a filename
        target: a string valid as a filename
        target_sortorder: field on which target contents are to be sorted
    """
    source_matchfield: int = None
    source_matchpattern: str = None
    source: str = None
    target: str = None
    target_sortorder: int = 0

    sources_list_is_initialized = False
    sources_list = []

    def is_valid(self, valid_filename_characters=VALID_FILENAME_CHARS):
        """Returns True if Rule object passes all tests."""
        self._source_matchfield_and_target_sortorder_are_integers()
        self._source_matchpattern_is_valid()
        self._filenames_are_valid(valid_filename_characters)
        self._source_is_not_equal_target()
        self._source_is_precedented()
        return True

    def _source_matchfield_and_target_sortorder_are_integers(self):
        """Returns True 
        * if source_matchfield and target_sortorder are integers - or
        * if the fields can be silently converted into integers"""
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
                f"source_matchpattern is not valid as a regular expression "
                "-- try escaping metacharacters.")
        return True

    def _filenames_are_valid(self, valid_chars=VALID_FILENAME_CHARS):
        """Returns True if filenames use only valid characters."""
        for field in [self.source, self.target]:
            for char in str(field):
                if char not in valid_chars:
                    print(f"In rule: {self}")
                    raise BadFilenameError(
                        f"{repr(char)} is not a valid filename character.")
        return True

    def _source_is_not_equal_target(self):
        """Returns True if source is not equal to target.
        """
        if self.source == self.target:
            raise SourceEqualsTargetError("source must not equal target.")
        return True

    def _source_is_precedented(self):
        """Checks if source in list of previously registered sources:
        * initializes list of sources from first rule
        * if source is not in list of sources, raise exception and exit
        * if source is in list of sources, add target to list of sources"""
        if not Rule.sources_list_is_initialized:
            Rule.sources_list.append(self.source)
            Rule.sources_list_is_initialized = True
        if self.source not in Rule.sources_list:
            print(f"In rule: {self}")
            print(f"Rule.sources_list = {Rule.sources_list}")
            raise UninitializedSourceError(
                f"{repr(self.source)} not initialized.")
        if self.target not in Rule.sources_list:
            Rule.sources_list.append(self.target)
        return True

