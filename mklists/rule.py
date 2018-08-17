"""Rule docstring"""

import re
import string
from dataclasses import dataclass

VALID_FILENAME_CHARS = '@:-_=.{}{}'.format(string.ascii_letters, string.digits)

@dataclass
class Rule:
    """Validates individual rules.

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

    def validate(self):
        """Validates a rule.

        Calls private methods to validate specific aspects.

        Returns:
            True

        Raises:
        """

        self._source_matchfield_is_integer()
        self._target_sortorder_is_integer()
        self._source_matchpattern_is_valid()
        self._source_filename_is_valid()
        self._target_filename_is_valid()
        self._source_is_not_equal_target()
        return self

    def _source_matchfield_is_integer(self):
        """Verifies that source_matchfield is an integer.

        Returns:
            True

        Raises:
            NotIntegerError
        """
        try:
            self.source_matchfield = int(self.source_matchfield)
        except:
            print(f"In rule: {self}")
            print(f"source_matchfield is not an integer")
            raise NotIntegerError
        return True

    def _target_sortorder_is_integer(self):
        """Verifies that target_sortorder is an integer.

        Returns:
            True

        Raises:
            NotIntegerError
        """
        try:
            self.target_sortorder = int(self.target_sortorder)
        except:
            print(f"In rule: {self}")
            print(f"target_sortorder is not an integer")
            raise NotIntegerError
        return True

    def _source_matchpattern_is_valid(self):
        """Confirms that source_matchpattern compiles as regular expression.

        Returns:
            True

        Raises:
            SourceMatchpatternError
        """
        try:
            re.compile(self.source_matchpattern)
        except re.error:
            raise SourceMatchpatternError
        return True

    def _source_filename_is_valid(self):
        """Confirms that source filename uses only valid characters.

        Returns:
            True

        Raises:
            NotValidFilenameError
        """

        for single_character in str(self.source):
            if single_character not in VALID_FILENAME_CHARS:
                print(f"In rule: {self}")
                print(f"filename {self.source} has invalid character(s).")
                print(f"Valid: {VALID_FILENAME_CHARS}")
                raise NotValidFilenameError
        return True

    def _target_filename_is_valid(self):
        """Confirms that target filename uses only valid characters.

        Returns:
            True

        Raises:
            NotValidFilenameError
        """

        for single_character in str(self.target):
            if single_character not in VALID_FILENAME_CHARS:
                print(f"In rule: {self}")
                print(f"filename {self.target} has invalid character(s).")
                print(f"Valid: {VALID_FILENAME_CHARS}")
                raise NotValidFilenameError
        return True

    def _source_is_not_equal_target(self):
        """Confirms that source is not equal to target.

        Returns:
            True

        Raises:
            SourceEqualsTargetError
        """
        if self.source == self.target:
            raise SourceEqualsTargetError
        return True

class RuleError(SystemExit):
    """Super-category for exceptions related to rules."""


class NotIntegerError(RuleError):
    """Value is not an integer."""


class NotValidFilenameError(RuleError):
    """Filename uses character not in list of valid characters."""


class SourceEqualsTargetError(RuleError):
    """Source equals target."""


class SourceMatchpatternError(RuleError):
    """Match pattern does not compile correctly as a regular expression."""
