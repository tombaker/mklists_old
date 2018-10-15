"""Rule module docstring"""

import re
import string
from collections import defaultdict
from dataclasses import dataclass
from mklists import (
    VALID_FILENAME_CHARS,
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
        mklists_dict: 
        * key: always a string that is valid as a filename
        * value: always a list of (part of the) data lines
    """
    mklists_dict = defaultdict(list)
    source_is_initialized = False

    if not rules_list:
        raise NoRulesError("No rules specified.")

    if not datalines_list:
        raise NoDataError("No data specified.")

    # Evaluate rules, one-by-one, to process entries in mklists_dict.
    for rule in rules_list:

        # Initialize dictionary with
        #    first key: 'source' field of first rule (a valid filename)
        #    corresponding value: list of all data lines
        if not source_is_initialized:
            mklists_dict[rule.source] = datalines_list
            source_is_initialized = True

        # Evaluate 'source' lines against rule and move matches to 'target'.
        for line in mklists_dict[rule.source]:
            if _line_matches(matchpattern=rule.source_matchpattern, 
                             matchfield=rule.source_matchfield, 
                             dataline=line):
                mklists_dict[rule.target].extend([line])
                mklists_dict[rule.source].remove([line])

        # Sort matching lines if valid sortorder specified.
        if rule.target_sortorder:
            eth_sortorder = rule.target_sortorder - 1
            decorated = [(line.split()[eth_sortorder], __, line)
                         for (__, line) 
                         in enumerate(mklists_dict[rule.target])]
            decorated.sort()
            mklists_dict[rule.target] = [line for (___, __, line) 
                                        in decorated]

    return mklists_dict


def _line_matches(matchpattern=None, matchfield=None, dataline=None):
    """Returns True if a given field in a data line matches a given pattern."""

    # Line does not match if given field is greater than length of line.
    if matchfield > len(dataline.split()):
        return False

    # Line matches if given field is zero and pattern found anywhere in line.
    if matchfield == 0:
        if re.search(matchpattern, dataline):
            return True

    # Line matches if pattern is found in given field of line.
    if matchfield > 0:
        eth = matchfield - 1
        if re.search(matchpattern, dataline.split()[eth]):
            return True

    return False


@dataclass
class Rule:
    """Holds attributes and self-validation methods for a single rule.

    Attributes:
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

    source_is_initialized = False
    sources = []

    def is_valid(self, valid_filename_characters):
        """Returns True if Rule object passes all tests."""
        self._source_matchfield_and_target_sortorder_are_integers()
        self._source_matchpattern_is_valid()
        self._source_and_target_filenames_are_valid(valid_filename_characters)
        self._source_is_not_equal_target()
        self._source_has_been_initialized()
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

    def _source_has_been_initialized(self):
        """Returns True if source has previously been initialized."""
        if not self.__class__.source_is_initialized:
            self.__class__.sources.append(self.source)
            self.__class__.source_is_initialized = True
        if self.source not in self.__class__.sources:
            print(f"In rule: {self}")
            print(f"self.__class__.sources = {self.__class__.sources}")
            raise BadSourceError(f"{repr(self.source)} not initialized.")
        if self.target not in Rule.sources:
            Rule.sources.append(self.target)
        return True

