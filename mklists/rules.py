"""Factory to create, self-test, and lightly correct a rule object."""

import csv
import os
from dataclasses import dataclass
from collections import defaultdict
from .booleans import (
    filename_is_valid_as_filename,
    regex_is_valid_as_regex,
    dataline_is_match_to_ruleobj,
)

from .constants import RULES_CSVFILE_NAME, CONFIG_YAMLFILE_NAME
from .decorators import preserve_cwd
from .exceptions import (
    BadFilenameError,
    BadRuleError,
    MissingValueError,
    NoDataError,
    NoRulefileError,
    NoRulesError,
    SourceEqualsTargetError,
    SourceMatchpatternError,
    UninitializedSourceError,
)

# pylint: disable=bad-continuation
# Black disagrees.


def return_list_of_lists_pyobj_from_rules_csvfile(csvfile=None):
    """Return lists of lists, string items stripped, from pipe-delimited CSV file."""
    csv.register_dialect("rules", delimiter="|", quoting=csv.QUOTE_NONE)
    try:
        # encoding 'utf-8-sig' for Excel files with U+FEFF
        # newline '' for MS-Windows '\r\n' line endings
        csvfile_obj = open(csvfile, newline="", encoding="utf-8-sig")
    except FileNotFoundError:
        raise NoRulefileError(f"Rule file not found.")
    except TypeError:
        raise NoRulefileError(f"No rule file specified.")

    rules_parsed_list_raw = list(csv.reader(csvfile_obj, dialect="rules"))
    rules_parsed_list = []
    for single_rule_list in rules_parsed_list_raw:
        single_rule_list_depadded = []
        if len(single_rule_list) > 4:
            for item in single_rule_list:
                single_rule_list_depadded.append(item.strip())
        if single_rule_list_depadded:
            if single_rule_list_depadded[0].isdigit():
                rules_parsed_list.append(single_rule_list_depadded[0:5])
    return rules_parsed_list


def return_names2lines_dict_from_ruleobj_and_dataline_lists(
    _ruleobjs_list=None, _datalines_list=None
):
    """Applies rules, one by one, to process aggregated datalines.

    Args:
        _ruleobjs_list: list of rule objects
        _datalines_list: list of strings (all data lines)

    Returns:
        datadict - dictionary where:
        * key: always a string that is valid as a filename
        * value: always a list of (part of the) data lines
    """
    datadict = defaultdict(list)
    first_key_is_initialized = False

    if not _ruleobjs_list:
        raise NoRulesError("No rules specified.")

    if not _datalines_list:
        raise NoDataError("No data specified.")

    # Evaluate rules, one-by-one, to process entries in datadict.
    for ruleobj in _ruleobjs_list:

        # Initialize datadict with first rule.
        #    key: valid filename (from 'source' field of first ruleobj)
        #    value: list of all data lines
        if not first_key_is_initialized:
            datadict[ruleobj.source] = _datalines_list
            first_key_is_initialized = True

        # Match lines in 'ruleobj.source' against 'rulesobj.regex'.
        #    append matching lines to value of 'ruleobj.target'
        #    remove matching lines from value of 'ruleobj.source'
        for line in datadict[ruleobj.source]:
            if dataline_is_match_to_ruleobj(ruleobj, line):
                datadict[ruleobj.target].extend([line])
                datadict[ruleobj.source].remove(line)

        # Sort 'ruleobj.target' lines by field if sortorder was specified.
        if ruleobj.target_sortorder:
            eth_sortorder = ruleobj.target_sortorder - 1
            decorated = [
                (line.split()[eth_sortorder], __, line)
                for (__, line) in enumerate(datadict[ruleobj.target])
            ]
            decorated.sort()
            datadict[ruleobj.target] = [line for (___, __, line) in decorated]

    return dict(datadict)


@preserve_cwd
def _return_rulefile_pathnames_chain(
    startdir_pathname=None,
    rules_csvfile_name=RULES_CSVFILE_NAME,
    config_yamlfile_name=CONFIG_YAMLFILE_NAME,
):
    """Return chain of rule files leading from parent directories
    to starting directory (default: the current directory).

    Looks no higher than the root directory of a mklists repo, i.e., the
    directory with a YAML configuration file (by default "mklists.yml").

    Args:
        startdir_pathname:
        rules_csvfile_name:
        config_yamlfile_name:
    """
    if not startdir_pathname:
        startdir_pathname = os.getcwd()
    os.chdir(startdir_pathname)
    rulefile_pathnames_list = []
    while rules_csvfile_name in os.listdir():
        rulefile_pathnames_list.insert(0, os.path.join(os.getcwd(), rules_csvfile_name))
        if config_yamlfile_name in os.listdir():
            break
        os.chdir(os.pardir)
    return rulefile_pathnames_list


