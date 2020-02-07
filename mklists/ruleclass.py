"""Class holding state, transforms, and self-validation methods for rule objects."""

from dataclasses import dataclass
from .booleans import filename_is_valid, regex_is_valid
from .exceptions import (
    BadFilenameError,
    BadRuleError,
    MissingValueError,
    SourceEqualsTargetError,
    SourceMatchpatternError,
    UninitializedSourceError,
)


@dataclass
class Rule:
    """Holds state, transforms, and self-validation methods for a single rule object."""

    source_matchfield: int = None
    source_matchpattern: str = None
    source: str = None
    target: str = None
    target_sortorder: int = None
    sources_list_is_initialized = False
    sources_list = []

    def coerce_types(self):
        """Coerces string integers to real integers."""
        self._coerce_source_matchfield_as_integer()
        self._coerce_target_sortorder_as_integer()
        return self

    def _coerce_source_matchfield_as_integer(self):
        """Coerces source_matchfield to be of type integer."""
        value = self.source_matchfield
        try:
            self.source_matchfield = abs(int(self.source_matchfield))
        except ValueError:
            print(self)
            raise BadRuleError(f"Source matchfield {repr(value)} is not an integer.")

    def _coerce_target_sortorder_as_integer(self):
        """Coerces target_sortorder to be of type integer."""
        value = self.target_sortorder
        try:
            self.target_sortorder = abs(int(self.target_sortorder))
        except ValueError:
            print(self)
            raise BadRuleError(f"Target sortorder {repr(value)} is not an integer.")

    def is_valid(self):
        """Return True if Rule object passes all conversions and tests."""
        self._source_is_valid_filename()
        self._target_is_valid_filename()
        self._source_matchpattern_field_string_is_valid_as_regex()
        self._source_filename_field_is_not_equal_target()
        self._source_filename_field_was_properly_initialized()
        return True

    def _source_is_valid_filename(self):
        """Return source as valid filename as per filename rules."""
        filename = self.source
        if not filename_is_valid(filename):
            raise BadFilenameError(f"{repr(filename)} must be a valid filename.")
        return True

    def _target_is_valid_filename(self):
        """Return target as valid filename as per filename rules."""
        filename = self.target
        if not filename_is_valid(filename):
            raise BadFilenameError(f"{repr(filename)} must be a valid filename.")
        return True

    def _source_filename_field_was_properly_initialized(self):
        """Returns True if 'source' filename was initialized as a source."""
        if not Rule.sources_list_is_initialized:
            Rule.sources_list.append(self.source)
            Rule.sources_list_is_initialized = True
        # print(f"if {self.source} not in {Rule.sources_list}")
        if self.source not in Rule.sources_list:
            # print(f"In rule: {self}")
            # print(f"Rule.sources_list = {Rule.sources_list}")
            raise UninitializedSourceError(f"{repr(self.source)} not initialized.")
        if self.target not in Rule.sources_list:
            Rule.sources_list.append(self.target)
        return True

    def _source_filename_field_is_not_equal_target(self):
        """Returns True if source is not equal to target."""
        if self.source == self.target:
            # print(f"{self}")
            raise SourceEqualsTargetError("source must not equal target.")
        return True

    def _source_matchpattern_field_string_is_valid_as_regex(self):
        """Returns True if source_matchpattern is valid regular expression."""
        if self.source_matchpattern is None:
            raise MissingValueError(
                f"'None' is not a valid value for 'source_matchpattern'."
            )
        if not regex_is_valid(self.source_matchpattern):
            # print(f"{self}")
            raise SourceMatchpatternError(
                "Value for 'source_matchpattern' must be a valid regex."
            )
        return True
