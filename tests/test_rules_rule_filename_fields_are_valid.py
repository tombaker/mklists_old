"""Tests whether filenames (third and fourth components of a rule) are valid is filenames."""

import pytest
from mklists.rules import Rule


def test_rule_filename_fields_are_valid_source_filename_valid():
    """Third field of Rule object ('source') is valid as a filename."""
    rule_instance = Rule(1, "^X 19", "a.txt", "b.txt", 2)
    assert rule_instance._filename_fields_are_valid()


def test_rule_filename_fields_are_valid_target_filename_valid():
    """Fourth field of Rule object ('target') is valid as a filename."""
    rule_instance = Rule(1, "^X 19", "a.txt", "b.txt", 2)
    assert rule_instance._filename_fields_are_valid()


def test_rule_filename_fields_are_valid_target_filename_not_valid():
    """Fourth field of Rule object ('target') not valid, raises SystemExit."""
    rule_instance = Rule(1, "^X 19", "a.txt", "b^.txt", 2)
    with pytest.raises(SystemExit):
        rule_instance._filename_fields_are_valid()


def test_rule_filename_fields_are_valid_filenames_are_not_none():
    """Fourth field of Rule object ('target') not valid, raises SystemExit."""
    rule_instance = Rule(1, "^X 19", None, None, 2)
    with pytest.raises(SystemExit):
        rule_instance._filename_fields_are_valid()


def test_rule_field_source():
    """Third field of Rule object is 'source'."""
    rule_instance = Rule(1, ".", "a", "b", 2)
    assert rule_instance.source == "a"