def _return_ruleobj_list_from_pyobj(pyobj=None):
    """Return list of Rule objects from CSV string."""
    if not pyobj:
        raise NoRulesError(f"No rules list specified.")
    ruleobj_list = []
    # pyobj_filtered = [x for x in pyobj if re.match("[0-9]", x[0])]
    # for item in pyobj_filtered:
    for item in pyobj:
        try:
            if Rule(*item).is_valid():
                ruleobj_list.append(Rule(*item))
        except MissingValueError:
            print(f"Skipping badly formed rule: {item}")
        except ValueError:
            print(f"Value error.")
        except TypeError:
            raise BadRuleError(f"Rule {repr(item)} is badly formed.")
    if not ruleobj_list:
        raise NoRulesError(f"No rules found.")
    return ruleobj_list


def return_one_ruleobj_list_from_rulefile_pathnames_list(rulefile_pathnames_list=None):
    """Return list of Rule objects from pipe-delimited CSV file."""
    one_ruleobj_list = []
    for rulefile_pathname in rulefile_pathnames_list:
        pyobj = return_list_of_lists_pyobj_from_rules_csvfile(rulefile_pathname)
        one_ruleobj_list.append(_return_ruleobj_list_from_pyobj(pyobj))
    return one_ruleobj_list


@dataclass
class Rule:
    """Holds state, transforms, and self-validation methods for a single rule object.

    Fields:
        source_matchfield: data line field to be matched to source_matchpattern.
        source_matchpattern: regex matched to source_matchfield.
        source: filename of source of data lines to be matched to source_matchpattern.
        target: filename of destination of data lines that match source_matchpattern.
        target_sortorder: field on which target data lines are sorted.
        sources_list_is_initialized: when first instantiated, rule object...
        sources_list: for collecting list of declared sources."""

    source_matchfield: int = None
    source_matchpattern: str = None
    source: str = None
    target: str = None
    target_sortorder: int = None
    sources_list_is_initialized = False
    sources_list = []

    def is_valid(self):
        """Return True if Rule object passes all tests."""
        self._coerce_field_types()  # TODO: break this up into coerce_a, coerce_b...
        self._source_matchpattern_field_string_is_valid_as_regex()
        self._filename_fields_are_valid()
        self._source_filename_field_is_not_equal_target()
        self._source_filename_field_was_properly_initialized()
        return True

    def _coerce_field_types(self):
        """Re-assigns dataclass fields coercing correct type (string or integer)."""
        self.source_matchfield = int(self.source_matchfield)
        self.source_matchpattern = str(self.source_matchpattern)
        self.source = str(self.source)
        self.target = str(self.target)
        self.target_sortorder = int(self.target_sortorder)

    def _filename_fields_are_valid(self):
        """Returns True if filenames use only valid characters."""
        for filename in [self.source, self.target]:
            if filename is None:
                print(f"{self}")
                raise MissingValueError(
                    f"'None' is not a valid value for 'source' or 'target'."
                )
            if not filename_is_valid_as_filename(filename):
                print(f"{self}")
                raise BadFilenameError(
                    f"'source' and 'target' must be valid filenames."
                )
        return True

    def _source_filename_field_was_properly_initialized(self):
        """Returns True if 'source' filename was initialized as a source."""
        if not Rule.sources_list_is_initialized:
            Rule.sources_list.append(self.source)
            Rule.sources_list_is_initialized = True
        if self.source not in Rule.sources_list:
            print(f"In rule: {self}")
            print(f"Rule.sources_list = {Rule.sources_list}")
            raise UninitializedSourceError(f"{repr(self.source)} not initialized.")
        if self.target not in Rule.sources_list:
            Rule.sources_list.append(self.target)
        return True

    def _source_filename_field_is_not_equal_target(self):
        """Returns True if source is not equal to target."""
        if self.source == self.target:
            print(f"{self}")
            raise SourceEqualsTargetError("source must not equal target.")
        return True

    def _source_matchpattern_field_string_is_valid_as_regex(self):
        """Returns True if source_matchpattern is valid regular expression."""
        if self.source_matchpattern is None:
            raise MissingValueError(
                f"'None' is not a valid value for 'source_matchpattern'."
            )
        if not regex_is_valid_as_regex(self.source_matchpattern):
            print(f"{self}")
            raise SourceMatchpatternError(
                "Value for 'source_matchpattern' must be a valid regex."
            )
        return True
