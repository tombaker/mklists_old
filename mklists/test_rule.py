import pytest
from mklists.rule import *

# source_matchfield, source_matchpattern, source, target, target_sortorder

def test_rule():
    x = Rule('1', '.', 'a', 'b', '2')
    assert x.source == 'a'

def test_rulestring_regex_has_space():
    x = Rule('1', '^X 19', 'a', 'b', '2')
    assert x.source_matchpattern == '^X 19'

def test_rulestring_not_enough_fields():
    x = Rule('1', '^X 19', 'a')
    with pytest.raises(SystemExit):
        x.has_five_fields()

#def test_rulestring_field1_is_not_digit():
#def test_rulestring_is_empty():
#def test_rulestring_is_comment_only():
#def test_srules_to_lrules():
#def test_check_lrule_field1_error_exit():
#def test_lrule_backto_srule():
#def test_lrule_backto_srule_one_field_only():
