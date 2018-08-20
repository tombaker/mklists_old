"""Rule docstring"""

import re
import string
from dataclasses import dataclass
from mklists import VALID_FILENAME_CHARS


@dataclass
class Rule:
    """Validates an individual rule.

    Attributes:
        source_matchfield:
        source_matchpattern:
        source:
        target:
        target_sortorder:
    """
    source_matchfield: int = None
    source_matchpattern: str = None
    source: str = None
    target: str = None
    target_sortorder: int = 0

    initialized = False
    sources = []

    def is_valid(self):
        """Returns True if instance of Rule is valid.
        """
        self._source_matchfield_and_target_sortorder_are_integers()
        self._source_matchpattern_is_valid()
        self._source_and_target_filenames_are_valid()
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
            raise SourceMatchpatternError(f"source_matchpattern is not valid.")
        return True

    def _source_and_target_filenames_are_valid(self):
        """Returns True if filenames use only valid characters."""
        for field in [self.source, self.target]:
            for char in str(field):
                if char not in VALID_FILENAME_CHARS:
                    print(f"In rule: {self}")
                    raise BadFilenameError(
                        f"{repr(char)} is not a valid filename character.")
        return True

    def _source_is_not_equal_target(self):
        """Returns True if source is not equal to target.
        """
        if self.source == self.target:
            raise SourceEqualsTargetError("source must not be same as target.")
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


class RuleError(SystemExit):
    """Super-category for exceptions related to rules."""


class NotIntegerError(RuleError):
    """Value is not an integer."""


class BadFilenameError(RuleError):
    """Filename uses character not in list of valid characters."""


class SourceEqualsTargetError(RuleError):
    """Source equals target."""


class SourceMatchpatternError(RuleError):
    """Match pattern does not compile correctly as a regular expression."""

class BadSourceError(RuleError):
    """Source has not been initialized as a source (has no precedent)."""
