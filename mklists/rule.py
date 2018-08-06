import re
import sys
import string
from textwrap import dedent
from dataclasses import dataclass
from typing import List

class NotFiveFieldsError(SystemExit): pass

@dataclass
class Rule:
    source_matchfield: int = None
    source_matchpattern: str = None
    source: str = None
    target: str = None
    target_sortorder: int = 0

    initialized = False
    sources = []

    def has_five_fields(self):
        if len([v for v in self.__dict__.values() if v is not None]) != 5:
            raise NotFiveFieldsError

    def register_source(self):
        """\
        When class is first created, class variables 'initialized' 
        (a flag) and 'sources' (a list) are initialized.

        Note that every time I edit then execute the module, the 
        registry of sources is wiped clean.

        When Rule instantiated for first time: 
        * value of self.target added to 'sources' list
        * value of self.source _also_ added to 'sources' list 
        * 'initialized' flag is set to True

        When Rule is instantiated each subsequent time
        * iff value of self.source is in 'sources' list
          * value of self.target added to 'sources' list
        * iff value of self.source is _not_ in 'sources' list
          * exit with error message

        @@@Todo: create 
        """
        if not Rule.initialized:
            Rule.sources.append(self.source)
            Rule.initialized = True
        if self.source not in Rule.sources:
            print(f"oh no! {self.source} is not in Rule.sources!")
        if self.target not in Rule.sources:
            Rule.sources.append(self.target)
        print(Rule.sources)
