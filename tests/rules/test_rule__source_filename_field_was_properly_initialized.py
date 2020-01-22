"""Rules are listed in a chain where:
* the first rule initializes the 'source' field
* in every subsequent rule, the 'source' must have been
  initialized by a previous rule, either in the initial
  source field or in one of the target fields."""

from mklists.rules import Rule

# pylint: disable=bad-continuation
# Black disagrees.
# pylint: disable=unused-argument
# In tests, fixture arguments may look like they are unused.


def test_rule_source_filename_field_was_properly_initialized_initial_source(
    reinitialize_ruleclass_variables
):
    """The 'source' field in the first rule (here: "a.txt")
    is used to initialize the list of sources."""
    rule_obj = Rule(1, "NOW", "a.txt", "b.txt", 0)
    assert rule_obj._source_filename_field_was_properly_initialized()


def test_rule_source_filename_field_was_properly_initialized_subsequent_source(
    reinitialize_ruleclass_variables
):
    """Once initialized, the list of sources grows with each additional target."""
    rule_obj = Rule(1, "NOW", "lines", "now.txt", 0)
    rule_obj._source_filename_field_was_properly_initialized()
    rule_obj2 = Rule(2, "WORK", "now.txt", "now_work.txt", 0)
    assert rule_obj2._source_filename_field_was_properly_initialized()
