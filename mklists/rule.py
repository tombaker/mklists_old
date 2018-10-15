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
    BadSourceError)

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

        # Initialize dictionary with
        #    first key: 'source' field of first rule (a valid filename)
        #    corresponding value: list of all data lines
        if not first_key_is_initialized:
            mklists_dict[rule.source] = datalines_list
            first_key_is_initialized = True

        # Evaluate 'source' lines against rule and move matches to 'target'.
        # breakpoint()
        for line in mklists_dict[rule.source]:
            if _line_matches(rule, line):
                mklists_dict[rule.target].extend([line])
                mklists_dict[rule.source].remove(line)

        # Sort matching lines if valid sortorder specified.
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
    """Returns True if a given field in a data line matches a given pattern."""

    # Line does not match if given field is greater than length of line.
    if given_rule.source_matchfield > len(given_line.split()):
        return False

    # Line matches if given field is zero and pattern found anywhere in line.
    if given_rule.source_matchfield == 0:
        if re.search(given_rule.source_matchpattern, given_line):
            return True

    # Line matches if pattern is found in given field of line.
    if given_rule.source_matchfield > 0:
        eth = given_rule.source_matchfield - 1
        if re.search(given_rule.source_matchpattern, given_line.split()[eth]):
            return True

    return False


@dataclass
class Rule:
    """Holds attributes and self-validation methods for a single rule.

    Dataclass Fields:
        source_matchfield: @@@@
        source_matchpattern: @@@@
        source: @@@@
        target: @@@@
        target_sortorder: @@@@
    """
    source_matchfield: int = None
    source_matchpattern: str = None
    source: str = None
    target: str = None
    target_sortorder: int = 0

    sources_list_is_initialized = False
    sources_list = []

    # Silently convert strings (x.isdecimal()) into integers.
    try:
        self.source_matchfield = int(self.source_matchfield)
        self.target_sortorder = int(self.target_sortorder)
    except:
        pass 

    def is_valid(self, valid_filename_characters):
        """Returns True if Rule object passes all tests."""
        self._source_matchfield_and_target_sortorder_are_integers()
        self._source_matchpattern_is_valid()
        self._source_and_target_filenames_are_valid(valid_filename_characters)
        self._source_is_not_equal_target()
        self._source_is_precedented()
        return True

    def _source_matchfield_and_target_sortorder_are_integers(self):
        """Returns True if source_matchfield and target_sortorder are integers.
        """
        for field in [self.source_matchfield, self.target_sortorder]:
            if not isinstance(field, int):
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

    def _source_and_target_filenames_are_valid(self, valid_chars):
        """Returns True if filenames use only valid characters."""
        for field in [self.source, self.target]:
            for char in str(field):
                if char not in valid_chars:
                    print(f"In rule: {self}")
                    raise BadFilenameError(f"{repr(char)} is not a valid "
                                            "filename character.")
        return True

    def _source_is_not_equal_target(self):
        """Returns True if source is not equal to target.
        """
        if self.source == self.target:
            raise SourceEqualsTargetError("source must not equal target.")
        return True

    def _source_is_precedented(self):
        """Returns True if source has previously been initialized."""
        if not Rule.sources_list_is_initialized:
            Rule.sources_list.append(self.source)
            Rule.sources_list_is_initialized = True
        if self.source not in Rule.sources_list:
            print(f"In rule: {self}")
            print(f"Rule.sources_list = {Rule.sources_list}")
            raise BadSourceError(f"{repr(self.source)} not initialized.")
        if self.target not in Rule.sources_list:
            Rule.sources_list.append(self.target)
        return True

