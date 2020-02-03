"""Returns dictionary (keys are filenames, values are lists of text lines),
given list of rule objects and list of text lines aggregated from data files."""

import pytest
from mklists.ruleclass import Rule
from mklists.rules import return_names2lines_dict_from_ruleobj_and_dataline_lists

# pylint: disable=expression-not-assigned
# Right, because these are tests...


def test_return_names2lines_dict_correct_result():
    """Returns correct dictionary from good inputs."""
    ruleobjs_list = [Rule(0, "i", "a.txt", "b.txt", 0)]
    datalines_list = ["two ticks\n", "an ant\n", "the mite\n"]
    result_dict = {"a.txt": ["an ant\n"], "b.txt": ["two ticks\n", "the mite\n"]}
    return_names2lines_dict_from_ruleobj_and_dataline_lists(
        _ruleobjs_list=ruleobjs_list, _datalines_list=datalines_list
    ) == result_dict


def test_return_names2lines_dict_another_correct_result():
    """Returns correct dictionary from good inputs."""
    ruleobjs_list = [Rule(2, "i", "a.txt", "b.txt", 1)]
    datalines_list = ["two ticks\n", "an ant\n", "the mite\n"]
    result_dict = {"a.txt": ["an ant\n"], "b.txt": ["the mite\n", "two ticks\n"]}
    return_names2lines_dict_from_ruleobj_and_dataline_lists(
        _ruleobjs_list=ruleobjs_list, _datalines_list=datalines_list
    ) == result_dict


def test_return_names2lines_dict_yet_another_correct_result():
    """Returns correct dictionary from good inputs."""
    ruleobjs_list = [
        Rule(1, "NOW", "a.txt", "now.txt", 0),
        Rule(1, "LATER", "a.txt", "later.txt", 0),
    ]
    datalines_list = ["NOW Summer\n", "LATER Winter\n"]
    result_dict = {
        "now.txt": ["NOW Summer\n"],
        "later.txt": ["LATER Winter\n"],
        "a.txt": [],
    }
    return_names2lines_dict_from_ruleobj_and_dataline_lists(
        _ruleobjs_list=ruleobjs_list, _datalines_list=datalines_list
    ) == result_dict


def test_return_names2lines_dict_correct_result_too():
    """Returns correct dictionary from good inputs."""
    ruleobjs_list = [Rule(1, ".", "a.txt", "now.txt", 1)]
    datalines_list = ["LATER Winter\n", "NOW Summer\n"]
    result_dict = {"now.txt": ["NOW Summer\n", "LATER Winter\n"], "a.txt": []}
    return_names2lines_dict_from_ruleobj_and_dataline_lists(
        _ruleobjs_list=ruleobjs_list, _datalines_list=datalines_list
    ) == result_dict


def test_return_names2lines_dict_no_rules_specified():
    """Exits with error if list of rule objects is not passed as an argument."""
    datalines_list = [["a line\n"]]
    with pytest.raises(SystemExit):
        return_names2lines_dict_from_ruleobj_and_dataline_lists(
            _ruleobjs_list=None, _datalines_list=datalines_list
        )


def test_return_names2lines_dict_no_rules_specified_either():
    """Exits with error if rule objects list passed as argument is empty."""
    ruleobjs_list = []
    datalines_list = ["NOW Summer\n", "LATER Winter\n"]
    with pytest.raises(SystemExit):
        return_names2lines_dict_from_ruleobj_and_dataline_lists(
            _ruleobjs_list=ruleobjs_list, _datalines_list=datalines_list
        )


def test_return_names2lines_dict_no_data_specified():
    """Exits with error no datalines list is passed as argument."""
    ruleobjs_list = [[Rule(1, "a", "b", "c", 2)]]
    with pytest.raises(SystemExit):
        return_names2lines_dict_from_ruleobj_and_dataline_lists(
            _ruleobjs_list=ruleobjs_list, _datalines_list=None
        )


def test_return_names2lines_dict_no_data_specified_either():
    """Exits with error if datalines list passed as argument is empty."""
    ruleobjs_list = [
        Rule(1, "NOW", "a.txt", "now.txt", 0),
        Rule(1, "LATER", "a.txt", "later.txt", 0),
    ]
    datalines_list = []
    with pytest.raises(SystemExit):
        return_names2lines_dict_from_ruleobj_and_dataline_lists(
            _ruleobjs_list=ruleobjs_list, _datalines_list=datalines_list
        )
