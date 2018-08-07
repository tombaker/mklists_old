import re
import sys
import string
from textwrap import dedent
from dataclasses import dataclass
from typing import List

class NotValidFilenameError(SystemExit): 
    pass

class NotDigitError(SystemExit): 
    pass

class SourceNotRegisteredError(SystemExit): 
    pass

class SourceEqualsTargetError(SystemExit): 
    pass

class BadRegexError(SystemExit):
    pass

# Eventually, add check whether set in '.mklistsrc' and, if so, override
VALID_FILENAME_CHARS = '@:-_=.{}{}'.format(string.ascii_letters, string.digits)

@dataclass
class Rule:
    source_matchfield: int = None
    source_matchpattern: str = None
    source: str = None
    target: str = None
    target_sortorder: int = 0

    initialized = False
    sources = []

    def source_matchfield_is_digit(self):
        try:
            self.source_matchfield = int(self.source_matchfield)
        except:
            print(f"In rule: {self}")
            print(f"source_matchfield is not a digit")
            raise NotDigitError
        return True

    def target_sortorder_is_digit(self):
        try:
            self.target_sortorder = int(self.target_sortorder)
        except:
            print(f"In rule: {self}")
            print(f"target_sortorder is not a digit")
            raise NotDigitError
        return True

    def source_matchpattern_is_valid(self):
        try:
            re.compile(self.source_matchpattern)
        except re.error:
            raise BadRegexError
        return True

    def source_filename_valid(self):
        for c in self.source: 
            if c not in VALID_FILENAME_CHARS:
                print(f"In rule: {self}")
                print(f"filename {self.source} has invalid character(s).")
                print(f"Valid: {VALID_FILENAME_CHARS}")
                raise NotValidFilenameError
        return True

    def target_filename_valid(self):
        for c in self.target: 
            if c not in VALID_FILENAME_CHARS:
                print(f"In rule: {self}")
                print(f"filename {self.target} has invalid character(s).")
                print(f"Valid: {VALID_FILENAME_CHARS}")
                raise NotValidFilenameError
        return True

    def source_not_equal_target(self):
        if self.source == self.target:
            raise SourceEqualsTargetError
        return True

    def register_source(self):
        if not Rule.initialized:
            Rule.sources.append(self.source)
            Rule.initialized = True
        if self.source not in Rule.sources:
            print(f"oh no! {self.source} is not in Rule.sources!")
            raise SourceNotRegisteredError
        if self.target not in Rule.sources:
            Rule.sources.append(self.target)
        print(Rule.sources)
