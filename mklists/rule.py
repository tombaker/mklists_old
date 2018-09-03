"""Rule module docstring"""

import re
import string
from dataclasses import dataclass
from mklists import (
    VALID_FILENAME_CHARS,
    NotIntegerError,
    BadFilenameError,
    SourceEqualsTargetError,
    SourceMatchpatternError,
    BadSourceError)


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

    initialized = False
    sources = []

    def is_valid(self, valid_filename_characters):
        """Returns True if instance of Rule is valid."""
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
            raise SourceMatchpatternError(f"source_matchpattern is not valid "
                                           "as a regular expression -- "
                                           "try escaping metacharacters.")
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
        if not self.__class__.initialized:
            self.__class__.sources.append(self.source)
            self.__class__.initialized = True
        if self.source not in self.__class__.sources:
            print(f"In rule: {self}")
            print(f"self.__class__.sources = {self.__class__.sources}")
            raise BadSourceError(f"{repr(self.source)} not initialized.")
        if self.target not in Rule.sources:
            Rule.sources.append(self.target)
        return True

