import re
import sys
import string
from textwrap import dedent
from dataclasses import dataclass
from typing import List

@dataclass
class Rule:
    source_matchfield: int = None
    source_matchpattern: str = None
    source: str = None
    target: str = None
    target_sortorder: str = None

