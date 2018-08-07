import re
import sys
import string
from textwrap import dedent
from dataclasses import dataclass
from typing import List

class NotValidFilenameError(SystemExit): pass
class SourceNotRegisteredError(SystemExit): pass

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
