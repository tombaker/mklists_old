import pytest
from mklists.rules import *

def test_rules_constant():
    assert print_constant() == "Hello, world!"
