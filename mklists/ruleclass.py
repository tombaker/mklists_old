"""Factory to create, self-test, and lightly correct a rule object."""

import re
from dataclasses import dataclass
from mklists.utils import has_valid_name
from mklists import (
    NotIntegerError,
    BadFilenameError,
    SourceEqualsTargetError,
    SourceMatchpatternError,
    UninitializedSourceError,
)


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
